import string
import random
from argon2 import PasswordHasher
import sympy
from socket import *
from gmpy2 import invert

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

if __name__=='__main__':
    while 1:
        #获得ID
        client = socket(AF_INET, SOCK_STREAM)
        client.connect(('127.0.0.1', 12301))
        ph = PasswordHasher()
        a = 2
        #随机情况
        '''
        up = get_random_uipi(1, 4, 6, 6, 9)
        myhash = ph.hash(up[0])[31:]
        k = myhash[:2]
        h = msg2int([myhash])
        v = pow(h[0], a)
        '''
        #测试泄露情况下的代码

        test_up='xyK88tsD3XBBI3'
        testup_hash=ph.hash(test_up)[54:]
        k = testup_hash[:2]
        h = msg2int([testup_hash])
        v = pow(h[0], a)



        sdata=k+str(v)
        client.send(sdata.encode('utf-8'))
        data=client.recv(65536*16).decode('UTF-8', 'ignore')
        data=eval(data)
        print('=' * 75)
        try:
            if len(data) == 2:
                h_ab = int(data[1])
                h_b = int(pow(h_ab, 0.5))
                print("S=",data[0])
                print('h^b=',h_b)
                if h_b in data[0]:
                    print("查询结果：您的账户信息存在泄露风险")
        except:
            print("查询结果：您的账户信息暂无泄露风险")
        print('=' * 75)
        break
    client.close()
