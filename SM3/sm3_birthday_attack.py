from gmssl import sm3, func
from faker import Faker
import time

# 部分bit的hash的碰撞
# 二进制位数
bin_length = 16
# 十六进制位数
hex_length = bin_length // 4


# 随机生成消息
def getRandomList():
    str_list = []
    faker = Faker(locale='zh_CN')
    for i in range(pow(2, bin_length)):
        str_list.append(faker.name() + ',' + faker.address() + ',' + faker.email() + ',' + faker.phone_number())
    return str_list

def birthday_attack():
    # 存储随机字符串
    str_list = getRandomList()
    # 存储字符串对应的hash值
    hash_list = []
    for i in range(len(str_list)):
        hash_value = sm3.sm3_hash(func.bytes_to_list(bytes(str_list[i], encoding='utf-8')))[0:hex_length]
        if hash_value in hash_list:
            print()
            print("消息1:", str_list[hash_list.index(hash_value)])
            print("消息1的hash值:", sm3.sm3_hash(func.bytes_to_list(bytes(str_list[hash_list.index(hash_value)], encoding='utf-8'))))
            print("消息2:", str_list[i])
            print("消息2的hash值:", sm3.sm3_hash(func.bytes_to_list(bytes(str_list[i], encoding='utf-8'))))
            return True
        hash_list.append(hash_value)

if __name__ == '__main__':
    print("="*75)
    print("部分bit的hash（{}bits）值碰撞:".format(bin_length))
    start = time.time()
    while 1:
        ret = birthday_attack()
        if ret:
            break
    end = time.time()
    print()
    print("The total time is:{}".format(end - start) + "s")
    print("="*75)
