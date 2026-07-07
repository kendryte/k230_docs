# K230 SDK 更新nncase运行时库指南

## nncase运行时库版本问题说明

### kmodel 版本说明

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

### 版本不兼容问题

由于nncase各版本之间可能存在不兼容的情况，而SDK中的nncase运行时库版本可能与编译 `kmodel`时使用的nncase版本不一致，从而导致上板推理时出现异常。因此最好在上板推理前，检查两者的版本是否匹配。

有以下两种方式可供确认版本信息是否匹配：

- 通过[版本对应关系表](./K230_SDK_nncase_version_correspondence.md#k230-sdk-nncase-version-mapping)查询。
- 通过镜像名字确定两者的版本，例如 `k230_canmv_sdcard_v1.4_nncase_v2.8.0.img.gz`，其中 `v1.4` 表示SDK版本，`v2.8.0`表示 nncase 版本，即SDK-v1.4可以推理nncase-v2.8.0编译生成的 `kmodel`。
  镜像可通过[勘智开发者社区](https://www.kendryte.com/resource)获取。

### 版本不兼容解决办法

1. 与SDK版本对齐
   在确定好需要的nncase版本后，使用 `pip`进行安装，具体参考[nncase install](https://github.com/kendryte/nncase?tab=readme-ov-file#install)，之后重新编译`kmodel`。
1. 与nncase版本对齐
   在[nncase release界面](https://github.com/kendryte/nncase/releases)下载与编译 `kmodel`时nncase版本一致的运行时库，例如，"nncase_k230_v2.8.0_runtime.tgz"即为nncase-2.8.0的运行时库。之后按照以下步骤进行SDK中nncase运行时库版本更新：

   ```shell
   #准备工作
   git clone https://github.com/kendryte/k230_sdk.git
   cd k230_sdk
   PATH_TO_K230_SDK=`pwd`
   make prepare_sourcecode
   # 注意检查该命令执行后是否存在以下文件夹
   # src/big/nncase/riscv64/nncase/

   #解压nncase_k230_v2.8.0_runtime.tgz
   tar -xf nncase_k230_v2.8.0_runtime.tgz

   #替换nncase运行时库
   cp -r nncase_k230_v2.8.0_runtime/* $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/

   #检查nncase运行时库版本是否正确更新
   cat $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/include/nncase/version.h | grep NNCASE_VERSION
   > #define NNCASE_VERSION "2.8.0"
   ```

至此，SDK中的nncase运行时库版本已更新为nncase-2.8.0。如果需要更换其他版本，下载好对应版本的运行时库，按照上述步骤进行更新即可。
