# K230 SDK使用说明

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

本文档主要介绍K230 SDK 的安装和使用。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
|------|------|
|      |      |

### 修订记录

| 文档版本号 | 修改说明                   | 修改者 | 日期       |
| ---------- | -------------------------- | ------ | ---------- |
| V1.0       | 初版                       | 杨光   | 2023-03-10 |
| V1.1       | 新增安全镜像及emmc烧录说明    | 王建新 | 2023-04-07 |
| V1.2       | 新增spinor镜像烧录说明       | 王建新 | 2023-05-05 |
| V1.3       | 快起和安全镜像说明           | 王建新 | 2023-05-29 |
| V1.4       | 大核自启动程序说明           | 郝海波 | 2023-06-1  |
| v1.5       | usip lp4                  | 王建新 | 2023-06-12 |
| V1.6       | 修改大核自启动程序说明           | 赵忠祥 | 2023-06-28  |
| v1.7 | 增加启动介质分区章节,镜像烧录章节调整， | 王建新 | 2023-07-05 |

## 1. 概述

### 1.1 SDK软件架构概述

K230 SDK 是面向K230 开发板的软件开发包，包含了基于Linux&RT-smart 双核异构系统开发需要用到的源代码，工具链和其他相关资源。

K230 SDK 软件架构层次如图 1-1 所示：

![logo](images/cee49715351f6dd3496baf19af1262ed.png)

图1-1 K230 SDK 软件架构图

## 2. 开发环境搭建

### 2.1 支持的硬件

K230-USIP-LP3-EVB：具体硬件信息参考 《K230-USIP-LP3-EVB-硬件使用说明》

K230-USIP-LP4-EVB：具体硬件信息参考 《K230-USIP-LP4-EVB-硬件使用说明》

K230-SIP-EVB：具体硬件信息参考 《K230_硬件设计指南》

k230-pi(canmv):具体硬件信息参考 《K230_硬件设计指南》

### 2.2 开发环境搭建

#### 2.2.1 编译环境

| 主机环境                    | 描述                                                 |
|-----------------------------|------------------------------------------------------|
| Docker编译环境              | SDK提供了dockerfile，可以生成docker镜像，用于编译SDK |
| Ubuntu 20.04.4 LTS (x86_64) | SDK可以在ubuntu 20.04环境下编译                      |

K230 SDK需要在linux环境下编译，SDK支持docker环境编译，SDK开发包中发布了docker file（`tools/docker/Dockerfile`），可以生成docker镜像。具体dockerfile使用和编译步骤，详见4.3.1章节。

SDK使用的Docker 镜像以ubuntu 20.04 为基础，如果不使用docker编译环境，可以在ubuntu 20.04 主机环境下参考dockerfile的内容，安装相关HOST package和工具链后，编译SDK。

K230 SDK没有在其他Linux版本的主机环境下验证过，不保证SDK可以在其他环境下编译通过。

#### 2.2.2 SDK开发包

K230 SDK以压缩包的形式发布，或者自己使用`git clone https://github.com/kendryte/k230_sdk`命令下载。

### 2.3 单板准备

本章节以K230-USIP-LP3-EVB为例

请准备如下硬件：

- K230-USIP-LP3-EVB
- Typec USB线  至少2根
- TypeC USB 转以太网转换器(可选)
- 网线一根(可选)
- SD卡(可选)

说明：TypeC USB 转以太网推荐型号是<https://item.jd.com/5326738.html>

参考《K230-USIP-LP3-EVB-硬件使用说明》准备开发板。

K230 EVB通过USB提供两路调试串口，windows下使用调试串口，需要安装USB转串口驱动程序，驱动下载链接如下：

<https://ftdichip.com/wp-content/uploads/2021/11/CDM-v2.12.36.4.U-WHQL-Certified.zip>

安装了驱动后，板子上电，PC使用type C数据线连接EVB的调试串口后，可以发现两个USB串口设备，如下图所示：

![图形用户界面, 文本, 应用程序 描述已自动生成](images/bcb6636268b91758f87ff54523251eeb.png)

图2-1 USB串口设备

以上图为例，`COM47`为小核的调试串口，`COM48`为大核的调试串口。

