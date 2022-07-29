# pitfalls_Schnorr

**项目内容**
(1) Leaking k leads to leaking of d (k的泄露会导致泄露d)

(2) Reusing k leads to leaking of d (对不同的消息使用相同的k进行签名会泄露d)

(3) Two users, using k leads to leaking of d, that is they can deduce each other's d (两个不同的user使用相同的k,可以相互推测对方的私钥d)

(4) Malleability, e.g. (r,s) and (r,-s) are both valid signatures (验证(r,s) and (r,-s)均为合法签名)

(5) Same d and k between ECDSA and Schnorr, leads to leaking d (ECDSA与Schnorr使用相同的d和k而泄露d)

注意：其中1和2还分别根据推测得到的d值进行了消息的伪造并成功通过验签
    
**实验思路**
(1) Leaking k leads to leaking of d (k的泄露会导致泄露d):

    由签名算法中s = (k + ed) mod n 推得 d = (s - k) / e
    
(2) Reusing k leads to leaking of d (对不同的消息使用相同的k进行签名会泄露d):

    s1 = (k + e1d) mod n
    
    s2 = (k + e2d) mod n
    
    推得 d = (s1 - s2) / (e1 - e2)
    
(3) Two users, using k leads to leaking of d, that is they can deduce each other's d (两个不同的user使用相同的k,可以相互推测对方的私钥d):

    两个不同的user使用相同的k:此类情况下相当于leaking k,所以可以相互推测对方的私钥d
    
(4) Malleability, e.g. (r,s) and (r,-s) are both valid signatures (验证(r,s) and (r,-s)均为合法签名):

    首先生成签名(r, s),然后使用验签算法验证(r, -s)是否是合法签名
    
(5) Same d and k between ECDSA and Schnorr, leads to leaking d (ECDSA与Schnorr使用相同的d和k而泄露d):
    
    s1 = k^-1(e1 + dr) mod n
    
    s2 = (k + e2d) mod n
    
    推得 d = (s2 - e1 / s1) / (r / s1 + e2)
    
**代码说明**

见代码注释

**运行指导**

将Schnorr.py和Schnorr_pitfalls.py放在同一路径下，然后执行Schnorr_pitfalls.py即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181772499-c7e4504e-77b3-428e-9014-4a83af2a046a.png)

![image](https://user-images.githubusercontent.com/105548921/181772523-464e740f-ce3b-4de3-8233-902a666a8652.png)
