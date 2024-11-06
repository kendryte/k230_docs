# K230 SDK 常见问题解答（C）

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

## 目录

[TOC]

## 1 TF boot failed with exit code 13

问题： TF卡启动报boot failed with exit code 13错误

答：原因如下  1.启动介质里面文件错误。2.启动管脚设置错误。

TF卡启动管脚设置特别说明： 两个启动管脚电平为高(需要拨到丝印的1和2，也就是ON的反方向)时才会从TF卡启动。

## 2 bootrom启动错误码

问题：bootrom 启动错误码含义是什么？

bootrom引导失败时会打印类似下面错误  boot failed with exit code 19，最后的数字是错误原因，常见错误含义如下

| 值   | 含义                                                |
| ---- | --------------------------------------------------- |
| 13   | 启动介质里面文件错误                                |
| 19   | 启动介质初始化失败，比如没有插sd卡等                |
| 17   | otp要求必需是安全镜像，但是介质里面文件是非安全镜像 |

## 3 spi nor 和 spi nand flash识别

问题： 怎么知道evb板上连接的是spi nor还是spi nand flash？

答：方法1：子板丝印不一样，丝印会有nor或nand标识。

​       方法2：linux启动log会有打印，比如连接spi nor时会有类似下面打印

```bash
[root@canaan ~ ]#dmesg | grep spi
[    1.299989] spi spi0.0: setup mode 0, 8 bits/w, 100000000 Hz max --> 0
[    1.306704] spi-nor spi0.0: gd25lx256e (32768 Kbytes)
[    1.311786] 2 fixed-partitions partitions found on MTD device spi0.0
[    1.318147] Creating 2 MTD partitions on "spi0.0":
```

## 4 perf 使用

问题：perf如何编译，支持那些硬件事件？

答：perf的时候可以使用raw事件，比如perf stat -e r12 ,perf工具编译命令如下:

```bash
cd src/little/linux/tools
make CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv perf V=1 WERROR=0
#目标文件是  perf/perf ，把这个文件复制到板子上就可以了。
```

特别说明：1.1以前版本进行如下修改

```bash
#src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi 添加如下内容
pmu_thead: pmu_thead {
    interrupt-parent = <&cpu0_intc>;
    interrupts = <17>;
    compatible = "thead,c900_pmu";
};
#src/little/linux/arch/riscv/configs/k230_evb_defconfig  文件增加如下配置
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

## 5大核运行vector linux

问题：大核如何运行带vector的linux？

答：请使用如下命令编译

```bash
make CONF=k230_canmv_only_linux_defconfig
#k230_canmv_only_linux_defconfig 对应的是带vector大核linux镜像
```

## 6 大核串口id

问题：怎么修改大核的串口id？

答：configs下面配置文件 CONFIG_RTT_CONSOLE_ID代表大核串口id，修改为正确的值就可以了。

## 7 uboot命令行

怎么编译可以进入uboot命令行的版本

答：  configs下面配置文件 CONFIG_QUICK_BOOT代表快起，修改为CONFIG_QUICK_BOOT=n 就可以生成可进去uboot命令行版本。

## 8 慢启怎么变快启动

答：进入uboot命令行执行如下命令：

```bash
setenv quick_boot true;saveenv;reset;
```

## 9 linux如何修改最后一个分区大小

答：使用parted工具可以动态修改最后一个分区大小，参考命令如下：

```bash
umount /sharefs/
parted   -l /dev/mmcblk1
parted  -a minimal  /dev/mmcblk1  resizepart 4  31.3GB
mkfs.ext2 /dev/mmcblk1p4
mount /dev/mmcblk1p4 /sharefs
#参考操作log如下
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

## 10如何修改bootargs

答：方法1：修改使用env文件里面的bootargs 。比如可以在board/common/env/default.env文件里面添加如下内容：

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi；
```

方法2：进入uboot命令行，参考下面命令修改bootargs。

```bash
setenv bootargs  "root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi" ;saveenv;reset;
```

## 11如何查看bootargs

答：方法1：linux下 输入cat /proc/cmdline  查看

```bash
[root@canaan ~ ]#cat /proc/cmdline
root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan ~ ]#

