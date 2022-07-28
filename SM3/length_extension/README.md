# implement length extension attack for SM3

**项目内容**

实现sm3的长度扩展攻击

**实验原理**

1.首先计算原消息(msg)的hash值

2.在msg+padding之后附加一段消息,用原消息的hash值作为IV计算附加消息之后的hash值,得到消息扩展后的hash1,用以与攻击得到的hash值对比验证攻击是否成功

3.用sm3加密伪造后的整体消息，得到hash2

4.验证hash1与hash2是否相等

**代码说明**

见代码注释

**运行指导**

运行sm3_length_extension.py文件即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181410690-d509eb9f-a993-40eb-91ca-6831416e864c.png)
