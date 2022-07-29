#  forge a signature to pretend that you are Satoshi

**项目内容**

使用ECDSA算法在不验证消息的情况下伪造中本聪的签名

**实验原理**

1.随机选取两个元素a、b，其中a、b∈Fn*

2.按照下图所示，计算得出（r，s）（伪造的签名）

![image](https://user-images.githubusercontent.com/105548921/181241176-8dd3a193-f3ad-49b6-82f4-33296f683092.png)

注意：forge_signature.py中使用的公钥是代码随机生成的。

**代码说明**

见代码注释

**运行指导**

直接运行forge_signature.py文件即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/181724504-cd727734-2007-4389-a1ec-3d2d1f6337c5.png)