```

方法2：linux命令行输入 dmesg | grep  command查看

```bash
[root@canaan ~ ]#dmesg | grep  command
[    0.000000] Kernel command line: root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan
```

## 12小核默认串口修改

答：目前sdk里面小核串口默认0，如果需要修改成其他串口(比如串口2)，请参考下面进行修改：

修改1：参考下面修改uboot设备树(比如arch/riscv/dts/k230_evb.dts)：

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

修改2：参考下面修改linux设备树(比如arch/riscv/boot/dts/kendryte/k230_evb.dts)

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

修改3：  修改使用env文件里面的bootargs (参考2.10)。

 比如可以在board/common/env/default.env文件里面添加如下内容：

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS2,115200 earlycon=sbi；
```

## 13如何彻底重编sdk

答：更新修改SDK源代码之后，或者修改SDK源代码之后，建议输入如下命令彻底重编下sdk。

```bash
make clean; make;
```

## 14 支持的sensor list在哪里

答：请参考 [K230_Camera_Sensor适配指南](../01_software/board/mpp/K230_Camera_Sensor适配指南.md) 第4.1章节“支持的sensor类型”，目前支持

ov9732

ov9286

imx335

sc035

ov5647

sc201

gc2053

gc2093

os08a20

sc132gs

## 15canmmv板子是否可以使用平头哥的cklink进行jtag调试

答：默认不可以(uboot会关闭jtag功能)，需要进行如下修改才可以使用平头哥cklink进行jtag调试。

``` bash
    #src/little/uboot/arch/riscv/dts/k230_canmv.dts 文件gpio5和gipi6修改为如下内容
    (IO5 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 0<<PU | 0<<PD | 4<<DS | 0<<ST )
    (IO6 ) ( 1<<SEL | 0<<SL | BANK_VOLTAGE_IO2_IO13 <<MSC | 1<<IE | 0<<OE | 1<<PU | 0<<PD | 4<<DS | 0<<ST )
```

>修改完后需要重新编译uboot代码

## 16 如何快速编译buildroot下面的某一个软件包

答：参考如下命令快速重编buildroot下面的某一个软件包

``` bash
    #重编lvgl软件包命令参考,
    cd output/k230_canmv_defconfig/little/buildroot-ext/; #以k230_canmv_defconfig 为例
    make  lvgl-dirclean;
    make  lvgl && make;
    cd -  #切换到sdk主目录；
    make build-image #重新生成下镜像
```

更多信息请百度搜索buildroot how to rebuild packages。

## 17 canmv如何仅运行rtt系统，并且挂载sd卡？

答：请使用如下命令编译

```bash
make CONF=k230_canmv_only_rtt_defconfig
#k230_canmv_only_rtt_defconfig对应镜像仅运行rtt系统，并且rtt挂载sd。
```

## 18 linux下如何快速验证下串口收发是否正常？

答：参考如下命令，

```bash
#以串口2为例,请根据实际情况修改命令
stty -a  -F  /dev/ttyS2  #查看串口配置；
stty  -F  /dev/ttyS2 115200   #设置下波特率，默认9600
echo 00000000000000000000000000000011111111111111 > /dev/ttyS2  #发送字符串，电脑可以收到正确数据
cat  /dev/ttyS2   #接受串口数据
```

## 19 如何快速修改linux配置？

答：
1).Makefile里面linux-savedefconfig目标修改为如下内容(382行附近)：

```makefile
linux-savedefconfig:
	cd $(LINUX_SRC_PATH); \
	make O=$(LINUX_BUILD_DIR) CROSS_COMPILE=$(LINUX_EXEC_PATH)/$(LINUX_CC_PREFIX) ARCH=riscv savedefconfig; \
	cp $(LINUX_BUILD_DIR)/defconfig  arch/riscv/configs/$(LINUX_KERNEL_DEFCONFIG);\
	cd -
```

2).修改保存linux配置

```bash
make linux-menuconfig #修改linux配置
make linux-savedefconfig #保存linux配置
```

## 20大核如何切换自启动程序

答：
如果自启动程序在/bin目录下，修改方法如下：

```c
//src/big/rt-smart/init.sh 文件里面修改为你需要自启动的程序，比如修改为
/bin/fastboot_app.elf /bin/test.kmodel
```

如果自启动程在共享文件系统里面，需要修改2个地方，参考修改方法如下：

修改1：修改src/big/rt-smart/init.sh文件

```c
//src/big/rt-smart/init.sh 文件里面修改为类似如下内容
cd /sdcard/app/onboard
./sample_vo.elf
/sharefs/onboard/xxxx.sh
```

修改2 添加等待共享文件系统动作（适应于sdk 1.5及以后版本）

