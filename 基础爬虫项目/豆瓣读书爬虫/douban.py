import requests
from bs4 import BeautifulSoup
from urllib import parse
import xlwt
from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(
    'mysql+pymysql://root:123456@127.0.0.1:3306/test?charset=utf8',
    max_overflow=5,
    pool_size=10,
    echo=True
)

class Book(Base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64), nullable=False)
    author = Column(String(128), nullable=False)
    desc = Column(String(256), nullable=False)

Base.metadata.create_all(engine)

# https://book.douban.com/tag/%E7%BC%96%E7%A8%8B?start=20&type=T
# https://book.douban.com/tag/%E7%BC%96%E7%A8%8B?start=40&type=T

headers = {
    "Cookie":'bid=nLUEXUfMlaI; douban-fav-remind=1; ap_v=0,6.0; __utma=30149280.2022309183.1586262130.1586262130.1586262130.1; __utmc=30149280; __utmz=30149280.1586262130.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=81379588.2017833403.1586262130.1586262130.1586262130.1; __utmc=81379588; __utmz=81379588.1586262130.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); gr_user_id=46b8880b-f881-4d4d-be04-08408bf8f895; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=f28dcb08-36ed-4191-a5a7-f26c760b5174; gr_cs1_f28dcb08-36ed-4191-a5a7-f26c760b5174=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_f28dcb08-36ed-4191-a5a7-f26c760b5174=true; __yadk_uid=cwCA7A44TzH5bPRP0tc3SvbmrqfyOq1F; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1586262130%2C%22https%3A%2F%2Fwww.google.com%2F%22%5D; _pk_ses.100001.3ac3=*; _vwo_uuid_v2=D17010DBD55D6C55FF5A1166468E9E2C9|a4edbc470ce3dc5b4564417f2b11d744; viewed="1139336"; __gads=ID=1018b10adcfa7a99:T=1586262165:S=ALNI_MbjPELyldlu-86gD6qx3TujdqxPKg; _pk_id.100001.3ac3=80a49be001e43703.1586262130.1.1586262389.1586262130.; __utmb=30149280.7.10.1586262130; __utmb=81379588.7.10.1586262130',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}


def write_excel(title_list, author_list, desc_list, page):
    zip_ = list(zip(title_list, author_list, desc_list))
    k = 0
    for i in range((page+1)*20,  (page+1)*20+len(title_list)):
        row = int(int(i / 20) - page + k - 1 )
        k += 1
        for j in range(0, 3):
            sheet.write(i, j, zip_[row][j])


def get_content(html, page):
    # print(html)
    titles, authors, desces = [], [], []
    soup = BeautifulSoup(html, 'lxml')
    title_list = soup.select("#subject_list > ul > li > div.info > h2 > a")
    for title in title_list:
        titles.append(title.text)
    author_list = soup.select("#subject_list > ul > li > div.info > div.pub")
    for author in author_list:
        authors.append(author.text)
    desc_list = soup.select("#subject_list > ul > li > div.info > p")
    for desc in desc_list:
        desces.append(desc.text)

    # 写入数据库
    for i in range(len(titles)):
        book = Book(
            title=titles[i],
            author=authors[i],
            desc=desces[i]
        )
        session.add(book)
        session.commit()

    write_excel(titles, authors, desces, page)



def get_html(url):
    try:
        r = requests.get(url, headers=headers)
        r.encoding = r.apparent_encoding
        r.raise_for_status()
        # print("SUCCESSED!")
        return r.text
    except:
        print("ERROR!")



if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    # 创建工作簿
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("豆瓣图书表")
    sheet.write(0, 0, "书名")
    sheet.write(0, 1, "作者、价格和出版社")
    sheet.write(0, 2, "简要描述")
    KEYWORD = input("输入要搜索的图书类：")
    url = "https://book.douban.com/tag/{0}?start={1}&type=T"
    for i in range(0, 10):
        url = url.format(parse.quote(KEYWORD), i * 20)
        html = get_html(url)
        # print(html)
        get_content(html, i)
    workbook.save("./doupan.xls")