# K230 SDK User Guide

![cover](../../../zh/01_software/board/images/canaan-cover.png)

Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contract and terms of Canaan Creative (Beijing) Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. Some or all of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not make any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is only for guidance and reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/01_software/board/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Canaan Creative (Beijing) Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may copy or reproduce any part or all of the content of this document, nor may it be disseminated in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the installation and use of the K230 SDK.

### Target Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
|              |             |

### Revision History

| Document Version | Modification Description       | Modifier | Date       |
|------------------|--------------------------------|----------|------------|
| V1.0             | Initial version                | Yang Guang | 2023-03-10 |
| V1.1             | Added secure image and emmc burning instructions | Wang Jianxin | 2023-04-07 |
| V1.2             | Added spinor image burning instructions | Wang Jianxin | 2023-05-05 |
| V1.3             | Quick start and secure image instructions | Wang Jianxin | 2023-05-29 |
| V1.4             | Large core self-start program instructions | Hao Haibo | 2023-06-01 |
| V1.5             | usip lp4                      | Wang Jianxin | 2023-06-12 |
| V1.6             | Modified large core self-start program instructions | Zhao Zhongxiang | 2023-06-28 |
| V1.7             | Added boot medium partition chapter, adjusted image burning chapter | Wang Jianxin | 2023-07-05 |
| V1.8             | Added CanMV-K230 motherboard information | Chen Haibin | 2023-10-11 |

## 1. Overview

### 1.1 SDK Software Architecture Overview

The K230 SDK is a software development kit for the K230 development board, containing the source code, toolchain, and other related resources needed for dual-core heterogeneous system development based on Linux & RT-smart.

The K230 SDK software architecture is shown in Figure 1-1:

![logo](../../../zh/01_software/board/images/cee49715351f6dd3496baf19af1262ed.png)

Figure 1-1 K230 SDK Software Architecture Diagram

## 2. Development Environment Setup

### 2.1 Supported Hardware

For hardware information on the K230 platform, refer to the directory: [00_hardware](../../00_hardware). The hardware information documents for different motherboards are as follows:

| Motherboard Type      | Hardware Reference Directory |
|-----------------------|------------------------------|
| K230-USIP-LP3-EVB     | For specific hardware information, refer to: [00_hardware/K230_LP3](../../../zh/00_hardware/K230_LP3) |
| K230-USIP-LP4-EVB     | For specific hardware information, refer to: [00_hardware/K230_LP4](../../../zh/00_hardware/K230_LP4) |
| K230-SIP-LP3-EVB      | For specific hardware information, refer to: [00_hardware/K230D](../../../zh/00_hardware/K230D) |
| CanMV-K230            | For specific hardware information, refer to: [00_hardware](../../../zh/00_hardware/CanMV_K230) |
| CanMV-K230D-Zero      |                              |

### 2.2 Development Environment Setup

#### 2.2.1 Compilation Environment

| Host Environment              | Description                                               |
|-------------------------------|-----------------------------------------------------------|
| Docker Compilation Environment | The SDK provides a dockerfile to generate a docker image for compiling the SDK |
| Ubuntu 20.04.4 LTS (x86_64)   | The SDK can be compiled in the Ubuntu 20.04 environment     |

The K230 SDK needs to be compiled in a Linux environment. The SDK supports compilation in a Docker environment, and the SDK development package includes a dockerfile (`tools/docker/Dockerfile`) to generate the Docker image. For detailed dockerfile usage and compilation steps, see section 4.3.1.

The Docker image used by the SDK is based on Ubuntu 20.04. If not using the Docker compilation environment, you can refer to the dockerfile content in the Ubuntu 20.04 host environment, install the relevant host packages and toolchains, and then compile the SDK.

The K230 SDK has not been verified in other Linux versions of host environments, and it is not guaranteed that the SDK can be compiled in other environments.

#### 2.2.2 SDK Development Package

The K230 SDK is released in the form of a compressed package, or you can download it using the `git clone https://github.com/kendryte/k230_sdk` command.

### 2.3 Board Preparation

This section takes the K230-USIP-LP3-EVB and CanMV-K230 motherboards as examples.

#### 2.3.1 CanMV-K230

Please prepare the following hardware:

- CanMV-K230
- At least one Type-C USB cable
- One Ethernet cable (optional)
- One HDMI cable
- SD card
- HDMI-compatible monitor

Note: The CanMV-K230 motherboard shares a Type-C port for power and serial communication, as shown below:

![Diagram](../../../zh/01_software/board/images/canmv_power_001.png)

