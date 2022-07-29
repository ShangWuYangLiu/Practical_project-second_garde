import socket
from new_sm2 import *
import secrets
from gmssl import sm3, func

def beginAC():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 1:生成私钥d1和P1,向服务器发送P1
    d1 = secrets.randbelow(N)
    P1 = elliptic_mult(mod_inverse(d1, N),G)
    sdata = str(P1[0]) + ',' + str(P1[1])
    client.sendto(sdata.encode(), ("127.0.0.1", 12345))

    # 2:计算Q、e并发送给服务器
    myID='client'
    hisID='server'
    Z=myID+hisID
    M='202000460012'
    M_=Z+M
    M_b = bytes(M_, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(M_b))
    k1 = secrets.randbelow(N)
    Q1 = elliptic_mult(k1, G)
    sdata = str(Q1[0]) + ',' + str(Q1[1]) + '&' + e
    client.sendto(sdata.encode(), ("127.0.0.1", 12345))

    # 3:接收r，s2，s3并计算(r,s)
    data, addr = client.recvfrom(1024)
    data=data.decode()
    index1 = data.index(',')
    index2 = data.index('&')
    r = int(data[:index1])
    s2 = int(data[index1 + 1:index2])
    s3 = int(data[index2 + 1:])
    s = ((d1 * k1) * s2 + d1 * s3 - r) % N
    if s != 0 or s != N - r:
        signature=(r,s)
        print("签名为:",signature)
    else:
        print('error')
        client.close()
    client.close()

if __name__ == "__main__":
    beginAC()
