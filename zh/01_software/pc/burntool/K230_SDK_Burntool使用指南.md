# K230 SDK Burntool使用指南

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

本文档描述了Tuning Tool的使用说明。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明                                                       |

### 修订记录

| 文档版本号  | 修改说明                           | 修改者 | 日期       |
|------------|-----------------------------------|--------|------------|
| V1.0       | 初版                              | jiangxiangbing | 2023-08-01 |
| V2.0       | 删除完整镜像烧录页，增加loader_sip.bin支持SIP烧录     | jiangxiangbing | 2023-10-12 |

## 1. Burntool烧录机制

1.K230芯片刚上电会执行固化在芯片ROM上的程序。当启动失败打印“boot failed with exit code xx”后，如果检测到USB0连接了USB线，ROM程序会进入USB烧录模式。
所以烧录时，建议把BOOTIO拨码到SD卡启动，同时不插SD卡，USB0连接typeC线。然后上电。此时电脑设备管理器可以看到K230 USB Boot Device

![k230_usb_boot_device](images/k230_usb_boot_device.png)

2.烧录工具会先通过USB通信把loader程序下载到K230的SRAM空间运行。该loader程序基于uboot开发，主要完成DDR training，以及DFU功能。

3.接下来就是DFU方式烧录各种存储介质，支持eMMC/norflash烧录。

## 2. 软件获取及安装

### 2.1 软件获取

[下载链接](https://kendryte-download.canaan-creative.com/k230/downloads/burn_tool/k230_burntool_v2.7z)

### 2.2 Windows系统环境安装

在系统没有K230 USB Boot Device驱动的情况下使用zadig-2.8.exe安装

![zadig](images/zadig.png)

## 3. 分区镜像烧录

### 3.1 界面各项说明

![interface_disc](images/interface_disc.png)

1. 选择是否烧录该分区
1. 配置分区起始地址，双击修改，地址都是字节偏移。地址与genimage的配置文件一致，例如emmc的镜像，镜像配置路径：k230_sdk/board/common/genimage-sdcard.cfg

    ```shell
        partition linux {
            #50M@30M   0x800@0x800
            offset = 30M
            image = "little-core/linux_system.bin"
            size = 50M
        }
    ```

    linux_system.bin 分区的起始地址为30MB，0x1E00000

    烧录由SDK编译生成的sysimage-sdcard.img和sysimage-spinor32m.img完整镜像，分区起始地址配置为0。

1. 配置分区名称，除了loader，其他名称可以随意，只要不重复即可，双击修改。
1. 分区镜像文件路径。
1. 选择分区镜像文件。loader使用压缩包内doc目录下提供的即可，需配置其分区名称固定为“loader”。loader的种类是由于DDR training程序不一样导致的。如果是SIP芯片设备，ddr training一样，loader选择k230_burntool_v2/doc/loader_sip.bin，如果是EVB LP3设备，loader选择k230_burntool_v2/doc/loader_evb_lp3.bin，如果使用unsip芯片的其他板子，则loader程序需要根据ddr training代码重新编译。
1. 选择emmc或norflash
1. 开始烧录，烧录单个设备可以采用这种方式。
1. 自动烧录，电脑可以通过USB连接多台K230设备，自动并行烧录。