#### 2.3.2 K230-USIP-LP3-EVB

Please prepare the following hardware:

- K230-USIP-LP3-EVB
- At least two Type-C USB cables
- Type-C USB to Ethernet adapter (optional)
- One Ethernet cable (optional)
- SD card (optional)

Note: The recommended model for the Type-C USB to Ethernet adapter is `https://item.jd.com/5326738.html`.

Refer to the "K230 DEMO BOARD Resource Usage Instructions" to prepare the development board.

#### 2.3.3 Serial Port

The K230 motherboard provides two debug serial ports via USB. To use the debug serial ports on Windows, you need to install the USB to serial driver. The driver download link is as follows:

`https://ftdichip.com/wp-content/uploads/2021/11/CDM-v2.12.36.4.U-WHQL-Certified.zip`

After installing the driver, power on the board, connect the PC to the debug serial port of the motherboard using a Type-C data cable, and you should see two USB serial devices as shown below:

![Diagram](../../../zh/01_software/board/images/bcb6636268b91758f87ff54523251eeb.png)

Figure 2-1 USB Serial Devices

In the example above, `COM47` is the debug serial port for the small core, and `COM48` is the debug serial port for the large core.

Serial port baud rate settings: `115200 8N1`

## 3. SDK Installation Preparation

### 3.1 Install SDK

The K230 SDK development package is released in the form of a compressed package for use in a Linux environment.

### 3.2 SDK Directory Structure

The K230 SDK directory structure is shown below:

```shell
k230_sdk
├── configs
│   ├── k230_evb_defconfig
│   └── k230_evb_usiplpddr4_defconfig
│   └── k230d_defconfig
├── Kconfig
├── LICENSE
├── Makefile
├── parse.mak
├── README.md
├── repo.mak
├── src
│   ├── big
│   │   ├── mpp
│   │   ├── rt-smart
│   │   └── unittest
│   ├── common
│   │   ├── cdk
│   │   └── opensbi
│   ├── little
│   │   ├── buildroot-ext
│   │   ├── linux
│   │   └── uboot
│   └── reference
│       ├── ai_poc
│       ├── business_poc
│       └── fancy_poc
├── board
│   ├── common
│   │   ├── env
│   │   └── gen_image_cfg
│   │   ├── gen_image_script
│   │   └── post_copy_rootfs
│   ├── k230_evb_doorlock
│   └── k230_evb_peephole_device
└── tools
    ├── docker
    │   └── Dockerfile
    ├── doxygen
    ├── firmware_gen.py
    └── get_download_url.sh
```

The purpose of each directory is described as follows:

- `configs`: Stores the board-level default configurations of the SDK, mainly including information such as reference board type, toolchain path, memory layout planning, and storage planning configuration.

- `src`: Source code directory, divided into three directories: large core code (`big`), common components (`common`), and small core code (`little`).

    Large core code includes: `rt-smart` operating system code, `mpp` code, `unittest` code.

    Common components include: `cdk` code and `opensbi` code.

    Small core code includes: `linux` kernel code, `buildroot` code, `uboot` code.

- `tools`: Stores various tools, scripts, etc., such as `kconfig`, `doxygen`, `dockerfile`, etc.
- `board`: Environment variables, image configuration files, file systems, etc.

## 4. SDK Compilation

### 4.1 SDK Compilation Introduction

The K230 SDK supports one-click compilation of large and small core operating systems and common components, generating image files that can be burned for deployment to the development board for startup and operation. The username of the Linux system on the device is root without a password.

### 4.2 SDK Configuration

The K230 SDK uses Kconfig as the SDK configuration interface, and the default board-level configurations supported are placed in the configs directory.

#### 4.2.1 Some Configuration File Descriptions

`k230_evb_defconfig`: Default SDK configuration file based on K230 USIP LP3 EVB.

`k230_evb_usiplpddr4_defconfig`: Default SDK configuration file based on K230 USIP LP4 EVB.

`k230d_defconfig`: Default SDK configuration file based on K230-SIP-LP3-EVB.

`k230_evb_nand_defconfig`: Default SDK configuration file for generating nand images based on K230 USIP LP3 EVB.

`k230_canmv_defconfig`: Default SDK configuration file based on CanMV-K230 V1.0/V1.1.

`k230_evb_doorlock_defconfig`: Default SDK configuration file for door lock POC based on K230 USIP LP3 EVB.

`k230_evb_peephole_device_defconfig`: Default SDK configuration file for peephole POC based on K230 USIP LP3 EVB.

