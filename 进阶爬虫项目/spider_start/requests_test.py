import json
import requests

# res = requests.get("http://www.baidu.com")
# print(res.text)
url = "http://127.0.0.1:8000"
params = {
    "username":"bobby",
    "passoword":"bobby"
}
# res = requests.get("http://127.0.0.1:8000", params=params)
#data和json参数都可以传递两种数据类型 1. 字符串 2.dict
res = requests.post(url, data=params)
print(res.encoding)

# res = requests.get("http://www.taobao.com")
# print(res.status_code)

# my_headers = {
#     "user-agent":"requests",
#     "imooc_uid":"321"
# }
# res = requests.get(url, headers=my_headers)
# print(res.headers)

# res = requests.get("https://www.baidu.com")
# print(res.headers)

#浏览器和requests最终都是需要拼接处满足http协议的字符串

