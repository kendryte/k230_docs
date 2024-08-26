# K230 SDK 更新nncase运行时库指南

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

[TOC]

## nncase运行时库版本问题说明

### 1. kmodel 版本说明

由于 `kmodel`中***没有包含nncase的版本信息***，因此无法直接判断 `kmodel`是由哪个版本的nncase生成。需自行进行版本信息管理，以下两种方式可供参考：

- 保留完整的编译工程(校正集，参数配置)，便于使用任意nncase版本生成 `kmodel`。
- 通过 `kmodel`的名字进行版本区分，示例代码如下：

  ```python
  with open("test.kmodel", "wb") as f:
      f.write(kmodel)

  # 将上面代码替换为以下内容
  import _nncase
  with open("test_{}.kmodel".format(_nncase.__version__), "wb") as f:
      f.write(kmodel)
  ```

### 2. 版本不兼容问题

由于nncase各版本之间可能存在不兼容的情况，而SDK中的nncase运行时库版本可能与编译 `kmodel`时使用的nncase版本不一致，从而导致上板推理时出现异常。因此最好在上板推理前，检查两者的版本是否匹配。

有以下两种方式可供确认版本信息是否匹配：

- 通过[版本对应关系表](./K230_SDK_nncase版本对应关系.md#k230-sdk-nncase版本对应关系)查询。
- 通过镜像名字确定两者的版本，例如 `k230_canmv_sdcard_v1.4_nncase_v2.8.0.img.gz`，其中 `v1.4` 表示SDK版本，`v2.8.0`表示 nncase 版本，即SDK-v1.4可以推理nncase-v2.8.0编译生成的 `kmodel`。
  镜像可通过[嘉楠开发者社区](https://developer.canaan-creative.com/resource)获取。

### 3. 版本不兼容解决办法

1. 与SDK版本对齐
   在确定好需要的nncase版本后，使用 `pip`进行安装，具体参考[nncase install](https://github.com/kendryte/nncase?tab=readme-ov-file#install)，之后重新编译`kmodel`。
1. 与nncase版本对齐
   在[nncase release界面](https://github.com/kendryte/nncase/releases)下载与编译 `kmodel`时nncase版本一致的运行时库，例如，"nncase_k230_v2.8.0_runtime.tgz"即为nncase-2.8.0的运行时库。之后按照以下步骤进行SDK中nncase运行时库版本更新：

   ```shell
   #0. 准备工作
   git clone https://github.com/kendryte/k230_sdk.git
   cd k230_sdk
   PATH_TO_K230_SDK=`pwd`
   make prepare_sourcecode
   # 注意检查该命令执行后是否存在以下文件夹
   # src/big/nncase/riscv64/nncase/

   #1. 解压nncase_k230_v2.8.0_runtime.tgz
   tar -xf nncase_k230_v2.8.0_runtime.tgz

   #2. 替换nncase运行时库
   cp -r nncase_k230_v2.8.0_runtime/* $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/

   #3. 检查nncase运行时库版本是否正确更新
   cat $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/include/nncase/version.h | grep NNCASE_VERSION
   > #define NNCASE_VERSION "2.8.0"
   ```

至此，SDK中的nncase运行时库版本已更新为nncase-2.8.0。如果需要更换其他版本，下载好对应版本的运行时库，按照上述步骤进行更新即可。