`k230d_doorlock_defconfig`: Default SDK configuration file for door lock POC based on K230-SIP-LP3-EVB.

`k230_canmv_v2_defconfig`: Default SDK configuration file based on Canmv-K230 V2.0 board.

`k230_canmv_only_rtt_defconfig`: RT-Thread system configuration file based on Canmv-K230 V1.0/V1.1 board.

`k230_canmv_v2_only_rtt_defconfig`: RT-Thread system configuration file based on Canmv-K230 V2.0 board.

`k230d_canmv_only_rtt_defconfig`: RT-Thread system configuration file based on CanMV-K230-Zero board.

### 4.3 Compile SDK

#### 4.3.1 Compilation Steps

Note: The commands in this section are for reference only. Please replace the file names according to the actual situation.

Step 1: Download the code

`git clone https://github.com/kendryte/k230_sdk`

Step 2: Enter the SDK root directory

`cd k230_sdk`

Step 3: Download the toolchain

```shell
source tools/get_download_url.sh && make prepare_sourcecode
```

> `make prepare_sourcecode` will download both Linux and RT-Smart toolchain, buildroot package, and AI package from Microsoft Azure cloud server with CDN. The download time may vary based on your network connection speed.

Step 4: Generate the Docker image (required for the first compilation, skip this step if the Docker image has already been generated)

`docker build -f tools/docker/Dockerfile -t k230_docker tools/docker`

Step 5: Enter the Docker environment

`docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash`

Step 6: In the Docker environment, execute the following command to compile the SDK

```bash
make CONF=k230_evb_defconfig  # Compile image for K230-USIP-LP3-EVB board
#make CONF=k230_evb_usiplpddr4_defconfig  # Compile image for K230-USIP-LP4-EVB board
#make CONF=k230d_defconfig  # Compile image for K230-SIP-LP3-EVB board
#make CONF=k230_evb_nand_defconfig  # Compile nand image for K230-USIP-LP3-EVB board
```

> - To compile the image for the K230-USIP-LP4-EVB board, use the `make CONF=k230_evb_usiplpddr4_defconfig` command.
> - To compile the image for the K230-USIP-LP3-EVB board, use the `make CONF=k230_evb_defconfig` command.
> - To compile the image for the K230-SIP-LP3-EVB board, use the `make CONF=k230d_defconfig` command.
> - To compile the NAND image for the K230-USIP-LP3-EVB board, use the `make CONF=k230_evb_nand_defconfig` command.
> - To compile the image for the CanMV-K230 board, use the `make CONF=k230_canmv_defconfig` command.

Note:
The SDK does not support multi-process compilation, so do not add multi-process compilation parameters like `-j32`.

#### 4.3.2 Compilation Output

After the compilation is complete, you can find the output products in the `output/xx_defconfig/images` directory. Example:

![Text Description Automatically Generated](../../../zh/01_software/board/images/da6d48091ee0af8107a63cde01a2b75b.png)

Figure 4-1 Compilation Output

The image files in the `images` directory are explained as follows:

- `sysimage-sdcard.img` — Non-secure boot image for SD and eMMC.
- `sysimage-sdcard.img.gz` — Compressed non-secure boot image for SD and eMMC (gzip compressed package of `sysimage-sdcard.img`), needs to be decompressed before burning.
- `sysimage-sdcard_aes.img.gz` — AES secure boot image compressed package for SD and eMMC, needs to be decompressed before burning.
- `sysimage-sdcard_sm.img.gz` — SM secure boot image compressed package for SD and eMMC, needs to be decompressed before burning.

Secure images are not generated by default. If secure images are needed, refer to section 4.3.4 to enable secure images.

The compilation output for the large core system is placed in the `images/big-core` directory.

The compilation output for the small core system is placed in the `images/little-core` directory.

#### 4.3.3 Non-Quick Boot Image

By default, the SDK compiles a quick boot image (U-Boot directly starts the system and does not enter the U-Boot command line). If you need to enter the U-Boot command line, refer to the following to disable the `CONFIG_QUICK_BOOT` configuration:

In the SDK main directory, execute `make menuconfig`, select `board configuration`, and uncheck the `quick boot` configuration option.

To convert a non-quick boot system to a quick boot system: enter the U-Boot command line and execute `setenv quick_boot true; saveenv;`.

#### 4.3.4 Secure Image

By default, the SDK does not generate secure images. If secure images are needed, refer to the following to add the `CONFIG_GEN_SECURITY_IMG` configuration:

