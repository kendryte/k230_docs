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

RVV（RISC-V Vector Extension）是指RISC-V指令集架构的向量扩展。RISC-V是一种开源的指令集架构，它的设计简洁、可扩展性强，并且具有广泛的应用领域。RVV作为RISC-V的一个可选扩展，旨在支持向量处理和并行计算。RVV定义了一组新的指令，用于执行向量操作。这些指令允许同时处理多个数据元素，从而提高计算效率和吞吐量。向量操作可以在单个指令中执行，而不需要通过循环或逐个操作来处理每个数据元素。RVV支持不同的向量长度，可以根据应用的需求选择不同的向量长度。向量长度可以是固定的，也可以是可配置的。RVV还支持不同的数据类型，包括整数、浮点数和定点数等。

RVV的引入为处理器提供了向量处理和并行计算的能力，可以加速各种应用，如图像处理、信号处理、机器学习、科学计算等。同时，RVV的开放和可扩展性也使得各个厂商和开发者根据自己的需求进行定制和优化。K230 采用的是玄铁C908双核处理器,其中大核C908带了RVV1.0扩展，本文描述了如何在大核rt-smart上使用rvv功能。以及体验RVV加速带来的实际效果。

## 环境准备

### 硬件环境

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### 软件环境

k230_SDK

## 使用RVV功能

### 源码编写

为了体验RVV在向量计算上加速的优势，我们以图像缩放作为应用场景，编写一个demo。在sdk的如下路径创建一个文件夹

`k230_sdk/src/big/rt-smart/userapps/testcases/scale`

注意如果在k230_sdk下运行了make或者make rt-smart的话可能会导致修改被覆盖，读者可以将完成后的源码拷贝一份到如下目录

`k230_sdk/src/big/unittest/testcases`

#### 源码

在scale目录下创建C源码文件scale.c

``` C
#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>
#include <stdint.h>
#include <time.h>

#pragma pack(push, 1)
typedef struct {
    unsigned short signature;
    unsigned int fileSize;
    unsigned short reserved1;
    unsigned short reserved2;
    unsigned int dataOffset;
} BitmapFileHeader;

typedef struct {
    unsigned int headerSize;
    int width;
    int height;
    unsigned short planes;
    unsigned short bitsPerPixel;
    unsigned int compression;
    unsigned int imageSize;
    int xPixelsPerMeter;
    int yPixelsPerMeter;
    unsigned int colorsUsed;
    unsigned int colorsImportant;
} BitmapInfoHeader;
#pragma pack(pop)



void __attribute__((optimize(3)))
scaleBMP(const char* inputPath, const char* outputPath, float scaleFactor) {
    // 读取输入BMP文件
    FILE* inputFile = fopen(inputPath, "rb");
    if (inputFile == NULL) {
        printf("Failed to open input BMP file.\n");
        return;
    }

    BitmapFileHeader fileHeader;
    BitmapInfoHeader infoHeader;
    fread(&fileHeader, sizeof(BitmapFileHeader), 1, inputFile);
    fread(&infoHeader, sizeof(BitmapInfoHeader), 1, inputFile);

    int originalWidth = infoHeader.width;
    int originalHeight = infoHeader.height;
    int originalImageSize = infoHeader.imageSize;

    unsigned char* originalImageData = (unsigned char*) malloc(originalImageSize);
    fread(originalImageData, originalImageSize, 1, inputFile);
    fclose(inputFile);

    // 计算缩放后的图像尺寸
    int scaledWidth = (int)(originalWidth * scaleFactor);
    int scaledHeight = (int)(originalHeight * scaleFactor);
    int scaledImageSize = scaledWidth * scaledHeight * 3;

    // 创建输出BMP文件
    FILE* outputFile = fopen(outputPath, "wb");
    if (outputFile == NULL) {
        printf("Failed to create output BMP file.\n");
        free(originalImageData);
        return;
    }

    // 更新BMP文件头信息
    fileHeader.fileSize = sizeof(BitmapFileHeader) + sizeof(BitmapInfoHeader) + scaledImageSize;
    infoHeader.width = scaledWidth;
    infoHeader.height = scaledHeight;
    infoHeader.imageSize = scaledImageSize;
    fwrite(&fileHeader, sizeof(BitmapFileHeader), 1, outputFile);
    fwrite(&infoHeader, sizeof(BitmapInfoHeader), 1, outputFile);

    clock_t start, finish;
    start = clock();
    // 缩放图像数据
    unsigned char* scaledImageData = (unsigned char*) malloc(scaledImageSize);
    for (int y = 0; y < scaledHeight; y++) {
        for (int x = 0; x < scaledWidth; x++) {
            int originalX = (int)(x / scaleFactor);
            int originalY = (int)(y / scaleFactor);
            scaledImageData[(y * scaledWidth + x) * 3 + 0] = originalImageData[(originalY * originalWidth + originalX) * 3 + 0];
            scaledImageData[(y * scaledWidth + x) * 3 + 1] = originalImageData[(originalY * originalWidth + originalX) * 3 + 1];
            scaledImageData[(y * scaledWidth + x) * 3 + 2] = originalImageData[(originalY * originalWidth + originalX) * 3 + 2];
        }
    }
    finish = clock();
    printf("scale cacl use time:%f ms\n",(double)(finish - start) / CLOCKS_PER_SEC);

    // 写入缩放后的图像数据
    fwrite(scaledImageData, scaledImageSize, 1, outputFile);
    fclose(outputFile);

    free(originalImageData);
    free(scaledImageData);

    printf("BMP image scaling completed.\n");
}


int main() 
{
    const char* inputPath = "input.bmp";
    const char* outputPath = "output.bmp";
    float scaleFactor = 0.5; // 缩放因子
    scaleBMP(inputPath, outputPath, scaleFactor);
    return 0;
}
```

