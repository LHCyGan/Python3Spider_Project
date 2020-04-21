#socket客户端
import socket
client = socket.socket()
client.connect(('192.168.0.106', 8000))

# client.send(b"bobby")
#当输出完成以后 以#结尾就代码提交完成
# server_data = client.recv(1024)
# print("server response: {}".format(server_data.decode("utf8")))
while True:
    input_data = input()
    client.send(input_data.encode("utf8"))
    server_data = client.recv(1024)
    print("server response: {}".format(server_data.decode("utf8")))

# client.close()
