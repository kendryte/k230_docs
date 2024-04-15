# K230_Opencv调用UVC指南

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

本文将讲解如何在k230开发板Linux侧驱动USB摄像头，并通过opencv调用uvc。

## linux下UVC使用说明

以k230-canmv为例

### 配置修改

修改`K230_SDK/src/little/linux/arch/riscv/configs/k230_canmv_defconfig`配置文件，增加以下配置

```shell
CONFIG_MEDIA_USB_SUPPORT=y
CONFIG_USB_VIDEO_CLASS=y
```

修改`K230_SDK/src/little/buildroot-ext/configs/k230_evb_defconfig`配置文件，增加以下配置

```shell
BR2_PACKAGE_LIBV4L=y
BR2_PACKAGE_LIBV4L_UTILS=y
BR2_PACKAGE_OPENCV3=y
BR2_PACKAGE_OPENCV3_LIB_HIGHGUI=y
BR2_PACKAGE_OPENCV3_WITH_V4L=y
BR2_PACKAGE_OPENCV3_WITH_JPEG=y
BR2_PACKAGE_OPENCV3_WITH_PNG=y
```

修改完成后执行`make`，生成镜像并烧录

### 上板测试

#### 连接设备

系统启动后，连接USB摄像头，系统会检测到USB设备插入，同时`/dev`目录下会生成`/dev/video0` `dev/video1`两个设备文件

```sh
[root@canaan ~ ]#lsusb
Bus 001 Device 001: ID 1d6b:0002
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]#[   45.053193] usb usb1-port1: Cannot enable. Maybe the USB cable is bad?
[   46.049135] usb 1-1: new full-speed USB device number 3 using dwc2
[   46.261329] usb 1-1: not running at top speed; connect to a high speed hub
[   46.269490] usb 1-1: config 1 interface 1 altsetting 1 endpoint 0x84 has invalid maxpacket 1024, setting to 1023
[   46.279757] usb 1-1: config 1 interface 4 altsetting 0 endpoint 0x3 has invalid maxpacket 512, setting to 64
[   46.290402] usb 1-1: New USB device found, idVendor=0380, idProduct=2006, bcdDevice= 0.20
[   46.298651] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[   46.305838] usb 1-1: Product: FHD Camera
[   46.309790] usb 1-1: Manufacturer: ANYKA
[   46.313728] usb 1-1: SerialNumber: 12345
[   46.320244] uvcvideo: Unknown video format 35363248-0000-0010-8000-00aa00389b71
[   46.327669] uvcvideo: Found UVC 1.00 device FHD Camera (0380:2006)
[   46.342750] usbhid 1-1:1.4: couldn't find an input interrupt endpoint

[root@canaan ~ ]#lsusb
Bus 001 Device 001: ID 1d6b:0002
Bus 001 Device 003: ID 0380:2006
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]#ls /dev/video*
/dev/video0  /dev/video1
```

#### 检查设备状态

使用`v4l2-ctl -d /dev/video0 --all`命令查看摄像头信息

```sh
[root@canaan ~ ]#v4l2-ctl -d /dev/video0 --all
Driver Info:
        Driver name      : uvcvideo
        Card type        : FHD Camera: FHD Camera
        Bus info         : usb-91500000.usb-otg-1
        Driver version   : 5.10.4
        Capabilities     : 0x84a00001
                Video Capture
                Metadata Capture
                Streaming
                Extended Pix Format
                Device Capabilities
        Device Caps      : 0x04200001
                Video Capture
                Streaming
                Extended Pix Format
Media Driver Info:
        Driver name      : uvcvideo
        Model            : FHD Camera: FHD Camera
        Serial           : 12345
        Bus info         : usb-91500000.usb-otg-1
        Media version    : 5.10.4
        Hardware revision: 0x00000020 (32)
        Driver version   : 5.10.4
Interface Info:
        ID               : 0x03000002
        Type             : V4L Video
Entity Info:
        ID               : 0x00000001 (1)
        Name             : FHD Camera: FHD Camera
        Function         : V4L2 I/O
        Flags         : default
        Pad 0x01000007   : 0: Sink
          Link 0x0200000d: from remote pad 0x100000a of entity 'Processing 2': Data, Enabled, Immutable
Priority: 2
Video input : 0 (Camera 1: ok)
Format Video Capture:
        Width/Height      : 1920/1080
        Pixel Format      : 'MJPG' (Motion-JPEG)
        Field             : None
        Bytes per Line    : 0
        Size Image        : 4147200
        Colorspace        : Default
        Transfer Function : Default (maps to Rec. 709)
        YCbCr/HSV Encoding: Default (maps to ITU-R 601)
        Quantization      : Default (maps to Full Range)
        Flags             : 
Crop Capability Video Capture:
        Bounds      : Left 0, Top 0, Width 1920, Height 1080
        Default     : Left 0, Top 0, Width 1920, Height 1080
        Pixel Aspect: 1/1
Selection Video Capture: crop_default, Left 0, Top 0, Width 1920, Height 1080, Flags: 
Selection Video Capture: crop_bounds, Left 0, Top 0, Width 1920, Height 1080, Flags: 
Streaming Parameters Video Capture:
        Capabilities     : timeperframe
        Frames per second: 30.000 (30/1)
        Read buffers     : 0
```

#### 使用v4l获取图像

使用`v4l2-ctl --device /dev/video0 --stream-mmap --stream-to=video0-output.jpg --stream-count=1`命令采集一张jpg图片

```sh
[root@canaan ~ ]#v4l2-ctl --device /dev/video0 --stream-mmap --stream-to=video0-
output.jpg --stream-count=1
<
[root@canaan ~ ]#ls -lh
total 222K   
-rw-r--r--    1 root     root      221.7K Jan  1 00:11 video0-output.jpg
```

#### 使用opencv获取图像

拷贝`video_cap`测试应用到文件系统中并执行，会生成一个test.jpg文件

```sh
[root@canaan ~ ]#./video_cap 
[root@canaan ~ ]#ls
nfs        test.jpg   video_cap
```

video_cap可通过命令`/opt/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-g++ --sysroot=$HOME/k230/k230_sdk/output/k230_evb_defconfig/little/buildroot-ext/host/riscv64-buildroot-linux-gnu/sysroot video_cap.cpp  -lopencv_videoio -lopencv_core -lopencv_imgcodecs -o video_cap`来编译生成，video_cap.cpp源码如下：

```cpp
#include "opencv2/opencv.hpp"
using namespace cv;

int main()
{
    VideoCapture capture(0);
    Mat frame;
    capture>>frame;
    imwrite("test.jpg", frame);
    return 0;
}
```

### 用户应用

1. 通过v4l接口去采集图像，具体请参考`v4l用户编程API`或`v4l-utils源码`
1. 通过opencv接口去采集图像，具体请参考`opencv编程`

### 参考连接

[v4l-utils源码](https://linuxtv.org/downloads/v4l-utils/)
