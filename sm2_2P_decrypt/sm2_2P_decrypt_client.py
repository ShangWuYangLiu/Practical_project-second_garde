import socket
from new_sm2 import *
import secrets
from gmssl import sm3, func

def beginAC():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # 1:生成私钥和P1,向服务端发送P1
    d1 = secrets.randbelow(N)
    P1 = elliptic_mult(mod_inverse(d1, N), G)
    sdata = str(P1[0]) + ',' + str(P1[1])
    client.sendto(sdata.encode(), ("127.0.0.1", 12345))

    # 2:接收服务器发来的密文
    data, addr = client.recvfrom(4096)
    data = eval(data)
    C1, C2, C3 = data
    print("接收的密文为:")
    print("C1:", C1)
    print("C2:", C2)
    print("C3:", C3)

    # 3:检查C1 != 0并且计算T1,并发送给服务端T1
    if C1 == 0:
        print('error')
        client.close()
    T1 = elliptic_mult(mod_inverse(d1, N), C1)
    sdata = str(T1[0]) + ',' + str(T1[1])
    client.sendto(sdata.encode(), addr)

    # 4:接收服务端发来的T2
    data, addr = client.recvfrom(1024)
    data = data.decode()
    index1 = data.index(',')
    T2 = (int(data[:index1]), int(data[index1 + 1:]))

    # 5:由密文恢复明文
    #T2 - C1 = (x2, y2) = kP
    x2, y2 = elliptic_sub(T2, C1)
    x2 = hex(x2)[2:]
    y2 = hex(y2)[2:]
    klen = len(C2) * 4
    #t = KDF(x2 || y2, klen)
    t = KDF(x2 + y2, klen)
    #M = C2 xor t
    M = dec_xor(C2, t)
    #u = Hash(x2 || M || y2)
    u = sm3.sm3_hash(func.bytes_to_list(bytes((x2 + M + y2), encoding='utf-8')))
    if u == C3:
        print("恢复的明文为:",M)
    print("finished.")
    client.close()

if __name__=="__main__":
    beginAC()
