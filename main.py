import os
import re
import random
from concurrent.futures import ThreadPoolExecutor
import requests
from bs4 import BeautifulSoup

URL = 'https://zastavok.net/2560x1440/'
HOST = 'https://zastavok.net'
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
    " Chrome/91.0.4472.124 Safari/537.36",
]

def get_html(url, params=None):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all('div', class_='short_prev')
    links = [HOST + item.find('a').get('href') for item in all_links]
    return links

def get_pic(html):
    soup = BeautifulSoup(html, 'html.parser')
    try:
        return HOST + soup.find('a', id="orig_size").get('href')
    except AttributeError:
        print("Image link not found.")
        return None

def download_image(pic_url, output_dir):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(pic_url, headers=headers, stream=True)
        response.raise_for_status()
        filename = re.findall("filename=\"(.+?)\"", response.headers.get('content-disposition', ''))
        if not filename:
            filename = os.path.basename(pic_url)
        else:
            filename = filename[0]

        filepath = os.path.join(output_dir, filename)
        if os.path.exists(filepath):
            print(f"Image {filename} already exists.")
            return

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Image {filename} downloaded successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {pic_url}: {e}")

def scrape_images(start_page, end_page, output_dir, max_workers=5):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pic_urls = []
    for page_num in range(start_page, end_page + 1):
        print(f"Fetching page {page_num}...")
        response = get_html(URL + str(page_num))
        if not response:
            print(f"Skipping page {page_num} due to errors.")
            continue

        links = get_links(response.text)
        print(f"Found {len(links)} image page links on page {page_num}.")

        for link in links:
            image_page = get_html(link)
            if image_page:
                pic_url = get_pic(image_page.text)
                if pic_url:
                    pic_urls.append(pic_url)
            else:
                print(f"Skipping image page {link}.")

    print(f"Total images to download: {len(pic_urls)}")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for pic_url in pic_urls:
            futures.append(
                executor.submit(download_image, pic_url, output_dir)
            )
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Task failed with error: {e}")

def main():
    try:
        start_page = int(input("Enter the starting page number: "))
        end_page = int(input("Enter the ending page number: "))
        output_dir = input("Enter the directory to save images (default: 'pics/'): ") or 'pics/'

        print(f"Starting scraping from page {start_page} to {end_page}...")
        scrape_images(start_page, end_page, output_dir)
        print("Scraping completed.")
    except ValueError:
        print("Invalid input. Please enter valid numbers for the page range.")
    except KeyboardInterrupt:
        print("\nScraping interrupted by the user.")

if __name__ == "__main__":
    main()
