import os
import random
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from .utils import get_html, download_image
from .settings import HOST, URL, DELAY_RANGE, MAX_WORKERS
from bs4 import BeautifulSoup


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


def scrape_images(start_page, end_page, output_dir):
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
            sleep(random.uniform(*DELAY_RANGE))
            image_page = get_html(link)
            if image_page:
                pic_url = get_pic(image_page.text)
                if pic_url:
                    pic_urls.append(pic_url)
            else:
                print(f"Skipping image page {link}.")

    print(f"Total images to download: {len(pic_urls)}")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for pic_url in pic_urls:
            executor.submit(download_image, pic_url, output_dir)
