import socket

http_client = socket.socket()
http_client.connect(("127.0.0.1", 8000))
http_client.send("""POST /xadmin/ HTTP/1.1
Host: 127.0.0.1:8000
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Referer: http://127.0.0.1:8000/xadmin/
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cookie: csrftoken=xJL5Y8tMXVYVJ5B10Lm1tw7MNfcRIXWWeS3NN7Xy6Yvrl9iVJ46UKH1SvLH6NhuP; sessionid=3rme6xhzumq6o40bnbk2mzv6wtc7tz8s

""".encode("utf8"))
data = b""
while True:
    tmp = http_client.recv(1024)
    if tmp:
        data += tmp
    else:
        break

print(data.decode("utf8"))