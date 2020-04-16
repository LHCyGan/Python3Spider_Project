from urllib.parse import quote, unquote
import requests
import csv

# https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
# https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false
# https://www.lagou.com/c/approve.json?companyIds=422506%2C348784%2C82991%2C346584%2C173661%2C131339%2C244460%2C82787163%2C917%2C436%2C520478%2C128998%2C111175
# print(unquote('%E7%88%AC%E8%99%AB'))

headers = {
    'Referer': 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}



def save_pos(company, salary):
    writer.writerow([company, salary])

def post_laGou(url, first, page, sid=None):
    url1 = 'https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python'
    data = {
        "first": first,
        'pn': page,
        'kd': 'python爬虫',
        'sid': '622166e2f2e249c08f5e41f542c1537b'}
    # 获取cookies
    res = session.get(url1, headers=headers)
    cookies = res.cookies.get_dict()
    print(cookies)

    r = session.post(url, data=data, headers=headers, cookies=cookies)
    print(r.status_code)
    json_data = r.json()
    print(json_data)
    pos_Content = json_data['content']
    pos_Info = pos_Content['positionResult']['result']
    for pos in pos_Info[:-1]:
        companyName = pos['companyFullName']
        salary = pos['salary']
        print(companyName, salary, sep='\t')
        save_pos(companyName, salary)

if __name__ == '__main__':
    session = requests.session()
    f = open('./lagou.csv', 'w', encoding='utf-8', newline='')
    writer = csv.writer(f)
    writer.writerow(['公司名称', '薪金'])
    url = 'https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false'
    for i in range(1, 10):
        if i == 1:
            post_laGou(url, 'true', i)
        else:
            post_laGou(url, 'false', i)
    f.close()
