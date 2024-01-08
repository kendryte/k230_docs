# K230 FAQ

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../zh/03_other/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserve**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly describes the content related to the release of K230 SDK V0.9.0, including the hardware, features, and usage restrictions supported by the current version.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation               | illustrate                                                   |
|--------------------|--------------------------------------------------------|
| K230 USIP LP3 EVB | The K230 chip in the USIP package is equipped with an LPDDR3 development board              |
| EXPIRES               | Video Encoder, a video coding module                            |
| VDEC               | Video Decoder, a video decoding module                            |
| VICAP              | Video Input Capture, an image input acquisition module                  |
| IN                 | Video Output, a video output module                             |
| .AI                 | Audio Input, the audio input module                              |
| TO                 | Audio Output, the audio output module                             |
| AENC               | Audio Encoder, an audio coding module                            |
| ADEC               | Audio Decoder, an audio decoding module                            |
| NonAI-2D           | 2D graphics acceleration processing module, support OSD overlay, picture frame, CSC transformation and other functions. |
| MCM                | Multi Camera Management                  |

### Revision history

| Document version number | Modify the description | Author     | date     |
|------------|----------|------------|----------|
| V1.0       | Initial     | System Software Department | 2023-9-4 |

## 1. Version Information

| Affiliated products | Version number | Release date |
|----------|--------|----------|
| K230 SDK | V1.0.0 | 2023-9-4|

## 2. FAQs

### 2.1 TF boot failed with exit code 13

Problem: TF card boot fails with exit code 13 error

Answer: The reasons are as follows: 1. The file error in the boot media. 2. The startup pin is set incorrectly.

TF card boot pin setting special instructions: The two start pin levels are high (need to dial to silkscreen 1 and 2, that is, the opposite direction of ON) to boot from the TF card.

### 2.2 BootROM boot error code

Question: What does the bootrom boot error code mean?

When bootROM fails to boot, it will print an error similar to the following boot failed with exit code 19, the last number is the cause of the error, and the common error meaning is as follows

| value   | meaning                                                |
| ---- | --------------------------------------------------- |
| 13   | The boot media contains a file error                                |
| 19   | Boot media initialization failed, such as not inserting an SD card                |
| 17   | The OTP requirement must be a secure image, but the files on the media are non-secure images |

### 2.3 SPI NOR and SPI NAND Flash identify

Question: How do I know if SPI NOR or SPI NAND Flash is connected to the EVB board?

Answer: Method 1: The daughter plate silk screen printing is different, the silk screen will have NOR or NAND logo.

Method 2: The Linux boot log will be printed, for example, when connecting to SPI Nor, it will be printed like the following

```bash
[root@canaan ~ ]#dmesg | grep spi
[    1.299989] spi spi0.0: setup mode 0, 8 bits/w, 100000000 Hz max --> 0
[    1.306704] spi-nor spi0.0: gd25lx256e (32768 Kbytes)
[    1.311786] 2 fixed-partitions partitions found on MTD device spi0.0
[    1.318147] Creating 2 MTD partitions on "spi0.0":
```

### 2.4 Perf Use

Question: How is perf compiled and what hardware events are supported?

A: The reference image with PERF function is linked below<https://kvftsfijpo.feishu.cn/file/LJjpbwxnzowI9RxvL0NcEK73nkf?from=from_copylink>

When perf, you can use the RAW event, such as perf stat -e r12, and the perf tool compile command as follows

```bash
cd src/little/linux/tools
make CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv perf V=1 WERROR=0
#The target file is perf/perf, please copy this file to the board.
```

Special note: Versions prior to 1.1 have the following modifications

```bash
#src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi add the following info:
pmu_thead: pmu_thead {
    interrupt-parent = <&cpu0_intc>;
    interrupts = <17>;
    compatible = "thead,c900_pmu";
};
#src/little/linux/arch/riscv/configs/k230_evb_defconfig  add the following configuration to the file
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
CONFIG_PERF_EVENTS=y
CONFIG_DEBUG_PERF_USE_VMALLOC=y
CONFIG_KUSER_HELPERS=y
CONFIG_DEBUG_INFO=y
CONFIG_FRAME_POINTER=y
```

```bash
[root@canaan ~ ]#perf list hw cache  > a ;cat a
  branch-instructions OR branches                    [Hardware event]
  branch-misses                                      [Hardware event]
  bus-cycles                                         [Hardware event]
  cache-misses                                       [Hardware event]
  cache-references                                   [Hardware event]
  cpu-cycles OR cycles                               [Hardware event]
  instructions                                       [Hardware event]
  ref-cycles                                         [Hardware event]
  stalled-cycles-backend OR idle-cycles-backend      [Hardware event]
  stalled-cycles-frontend OR idle-cycles-frontend    [Hardware event]
  L1-dcache-load-misses                              [Hardware cache event]
  L1-dcache-loads                                    [Hardware cache event]
  L1-dcache-store-misses                             [Hardware cache event]
  L1-dcache-stores                                   [Hardware cache event]
  L1-icache-load-misses                              [Hardware cache event]
  L1-icache-loads                                    [Hardware cache event]
  LLC-load-misses                                    [Hardware cache event]
  LLC-loads                                          [Hardware cache event]
  LLC-store-misses                                   [Hardware cache event]
  LLC-stores                                         [Hardware cache event]
  dTLB-load-misses                                   [Hardware cache event]
  dTLB-loads                                         [Hardware cache event]
  dTLB-store-misses                                  [Hardware cache event]
  dTLB-stores                                        [Hardware cache event]
  iTLB-load-misses                                   [Hardware cache event]
  iTLB-loads                                         [Hardware cache event]
[root@canaan ~ ]#

```

