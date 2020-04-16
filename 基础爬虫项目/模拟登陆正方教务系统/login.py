import requests
import pytesseract
from PIL import Image
from lxml import etree
from .INFO import USERNAME, PASSWORD

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

# 获取验证码图片，保存到本地
def get_checkcode():
    img_url = "http://202.200.112.210/CheckCode.aspx"
    r = requests.get(img_url)
    with open("./check.png", 'wb') as f:
        f.write(r.content)

def get_html():
    url = "http://202.200.112.210/Default2.aspx"
    r1 = requests.get(url, headers=headers)
    html1 = r1.content
    soup1 = etree.HTML(html1)
    # 获取必要post请求参数
    __VIEWSTATE = soup1.xpath("//form/input[1]/@value")
    __VIEWSTATEGENERATOR = soup1.xpath("////form/input[2]/@value")
    get_checkcode()
    # 识别验证码
    text = pytesseract.image_to_string(Image.open("./check.png"))
    print(text)

    data = {
        '__VIEWSTATE': __VIEWSTATE,
        '__VIEWSTATEGENERATOR': __VIEWSTATEGENERATOR,
        'txtUserName': USERNAME,
        'TextBox2': PASSWORD,
        'txtSecretCode': text
    }
    r2 = requests.post(url, headers, data=data)
    print(r2.text)

if __name__ == '__main__':
    get_html()

