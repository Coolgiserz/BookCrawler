from selenium import webdriver
# chromedriver的绝对路径
from lxml import etree
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import TimeoutException
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"

driver_path = r'/Users/zhuge/Softwares/chromedriver/chromedriver90'

chrome_options = Options()
chrome_options.add_argument("blink-settings=imagesEnabled=false")
chrome_options.add_argument('--user-agent=%s' % user_agent)
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)

try:
    # driver.get(
    #     'http://product.dangdang.com/28558528.html')  # driver.find_element_by_id('detail').text 无详情 #driver.find_element_by_id('content').text
    # driver.implicitly_wait(30)
    # driver.get(
    #     'https://item.jd.com/11986338.html')
    driver.get(
        'https://search.jd.com/Search?keyword=英汉口译&page=1')

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")

    time.sleep(2)
      # ⑦向下滑动滚动条到顶部
    driver.execute_script("window.scrollTo(0,-document.body.scrollHeight)")

    time.sleep(2)
#driver.find_element_by_xpath('//div[@id="J_goodsList"]/ul//li')

except TimeoutException:
    print("{} timeout")
element = WebDriverWait(driver, timeout=60, poll_frequency=5).until(
        EC.presence_of_element_located((By.ID, 'J_goodsList')))  # detail出现比content早，要等到content出来
#driver.find_elements_by_xpath('//div[@id="J_goodsList"]/ul//li//div[@class="p-name"]')
# element = WebDriverWait(driver, timeout=60, poll_frequency=5).until(EC.presence_of_element_located((By.ID, 'detail-tag-id-6')))  # detail出现比content早，要等到content出来
print(element)
# print(driver.find_element_by_id('detail').text)
print(driver.find_element_by_id('detail-tag-id-6').text)
print(driver.find_element_by_id('detail-tag-id-3').text)


pass