### 2.5 Big core run vector Linux

Question: How does Big Core run Linux with Vector?

Answer: make CONF=k230_evb_only_linux_defconfig ; The compiled image, the big core runs Linux with vector by default.

### 2.6 Big core serial port ID

Question: How to modify the serial port ID of the big core?

Answer: The configuration file below configs CONFIG_RTT_CONSOLE_ID stands for the big core serial port ID, modify it to the correct value.

### 2.7uboot command line

How to compile the version that can enter the uboot command line

Answer: The configuration file below configs CONFIG_QUICK_BOOT stands for fast, modify it to CONFIG_QUICK_BOOT=n to generate a command-line version that can be entered into uboot.

### 2.8 How to start slowly

Answer: Enter the uboot command line and execute the following command:

```bash
setenv quick_boot true;saveenv;reset;
```

### 2.9 Linux How to modify the last partition size

Answer: You can use the parted tool to dynamically modify the size of the last partition, refer to the following command:

```bash
umount /sharefs/
parted   -l /dev/mmcblk1
parted  -a minimal  /dev/mmcblk1  resizepart 4  31.3GB
mkfs.ext2 /dev/mmcblk1p4
mount /dev/mmcblk1p4 /sharefs
#please refer to below log:
[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   487MB   268MB   fat16        fat32appfs


[root@canaan ~ ]#umount /sharefs/
[root@canaan ~ ]#parted  -a minimal  /dev/mmcblk1  resizepart 4  31.3GB
Information: You may need to update /etc/fstab.

[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   31.3GB  31.1GB  fat16        fat32appfs


[root@canaan ~ ]#mkfs.ext2 /dev/mmcblk1p4
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
1896832 inodes, 7586811 blocks
379340 blocks (5%) reserved for the super user
First data block=0
Maximum filesystem blocks=8388608
232 block groups
32768 blocks per group, 32768 fragments per group
8176 inodes per group
Superblock backups stored on blocks:
32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000
[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   31.3GB  31.1GB  ext2         fat32appfs


[root@canaan ~ ]#mount /dev/mmcblk1p4 /sharefs/
[  332.688642] EXT4-fs (mmcblk1p4): mounted filesystem without journal. Opts: (null)
[root@canaan ~ ]#df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                73.5M     60.9M     10.2M  86% /
devtmpfs                 41.7M         0     41.7M   0% /dev
tmpfs                    51.8M         0     51.8M   0% /dev/shm
tmpfs                    51.8M     56.0K     51.7M   0% /tmp
tmpfs                    51.8M     36.0K     51.7M   0% /run
/dev/mmcblk1p4           28.5G     20.0K     27.0G   0% /sharefs
[root@canaan ~ ]#

```

### 2.10 How to modify bootargs

Answer: Method 1: Modify bootargs using env file. For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi；
```

Method 2: Enter the uboot command line and modify bootargs with reference to the following command.

```bash
setenv bootargs  "root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi" ;saveenv;reset;
```

### 2.11 How to view bootargs

Answer: Method 1: Under linux, enter cat /proc/cmdline to view

```bash
[root@canaan ~ ]#cat /proc/cmdline
root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan ~ ]#

```

Method 2: Linux command line input dmesg | grep command view

```bash
[root@canaan ~ ]#dmesg | grep  command
[    0.000000] Kernel command line: root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan
```

### 2.12 The default serial port modification of little core

Answer: At present, the little core serial port in the SDK defaults to 0, if you need to modify it to other serial ports (such as serial port 2), please refer to the following to modify:

Modification 1: Refer to the following to modify the uboot device tree (e.g. arch/riscv/dts/k230_evb.dts):

```bash
aliases {
        uart2 = &serial2;
    };

    chosen {
        stdout-path = "uart2:115200n8";
    };

    serial2: serial@91402000 {
    compatible = "snps,dw-apb-uart";
    reg = <0x0 0x91402000 0x0 0x400>;
    clock-frequency = <50000000>;
    clock-names = "baudclk";
    reg-shift = <2>;
    reg-io-width = <4>;
    u-boot,dm-pre-reloc;
};
```

Modification 2: Refer to the following to modify the Linux device tree (e.g. arch/riscv/boot/dts/kendryte/k230_evb.dts)

```bash
aliases {
        serial2 = &uart2;
    };
chosen {
        stdout-path = "serial2";
    };

&uart2 {
    status = "okay";
};
```

Modification 3: Modify bootargs using env files (see 2.10).

 For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS2,115200 earlycon=sbi；
```

### 2.13 How to completely reprogram the SDK

Answer: After updating and modifying the SDK source code, or after modifying the SDK source code, it is recommended to enter the following command to completely reprogram the SDK.

```bash
make clean; make;
```

### 2.15 Whether cklink jtag can be used on canmmv?

Answer：uboot default disable cklink jtag,you can enable cklink jtag by modify follow code:

``` bash
    #src/little/uboot/arch/riscv/dts/k230_canmv.dts gpio5 and gipi6 modify
    (IO5 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 0<<PU | 0<<PD | 4<<DS | 0<<ST )
    (IO6 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 1<<PU | 0<<PD | 4<<DS | 0<<ST )
```

>need rebuild uboot code

Special note: The SDK does not support multi-process compilation, do not add multi-process compilation options like -j32.
