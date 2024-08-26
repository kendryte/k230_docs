# K230_Opencv UVC Usage Guide

![cover](../../../zh/images/canaan-cover.png)

Copyright © 2023 Canaan Creative

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Canaan Creative and its affiliates (hereinafter referred to as "the Company"). The products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not make any explicit or implicit statements or guarantees regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Canaan Creative and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Overview

This document explains how to drive a USB camera on the Linux side of the K230 development board and call UVC through OpenCV.

## UVC Usage Instructions on Linux

Using k230-canmv as an example

### Configuration Modifications

Modify the `K230_SDK/src/little/linux/arch/riscv/configs/k230_canmv_defconfig` configuration file to add the following configurations:

```shell
CONFIG_MEDIA_USB_SUPPORT=y
CONFIG_USB_VIDEO_CLASS=y
```

Modify the `K230_SDK/src/little/buildroot-ext/configs/k230_evb_defconfig` configuration file to add the following configurations:

```shell
BR2_PACKAGE_LIBV4L=y
BR2_PACKAGE_LIBV4L_UTILS=y
BR2_PACKAGE_OPENCV3=y
BR2_PACKAGE_OPENCV3_LIB_HIGHGUI=y
BR2_PACKAGE_OPENCV3_WITH_V4L=y
BR2_PACKAGE_OPENCV3_WITH_JPEG=y
BR2_PACKAGE_OPENCV3_WITH_PNG=y
```

After modification, execute `make` to generate the image and burn it.

### Board Testing

#### Connecting the Device

After the system starts, connect the USB camera. The system will detect the USB device insertion, and two device files, `/dev/video0` and `dev/video1`, will be generated in the `/dev` directory.

```sh
[root@canaan ~ ]# lsusb
Bus 001 Device 001: ID 1d6b:0002
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]# [   45.053193] usb usb1-port1: Cannot enable. Maybe the USB cable is bad? [   46.049135] usb 1-1: new full-speed USB device number 3 using dwc2
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

[root@canaan ~ ]# lsusb
Bus 001 Device 001: ID 1d6b:0002
Bus 001 Device 003: ID 0380:2006
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]# ls /dev/video*
/dev/video0  /dev/video1
```

#### Checking Device Status

Use the `v4l2-ctl -d /dev/video0 --all` command to view camera information.

```sh
[root@canaan ~ ]# v4l2-ctl -d /dev/video0 --all
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
        Flags            : default
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

#### Capturing Images with v4l

Use the `v4l2-ctl --device /dev/video0 --stream-mmap --stream-to=video0-output.jpg --stream-count=1` command to capture a jpg image.

```sh
[root@canaan ~ ]# v4l2-ctl --device /dev/video0 --stream-mmap --stream-to=video0-output.jpg --stream-count=1
<
[root@canaan ~ ]# ls -lh
total 222K   
-rw-r--r--    1 root     root      221.7K Jan  1 00:11 video0-output.jpg
```

#### Capturing Images with OpenCV

Copy the `video_cap` test application to the file system and execute it to generate a test.jpg file.

```sh
[root@canaan ~ ]# ./video_cap 
[root@canaan ~ ]# ls
nfs        test.jpg   video_cap
```

The `video_cap` application can be compiled using the command `/opt/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-g++ --sysroot=$HOME/k230/k230_sdk/output/k230_evb_defconfig/little/buildroot-ext/host/riscv64-buildroot-linux-gnu/sysroot video_cap.cpp -lopencv_videoio -lopencv_core -lopencv_imgcodecs -o video_cap`. The source code for video_cap.cpp is as follows:

```cpp
#include "opencv2/opencv.hpp"
using namespace cv;

int main()
{
    VideoCapture capture(0);
    Mat frame;
    capture >> frame;
    imwrite("test.jpg", frame);
    return 0;
}
```

### User Applications

1. Capture images using the v4l interface. For details, please refer to the `v4l User Programming API` or `v4l-utils source code`.
1. Capture images using the OpenCV interface. For details, please refer to `OpenCV Programming`.

### Reference Links

[v4l-utils source code](https://linuxtv.org/downloads/v4l-utils/)
