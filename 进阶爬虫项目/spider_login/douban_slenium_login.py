import time

import requests
from selenium import webdriver

url = "https://www.douban.com/"
browser = webdriver.Chrome(executable_path="E:/爬虫0基础入门/chromedriver_win32/chromedriver.exe")


def login():
    #通过selenium模拟登录都豆瓣
    username = "18782902568"
    password = "admin123"
    browser.get(url)
    time.sleep(3)
    browser.switch_to.frame(browser.find_element_by_tag_name("iframe"))
    login_ele = browser.find_element_by_xpath("//li[@class='account-tab-account']")
    login_ele.click()

    username_ele = browser.find_element_by_xpath("//input[@id='username']")
    password_ele = browser.find_element_by_xpath("//input[@id='password']")
    username_ele.send_keys(username)
    password_ele.send_keys(password)

    submit_btn = browser.find_element_by_xpath("//a[@class='btn btn-account btn-active']")
    submit_btn.click()

    time.sleep(10)
    cookies = browser.get_cookies()
    cookie_dict = {}
    for item in cookies:
        cookie_dict[item["name"]] = item["value"]

    res = requests.get(url, cookies=cookie_dict)
    if "bobby_liyao" in res.text:
        print("已经登录")


if __name__ == "__main__":
    login()
