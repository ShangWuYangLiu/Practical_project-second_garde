# PoC impl of the scheme, or do implement analysis by Google

**项目内容**

按照下图所示步骤，自行编写代码，要求实现根据用户提供的数据检测账户信息是否泄露的功能。

![image](https://user-images.githubusercontent.com/105548921/180647923-0b1df700-9da9-4914-95b3-71a84c89cde0.png)

**实验原理**

1.服务器端维护着自己的一个数据库，根据k的取值将数据库划分成几个大的集合

2.客户端向服务器发送（k，v），服务器根据客户端发送来的k在自己的数据库中进行检索，如果k是属于某一个集合的，服务器将（v^b，S）发送给客户端

3.客户端经过一些步骤处理后，确定自己的账户信息是否存在风险

**代码说明**

1.使用python实现，首先安装argon2-cffi库（pip install argon2-cffi）

2.原本的库函数实现过程中，salt的值是随机的，这会导致同样的message所得到的hash值不同，不便于我们实现上述功能，所以将库函数hash调用hash_secret参数中的salt改为固定值：b'7}\x1d\xdd\xd9Z\xfa\xb4\xecU\xd5\x85\x12\xfc\x17\x0f'

3.代码根据上图步骤编写即可，且在server.py和client.py中有详细的注释说明

**运行指导**

1.运行server.py

2.运行client.py

**测试结果**

1.用户随机生成自己的id和password进行测试，结果如下：

server.py运行结果：

![image](https://user-images.githubusercontent.com/105548921/181724067-6eda6cf6-31cd-46d5-aa0f-d26506b93d39.png)

client.py运行结果：

![image](https://user-images.githubusercontent.com/105548921/181724045-0ad53a22-7848-4d57-9973-fe5a2a1a9bec.png)

2.在服务器端中的数据库加入多次uid+password=‘xyK88tsD3XBBI3’和其hash值，用户也使用这个id和password进行测试（服务器端和客户端需要将注释为测试代码的部分取消注释，同时客户端要注释为随机情况的代码段注释掉），结果如下：

server.py运行结果：

![image](https://user-images.githubusercontent.com/105548921/181723965-aafa77a6-1aba-424c-9c03-c0dfc49db445.png)

client.py运行结果：

![image](https://user-images.githubusercontent.com/105548921/181723892-82f49634-71f4-4053-b64d-abffca7fc1c2.png)

