# K230 实战基础篇 - hello world

## 概述

本文将讲解如果在pc端使用交叉编译工具编译一个hello world的基础程序，并在大核rt-smart或小核linux上运行。

## 环境准备

### 硬件环境

- K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1
- Ubuntu PC 20.04
- Typec USB线 * 2 至少
- USB TypeC转以太网(如果使用TFTP加载和NFS文件系统)
- 网线一根
- SD卡(如果使用SD卡启动，或软件需要访问SD卡)

### 软件环境

k230_sdk中提供了工具链，分别在如下路径。

- 大核rt-samrt工具链

``` shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu
```

- 小核linux工具链

``` shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0
```

也可通过以下链接下载工具链

``` shell
wget https://download.rt-thread.org/rt-smart/riscv64/riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230222.tar.bz2
wget https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource//1659325511536/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0-20220715.tar.gz
```

### 代码编写

在ubuntu上创建一个C文件hello.c并加入如下代码

```C
#include <stdio.h>
int main (void)
{
    printf("hello world\n");
    return 0;
}
```

将hello.c放到与k230_sdk同一级目录下

``` shell
canaan@develop:~/work$ ls
hello.c   k230_sdk
```

### 编译适用于小核linux的可执行程序

``` shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc hello.c -o hello
```

### 编译适用于大核rt-smart的可执行程序

``` shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.o -c -mcmodel=medany -march=rv64imafdcv -mabi=lp64d hello.c

k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/riscv64-unknown-linux-musl-gcc -o hello.elf -mcmodel=medany -march=rv64imafdcv -mabi=lp64d -T k230_sdk/src/big/mpp/userapps/sample/linker_scripts/riscv64/link.lds  -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib -Wl,--whole-archive -lrtthread -Wl,--no-whole-archive -n --static hello.o -Lk230_sdk/src/big/rt-smart/userapps/sdk/lib/risc-v/rv64 -Lk230_sdk/src/big/rt-smart/userapps/sdk/rt-thread/lib/risc-v/rv64 -Wl,--start-group -lrtthread -Wl,--end-group
```

### 运行程序

将编译好的hello以及hello.elf拷贝到sd卡的vfat分区内(sd卡烧写完镜像后可以在pc端看到一个可用的盘符)，或通过其他方式(参考sdk使用说明文档)将可执行程序拷贝到小核的/sharefs目录下。

- 开发板启动后，在小核端运行测试程序,小核启动后输入`root`进入控制台

``` shell
Welcome to Buildroot
canaan login: root
[root@canaan ~ ]#cd /sharefs
[root@canaan /sharefs ]#./hello
hello world
```

- 在大核端运行测试程序

``` shell
msh /sharefs>hello.elf
hello world
```

### 大核程序编译进阶

大核如果用musl-gcc直接编译的话，编译参数是比较多的，对于初学者来说很不方便，也不太好理解，当前sdk中提供了两种用于编译大核程序的方式，分别是scons和Makefile,这里我们介绍scons的编译方式，Makefile的编译构建较为复杂，不是rt-smart官方提供的编译方式，感兴趣的读者可参考`src/big/mpp/userapps/sample`中的Makefile结构来编译。

到`k230_sdk/src/big/rt-smart/userapps`目录下创建一个文件夹，命名为hello

``` shell
cd k230_sdk/src/big/rt-smart/userapps
mkdir hello
cd hello
```

创建以下三个文件

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

之后回到`k230_sdk/src/big/rt-smart/`目录，配置环境变量

``` shell
canaan@develop:~/k230_sdk/src/big/rt-smart$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/canaan/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin

```

进入`k230_sdk/src/big/rt-smart/userapps`目录，编译程序

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

编译好的程序在hello文件夹下

``` shell
canaan@develop:~/k230_sdk/src/big/rt-smart/userapps$ ls hello/
build  cconfig.h  hello.c  hello.elf  SConscript  SConstruct
```

之后即可将hello.elf拷贝到小核linux上，然后大核rt-smart通过/sharefs即可运行该程序
