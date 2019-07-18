import requests
import threading
from multiprocessing import cpu_count, Pool
from bs4 import BeautifulSoup
import re
import time
import random
import os


DIR_PATH = r"D:\Sublime\workspace\Spiders\wallpapers\wallpapers"

HEADERS = {
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Referer': 'www.win4000.com'
}

def get_urls():
    page_urls = ['http://www.win4000.com/zt/meinv_{cnt}.html'.format(cnt=cnt) for cnt in range(2, 6)]
    img_urls = []
    for page_url in page_urls:
        try:
            time.sleep(random.random() * 2)
            bs = BeautifulSoup(
                requests.get(page_url, headers=HEADERS, timeout=10).text,
                'lxml').find('div', class_='tab_box').find('ul', class_='clearfix')
            result = re.findall(r'(?<=href=)\S+', str(bs))
            img_url = [url.replace('"', "") for url in result]
            img_urls.extend(img_url)
        except Exception as e:
            print(str(e))
    return set(img_urls)

lock = threading.Lock()

def urls_crawler(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=10).text
        folder_name = BeautifulSoup(r, 'lxml').find(
            'div', class_='pic-meinv').find('img')['alt']
        with lock:
            if make_dir(folder_name):
                max_count = BeautifulSoup(r, 'lxml').find(
                    'div', class_='Bigimg').find('div', class_='ptitle').find(
                    'em').get_text()
                page_urls = [url[:-5] + '_' + str(i) + '.html' for i in range(1, int(max_count) + 1)]
                img_urls = []

                for _, page_url in enumerate(page_urls):
                    time.sleep(random.random())
                    result = requests.get(page_url, headers=HEADERS, timeout=10).text
                    img_url = BeautifulSoup(result, 'lxml').find(
                        'div', class_='pic-meinv').find('img', class_='pic-large')['src']
                    img_urls.append(img_url)
                for cnt, url in enumerate(img_urls):
                    save_pic(url, cnt)
    except Exception as e:
        print(str(e))

def save_pic(pic_src, pic_cnt):
    try:
        time.sleep(random.random())
        img = requests.get(pic_src, headers=HEADERS, timeout=10)
        img_name = "pic_cnt_{}.jpg".format(pic_cnt + 1)
        with open(img_name, 'ab') as f:
            f.write(img.content)
            print(f'save picture: {img_name}')
    except Exception as e:
        print(str(e))

def make_dir(folder_name):
    path = os.path.join(DIR_PATH, folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print('Folder already exists!')
    return False

if __name__ == '__main__':
    urls = get_urls()
    pool = Pool(processes=cpu_count())
    try:
        pool.map(urls_crawler, urls)
    except Exception:
        time.sleep(random.random() * 2)
        pool.map(urls_crawler, urls)

