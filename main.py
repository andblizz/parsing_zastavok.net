from urllib.request import urlretrieve
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import os
import time
import random
from tqdm import tqdm


URL = 'https://zastavok.net/2560x1440/'
HOST = 'https://zastavok.net'
ua = UserAgent()

def get_html(url, params=None):
    r = requests.get(url, headers={'User-Agent': ua.random}, params=params)
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
    exitFlag = False
    pages = int(input('Введите нужное количество страниц: ')) + 1
    for i in range(1+15, pages+1+15):
        html_all_pics = get_html(URL + str(i))
        print(f'Парсинг страницы {html_all_pics.url}...')
        if html_all_pics.ok:
            links = get_links(html_all_pics.text)
        else:
            print('Сайт не отвечает')
        for link in tqdm(links):
            html_link_content = get_html(link)
            if html_link_content.ok:
                pic_link = get_pic(html_link_content.text)
                r = requests.get(pic_link)
                try:
                    d = r.headers['content-disposition']
                except:
                    print('Достигнут лимит скачивания на этом IP.')
                    exitFlag = True
                    break
                file_name = re.findall("filename=(.+)", d)[0].replace('"', '')
                try:
                    os.mkdir('pics/')
                except:
                    pass
                if file_name not in os.listdir(path='pics/'):
                    urlretrieve(pic_link, 'pics/' + file_name)
                    print(f'Изображение {file_name} сохранено успешно.')
                else:
                    print(f'Изображение {file_name} уже было скачано.')
                # time.sleep(random.randint(3, 9))
            else:
                print('Сайт не отвечает')
        if exitFlag:
            break




parsing()