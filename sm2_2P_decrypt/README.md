# implement sm2 2P decrypt with real network communication

**项目内容**

按照下图所示步骤，自行编写代码，要求在客户端实现服务器端加密的密文的解密

![image](https://user-images.githubusercontent.com/105548921/181768607-0ddcaecb-ea5b-469a-8f4f-a935bd92de22.png)

**代码说明**

1.关键是sm2的签名、验签和加解密的实现，签名验签函数在project 8：impl sm2 with RFC6979已经实现，加解密函数的实现参考了博客：https://blog.csdn.net/qq_33439662/article/details/122590298

2.客户端、服务器端的代码按照上图流程编写即可

**运行指导**

将new_sm2.py,sm2_2P_decrypt_client.py,sm2_2P_decrypt_server.py放在同一路径下，先运行sm2_2P_decrypt_server.py，后运行sm2_2P_decrypt_client.py

**运行结果**

1.服务器端：

![image](https://user-images.githubusercontent.com/105548921/181770095-6e7636aa-477b-4f6b-b187-72cf6d45e232.png)

2.客户端：

![image](https://user-images.githubusercontent.com/105548921/181770140-017882cd-31eb-4873-a91a-eaed9b2b1556.png)
