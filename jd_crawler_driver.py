import os
from lxml import etree
import xlwt
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from base_crawler import BaseCrawler

from utils.db import MongoDB
"""
列表：
    p-bookdetails/p-bi-date: 出版日期
详情页：
    class sku-name： 书名
    detail-tag-id-2: 编辑推荐
    detail-tag-id-3: 内容简介
    detail-tag-id-4: 作者简介
    目录，id: detail-tag-id-6、J-detail-content、
"""
XPATH_CONSTANT = {
    "GOODLIST": '//div[@id="J_goodsList"]/ul/li',
    "TITLES": '//div[@id="J_goodsList"]/ul/li//div[@class="p-name"]/a',
    "PRICES": '//div[@id="J_goodsList"]//div[@class="p-price"]/strong/i',
    "AUTHORS": '//div[@id="J_goodsList"]//div/span[@class="p-bi-name"]/a',
    "DATES": '//div[@id="J_goodsList"]/ul/li//div/span[@class="p-bi-date"]',
    "ORGAN": '//div[@id="J_goodsList"]/ul/li//div/span[@class="p-bi-store"]/a',
    "LINKS": '//div[@id="J_goodsList"]//div[@class="p-name"]/a',


}


import codecs
import csv
def write_data(datalist, header, file_name='data.csv'):
    # 指定编码为 utf-8, 避免写 csv 文件出现中文乱码
    with codecs.open(file_name, 'w+', 'utf-8') as csvfile:
        # filednames = ['书名', '页面地址', '图片地址']
        writer = csv.DictWriter(csvfile, fieldnames=header)
        writer.writeheader()
        for data in datalist:
            print(data)

            try:
                writer.writerow({'书名': data, '页面地址': data, '图片地址': data})
            except UnicodeEncodeError:
                print("编码错误, 该数据无法写到文件中, 直接忽略该数据")


