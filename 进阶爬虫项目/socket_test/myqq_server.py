#qq服务器
#1. 转发消息
#2. 处理登录
#3. 处理退出
#4. 维护历史消息， 维护在线用户和维护用户的连接
import socket
import json
from collections import defaultdict
import threading

#1. 维护用户连接
online_users = defaultdict(dict)

#2. 维护用户的历史消息
user_msgs = defaultdict(list)

server = socket.socket()

#绑定ip
server.bind(("0.0.0.0", 8000))
server.listen()

def handle_sock(sock, addr):
    while True:
        data = sock.recv(1024)
        json_data = json.loads(data.decode("utf8"))
        action = json_data.get("action", "")
        if action == "login":
            online_users[json_data["user"]] = sock
            sock.send("登录成功!".encode("utf8"))
        elif action == "list_user":
            #获取当前在线用户
            all_users = [user for user, sock in online_users.items()]
            sock.send(json.dumps(all_users).encode("utf8"))
        elif action == "history_msg":
            sock.send(json.dumps(user_msgs.get(json_data["user"], [])).encode("utf8"))
        elif action == "send_msg":
            if json_data["to"] in online_users:
                online_users[json_data["to"]].send(json.dumps(json_data).encode("utf8"))
            user_msgs[json_data["to"]].append(json_data)
        elif action == "exit":
            del online_users[json_data["user"]]
            sock.send("退出成功!".encode("utf8"))

while True:
    #阻塞等待连接
    sock, addr = server.accept()
    #启动一个线程去处理新的用户连接
    client_thread = threading.Thread(target=handle_sock, args=(sock, addr))
    client_thread.start()

#1. 多线程去处理每个用户连接，防止主线程阻塞住
#2. 自定义了消息协议并且自己完成了消息协议的解析
