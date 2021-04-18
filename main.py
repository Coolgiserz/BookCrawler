from selenium import webdriver
import argparse
# chromedriver的绝对路径
from lxml import etree

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException

from jd_crawler_driver import JingDongCrawler

def init_webdriver():
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
    driver_path = r'/Users/zhuge/Softwares/chromedriver/chromedriver90'
    chrome_options = Options()
    chrome_options.add_argument("blink-settings=imagesEnabled=false")
    chrome_options.add_argument('--user-agent=%s' % user_agent)
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    return driver

def parse_arg():
    parser = argparse.ArgumentParser(description='Book Crawler')
    parser.add_argument('--keyword', type=str, default='口译',
                        help='keyword of the book')
    return parser



if __name__ == '__main__':
    keywords = [
        '英汉口译',
        '汉英口译',

    ]
    args = parse_arg().parse_args()
    driver = init_webdriver()
    crawler = JingDongCrawler(driver=driver, save_path='result_1')
    # crawler.run(args.keyword)
    # crawler.parse_book_detail_by_id(bookid=11986338)#10028101759074，10024078052330,11986338
    import os
    import glob
    lis = glob.glob('result/data_{}*.csv'.format('口译'))
    print("len: ", len(lis))
    sorted_lis = sorted(lis)
    for i in range(49, len(sorted_lis)):
        print('----++++====',i, "-",  sorted_lis[i])
        # crawler.get_book_items(csv_path='result/{}'.format(i))
        crawler.get_book_items(csv_path=sorted_lis[i])


"""
京东图书的目录和简介也不是统一格式的，部分图书目录处源码不同，甚至没有目录

商品每天会更新，部分链接会下架，需要判断哪些还在
"""

