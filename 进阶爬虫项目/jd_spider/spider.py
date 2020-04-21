import json

import requests
from scrapy import Selector
#1. 商品的价格

# print(requests.get("https://p.3.cn/prices/mgets?type=1&pdtk=&skuIds=J_7299782&source=item-pc").text)
print(requests.get("https://sclub.jd.com/comment/productPageComments.action?productId=7299782&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1").text)


def parse_good(good_id):
    good_url = "https://item.jd.com/{}.html".format(good_id)
    html = requests.get(good_url).text
    sel = Selector(text=html)
    name = "".join(sel.xpath("//div[@class='sku-name']/text()").extract()[0]).strip()

    #获取商品的价格
    price_url = "https://p.3.cn/prices/mgets?type=1&pdtk=&skuIds=J_{}&source=item-pc".format(good_id)
    price_text = requests.get(price_url).text.strip()

    price_list = json.loads(price_text)
    if price_list:
        price = float(price_list[0]["p"])

    # 获取商品的评价信息
    evaluate_url = "https://sclub.jd.com/comment/productPageComments.action?productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&fold=1".format(good_id, 0)
    evaluate_json = json.loads(requests.get(evaluate_url).text)
    max_page = 0
    max_page = evaluate_json["maxPage"]
    statistics = evaluate_json["hotCommentTagStatistics"]
    summary = evaluate_json["productCommentSummary"]
    evaluates = evaluate_json["comments"]
    pass

if __name__ == "__main__":

    parse_good(7299782)