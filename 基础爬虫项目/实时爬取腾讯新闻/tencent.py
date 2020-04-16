import requests
import json
import datetime

today = datetime.date.today().strftime("%Y_%m_%d")


headers = {
        "referer": "https://news.qq.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


def get_html():
    url1 = "https://news.qq.com/"
    url2 = "https://news.qq.com/ext2020/apub/json/prevent.new.json"
    # 获取cookies
    cookies = requests.get(url1, headers=headers).cookies.get_dict()
    response = requests.get(url2, headers=headers)
    # news_data = json.loads(response.text)
    news_data = response.json()
    save_news(news_data)


def save_news(news_data):
    with open("./{}_news.txt".format(today), "a+", encoding='utf-8') as f:
        for i, news in enumerate(news_data):
            f.write(str(i) + "、" + "\t" + news['title'] + '\n')


if __name__ == '__main__':
    # save_news()
    get_html()