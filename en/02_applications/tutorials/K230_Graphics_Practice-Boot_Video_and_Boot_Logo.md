# K230 Graphics Practice - Boot Video and Boot Logo

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

This article explains how to implement the boot video and boot logo on the K230 EVB development board through video decoding.
The video decoding module supports H.264/H.265/MJPEG decoding, and the maximum resolution of the screen display is 1920x1080, which can be rotated.

## 1. Environmental preparation

### 1.1 Hardware Environment

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1
- Typec USB cable for power supply.
- SD card
- Screen and cable
- Camera board (IMX335)

### 1.2 Software Environment

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

## 2. Source code location

The SDK contains a user-mode decoding demo at .`k230_sdk/src/big/mpp/userapps/sample/sample_vdec` The compiled executable file is `k230_sdk/src/big/mpp/userapps/sample/elf/sample_vdec.elf`not loaded into the big core image by default, and you need to modify the Makefile according to the execution mode section to generate the executable file in the directory `/mnt` after the big core is started.

## Source code analysis

1. `sample_vb_init`: Configure VB Pool CNT and initialize VB.
1. `vb_create_pool`: Configure the block size and number of each pool in VB.
1. `kd_mpi_vdec_create_chn`: Create a decoding channel.
1. `kd_mpi_vdec_start_chn`: Turn on the decoding channel.
1. `sample_vdec_bind_vo`: Bind the decoding to VO.
1. `input_thread`: Reads data from a file and calls`kd_mpi_vdec_send_stream` to send data to the VPU.
1. `output_thread`: Get the decoded data from the VPU.

## 3. Program Execution

1. Modify the `mpp-apps`compilation script in `k230_sdk/Makefile`. Modify

   ```sh
   cp userapps/sample/fastboot_elf/* $(RTSMART_SRC_DIR)/userapps/root/bin/; \
   ```

   as

    ```sh
    cp userapps/sample/elf/sample_vdec.elf $(RTSMART_SRC_DIR)/userapps/root/bin/; \
    ```

1. Copy the H.264/H.265/MJPEG/JPEG files that need to be displayed to the`k230_sdk/src/big/rt-smart/userapps/root/bin` directory

1. Modify `k230_sdk/src/big/rt-smart/init.sh`to the following command:

    ```sh
    /bin/sample_vdec -i <filename> [-t <sec>]
    ```

    - `<filename>`is the video file copied in the previous step
    - `-t`is the time the picture is displayed, Used only when a picture is displayed.

1. Execute the command `make` under the directory `k230_sdk`.
1. The compiled and generated `k230_sdk/output/k230_evb_defconfig/images/sysimage-sdcard.img`programming is flashed to the SD card, and the EVB board DIP switch is all dialed to OFF (boot from the SD card) to realize the boot display video.

The display effect is as follows:
![boot_logo](../../../zh/02_applications/tutorials/images/boot_logo.png)
