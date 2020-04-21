import json
import pickle

import requests


def login():
    session = requests.session()
    username = "18782902568"
    password = "admin123"
    url = "https://accounts.douban.com/j/mobile/login/basic"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    }

    post_data = {
        "ck": "",
        "name": username,
        "password": password,
        "remember": "true",
        "ticket": ""
    }

    res = session.post(url, data=post_data, headers=headers)
    res_json = json.loads(res.text)
    if res_json["status"] == "success":
        print("登录成功")
        with open("douban.cookie", "wb") as f:
            pickle.dump(res.cookies, f)
    else:
        print("登录失败")

    with open("douban.cookie", "rb") as f:
        cookies = pickle.load(f)
        html = requests.get("https://www.douban.com/", cookies=cookies).text
        if "bobby_liyao" in html:
            print("已经登录")
        else:
            print("未登录")


if __name__ == "__main__":
    login()
