import requests
import re
import csv
from bs4 import BeautifulSoup
import time
import random

def get_one_page(url):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text


# 正则表达式版本
# re.S：匹配任意字符，如果不加则无法匹配换行符；
# yield：使用yield的好处是作为生成器，可以遍历迭代，并且将数据整理形成字典，输出结果美观。
# .strip()：用于去掉字符串中的空格。
def parse_one_page(html):
    # 如果不使用re.S参数，则只在每一行内进行匹配，如果一行没有，就换下一行重新开始，不会跨行。而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，将“\n”当做一个普通的字符加入到这个字符串中，在整体中进行匹配。
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
        'index': item[0],
        'thumb': get_thumb(item[1]),
        'name': item[2],
        'star': item[3].strip()[3:],
        'time': get_release_time(item[4].strip()[5:]),
        'area': get_release_area(item[4].strip()[5:]),
        'score': item[5].strip() + item[6].strip()
        }

# find_all(name , attrs , recursive , text , **kwargs)
'''
soup.find_all(name='ul')： 查找所有ul节点，ul 节点内还可以嵌套；
li.string 和 li.get_text()：都是获取li节点的文本，但推荐使用后者；
soup.find_all(attrs={'id': 'list-1'}))：传入 attrs 参数，参数的类型是字典类型，表示查询 id 为 list-1 的节点；
常用的属性比如 id、class 等，可以省略 attrs 采用更简洁的形式，例如：
soup.find_all(id='list-1')
soup.find_all(class_='element')
'''
def parse_one_page_bs(html):
    soup = BeautifulSoup(html,'lxml')
    items = range(10)
    for item in items:
        yield{
            'index': soup.find_all(class_='board-index')[item].string,
            'thumb': soup.find_all(class_ = 'board-img')[item].attrs['data-src'][:-16],
            # 用.get('data-src')获取图片 src 链接，或者用 attrs['data-src']
            'name': soup.find_all(name = 'p',attrs = {'class' : 'name'})[item].string,
            'star': soup.find_all(name = 'p',attrs = {'class':'star'})[item].string.strip()[3:],
            'time': get_release_time(soup.find_all(class_ ='releasetime')[item].string.strip()[5:]),
            'area': get_release_area(soup.find_all(class_ ='releasetime')[item].string.strip()[:]),
            'score':soup.find_all(name = 'i',attrs = {'class':'integer'})[item].string.strip() + soup.find_all(name = 'i',attrs = {'class':'fraction'})[item].string.strip()
        }

# group和groups是两个不同的函数。
# 一般，m.group(N) 返回第N组括号匹配的字符。
# 而m.group() == m.group(0) == 所有匹配的字符，与括号无关，这个是API规定的。
# m.groups() 返回所有括号匹配的字符，以tuple格式。
# m.groups() == (m.group(0), m.group(1), ...)
def get_thumb(url):
    pattern = re.compile(r'(.*?)@.*?')
    thumb = re.search(pattern, url)
    return thumb.group(1)

def get_release_time(data):
    pattern = re.compile(r'(.*?)(\(|$)')
    items = re.search(pattern, data)
    if items is None:
        return '未知'
    return items.group(1)  # 返回匹配到的第一个括号(.*?)中的结果即可

'''
表达式 .* 就是单个字符匹配任意次，即贪婪匹配。 表达式 .*? 是满足条件的情况只匹配一次，即最小匹配.
\s    匹配任何空白非打印字符，包括空格、制表符、换页符等等。等价于 [ \f\n\r\t\v]。注意 Unicode 正则表达式会匹配全角空格符。

\S    匹配任何非空白非打印字符。等价于 [^ \f\n\r\t\v]。

*限定符是贪婪的，因为它们会尽可能多的匹配文字，只有在它们的后面加上一个?就可以实现非贪婪或最小匹配。

比如：<H1>Chapter 1 - 介绍正则表达式</H1>
使用/<.*>/匹配的结果为：H1>Chapter 1 - 介绍正则表达式</H1。
使用/<.*?>/匹配结果为：H1。
'''


def get_release_area(data):
    pattern = re.compile(r'.*\((.*)\)')
    # $表示匹配一行字符串的结尾，这里就是(.*?)；\(|$,表示匹配字符串含有(,或者只有(.*?)
    items = re.search(pattern, data)
    if items is None:
        return '未知'
    return items.group(1)

def download_thumb(name, url, num):
    try:
        response = requests.get(url)
        # 不能使 w ，否则会报错，因为图片是二进制数据所以要用 wb
        with open('covers/' + name + '.jpg', 'wb') as f:
            f.write(response.content)
            print(f'第 {num} 部电影封面下载完毕')
            print('-' * 20)
    except Exception as e:
        print(str(e))
        pass

def write_to_file(item):
    with open('top100.csv', 'a', encoding='utf_8_sig', newline='') as f:
        # utf_8_sig 格式导出 csv 不乱码
        fieldnames = ['index', 'thumb', 'name', 'star', 'time', 'area', 'score']
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writerow(item)

def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for item in parse_one_page_bs(html):
        name = item['name']
        url = item['thumb']
        index = item['index']
        # download_thumb(name, url, index)
        write_to_file(item)

if __name__ == '__main__':
    for i in range(10):
        time.sleep(random.random())
        main(offset=i*10)

