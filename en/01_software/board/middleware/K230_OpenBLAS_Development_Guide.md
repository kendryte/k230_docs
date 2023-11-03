# K230 OpenBLAS Development Guide

![cover](../../../../zh/01_software/board/middleware/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/middleware/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## directory

[TOC]

## preface

### overview

This document focuses on the K230 OpenBLAS.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate                                                        |
|------|-------------------------------------------------------------|
| OpenBLAS  | Open Basic Linear Algebra Subprograms                   |

### Revision history

| Document version number | Modify the description | Modified by     | date       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | first edition     | Algorithm Department | 2023-05-30 |

## 1.Introduction to OpenBLAS

OpenBLAS is an optimized BLAS computing library based on the BSD license (open source). BLAS (Basic Linear Algebra Subprograms) is an application program interface (API) standard that specifies the publication of numerical libraries for basic linear algebra operations (such as vector or matrix multiplication), OpenBLAS is a concrete implementation of the BLAS standard.
In the SDK, the pre-cross-compiled OpenBLAS library (located under the path) is included,`k230_sdk/src/big/utils/lib/openblas/` and users can directly use this static library to compile their own executable programs.

## 2. Test case compilation

Note:
>This section explains how to compile executable programs using the default OpenBLAS static libraries in the SDK. The SDK already contains several examples of compiled executable programs based on OpenBLAS implementations (located`k230_sdk/src/big/utils/examples/openblas/` in the path), and this section builds on these examples.

`k230_sdk/src/big/utils/examples/openblas/`The directory structure under the path is described as follows:

```text
|-- 1_openblas_level1             # OpenBLAS Example 1
|   |-- CMakeLists.txt            # CMake Configuration File for OpenBLAS Example 1
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
|-- CMakeLists.txt               # Overall CMake Configuration File
|-- build_app.sh                 # Overall Compilation Script
|-- cmake                        # Default CMaek configuration
|   |-- Riscv64.cmake
|   `-- link.lds
```

First, `k230_sdk/src/big/utils/examples/openblas/`under the path, run`build_app.sh` the file:

```shell
./build_app.sh
```

The following prompt appears in the terminal to indicate that the executable program is compiled successfully:

```text
Install the project...
-- Install configuration: "Release"
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/1_openblas_level1.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/2_openblas_level2.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/3_openblas_level3.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/openblas/out/bin/4_openblas_fortran.elf
```

Finally, all `k230_sdk/src/big/utils/examples/openblas/out/bin`the compiled ELF files are included in the folder:

- `1_openblas_level1.elf`
- `2_openblas_level2.elf`
- `3_openblas_level3.elf`
- `4_openblas_fortran.elf`

## 3. Test case run demo

### 3.1 level_1 Test Cases

The following is an example of the operation mode and output result:

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

### 3.2 level_2 Test Cases

The following is an example of the operation mode and output result:

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

### 3.3 level_3 Test Cases

The following is an example of the operation mode and output result:

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

### 3.4 Fortran Interface Test Cases

The following is an example of the operation mode and output result:

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

## 4.OpenBLAS cross-compilation

Note:
>Although the SDK already contains pre-cross-compiled OpenBLAS libraries (located `k230_sdk/src/big/utils/lib/openblas/`in the path), interested users can also cross-compile OpenBLAS themselves to get OpenBLAS static libraries adapted to K230.

### 4.1 OpenBLAS compilation environment is set up

#### 4.1.1 Git code download

First use git to get the OpenBLAS repository, since OpenBLAS comes from Github, the cloning speed is normal, please be patient:

```shell
git clone https://github.com/xianyi/OpenBLAS.git
```

There are many versions in OpenBLAS, and since version 0.3.21 lacks some features compared to the latest branch, we choose the current one
Submit:

```shell
git checkout e9a911fb9f011c886077e68eab81c48817cdb782
```

#### 4.1.2 Patch Service Pack Application

Note:
>The path of the patch service pack in the SDK is`k230_sdk/src/big/rt-smart/userapps/openblas/`.

First, in the root directory of OpenBLAS, create a new`patch` directory, copy the patch service package to `patch`the directory, and the folder directory structure is shown below:

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
|-- patch # Patch Pack for OpenBLAS
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

Run the following command in the OpenBLAS root directory to apply the patch:

```shell
git am ./patch/*.patch
```

### 4.3 OpenBLAS compilation

Go to the root directory of OpenBLAS and execute the following command to compile:

```shell
# Note: The tool chain path may vary depending on the developer's specific environment, and the path prefix may vary for reference only.
make TARGET=C908V HOSTCC=gcc BINARY=64 FC=k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gfortran CC=k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknownlinux-musl-gcc NOFORTRAN=0 USE_THREAD=0 LIBPREFIX="./libopenblas" LAPACKE="NO_LAPACKE=0" INTERFACE64=0 NO_STATIC=0 NO_SHARED=1 -Wimplicit-functiondeclaration
```

After the compilation is complete, the compiled library is installed in the specified folder, and this example is installed in the folder`./install`:

```shell
# Note: You can modify the corresponding installation path according to your own needs.
make PREFIX=./install NO_STATIC=0 NO_SHARED=1 install
```
