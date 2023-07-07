# K230 RVV实战

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

## 概述

提高数据并行性的一种方式是向量计算技术，Riscv使用了这项技术。 K230 采用的是玄铁C908双核处理器,其中大核C908带了RVV1.0扩展，本文描述了如何在大核rt-smart上使用rvv功能

## 环境准备

### 硬件环境

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### 软件环境

k230_SDK

## 使用RVV功能

### 源码位置

`src/big/unittest/testcases/rvv_utest`

### 编译

在k230_sdk目录下运行

``` shell
make rt-smart-apps
```

进入目录 `src/big/rt-smart` 运行脚本 `source smart-env.sh riscv64` 配置环境变量。

```shell
$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/testUser/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
```

进入`userapps/testcases/rvv_utest`目录运行`scons`编译

``` shell
$ cd userapps/testcases/rvv_utest
$ scons
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: building associated VariantDir targets: build/rvv_utest
CC build/rvv_utest/rvv_utest.o
LINK rvv_utest.elf
/home/testUser/k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/../lib/gcc/riscv64-unknown-linux-musl/12.0.1/../../../../riscv64-unknown-linux-musl/bin/ld: warning: rvv_utest.elf has a LOAD segment with RWX permissions
```

之后即可将编译完成的rvv_utest.elf拷贝到sharefs内运行

``` shell
msh /sharefs>./rvv_utest.elf
enter thread run [1] times
enter thread run [67] times
enter thread run [96] times
enter thread run [56] times
enter thread run [89] times
enter thread run [51] times
enter thread run [55] times
enter thread run [1] times
enter thread run [29] times
enter thread run [53] times
vadd_test check passed
```

在源码目录下使用objdump工具反编译可确认是否产生了vector指令

``` text
$ riscv64-unknown-linux-musl-objdump -D rvv_utest.elf | grep 'vadd'
0000000200002b48 <vadd>:
   200002b48: 04d05e63          blez a3,200002ba4 <vadd+0x5c>
   200002b5c: 04f76563          bltu a4,a5,200002ba6 <vadd+0x5e>
   200002b68: 02f87363          bgeu a6,a5,200002b8e <vadd+0x46>
   200002b7c: 038c8c57          vadd.vv v24,v24,v25
   200002b8a: f2ed              bnez a3,200002b6c <vadd+0x24>
   200002ba0: feb699e3          bne a3,a1,200002b92 <vadd+0x4a>
   200002ba8: bf65              j 200002b60 <vadd+0x18>
0000000200002baa <vadd_test>:
   200002c36: f13ff0ef          jal ra,200002b48 <vadd>
   200002c3e: a835              j 200002c7a <vadd_test+0xd0>
   200002c5c: 00f70a63          beq a4,a5,200002c70 <vadd_test+0xc6>
   200002c84: fae7dee3          bge a5,a4,200002c40 <vadd_test+0x96>
   200002cd0: edbff0ef          jal ra,200002baa <vadd_test>
      90: 00000d57          vadd.vv v26,v0,v0,v0.t
     1b6: 00000157          vadd.vv v2,v0,v0,v0.t
     24a: 007c0357          vadd.vv v6,v7,v24,v0.t
     2a0: 000006d7          vadd.vv v13,v0,v0,v0.t
     360: 00000c57          vadd.vv v24,v0,v0,v0.t
     b14: 00000d57          vadd.vv v26,v0,v0,v0.t
```

### 源码简介

``` C
void __attribute__((noinline, noclone, optimize(3)))
vadd (int *dst, int *op1, int *op2, int count)
{
  for (int i = 0; i < count; ++i)
    dst[i] = op1[i] + op2[i];
}

#define ELEMS 10

int vadd_test(void)
{
    int in1[ELEMS] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    int in2[ELEMS] = { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 };
    int out[ELEMS];
    int check[ELEMS] = { 3, 5, 7, 9, 11, 13, 15, 17, 19, 21 };

    vadd (out, in1, in2, ELEMS);

    for (int i = 0; i < ELEMS; ++i)
    {
        if (out[i] != check[i]) {
            printf("check error\n");
            __builtin_abort();
        }
    }
    return 0;
}
```

vadd_test函数中预先计算了俩个数组(in1 in2)的和作为校验结果，之后使用vadd函数做数组加法。vadd函数在定义时添加了optimize(3)的属性设置，该函数将使用O3编译。
之后编译器会将数组加法优化为向量指令计算。
`src/big/rt-smart/tools/riscv64.py`文件内定义了编译参数可使用V指令扩展优化。

DEVICE = ' -mcmodel=medany -march=rv64imafdc`v` -mabi=lp64d'
