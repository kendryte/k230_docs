# K230_SDK_update_nncase_runtime_tutorial

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../zh/03_other/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

[toc]

## Nncase Runtime Library Version Description

### 1. Kmodel Version Description

Since the `kmodel` does not contain version information about "nncase", it is impossible to directly determine which version of nncase was used to generate the `kmodel`. It is necessary to manage version information independently; here are two approaches for reference:

- Retain the complete compilation project (calibration set, parameter configurations), making it convenient to generate the `kmodel`.
- Differentiate versions by naming the `kmodel`, as demonstrated in the following sample code.

    ```python
    with open("test.kmodel", "wb") as f:
        f.write(kmodel)
    
    # Replace the above code with the following content
    import _nncase
    with open("test_{}.kmodel".format(_nncase.__version__), "wb") as f:
        f.write(kmodel)
    ```

### 2. Version Incompatibility Issue

Due to potential incompatibilities between different versions of nncase, the version of the nncase runtime library included in the SDK may not match the version of nncase used to compile the `kmodel`,  which could lead to abnormalities during on-board inference. Therefore, it is advisable to check whether the two versions are compatible before performing on-board inference.

There are two methods available for verifying the version compatibility:

- Query the version correspondence table: Refer to the [Version Correspondence Table](./K230_SDK_nncase_version_correspondence.md#correspondence-between-sdk-canmv-version-and-nncase-version) to confirm that the SDK and nncase versions match.
- Determine the versions through the image name: For instance, in the image file named `k230_canmv_sdcard_v1.4_nncase_v2.8.0.img.gz`, `v1.4` represents the SDK version, while `v2.8.0` indicates the nncase version. This means that SDK-v1.4 can correctly infer `kmodel` has compiled by nncase-v2.8.0.
The corresponding images can be obtained from the [Canaan Developer Community](https://developer.canaan-creative.com/resource).

### 3. Solutions for Version Incompatibility

1. Align with SDK Version
After determining the required nncase version, install it using `pip`, referring to the [nncase Installation Guide](https://github.com/kendryte/nncase?tab=readme-ov-file#install) for specific instructions.

1. Align with Nncase Version
Download the runtime library that matches the version of nncase used when compiling the `kmodel` file from the [nncase Release Page](https://github.com/kendryte/nncase/releases). For instance, ‘nncase_k230_v2.8.0_runtime.tgz’ represents the runtime library compatible with nncase version 2.8.0. Following this, proceed with updating the nncase runtime library version within the SDK by following these steps:

    ```shell
    #0. Preparation work.
    git clone https://github.com/kendryte/k230_sdk.git
    cd k230_sdk
    PATH_TO_K230_SDK=`pwd`
    make prepare_sourcecode
    # Please make sure to verify if the following directory exists after running the given command.
    # src/big/nncase/riscv64/nncase/
    
    #1. decompressing files "nncase_k230_v2.8.0_runtime.tgz"
    tar -xf nncase_k230_v2.8.0_runtime.tgz
    
    #2. update nncase runtime library.
    cp -r nncase_k230_v2.8.0_runtime/* $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/
    
    #3. Check whether the nncase runtime library has been correctly updated.
    cat $PATH_TO_K230_SDK/src/big/nncase/riscv64/nncase/include/nncase/version.h | grep NNCASE_VERSION
    > #define NNCASE_VERSION "2.8.0"
    ```

Now, the version of nncase runtime library within the SDK has been upgraded to nncase-2.8.0. Should you require switching to a different version, just download the matching runtime library and proceed with the update using the aforementioned steps.
