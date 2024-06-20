# K230 SDK Zero CanMV Board Demo使用指南

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

## 前言

### 概述

本文档主要介绍K230 SDK中提供适配Canmv-K230D-Zero开发板上的demo程序。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明                                                        |
|------|-------------------------------------------------------------|
| UVC  | USB video class（USB摄像头）                                |
| VVI  | virtual video input，虚拟视频输入，主要用于 pipeline 的调试 |

### 修订记录

| 文档版本号 | 修改说明  | 修改者 | 日期  |
|---|---|---|---|
| V1.0       | 初版 | 系统软件部 | 2023-10-11 |

## 1. 概述

此文档介绍K230 SDK提供的demo功能，使用方法等。

## 2. Demo介绍

### 2.1 Vicap_demo

#### 2.1.1 vicap_demo简介

vicap demo通过调用mpi接口实现摄像头数据采集预览功能。

#### 2.1.2 Feature说明

CanMV开发板默认使用OV5647摄像头模组，支持单个摄像头最多输出三路数据流。

#### 2.1.3 依赖资源

摄像头模组

#### 2.1.4 使用说明

##### 2.1.4.1 编译

软件编译环境参考SDK中的`README.md`。

1. 在k230_sdk目录下执行`make mpp-clean && make rt-smart && make build-image`，将修改编译进sd卡镜像中，会在`k230_sdk/output/k230_evb_defconfig/images/`目录下生成镜像文件`sysimage-sdcard.img`。

##### 2.1.4.2 执行

1. 在大核端，通过`cd /sdcard/app` 命令进入`/sdcard/app`
1. 在该目录下执行`./sample_vicap`命令获取命令帮助信息

当输入：`sample_vicap`命令后打印如下提示信息：

```shell
usage: ./sample_vicap -mode 0 -dev 0 -sensor 23 -chn 0 -chn 1 -ow 640 -oh 480 -preview 1 -rotation 1
Options:
 -mode:         vicap work mode[0: online mode, 1: offline mode. only offline mode support multiple sensor input]     default 0
 -dev:          vicap device id[0,1,2]        default 0
 -dw:           enable dewarp[0,1]    default 0
 -sensor:       sensor type[0: ov9732@1280x720, 1: ov9286_ir@1280x720], 2: ov9286_speckle@1280x720]
 -ae:           ae status[0: disable AE, 1: enable AE]        default enable
 -awb:          awb status[0: disable AWB, 1: enable AWb]     default enable
 -chn:          vicap output channel id[0,1,2]        default 0
 -ow:           the output image width, default same with input width
 -oh:           the output image height, default same with input height
 -ox:           the output image start position of x
 -oy:           the output image start position of y
 -crop:         crop enable[0: disable, 1: enable]
 -ofmt:         the output pixel format[0: yuv, 1: rgb888, 2: rgb888p, 3: raw], only channel 0 support raw data, default yuv
 -preview:      the output preview enable[0: disable, 1: enable], only support 2 output channel preview
 -rotation:     display rotaion[0: degree 0, 1: degree 90, 2: degree 270, 3: degree 180, 4: unsupport rotaion]
 -help:         print this help
```

参数说明如下：

| **参数名称** | **可选参数值** | **参数说明** |
|---|---|---|
| -dev         | 0：vicap设备0 1：vicap设备1 2：vicap设备2.                             | 指定当前使用的vicap设备，系统最多支持三个vicap设备。通过指定设备号实现sensor与不同vicap设备之间的绑定关系。 例如： -dev 1 -sensor 0即表示将ov9732 1280x720 RGB图像输出绑定到vicap设备1.                   |
| -mode | 0：在线模式；1：离线模式 | 指定vicap设备工作模式，当前之前在线模式和离线模式。对于多个sensor输入，必须指定为离线模式。 |
| -conn | 0: 屏 hx8399； 1: HDMI 3: st7701 480x800  |   指定显示方式，可以选择屏或者HDMI 默认为0 |
| -sensor      | 19：OV5647（Canmv-K230D-Zero板）  | 指定当前使用的sensor类型                                                         |
| -chn         | 0：vicap设备输出通道0 1：vicap设备输出通道1 2：vicap设备输出通道2.     | 指定当前使用的vicap设备的输出通道，一个vicap设备最多支持三路输出，仅通道0支持RAW图像格式输出  |
| -ow          |                                                                         | 指定输出图像宽度，默认为输入图像宽度。宽度需要16字节对齐。 如果默认宽度超过显示屏输出最大宽度，则使用显示输出宽度作为图像最终输出宽度 如果输出宽度小于输入图像宽度，且未指定ox或者oy参数，则默认为缩放输出 |
| -oh          |                                                                         | 指定输出图像高度，默认为输入图像高度。 如果默认高度超过显示屏输出最大高度，则使用显示输出高度作为图像最终输出高度 如果输出高度小于输入图像高度，且未指定ox或者oy参数，则默认为缩放输出  |
| -ox          |                                                                         | 指定图像输出水平起始位置，该参数大于0将执行输出裁剪操作  |
| -oy          |                                                                         | 指定图像输出垂直起始位置，该参数大于0将执行输出裁剪操作 |
| -crop        | 0：禁用裁剪功能 1：使能裁剪功能                                         | 当输出图像尺寸小于输入图像尺寸时，默认未缩放输出，如果指定了该标志，则为裁剪输出  |
| -ofmt        | 0：yuv格式输出 1：rgb格式输出 2：raw格式输出                            | 指定输出图像格式，默认为yuv输出。  |
| -preview     | 0：禁用预览显示 1：使能预览显示                                         | 指定输出图像预览显示功能。默认为使能。当前最多支持2路输出图像同时预览。 |
| -rotation    | 0：旋转0度 1：旋转90度 2：旋转180度 3：旋转270度 4：不支持旋转          | 指定预览显示窗口旋转角度。默认仅第一路输出图像窗口支持旋转功能。 |

