# K230 Practical Basics - hello world

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## overview

This article will explain how to use the cross-compilation tool on the PC side to compile a Hello World basic program and run it on the large-core RT-Smart or small-core Linux.

## Environment preparation

### Hardware environment

- K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1
- Ubuntu PC 20.04
- Typec USB cable * 2 at least
- USB TypeC to Ethernet (if using TFTP loading and NFS file system)
- One network cable
- SD card (if booting with an SD card, or software requires access to the SD card)

### Software environment

The toolchains are provided in the k230_sdk and are available in the following paths.

- Big core RT-SAMRT toolchain

``` shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu
```

- Small-core Linux toolchain

``` shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0
```

The toolchain can also be downloaded via the link below

``` shell
wget https://download.rt-thread.org/rt-smart/riscv64/riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230222.tar.bz2
wget https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource//1659325511536/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0-20220715.tar.gz
```

### Code writing

Create a C file hello.c on ubuntu and add the following code

```C
#include <stdio.h>
int main (void)
{
    printf("hello world\n");
    return 0;
}
```

Put hello.c in the same directory as k230_sdk

``` shell
canaan@develop:~/work$ ls
hello.c   k230_sdk
```

### Compile executable programs for small-core Linux

``` shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc hello.c -o hello
```

### Compile executable programs for large-core rt-smart

``` shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.o -c -mcmodel=medany -march=rv64imafdcv -mabi=lp64d hello.c

k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.elf -mcmodel=medany -march=rv64imafdcv -mabi=lp64d -T k230_sdk/src/big/mpp/userapps/sample/linker_scripts/riscv64/link.lds  -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib -Wl,--whole-archive -lrtthread -Wl,--no-whole-archive -n --static hello.o -Lk230_sdk/src/big/rt-smart/userapps/sdk/lib/risc-v/rv64 -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib/risc-v/rv64 -Wl,--start-group -lrtthread -Wl,--end-group
```

### Run the program

Copy the compiled hello and hello.elf to the vfat partition of the sd card (you can see an available drive letter on the PC after the sd card has flashed the image), or copy the executable program to the /sharefs directory of the little core by other means (refer to the SDK user documentation).

- After the board starts, run the test program on the little core side, and enter the console after the little core is started`root`

``` shell
Welcome to Buildroot
canaan login: root
[root@canaan ~ ]#cd /sharefs
[root@canaan /sharefs ]#./hello
hello world
```

- Run the test program on the big core side

``` shell
msh /sharefs>hello.elf
hello world
```

### Advanced compilation of big core programs

If the big core is compiled directly with musl-gcc, the compilation parameters are more, which is very inconvenient for beginners and not easy to understand, the current SDK provides two ways for compiling big core programs, respectively scons and Makefile, here we introduce the compilation method of scons, the compilation and construction of Makefile is more complicated, not the compilation method provided by rt-smart officially, interested readers can refer to`src/big/mpp/userapps/sample`Makefile structure to compile.

Go to the `k230_sdk/src/big/rt-smart/userapps`directory and create a folder named hello

``` shell
cd k230_sdk/src/big/rt-smart/userapps
mkdir hello
cd hello
```

Create the following three files

- hello.c
- SConscript

``` python
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

``` python
import os
import sys

# add building.py path
sys.path = sys.path + [os.path.join('..','..','tools')]
from building import *

BuildApplication('hello', 'SConscript', usr_root = '../')

```

After that, go back to the `k230_sdk/src/big/rt-smart/`directory and configure the environment variables

``` shell
canaan@develop:~/k230_sdk/src/big/rt-smart$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/canaan/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin

```

Go to `k230_sdk/src/big/rt-smart/userapps`the directory and compile the program

``` shell
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

The compiled program is in the hello folder

``` shell
canaan@develop:~/k230_sdk/src/big/rt-smart/userapps$ ls hello/
build  cconfig.h  hello.c  hello.elf  SConscript  SConstruct
```

Hello.Elf can then be copied to the small-core Linux, and the large-core rt-smart can run the program through /sharefs
