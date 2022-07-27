"""
forge a signature to pretend that you are Satoshi
在不验证m的情况下,能够伪造签名

原理：

r = x mod n
e = rab^-1 mod n
s = rb^-1 mod n

"""
import secrets
import random
from gmssl import sm3, func

# 定义椭圆曲线参数、基点和阶
A = 0
B = 7

G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
#有限域的阶
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
#椭圆曲线的阶
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1

#扩展欧几里得算法:返回最大公因子和系数
def extended_euclidean(a, b):
    if a == b:
        return (a, 1, 0)
    else:
        i = 0
        a_list = [a]
        b_list = [b]
        q_list = []
        r_list = []
        while 1:
            q_list.append(int(b_list[i]/a_list[i]))
            r_list.append(b_list[i]%a_list[i])
            b_list.append(a_list[i])
            a_list.append(r_list[i])
            i += 1
            if r_list[i-1] == 0:
                break
        i -= 1
        gcd = a_list[i]
        x_list = [1]
        y_list = [0]
        i -= 1
        all_steps = i
        while i >= 0:
            y_list.append(x_list[all_steps-i])
            x_list.append(y_list[all_steps-i] - q_list[i]*x_list[all_steps-i])
            i -= 1
        return (gcd, x_list[-1], y_list[-1])#返回最后一个元素

def mod_inverse(j, n):
    (gcd, x, y) = extended_euclidean(j, n)
    if gcd == 1:
        return x%n
    else:
        return -1

#椭圆曲线加法运算
def elliptic_add(p, q):
    if p == 0 and q == 0:
        return 0
    elif p == 0:
        return q
    elif q == 0:
        return p
    else:
        if p[0] > q[0]:#交换p、q
            temp = p
            p = q
            q = temp
        r = []
        rel= (q[1] - p[1])*mod_inverse(q[0] - p[0], P) % P
        r.append((rel*rel - p[0] - q[0]) % P)
        r.append((rel*(p[0] - r[0]) - p[1]) % P)
        return (r[0], r[1])

#2P
def elliptic_double(p):
    r = []
    rel = (3*p[0]**2 + A)*mod_inverse(2*p[1], P) % P
    r.append((rel*rel - 2*p[0])%P)
    r.append((rel*(p[0] - r[0]) - p[1])%P)
    return (r[0], r[1])

#椭圆曲线乘法运算
def elliptic_mult(s, p):
    n = p
    r = 0 #无穷远点
    s_binary = bin(s)[2:]
    s_length = len(s_binary)
    for i in reversed(range(s_length)):
        if s_binary[i] == '1':
            r = elliptic_add(r, n)
        n = elliptic_double(n)
    return r

#得到x的bit长度
def get_bit_num(x):
    if isinstance(x, int):  # when int
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):  # when string
        return len(x.encode()) << 3
    elif isinstance(x, bytes):  # when bytes
        return len(x) << 3
    return 0

#生成公私钥对
def generate_key():
    private_key = int(secrets.token_hex(32), 16)#生成一个十六进制格式的安全随机文本字符串
    public_key = elliptic_mult(private_key, G)
    return private_key, public_key

#签名函数
def sign(private_key, message, Z_A):
    M = Z_A + message
    M_b = bytes(M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(M_b))
    e = int(e, 16)
    k = secrets.randbelow(P)#生成安全的整数
    random_point = elliptic_mult(k, G)
    r = (e + random_point[0]) % N
    s = (mod_inverse(1 + private_key, N) * (k - r * private_key)) % N
    return (r, s)


#验证签名（不使用message）
def verify_no_msg(signature, e, pk):
    r, s = signature
    x = elliptic_mult(mod_inverse(s, N), elliptic_add(elliptic_mult(e, G), elliptic_mult(r, pk)))
    return x[0] % N == r


# 伪造中本聪的签名
def pretend_Satoshi(pk):
    u = random.randrange(1, N - 1)
    v = random.randrange(1, N - 1)
    R = elliptic_add(elliptic_mult(u, G), elliptic_mult(v, pk))
    r = R[0] % N
    e = (r * u * mod_inverse(v, N)) % N
    s = (r * mod_inverse(v, N)) % N
    signature_forge = (r, s)
    print("The forged signature is:")
    print((hex(r)[2:], hex(s)[2:]))#去掉0x
    return verify_no_msg(signature_forge, e, pk)


if __name__ == '__main__':
    # Satoshi的公私钥对
    sk, pk = generate_key()
    print('='*135)
    # 伪造Satoshi的签名
    print("Determining whether the forged signature is a legitimate signature:", pretend_Satoshi(pk))
    print('='*135)
