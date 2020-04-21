#qq客户端
import socket
import json
import threading

client = socket.socket()
client.connect(("127.0.0.1", 8000))

user = "bobby3"

#1. 登录
login_template = {
    "action":"login",
    "user":user
}
client.send(json.dumps(login_template).encode("utf8"))
res = client.recv(1024)
print(res.decode("utf8"))

#2. 获取在线用户
get_user_template = {
    "action":"list_user"
}
client.send(json.dumps(get_user_template).encode("utf8"))
res = client.recv(1024)
print("当前在线用户:{}".format(res.decode("utf8")))

#2. 获取历史消息
offline_msg_template = {
    "action":"history_msg",
    "user":user
}
client.send(json.dumps(offline_msg_template).encode("utf8"))
res = client.recv(1024)
print("历史消息:{}".format(res.decode("utf8")))

exit = False
def hanle_receive():
    #处理接收请求
    while True:
        if not exit:
            try:
                res = client.recv(1024)
            except:
                break
            res = res.decode("utf8")
            try:
                res_json = json.loads(res)
                msg = res_json["data"]
                from_user = res_json["from"]
                print("")
                print("收到来自({})的消息: {}".format(from_user, msg))
            except:
                print("")
                print(res)
        else:
            break

def handle_send():
    while True:
        #1. 随时可以发送消息
        #2. 有新消息随时能接收到
        op_type = input("请输入你要进行的操作: 1. 发送消息, 2. 退出, 3. 获取在线用户")
        if op_type not in ["1","2","3"]:
            print("不支持该操作!!!")
            op_type = input("请输入你要进行的操作: 1. 发送消息, 2. 退出, 3. 获取在线用户")
        elif op_type == "1":
            to_user = input("请输入你要发送的用户:")
            msg = input("请输入你要发送的消息")
            send_data_template = {
                "action": "send_msg",
                "to": to_user,
                "from": user,
                "data": msg
            }
            client.send(json.dumps(send_data_template).encode("utf8"))
        elif op_type == "2":
            exit_template = {
                "action": "exit",
                "user": user
            }
            client.send(json.dumps(exit_template).encode("utf8"))
            exit = True
            client.close()
            break
        elif op_type == "3":
            get_user_template = {
                "action": "list_user"
            }
            client.send(json.dumps(get_user_template).encode("utf8"))

if __name__ == "__main__":
    send_thread = threading.Thread(target=handle_send)
    receive_thread = threading.Thread(target=hanle_receive)
    send_thread.start()
    receive_thread.start()




