import socket
import secrets
from new_sm2 import *

def beginAC():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('127.0.0.1', 12345))
    while 1:
        # 1:接收P1=(d1^-1)G
        data, addr = server.recvfrom(1024)
        message = "IP " +addr[0] + ":" + str(addr[1]) + " Connected..."
        print(message)
        data = data.decode()
        index1 = data.index(',')
        P1 = (int(data[:index1]), int(data[index1 + 1:]))

        # 2:生成私钥d，公钥P
        d2 = secrets.randbelow(N)
        P = elliptic_sub(elliptic_mult(mod_inverse(d2, N), P1), G)

        # 3:加密msg
        msg="202000460012"
        print("Server端加密的明文为:",msg)
        cipher=sm2_enc(msg,P)

        # 4:发送密文
        sdata=str(cipher)
        server.sendto(sdata.encode(), addr)

        # 5:接收T1，计算T2并发送
        data, addr = server.recvfrom(1024)
        data = data.decode()
        index1 = data.index(',')
        T1 = (int(data[:index1]), int(data[index1 + 1:]))
        T2 = elliptic_mult(mod_inverse(d2, N), T1)
        sdata = str(T2[0]) + ',' + str(T2[1])
        server.sendto(sdata.encode(), addr)
        print("finished.")
    server.close()


if __name__=="__main__":
    beginAC()
