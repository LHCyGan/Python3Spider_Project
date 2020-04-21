import time

from selenium import webdriver
from scrapy import Selector
from selenium.common.exceptions import NoSuchElementException


browser = webdriver.Chrome(executable_path="E:/爬虫0基础入门/chromedriver_win32/chromedriver.exe")
browser.get("https://item.jd.com/7652013.html")

try:
    click_ele = browser.find_element_by_xpath("//li[@clstag='shangpin|keycount|product|shangpinpingjia_1']")
    click_ele.click()
except NoSuchElementException as e:
    pass

sel = Selector(text=browser.page_source)
print(sel.xpath("//span[@class='price J-p-7652013']/text()").extract_first())
browser.close()
