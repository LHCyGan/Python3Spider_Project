from selenium import webdriver

browser = webdriver.Chrome('D:\\chromedriver.exe')
browser.get('http://www.baidu.com')

# 案例： 搜索python
input_ = browser.find_element_by_id('kw')
input_.send_keys('python')
submit = browser.find_element_by_id('su')
submit.click()
submit.clear()