示例：

`./sample_vicap.elf  -conn 3 -dev 0 -sensor 19 -chn 0  -ow 800 -oh 480 -rotation 1`

说明：将ov5647@1920x1080 绑定到vicap设备0,并使能vicap设备输出通道0，其中通道0输出800x480，通过屏显示。

### 2.2 DMA_demo

#### 2.2.1 DMA_demo简介

##### 2.2.1.1 非绑定模式

dma 通道 0-3 是 gdma，4-7 是 sdma。

- 通道 0 连续输入分辨率为 1920x1080 的图像，8bit，YUV400，单通道模式，旋转 90 度后输出，和 golden 数据比对
- 通道 1 连续输入分辨率为 1280x720 的图像，8bit，YUV420，双通道模式，旋转180 度后输出，和 golden 数据比对
- 通道 2 连续输入分辨率为 1280x720 的图像，10bit，YUV420，三通道模式，x-mirror，y-mirror 后输出，和 golden 数据比对
- 通道 4 为 1d 模式循环传输一段数据，传输完成后和 golden 数据比对
- 通道 5 为 2d 模式循环传输一段数据，传输完成后和 golden 数据比对

##### 2.2.1.2 绑定模式

使用 vvi 作为 dma 模拟输入，vvi 设备 0 的通道 0 绑定 dma 的通道 0，vvi 设备 0 的通道 1 绑定 dma 的通道 1。vvi 每隔一秒，向通道 0 输入 640x320，YUV400，8bit，旋转 90° 的图像，向通道 1 输入 640x320，YUV400，8bit，旋转 180° 的图像。

#### 2.2.2 Feature说明

包括 dma 设备属性配置，通道属性配置，图形输入、输出、释放，pipeline 绑定等功能。

#### 2.2.3 依赖资源

无

#### 2.2.4 使用说明

##### 2.2.4.1 编译

软件编译参考 release sdk 软件包中的 README.md。

##### 2.2.4.2 执行

1. 非绑定模式 demo 运行

`/sdcard/app/sample_dma.elf`

会有测试信息在屏幕上显示出来，输入 q 结束运行。

1. 绑定模式 demo 运行

`/sdcard/app/sample_dma_bind.elf`

会有测试信息在屏幕上显示出来，输入 q 结束运行。

### 2.3 USB_demo

#### 2.3.1 USB_demo简介

USB demo目前调试了4个功能，

作为device，模拟U盘，模拟鼠标键盘。

作为host，连接U盘，连接鼠标键盘。

#### 2.3.2 Feature说明

USB demo的功能是linux系统原始集成的功能。

#### 2.3.3 依赖资源

typeC线，typeC转typeA。

#### 2.3.4 使用说明

##### 2.3.4.1 作为device模拟U盘

```shell
#规划一块内存空间作为模拟U盘的磁盘空间。
[root@canaan / ]#gadget-storage-mem.sh
2+0 records in
2+0 records out
mkfs.fat 4.1 (2017-01-24)
[ 1218.882053] Mass Storage Function, version: 2009/09/11
[ 1218.887308] LUN: removable file: (no medium)
[ 1218.895464] dwc2 91500000.usb-otg: bound driver configfs-gadget
[root@canaan / ]#[ 1219.019554] dwc2 91500000.usb-otg: new device is high-speed
[ 1219.056629] dwc2 91500000.usb-otg: new address 5

##使用SD/eMMC的FAT分区当作模拟U盘的磁盘空间。
[root@canaan ~ ]#gadget-storage.sh
[  359.995510] Mass Storage Function, version: 2009/09/11
[  360.000762] LUN: removable file: (no medium)
[  360.013138] dwc2 91500000.usb-otg: bound driver configfs-gadget
[root@canaan ~ ]#[  360.136809] dwc2 91500000.usb-otg: new device is high-speed
[  360.173543] dwc2 91500000.usb-otg: new address 43
```

连接开发板的USB口，typeC连接PC，PC上显示U盘连接。

##### 2.3.4.2 作为HOST连接U盘

K230开发板USB口通过typeC转typeA连接U盘。

##### 2.3.4.3 作为device模拟鼠标键盘

K230开发板USB口通过typeC连接另外一台电脑设备来进行测试

