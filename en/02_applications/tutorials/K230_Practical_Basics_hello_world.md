# K230 Practical Basics - Hello World

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

All rights reserved ©2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**All rights reserved © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No part of this document may be excerpted, copied, or disseminated in any form by any unit or individual without the written permission of the Company.

<div style="page-break-after:always"></div>

## Overview

This document explains how to use a cross-compilation tool on a PC to compile a basic Hello World program and run it on a big core RT-Smart or a small core Linux.

## Environment Preparation

### Hardware Environment

- K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1
- Ubuntu PC 20.04
- At least 2 Type-C USB cables
- USB Type-C to Ethernet adapter (if using TFTP loading and NFS file system)
- One Ethernet cable
- SD card (if using SD card boot or if software needs to access the SD card)

### Software Environment

The k230_sdk provides toolchains located at the following paths.

- Big core RT-Smart toolchain

```shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu
```

- Small core Linux toolchain

```shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0
```

You can also download the toolchains from the following links:

```shell
wget https://download.rt-thread.org/rt-smart/riscv64/riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230222.tar.bz2
wget https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource//1659325511536/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0-20220715.tar.gz
```

### Code Writing

Create a C file named `hello.c` on Ubuntu and add the following code:

```c
#include <stdio.h>
int main(void)
{
    printf("hello world\n");
    return 0;
}
```

Place `hello.c` in the same directory level as `k230_sdk`.

```shell
canaan@develop:~/work$ ls
hello.c   k230_sdk
```

### Compiling an Executable for Small Core Linux

```shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc hello.c -o hello
```

### Compiling an Executable for Big Core RT-Smart

```shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.o -c -mcmodel=medany -march=rv64imafdcv -mabi=lp64d hello.c

k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.elf -mcmodel=medany -march=rv64imafdcv -mabi=lp64d -T k230_sdk/src/big/mpp/userapps/sample/linker_scripts/riscv64/link.lds  -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib -Wl,--whole-archive -lrtthread -Wl,--no-whole-archive -n --static hello.o -Lk230_sdk/src/big/rt-smart/userapps/sdk/lib/risc-v/rv64 -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib/risc-v/rv64 -Wl,--start-group -lrtthread -Wl,--end-group
```

### Running the Program

Copy the compiled `hello` and `hello.elf` to the vfat partition of the SD card (you can see an accessible drive letter on the PC after burning the image to the SD card), or use other methods (refer to the SDK usage documentation) to copy the executables to the `/sharefs` directory of the small core.

- After the development board starts, run the test program on the small core. Enter `root` to access the console after the small core starts.

```shell
Welcome to Buildroot
canaan login: root
[root@canaan ~ ]#cd /sharefs
[root@canaan /sharefs ]#./hello
hello world
```

- Run the test program on the big core

```shell
msh /sharefs>hello.elf
hello world
```

### Advanced Big Core Program Compilation

When using musl-gcc to compile for the big core directly, the compilation parameters are quite extensive, which can be inconvenient and hard to understand for beginners. The current SDK provides two methods for compiling big core programs: SCons and Makefile. Here, we introduce the SCons compilation method. The Makefile compilation build is more complex and is not the official RT-Smart compilation method. Interested readers can refer to the Makefile structure in `src/big/mpp/userapps/sample` for compilation.

Create a folder named `hello` under `k230_sdk/src/big/rt-smart/userapps`.

```shell
cd k230_sdk/src/big/rt-smart/userapps
mkdir hello
cd hello
```

Create the following three files:

- hello.c
- SConscript

```python
# RT-Thread building script for component

from building import *

cwd = GetCurrentDir()
src = Glob('*.c')
CPPPATH = [cwd]

CPPDEFINES = [
    'HAVE_CCONFIG_H',
]
group = DefineGroup('hello', src, depend=[''], CPPPATH=CPPPATH, CPPDEFINES=CPPDEFINES)

Return('group')
```

- SConstruct

```python
import os
import sys

# add building.py path
sys.path = sys.path + [os.path.join('..', '..', 'tools')]
from building import *

BuildApplication('hello', 'SConscript', usr_root='../')
```

Then return to the `k230_sdk/src/big/rt-smart/` directory and configure the environment variables.

```shell
canaan@develop:~/k230_sdk/src/big/rt-smart$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/canaan/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
```

Go to the `k230_sdk/src/big/rt-smart/userapps` directory and compile the program.

```shell
canaan@develop:~/k230_sdk/src/big/rt-smart/userapps$ scons --directory=hello
scons: Entering directory `/home/canaan/k230_sdk/src/big/rt-smart/userapps/hello'
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: building associated VariantDir targets: build/hello
CC build/hello/hello.o
LINK hello.elf
/home/canaan/k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/../lib/gcc/riscv64-unknown-linux-musl/12.0.1/../../../../riscv64-unknown-linux-musl/bin/ld: warning: hello.elf has a LOAD segment with RWX permissions
scons: done building targets.
```

The compiled program is in the `hello` folder.

```shell
canaan@develop:~/k230_sdk/src/big/rt-smart/userapps$ ls hello/
build  cconfig.h  hello.c  hello.elf  SConscript  SConstruct
```

Afterwards, you can copy `hello.elf` to the small core Linux, and the big core RT-Smart can run the program via `/sharefs`.
