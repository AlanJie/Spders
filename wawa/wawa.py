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
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv4822&productId=1263013576&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&fold=1' % page
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
    except Exception as e:
        print('error happens here!')

    print(f'working on page {page}')

    # 获取json数据字符串
    r_json_str = r.text[26:-2]
    # 字符串转json对象
    r_json_obj = json.loads(r_json_str)
    r_json_comments = r_json_obj['comments']
    for r_json_comment in r_json_comments:
        with open(FILE_PATH, 'a+') as f:
            f.write(r_json_comment['content'] + '\n')
        # print(r_json_comment['content'])

def batch_spider_comment():
    if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
    for i in range(2500):
        spdier_comment(i)
        time.sleep(random.random() * 5)



if __name__ == '__main__':
    batch_spider_comment()

