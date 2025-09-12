# K230视频编解码API参考

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

本文档主要介绍vicap 配置文件转换成bin 的使用方式

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
|------|------|
|      |      |
|      |      |

### 修订记录

| 文档版本号 | 修改者 | 日期 | 修改说明 |
|---|---|---|---|
| V1.0       | 系统软件部 | 2024.04.10 | 初版  |

## 概述

这个文档主要是介绍vicap中的配置文件转换成bin 的格式、为了节约vicap解析配置文件所消耗的时间

## 使用方式

下载最新的sdk、vicap 将配置文件转换成bin 的代码在如下路径：

```c
k230_sdk/src/big/mpp/userapps/sample/sample_vicap_transform_bin/
```

默认这个demo 是没有做编译的，需要自行增加demo 的配置到makefile 中

```c
@cd sample_vicap_transform_bin; make || exit 1
```

代码中主要就是调用一个api，api介绍如下：

```c
int kd_mpi_export_vicap_config_to_bin(char *path, char *config_name)
```

- path ：配置文件的路径（对应sensor 的xml、json文件的路径）。
- config_name ：配置文件的名称，可以参考 k_vicap_sensor_info 中database_name。

下边以imx335 1920x1080 的配置为例子：

```c
char *path = "/sharefs/sharefs/";
char *config_name = "imx335-1920x1080";
kd_mpi_export_vicap_config_to_bin(path, config_name);
```

运行结果如下：

```c
cfg_file is /sharefs/sharefs/imx335-1920x1080_manual.json
cfg_file is /sharefs/sharefs/imx335-1920x1080_auto.json
calib_file is /sharefs/sharefs/imx335-1920x1080_auto.json
illuminationNumber is 5 lscNumber 5 ccNumber 5 ecmNumber 3
bls num is 1 deGammaNumber is 1 cacNumber 1  dpfNumber is 1 dpccNumber is 1
ret = 409656
```

会打印要转换json 和xml 的路径，ret 的值是配置文件转换成bin文件的大小。运行结束后会在当前目录下生成一个bin 文件

```c
imx335-1920x1080_fastboot.bin           409656
```

将bin文件考到下边目录，从新编译镜像即可

```c
k230_sdk/src/big/mpp/userapps/src/sensor/config
```

烧录后，会在bin 下看见imx335-1920x1080_fastboot.bin 文件、然后在运行程序即可

```c
msh /sharefs/sharefs>ls /bin/
imx335-1920x1080_fastboot.bin
```
