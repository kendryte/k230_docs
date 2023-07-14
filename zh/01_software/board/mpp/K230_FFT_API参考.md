# K230 FFT API参考

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍 K230 FFT的使用，内容主要包括 FFT 的使用及测试程序介绍。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称    | 说明 |
| ----    | ---- |
| FFT | Fast Fourier Transform，离散傅里叶变换快速算法 |
| IFFT | Inverse fast Fourier transform，快速傅里叶逆变换 |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 王建新       | 2023-08-08 |

## 1. k230 fft介绍

K230 的FFT模块主要用于硬件加速FFT、IFFT的计算，其特性如下：

支持64、128、256、512、1024、2048、4096点fft、ifft计算。
支持int16计算精度，即输入输出的实部、虚部均为int16格式。
支持标准的axi4 slave接口，参数配置与数据搬移均使用该接口。
输入支持RIRI....、RRRR....（纯实部）、RRRR...IIII...格式排列，输出支持RIRI....、RRRR...IIII...格式排列。
采用基2-时间抽取的计算方式，内部只有一个蝶形算子。
采用单时钟域设计，总线时钟同时做为运算时钟，以节省跨时钟域的开销。
4096点fft/ifft的计算时长控制在1ms以内，包括数据搬移、计算、中断交互的总开销。
支持中断mask、原始中断查询。

## 2. API 参考

k230 FFT模块主要提供了以下 API：

- [k230_fft_ifft](#2.1 k230_fft_ifft)

### 2.1 k230_fft_ifft

【描述】

fft或者ifft计算。

【语法】

```c
int k230_fft_ifft(int point_num , fft_mode_e mode, fft_input_mode_e im, 
                fft_out_mode_e om,  k_u32 time_out , k_u16 shift , k_u16 dma_ch,
                short *rx_input, short *iy_input, short *rx_out, short *iy_out);
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| point_num   | 点数，有效值为64、128、256、512、1024、2048、4096 | 输入      |
| mode        | fft_mode_e FFT_MODE :fft  IFFT_MODE :ifft | 输入      |
| im          | fft_input_mode_e  输入模式 | 输入    |
| om | fft_out_mode_e 输出模式 | 输入 |
| time_out | 超时时间 | 输入 |
| shift | 偏移 | 输入 |
| dma_ch | dma通道  0-3有效；其他值非法 | 输入 |
| rx_input | 输入实数数据 | 输入 |
| iy_input | 输入虚数数据 | 输入 |
| rx_out | 计算结果实数数据 | 输出 |
| iy_out | 计算结果虚数数据 | 输出 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败 |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

无

【相关主题】

无

## 3. 调试及打印信息

写一个用户态应用程序 fft_main.c 来测试 fft功能。

测试代码已经写好，位于 mpp/userapps/sample/sample_fft/ 目录下，具体的调试方法如下：

1. 大小核启动之后，进入 */sharefs/app* 目录；
1. 运行 *./sample_fft.elf*  1 0 程序；
1. 打印信息。

具体的打印信息如下所示：

```text
msh /sharefs/app>./sample_fft.elf 1 0
-----fft ifft point 0064  -------
    max diff 0003 0001 
    i=0045 real  hf 0000  hif fc24 org fc21 dif 0003
    i=0003 imag  hf ffff  hif 0001 org 0000 dif 0001
-----fft ifft point 0064 use 133 us result: ok 


-----fft ifft point 0128  -------
    max diff 0003 0002 
    i=0015 real  hf 0001  hif fca1 org fc9e dif 0003
    i=0031 imag  hf 0001  hif fffe org 0000 dif 0002
-----fft ifft point 0128 use 121 us result: ok 


-----fft ifft point 0256  -------
    max diff 0003 0001 
    i=0030 real  hf 0000  hif fca1 org fc9e dif 0003
    i=0007 imag  hf ffff  hif 0001 org 0000 dif 0001
-----fft ifft point 0256 use 148 us result: ok 


-----fft ifft point 0512  -------
    max diff 0003 0003 
    i=0060 real  hf 0000  hif fca1 org fc9e dif 0003
    i=0314 imag  hf 0001  hif fffd org 0000 dif 0003
-----fft ifft point 0512 use 206 us result: ok 


-----fft ifft point 1024  -------
    max diff 0005 0002 
    i=0511 real  hf 0000  hif fc00 org fc05 dif 0005
    i=0150 imag  hf 0000  hif fffe org 0000 dif 0002
-----fft ifft point 1024 use 328 us result: ok 


-----fft ifft point 2048  -------
    max diff 0005 0003 
    i=1022 real  hf 0000  hif fc00 org fc05 dif 0005
    i=1021 imag  hf 0000  hif 0003 org 0000 dif 0003
-----fft ifft point 2048 use 574 us result: ok 


-----fft ifft point 4096  -------
    max diff 0005 0002 
    i=4094 real  hf 027b  hif 041f org 0424 dif 0005
    i=0122 imag  hf 0000  hif 0002 org 0000 dif 0002
-----fft ifft point 4096 use 1099 us result: ok 

```
