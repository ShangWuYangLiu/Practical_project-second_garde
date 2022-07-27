import pre_SM2
import secrets
from gmssl import sm3, func
import socket
import mySM2

def step1():
    """step 1 of left
    :return d1, P1
    """
    d1 = secrets.randbelow(pre_SM2.N)
    tmp = pre_SM2.inv(d1, pre_SM2.N)
    P1 = pre_SM2.EC_multi(tmp, pre_SM2.G)
    return d1, P1

def step2(d1, C1):
    """check C1 and compute T1"""
    if C1 == 0: return 'error'
    tmp = pre_SM2.inv(d1, pre_SM2.N)
    T1 = pre_SM2.EC_multi(tmp, C1)
    return T1

def step3(T2, C1, C2, C3):
    """compute M'"""
    tmp = pre_SM2.EC_sub(T2, C1)  # kP = (x2, y2)
    x2 = hex(tmp[0])[2:]
    y2 = hex(tmp[1])[2:]
    klen = len(C2) * 4
    t = mySM2.KDF(x2 + y2, klen)
    m = mySM2.dec_XOR(C2, t)
    tmp_b = bytes((x2 + m + y2), encoding='utf-8')
    u = sm3.sm3_hash(func.bytes_to_list(tmp_b))
    if u != C3: return 'error:u != C3'
    return m





s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


d1, P1 = step1()
data = str(P1[0]) + ',' + str(P1[1])
s.sendto(data.encode(), ("127.0.0.1" ,12300))
data, addr=s.recvfrom(1024)
data = data.decode()
index1 = data.index(',')
public_key_P = (int(data[:index1]), int(data[index1 + 1:]))



M = "sm2 2p decrypt."
C1, C2, C3 = mySM2.SM2_enc(M, public_key_P)



T1 = step2(d1, C1)
data = str(T1[0]) + ',' + str(T1[1])
s.sendto(data.encode(), addr)



data, addr=s.recvfrom(1024)
data = data.decode()
index1 = data.index(',')
T2 = (int(data[:index1]), int(data[index1 + 1:]))
m = step3(T2, C1, C2, C3)  # computed plaintext

s.close()
print("---------connect closed---------")


print("\nmassage: {}".format(M))
print("\nplaintext from ciphertext:{}".format(m))

