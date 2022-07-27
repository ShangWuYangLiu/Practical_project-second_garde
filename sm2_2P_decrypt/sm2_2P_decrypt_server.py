import socket
import secrets
import pre_SM2

def step1(P1):
    """step 1 of right
    :param P1: received P1
    :return d2:random sub private key
    :return public_key_P: public key should be published
    """
    d2 = secrets.randbelow(pre_SM2.N)
    tmp = pre_SM2.inv(d2, pre_SM2.N)
    tmp = pre_SM2.EC_multi(tmp, P1)
    public_key_P = pre_SM2.EC_sub(tmp, pre_SM2.G)
    return d2, public_key_P


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('', 12300))


data, addr=s.recvfrom(1024)
data = data.decode()
index1 = data.index(',')
P1 = (int(data[:index1]), int(data[index1 + 1:]))
d2, public_key_P = step1(P1)
data = str(public_key_P[0]) + ',' + str(public_key_P[1])
s.sendto(data.encode(), addr)

data, addr=s.recvfrom(1024)
data = data.decode()
index1 = data.index(',')
T1 = (int(data[:index1]), int(data[index1 + 1:]))
tmp = pre_SM2.inv(d2, pre_SM2.N)
T2 = pre_SM2.EC_multi(tmp, T1)
data = str(T2[0]) + ',' + str(T2[1])
s.sendto(data.encode(), addr)


s.close()
print("---------connect closed---------")
