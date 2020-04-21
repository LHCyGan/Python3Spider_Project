#通过ip代理绕过ip反爬
"""
A -----> B
A <----- B
A ---告诉C->C ----> B ---->C ---->A
"""

import requests
from scrapy import Selector


def get_html(url):
    # 代理服务器
    print("开始下载url : {}".format(url))
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "H58G6G30137G865D"
    proxyPass = "043F1F63DA9899C8"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    from fake_useragent import UserAgent
    ua = UserAgent()
    print(ua.random)
    headers = {
        "User-Agent": ua.random
    }

    resp = requests.get(url, proxies=proxies, headers=headers)
    return resp

#1. 随机去ip可能会重复
#2. 用的人太多
#1. 为什么代理可行，在什么情况下ip代理可行()

if __name__ == "__main__":
    for i in range(1, 30):
        job_list_url = "https://www.lagou.com/zhaopin/Python/{}/?filterOption={}".format(i, i)
        job_list_res = get_html(job_list_url)
        job_list_html = job_list_res.content.decode("utf8")
        sel = Selector(text=job_list_html)
        all_lis = sel.xpath(
            "//div[@id='s_position_list']//ul[@class='item_con_list']/li//div[@class='position']//a[1]/@href").extract()
        for url in all_lis:
            success = False
            while 1:
                try:
                    job_res = get_html(url)
                    job_html = job_res.content.decode("utf8")
                    job_sel = Selector(text=job_html)
                    print(job_html)
                    print(job_sel.xpath("//div[@class='job-name']//span[1]/text()").extract()[0])
                except Exception as e:
                    print("下载失败")
                    pass