#### SCONS配置文件

- 创建SConscript文件

```python
# RT-Thread building script for component

from building import *

cwd = GetCurrentDir()
src = Glob('*.c')
CPPPATH = [cwd]

CPPDEFINES = [
    'HAVE_CCONFIG_H',
]
group = DefineGroup('scale', src, depend = [''], CPPPATH = CPPPATH, CPPDEFINES = CPPDEFINES)

Return('group')
```

- 创建SConstruct文件

``` python
import os
import sys

# add building.py path
sys.path = sys.path + [os.path.join('..','..','..','tools')]
from building import *

BuildApplication('scale', 'SConscript', usr_root = '../../..')
```

### 编译

进入目录 `src/big/rt-smart` 运行脚本 `source smart-env.sh riscv64` 配置环境变量。

```shell
$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/testUser/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
```

进入`userapps/testcases/scale`目录运行`scons --release`编译

``` shell
$ cd userapps/testcases/scale
$ scons --release
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: building associated VariantDir targets: build/scale
CC build/scale/scal.o
LINK scale.elf
/home/haohaibo/work/k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/../lib/gcc/riscv64-unknown-linux-musl/12.0.1/../../../../riscv64-unknown-linux-musl/bin/ld: warning: scale.elf has a LOAD segment with RWX permissions
scons: done building targets.
```

将编译好的程序重命名

``` shell
mv scale.elf scale_with_rvv.elf
```

编辑k230_sdk/src/big/rt-smart/tools/riscv64.py文件，去掉编译选项的v扩展。

``` diff
$:k230_sdk/src/big/rt-smart/userapps/testcases/scale$ git diff
diff --git a/tools/riscv64.py b/tools/riscv64.py
index 16fc9b2..c045bf5 100644
--- a/tools/riscv64.py
+++ b/tools/riscv64.py
@@ -44,7 +44,7 @@ class ARCHRISCV64():
                 EXT_CFLAGS = ''
                 EXT_LFLAGS = ''
 
-            DEVICE = ' -mcmodel=medany -march=rv64imafdcv -mabi=lp64d'
+            DEVICE = ' -mcmodel=medany -march=rv64imafdc -mabi=lp64d'
             self.CFLAGS    = configuration.get('CFLAGS', DEVICE + ' -Werror -Wall' + EXT_CFLAGS)
             self.AFLAGS    = configuration.get('AFLAGS', ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLY__ -I.' + EXT_CFLAGS)
             LINK_SCRIPT    = configuration.get('LINK_SCRIPT', os.path.join(USR_ROOT, 'linker_scripts', 'riscv64', 'link.lds'))
haohaibo@develop:~/work/k230_sdk/src/big/rt-smart/userapps/testcases/scale$ 

```

重新编译源码,之后将编译完的scale.elf和scale_with_rvv.elf全部拷贝到sharefs下运行。

### 运行

准备一张24位bmp的图片，命名为input.bmp(可以用PC画图软件保存生成), 与程序放在同一目录，之后大核通过sharefs运行这俩个程序。

``` shell
msh /sharefs>scale.elf
scale cacl use time:0.013952 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale cacl use time:0.013960 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale cacl use time:0.013941 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale cacl use time:0.013936 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale cacl use time:0.013945 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale cacl use time:0.013957 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale cacl use time:0.010139 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale cacl use time:0.010133 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale cacl use time:0.010135 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale cacl use time:0.010144 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale cacl use time:0.010142 ms
BMP image scaling completed.
```

从打印信息看，使用了V扩展指令后，数组的计算明显加快了，如果增大图像的分辨率到4K，可以看到更明显的对比。

### 反编译

可以在源码目录下使用objdump工具反编译可确认是否产生了vector指令

``` text
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S |grep 'vadd'
   200002c7e:03bf4dd7          vadd.vx v27,v27,t5
   200002c94:03834c57          vadd.vx v24,v24,t1
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S |grep 'vmul'
   200002c98:97856c57           vmul.vx v24,v24,a0

```