In the SDK main directory, execute `make menuconfig`, select `board configuration`, and check the `create security image` option.

#### 4.3.5 Debug Image

By default, the SDK generates a release image. If a debug image is needed, refer to the following to add the `CONFIG_BUILD_DEBUG_VER` configuration:

In the SDK main directory, execute `make menuconfig`, select `build debug/release version`, and check the `debug` option.

## 5. SDK Image Burning

Depending on the hardware characteristics and software requirements of different boards, choose the supported image burning method.
> The CanMV-K230 board only supports SD card image booting.

### 5.1 SD Card Image Burning

#### 5.1.1 Burning on Ubuntu

Before inserting the SD card into the host, enter:

`ls -l /dev/sd*`

to view the current storage devices.

After inserting the SD card into the host, enter again:

`ls -l /dev/sd*`

to view the storage devices at this time. The newly added device is the SD card device node.

Assuming `/dev/sdc` is the SD card device node, execute the following command to burn the SD card:

`sudo dd if=sysimage-sdcard.img of=/dev/sdc bs=1M oflag=sync`

Note: `sysimage-sdcard.img` can be the `sysimage-sdcard.img` file in the `images` directory or the decompressed file of the `sysimage-sdcard_aes.img.gz`, `sysimage-sdcard.img.gz`, or `sysimage-sdcard_sm.img.gz` files.

#### 5.1.2 Burning on Windows

On Windows, you can use the Rufus tool to burn the TF card (Rufus tool download link: `http://rufus.ie/downloads/`).

1) Insert the TF card into the PC, then start the Rufus tool and click the "Select" button on the tool interface to choose the firmware to be burned.
![rufus-flash-from-file](../../../zh/images/rufus_select.png)
1) Click the "Start" button to begin burning. The burning process will display a progress bar, and it will indicate "Ready" when the burning is complete.

![rufus-flash](../../../zh/images/rufus_start.png)
![rufus-sure](../../../zh/images/rufus_sure.png)
![rufus-warning](../../../zh/images/rufus_warning.png)
![rufus-finish](../../../zh/images/rufus_finish.png)

### 5.2 eMMC Image Burning Reference

#### 5.2.1 Burning eMMC on Linux

1) Download the compressed image package to the SD card.
Boot Linux from the SD card. In Linux, you can refer to the following commands to download the compressed image package to the SD card:

```shell
ifconfig eth0 up; udhcpc; mount /dev/mmcblk1p4 /mnt; cd /mnt/;
scp wangjianxin@10.10.1.94:/home/wangjianxin/k230_sdk/output/k230_evb_defconfig/images/sysimage-sdcard.img.gz .
```

1) Decompress the package to eMMC:
`gunzip sysimage-sdcard.img.gz -c > /dev/mmcblk0`
1) Switch to eMMC boot and restart the board.

#### 5.2.2 Burning eMMC in U-Boot

1) Download the `sysimage-sdcard.img.gz` image to memory:

```bash
usb start; dhcp; tftp 0x9000000 10.10.1.94:wjx/sysimage-sdcard.img.gz;
# Note: Replace 0x9000000 based on memory size, e.g., if memory is only 128MB, replace it with 0x2400000
```

1) Write the image to eMMC:

```bash
gzwrite mmc 0 0x${fileaddr} 0x${filesize};
```

1) Restart the board.

### 5.3 Spinor Image Burning Reference

#### 5.3.1 Burning in U-Boot

1) Download the `sysimage-spinor32m.img` image to memory:

```bash
usb start; dhcp; tftp 0x9000000 10.10.1.94:wjx/sysimage-spinor32m.img;
# Note: Replace 0x9000000 based on memory size, e.g., if memory is only 128MB, replace it with 0x2400000
```

1) Write the image to SPI NOR flash:

```bash
sf probe 0:0; sf erase 0 0x2000000; sf write 0x$fileaddr 0 0x$filesize; sf remove;
```

1) Restart the board.

#### 5.3.2 Burning Spinor on Linux

1) Download the spinor image `sysimage-spinor32m.img` to the SD card.

Boot Linux from the SD card. In Linux, you can refer to the following commands to download the image to the SD card:

```bash
ifconfig eth0 up; udhcpc; mount /dev/mmcblk1p4 /mnt; cd /mnt/;
scp wangjianxin@10.10.1.94:/home/wangjianxin/k230_sdk/output/k230_evb_defconfig/images/sysimage-spinor32m.img .
```

