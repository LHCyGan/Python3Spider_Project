import requests
from lxml import etree


headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

def get_comments():
    """获取评论"""
    with open("comments.txt", 'a+', encoding='utf-8') as f:
        for i in range(23):
            url = f"https://movie.douban.com/subject/30488569/reviews?start={20 * i}"
            r = requests.get(url, headers=headers)
            soup = etree.HTML(r.text)
            comments = soup.xpath('//div[@class="main review-item"]//div[@class="main-bd"]/div[@class="review-short"]/div[@class="short-content"]/text()[1]')
            # print(comments)
            for comment in comments:
                comment = comment.strip().replace("\xa0", '').strip('\n').replace('(', '')
                print(comment)
                f.write(comment + "\n")

def get_PiFen():
    """获取评分"""
    with open("PF.txt", 'a+', encoding='utf-8') as f:
        url = "https://movie.douban.com/subject/30488569/"
        r = requests.get(url, headers=headers)
        soup = etree.HTML(r.text)
        PF = soup.xpath('//div[@class="ratings-on-weight"]/div/span[1]/text()')
        people = soup.xpath('//div[@class="ratings-on-weight"]/div/span[2]/text()')
        # print(comments)
        for i, j in zip(PF, people):
            i, j = i.strip(), j.strip()
            print(i, j, sep='\t')
            f.write(i + '\t' + j + "\n")

def get_place():
    session = requests.session()
    session.headers = headers
    login = session.get('https://accounts.douban.com/passport/login')
    cookies = login.cookies
    session.cookies = cookies
    # print(cookies)
    data = {
        'name': 15591730713,
        'password': 'iu111111',
        'remember': 'false'
    }
    sess = session.post("https://accounts.douban.com/j/mobile/login/basic", data=data)
    with open("place.csv", 'w', encoding='utf-8') as f:
        for i in range(23):
            url = f"https://movie.douban.com/subject/30488569/reviews?start={20 * i}"
            r = session.get(url, headers=headers)
            soup = etree.HTML(r.text)
            pepole_hrefs = soup.xpath('//div[@class="article"]/div[1]/div/div/header/a[1]/@href')
            print(pepole_hrefs)
            # print(comments)
            for href in pepole_hrefs:
                res = session.get(href, headers=headers, timeout=20)
                # print(res.text)
                soup_ = etree.HTML(res.text)
                place = soup_.xpath('//*[@id="profile"]/div/div[@class="bd"]/div[@class="basic-info"]/div/a/text()')
                print(place)
                try:
                    if place is not None:
                        f.write(place[0] + '\n')
                except:
                    continue


if __name__ == '__main__':
    get_place()