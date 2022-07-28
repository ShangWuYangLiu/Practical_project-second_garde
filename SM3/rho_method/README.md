# implement the Rho method of reduced SM3

**项目内容**

使用pollard-rho方法找到sm3的碰撞

**实验原理**

1.随机生成一个消息，计算hash值

2.前面消息的hash作为新的消息，计算hash值

3.判断是否有环存在

**代码说明**

见代码注释

**运行指导**

运行sm3_rho_method.py文件

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181413275-602d5918-77ab-4934-8a13-2398ddfb9780.png)
