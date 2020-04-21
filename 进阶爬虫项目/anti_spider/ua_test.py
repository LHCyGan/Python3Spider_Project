import requests
from fake_useragent import UserAgent


ua = UserAgent()
headers = {
    "User-Agent": ua.random
}
res = requests.get("http://127.0.0.1", headers=headers)
print(res.text)