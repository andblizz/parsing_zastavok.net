import random
import requests
from .settings import USER_AGENTS, PROXIES
import os
import re


def get_html(url, params=None):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    proxy = {'http': random.choice(PROXIES)} if PROXIES else None
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10, proxies=proxy)
        response.encoding = 'utf-8'
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return None


def download_image(pic_url, output_dir):
    try:
        response = requests.get(pic_url, stream=True)
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

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            error_response = requests.get(pic_url)
            print(f"404 Error. Text on the page:\n{error_response.text}")
        else:
            print(f"HTTP Error occurred: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download image from {pic_url}: {e}")
