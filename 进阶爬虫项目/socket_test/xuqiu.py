"""
    需求：
        1. 实现聊天服务器
        2. 实现聊天客户端
    功能：
        1. 登录
        2. 退出
        3. 发送消息
        4. 获取离线消息
        5. 获取在线用户
"""
"""
login  #第一行 接口
to:user #第二行开始 就是额外的字段
from:user

i am bobby #正文内容
"""


#登录
login_template = {
    "action":"login",
    "user":"bobby1"
}
#给某个用户发送消息
send_data_template = {
    "action":"send_msg",
    "to":"user",
    "from":"user",
    "data":"i am bobby"
}
#历史消息
offline_msg_template = {
    "action":"history_msg",
    "user":"user",
}
#获取在线用户
get_user_template = {
    "action":"list_user"
}

#退出
exit_template = {
    "action":"exit",
    "user":""
}