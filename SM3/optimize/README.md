# do your best to optimize SM3 implementation (software)

**项目内容**

实现sm3的软件优化

**实验原理**

1.每一轮压缩函数优化：

  (1)初始化时，消息扩展只计算W0-W3四个32-bit字，在优化后的轮函数中首先计算W[i+4]，然后再计算W'[i]=W[i]^W[i+4]
  
  (2)计算中间变量TT2、TT1，过程如下图所示：
  
  ![image](https://user-images.githubusercontent.com/105548921/180443352-1e20cf24-8740-45a7-94fa-4eded0b1d448.png)
  
  (3)只更新B、D、F、H，过程如下图所示：
  
  ![image](https://user-images.githubusercontent.com/105548921/180443460-f5c81804-7436-48b0-bfaf-4cc79ec20ae6.png)

2.消息处理函数优化：

为了减少循环移位导致的不必要的赋值运算，可以将字的循环右移变更每轮输入字顺序的变动，且这个顺序变动会在4轮后还原，具体情况如下：[1]

![image](https://user-images.githubusercontent.com/105548921/180443726-ed1f9586-7a95-493d-acf3-e989a1335e8b.png)

3.预计算T[i]<<<i，储存在列表t中

**代码说明**

见代码注释

**运行指导**

将sm3.h作为头文件，运行sm3_optimize.cpp即可

**运行结果**

![image](https://user-images.githubusercontent.com/105548921/180443892-1c7397f5-d06f-4b79-a968-091867c75479.png)