串口波特率设置： `115200 8N1`

## 3. SDK 安装准备工作

### 3.1 安装SDK

K230 SDK开发包采用压缩包的方式发布，在linux环境下使用。

### 3.2 SDK 目录结构

K230 SDK目录结构如下图所示：

```shell
k230_sdk
├── configs
│   ├── k230_evb_defconfig
│   └── k230_evb_usiplpddr4_defconfig
│   └── k230d_defconfig
├── Kconfig
├── LICENSE
├── Makefile
├── parse.mak
├── README.md
├── repo.mak
├── src
│   ├── big
│   │   ├── mpp
│   │   ├── rt-smart
│   │   └── unittest
│   ├── common
│   │   ├── cdk
│   │   └── opensbi
│   ├── little
│   │   ├── buildroot-ext
│   │   ├── linux
│   │   └── uboot
│   └── reference
│       ├── ai_poc
│       ├── business_poc
│       └── fancy_poc
├── board
│   ├── common
│   │   ├── env
│   │   └── gen_image_cfg
│   │   ├── gen_image_script
│   │   └── post_copy_rootfs
│   ├── k230_evb_doorlock
│   └── k230_evb_peephole_device
└── tools
    ├── docker
    │   └── Dockerfile
    ├── doxygen
    ├── firmware_gen.py
    └── get_download_url.sh
```

各个目录用途描述如下：

- `configs`： 存放SDK的板级默认配置，主要包含如下信息：参考板类型，toolchain路径，

    内存布局规划，存储规划配置等

- `src`：源代码目录，分为 大核代码（`big`），公共组件（`common`），小核代码（`little`）三个目录。

    大核代码包含：`rt-smart`操作系统代码，`mpp`代码，`unittest`代码

    公共组件包含：`cdk`代码和`opensbi`代码

    小核代码包含：`linux`内核代码，`buildroot`代码，`uboot`代码

- `tools`：存放各种工具，脚本等。例如`kconfig`，`doxygen`，`dockerfile`等
- `board`：环境变量、镜像配置文件、文件系统等

## 4. SDK 编译

### 4.1 SDK 编译介绍

K230 SDK支持一键编译大小核操作系统和公共组件，生成可以烧写的镜像文件，用于部署到开发板启动运行。设备上linux系统的用户名是root无密码；

### 4.2 SDK 配置

K230 SDK采用Kconfig作为SDK配置接口，默认支持的板级配置放在configs目录下。

#### 4.2.1 配置文件说明

`k230_evb_defconfig` ：基于K230 USIP LP3 EVB的默认SDK配置文件
`k230_evb_usiplpddr4_defconfig` ：基于K230 USIP LP4 EVB的默认SDK配置文件
`k230d_defconfig` ：基于K230-SIP-EVB的默认SDK配置文件
`k230_evb_nand_defconfig` ：基于K230 USIP LP3 EVB会生成nand镜像的默认SDK配置文件
`k230_canmv_defconfig` ：基于K230-PI(canmv)的默认SDK配置文件
`k230_evb_doorlock_defconfig` ：基于K230 USIP LP3 EVB的门锁poc默认SDK配置文件
`k230_evb_peephole_device_defconfig` ：基于K230 USIP LP3 EVB的猫眼POC
`k230d_doorlock_defconfig` ：基于K230-SIP-EVB的门锁POC

### 4.3 编译 SDK

#### 4.3.1 编译步骤

说明：本章节命令仅供参考，文件名请根据实际情况进行替换。
Setp 1：下载代码

`git clone https://github.com/kendryte/k230_sdk`

Step 2：进入SDK根目录

`cd k230_sdk`

Step 3：下载toolchain

```shell
source tools/get_download_url.sh && make prepare_sourcecode
```

>`make prepare_sourcecode` will download both Linux and RT-Smart toolchain, buildroot package and AI package from Microsoft Azure cloud server with CDN, the download cost time may based on your network connection speed.

Step 4：生成docker镜像（第一次编译需要，已经生成docker镜像后跳过此步骤）

`docker build -f tools/docker/Dockerfile -t k230_docker tools/docker`

Step 5: 进入docker环境，

`docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash`

Step 6: Docker环境下执行下面命令进行编译SDK

