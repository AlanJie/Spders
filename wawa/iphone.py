import requests
import json
import os
import random
import time


FILE_PATH = 'D:\Sublime\workspace\Spiders\wawa\comments.txt'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Referer': 'https://item.jd.com/1263013576.html'
}

def spdier_comment(page=0):
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv10253&productId=100000287113&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % page
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print('error happens here!')


    # 获取json数据字符串
    r_json_str = r.text[27:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    r_json_comments = r_json_obj['comments']
    for r_json_comment in r_json_comments:
        with open(FILE_PATH, 'a+') as f:
            content = r_json_comment['content'].encode('utf-8')
            content = content.strip()
            f.write(content.decode('utf-8') + '\n')
        # print(r_json_comment['content'])

def batch_spider_comment():
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
    for i in range(100):
        print(f'working on page {i}')
        spdier_comment(i)
        time.sleep(random.random() * 5)



if __name__ == '__main__':
    batch_spider_comment()

