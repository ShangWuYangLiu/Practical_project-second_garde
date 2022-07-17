from math import ceil


#ff函数
def ff(x,y,z,j):
    #x,y,z分别为3个32位向量（int），j为轮数（0<=j<64）
    if 0<=j<16:
        ret=x^y^z
    elif 16<=j<64:
        ret=(x&y)|(x&z)|(y&z)
    return ret

#gg函数
def gg(x,y,z,j):
    #x,y,z分别为3个32位向量（int），j为轮数（0<=j<64）
    if 0<=j<16:
        ret=x^y^z
    elif 16<=j<64:
        ret=(x&y)|((~x)&z)
    return ret

#左移函数
def shift_left(x,n):
    #x是32位的向量
    strx=bin(x)[2:].zfill(32)
    add='0'*n
    strret=strx[n:]+add
    ret=int(strret,2)
    return ret

#p1置换(消息扩展)
def p1(x):
    ret=x^(shift_left(x,15))^(shift_left(x,23))
    return ret

#p0置换(压缩函数)
def p0(x):
    ret=x^(shift_left(x,9))^(shift_left(x,17))
    return ret


#常量
T1=[0x79cc4519]
T2=[0x7a879d8a]
T=T1*16+T2*48
V=[0x7380166f,0x4914b2b9,0x172442d7,0xda8a0600,0xa96f30bc,0x163138aa,0xe38dee4d,0xb0fb0e4e]

#压缩函数cf
def sm3_cf(vi,bi):
    #消息扩展
    w=[]
    #w列表都是十进制整数
    #生成w0-w15
    for i in range(16):
        wei=0x1000000 #权重 初始为2^24
        rel=0
        for j in range(i*4,(i+1)*4):#将4字节数整合成一个字
            rel=rel+bi[j]*wei  #bi[j]数据类型是二进制对应的整数，比如0b101--5
            wei=int(wei/0x100) #权重每次减少2^8
        w.append(rel)

    #生成w16-w67
    for k in range(16,68):
        tmp=p1(w[k-16]^w[k-9]^shift_left(w[k-3],15))^shift_left(w[k-13],7)^w[k-6]
        w.append(tmp)
    w1=[]
    #生成w’0-w‘64
    for k in range(0,64):
        tmp=w[k]^w[k+4]
        w1.append(tmp)
    A,B,C,D,E,F,G,H=vi
    #64轮加密
    for j in range(0,64):
        #
        ss1=shift_left((shift_left(A,12))^E^(shift_left(T[j],j%32)),7)
        #
        ss2=ss1^shift_left(A,12)
        tt1=ff(A,B,C,j)^D^ss2^w1[j]
        tt2=gg(E,F,G,j)^H^ss1^w[j]
        D=C
        C=shift_left(B,9)
        B=A
        A=tt1
        H=G
        G=shift_left(F,19)
        F=E
        E=p0(tt2)
    v_i=[A,B,C,D,E,F,G,H]
    return [v_i[i]^vi[i] for i in range(0,8)]

#填充函数
def fill(msg):
    '''
    填充方法：将字符串中每个字符首先变成ascii码，然后再变成二进制串
    '''
    msg_bin = ''
    for i in msg:
        ascii_i = ord(i)
        msg_bin = msg_bin + bin(ascii_i)[2:]
    len1 = len(msg_bin)
    msg_bin = msg_bin + '1'
    k = 0
    while 1:
        if (len1 + 1 + k) % 512 == 448:
            break
        k = k + 1
    msg_bin = msg_bin + '0' * k + bin(len1)[2:].zfill(64)
    # 填充之后长度
    len2 = len(msg_bin)
    # 分组个数
    num = ceil(len2 / 512)
    temp = []
    for i in range(0, len2, 8):
        tmp = msg_bin[i:i + 8]
        tmp = int(tmp, 2)
        temp.append(tmp)
    b = [0] * num
    instate = []
    for i in range(0, len(temp)):
        instate.append(temp[i])
        if (i + 1) % 64 == 0:
            b[int(i / 64) - 1] = instate
            instate = []
    return b

#普通sm3
def sm3(msg):
    #消息填充,msg是字符串类型
    b=fill(msg)
    v=[]

    for i in range(0,len(b)):
        if i==0:
            v.append(sm3_cf(V, b[i]))
        else:
            v[0]=sm3_cf(v[i-1],b[i])

    result=''
    for j in range(0,8):
        result=result+hex(v[0][j])[2:]
    return result

#计算第二轮往后的sm3哈希值（包括第二轮）
def sm3_new(msg_pad,new_v):
    #消息填充,msg是字符串类型
    b1=fill(msg_pad)
    v=[]
    for i in range(0,len(b1)):
        if i==0:
            v.append(sm3_cf(new_v, b1[i]))
        else:
            v[0]=sm3_cf(v[i-1], b1[i])
    result=''
    for j in range(0,8):
        result=result+hex(v[0][j])[2:]
    return result

#填充的字符串十六进制表示
def hexmsg_fill(msg):
    msg_bin = ''
    for i in msg:
        ascii_i = ord(i)
        msg_bin = msg_bin + bin(ascii_i)[2:]
    len1 = len(msg_bin)
    msg_bin = msg_bin + '1'
    k = 0
    while 1:
        if (len1 + 1 + k) % 512 == 448:
            break
        k = k + 1
    msg_bin = msg_bin + '0' * k + bin(len1)[2:].zfill(64)
    ret=hex(int(msg_bin,2))[2:]
    return ret

#字符串十六进制表示
def hexmsg(msg):
    msg_bin = ''
    for i in msg:
        ascii_i = ord(i)
        msg_bin = msg_bin + bin(ascii_i)[2:]
    ret = hex(int(msg_bin, 2))[2:]
    return ret

#用以实现计算伪造消息的hash值
def sm3_lenattack_hash(msg,msg_pad):
    b=fill(msg)
    b1=fill(msg_pad)
    b=b+b1
    v = []
    for i in range(0, len(b)):
        if i == 0:
            v.append(sm3_cf(V, b[i]))
        else:
            v[0] = sm3_cf(v[i - 1], b[i])

    result = ''
    for j in range(0, 8):
        result = result + hex(v[0][j])[2:]
    return result


if __name__=="__main__":
    newv=sm3('12346789')
    new_v=[]
    for i in range(0,len(newv),8):
        new_v.append(newv[i:i+8])
    for i in range(0,len(new_v)):
        new_v[i]=int(new_v[i],16)
    re=sm3_new('0123320',new_v)
    pp=sm3_lenattack_hash('12346789','0123320')
    print("消息",hexmsg('12346789'),"的哈希值为:",newv)
    print("附加消息为:",hexmsg('0123320'))
    print("认为构造消息的hash值:",re)
    print("构造的新消息为:",hexmsg_fill('12346789')+hexmsg('0123320'))
    print("计算新消息(原消息+padding+附加消息)的哈希值:",pp)
    print("验证是否攻击成功:",pp==re)