```bash
make CONF=k230_evb_defconfig  #编译K230-USIP-LP3-EVB板子镜像
#make CONF=k230_evb_usiplpddr4_defconfig  #编译K230-USIP-LP4-EVB板子镜像
#make CONF=k230d_defconfig  #编译K230-SIP-EVB板子镜像
#make CONF=k230_evb_nand_defconfig  #编译K230-USIP-LP3-EVB板子nand镜像
```

> 编译K230-USIP-LP4-EVB板子镜像使用`make CONF=k230_evb_usiplpddr4_defconfig`命令
> 编译K230-USIP-LP3-EVB板子镜像使用`make CONF=k230_evb_defconfig`  命令。
> 编译K230-SIP-EVB板子镜像使用`make CONF=k230d_defconfig`  命令。
> 编译K230-USIP-LP3-EVB板子的nand镜像使用 `make CONF=k230_evb_nand_defconfig`  命令

备注：
当编译k230d_defconfig镜像需要替换k230_sdk\src\big\mpp\kernel\lib\libvo.a。替换方法如下：
下载
<https://kendryte-download.canaan-creative.com/k230/downloads/mpp_lib/libvo_k230d.a>

替换
先备份一份libvo.a，然后将下载的libvo_k230d.a 替换成 libvo.a。重新编译即可

#### 4.3.2 编译输出产物

编译完成后，在`output/xx_defconfig/images`目录下可以看到编译输出产物。

![文本 描述已自动生成](images/da6d48091ee0af8107a63cde01a2b75b.png)

图4-1 编译产物

`images`目录下镜像文件说明如下：

`sysimage-sdcard.img` -------------是sd和emmc的非安全启动镜像；

`sysimage-sdcard.img.gz` --------是SD和emmc的非安全启动镜像压缩包(sysimage-sdcard.img文件的gzip压缩包)，烧录时需要先解压缩。

`sysimage-sdcard_aes.img.gz`是SD和emmc的aes安全启动镜像压缩包，烧录时需要先解压缩。

`sysimage-sdcard_sm.img.gz`是SD和emmc的sm安全启动镜像压缩包，烧录时需要先解压缩。

安全镜像默认不会产生，如果需要安全镜像请参考4.3.4使能安全镜像。

大核系统的编译产物放在`images/big-core`目录下。

小核系统的编译产物放在`images/little-core`目录下。

#### 4.3.3 非快起镜像

sdk默认编译的是快起镜像(uboot直接启动系统，不会进入uboot命令行)，如果需要进入uboot命令行，请参考下面取消`CONFIG_QUICK_BOOT`配置：

在sdk主目录 执行 `make menuconfig` ，选择`board configuration`，取消`quick boot` 配置选项。

非快起系统变快起系统方法：进入uboot命行执行`setenv quick_boot true;saveenv;`

#### 4.3.4 安全镜像

sdk默认不产生安全镜像，如果需要安全镜像，请参考下面增加CONFIG_GEN_SECURITY_IMG配置：

在sdk主目录 执行`make menuconfig` ，选择`board configuration`，配上`create security image` 选项。

#### 4.3.5 debug镜像

sdk默认产生release镜像，如果需要调试镜像，请参考下面增加CONFIG_BUILD_DEBUG_VER配置：

在sdk主目录 执行`make menuconfig` ，选择`build debug/release version`，配上`debug` 选项。

## 5. SDK 镜像烧写

### 5.1 sd卡镜像烧录

#### 5.1.1 ubuntu下烧录

在sd卡插到宿主机之前，输入：

`ls -l /dev/sd\*`

查看当前的存储设备。

将sd卡插入宿主机后，再次输入：

`ls -l /dev/sd\*`

查看此时的存储设备，新增加的就是 sd 卡设备节点。

假设/dev/sdc 就是 sd卡设备节点，执行如下命令烧录SD卡：

`sudo dd if=sysimage-sdcard.img of=/dev/sdc bs=1M oflag=sync`

说明：`sysimage-sdcard.img`可以是`images`目录下的`sysimage-sdcard.img`文件，或者`sysimage-sdcard_aes.img.gz`、`sysimage-sdcard.img.gz`、`sysimage-sdcard_sm.img.gz`文件解压缩后的文件。