1) Refer to the following command to write the image to SPI NOR flash:

```bash
[root@canaan /mnt]# flashcp -v sysimage-spinor32m.img /dev/mtd9
Erasing blocks: 508/508 (100%)
Writing data: 32512k/32512k (100%)
Verifying data: 32512k/32512k (100%)
[root@canaan /mnt]#
```

1) Switch to SPI NOR boot and restart the board.

#### 5.3.3 Spinor Image Description

Due to the small size of the spinor flash, Linux has removed ko files and RT-Thread has removed some demo programs.

### 5.4 Spinand Image Burning Reference

#### 5.4.1 Burning in U-Boot

1) Download the `sysimage-spinand32m.img` image to memory:

`usb start; dhcp; tftp 0x9000000 10.10.1.94:wjx/sysimage-spinand32m.img;`

1) Write the image to SPI NAND flash:

`mtd erase spi-nand0 0 0x2000000; mtd write spi-nand0 0x$fileaddr 0 0x$filesize;`

1) Restart the board.

## 6. SDK Boot Medium Partition and Modification

### 6.1 SPI NOR

#### 6.1.1 Default SPI NOR Partition

![image-spi_nor_default_part](../../../zh/01_software/board/images/image-spi_nor_default_part.png)

| SPI NOR Partition |           |          |        |         |
|-------------------|-----------|----------|--------|---------|
| Content           | Start Addr| Size     | Size MB| Size    |
| Primary U-Boot    | 0x0       | 512KB    | 0.5    | 512KB   |
| Secondary U-Boot  | 0x80000   | 0x160000 | 1.375  | 1.375MB |
| U-Boot Env Vars   | 0x1e0000  | 128KB    | 0.125  | 128KB   |
| Quick Boot Params | 0x200000  | 512KB    | 0.5    | 512KB   |
| Face Features     | 0x280000  | 512kB    | 0.5    | 512kB   |
| Calibration Params| 0x300000  | 256KB    | 0.25   | 256KB   |
| AI Model          | 0x340000  | 3MB      | 3      | 3MB     |
| Speckle           | 0x640000  | 2MB      | 2      | 2MB     |
| RT-Thread         | 0x840000  | 0x1c0000 | 1.75   | 1.75MB  |
| RT-Thread App     | 0xa00000  | 0x5c0000 | 5.75   | 3.75MB  |
| Linux             | 0xfc0000  | 0x700000 | 7      | 7MB     |
| Rootfs            | 0x16c0000 | 0xb00000 | 13     | 13MB    |

#### 6.1.2 Partition Modification and Implementation Description

In the SDK main directory, execute `make menuconfig` ---> `storage configurations` ---> `spi nor partition config` to modify the partition (interface shown below). After modification, execute `make build-image`.

![image-image-menuconfig_spi_nor_part](../../../zh/01_software/board/images/image-menuconfig_spi_nor_part.png)

Detailed implementation of partition modification through menuconfig:

After configuring with `make menuconfig`, a `.config` file is generated (partial content shown below):

```bash
CONFIG_SPI_NOR_SENSOR_CFG_CFG_BASE=0x300000
CONFIG_SPI_NOR_SENSOR_CFG_CFG_SIZE=0x40000
CONFIG_SPI_NOR_AI_MODE_CFG_BASE=0x340000
CONFIG_SPI_NOR_AI_MODE_CFG_SIZE=0x300000
CONFIG_SPI_NOR_SPECKLE_CFG_BASE=0x640000
CONFIG_SPI_NOR_SPECKLE_CFG_SIZE=0x200000
CONFIG_SPI_NOR_RTTK_BASE=0x840000
CONFIG_SPI_NOR_RTTK_SIZE=0x1c0000
CONFIG_SPI_NOR_RTT_APP_BASE=0xa00000
CONFIG_SPI_NOR_RTT_APP_SIZE=0x5c0000
CONFIG_SPI_NOR_LK_BASE=0xfc0000
CONFIG_SPI_NOR_LK_SIZE=0x700000
CONFIG_SPI_NOR_LR_BASE=0x16c0000
CONFIG_SPI_NOR_LR_SIZE=0x900000
```

The `tools/menuconfig_to_code.sh` script will dynamically modify the Linux device tree and `board/common/gen_image_cfg/genimage-spinor.cfg` file based on these definitions (key script shown below):