```shell
[root@canaan / ]#gadget-hid.sh

[root@canaan / ]#hid_gadget_test /dev/hidg0 mouse
#根据提示输入相应的操作，比如-123 -123，可以看到PC上的鼠标指针移动。

[root@canaan / ]#hid_gadget_test /dev/hidg1 keyboard
#根据提示输入相应的操作，可以看到PC上的类似键盘输入。比如a b c --return
```

##### 2.3.4.4 作为HOST连接鼠标键盘

K230开发板USB通过typeC转typeA连接鼠标或键盘。

```shell
#通过以下命令确定input设备对应的event。K230开发板如果没有连接屏幕，连接鼠标键盘对应的event会改变。
[root@canaan ~ ]#cat /proc/bus/input/devices
...
I: Bus=0003 Vendor=046d Product=c52f Version=0111
N: Name="Logitech USB Receiver"
P: Phys=usb-91500000.usb-otg-1/input0
S: Sysfs=/devices/platform/soc/91500000.usb-otg/usb1/1-1/1-1:1.0/0003:046D:C52F.0001/input/input2
U: Uniq=
H: Handlers=event2
B: PROP=0
B: EV=17
B: KEY=ffff0000 0 0 0 0
B: REL=1943
B: MSC=10
```

```shell
[root@canaan / ]$ test_mouse /dev/input/event2
#点击或移动鼠标，串口会有对应的显示。

[root@canaan / ]$ test_keyboard /dev/input/event2
#按下键盘不同的按键，串口会有对应的显示。
```

### 2.4 FaceAeDemo

#### 2.4.1 Demo介绍

该demo在大核使用，是VICAP、KPU、VO（视频输出）、AERoi联调的demo，可通过人脸检测的接口适当调节人脸曝光亮度。

#### 2.4.2 编译

1. 首先参考release sdk软件包中的README.md，使用docker编译镜像。
1. 编译完成后，默认将该sample（sample_face_ae.elf）存放在该路径下`k230_sdk/src/big/mpp/userapps/sample/elf`
1. 由于KPU联动需要使用检测模型test.kmodel，编译后存放路径`k230_sdk/src/big/mpp/userapps/sample/elf`

#### 2.4.3 执行

```shell
cd /sdcard/app
./sample_face_ae.elf test.kmodel 1 # arg1: 模型名称， arg2： 开启face ae
等待初始化完成提示任意字母+enter
键入a，键入回车，运行face ae demo
执行成功后，会打印每一帧图像的物理地址
```

### 2.5 FFT Demo

#### 2.5.1 Demo 简介

本 demo 用于验证fft api使用，测试fft功能，代码见src/big/mpp/userapps/sample/sample_fft/

#### 2.5.2 Feature说明

先进行fft计算，在进行ifft计算

#### 2.5.3 依赖资源

无

#### 2.5.4 使用说明

##### 2.5.4.1 编译

> 请参考release sdk软件包中的README.md。

##### 2.5.4.2 执行

1. 系统都起来后，在大核命令行执行下面命令：

   ```bash
   cd /sdcard/app;./sample_fft.elf
   ```

   大核串口输出内容如下：

   ```text
   msh /sdcard/app>./sample_fft.elf 1 0
   -----fft ifft point 0064  -------
       max diff 0003 0001
       i=0045 real  hf 0000  hif fc24 org fc21 dif 0003
       i=0003 imag  hf ffff  hif 0001 org 0000 dif 0001
   -----fft ifft point 0064 use 133 us result: ok


   -----fft ifft point 0128  -------
       max diff 0003 0002
       i=0015 real  hf 0001  hif fca1 org fc9e dif 0003
       i=0031 imag  hf 0001  hif fffe org 0000 dif 0002
   -----fft ifft point 0128 use 121 us result: ok


   -----fft ifft point 0256  -------
       max diff 0003 0001
       i=0030 real  hf 0000  hif fca1 org fc9e dif 0003
       i=0007 imag  hf ffff  hif 0001 org 0000 dif 0001
   -----fft ifft point 0256 use 148 us result: ok


   -----fft ifft point 0512  -------
       max diff 0003 0003
       i=0060 real  hf 0000  hif fca1 org fc9e dif 0003
       i=0314 imag  hf 0001  hif fffd org 0000 dif 0003
   -----fft ifft point 0512 use 206 us result: ok


   -----fft ifft point 1024  -------
       max diff 0005 0002
       i=0511 real  hf 0000  hif fc00 org fc05 dif 0005
       i=0150 imag  hf 0000  hif fffe org 0000 dif 0002
   -----fft ifft point 1024 use 328 us result: ok


   -----fft ifft point 2048  -------
       max diff 0005 0003
       i=1022 real  hf 0000  hif fc00 org fc05 dif 0005
       i=1021 imag  hf 0000  hif 0003 org 0000 dif 0003
   -----fft ifft point 2048 use 574 us result: ok


   -----fft ifft point 4096  -------
       max diff 0005 0002
       i=4094 real  hf 027b  hif 041f org 0424 dif 0005
       i=0122 imag  hf 0000  hif 0002 org 0000 dif 0002
   -----fft ifft point 4096 use 1099 us result: ok

   ```