#### 5.1.2 Windows下烧录

Windows下可通过balena Etcher工具对sd卡进行烧录（balena Etcher工具下载地址<https://www.balena.io/etcher/>）。

1）将TF卡插入PC，然后启动balena Etcher工具，点击工具界面的"Flash from file”按钮，选择待烧写的固件，如下图。

![图形用户界面, 应用程序 描述已自动生成](images/3e2358e04601c3e03bf233c84f8b3ec4.png)

图5-1 选择固件

2）点击工具界面的“Select target”按钮，选择目标sdcard卡。

![图形用户界面, 文本, 应用程序 描述已自动生成](images/4d9f7101ce0225108752d4cae16c9663.png)

图5-2 选择SD卡

3）点击“Flash”按钮开始烧写，烧写过程有进度条展示，烧写结束后会提示Flash Finish。

4）当烧录完成后，将SD卡插入开发板卡槽，选择 BOOT为从SD启动，最后开发板上电即可从SD卡启动。

![手机屏幕的截图 描述已自动生成](images/84c28ea8eb1de88fe5b4a1b2c122767d.jpg)

图5-3 开始烧录

![图形用户界面, 应用程序 描述已自动生成](images/578b62c404f1f18af8c6aa342e5830b5.jpg)

图5-4 烧录完成

说明：使用`sysimage-sdcard_aes.img.gz`、`sysimage-sdcard.img.gz`、`sysimage-sdcard_sm.img.gz`文件时需要先解压缩，烧录解压缩后的文件。

### 5.2 Emmc镜像烧写参考

#### 5.2.1 Linux下烧写emm参考

1)把镜像的压缩包下载到sd卡

从sd卡启动linux，在linux下可以参考如下命令把镜像的压缩包下载到sd卡

```shell
ifconfig eth0 up;udhcpc;mount /dev/mmcblk1p4 /mnt;cd /mnt/;

scp wangjianxin@10.10.1.94:/home/wangjianxin/k230_sdk/output/k230_evb_defconfig/images/sysimage-sdcard.img.gz  .
```

2)把压缩包解压缩到emmc

`gunzip sysimage-sdcard.img.gz -c >/dev/mmcblk0`

3)切成emmc启动，重启板子

#### 5.2.1 Uboot下烧写emmc参考

1）把ssysimage-sdcard.img.gz镜像下载到内存。

```bash
usb start; dhcp;  tftp 0x900000010.10.1.94:wjx/sysimage-sdcard.img.gz;
 #注意：需要根据内存大小替换下0x9000000，比如内存只有128M的话，可以替换为0x2400000 
```

2）把镜像写到emmc

```bash
gzwrite mmc  0   0x${fileaddr}  0x${filesize};
```

3）重启板子

### 5.3 Spinor镜像烧写参考

#### 5.3.1 Uboot下烧写参考

1）把sysimage-spinor32m.img镜像下载到内存。

