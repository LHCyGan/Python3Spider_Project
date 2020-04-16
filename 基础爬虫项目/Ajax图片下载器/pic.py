import requests
from urllib.parse import quote
import os
from uuid import uuid4

# https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=iu&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=iu&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn=30&rn=30&gsm=1e&1586004922304=
# https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord=iu&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word=iu&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn=60&rn=30&gsm=3c&1586004925006=

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Referer": "https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=index&fr=&hs=0&xthttps=111111&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8&word=iu&oq=iu&rsp=-1",
    "Cookie": "BDqhfp=iu%26%260-10-1undefined%26%260%26%261; BIDUPSID=51810A34B5AEE2F2BF001999D9E0E112; BAIDUID=CA11608E51AFA1B25749A6EC5B847111:FG=1; PSTM=1579058834; cflag=13%3A3; BDUSS=WRMeVBud0ZUaWRSLTV5WTVFaWgzenRnQUF4VTlydVZUSllhZVlsSEpxdEtOSzFlRUFBQUFBJCQAAAAAAAAAAAEAAAAwhcBNu~C1xMu7w~kAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEqnhV5Kp4VeS; H_PS_PSSID=1427_31120_21095_31186_30908_30824_31086_26350_31164; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=www.baidu.com; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%22iu%22%5D; cleanHistoryStatus=0"
}

session = requests.session()
session.headers = headers

def download(img_url, page, num):
    if not os.path.exists("./images"):
        os.mkdir("./images")
    content = session.get(img_url).content
    with open("./images/{}.jpg".format(uuid4()), 'wb') as f:
        f.write(content)

def get_img_url(url, page):
    html = session.get(url)
    if html.status_code == 200:
        # print("Success...")
        json_data = html.json()
        img_urls = json_data['data']
        for i in img_urls[:-1]:
            img_url = i['middleURL']
            print(img_url)
            download(img_url, page, i)
    else:
        print("Failed...")


if __name__ == '__main__':
    keyword = input("请输入要下载的内容：")
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord={0}" \
          "&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word={0}" \
          "&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&cg=star&pn={1}&rn=30&gsm=1e&1586004922304="
    for i in range(10):
        url = url.format(quote(keyword), i*30)
        get_img_url(url, i)

