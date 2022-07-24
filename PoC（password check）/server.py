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
def get_random_strpi(number,len_min,len_max):#参数为个数和长度范围
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
    #参考python关于argon2-cffi使用说明文档
    upi_hash=[]
    ph = PasswordHasher()
    for i in range(len(upi)):
        hash = ph.hash(upi[i])
        upi_hash.append(hash[54:])#截取哈希值
    return upi_hash

#将字符串转换成数字，此处的转换方法为，将字符串的每一个字符转换为十进制数字，然后乘以权重（如第一个字符转换为数字乘1，第二个字符转换为数字乘2，……），最后加和作为某一个字符串对应的数字，这样转换的目的是便于幂运算
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
        print(message)
        while True:
            try:
                #要生成的id+password数目
                number=128
                upi = get_random_uipi(number, 4, 6, 6, 9)#第二个和第三个参数是id的长度范围，第四个和第五个参数是password的长度范围
                #测试代码：
                #upi[0]='xyK88tsD3XBBI3'
                #upi[1]='xyK88tsD3XBBI3'
                #upi[2]='xyK88tsD3XBBI3'
                #upi[3]='xyK88tsD3XBBI3'
                
                #生成hash值
                upi_hash = myargon2(upi)
                #转成数字
                hi = msg2int(upi_hash)
                #生成ki
                ki = []
                for i in range(len(upi_hash)):
                    ki.append(upi_hash[i][:2])
                #tag列表用于分割数据集
                tag=[1]*number
                #字典的键（元素是ki中的）（不重复）
                divi_hash_key = []
                #字典的值（元素是upi_hash中的）
                divi_hash_value = []
                #分割数据集，根据ki进行分割，前两位一样的放到一个集合里
                for i in ki:
                    if ki.count(i) > 1 and tag[ki.index(i)] == 1:
                        temp = []
                        tmp = 0
                        for j in range(0, ki.count(i)):
                            index = ki[tmp:].index(i)
                            temp.append(upi_hash[index + tmp])
                            tag[index + tmp] = 0
                            tmp = index
                        divi_hash_key.append(i)
                        divi_hash_value.append(temp)
                    elif tag[ki.index(i)] == 1:
                        index = ki.index(i)
                        divi_hash_key.append(i)
                        divi_hash_value.append(upi_hash[index])
                #整合成字典
                divi_hash = dict(zip(divi_hash_key, divi_hash_value))
                #生成一个随机素数，服务器端的私钥，为了便于计算生成一个小的素数
                b = sympy.randprime(10 ** 1, 10 ** 2)
                #计算vi
                vi = []
                for i in hi:
                    vi.append(pow(i, b))
                #收到客户发来的（k，v）
                data = self.request.recv(2048).decode('UTF-8', 'ignore').strip()
                uk=data[:2]
                uv=data[2:]
                uv=int(uv)
                v=pow(uv,b)
                #检测客户的id+password是否在服务器端所有的数据库中，若存在，则计算v^b，并且返回用户的k所在的集合和v^b，否则返回一个‘ ’和v^b
                if uk in divi_hash_key:
                    sdata=(divi_hash[uk],str(v))#以元组的方式
                    sdata=str(sdata)
                else:
                    sdata=' '+str(v)
                #发送数据
                self.request.sendall(sdata.encode())
                print('finished.')
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
