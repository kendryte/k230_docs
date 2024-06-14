# K230 Fancy POC介绍

![cover](../tutorials/images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../tutorials/images/logo.png)“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## K230 Fancy POC

### 概述

K230 Fancy Poc集合包括multimodal_chat_robot(多模态聊天机器人)、meta_human(数字人)、meta_hand(手势渲染)和finger_reader(指读)等项目，该工程旨在为客户提供POC搭建流程思路。

### 硬件环境

- `CanMV-K230-V1.x / CanMV-K230-V2.x / K230-UNSIP-LPx-EVB-V1.x`

### 源码位置

源码路径位于`k230_sdk/src/reference/fancy_poc`，目录结构如下：

```shell
.
├── ai_scale
├── build_app.sh
├── cmake
├── CMakeLists.txt
├── face_recognition
├── finger_reader
├── housekeeper
├── meta_hand
├── meta_human
├── multimodal_chat_robot
└── version
```

### 编译及运行程序

#### a.自编译上板镜像

- 确保已根据[k230 sdk官方说明](https://github.com/kendryte/k230_sdk)构建docker容器，并构建镜像
- 进入k230_sdk/src/reference/fancy_poc
- 执行build_app.sh，会生成相应大核、小核对应文件到k230_sdk/src/reference/fancy_poc/k230_bin目录
- 从k230_bin目录中选取所要参考的poc可执行文件，拷贝到开发板上。(每个POC对应的可执行程序可以参考每个POC下的readme)
- 每个POC上板所需的kmodel等二进制文件参考POC目录中的src/download.sh下载使用

#### b.直接下载官网上板镜像

（1）确保已根据[k230 sdk官方说明](https://github.com/kendryte/k230_sdk)构建docker容器

（2）从[官网资源库](https://developer.canaan-creative.com/resource)下载镜像

（3）环境准备

```bash
cd k230_sdk
make prepare_sourcecode #（若之前已执行，请忽略）
make mpp
#根据使用的开发板型号，分别执行不同的命令
#若是型号是CanMV-K230-V1.x，执行以下命令
make CONF=k230_canmv_defconfig prepare_memory
#若是型号是CanMV-K230-V2.x，执行以下命令
make CONF=k230_canmv_v2_defconfig prepare_memory
#若是型号是K230-xxx-xxx-EVB-V1.x，执行以下命令
make CONF=k230_evb_defconfig prepare_memory
cd k230_sdk/src/reference/fancy_poc
```

- 执行build_app.sh，会生成相应大核、小核对应文件到k230_sdk/src/reference/fancy_poc/k230_bin目录
- 从k230_bin目录中选取所要参考的POC可执行文件，拷贝到开发板上。(每个POC对应的可执行程序可以参考每个POC下的readme)
- 每个POC上板所需的kmodel等二进制文件参考POC目录中的src/download.sh下载使用
