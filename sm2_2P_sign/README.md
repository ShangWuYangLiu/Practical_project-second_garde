# implement sm2 2P sign with real network communication

**项目内容**

按照下图所示步骤，自行编写代码，要求在客户端实现签名的计算

![image](https://user-images.githubusercontent.com/105548921/181786953-afeb6dd5-4cb4-4b0e-82ef-fec5fa7f8e1a.png)

**代码说明**

1.关键是sm2的签名、验签和加解密的实现，签名验签函数在project 8：impl sm2 with RFC6979已经实现，加解密函数的实现参考了博客：https://blog.csdn.net/qq_33439662/article/details/122590298

2.客户端、服务器端的代码按照上图流程编写即可

**运行指导**

将new_sm2.py,sm2_2P_sign_client.py,sm2_2P_sign_server.py放在同一路径下，先运行sm2_2P_sign_server.py，后运行sm2_2P_sign_client.py

**运行结果**

(1)服务器端：

![image](https://user-images.githubusercontent.com/105548921/181787236-d58cb2a9-ae26-45c7-b2c6-d7b9bdf3e717.png)

(2)客户端：

![image](https://user-images.githubusercontent.com/105548921/181787341-265e0147-1ac8-4795-b06d-13122c91308e.png)

**参考文献**

[1] https://blog.csdn.net/qq_33439662/article/details/122590298
