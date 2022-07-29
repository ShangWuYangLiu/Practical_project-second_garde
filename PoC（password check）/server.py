from argon2 import PasswordHasher
from socket import *
from socketserver import TCPServer, StreamRequestHandler, ThreadingMixIn
import traceback
import sympy
import random
import string

#为了生成加密安全的随机字符串，使用 random.SystemRandom() 方法，该方法从操作系统的源中生成随机数。
#生成随机的uid
def get_random_strui(number,len_min,len_max):#参数为个数和长度范围
    number_of_strings = number
    ui_list=[]
    for x in range(number_of_strings):
        length_of_string = random.randint(len_min, len_max)
        ui_list.append(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
    return ui_list

#生成随机的password
def get_random_strpi(number,len_min,len_max):
    number_of_strings = number
    pi_list = []
    for x in range(number_of_strings):
        length_of_string = random.randint(len_min, len_max)
        pi_list.append(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
    return pi_list

#将uid和password合并到一块方便哈希
def get_random_uipi(number,len_min1,len_max1,len_min2,len_max2):
    ui=get_random_strui(number,len_min1,len_max1)
    pi = get_random_strpi(number,len_min2,len_max2)
    up_list=[]
    for i in range(number):
        up_list.append(ui[i]+pi[i])
    return up_list

#哈希函数
def myargon2(upi):
    upi_hash=[]
    ph = PasswordHasher()
    for i in range(len(upi)):
        hash = ph.hash(upi[i])
        upi_hash.append(hash[54:])
    return upi_hash

def msg2int(msg):
    msg_int=[]
    for j in msg:
        my_int=0
        count=1
        for i in j:
            temp=ord(i)*count
            count=count+1
            my_int=my_int+temp
        msg_int.append(my_int)
    return msg_int


class MyBaseRequestHandler(StreamRequestHandler):
    def handle(self):
        self.addr = self.request.getpeername()
        self.server.users[self.addr[1]] = self.request
        message = "IP " + self.addr[0] + ":" + str(self.addr[1]) + " Connected..."
        print('='*75)
        print(message)
        while True:
            try:
                number=16
                upi = get_random_uipi(number, 4, 6, 6, 9)
                #测试代码：
                upi[0]='xyK88tsD3XBBI3'
                upi[5]='xyK88tsD3XBBI3'
                upi[2]='xyK88tsD3XBBI3'
                upi[6]='xyK88tsD3XBBI3'
                upi_hash = myargon2(upi)
                hi = msg2int(upi_hash)
                ki = []
                for i in range(len(upi_hash)):
                    ki.append(upi_hash[i][:2])
                vi = []
                b=3
                for i in hi:
                    vi.append(pow(i, b))
                divi_hash_key=list(set(ki))#去掉重复的
                divi_hash_value = []
                for i in ki:
                    temp=[]
                    for j in range(len(ki)):
                        if ki[j]==i:
                            temp.append(vi[j])
                    divi_hash_value.append(temp)
                divi_hash = dict(zip(divi_hash_key, divi_hash_value))
                data = self.request.recv(2048).decode('UTF-8', 'ignore').strip()
                uk=data[:2]
                uv=data[2:]
                uv=int(uv)
                v=pow(uv,b)
                if uk in divi_hash_key:
                    sdata=(divi_hash[uk],str(v))
                    sdata=str(sdata)
                else:
                    sdata=(str(v))
                self.request.sendall(sdata.encode())
                print('finished.')
                print('=' * 75)
                break
            except:
                traceback.print_exc()
                break
# 源码：class ThreadingTCPServer(ThreadingMixIn, TCPServer): pass
# 从ThreadingMixIn和TCPServer继承，实现多线程
class MyThreadingTCPServer(ThreadingMixIn, TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.users = {}

class MyTCPserver():
    def __init__(self, server_addr='127.0.0.1', server_port=12301):
        self.server_address = server_addr
        self.server_port = server_port
        self.server_tuple = (self.server_address, self.server_port)


    def run(self):
    # server = TCPServer(self.server_tuple, MyBaseRequestHandler)
        server = MyThreadingTCPServer(self.server_tuple, MyBaseRequestHandler)
        server.serve_forever()


if __name__ == '__main__':
    myserver = MyTCPserver()
    myserver.run()
