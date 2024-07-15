# K230 OpenBLAS Development Guide

![cover](../../../../zh/01_software/board/middleware/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contract and terms of Beijing Canaan Creative Information Technology Co., Ltd. (“the Company”) and its affiliates. All or part of the products, services, or features described in this document may not be within your purchase or usage scope. Unless otherwise agreed in the contract, the Company does not provide any express or implied statement or warranty regarding the correctness, reliability, completeness, merchantability, suitability for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/middleware/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces K230 OpenBLAS.

### Target Audience

This document (guide) is primarily intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                                        |
|--------------|-----------------------------------------------------|
| OpenBLAS     | Open Basic Linear Algebra Subprograms              |

### Revision History

| Document Version | Modification Description | Modifier | Date       |
|------------------|--------------------------|----------|------------|
| V1.0             | Initial Version          | Algorithm Department | 2023-05-30 |

## 1. Introduction to OpenBLAS

OpenBLAS is an optimized BLAS computation library distributed under the BSD license (open-source). BLAS (Basic Linear Algebra Subprograms) is an API standard for releasing numerical libraries for basic linear algebra operations (such as vector or matrix multiplication). OpenBLAS is a specific implementation of the BLAS standard.
In the SDK, a pre-cross-compiled OpenBLAS library is included (located at the path `k230_sdk/src/big/utils/lib/openblas/`). Users can directly use this static library to compile their own executable programs.

## 2. Test Case Compilation

Note:
>This section explains how to compile executable programs using the pre-set OpenBLAS static library in the SDK. The SDK includes multiple examples of executable program compilation based on OpenBLAS (located at `k230_sdk/src/big/utils/examples/openblas/`). This section explains based on these examples.

The directory structure under the path `k230_sdk/src/big/utils/examples/openblas/` is as follows:

```text
|-- 1_openblas_level1             # OpenBLAS Example 1
|   |-- CMakeLists.txt            # CMake configuration file for OpenBLAS Example 1
|   `-- openblas_level1.cpp
|-- 2_openblas_level2
|   |-- CMakeLists.txt
|   `-- openblas_level2.cpp
|-- 3_openblas_level3
|   |-- CMakeLists.txt
|   `-- openblas_level3.cpp
|-- 4_fortran_example
|   |-- CMakeLists.txt
|   `-- openblas_fortran.cpp
|-- CMakeLists.txt               # Overall CMake configuration file
|-- build_app.sh                 # Overall compilation script
|-- cmake                        # Default CMake configuration
|   |-- Riscv64.cmake
|   `-- link.lds
```

First, run the `build_app.sh` file under the path `k230_sdk/src/big/utils/examples/openblas/`:

```shell
./build_app.sh
```

If the following prompt appears in the terminal, it indicates that the executable program has been successfully compiled:

```text
Install the project...
-- Install configuration: "Release"
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/1_openblas_level1.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/2_openblas_level2.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/3_openblas_level3.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/4_openblas_fortran.elf
```

Finally, the `k230_sdk/src/big/utils/examples/openblas/out/bin` folder contains all the compiled elf files:

- `1_openblas_level1.elf`
- `2_openblas_level2.elf`
- `3_openblas_level3.elf`
- `4_openblas_fortran.elf`

## 3. Test Case Execution Demonstration

### 3.1 level_1 Test Case

Execution method and output example:

```shell
msh /sharefs/bin_openblas>./1_openblas_level1.elf
*********************************************************
This is the result:
4 7 11 14
*********************************************************
This is the reference:
4 7 11 14
{Test PASS}.
```

### 3.2 level_2 Test Case

Execution method and output example:

```shell
msh /sharefs/bin_openblas>./2_openblas_level2.elf
*********************************************************
This is the result:
20 40 10 20 30 60
*********************************************************
This is the reference:
20 40 10 20 30 60
{Test PASS}.
```

### 3.3 level_3 Test Case

Execution method and output example:

```shell
msh /sharefs/bin_openblas>./3_openblas_level3.elf
*********************************************************
This is the result:
7 10 15 22
*********************************************************
This is the reference:
7 10 15 22
{Test PASS}.
```

### 3.4 Fortran Interface Test Case

Execution method and output example:

```shell
msh /sharefs/bin_openblas>./4_openblas_fortran.elf
m=2,n=3,k=4,alpha=1.200000,beta=0.001000,sizeofc=6
This is matrix A

1.000000 2.000000 3.000000 1.000000 2.000000 3.000000 1.000000 2.000000
This is matrix B

1.000000 2.000000 3.000000 1.000000 2.000000 3.000000 1.000000 2.000000 3.000000 1.000000 2.000000 3.000000
*********************************************************
This is the result:
16.801 18.002 18.003 16.801 15.602 22.803
*********************************************************
This is the reference:
16.801 18.002 18.003 16.801 15.602 22.803
{Test PASS}.
```

## 4. OpenBLAS Cross Compilation

Note:
>Although the SDK includes a pre-cross-compiled OpenBLAS library (located at the path `k230_sdk/src/big/utils/lib/openblas/`), interested users can also cross-compile OpenBLAS themselves to obtain the OpenBLAS static library adapted to K230.

### 4.1 Setting Up the OpenBLAS Compilation Environment

#### 4.1.1 Git Code Download

First, use git to obtain the OpenBLAS repository. Since OpenBLAS comes from GitHub, slow cloning speed is normal, please be patient:

```shell
git clone https://github.com/xianyi/OpenBLAS.git
```

OpenBLAS has many versions. Since version 0.3.21 lacks some features compared to the latest branch, we use the current latest commit:

```shell
git checkout e9a911fb9f011c886077e68eab81c48817cdb782
```

#### 4.1.2 Applying Patch Package

Note:
>The patch package is located in the SDK at `k230_sdk/src/big/rt-smart/userapps/openblas/`.

First, create a `patch` directory in the root directory of OpenBLAS and copy the patch package to the `patch` directory. The directory structure after placing the folder is shown as follows:

```text
├── appveyor.yml
├── azure-pipelines.yml
├── BACKERS.md
├── benchmark
├── cblas.h
...
├── common_lapack.h
├── common_level1.h
├── common_level2.h
├── common_level3.h
├── common_linux.h
├── common_loongarch64.h
├── common_macro.h
|-- patch # Patch package for OpenBLAS
| |-- 0001-****.patch
| |-- 0002-****.patch
| |-- 0003-****.patch
...
| |-- 0009-****.patch
| |-- 0010-****.patch
| |-- 0011-****.patch
...
...
...
├── utest
└── version.h
```

Execute the following command in the root directory of OpenBLAS to apply the patches:

```shell
git am ./patch/*.patch
```

### 4.3 OpenBLAS Compilation

Enter the root directory of OpenBLAS and execute the following command to compile:

```shell
# Note: The toolchain path will vary depending on the developer's specific environment, and the path prefix is for reference only.
make TARGET=C908V HOSTCC=gcc BINARY=64 FC=k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gfortran CC=k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknownlinux-musl-gcc NOFORTRAN=0 USE_THREAD=0 LIBPREFIX="./libopenblas" LAPACKE="NO_LAPACKE=0" INTERFACE64=0 NO_STATIC=0 NO_SHARED=1 -Wimplicit-functiondeclaration
```

After the compilation is complete, install the compiled library to a specified folder. In this example, it is installed in the `./install` folder:

```shell
# Note: You can modify the installation path according to your needs.
make PREFIX=./install NO_STATIC=0 NO_SHARED=1 install
```
