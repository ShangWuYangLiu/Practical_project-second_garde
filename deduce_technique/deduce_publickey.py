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


# Tonelli_Shanks求二次剩余
def legendre(n, p):  # 这里用勒让德符号来表示判断二次（非）剩余的过程
    return pow(n, (p - 1) // 2, p)


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

#椭圆曲线逆元
def elliptic_inv(p):
    r = [p[0]]
    r.append(P - p[1])
    return r


# 椭圆曲线减法:p - q
def elliptic_sub(p, q):
    q_inv = elliptic_inv(q)
    return elliptic_add(p, q_inv)


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


# ECDSA签名
def ECDSA_sign(m, sk):
    """
    m:message
    sk:私钥
    返回(r,s)签名值
    """
    while 1:
        k = secrets.randbelow(N)  # N is prime, then k <- Zn*
        R = elliptic_mult(k, G)
        r = R[0] % N  # Rx mod n
        if r != 0:
            break
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    tmp1 = mod_inverse(k, N)
    tmp2 = (e + sk * r) % N
    s = tmp1 * tmp2 % N
    return (r, s)


# ECDSA验签
def ECDSA_verify(signature, m, pk):
    """
    signature:(r,s)
    m:message
    pk:公钥
    返回验证通过or不通过
    """
    r, s = signature
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))  # e = hash(m)
    e = int(e, 16)
    w = mod_inverse(s, N)
    tmp1 = elliptic_mult(e * w, G)
    tmp2 = elliptic_mult(r * w, pk)
    dot = elliptic_add(tmp1, tmp2)
    x = dot[0]
    return x == r


# 由签名推得公钥pk
# s * kG = eG + rP mod n
def deduce_pk_from_sig(signature, msg):
    r, s = signature
    # kG = R = (x, y)
    x = r % P
    y2 = pow(x, 3) + A * x + B
    y = Tonelli_Shanks(y2, P)
    # 两个候选点
    R1 = (x, y)
    R2 = (x, P - y)
    # 求e = hash(m)
    e = sm3.sm3_hash(func.bytes_to_list(bytes(msg, encoding='utf-8')))
    # 由R1求pk1
    pk1 = elliptic_mult(mod_inverse(r, N), elliptic_sub(elliptic_mult(s, R1), elliptic_mult(int(e, 16), G)))
    # 由R2求pk2
    pk2 = elliptic_mult(mod_inverse(r, N), elliptic_sub(elliptic_mult(s, R2), elliptic_mult(int(e, 16), G)))
    return pk1,pk2


if __name__ == '__main__':
    print("="*175)
    sk, pk = generate_key()
    print("正确的公钥为:", pk)
    print("="*175)
    msg = "202000460012"
    signature = ECDSA_sign(msg, sk)
    print("对消息签名:", signature)
    print("="*175)
    pk1,pk2=deduce_pk_from_sig(signature, msg)
    print("推测的公钥为:")
    print("pk1:",pk1)
    print("pk2:",pk2)
    print("=" * 175)
    if pk1==pk or pk2==pk:
        print("验证推测是否成功:True")
    print("=" * 175)
