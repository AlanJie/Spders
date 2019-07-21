import requests
from bs4 import BeautifulSoup
import re
import os
from requests.exceptions import RequestException
from multiprocessing import Pool
from urllib.parse import urlencode
import random
import time


HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

# 获取索引页面网页内容
def get_page_index(i):
    paras = {
        'nodeids': 25635,
        'pageidx': i
    }
    url = 'https://www.thepaper.cn/load_index.jsp?' + urlencode(paras)

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.text

def parse_page_index(html):
    soup = BeautifulSoup(html, 'lxml')

    num = soup.find_all(name='div', class_='news_li')
    for i in range(len(num)):
        yield{
        # 获取 title
        'title': soup.select('h2 a')[i].get_text(),
        'url': 'https://www.thepaper.cn/' + soup.select('h2 a')[i].attrs['href']
        }

# 获取每条文章的详情页内容
def get_page_detail(item):
    url = item.get('url')

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.text

    except RequestException as e:
        print(f'网页请求失败，错误{e}')
        return None

# 解析每条文章的详情页内容
def parse_page_detail(html):
    soup = BeautifulSoup(html, 'lxml')
    # 获取title
    if soup.h1:  # 有的网页没有 h1 节点，因此必须要增加判断，否则会报错
        # 每个网页只能有一个 h1 标签，因此唯一
        title = soup.h1.get_text()
        items = soup.find_all(name='img', width=['100%', '600'])
        for i in range(len(items)):
            pic = items[i].attrs['src']
            yield{
            'title': title,
            'pic': pic,
            'num': i
            }

def save_pic(pic):
    title = pic.get('title')
    # re.sub(pattern, repl, string, count=0, flags=0)
    # pattern：表示正则表达式中的模式字符串；
    # repl：被替换的字符串（既可以是字符串，也可以是函数）；
    # string：要被处理的，要被替换的字符串；
    # count：匹配的次数, 默认是全部替换
    # flags：具体用处不详
    title = re.sub('[\/:*?"<>|]', '-', title).strip()
    url = pic.get('pic')
    # 设置图片编号顺序
    num = pic.get('num')

    file_dir  = f'pictures\{title}'
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)

    # 获取图片url网页信息
    response = requests.get(url, headers=HEADERS)
    try:
        # 建立图片存放地址
        if response.status_code == 200:
            file_path = f'{file_dir}\{num}.jpg'
        # 文件名采用编号方便按顺序查看，而未采用哈希值 md5(response.content).hexdigest()
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                    print(f'文章"{title}"的第{num}张图片下载完成')
            else:
                print(f'图片{title}已下载')
    except RequestException as e:
        print(f'{e}, 图片获取失败')
        return None

def main(i):
    html = get_page_index(i)
    data = parse_page_index(html)
    for item in data:
        html = get_page_detail(item)
        data = parse_page_detail(html)
        for pic in data:
            save_pic(pic)


# if __name__ == '__main__':
#     for i in range(1, 26):
#         main(i)

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i for i in range(1, 26)])
    pool.close()
    pool.join()