```bash
image sysimage-spinor32m.img {
    flash {}
    flashtype = "spinor-32M-gd25lx256e"
    .....
    partition quick_boot_cfg {
        offset = ${CONFIG_SPI_NOR_QUICK_BOOT_CFG_BASE}
        image = "${quick_boot_cfg_data_file}"
        size = ${CONFIG_SPI_NOR_QUICK_BOOT_CFG_SIZE}
    }

    partition face_db {
        offset = ${CONFIG_SPI_NOR_FACE_DB_CFG_BASE}
        image = "${face_database_data_file}"
        size = ${CONFIG_SPI_NOR_FACE_DB_CFG_SIZE}
    }

    partition sensor_cfg {
        offset = ${CONFIG_SPI_NOR_SENSOR_CFG_CFG_BASE}
        image = "${sensor_cfg_data_file}"
        size = ${CONFIG_SPI_NOR_SENSOR_CFG_CFG_SIZE}
    }

    partition ai_mode {
        offset = ${CONFIG_SPI_NOR_AI_MODE_CFG_BASE}
        image = "${ai_mode_data_file}"
        size = ${CONFIG_SPI_NOR_AI_MODE_CFG_SIZE}
    }

    partition speckle_cfg {
        offset = ${CONFIG_SPI_NOR_SPECKLE_CFG_BASE}
        image = "${speckle_data_file}"
        size = ${CONFIG_SPI_NOR_SPECKLE_CFG_SIZE}
    }

    partition rtt {
        offset = ${CONFIG_SPI_NOR_RTTK_BASE}
        image = "big-core/rtt_system.bin"
        size = ${CONFIG_SPI_NOR_RTTK_SIZE}
    }
    partition rtt_app {
        offset = ${CONFIG_SPI_NOR_RTT_APP_BASE}
        image = "${rtapp_data_file}"
        size = ${CONFIG_SPI_NOR_RTT_APP_SIZE}
    }

    partition linux {
        offset = ${CONFIG_SPI_NOR_LK_BASE}
        image = "little-core/linux_system.bin"
        size = ${CONFIG_SPI_NOR_LK_SIZE}
    }
    partition rootfs_ubi {
        offset = ${CONFIG_SPI_NOR_LR_BASE}
        image = "rootfs.ubi"
        size = ${CONFIG_SPI_NOR_LR_SIZE}
    }
}
```

Finally, `genimage` will parse the `board/common/gen_image_cfg/genimage-spinor.cfg` file and generate the correct image.

```bash
genimage --rootpath little-core/rootfs/ --tmppath genimage.tmp --inputpath images --outputpath images --config board/common/gen_image_cfg/genimage-spinor.cfg
```

### 6.1.3 Partition Data Format and Generation Process

Currently, the data in parameter partitions such as quick boot parameters, facial features, calibration parameters, AI models, speckle, RTT, and RTApp are not encrypted. The format and generation process are as follows:

![image-20230705151949318](../../../zh/01_software/board/images/image-non_crypt.png)

The main generation script is as follows:

```bsh
# For more detailed generation details, please read the gen_cfg_part_bin function in the board/common/gen_image_script/gen_image_comm_func.sh script
${k230_gzip} -f -k ${filename}  # gzip
sed -i -e "1s/\x08/\x09/"  ${filename}.gz
# add uboot head
${mkimage} -A riscv -O linux -T firmware -C gzip -a ${add} -e ${add} -n ${name}  -d ${filename}.gz  ${filename}.gzu;
python3  ${firmware_gen}   -i ${filename}.gzu -o fh_${filename} ${arg}; # add k230 firmware head
```

The corresponding execution process prints as follows:

```bash
##  + k230_priv_gzip -n8 -f -k speckle.bin
##  + sed -i -e '1s/\x08/\x09/' speckle.bin.gz
##  + mkimage -A riscv -O linux -T firmware -C gzip -a 0x14040000 -e 0x14040000 -n speckle -d speckle.bin.gz speckle.bin.gzu
##  Image Name:   speckle
##  Created:      Wed Jul  5 15:37:49 2023
##  Image Type:   RISC-V Linux Firmware (gzip compressed)
##  Data Size:    45 Bytes = 0.04 KiB = 0.00 MiB
##  Load Address: 14040000
##  Entry Point:  14040000
##  + python3 /home/wangjianxin/k230_sdk/tools/firmware_gen.py -i speckle.bin.gzu -o fh_speckle.bin -n
##  the magic is:  b'K230'
##  ----- NO ENCRYPTION + HASH-256 -----
##  the encryption type:  0
##  mesg_hash:  b'3543e2038aedad88a29f8ee98983064367cc79f6e709ed7571df9b391884b8b1'
```