class JingDongCrawler(BaseCrawler):
    def __init__(self, driver, save_path=None):
        super(JingDongCrawler, self).__init__(driver, save_path)
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        # self.search_url = 'https://search.jd.com/Search?keyword=英汉口译&page=2'
        # self.detail_url = 'https://item.jd.com/11986338.html'
        self.search_url = 'https://search.jd.com/Search?keyword={}&page={}'
        self.detail_url = 'https://item.jd.com/{}.html'
        self.driver = driver

    def _is_element_exist(self, element='detail-tag-id-6'):
        flag = True
        try:
            self.driver.find_element_by_id(element)
            return flag
        except:
            flag = False
            return flag

    def parse_book_list(self, keyword='英汉口译', page=1):
        """

        :param keyword:
        :param page:
        :return:
        """
        url = self.search_url.format(keyword, str(page))
        try:
            self.driver.get(url)

            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

            time.sleep(2)
            # ⑦向下滑动滚动条到顶部
            self.driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")

            time.sleep(2)
        # driver.find_element_by_xpath('//div[@id="J_goodsList"]/ul//li')

        except TimeoutException:
            print("{} timeout")
        print(url)
        WebDriverWait(self.driver, timeout=60, poll_frequency=5).until(
            EC.presence_of_element_located((By.ID, 'J_goodsList')))
        page_total = self.driver.find_element_by_xpath('//div[@id="J_bottomPage"]/span[@class="p-skip"]/em/b').text
        print("一共{}页".format(page_total))
        print("Crawling: ", url)

        """
        注意： 有些信息不是所有书都提供，比如作者、出版日期
        """
        ids = self.driver.find_elements_by_xpath('//div[@id="J_goodsList"]/ul/li') #[0].get_attribute('data-sku')
        titles = self.driver.find_elements_by_xpath(XPATH_CONSTANT["TITLES"]) #.text
        prices = self.driver.find_elements_by_xpath(XPATH_CONSTANT["PRICES"]) #.text
        # authors = self.driver.find_elements_by_xpath(XPATH_CONSTANT["AUTHORS"]) #/@title get_attribute('title')
        # publish_date = self.driver.find_elements_by_xpath(XPATH_CONSTANT["DATES"])#.get_attribute('innerHTML')#text() #g
        # publish_org = self.driver.find_elements_by_xpath(XPATH_CONSTANT["ORGAN"])#.get_attribute('title')@title
        links = self.driver.find_elements_by_xpath(XPATH_CONSTANT["LINKS"]) #get_attribute('href')
        # print("ids: %s, prices: %s, titles: %s, authors: %s, dates: %s, org: %s, links: %s"%(len(ids),len(prices),len(titles), len(authors), len(publish_date),len(publish_org),len(links)))

        # 将数据写入到文件中
        with open(os.path.join(self.save_path, 'data_{}_{}.csv'.format(keyword, page)), 'w+') as fw:
            for i in range(len(ids)):
                id = ids[i].get_attribute('data-sku')
                title = titles[i].text
                price = prices[i].text
                # author = authors[i].get_attribute('title')
                # org = publish_org[i].get_attribute('title')
                # date = publish_date[i].get_attribute('innerHTML')
                link = links[i].get_attribute('href')
                # fw.write("{}, {}, {}, {}, {}, {},{}\n".format(id, title, price, author, org, date, link))
                # fw.write("{}, {}, {},{}\n".format(id, title, price, link))
                fw.write("{};;;{};;;{};;;{}\n".format(id, title, price, link))

        if page < int(page_total):
            self.parse_book_list(keyword, page+1)

    def _parse_book_detail_by_url(self, detail_url):
        """
        解析书籍详情

        作者: id="p-author"
        简介:
        目录
        :param detail_url:
        :return:
        """
        try:
            self.driver.get(detail_url)
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")
            time.sleep(2)
        except TimeoutException:
            print("{} timeout")
        J_detail_content= WebDriverWait(self.driver, timeout=60, poll_frequency=5).until(
            EC.presence_of_element_located((By.ID, 'J-detail-content')))

        catalog_flag = False # 标记是否有明确目录结构
        # page_total = self.driver.find_element_by_xpath('//div[@id="J_bottomPage"]/span[@class="p-skip"]/em/b').text
        # print("一共{}页".format(page_total))
        print("------Crawling: ", detail_url)
        #  作者
        author = self.driver.find_element_by_id('p-author').text

        if self._is_element_exist():
            catalog_flag = True
            # 内容简介

            summary = self.driver.find_element_by_id('detail-tag-id-3').text

            # 目录
            catalog = self.driver.find_element_by_id('detail-tag-id-6').text
        else:
            summary = ''
            catalog = ''
        return str(author), str(summary), str(catalog)

    def parse_book_detail_by_id(self, bookid):
        url = self.detail_url.format(bookid)
        print(url)
        return self._parse_book_detail_by_url(url)


    def get_book_items(self, csv_path='result/data_汉英口译_1.csv'):
        from utils.book_parse import read_data
        df = read_data(csv_path)


        db = MongoDB()
        db.connect()
        db.connectDB('JDbook', 'detail')
        # # with open(save_path, 'w+') as fw:
        from tqdm import tqdm
        for index, row in tqdm(df.iterrows()):
            author, summary, catalog = self.parse_book_detail_by_id(row['id'])
            db.insert({
                "id": row['id'],
                "author": author,
                "summary": summary,
                "catalog": catalog
            })
            # sheet.write(index, 0, row['id'])
            # sheet.write(index, 1, author)
            # sheet.write(index, 2, summary)
            # sheet.write(index, 3, catalog)
            #
            #
        print("===写入完成")

        ######==== writing to excel
        # save_path = os.path.join(self.save_path, 'detail.xlsx')
        # os.path.exists(save_path)
        # f = xlwt.Workbook()
        # sheet = f.add_sheet("Book_DETAIL")
        #
        # # with open(save_path, 'w+') as fw:
        # for index, row in df.iterrows():
        #     author, summary, catalog = self.parse_book_detail_by_id(row['id'])
        #     sheet.write(index, 0, row['id'])
        #     sheet.write(index, 1, author)
        #     sheet.write(index, 2, summary)
        #     sheet.write(index, 3, catalog)
        #
        # f.save(save_path)
        # print("===保存Excel文件")
    def run(self, keyword):

        # 解析书列表

        # self.parse_book_list(keyword=keyword)


        # 解析单本书详情
        pass