`usb start; dhcp; tftp 0x9000000 10.10.1.94:wjx/sysimage-spinor32m.img;
 #注意：需要根据内存大小替换下0x9000000，比如内存只有128M的话，可以替换为0x2400000

2）把镜像写到spi nor flash

`sf probe 0:0;sf erase 0 0x2000000;sf write 0x$fileaddr 0 0x$filesize; sf remove;`

3）重启板子

#### 5.3.2 linux烧写spinor

1)把spinor镜像sysimage-spinor32m.img下载到sd卡

从sd卡启动linux，在linux下可以参考如下命令把镜像到sd卡

```bash
ifconfig eth0 up; udhcpc; mount /dev/mmcblk1p4 /mnt;cd /mnt/;
scp wangjianxin@10.10.1.94:/home/wangjianxin/k230_sdk/output/k230_evb_defconfig/images/sysimage-spinor32m.img  .
```

2)参考下面命令把镜像写入spi nor flash

```bash
[root@canaan /mnt ]#flashcp -v sysimage-spinor32m.img  /dev/mtd9
Erasing blocks: 508/508 (100%)
Writing data: 32512k/32512k (100%)
Verifying data: 32512k/32512k (100%)
[root@canaan /mnt ]#
```

3)切成spi nor启动，重启板子

#### 5.3.3 Spinor镜像说明

由于spinor flash比较小， linux删掉了ko、rtt删掉了部分demo程序。

### 5.4. Spinand镜像烧写参考

#### 5.4.1 Uboot下烧写参考

1）把sysimage-spinand32m.img镜像下载到内存。

`usb start; dhcp;  tftp 0x9000000 10.10.1.94:wjx/sysimage-spinand32m.img;`

2）把镜像写到spi nand flash

`mtd erase spi-nand0 0 0x2000000;mtd write spi-nand0 0x$fileaddr  0 0x$filesize;`

3）重启板子

## 6. sdk启动介质分区及修改

### 6.1 spi nor

#### 6.1.1 spi nor默认分区

![image-spi_nor_default_part](images/image-spi_nor_default_part.png)

| spinor分区    |           |          |        |         |
| ------------- | --------- | -------- | ------ | ------- |
| 内容          | 开始地址  | 大小     | 大小MB | 大小    |
| 一级uboot     | 0x0       | 512KB    | 0.5    | 512KB   |
| 二级uboot     | 0x80000   | 0x160000 | 1.375  | 1.375MB |
| uboot环境变量 | 0x1e0000  | 128KB    | 0.125  | 128KB   |
| 快起参数      | 0x200000  | 512KB    | 0.5    | 512KB   |
| 人脸特性      | 0x280000  | 512kB    | 0.5    | 512kB   |
| 标定参数      | 0x300000  | 256KB    | 0.25   | 256KB   |
| ai模型        | 0x340000  | 3MB      | 3      | 3MB     |
| 散斑          | 0x640000  | 2MB      | 2      | 2MB     |
| rtt           | 0x840000  | 0x1c0000 | 1.75   | 1.75MB  |
| rtapp         | 0xa00000  | 0x5c0000 | 5.75   | 3.75MB  |
| linux         | 0xfc0000  | 0x700000 | 7      | 7MB     |
| rootfs        | 0x16c0000 | 0xb00000 | 13     | 13MB    |

#### 6.1.2 分区修改及实现说明

在sdk主目录执行 make menuconfig --->storage configurations--->spi nor partion config 进行分区修改(界面如下)；修改完后执行下make build-image;

![image-image-menuconfig_spi_nor_part](images/image-menuconfig_spi_nor_part.png)

通过menuconfig修改分区详细实现说明：

make menuconfig配置完后会生成.config(部分内容如下)

```bash
CONFIG_SPI_NOR_SENSOR_CFG_CFG_BASE=0x300000
CONFIG_SPI_NOR_SENSOR_CFG_CFG_SIZE=0x40000
CONFIG_SPI_NOR_AI_MODE_CFG_BASE=0x340000
CONFIG_SPI_NOR_AI_MODE_CFG_SIZE=0x300000
CONFIG_SPI_NOR_SPECKLE_CFG_BASE=0x640000
CONFIG_SPI_NOR_SPECKLE_CFG_SIZE=0x200000
CONFIG_SPI_NOR_RTTK_BASE=0x840000
CONFIG_SPI_NOR_RTTK_SIZE=0x1c0000
CONFIG_SPI_NOR_RTT_APP_BASE=0xa00000
CONFIG_SPI_NOR_RTT_APP_SIZE=0x5c0000
CONFIG_SPI_NOR_LK_BASE=0xfc0000
CONFIG_SPI_NOR_LK_SIZE=0x700000
CONFIG_SPI_NOR_LR_BASE=0x16c0000
CONFIG_SPI_NOR_LR_SIZE=0x900000
```

tools/menuconfig_to_code.sh 脚本会根据这些定义动态(关键脚本如下)修改linux设备树和board/common/gen_image_cfg/genimage-spinor.cfg文件；

```bash
image sysimage-spinor32m.img {
    flash  {}
    flashtype = "spinor-32M-gd25lx256e"
    .....
    partition quick_boot_cfg {
        offset = ${CONFIG_SPI_NOR_QUICK_BOOT_CFG_BASE}
        image = "${quick_boot_cfg_data_file}"
        size = ${CONFIG_SPI_NOR_QUICK_BOOT_CFG_SIZE}
    }

    partition face_db {
        offset = ${CONFIG_SPI_NOR_FACE_DB_CFG_BASE}
        image = "${face_database_data_file}"
        size = ${CONFIG_SPI_NOR_FACE_DB_CFG_SIZE}
    }

    partition sensor_cfg {
        offset = ${CONFIG_SPI_NOR_SENSOR_CFG_CFG_BASE}
        image = "${sensor_cfg_data_file}"
        size = ${CONFIG_SPI_NOR_SENSOR_CFG_CFG_SIZE}
    }

    partition ai_mode {
        offset = ${CONFIG_SPI_NOR_AI_MODE_CFG_BASE}
        image = "${ai_mode_data_file}"
        size = ${CONFIG_SPI_NOR_AI_MODE_CFG_SIZE}
    }

    partition speckle_cfg {
        offset = ${CONFIG_SPI_NOR_SPECKLE_CFG_BASE}
        image = "${speckle_data_file}"
        size = ${CONFIG_SPI_NOR_SPECKLE_CFG_SIZE}
    }

    partition rtt {
        offset = ${CONFIG_SPI_NOR_RTTK_BASE}
        image = "big-core/rtt_system.bin"
        size = ${CONFIG_SPI_NOR_RTTK_SIZE}
    }
    partition rtt_app {
        offset = ${CONFIG_SPI_NOR_RTT_APP_BASE}
        image = "${rtapp_data_file}"
        size = ${CONFIG_SPI_NOR_RTT_APP_SIZE}
    }

    partition linux {
        offset = ${CONFIG_SPI_NOR_LK_BASE}
        image = "little-core/linux_system.bin"
        size = ${CONFIG_SPI_NOR_LK_SIZE}
    }
    partition rootfs_ubi {
        offset = ${CONFIG_SPI_NOR_LR_BASE}
        image = "rootfs.ubi"
        size = ${CONFIG_SPI_NOR_LR_SIZE}
    }
}
```

最后genimage 会解析board/common/gen_image_cfg/genimage-spinor.cfg 文件并生成正确的镜像。

```bash
genimage --rootpath little-core/rootfs/ --tmppath genimage.tmp --inputpath images --outputpath images
--config board/common/gen_image_cfg/genimage-spinor.cfg
```

#### 6.1.3分区数据格式及生成过程

目前快起参数、人脸特性、标定参数、ai模型、散斑、rtt、rtapp等参数分区的数据均不加密，其格式及生成过程如下：

![image-20230705151949318](images/image-non_crypt.png)

主要生成脚本如下：

```bsh
#更详细的生成细节请阅读 board/common/gen_image_script/gen_image_comm_func.sh 脚本的gen_cfg_part_bin函数
${k230_gzip} -f -k ${filename}  #gzip
sed -i -e "1s/\x08/\x09/"  ${filename}.gz
#add uboot head
${mkimage} -A riscv -O linux -T firmware -C gzip -a ${add} -e ${add} -n ${name}  -d ${filename}.gz  ${filename}.gzu;
python3  ${firmware_gen}   -i ${filename}.gzu -o fh_${filename} ${arg}; #add k230 firmware head

