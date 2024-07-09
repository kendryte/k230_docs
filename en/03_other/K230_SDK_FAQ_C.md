# K230 SDK Frequently Asked Questions (C)

![cover](../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise stipulated in the contract, the Company does not make any express or implied statements or guarantees regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No unit or individual may excerpt, copy, or disseminate part or all of the content of this document in any form without written permission from the Company.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## 1 TF Boot Failed with Exit Code 13

Issue: TF card boot reports boot failed with exit code 13 error

Answer: The reasons are as follows: 1. File error in the boot medium. 2. Incorrect boot pin settings.

Special note on TF card boot pin settings: The TF card will only boot when the two boot pins are high (need to be switched to the silk screen positions 1 and 2, which is the opposite direction of ON).

## 2 Bootrom Startup Error Codes

Issue: What is the meaning of the bootrom startup error codes?

When bootrom boot fails, it will print an error similar to boot failed with exit code 19. The last digit is the error reason. The common error meanings are as follows:

| Value | Meaning                                                    |
| ----- | ---------------------------------------------------------- |
| 13    | File error in the boot medium                              |
| 19    | Boot medium initialization failed, such as no SD card inserted |
| 17    | OTP requires a secure image, but the file in the medium is a non-secure image |

## 3 SPI NOR and SPI NAND Flash Identification

Issue: How to know whether the EVB board is connected to SPI NOR or SPI NAND flash?

Answer: Method 1: The sub-board silkscreen is different, and the silkscreen will have NOR or NAND markings.

​       Method 2: The Linux startup log will print, for example, when connected to SPI NOR, it will print something similar to the following:

```bash
[root@canaan ~ ]#dmesg | grep spi
[    1.299989] spi spi0.0: setup mode 0, 8 bits/w, 100000000 Hz max --> 0
[    1.306704] spi-nor spi0.0: gd25lx256e (32768 Kbytes)
[    1.311786] 2 fixed-partitions partitions found on MTD device spi0.0
[    1.318147] Creating 2 MTD partitions on "spi0.0":
```

## 4 Perf Usage

Issue: How to compile perf and what hardware events does it support?

Answer: You can use raw events for perf, such as perf stat -e r12. The compilation command for the perf tool is as follows:

```bash
cd src/little/linux/tools
make CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv perf V=1 WERROR=0
# The target file is perf/perf, just copy this file to the board.
```

Special note: For versions before 1.1, make the following modifications:

```bash
# Add the following content to src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi
pmu_thead: pmu_thead {
    interrupt-parent = <&cpu0_intc>;
    interrupts = <17>;
    compatible = "thead,c900_pmu";
};
# Add the following configurations to src/little/linux/arch/riscv/configs/k230_evb_defconfig
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

## 5 Running Vector Linux on the Big Core

Issue: How to run Linux with vector support on the big core?

Answer: Please use the following command to compile:

```bash
make CONF=k230_canmv_only_linux_defconfig
# k230_canmv_only_linux_defconfig corresponds to the Linux image with vector support for the big core
```

## 6 Big Core Serial Port ID

Issue: How to modify the serial port ID of the big core?

Answer: The configuration file CONFIG_RTT_CONSOLE_ID under configs represents the serial port ID of the big core. Modify it to the correct value.

## 7 Uboot Command Line

How to compile a version that can enter the Uboot command line?

Answer: The configuration file CONFIG_QUICK_BOOT under configs represents quick boot. Modify it to CONFIG_QUICK_BOOT=n to generate a version that can enter the Uboot command line.

## 8 How to Change Slow Boot to Fast Boot

Answer: Enter the Uboot command line and execute the following commands:

```bash
setenv quick_boot true;saveenv;reset;
```

## 9 How to Modify the Size of the Last Partition in Linux

Answer: You can dynamically modify the size of the last partition using the parted tool. Refer to the following commands:

```bash
umount /sharefs/
parted -l /dev/mmcblk1
parted -a minimal /dev/mmcblk1 resizepart 4 31.3GB
mkfs.ext2 /dev/mmcblk1p4
mount /dev/mmcblk1p4 /sharefs
# Refer to the following operation log
[root@canaan ~ ]#parted -l /dev/mmcblk1
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
[root@canaan ~ ]#parted -a minimal /dev/mmcblk1 resizepart 4 31.3GB
Information: You may need to update /etc/fstab.
[root@canaan ~ ]#parted -l /dev/mmcblk1
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
[root@canaan ~ ]#parted -l /dev/mmcblk1
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

## 10 How to Modify Bootargs

Answer: Method 1: Modify the bootargs in the env file. For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi;
```

Method 2: Enter the Uboot command line and modify the bootargs using the following commands:

```bash
setenv bootargs "root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi"; saveenv; reset;
```

## 11 How to View Bootargs

Answer: Method 1: In Linux, enter `cat /proc/cmdline` to view:

```bash
[root@canaan ~ ]#cat /proc/cmdline 
root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan ~ ]#
```

Method 2: In the Linux command line, enter `dmesg | grep command` to view:

```bash
[root@canaan ~ ]#dmesg | grep command
[    0.000000] Kernel command line: root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan ~ ]
```

## 12 How to Modify the Default Serial Port of the Small Core

Answer: Currently, the default serial port for the small core in the SDK is 0. If you need to change it to another serial port (e.g., serial port 2), please follow the steps below:

Modification 1: Modify the Uboot device tree (e.g., arch/riscv/dts/k230_evb.dts) as follows:

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

Modification 2: Modify the Linux device tree (e.g., arch/riscv/boot/dts/kendryte/k230_evb.dts) as follows:

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

Modification 3: Modify the bootargs in the env file (refer to section 2.10).

For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS2,115200 earlycon=sbi;
```

