import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

def get_html(page):
    url = f"https://www.oschina.net/news/widgets/_news_index_project_list?p={page}&type=ajax"
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print("Ok!")
        html = r.text
        save_content(html=html)
    else:
        print("Error!")

def save_content(html):
    soup = etree.HTML(html)
    contents = soup.xpath('//div[@class="item news-item"]/div[@class="content"]/h3/a[1]/text()')
    print(contents)
    with open("zixu.txt", 'a+', encoding='utf8') as f:
        for content in contents:
            f.writelines(content + "\n")

if __name__ == '__main__':
    for page in range(1, 5):
        get_html(page)