import socket
import base64
import hashlib
import sys
import time
import threading
from progressbar import *

"""
作者:emb
版权:你觉得呢
创作日期:2020.05.20
"""


#全局变量
worning_level0 = 0
worning_level1 = 0
# worning_level2 = 0
list_msg = []


def prog():
    print('正在上流')
    progress = ProgressBar()
    for i in progress(range(520)):
        time.sleep(0.01)
    return None


def base_msg_decode(msg_bas):
    msg_utf = base64.b64decode(msg_bas)
    msg = msg_utf.decode('UTF-8')
    return msg


def base_msg_encode(msg):
    msg_utf = msg.encode('UTF-8')
    msg_bas = base64.b64encode(msg_utf)
    return msg_bas


def login():
    print('=============上流聊天软件V1.0=============')
    print('''------------------------------------------
    |               使用说明                 |
    | 想使用该软件请先给自己取一个牛皮的名字 |
    | 1 加入聊天:输入聊天室密钥即可加入聊天  |
    | 2 创建聊天:该选项将生成一个聊天室密钥  |
    |  exit 退出程序:关闭牛皮的上流聊天软件  |
    |    加入聊天后可输入menu查看可选菜单    |
    ------------------------------------------''')
    user_name = input('请输入您牛皮的id:')
    print('id设置成功')
    options = input('请输入对应序号并按回车选择选项:')
    if options == '2':
        md5 = hashlib.md5()
        md5.update(user_name.encode('utf-8'))
        passwd = md5.hexdigest()
        print('您的密钥为:')
        print(passwd)
        return (user_name ,passwd)
    elif options == '1':
        passwd = input('请键入上流聊天室密钥')
        return (user_name ,passwd)
    elif options == 'exit':
        sys.exit(1)
    else:
        global worning_level1
        worning_level1 = worning_level1 + 1
        if worning_level1 == 1:
            print('再乱输入你就要出大事了')
            sys.exit(1)


# def out_msg():
#     global list_msg
#     while True:
#         time.sleep(1)
#         msg_one = base_msg_decode(s.recv(1024))
#         msg_two = ''
#         if msg_one.find(msg_two) == -1:
#             print(msg_one)
#             msg_two = msg_one
#         else:
#             pass
#         if worning_level0 == 1:
#             break


def in_msg():
    global list_msg ,msg_num
    while True:
        msg = input('>>>')
        list_msg.append(msg)
        if len(list_msg) == 100:
            list_msg.clear()
            msg_num = 0

    # while True:
    #     msg=input(">>>")
    #     # 发送数据:
    #     s.send(base_msg_encode(msg))
    #     if msg =='exit':
    #         global worning_level0
    #         worning_level0 = 1
    #         break



if __name__ == "__main__":
    key = login()
    print(key)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(type(s))
    # 建立连接:
    s.connect(('119.3.219.105', 9999))
    #接受连接信息
    print(base_msg_decode(s.recv(1024)))
    # 发送密钥和用户名
    s.send(base_msg_encode(str(key)))
    prog()
    msg_in = threading.Thread(target=in_msg)
    msg_in.start()
    msg_num = 0
    while True:
        # msg=input(">>>")
        # 发送数据:
        if len(list_msg) > msg_num:
            s.send(base_msg_encode(list_msg[msg_num]))
            if list_msg[msg_num] =='exit':
                break
            msg_num = msg_num + 1
        else:
            pass
        print(base_msg_decode(s.recv(1024)))
        print('>>>', end='')
    s.send(base_msg_encode('exit'))
    s.close()

