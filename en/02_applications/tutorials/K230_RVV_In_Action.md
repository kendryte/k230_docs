# K230 RVV Practical Guide

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

Your purchase of products, services, or features is subject to the commercial contracts and terms of Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan", and other Canaan trademarks are trademarks of Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without written permission from the Company, no unit or individual is allowed to excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Overview

RVV (RISC-V Vector Extension) refers to the vector extension of the RISC-V instruction set architecture. RISC-V is an open-source instruction set architecture known for its simplicity, scalability, and wide range of applications. RVV, as an optional extension of RISC-V, aims to support vector processing and parallel computing. RVV defines a set of new instructions for executing vector operations. These instructions allow multiple data elements to be processed simultaneously, thereby improving computational efficiency and throughput. Vector operations can be executed in a single instruction without needing loops or individual operations for each data element. RVV supports different vector lengths, which can be fixed or configurable based on application requirements. It also supports various data types, including integers, floating-point numbers, and fixed-point numbers.

The introduction of RVV provides processors with vector processing and parallel computing capabilities, accelerating various applications such as image processing, signal processing, machine learning, and scientific computing. The openness and scalability of RVV also enable manufacturers and developers to customize and optimize according to their needs. The K230 uses the XuanTie C908 dual-core processor, with the larger core C908 featuring the RVV1.0 extension. This document describes how to use the RVV functionality on the larger core rt-smart and experience the performance acceleration brought by RVV.

## Environment Preparation

### Hardware Environment

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### Software Environment

k230_SDK

## Using RVV Functionality

### Source Code Writing

To experience the advantages of RVV in vector computation, we will use image scaling as an application scenario and write a demo. Create a folder in the following path of the SDK:

`k230_sdk/src/big/rt-smart/userapps/testcases/scale`

Note that running `make` or `make rt-smart` in the k230_sdk directory may overwrite your changes. You can copy the completed source code to the following directory:

`k230_sdk/src/big/unittest/testcases`

#### Source Code

Create a C source file named `scale.c` in the scale directory:

```c
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
    // Read input BMP file
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

    // Calculate scaled image dimensions
    int scaledWidth = (int)(originalWidth * scaleFactor);
    int scaledHeight = (int)(originalHeight * scaleFactor);
    int scaledImageSize = scaledWidth * scaledHeight * 3;

    // Create output BMP file
    FILE* outputFile = fopen(outputPath, "wb");
    if (outputFile == NULL) {
        printf("Failed to create output BMP file.\n");
        free(originalImageData);
        return;
    }

    // Update BMP file header information
    fileHeader.fileSize = sizeof(BitmapFileHeader) + sizeof(BitmapInfoHeader) + scaledImageSize;
    infoHeader.width = scaledWidth;
    infoHeader.height = scaledHeight;
    infoHeader.imageSize = scaledImageSize;
    fwrite(&fileHeader, sizeof(BitmapFileHeader), 1, outputFile);
    fwrite(&infoHeader, sizeof(BitmapInfoHeader), 1, outputFile);

    clock_t start, finish;
    start = clock();
    // Scale image data
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
    printf("scale calc use time:%f ms\n", (double)(finish - start) / CLOCKS_PER_SEC);

    // Write the scaled image data
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
    float scaleFactor = 0.5; // Scaling factor
    scaleBMP(inputPath, outputPath, scaleFactor);
    return 0;
}
```

#### SCONS Configuration File

- Create SConscript file

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

- Create SConstruct file

```python
import os
import sys

# add building.py path
sys.path = sys.path + [os.path.join('..','..','..','tools')]
from building import *

BuildApplication('scale', 'SConscript', usr_root = '../../..')
```

### Compilation

Enter the directory `src/big/rt-smart` and run the script `source smart-env.sh riscv64` to configure the environment variables.

```shell
$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/testUser/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
```

Enter the `userapps/testcases/scale` directory and run `scons --release` to compile.

```shell
$ cd userapps/testcases/scale
$ scons --release
scons: Reading SConscript files ...
scons: done reading SConscript files.
scons: Building targets ...
scons: building associated VariantDir targets: build/scale
CC build/scale/scale.o
LINK scale.elf
/home/haohaibo/work/k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/../lib/gcc/riscv64-unknown-linux-musl/12.0.1/../../../../riscv64-unknown-linux-musl/bin/ld: warning: scale.elf has a LOAD segment with RWX permissions
scons: done building targets.
```

Rename the compiled program

```shell
mv scale.elf scale_with_rvv.elf
```

Edit the `k230_sdk/src/big/rt-smart/tools/riscv64.py` file to remove the v extension from the compilation options.

```diff
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

Recompile the source code, then copy both compiled `scale.elf` and `scale_with_rvv.elf` to the sharefs directory for execution.

### Execution

Prepare a 24-bit BMP image named `input.bmp` (you can use PC drawing software to save and generate it), place it in the same directory as the program, and then run these two programs on the large core through sharefs.

```shell
msh /sharefs>scale.elf
scale calc use time:0.013952 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale calc use time:0.013960 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale calc use time:0.013941 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale calc use time:0.013936 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale calc use time:0.013945 ms
BMP image scaling completed.
msh /sharefs>scale.elf
scale calc use time:0.013957 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale calc use time:0.010139 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale calc use time:0.010133 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale calc use time:0.010135 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale calc use time:0.010144 ms
BMP image scaling completed.
msh /sharefs>scale_with_rvv.elf
scale calc use time:0.010142 ms
BMP image scaling completed.
```

From the printed information, it is evident that using the V extension instructions significantly speeds up array calculations. If the image resolution is increased to 4K, the contrast will be even more apparent.

### Disassembly

You can use the objdump tool in the source directory to disassemble and confirm whether vector instructions are generated.

```text
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S | grep 'vadd'
   200002c7e:03bf4dd7          vadd.vx v27,v27,t5
   200002c94:03834c57          vadd.vx v24,v24,t1
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S | grep 'vmul'
   200002c98:97856c57          vmul.vx v24,v24,a0
```