When U-Boot starts, it will parse and verify the parameter partitions (quick boot parameters, facial features, calibration parameters, AI models, speckle, RTT, RTApp) data and load the parsed raw data into the correct memory locations.

The memory locations for each parameter partition can be configured via `make menuconfig -> Memory configuration` (reference interface below):

![image-20230705153242437](../../../zh/01_software/board/images/image-memconfig_part.png)

#### 6.1.4 Special Notes on RTApp and AI Model Partitions

The app in the RTApp partition cannot be executed repeatedly. The purpose of designing this partition is to save memory. After executing the app in this partition once, the memory may be released and cannot be executed again.

During compilation, the pointers to the model files in the large core ROMFS file system will be modified to the AI model area (see the script below). The usage method is the same as using ordinary files.

```bash
# For details, see the board/common/gen_image_script/gen_image.sh file
for f in ${all_kmode};
    do
        eval fstart="\${${f%%\.*}_start}"
        eval fsize="\${${f%%\.*}_size}"
        fstart=$(printf "0x%x" $((${fstart} + ${CONFIG_MEM_AI_MODEL_BASE})))
        fsize=$(printf "0x%x" ${fsize})
        sed -i "s/_bin_$f,/(char*)${fstart},/g" ${RTSMART_SRC_DIR}/kernel/bsp/maix3/applications/romfs.c
        sed -i "s/sizeof(_bin_$f)/${fsize}/g" ${RTSMART_SRC_DIR}/kernel/bsp/maix3/applications/romfs.c
    done
```

#### 6.1.5 Verified SPI NOR Models

- gd25lx256e

### 6.2 SD and eMMC

#### 6.2.1 Default SD and eMMC Partitions

![image-20230705100321637](../../../zh/01_software/board/images/sd_emmc_default_partion.png)

| SD/eMMC Default Partitions |           |            |        |       |
| -------------------------- | --------- | ---------- | ------ | ----- |
| Content                    | Start Addr| Size       | Size MB| Size  |
| MBR Partition Table        | 0x0       | 0x100000   | 1      | 1MB   |
| Primary U-Boot             | 0x100000  | 0x80000    | 0.5    | 512KB |
| Backup Primary Boot        | 0x180000  | 0x60000    | 0.375  | 384KB |
| U-Boot Environment Vars    | 0x1e0000  | 0x20000    | 0.125  | 128KB |
| Secondary U-Boot           | 0x200000  | 0x800000   | 0.5    | 8MB   |
| RTT                        | 0xa00000  | 0x1400000  | 20     | 20MB  |
| Linux                      | 0x1e00000 | 0x6200000  | 98     | 98MB  |
| Rootfs                     | 0x8000000 | 0x5000000  | 80     | 80MB  |
| Test Partition             | 0xd000000 | 0x10000000 | 256    | 256MB |

#### 6.2.2 SD and eMMC Partition Modification

If partitioning is required, modify the `board/common/gen_image_cfg/genimage-sdcard.cfg` file. After modification, execute `make build-image`.

### 6.3 SPI NAND

#### 6.3 Default SPI NAND Partitions

![image-20230705111015174](../../../zh/01_software/board/images/image-spi_nand_part.png)

| SPI NAND Partitions |           |          |           |        |         |
| ------------------- | --------- | -------- | --------- | ------ | ------- |
| Content             | Start Addr| Size     | Start Addr| Size MB| Size    |
| Primary U-Boot      | 0x0       | 512KB    | 0x0       | 0.5    | 512KB   |
| Secondary U-Boot    | 0x80000   | 0x160000 | 0x80000   | 1.375  | 1.375MB |
| U-Boot Environment Vars | 0x1e0000  | 128KB    | 0x1e0000  | 0.125  | 128KB   |
| RTT                 | 0x200000  | 0x800000 | 0x200000  | 8      | 8MB     |
| Linux               | 0xa00000  | 0x700000 | 0xa00000  | 7      | 7MB     |
| Rootfs              | 0x1100000 | 0xf00000 | 0x1100000 | 15     | 15MB    |

#### 6.3.2 SPI NAND Partition Modification

If partitioning is required, modify the `board/common/gen_image_cfg/genimage-spinand.cfg` file. After modification, execute `make build-image`.

#### 6.3.4 Verified SPI NAND Models

- w25n01gw

## 7. SDK Memory Configuration