## 13 How to Completely Recompile the SDK

Answer: After updating or modifying the SDK source code, it is recommended to enter the following commands to completely recompile the SDK:

```bash
make clean; make;
```

## 14 Where is the List of Supported Sensors

Answer: Please refer to section 4.1 "Supported Sensor Types" in the [K230_Camera_Sensor Adaptation Guide](../01_software/board/mpp/K230_Camera_Sensor_Adaptation_Guide.md). Currently supported sensors include:

- ov9732
- ov9286
- imx335
- sc035
- ov5647
- sc201

## 15 Can the Canmmv Board Use Pingtouge's CKLink for JTAG Debugging

Answer: By default, it cannot (Uboot disables the JTAG function). You need to make the following modifications to use Pingtouge CKLink for JTAG debugging:

```bash
# Modify the gpio5 and gpio6 settings in src/little/uboot/arch/riscv/dts/k230_canmv.dts as follows:
(IO5 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 0<<PU | 0<<PD | 4<<DS | 0<<ST )
(IO6 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 1<<PU | 0<<PD | 4<<DS | 0<<ST )
```

> After modification, you need to recompile the Uboot code.

## 16 How to Quickly Compile a Specific Package Under Buildroot

Answer: Refer to the following commands to quickly recompile a specific package under Buildroot:

```bash
# Example command to recompile the lvgl package:
cd output/k230_canmv_defconfig/little/buildroot-ext/; # Using k230_canmv_defconfig as an example
make lvgl-dirclean;
make lvgl && make;
cd -  # Switch back to the SDK main directory;
make build-image # Regenerate the image
```

For more information, search "buildroot how to rebuild packages" on Baidu.

## 17 How to Run Only the RTT System and Mount the SD Card on Canmv

Answer: Please use the following command to compile:

```bash
make CONF=k230_canmv_only_rtt_defconfig
# k230_canmv_only_rtt_defconfig corresponds to an image that only runs the RTT system and mounts the SD card.
```

## 18 How to Quickly Verify Serial Port Transmission and Reception in Linux

Answer: Refer to the following commands:

```bash
# Using serial port 2 as an example, modify the commands according to your actual situation:
stty -a -F /dev/ttyS2  # View serial port configuration;
stty -F /dev/ttyS2 115200  # Set the baud rate, default is 9600
echo 00000000000000000000000000000011111111111111 > /dev/ttyS2  # Send a string, the computer should receive the correct data
cat /dev/ttyS2  # Receive serial port data
```

## 19 How to Quickly Modify Linux Configuration

Answer:
1). Modify the linux-savedefconfig target in the Makefile as follows (around line 382):

```makefile
linux-savedefconfig:
	cd $(LINUX_SRC_PATH); \
	make O=$(LINUX_BUILD_DIR) CROSS_COMPILE=$(LINUX_EXEC_PATH)/$(LINUX_CC_PREFIX) ARCH=riscv savedefconfig; \
	cp $(LINUX_BUILD_DIR)/defconfig  arch/riscv/configs/$(LINUX_KERNEL_DEFCONFIG);\
	cd -
```

2). Modify and save the Linux configuration:

```bash
make linux-menuconfig # Modify Linux configuration
make linux-savedefconfig # Save Linux configuration
```

## 20 How to Switch the Auto-Start Program on the Big Core

Answer:
If the auto-start program is in the /bin directory, modify it as follows:

```c
// Modify the src/big/rt-smart/init.sh file to the program you need to auto-start, for example:
 /bin/fastboot_app.elf /bin/test.kmodel
```

If the auto-start program is in the shared file system, you need to modify two places. Refer to the following modification methods:

Modification 1: Modify the src/big/rt-smart/init.sh file

```c
// Modify the src/big/rt-smart/init.sh file to something like the following:
cd /sdcard/app/onboard
./sample_vo.elf
/sharefs/onboard/xxxx.sh
```

Modification 2: Add a wait for the shared file system action (applicable to SDK version 1.5 and later)

```c  
// Modify around line 34 in the src/big/rt-smart/kernel/bsp/maix3/applications/main.c file as follows:
        
    struct stat stat_buf;
    while(stat("/sharefs/onboard",&stat_buf));// Please modify to the correct file according to the actual situation 
    msh_exec("/bin/init.sh", 13); // The script to auto-start, please modify to the correct file according to the actual situation
```

Modification 2: Add a wait for the shared file system action (applicable to SDK version 1.4 and earlier)

