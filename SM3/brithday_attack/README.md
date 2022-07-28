# implement the naïve birthday attack of reduced SM3

**项目内容**

利用生日攻击的原理，找到关于sm3的部分bit的碰撞

**实验原理**

1.随机生成2^(n/2)个消息

2.调用库函数生成上述消息的hash值

3.寻找部分bit的碰撞（穷搜）

**代码说明**

见代码注释

**运行指导**

直接运行sm3_birthday_attack.py文件即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181408016-30f7a8a6-5d8a-449e-98b6-3b5d288595ba.png)
