#socket服务端
import socket
import json
import threading
server = socket.socket()
#绑定到0.0.0.0:8000端口上
server.bind(('0.0.0.0', 8002))
server.listen()

#服务在用户登录成功之后，给用户返回一段字符串sessionid(够复杂，生成算法别人伪造不了)
user_info = {
    "sessionid":"bobby"
}
#浏览器每一次请求(所有的url)都自动带上这个sessionid
#1.如何告知浏览器这个sessionid
#2.如何确保浏览器每一次请求都带上这个sessionid

#session和cookie的区别
#1. session是由服务器维护的，并由服务器解释，通过set-cookie交给浏览器
#2. cookie是浏览器的工具，并在后续的每一次请求中都带上这些值


def handle_sock(sock, addr):
    while True:
        # recv方法是阻塞的
        tmp_data = sock.recv(1024)
        print(tmp_data.decode("utf8"))
        response_template = '''HTTP/1.0 200 OK  
Content-type: text/html  
Set-Cookie: name=bobby
Set-Cookie: course_id=78
Set-Cookie: sessionid=abc123; Expires=Wed, 09 Jun 2021 10:18:14 GMT

{}

'''
        data = [
            {
                "name":"django打造在线教育",
                "teacher":"bobby",
                "url":"https://coding.imooc.com/class/78.html"
            },
            {
                "name": "python高级编程",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/200.html"
            },
            {
                "name": "scrapy分布式爬虫",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/92.html"
            },
            {
                "name": "django rest framework打造生鲜电商",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/131.html"
            },
            {
                "name": "tornado从入门到精通",
                "teacher": "bobby",
                "url": "https://coding.imooc.com/class/290.html"
            },
        ]
        sock.send(response_template.format(json.dumps(data)).encode("utf8"))
        sock.close()
        break

#获取客户端连接并启动线程去处理
while True:
    # 阻塞等待连接
    sock, addr = server.accept()

    #启动一个线程去处理新的用户连接
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()
