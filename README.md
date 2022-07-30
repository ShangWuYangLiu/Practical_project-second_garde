# 山东大学网络空间安全学院（研究院）网络空间安全创新创业实践课程project-2022

**项目完成情况说明**

1.完成人：202000460012 刘阳     账户名称：ShangWuYangLiu

（共完成12个项目，其中标注为协作完成的项目是与张卓龙（账户名称：Zhang-SDU）共同完成）

2.各项目简介在各项目的README中

**已完成的项目**

1.implement the naïve birthday attack of reduced SM3（个人完成）

路径：SM3/birthday_attack

2.implement the Rho method of reduced SM3（个人完成）

路径：SM3/rho_method

3.implement length extension attack for SM3（个人完成）

路径：SM3/length_extension

4.do your best to optimize SM3 implementation (software)（协作完成:张卓龙阅读论文[1]及撰写小部分代码，刘阳完成代码撰写) 

路径：SM3/optimize

5.Impl Merkle Tree following RFC6962（协作完成:张卓龙阅读RFC文档及撰写小部分代码，刘阳完成代码撰写)

路径：merkle_tree

6.report on the application of this deduce technique in Ethereum with ECDSA（个人完成）

路径：deduce_technique

7.impl sm2 with RFC6979（个人完成）

路径：SM2

8.verify the above pitfalls with proof-of-concept cod（协作完成：刘阳完成算法上的推导，张卓龙完成代码撰写）

路径：pitfalls

9.implement sm2 2P sign with real network communication（个人完成）

路径：sm2_2P_sign

10.implement sm2 2P decrypt with real network communication（个人完成，[2]）

路径：sm2_2P_decrypt

11.PoC impl of the scheme, or do implement analysis by Google（个人完成）

路径：PoC（password check）

12.forge a signature to pretend that you are Satoshi（个人完成）

路径：forge_signature

**未完成的项目**

1.Try to Implement this scheme

2.Implement the above ECMH scheme

3.Implement a PGP scheme with SM2

4.send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself

5.research report on MPT

6.Find a key with hash value “sdu_cst_20220610” under a message composed of your name followed by your student ID. For example, “San Zhan 202000460001”.

7.Find a 64-byte message under some k fulfilling that their hash value is symmetrical.

8.Write a circuit to prove that your CET6 grade is larger than 425.

  a.Your grade info is like (cn_id, grade, year, sig_by_moe). These grades are published as commitments onchain by MoE.

  b.When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade.

  The commitment scheme used by MoE is SHA256-based.

  a. commit = SHA256(cn_id, grade, year, sig_by_moe, r)

**参考文献**

[1] 杨先伟,康红娟.SM3杂凑算法的软件快速实现研究[J].智能系统学报,2015,10(06):954-959.

[2] https://blog.csdn.net/qq_33439662/article/details/122590298