Run `make menuconfig -> Memory configuration` under `k230_sdk` to configure the memory space used by each area. You can also directly compile `configs/k230_evb_defconfig` to modify. The descriptions of each area are as follows:

``` shell
CONFIG_MEM_TOTAL_SIZE="0x20000000"      # Total memory capacity          Not configurable
CONFIG_MEM_PARAM_BASE="0x00000000"      # Parameter partition start address Not configurable
CONFIG_MEM_PARAM_SIZE="0x00100000"      # Parameter partition size       Not configurable
CONFIG_MEM_IPCM_BASE="0x00100000"       # Inter-core communication start address Not configurable
CONFIG_MEM_IPCM_SIZE="0x00100000"       # Inter-core communication shared memory size Not configurable
CONFIG_MEM_RTT_SYS_BASE="0x00200000"    # Large core RTT start address   Configurable
CONFIG_MEM_RTT_SYS_SIZE="0x07E00000"    # Large core RTT address range   Configurable
CONFIG_MEM_AI_MODEL_BASE="0x1FC00000"   # AI model loading start address Configurable
CONFIG_MEM_AI_MODEL_SIZE="0x00400000"   # AI model loading address range Configurable
CONFIG_MEM_LINUX_SYS_BASE="0x08000000"  # Small core Linux start address Configurable
CONFIG_MEM_LINUX_SYS_SIZE="0x08000000"  # Small core Linux address range Configurable
CONFIG_MEM_MMZ_BASE="0x10000000"        # MMZ shared memory start address Configurable
CONFIG_MEM_MMZ_SIZE="0x0FC00000"        # MMZ shared memory range        Configurable
CONFIG_MEM_BOUNDARY_RESERVED_SIZE="0x00001000"  # Isolation zone         Not configurable
```

> The `CONFIG_MEM_LINUX_SYS_BASE` address needs to be 2MB aligned.

## 8. SDK Board Debugging

> The CanMV-K230 board's default debug port is a serial port. For debugging, please refer to the [SDK FAQ](../../../zh/03_other/K230_SDK常见问题解答_C.md).

### 8.1 Preparation for Debugging

1. Download the `T-Head-DebugServer` software and the "DebugServer User Guide v5.6" from T-Head's OCC platform `https://occ.t-head.cn/community/download`, and install the `T-Head-DebugServer` software on your PC following the "DebugServer User Guide v5.6".

![图形用户界面, 文本, 应用程序 描述已自动生成](../../../zh/01_software/board/images/830f7333997768ba1fa01e69aedeeb88.png)

![图形用户界面, 文本, 应用程序, 电子邮件 描述已自动生成](../../../zh/01_software/board/images/a3ee5b66a56b295c092465fec74ed086.png)

1. Prepare the T-Head CKLink, USB cable, and K230 EVB board as shown below:

![图片包含 游戏机, 电缆, 电路 描述已自动生成](../../../zh/01_software/board/images/8e91f1cc85daee080e3de5f875542bc8.png)

### 8.2 Debugging

1. Connect the CKLink, K230 EVB board, and PC as shown below, then power on the EVB.

![电子仪器被放在电脑旁边 中度可信度描述已自动生成](../../../zh/01_software/board/images/cc18bccbf8054dde022db7f9c07df307.png)

1. Open the T-Head DebugServer software on the PC. If the connection is successful, you will see output similar to the image below. If the connection fails, refer to the "DebugServer User Guide v5.6" to troubleshoot.
![文本 描述已自动生成](../../../zh/01_software/board/images/33d48fa7906e4bf8a0aed4aad7c28178.png)
1. On the server where the code is compiled, start `riscv64-unknown-linux-gnu-gdb` and execute the `target remote xx.xx.xx.xx:1025` command to connect to the board. Once connected, you can perform GDB debugging.
![文本 描述已自动生成](../../../zh/01_software/board/images/2fed09a9dbe48eeeb639b6f977861c77.png)

## 9. SDK Boot

With the default compiled image, after burning it to the board, the large core will automatically run a facial detection program, and the display will show images captured by the camera. After booting, you can enter 'q' on the large core console to exit the program.

> 1. If the EVB series board is not connected to the IMX335 camera, the auto-start program will report an error and exit automatically. Press Enter to return to the console.
> 1. To disable the auto-start function of the large core, comment out the content in `k230_sdk/src/big/rt-smart/init.sh`.

## 10. K230 Debian and Ubuntu Image Instructions

For the image and build methods, refer to [K230_debian_ubuntu.md](../../../en/03_other/K230_debian_ubuntu.md).
