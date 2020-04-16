import requests
from bs4 import BeautifulSoup
import csv

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

def get_detail(detail_num):
    details = []
    for i in range(0, len(detail_num), 5):
        detail = detail_num
        # print(detail)
        detail[0] = detail[0].strip('\n').split('\n')[0]
        details.append(detail)

    return details


if __name__ == '__main__':

    with open("./qiushi.csv", 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(1, 3):
            r = requests.get("https://www.qiushibaike.com/8hr/page/{}/".format(i), headers=headers)
            html = r.text
            soup = BeautifulSoup(html, 'lxml')
            detail_title = soup.select('.recmd-content')
            detail_title = [title.string for title in detail_title]
            print(detail_title)
            # detail_num = soup.find_all('div', class_='recmd-num')
            detail_num = soup.select('.recmd-num')
            detail_num = [num.text for num in detail_num]
            # print(detail_num)
            print(get_detail(detail_num))

            # detail_num = soup.find('div', _class='recmd-num')
            # print(detail_num)
            assert len(detail_title) == len(detail_num)
            for j in range(len(detail_title)):
                writer.writerow(zip([detail_title[j], detail_num[j]]))
