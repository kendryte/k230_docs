# K230 Image Practical - Boot Video and Boot Logo

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter referred to as "we") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, we do not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference as a usage guide only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without written permission from the Company, no unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Overview

This document explains how to implement boot video and boot logo on the K230 EVB development board through video decoding. The video decoding module supports H.264/H.265/MJPEG decoding, with a maximum screen display resolution of 1920x1080 and can be rotated.

## 1. Environment Preparation

### 1.1 Hardware Environment

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1
- Type-C USB cable for power supply.
- SD card
- Screen and cables
- Camera sub-board (IMX335)

### 1.2 Software Environment

The k230_sdk provides toolchains located in the following paths.

- Large core rt-smart toolchain

```shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu
```

- Small core Linux toolchain

```shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0
```

You can also download the toolchains via the following links:

```shell
wget https://download.rt-thread.org/rt-smart/riscv64/riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230222.tar.bz2
wget https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource//1659325511536/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0-20220715.tar.gz
```

## 2. Source Code Location

The SDK contains a user-space decoding demo located at `k230_sdk/src/big/mpp/userapps/sample/sample_vdec`. The compiled executable file is located at `k230_sdk/src/big/mpp/userapps/sample/elf/sample_vdec.elf`. By default, it is not loaded into the large core image and requires modification of the Makefile as described in the execution section to generate the executable file in the `/mnt` directory after the large core starts.

## Source Code Analysis

1. `sample_vb_init`: Configure vb pool count and initialize vb.
1. `vb_create_pool`: Configure the block size and number of each pool in vb.
1. `kd_mpi_vdec_create_chn`: Create a decoding channel.
1. `kd_mpi_vdec_start_chn`: Start the decoding channel.
1. `sample_vdec_bind_vo`: Bind the decoder to vo.
1. `input_thread`: Read data from the file and call `kd_mpi_vdec_send_stream` to send the data to the VPU.
1. `output_thread`: Retrieve decoded data from the VPU.

## 3. Program Execution

1. Modify the `mpp-apps` compilation script in `k230_sdk/Makefile`. Change

   ```sh
   cp userapps/sample/fastboot_elf/* $(RTSMART_SRC_DIR)/userapps/root/bin/; \
   ```

   to

   ```sh
   cp userapps/sample/elf/sample_vdec.elf $(RTSMART_SRC_DIR)/userapps/root/bin/; \
   ```

1. Copy the H.264/H.265/MJPEG/JPEG files to be displayed into the `k230_sdk/src/big/rt-smart/userapps/root/bin` directory.

1. Modify `k230_sdk/src/big/rt-smart/init.sh` with the following command:

   ```sh
   /bin/sample_vdec -i <filename> [-t <sec>]
   ```

   - `<filename>` is the video file copied in the previous step.
   - `-t` is used only when displaying images, specifying the display duration.

1. Execute the `make` command in the `k230_sdk` directory.
1. Write the compiled `k230_sdk/output/k230_evb_defconfig/images/sysimage-sdcard.img` to the SD card, set all DIP switches on the EVB board to OFF (boot from SD card), and the boot video will be displayed.

The display effect is as follows:
![boot_logo](../../../zh/02_applications/tutorials/images/boot_logo.png)
