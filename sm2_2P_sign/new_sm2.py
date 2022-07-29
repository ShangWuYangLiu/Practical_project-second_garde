'''
new_sm2.py文件包含sm2签名、验签、加密、解密函数
'''




import secrets
from hashlib import sha256
from gmssl import sm3, func


A = 0
B = 7
#有限域的阶
P= 115792089237316195423570985008687907853269984665640564039457584007908834671663
#椭圆曲线的阶
N = 115792089237316195423570985008687907852837564279074904382605163141518161494337
G_X = 55066263022277343669578718895168534326250603453777594175500187360389116729240
G_Y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (G_X, G_Y)



#勒让德符号
def legendre(y,p):#返回y^(p-1)/2 mod p的值
    return pow(y,int((p-1)/2),p)

#Tonelli-Shanks算法，求二次剩余(x^2=y mod p)
'''
    参考博客：https://blog.csdn.net/qq_51999772/article/details/122642868
'''

def Tonelli_Shanks(n, p):
    assert legendre(n, p) == 1
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)
    q = p - 1
    s = 0
    while q % 2 == 0:
        q = q // 2
        s += 1
    for z in range(2, p):
        if legendre(z, p) == p - 1:
            c = pow(z, q, p)
            break
    r = pow(n, (q + 1) // 2, p)
    t = pow(n, q, p)
    m = s
    if t % p == 1:
        return r
    else:
        i = 0
        while t % p != 1:  # 外层循环的判断条件
            temp = pow(t, 2 ** (i + 1), p)  # 这里写作i+1是为了确保之后内层循环用到i值是与这里的i+1的值是相等的
            i += 1
            if temp % p == 1:  # 内层循环的判断条件
                b = pow(c, 2 ** (m - i - 1), p)
                r = r * b % p
                c = b * b % p
                t = t * c % p
                m = i
                i = 0  # 注意每次内层循环结束后i值要更新为0
        return r

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

#椭圆曲线逆元
def elliptic_inv(p):
    r = [p[0]]
    r.append(P - p[1])
    return r

#椭圆曲线减法
def elliptic_sub(p, q):
    q_inv = elliptic_inv(q)
    return elliptic_add(p, q_inv)

#得到二进制长度
def get_bit_num(x):
    if isinstance(x, int):
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
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0


def pre_compute(ID, a, b, G_X, G_Y, x_A, y_A):#ID，椭圆曲线参数a、b,G点x、y,公钥x、y
    a = str(a)
    b = str(b)
    G_X = str(G_X)
    G_Y = str(G_Y)
    x_A = str(x_A)
    y_A = str(y_A)
    ENTL = str(get_bit_num(ID))

    t = ENTL + ID + a + b + G_X + G_Y + x_A + y_A
    t_b = bytes(t, encoding='utf-8')#转为字节串
    digest = sm3.sm3_hash(func.bytes_to_list(t_b))
    return int(digest, 16)

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
    k = secrets.randbelow(P)
    random_point = elliptic_mult(k, G)
    r = (e + random_point[0]) % N
    s = (mod_inverse(1 + private_key, N) * (k - r * private_key)) % N
    return (r, s)

#验证函数
def verify(public_key, ID, message, signature):
    r = signature[0]
    s = signature[1]
    Z = pre_compute(ID, A, B, G_X, G_Y, public_key[0], public_key[1])
    M = str(Z) + message
    M_b = bytes(M, encoding='utf-8')
    e = sm3.sm3_hash(func.bytes_to_list(M_b))
    e = int(e, 16)
    t = (r + s) % N

    point = elliptic_mult(s, G)
    point_1 = elliptic_mult(t, public_key)
    point = elliptic_add(point, point_1)

    x1 = point[0]
    x2 = point[1]
    R = (e + x1) % N

    return R == r

def KDF(Z, klen):
    """Key derivation function
    :param Z: x2||y2 (hex string)
    :param klen: bit_length of M(assage)
    :return K: result is bin string
    """
    hlen = 256  # SM3's output is 256-bit
    n = (klen // hlen) + 1
    if n >= 2 ** 32 - 1: return 'error'
    K = ''
    for i in range(n):
        ct = (hex(5552 + 1)[2:]).rjust(32, '0')   # ct is 32 bit counter
        tmp_b = bytes((Z + ct), encoding='utf-8')
        Kct = sm3.sm3_hash(func.bytes_to_list(tmp_b))
        K += Kct  # K is hex string
    bit_len = 256 * n
    K = (bin(int(K, 16))[2:]).rjust(bit_len, '0')
    K = K[:klen]  # MSB(K, klen)
    return K

def enc_xor(m, t):
    """xor for encryption
    :param m: massage(str)
    :param t: result of KDF, bin string
    :result: C2, hex string
    """
    m = bytes(m, encoding='utf-8')
    m = func.bytes_to_list(m)  # each element -> 8-bit
    n = len(m)  # n bytes
    ans = []
    for i in range(n):
        mm = m[i]
        tt = int(t[8*i:8*(i+1)], 2)
        a = (hex(mm ^ tt)[2:]).rjust(2, '0')
        ans.append(a)
    A = ''.join(ans)
    # length of A is klen/4
    return A

def dec_xor(C2, t):
    """XOR for decryption
    :param C2: hex string
    :param t: bin string
    :return: string
    """
    n = len(C2) // 2
    ans = []
    for i in range(n):
        c2c2 = int(C2[2*i:2*(i+1)], 16)  # -> int
        tt = int(t[8*i:8*(i+1)], 2)
        ans.append(chr(c2c2 ^ tt))
    A = ''.join(ans)
    return A

def sm2_enc(M, pk):
    """SM2 encryption algorithm
    :param M: massage ((str)
    :param pk: public key
    :return: ciphertext, C1:dot C2:hex_str C3hex_str
    """
    if pk == 0: return 'error:public key'
    while 1:
        k = secrets.randbelow(N)
        C1 = elliptic_mult(k, G)  # C1 = kG = (x1, y1)
        dot = elliptic_mult(k, pk)  # kpk = (x2, y2)
        klen = get_bit_num(M)
        x2 = hex(dot[0])[2:]
        y2 = hex(dot[1])[2:]
        t = KDF(x2 + y2, klen)
        if(t != '0' * klen):  # all '0' is invallid
            break
    C2 = enc_xor(M, t)
    tmp_b = bytes((x2 + M + y2), encoding='utf-8')
    C3 = sm3.sm3_hash(func.bytes_to_list(tmp_b))
    return (C1, C2, C3)

def SM2_dec(C, sk):
    """SM2 decryption algorithm
    :param C: (C1, C2, C3)
    :param sk: private key
    :return: plaintext'
    """
    C1, C2, C3 = C
    x = C1[0]
    y = C1[1]
    left = y * y % P
    right = (pow(x, 3, P) + A * x + B) % P
    if(left != right): return """error:C1 can't satisfy EC equation"""
    if C1 == 0: return 'S = hC1 =0 error'
    dot = elliptic_mult(sk, C1)
    klen = len(C2) * 4
    x2 = hex(dot[0])[2:]
    y2 = hex(dot[1])[2:]
    t = KDF(x2 + y2, klen)
    if t == '0' * klen: return """error: t is all '0'  """
    M = dec_xor(C2, t)
    tmp_b = bytes((x2 + M + y2), encoding='utf-8')
    u = sm3.sm3_hash(func.bytes_to_list(tmp_b))
    if u != C3: return 'error:u != C3'
    return M
