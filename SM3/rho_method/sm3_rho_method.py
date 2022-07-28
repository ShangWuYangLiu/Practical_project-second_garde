from gmssl import sm3, func
import random
import time

# 实现部分bit的hash碰撞
# 二进制位数
bit_length = 16
# 十六进制位数
hex_length = bit_length // 4


def rho_method():
    # 生成随机数
    x = str(random.randint(0, pow(2, bit_length)))
    # x_a = x_1
    x_a = sm3.sm3_hash(func.bytes_to_list(bytes(x, encoding='utf-8')))
    # x_b = x_2
    x_b = sm3.sm3_hash(func.bytes_to_list(bytes(x_a, encoding='utf-8')))
    # 记录原像
    msg1 = x
    msg2 = x_a
    while x_a[:hex_length] != x_b[:hex_length]:
        # x_a = x_i
        msg1 = x_a
        x_a = sm3.sm3_hash(func.bytes_to_list(bytes(x_a, encoding='utf-8')))
        # x_b = x_2i
        temp = sm3.sm3_hash(func.bytes_to_list(bytes(x_b, encoding='utf-8')))
        x_b = sm3.sm3_hash(func.bytes_to_list(bytes(temp, encoding='utf-8')))
        msg2 = temp
    print("message 1:", msg1)
    print("The hash value of message 1:", sm3.sm3_hash(func.bytes_to_list(bytes(msg1, encoding='utf-8'))))
    print()
    print("message 2:", msg2)
    print("The hash value of message 2:", sm3.sm3_hash(func.bytes_to_list(bytes(msg2, encoding='utf-8'))))


if __name__ == '__main__':
    print("="*75)
    print("Collision of hash ({}bits) values of some bits:".format(bit_length))
    print()
    start = time.time()
    rho_method()
    end = time.time()
    print()
    print("The total time is:{}".format(end - start) + "s")
    print("="*75)
