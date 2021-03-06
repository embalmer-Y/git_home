import socket
import threading
import time
import base64
import hashlib
import requests
import random
from random import randint


"""
作者:emb
版权:你觉得呢
创作日期:2020.05.20
"""

# 全局变量
list_key = []
list_name = []
dict_msg = {}
dict_key = {}
xg_bool = False
dict_msg_xg = {}
str_ywz = [' (°ー°〃)', '(#`O′)', '╰(*°▽°*)╯', '(＠_＠;)', '( =•ω•= )m', '(*/ω＼*)', '( ﹁ ﹁ ) ~→']


#上传获得消息内容到图灵机器人
def getMessage(msg):
    apiURL='http://www.tuling123.com/openapi/api'
    data={'key':'5a32cecd47d4457fafc61ee5b404c364',
        'info':msg,
        'userID':'YG'
        }
    r=requests.post(apiURL, data=data).json()
    global str_ywz
    ai_msg = f'{str_ywz[random.randint(0,5)]}：'+r.get('text')
    return ai_msg


def in_out_xg(passwd):
    print("已经连接到雪糕，不想聊了就说句‘滚’把")
    global dict_msg_xg ,dict_msg ,xg_bool
    xg_bool = True
    dict_msg_xg.update({passwd:[]})
    num = len(dict_msg[passwd])
    index_xg = dict_msg[passwd].index('xg' ,num-3)
    while True:
        if len(dict_msg[passwd]) >= index_xg:
            index_xg = index_xg + 1
            if dict_msg[passwd][index_xg] == '滚':
                xg_bool = False
                break
            else:
                dict_msg_xg[passwd].append(getMessage(dict_msg[passwd][index_xg]))
    dict_msg_xg[passwd].append("哭哭，再见")


def key_home(name ,passwd):
    '''
    对全局变量进行操作：
    记录聊天内容输入
    记录聊天室在线成员
    '''
    global list_key ,list_name ,dict_key ,dict_msg
    list_name.append(name)
    if passwd in list_key:
        dict_key[passwd].append(name)
    else:
        list_key.append(passwd)
        dict_key.update({passwd:[name]})
        dict_msg.update({passwd:[]})


def tuple_list(tuple_key):
    '''
    对输入昵称-密钥对进行操作使其返回一个列表
    '''
    str_key = ''
    for i in tuple_key:
        if i == '(' or i == ')' or i == ' ' or i == "'":
            pass
        else:
            str_key = str_key + i
    list_key_in = str_key.split(',',1)
    return list_key_in


def tcplink(sock, addr):
    '''
    接收密钥及分发连接成功信息
    '''
    print('Accept new connection from %s:%s...' % addr)
    sock.send(base_msg_encode('Welcome! connect server successful!'))
    time.sleep(1)
    key = sock.recv(1024)
    name ,passwd = tuple_list(tuple(base_msg_decode(key)))
    key_home(name ,passwd)
    t_in = threading.Thread(target=tcplink_in ,args=(name ,passwd ,sock))
    time.sleep(1)
    t_in.start()
    msg_out(name ,passwd ,sock)
    sock.close()
    global dict_key
    dict_key[passwd].remove(name)
    print('Connection from %s:%s closed.' % addr)


def msg_out(name ,passwd ,sock):
    msg_num = 0
    msg_num_xg = 0
    global dict_msg
    while True:
        for i in dict_msg[passwd][msg_num:]:
            if i[0] != name:
                sock.send(base_msg_encode(f'{i[0]}:{i[1]}'))
                msg_num = msg_num + 1
            else:
                msg_num = msg_num + 1
        if xg_bool:
            for j in dict_msg_xg[passwd]:
                sock.send(base_msg_encode(dict_msg_xg[passwd][msg_num_xg]))
                msg_num_xg = msg_num_xg + 1
        else:
            pass


def tcplink_in(name ,passwd ,sock):
    menu = '''
            menu:
            exit : 退出聊天室
            show : 显示当前聊天室在线人数
            lrs  ：启动狼人杀(完善中)
            xg   ：连接到雪糕
            '''
    while True:
        msg = base_msg_decode(sock.recv(1024))
        time.sleep(1)
        if not msg or msg == 'exit':
            break
        elif msg == 'menu':
            sock.send(base_msg_encode(menu))
        elif msg == 'lrs':
            pass
        elif msg == 'xg':
            xg_link = threading.Thread(target=in_out_xg, args=(passwd,))
            xg_link.start()
        elif msg == 'show':
            global dict_key
            sock.send(base_msg_encode(dict_key[passwd]))
        global dict_msg
        dict_msg[passwd].append((name ,msg))


def base_msg_encode(msg):
    '''
    加密聊天内容
    '''
    msg_utf = msg.encode('UTF-8')
    msg_bas = base64.b64encode(msg_utf)
    return msg_bas


def base_msg_decode(msg_bas):
    '''
    解密聊天内容
    '''
    msg_utf = base64.b64decode(msg_bas)
    msg = msg_utf.decode('UTF-8')
    return msg


if __name__ == "__main__":
    '''
    服务端监听连接并分发新的线程
    '''
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 9999))
    s.listen(10)
    print('Waiting for connection...')
    while True:
        # 接受一个新连接:
        sock, addr = s.accept()
        # 创建新线程来处理TCP连接:
        t_link = threading.Thread(target=tcplink, args=(sock, addr))
        t_link.start()
        for i in dict_key:
            if dict_key[i] == []:
                dict_key.pop(dict_key[i])
                dict_msg.pop(dict_key[i])