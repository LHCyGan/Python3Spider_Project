import requests

headers = {
    "Host": "ip.zdaye.com",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "http://ip.zdaye.com/",
    "Cookie": "acw_tc=781bad3115549168909987298e35a0462e38b3feef79d4456d6af845f803ff; ASPSESSIONIDSQBBDSTD=LKDPCDNCHNDLEBCCECFHIJGL; __51cke__=; Hm_lvt_8fd158bb3e69c43ab5dd05882cf0b234=1554916892; __tins__16949115=%7B%22sid%22%3A%201554916892021%2C%20%22vd%22%3A%203%2C%20%22expires%22%3A%201554918719960%7D; __51laig__=3; Hm_lpvt_8fd158bb3e69c43ab5dd05882cf0b234=1554916920"
}

res = requests.get("http://ip.zdaye.com/dayProxy/ip/301707.html", headers=headers)
print(res.content.decode("gb2312"))