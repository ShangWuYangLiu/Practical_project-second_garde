import secrets
from gmssl import sm3, func

# 定义椭圆曲线参数、基点和阶
A = 0
B = 7
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
h = 1


#扩展欧几里得算法
def extended_euclidean(a, b, arr):
    if b == 0:
        arr[0] = 1
        arr[1] = 0
        return a
    g = extended_euclidean(b, a % b, arr)
    t = arr[0]
    arr[0] = arr[1]
    arr[1] = t - int(a / b) * arr[1]
    return g


#求逆
def mod_inverse(a, n):
    arr = [0, 1, ]
    gcd = extended_euclidean(a, n, arr)
    if gcd == 1:
        return (arr[0] % n + n) % n
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


def get_bit_num(x):
    """获得x的比特长度"""
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


# Schnorr签名
def Schnorr_sign(M, sk):
    """
    :return signature: (R, s)
    """
    k = secrets.randbelow(N)
    R = elliptic_mult(k, G)
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    s = k + e * sk % N
    return (R, s)


# Schnorr验签
def Schnorr_verify(signature, M, pk):
    R, s = signature
    tmp = str(R[0]) + str(R[1]) + M
    e = int(sm3.sm3_hash(func.bytes_to_list(bytes(tmp, encoding='utf-8'))), 16)
    tmp1 = elliptic_mult(s, G)
    tmp2 = elliptic_mult(e, pk)
    tmp2 = elliptic_add(R, tmp2)
    return tmp1 == tmp2
