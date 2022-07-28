# report on the application of this deduce technique in Ethereum with ECDSA

**项目内容**

由ECDSA签名来恢复出相应的公钥

**实验思路**

1.首先了解ECDSA签名算法的步骤：

(1) 密钥生成：选择私钥(d,d<n),计算公钥P=dG

(2) 随机选取k∈Zn*,计算R=kG=(x,y)

(3) 计算r=Rx mod n,如果r=0,重新进行第二步

(4) 计算消息m的哈希值记作e

(5) 计算s=(e+dr)×k^-1 mod n

(6) 生成的签名为(r,s)

2.如何由签名恢复出公钥：

(1) 已知s=(e+dr)×k^-1 mod n，可得sk=(e+dr) mod n，进而可得s×kG=(eG+rP) mod n

(2) 通过r可以计算出点R的横坐标x，代入曲线方程可以求得纵坐标y，继而可以求得关于X轴对称的两个椭圆曲线的点R1，R2

(3) s×kG=(eG+rP) mod n中的s、kG、G、r已知，而e可以计算得出，故P=(s×kG-eG)×r^-1

**代码说明**

见代码注释

**运行指导**

直接运行deduce_publickey.py文件即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181577407-df01b9ab-a045-4a59-8e11-7e95b987fde1.png)
