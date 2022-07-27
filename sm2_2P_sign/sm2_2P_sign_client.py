import pre_SM2
import secrets
from gmssl import sm3, func
import socket
import time

def step1():
    """step 1 of left
    :return d1, P1
    """
    d1 = secrets.randbelow(pre_SM2.N)
    tmp = pre_SM2.inv(d1, pre_SM2.N)
    P1 = pre_SM2.EC_multi(tmp, pre_SM2.G)
    return d1, P1

def step2(Z, M):
    """step 2 of left
    :param Z: identifier for both parties
    :param M: massage
    :return k1, Q1, e
    """
    m = Z + M
    m_b = bytes(m, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(m_b))
    k1 = secrets.randbelow(pre_SM2.N)
    Q1 = pre_SM2.EC_multi(k1, pre_SM2.G)
    return k1, Q1, e

def step3(d1, k1, r, s2, s3):
    """step 3 of left
    :param d1: generated in step1
    :param k1: generated in step2
    :param r, s2, s3: received
    :return: signature(r, s) or 'error'
    """
    s = ((d1 * k1) * s2 + d1 * s3 - r) % pre_SM2.N
    if s != 0 or s != pre_SM2.N - r: return (r, s)
    else: return 'error'

s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)



d1, P1 = step1()
data = str(P1[0]) + ',' + str(P1[1])
s.sendto(data.encode(), ("127.0.0.1" ,12300))



time.sleep(1)
ID1 = 'ID2143'
ID2 = 'ID12300'
Z = ID1 + ID2
M = 'sm2 2p sign'
k1, Q1, e = step2(Z, M)
data = str(Q1[0]) + ',' + str(Q1[1]) + ';' + e
s.sendto(data.encode(), ("127.0.0.1" ,12300))



data, addr=s.recvfrom(1024)
data = data.decode()
index1 = data.index(',')
index2 = data.index(';')
r = int(data[:index1])
s2 = int(data[index1 + 1:index2])
s3 = int(data[index2+1:])
signa = step3(d1, k1, r, s2, s3)
print(signa)

s.close()
print("connect closed")