对应执行过程打印如下：
## + k230_priv_gzip -n8 -f -k speckle.bin
## + sed -i -e '1s/\x08/\x09/' speckle.bin.gz
## + mkimage -A riscv -O linux -T firmware -C gzip -a 0x14040000 -e 0x14040000 -n speckle -d speckle.bin.gz speckle.bin.gzu
## Image Name:   speckle
## Created:      Wed Jul  5 15:37:49 2023
## Image Type:   RISC-V Linux Firmware (gzip compressed)
## Data Size:    45 Bytes = 0.04 KiB = 0.00 MiB
## Load Address: 14040000
## Entry Point:  14040000
## + python3 /home/wangjianxin/k230_sdk/tools/firmware_gen.py -i speckle.bin.gzu -o fh_speckle.bin -n
## the magic is:  b'K230'
## ----- NO ENCRYPTION + HASH-256 -----
## the encryption type:  0
## mesg_hash:  b'3543e2038aedad88a29f8ee98983064367cc79f6e709ed7571df9b391884b8b1'
```

uboot启动的时候会解析校验参数分区(快起参数、人脸特性、标定参数、ai模型、散斑、rtt、rtapp)数据,并把解析后的原始数据读到内存的正确位置。

各个参数分区在内存的位置可以通过make menuconfig--Memory configuration进行配置(参考界面如下)

![image-20230705153242437](images/image-memconfig_part.png)

#### 6.1.4 rtapp和ai mode分区特殊说明

rtapp分区的app不能重复执行，设计这个分区的目的是节省内存，这个分区的app执行一遍后内存可能会被释放掉，不能重复执行；

编译的时候会把大核romfs文件系统里面模型文件的指针修改到ai模型区域(见下面脚本)，使用方法和普通文件一样使用就行。

```bash
#详见board/common/gen_image_script/gen_image.sh 文件
for f in ${all_kmode};
    do
        eval fstart="\${${f%%\.*}_start}"
        eval fsize="\${${f%%\.*}_size}"
        fstart=$(printf "0x%x" $((${fstart} + ${CONFIG_MEM_AI_MODEL_BASE})))
        fsize=$(printf "0x%x" ${fsize})
        sed -i "s/_bin_$f,/(char*)${fstart},/g" ${RTSMART_SRC_DIR}/kernel/bsp/maix3/applications/romfs.c
        sed -i "s/sizeof(_bin_$f)/${fsize}/g" ${RTSMART_SRC_DIR}/kernel/bsp/maix3/applications/romfs.c
    done
