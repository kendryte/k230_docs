# K230 SDK Update Guide for nncase Runtime Library

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliates. Some or all of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise stipulated in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../zh/03_other/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No part of this document may be excerpted, reproduced, or distributed in any form without the written permission of the Company.

<div style="page-break-after:always"></div>

[TOC]

## Explanation of nncase Runtime Library Version Issues

### 1. Explanation of kmodel Version

Since the `kmodel` ***does not include the nncase version information***, it is impossible to directly determine which version of nncase generated the `kmodel`. You need to manage version information yourself. Here are two reference methods:

- Retain the complete compilation project (calibration set, parameter configuration) to facilitate generating the `kmodel` using any nncase version.
- Distinguish versions by the name of the `kmodel`. Example code is as follows:

  ```python
  with open("test.kmodel", "wb") as f:
      f.write(kmodel)

  # Replace the above code with the following
  import _nncase
  with open("test_{}.kmodel".format(_nncase.__version__), "wb") as f:
      f.write(kmodel)
  ```

### 2. Version Incompatibility Issues

Due to potential incompatibilities between different versions of nncase, the version of the nncase runtime library in the SDK might not match the version of nncase used to compile the `kmodel`, causing anomalies during inference on the board. Therefore, it is best to check whether the versions match before inference on the board.

Here are two ways to confirm if the version information matches:

- Check the [version correspondence table](./K230_SDK_nncase_version_correspondence.md#k230-sdk-nncase-version-correspondence).
- Determine the versions by the image name, for example, `k230_canmv_sdcard_v1.4_nncase_v2.8.0.img.gz`, where `v1.4` indicates the SDK version, and `v2.8.0` indicates the nncase version. This means SDK-v1.4 can infer `kmodel` compiled by nncase-v2.8.0. The image can be obtained from the [Canaan Developer Community](https://developer.canaan-creative.com/resource).

### 3. Solutions for Version Incompatibility Issues

1. Align with the SDK version
   After determining the required nncase version, use `pip` to install it. Refer to [nncase install](https://github.com/kendryte/nncase?tab=readme-ov-file#install) for details. Then recompile 'kmodel'.
1. Align with the nncase version
   Download the runtime library that matches the nncase version used to compile the `kmodel` from the [nncase release page](https://github.com/kendryte/nncase/releases). For example, "nncase_k230_v2.8.0_runtime.tgz" is the runtime library for nncase-2.8.0. Then follow these steps to update the nncase runtime library version in the SDK:

   ```shell
   #0. Preparation
   git clone https://github.com/kendryte/k230_sdk.git
   cd k230_sdk
   PATH_TO_K230_SDK=`pwd`
   make prepare_sourcecode
   # Ensure the following folder exists after executing the above command
   # src/big/nncase/riscv64/nncase/

   #1. Extract nncase_k230_v2.8.0_runtime.tgz
   tar -xf nncase_k230_v2.8.0_runtime.tgz

   #2. Replace the nncase runtime library
   cp -r nncase_k230_v2.8.0_runtime/* $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/

   #3. Check if the nncase runtime library version is correctly updated
   cat $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/include/nncase/version.h | grep NNCASE_VERSION
   > #define NNCASE_VERSION "2.8.0"
   ```

At this point, the nncase runtime library version in the SDK has been updated to nncase-2.8.0. If you need to switch to another version, download the corresponding runtime library and follow the steps above to update it.
