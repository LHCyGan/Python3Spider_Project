import requests
import re
import json
import datetime
import traceback

today = datetime.date.today().strftime('%Y_%m_%d')


def crawl_dxy_data():
    """
     爬取丁香园实时统计数据，保存到data目录下，以当前日期作为文件名，存JSON文件
    """
    response = requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
    print(response.status_code)
    try:
        response.encoding = response.apparent_encoding
        html = response.text
        # print(html)
        # html = response.content.decode()
        # print(html)
        content = re.search(r'window.getAreaStat = (.*?)}]}catch', html, re.S)
        texts = content.group()
        print(texts)
        # 去除多余字符串
        texts = texts.replace('}catch', '').replace('window.getAreaStat = ', '')
        # 将json解码成python对象
        json_data = json.loads(texts)
        print(json_data)
        with open(today + '.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False)
    except:
        traceback.print_exc()


def crawl_statistics_data():
    """ 获取各个省份历史统计数据，保存到data目录下，存JSON文件 """
    with open(today + '.json', 'r', encoding='utf-8') as f:
        json_data = json.loads(f.read())

    statistics_data = {}
    try:
        for province in json_data:
            response = requests.get(province['statisticsData'])
            statistics_data[province['provinceShortName']] = json.loads(response.content.decode())['data']
    except:
        traceback.print_exc()

    with open('./statistics_data.json', 'w', encoding='utf-8') as f:
        json.dump(statistics_data, f, ensure_ascii=False)


if __name__ == '__main__':
    # crawl_dxy_data()
    crawl_statistics_data()