```

#### 6.1.5 spi nor验证过的型号

gd25lx256e

### 6.2 sd和emmc

#### 6.2.1 sd和emmc默认分区

![image-20230705100321637](images/sd_emmc默认分区.png)

| SD、emmc卡默认分区 |           |            |        |       |
| ------------------ | --------- | ---------- | ------ | ----- |
| 内容               | 开始地址  | 大小值     | 大小MB | 大小  |
| mbr分区表          | 0x0       | 0x100000   | 1      | 1MB   |
| 一级uboot          | 0x100000  | 0x80000    | 0.5    | 512KB |
| 备用一级boot       | 0x180000  | 0x60000    | 0.375  | 384KB |
| uboot环境变量      | 0x1e0000  | 0x20000    | 0.125  | 128KB |
| 二级uboot          | 0x200000  | 0x800000   | 0.5    | 8MB   |
| rtt                | 0xa00000  | 0x1400000  | 20     | 20MB  |
| linux              | 0x1e00000 | 0x6200000  | 98     | 98MB  |
| rootfs             | 0x8000000 | 0x5000000  | 80     | 80MB  |
| 测试分区           | 0xd000000 | 0x10000000 | 256    | 256MB |

#### 6.2.2 sd和emmc分区修改

如果需要分区请修改board/common/gen_image_cfg/genimage-sdcard.cfg 文件，修改完后执行下make build-image

### 6.3 spi nand

#### 6.3 spi nand默认分区

![image-20230705111015174](images/image-spi_nand_part.png)

| spinand分区   |           |          |           |        |         |
| ------------- | --------- | -------- | --------- | ------ | ------- |
| 内容          | 开始地址  | 大小     | 开始地址  | 大小MB | 大小    |
| 一级uboot     | 0x0       | 512KB    | 0x0       | 0.5    | 512KB   |
| 二级uboot     | 0x80000   | 0x160000 | 0x80000   | 1.375  | 1.375MB |
| uboot环境变量 | 0x1e0000  | 128KB    | 0x1e0000  | 0.125  | 128KB   |
| rtt           | 0x200000  | 0x800000 | 0x200000  | 8      | 8MB     |
| linux         | 0xa00000  | 0x700000 | 0xa00000  | 7      | 7MB     |
| rootfs        | 0x1100000 | 0xf00000 | 0x1100000 | 15     | 15MB    |

#### 6.3.2 spi nand分区修改

如果需要分区请修改board/common/gen_image_cfg/genimage-spinand.cfg 文件，修改完后执行下make build-image

#### 6.3.4  spi nand验证过的型号

w25n01gw

## 7. SDK内存配置

在k230_sdk下运行`make menuconfig->Memory configuration`可以配置各个区域使用的内存空间，也可以直接编译configs/k230_evb_defconfig修改，各区域说明如下

``` shell
CONFIG_MEM_TOTAL_SIZE="0x20000000"      #内存总体容量          不支持配置
CONFIG_MEM_PARAM_BASE="0x00000000"      #参数分区起始地址       不支持配置
CONFIG_MEM_PARAM_SIZE="0x00100000"      #参数分区大小           不支持配置
CONFIG_MEM_IPCM_BASE="0x00100000"       #核间通讯起始地址       不支持配置
CONFIG_MEM_IPCM_SIZE="0x00100000"       #核间通讯共享内存大小    不支持配置
CONFIG_MEM_RTT_SYS_BASE="0x00200000"    #大核RTT起始地址        支持配置
CONFIG_MEM_RTT_SYS_SIZE="0x07E00000"    #大核RTT使用的地址范围   支持配置
CONFIG_MEM_AI_MODEL_BASE="0x1FC00000"   #AI模型加载起始地址      支持配置
CONFIG_MEM_AI_MODEL_SIZE="0x00400000"   #AI模型加载地址区域      支持配置
CONFIG_MEM_LINUX_SYS_BASE="0x08000000"  #小核linux起始地址       支持配置
CONFIG_MEM_LINUX_SYS_SIZE="0x08000000"  #小核linux地址区域       支持配置
CONFIG_MEM_MMZ_BASE="0x10000000"        #mmz共享内存其实地址     支持配置
CONFIG_MEM_MMZ_SIZE="0x0FC00000"        #mmz 共享内存区域       支持配置
CONFIG_MEM_BOUNDARY_RESERVED_SIZE="0x00001000"  #隔离区         不支持配置
```

## 8. SDK单板调试

### 8.1 调试前准备

1.从 T-Head 公 司 的 OCC 平 台<https://occ.t-head.cn/community/download>下载`T-Head-DebugServer`软件和《DebugServer User Guide v5.6》，并参考《DebugServer User Guide v5.6》在pc电脑上安装`T-Head-DebugServer`软件；

![图形用户界面, 文本, 应用程序 描述已自动生成](images/830f7333997768ba1fa01e69aedeeb88.png)

![图形用户界面, 文本, 应用程序, 电子邮件 描述已自动生成](images/a3ee5b66a56b295c092465fec74ed086.png)

2.准备下图所示平头哥 cklink、usb线、k230 evb板

![图片包含 游戏机, 电缆, 电路 描述已自动生成](images/8e91f1cc85daee080e3de5f875542bc8.png)

### 8.2 调试

1.参考下图把cklink 、k230 evb板子、pc电脑 连接起来，随后给evb上电。

![电子仪器被放在电脑旁边 中度可信度描述已自动生成](images/cc18bccbf8054dde022db7f9c07df307.png)

2.电脑上打开第1步安装的T-HeadDebugServer软件，看到类似如下图打印说明连接成功，如果连接失败请参考《DebugServer User Guide v5.6》排查失败原因。

![文本 描述已自动生成](images/33d48fa7906e4bf8a0aed4aad7c28178.png)

3.在编译代码的服务器上启动riscv64-unknown-linux-gnu-gdb执行target remote xx.xx.xx.xx1025 命令连接板子,连接成功后进行gdb调试。

![文本 描述已自动生成](images/2fed09a9dbe48eeeb639b6f977861c77.png)

## 9. SDK启动

当前版本默认编译生成的镜像，烧录到板子上后，大核会自动运行一个程序。

SDK V0.7版本的自启动程序为基于OV9732摄像头的人脸检测程序，启动后可以在大核的控制台端输入'q'退出该程序。

若使用的EVB板没有连接OV9732，则该自启动程序会报错，同样在大核的控制台端输入'q'退出该程序。
若需要取消大核的自启动功能，需将 `k230_sdk/src/big/rt-smart/init.sh` 中的内容注释掉。

SDK V0.8版本的自启动程序是基于IMX335摄像头（板载晶振）的人脸检测程序，启动后在大核的控制台输入'q'可以退出程序。

同样的，如果没有连接IMX335，则自启动程序报错，程序自动退出。按回车即可回到控制台。
