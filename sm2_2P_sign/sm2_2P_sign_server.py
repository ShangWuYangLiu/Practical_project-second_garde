import socket
import secrets
from new_sm2 import *

def beginAC():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 12345))
    while 1:
        # 1:接收P1
        data, addr = server.recvfrom(1024)
        message = "IP " +addr[0] + ":" + str(addr[1]) + " Connected..."
        print(message)
        data = data.decode()
        index1 = data.index(',')
        P1 = (int(data[:index1]), int(data[index1 + 1:]))

        # 2:生成私钥d，公钥P
        d2 = secrets.randbelow(N)
        tmp = mod_inverse(d2, N)
        tmp = elliptic_mult(tmp, P1)
        P = elliptic_sub(tmp, G)

        # 3:接收Q1，e并计算r，s2，s3发送给客户端
        data, addr = server.recvfrom(1024)
        data = data.decode()
        index1 = data.index(',')
        index2 = data.index('&')
        Q1 = (int(data[:index1]), int(data[index1 + 1:index2]))
        e = data[index2 + 1:]
        e = int(e, 16)
        k2 = secrets.randbelow(N)
        k3 = secrets.randbelow(N)
        Q2 = elliptic_mult(k2, G)
        tmp = elliptic_mult(k3, Q1)
        tmp = elliptic_add(tmp, Q2)
        x1 = tmp[0]
        r = (x1 + e) % N
        if r==0:
            print('error')
            break
        s2 = d2 * k3 % N
        s3 = d2 * (r + k2) % N
        sdata = str(r) + ',' + str(s2) + '&' + str(s3)
        server.sendto(sdata.encode(), addr)

    server.close()


if __name__=="__main__":
    beginAC()