```c
// Modify around line 456 in the src/big/rt-smart/kernel/rt-thread/components/finsh/shell.c file as follows:
        if(shell_thread_first_run) {
            struct stat stat_buf;
            // shell_thread_first_run = 0;
            // msh_exec("/bin/init.sh", 13);
            if(0 == stat("/sharefs/onboard",&stat_buf)){ // Please modify to the correct file according to the actual situation
                shell_thread_first_run = 0;               
                msh_exec("/bin/init.sh", 13); // The script to auto-start, please modify to the correct file according to the actual situation
            }
            continue;
        }
```

## 21 Can libxml2 Be Used?

Answer: Yes, it can. Refer to the following method to enable BR2_PACKAGE_LIBXML2 in Buildroot.

Enabling libxml2 Method 1: If the SDK has already been compiled

```bash
# Method to use libxml2 (using k230_canmv_defconfig as an example), execute the following commands in the SDK main directory:
make -C output/k230_canmv_defconfig/little/buildroot-ext/ menuconfig
# Target packages --> Libraries --> JSON/XML --> libxml2 
# Enable the libxml2 library and save the configuration;
make -C output/k230_canmv_defconfig/little/buildroot-ext/ savedefconfig  # Save the configuration
make -C output/k230_canmv_defconfig/little/buildroot-ext/  # Compile Buildroot
make build-image
```

Enabling libxml2 Method 2: If the SDK has not been compiled

```bash
# Method to use libxml2 (using k230_canmv_defconfig as an example) execute the following commands in the SDK main directory:
echo "BR2_PACKAGE_LIBXML2=y" >> src/little/buildroot-ext/configs/k230_evb_defconfig
make CONF=k230_canmv_defconfig
```

libxml2 usage example:

```c
// Save the following code as io.c, see the compilation method below
#include <libxml/parser.h>

#if defined(LIBXML_TREE_ENABLED) && defined(LIBXML_OUTPUT_ENABLED)
int main(void)
{

    xmlNodePtr n;
    xmlDocPtr doc;
    xmlChar *xmlbuff;
    int buffersize;

    /*
     * Create the document. */
    doc = xmlNewDoc(BAD_CAST "1.0");
    n = xmlNewDocNode(doc, NULL, BAD_CAST "root", NULL);
    xmlNodeSetContent(n, BAD_CAST "content");
    xmlDocSetRootElement(doc, n);

    /*
     * Dump the document to a buffer and print it
     * for demonstration purposes. */
    xmlDocDumpFormatMemory(doc, &xmlbuff, &buffersize, 1);
    printf("%s", (char *) xmlbuff);

    /*
     * Free associated memory.
    */
    xmlFree(xmlbuff);
    xmlFreeDoc(doc);

    return (0);

}
#else
#include <stdio.h>

int main(void)
{
    fprintf(stderr,
            "library not configured with tree and output support\n");
    return (0);
}

// Compilation method 
/* Assuming the SDK main directory is SDK=/home/wangjianxin/k230_sdk
SDK=/home/wangjianxin/k230_sdk
BD=${SDK}/output/k230_canmv_defconfig/little/buildroot-ext
gcc=${SDK}/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc

all:
    ${gcc} io.c --sysroot=${BD}/host/riscv64-buildroot-linux-gnu/sysroot   -I=${sysroot}/usr/include/libxml2 -lxml2
*/
#endif
```

Special Note: The SDK does not support multi-process compilation, so do not add multi-process compilation options like -j32.

## 22 What Screens Are Supported?

Answer: For porting new screens, please refer to the [K230_LCD Adaptation Guide](../01_software/board/mpp/K230_LCD_Adaptation_Guide.md).
Currently, the supported screens are:

| Brand     | Model           | Driver Model  |  Resolution     |  Frame Rate | Remarks |
| --------- | --------------- | ------------- | --------------- | ----------- | ------- |
| JinZhaoHui | FPC55MH907C    |  HX8399       |  1080x1920      |  30         |         |
| DaXianWeiYe | D350T1013V1  |  ST7701       |   480x800       |  60         |         |
| DongDaXianKong | TC045IVFS-V40 | ST7701   |   480x854       |  30         |         |
| LongXun     | LT9611        |               |  1920x1080 <br> 1280x720 <br> 640x480  | 30/50/60 <br> 30/50/60 <br> 60  | HDMI |

When porting existing drivers, pay attention to the reset, backlight pins, and I2C used in the driver. These are defined in the k230_sdk/src/big/mpp/include/comm/k_board_config_comm.h file. These definitions may vary between different boards and are distinguished by board macros. For example:

```c
#elif defined(CONFIG_BOARD_K230_CANMV)
// display gpio
#define DISPLAY_LCD_RST_GPIO                            20
#define DISPLAY_LCD_BACKLIGHT_EN                        25
#elif defined(CONFIG_BOARD_K230_CANMV_V2)
// display gpio
#define DISPLAY_LCD_RST_GPIO                            22
#define DISPLAY_LCD_BACKLIGHT_EN                        25
```

The reset pins for the Canmv-K230-V1.0 and V2.0 boards are different. Please modify the corresponding pin numbers during porting.
