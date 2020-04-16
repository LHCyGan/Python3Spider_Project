import time
import requests
import traceback
from bs4 import BeautifulSoup
import base64
from .PASSWORD import PASSWORD

# 1586045482331
# print(1586045482331)
# print(int(time.time() * 1000))

def save_github(html):
    with open("github.html", "w", encoding='utf8') as f:
        f.write(html)
    print("Saved")

def post_github():
    url = "https://github.com/session"
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Referer": "https: // github.com / login",
    }
    # 获取data中的必要参数
    r = requests.get("https://github.com/login", headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    print(soup.select('#login > form > input[type=hidden]:nth-child(1)')[0].attrs['value'])
    authenticity_token = soup.select('#login > form > input[type=hidden]:nth-child(1)')[0].attrs['value'].strip()
    print(soup.select('#login > form > div.auth-form-body >input:nth-child(9)')[0].attrs['value'])
    timestamp = soup.select('#login > form > div.auth-form-body >input:nth-child(9)')[0].attrs['value'].strip()
    timestamp_sec = soup.select('#login > form > div.auth-form-body >input:nth-child(10)')[0].attrs['value'].strip()

    data = {
        "commit": "Sign in",
        "authenticity_token": authenticity_token,
        "login": "LHCyGan",
        "password": (base64.decodebytes(PASSWORD.encode())).decode(),
        "timestamp": timestamp,
        "timestamp_secret": timestamp_sec
    }
    print(r.cookies.get_dict())
    response = requests.post(url, headers=headers, data=data, cookies=r.cookies.get_dict())
    # print(response.text)

    try:
        if response.status_code == 200:
            print("Post 请求成功！")
            save_github(response.text)
        else:
            print("post 失败，状态码为： {}".format(response.status_code))
    except:
        traceback.print_exc()



if __name__ == '__main__':
    post_github()
