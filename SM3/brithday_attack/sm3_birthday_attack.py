from gmssl import sm3, func
import time
import random
import string

# 部分bit的hash的碰撞
# 二进制位数
bit_length = 16
# 十六进制位数
hex_length = bit_length // 4

#随机生成2的bit_length个字符串
def get_random_str(number):#参数为字符串个数
    number_of_strings = number
    str_list=[]
    for x in range(number_of_strings):
        length_of_string = random.randint(0, 100)
        str_list.append(''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(length_of_string)))
    return str_list


def birthday_attack():
    # 存储随机字符串
    str_list = get_random_str(pow(2,bit_length))
    # 存储字符串对应的hash值
    hash_list = []
    for i in range(len(str_list)):
        hash_value = sm3.sm3_hash(func.bytes_to_list(bytes(str_list[i], encoding='utf-8')))[0:hex_length]
        #判断是否找到碰撞
        if hash_value in hash_list:
            #去掉消息相同的情况
            if str_list[hash_list.index(hash_value)]!=str_list[i]:
                print()
                print("message 1:", str_list[hash_list.index(hash_value)])
                print("The hash value of message 1:",
                      sm3.sm3_hash(func.bytes_to_list(bytes(str_list[hash_list.index(hash_value)], encoding='utf-8'))))
                print("message 2:", str_list[i])
                print("The hash value of message 2:",
                      sm3.sm3_hash(func.bytes_to_list(bytes(str_list[i], encoding='utf-8'))))
                return True
        hash_list.append(hash_value)

if __name__ == '__main__':
    print("="*75)
    print("Collision of hash ({}bits) values of partial bits:".format(bit_length))
    start = time.time()
    #进行循环，一次生成的2^bit_length个字符串可能找不到碰撞
    while 1:
        if birthday_attack():
            break
    end = time.time()
    print()
    print("The total time is:{}".format(end - start) + "s")
    print("="*75)
