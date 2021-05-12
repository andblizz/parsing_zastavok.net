from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import re

URL = 'https://zastavok.net/1920x1080/'
HOST = 'https://zastavok.net'
ua = UserAgent()
HEADERS = {'User-Agent': ua.random}

def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    r.encoding = 'utf8'
    return r


def get_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    all_links = soup.find_all('div', class_ = 'short_prev')
    links = []
    for item in all_links:
        image_link = item.find('a').get('href')
        links.append(HOST + image_link)
    return links


def get_pic(html):
    soup = BeautifulSoup(html, 'html.parser')
    pic_link = HOST + soup.find('a', id="orig_size").get('href')
    return pic_link


def parsing():
    pages = int(input('Введите нужное количество страниц: ')) + 1
    for i in range(1, pages):
        html_all_pics = get_html(URL + str(i))
        print(f'Парсинг страницы {html_all_pics.url}...')
        if html_all_pics.ok:
            links = get_links(html_all_pics.text)
        else:
            print('Сайт не отвечает')
        for link in links:
            html_link_content = get_html(link)
            if html_link_content.ok:
                pic_link = get_pic(html_link_content.text)
                r = requests.get(pic_link)
                d = r.headers['content-disposition']
                file_name = 'pics/' + re.findall("filename=(.+)", d)[0].replace('"', '')
                urlretrieve(pic_link, file_name)
                print(f'Изображение {file_name} сохранено успешно.')
                time.sleep(3)
            else:
                print('Сайт не отвечает')




parsing()