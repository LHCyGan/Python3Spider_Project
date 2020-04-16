from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from urllib.parse import quote
from pyquery import PyQuery
import time
import csv



def crawl_page(page):
    try:
        url = "https://s.taobao.com/search?q=" + quote(KEYWORD)
        browser.get(url)
        time.sleep(15)

        if page > 1:
            page_box = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div#mainsrp-pager div.form input.input'))
            )
            submit_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#mainsrp-pager div.form >span.btn'))
            )
            page_box.clear()
            page_box.send_keys(page)
            submit_button.click()

        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m-itemlist .items .item'))
        )

        get_product()
    except TimeoutException as t:
        print(t)

def get_product():
    # 获取网页源代码
    html = browser.page_source
    # 解析html
    doc = PyQuery(html)
    # 定位
    items = doc('div.m-itemlist .items .item').items()

    for item in items:
        product = {
            'image': item.find('.pic img').attr('data-src'),
            'price': item.find('.price strong').text(),
            'deal': item.find('.deal-cnt').text(),
            'title': item.find('.title span').text(),
            'location': item.find('.location').text()
        }
        print(product)
        writer.writerow([product['image'],
                         float(product['price']),
                         product['deal'].replace('人付款', ''),
                         product['title'],
                         product['location']])




if __name__ == '__main__':
    KEYWORD = 'IPad'
    browser = webdriver.Chrome('D:\\chromedriver.exe')
    # 设置延迟时间
    wait = WebDriverWait(browser, 10)

    f = open('./ipad.csv', 'w', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(['image', 'price', 'deal', 'title', 'location'])


    for i in range(5):
        crawl_page(i)
    f.close()