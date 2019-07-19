import requests
import pandas as pd
from bs4 import BeautifulSoup
from lxml import etree
import time
import pymysql
from sqlalchemy import create_engine
from urllib.parse import urlencode
from multiprocessing import Pool


start_time = time.time()

def get_one_page(i, date):
    try:
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        paras = {
        'reportTime': date,
        'PageNum': i
        }
        url = 'http://s.askci.com/stock/a/?' + urlencode(paras)
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        print('爬取失败')

def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    # [0]将返回的list改为bs4类型
    content = soup.select('#myTable04')[0]
    # prettify()优化代码（自动格式化）
    # [0]从pd.read_html返回的list中提取出DataFrame
    tb1 = pd.read_html(content.prettify(), header=0)[0]
    tb1.rename(columns={'序号': 'serial_number', '股票代码': 'stock_code',
        '股票简称': 'stock_abbre', '公司名称': 'company_name',
        '省份': 'province', '城市': 'city',
        '主营业务收入(201712)': 'main_bussiness_income',
        '净利润(201712)': 'net_profit', '员工人数': 'employees',
        '上市日期': 'listing_date', '招股书': 'zhaogushu',
        '公司财报': 'financial_report', '行业分类': 'industry_classification',
        '产品类型': 'industry_type', '主营业务': 'main_business'}, inplace=True)
    return tb1


def generate_mysql():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='',
        port=3306,
        charset='utf8',
        db='stocks')
    cursor = conn.cursor()

    sql = 'CREATE TABLE IF NOT EXISTS listed_company (serial_number INT(20) NOT NULL,stock_code INT(20) ,stock_abbre VARCHAR(20) ,company_name VARCHAR(20) ,province VARCHAR(20) ,city VARCHAR(20) ,main_bussiness_income VARCHAR(20) ,net_profit VARCHAR(20) ,employees INT(20) ,listing_date DATETIME(0) ,zhaogushu VARCHAR(20) ,financial_report VARCHAR(20) , industry_classification VARCHAR(20) ,industry_type VARCHAR(100) ,main_business VARCHAR(200) ,PRIMARY KEY (serial_number))'
    cursor.execute(sql)
    conn.close()

def write_to_sql(tbl, db='stocks'):
    engine = create_engine('mysql+pymysql://root:@localhost:3306/{0}?charset=utf8'.format(db))
    try:
        # append 表示在原有基础上增加，但该表要有表头
        tbl.to_sql('listed_company', con=engine, if_exists='append', index=False)
    except Exception as e:
        print(str(e))

def main(page):
    generate_mysql()
    date = '2017-12-31'
    for i in range(1, page):
        html = get_one_page(i, date)
        tbl = parse_one_page(html)
        write_to_sql(tbl)

if __name__ == '__main__':
    pool = Pool(4)
    pool.map(main, [i for i in range(1, 10)])
    time_dur = time.time() - start_time
    print('程序运行了 %.2f 秒' % (time_dur))

