# K230 OpenCV开发指南

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

本文档主要介绍K230 在大核RTT端使用opencv调用板载摄像头的方法。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明                                                        |
|------|-------------------------------------------------------------|
| OpenCV  | Open Source Computer Vision Library                                |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 赵忠祥 | 2024-03-22 |

## 1.环境搭建

在 k230_sdk/src/big/mpp/userapps/src 下

```shell
git clone https://github.com/opencv/opencv.git
```

也可以把opencv先下载下来。放到

`k230_sdk/src/big/mpp/userapps/src/opencv`

补丁放在 k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0

```shell
cp k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0 k230_sdk/src/big/mpp/userapps/src/opencv/patch -r
```

v4.6.0复制为patch文件夹

在 opencv 根目录执行以下命令，应用补丁

```shell
git am ./patch/*.patch
```

不用理会警告。

## 2. 编译opencv

首先在 build.sh 路径确认工具链路径，打完patch build.sh即是正确的。

随后创建文件夹 build，在 build 目录中执行以下命令即可：

```shell
source ../build.sh
make -j
make install
```

在编译过程中，若终端未出现告警信息，则说明编译成功，编译完成的产物在 build/install 中，此文件即为 rt-smart 平台的 opencv 库文件。

## 3. 编译例程

修改 k230_sdk/src/big/mpp/userapps/sample/Makefile

将

```shell
#@cd opencv_camera_test; make || exit 1
```

修改为

```shell
@cd opencv_camera_test; make || exit 1
```

在k230_sdk下

```shell
make mpp-apps
```

在 k230_sdk\src\big\mpp\userapps\sample\elf 下面会生成 opencv_camera_test.elf文件。

将opencv_camera_test.elf 通过scp或nfs或直接copy至TF卡的方式，移至板端。

在大核执行

```shell
./opencv_camera_test.elf -D 101 -m 0 -d 0 -s 24 -c 0 -f 0 -W 1920 -H 1080
```

会在HDMI显示上显示ov5647采集的画面。
