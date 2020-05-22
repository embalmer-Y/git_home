import socket
import threading
import time
import base64
import hashlib

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


def key_home(name ,passwd):
    global list_key ,list_name ,dict_key ,dict_msg
    list_name.append(name)
    if passwd in list_key:
        dict_key[passwd].append(name)
    else:
        list_key.append(passwd)
        dict_key.update({passwd:[name]})
        dict_msg.update({passwd:[]})


def tuple_list(tuple_key):
    str_key = ''
    for i in tuple_key:
        if i == '(' or i == ')' or i == ' ' or i == "'":
            pass
        else:
            str_key = str_key + i
    list_key_in = str_key.split(',',1)
    return list_key_in



def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(base_msg_encode('Welcome! connect server successful!'))
    time.sleep(1)
    key = sock.recv(1024)
    name ,passwd = tuple_list(tuple(base_msg_decode(key)))
    key_home(name ,passwd)
    t_in = threading.Thread(target=tcplink_in ,args=(name ,passwd ,sock))
    t_in.start()
    msg_out(name ,passwd ,sock)
    # while True:
    #     data = sock.recv(1024)
    #     time.sleep(1)
    #     if not data or data.decode('utf-8') == 'exit':
    #         break
    #     print('Client:%s'%data.decode('utf-8'))
    #     sock.send(('Server:%s'% input()).encode('utf-8'))
    sock.close()
    global dict_key
    dict_key[passwd].pop(name)
    print('Connection from %s:%s closed.' % addr)


def msg_out(name ,passwd ,sock):
    # menu = '''
    #         menu:
    #         exit : 退出聊天室
    #         show : 显示当前聊天室在线人数
    #         lrs  ：启动狼人杀(完善中)
    #         xg   ：连接到雪糕(完善中)
    #         '''
    # while True:
    #     msg = base_msg_decode(sock.recv(1024))
    #     time.sleep(1)
    #     if not msg or msg == 'exit':
    #         break
    #     elif msg == 'menu':
    #         sock.send(base_msg_encode(menu))
    #     elif msg == 'lrs':
    #         pass
    #     elif msg == 'xg':
    #         pass
    #     elif msg == 'show':
    #         global dict_key
    #         sock.send(base_msg_encode(dict_key[passwd]))
    #     msg_num = -1
    #     global dict_msg
    #     dict_msg[passwd].append((name ,msg))
        for i in dict_msg[passwd]:
            msg_num = msg_num + 1
            if msg_num != len(dict_msg[passwd]):
                if i[0] != name:
                    sock.send(base_msg_encode(f'{i[0]}:{i[1]}'))



def tcplink_in(name ,passwd ,sock):
    menu = '''
            menu:
            exit : 退出聊天室
            show : 显示当前聊天室在线人数
            lrs  ：启动狼人杀(完善中)
            xg   ：连接到雪糕(完善中)
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
            pass
        elif msg == 'show':
            global dict_key
            sock.send(base_msg_encode(dict_key[passwd]))
        msg_num = -1
        global dict_msg
        dict_msg[passwd].append((name ,msg))


def base_msg_encode(msg):
    msg_utf = msg.encode('UTF-8')
    msg_bas = base64.b64encode(msg_utf)
    return msg_bas


def base_msg_decode(msg_bas):
    msg_utf = base64.b64decode(msg_bas)
    msg = msg_utf.decode('UTF-8')
    return msg


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 3389))
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