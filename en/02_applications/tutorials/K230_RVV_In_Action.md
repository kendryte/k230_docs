# K230 RVV in action

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

RVV (RISC-V Vector Extension) refers to the vector extension of the RISC-V instruction set architecture. RISC-V is an open source instruction set architecture with a simple design, high scalability, and a wide range of applications. RVV is an optional extension of RISC-V designed to support vector processing and parallel computing. RVV defines a new set of instructions for performing vector operations. These instructions allow multiple data elements to be processed simultaneously, increasing computational efficiency and throughput. Vector operations can be performed in a single instruction without the need to process each data element through loops or operations on a case-by-case basis. RVV supports different vector lengths, and different vector lengths can be selected according to the needs of the application. The vector length can be fixed or configurable. RVV also supports different data types, including integers, floats, and fixed-point numbers.

The introduction of RVVs provides processors with vector processing and parallel computing capabilities that can accelerate various applications such as image processing, signal processing, machine learning, scientific computing, and more. At the same time, the openness and scalability of RVVs also allow manufacturers and developers to customize and optimize according to their own needs. The K230 uses the Xuantie C908 dual-core processor, of which the large-core C908 comes with RVV1.0 expansion, and this article describes how to use the RVV function on the large-core rt-smart. and experience the practical effects of RVV acceleration.

## Environment preparation

### Hardware environment

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### Software environment

k230_SDK

## Use the RVV function

### Source code writing

In order to experience the advantages of RVV acceleration in vector computing, we write a demo using image scaling as an application scenario. Create a folder in the SDK path below

`k230_sdk/src/big/rt-smart/userapps/testcases/scale`

Note that if you run make or make rt-smart under the k230_sdk, the changes may be overwritten, and readers can copy the finished source code to the following directory

`k230_sdk/src/big/unittest/testcases`

#### source

Create the C source code file scale.c in the scale directory

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

    // Calculate the size of the scaled image
    int scaledWidth = (int)(originalWidth * scaleFactor);
    int scaledHeight = (int)(originalHeight * scaleFactor);
    int scaledImageSize = scaledWidth * scaledHeight * 3;

    // Creating Output BMP Files
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
    // Scaling image data
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

    // Write scaled image data
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
    float scaleFactor = 0.5; //scaling factor
    scaleBMP(inputPath, outputPath, scaleFactor);
    return 0;
}
```

#### SCONS configuration file

- Create a SConscript file

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

- Create a SConstruct file

``` python
import os
import sys

# add building.py path
sys.path = sys.path + [os.path.join('..','..','..','tools')]
from building import *

BuildApplication('scale', 'SConscript', usr_root = '../../..')
```

### compile

Go to the directory `src/big/rt-smart` Run  Script  to `source smart-env.sh riscv64` configure environment variables.

```shell
$ source smart-env.sh riscv64
Arch         => riscv64
CC           => gcc
PREFIX       => riscv64-unknown-linux-musl-
EXEC_PATH    => /home/testUser/k230_sdk/src/big/rt-smart/../../../toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
```

Go to the `userapps/testcases/scale`directory to run `scons --release`the compilation

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

Rename the compiled program

``` shell
mv scale.elf scale_with_rvv.elf
```

Edit the k230_sdk/src/big/rt-smart/tools/riscv64 .py file to remove the v extension for the compilation option.

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

Recompile the source code, and then copy all the compiled scale.elf and scale_with_rvv.elf to sharefs for running.

### run

Prepare a 24-bit bmp image, named input.bmp (which can be saved and generated with PC Paint software), put it in the same directory as the program, and then run the two programs through sharefs.

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

From the printing information, after using the V extension instruction, the calculation of the array is significantly faster, and if you increase the resolution of the image to 4K, you can see a more obvious contrast.

### Decompile

You can use the objdump tool to decompile in the source code directory to confirm whether the vector instruction is generated

``` text
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S |grep 'vadd'
   200002c7e:03bf4dd7          vadd.vx v27,v27,t5
   200002c94:03834c57          vadd.vx v24,v24,t1
$ riscv64-unknown-linux-musl-objdump scale_with_rvv.elf -S |grep 'vmul'
   200002c98:97856c57           vmul.vx v24,v24,a0

```