```c
//src/big/rt-smart/kernel/bsp/maix3/applications/main.c 文件 34行附近 修改为如下：

    struct stat stat_buf;
    while(stat("/sharefs/onboard",&stat_buf));// 请根据实际情况修改为正确的文件
    msh_exec("/bin/init.sh", 13); // 需要自启动的脚本,请根据实际情况修改为正确的文件
```

修改2 添加等待共享文件系统动作（适应于sdk 1.4及以前版本）

```c
//src/big/rt-smart/kernel/rt-thread/components/finsh/shell.c 文件 456行附近 修改为如下：
        if(shell_thread_first_run) {
            struct stat stat_buf;
            // shell_thread_first_run = 0;
            // msh_exec("/bin/init.sh", 13);
            if(0 == stat("/sharefs/onboard",&stat_buf)){ // 请根据实际情况修改为正确的文件
                shell_thread_first_run = 0;
                msh_exec("/bin/init.sh", 13); // 需要自启动的脚本,请根据实际情况修改为正确的文件
            }
            continue;
        }
```

## 21是否可以使用libxml2？

答：可以，参考下面方法在buildroot里面使能BR2_PACKAGE_LIBXML2就可以使用了。

使能libxml2方法1：备注sdk已经编译过

```bash
#使用libxml2方法(以k230_canmv_defconfig为例),在sdk主目录执行下面命令
make -C output/k230_canmv_defconfig/little/buildroot-ext/ menuconfig
#Target packages -->Libraries--->JSON/XML--> libxml2
#使能libxml2 库，并保存配置；
make -C output/k230_canmv_defconfig/little/buildroot-ext/ savedefconfig  #保存配置
make -C output/k230_canmv_defconfig/little/buildroot-ext/  #编译buildroot
make build-image
```

使能libxml2方法2：sdk没有编译过

```bash
#使用libxml2方法(以k230_canmv_defconfig为例) 在sdk主目录执行下面命令
echo "BR2_PACKAGE_LIBXML2=y" >> src/little/buildroot-ext/configs/k230_evb_defconfig
make CONF=k230_canmv_defconfig
```

libxml2使用例子

```c
//把如下代码 保存成io.c,编译方法见后面
#include <libxml/parser.h>

#if defined(LIBXML_TREE_ENABLED) && defined(LIBXML_OUTPUT_ENABLED)
int main(void)
{

    xmlNodePtr n;
    xmlDocPtr doc;
    xmlChar *xmlbuff;
    int buffersize;

    /*
     * Create the document.
     */
    doc = xmlNewDoc(BAD_CAST "1.0");
    n = xmlNewDocNode(doc, NULL, BAD_CAST "root", NULL);
    xmlNodeSetContent(n, BAD_CAST "content");
    xmlDocSetRootElement(doc, n);

    /*
     * Dump the document to a buffer and print it
     * for demonstration purposes.
     */
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

//编译方法
/* 假设sdk主目录是SDK=/home/wangjianxin/k230_sdk
SDK=/home/wangjianxin/k230_sdk
BD=${SDK}/output/k230_canmv_defconfig/little/buildroot-ext
gcc=${SDK}/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc

all:
    ${gcc} io.c --sysroot=${BD}/host/riscv64-buildroot-linux-gnu/sysroot   -I=${sysroot}/usr/include/libxml2 -lxml2
*/
#endif
```

特别说明：sdk不支持多进程编译，不要增加类似-j32多进程编译选项。

## 22 支持的屏有哪些？

答：移植新的屏请参考 [K230_LCD适配指南](../01_software/board/mpp/K230_LCD适配指南.md)。
目前我们支持的屏有

| 品牌     | 型号           | 屏驱型号  |  分辨率     |  帧率       | 备注 |
| -        | ------------- | --        |   ----      | ---        | --   |
| 今朝辉   | FPC55MH907C   |  HX8399   |  1080x1920  |  30        |      |
| 大显伟业 | D350T1013V1  |  ST7701    |   480x800   |  60        |      |
| 东大显控 | TC045IVFS-V40 | ST7701    |   480x854   |  30        |      |
| 龙迅     | LT9611       |            |  1920x1080 <br> 1280x720 <br> 640x480  | 30/50/60 <br> 30/50/60 <br> 60  | HDMI |

现有驱动移植，要注意驱动中使用的reset、背光脚管和i2c，这些都定义在k230_sdk/src/big/mpp/include/comm/k_board_config_comm.h文件里面，不同的板子这些定义可能不同。是通过板子的宏定义来进行区分的。例如

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

Canmv-K230-V1.0和V2.0板子的reset管脚不一样，移植时请修改相应的管脚编号。
