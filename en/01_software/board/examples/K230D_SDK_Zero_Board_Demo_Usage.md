# K230D SDK Zero Board Demo Usage Guide

![cover](../../../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company") and its affiliates. Some or all of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company makes no express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy part or all of the contents of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Foreword

### Overview

This document mainly introduces the demo programs provided in the K230 SDK that are adapted to the Canmv-K230D-Zero development board.

### Intended Audience

This document (this guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
| UVC          | USB video class (USB camera) |
| VVI          | Virtual video input, mainly used for pipeline debugging |

### Revision History

| Document Version | Description | Author | Date |
|------------------|-------------|--------|------|
| V1.0             | Initial version | System Software Department | 2023-10-11 |

## 1. Overview

This document introduces the demo functions provided by the K230 SDK, usage methods, etc.

## 2. Demo Introduction

### 2.1 Vicap_demo

#### 2.1.1 Vicap_demo Introduction

The vicap demo implements camera data capture and preview functions by calling the mpi interface.

#### 2.1.2 Feature Description

The CanMV development board uses the OV5647 camera module by default, supporting up to three data streams from a single camera.

#### 2.1.3 Dependency Resources

Camera module

#### 2.1.4 Usage Instructions

##### 2.1.4.1 Compilation

Refer to the `README.md` in the SDK for the software compilation environment.

1. Execute `make mpp-clean && make rt-smart && make build-image` in the k230_sdk directory to compile the changes into the SD card image. The image file `sysimage-sdcard.img` will be generated in the `k230_sdk/output/k230_evb_defconfig/images/` directory.

##### 2.1.4.2 Execution

1. On the main core, navigate to `/sdcard/app` using the command `cd /sdcard/app`.
1. Execute the command `./sample_vicap` in this directory to get command help information.

When the command `sample_vicap` is entered, the following prompt information is printed:

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
 -rotation:     display rotaion[0: degree 0, 1: degree 90, 2: degree 270, 3: degree 180, 4: unsupport rotaion, 17: gdma-degree 90, 18: gdma-degree 180, 19: gdma-degree 270]
 -help:         print this help
```

Parameter descriptions are as follows:

| **Parameter Name** | **Optional Values** | **Description** |
|--------------------|---------------------|-----------------|
| -dev               | 0: vicap device 0, 1: vicap device 1, 2: vicap device 2. | Specifies the current vicap device. The system supports up to three vicap devices. By specifying the device number, the sensor can be bound to different vicap devices. For example: `-dev 1 -sensor 0` means binding the ov9732 1280x720 RGB image output to vicap device 1. |
| -mode              | 0: online mode; 1: offline mode | Specifies the vicap device work mode. Currently, there are online and offline modes. For multiple sensor inputs, it must be specified as offline mode. |
| -conn              | 0: screen hx8399; 1: HDMI; 3: st7701 480x800 | Specifies the display method, either screen or HDMI. The default is 0. |
| -sensor            | 19: OV5647 (Canmv-K230D-Zero board) | Specifies the current sensor type |
| -chn               | 0: vicap device output channel 0; 1: vicap device output channel 1; 2: vicap device output channel 2. | Specifies the current vicap device output channel. A vicap device supports up to three outputs, with only channel 0 supporting RAW image format output. |
| -ow                | | Specifies the output image width, defaulting to the input image width. The width needs to be aligned to 16 bytes. If the default width exceeds the maximum width of the display output, the display output width is used as the final output width. If the output width is less than the input image width and the `ox` or `oy` parameters are not specified, it defaults to scaling output. |
| -oh                | | Specifies the output image height, defaulting to the input image height. If the default height exceeds the maximum height of the display output, the display output height is used as the final output height. If the output height is less than the input image height and the `ox` or `oy` parameters are not specified, it defaults to scaling output. |
| -ox                | | Specifies the horizontal start position of the image output. If this parameter is greater than 0, a cropping operation is performed. |
| -oy                | | Specifies the vertical start position of the image output. If this parameter is greater than 0, a cropping operation is performed. |
| -crop              | 0: disable cropping; 1: enable cropping | When the output image size is smaller than the input image size, it defaults to scaling output. If this flag is specified, it outputs as cropped. |
| -ofmt              | 0: yuv format output; 1: rgb format output; 2: raw format output | Specifies the output image format, defaulting to yuv output. |
| -preview           | 0: disable preview; 1: enable preview | Specifies the output image preview display function. The default is enabled. Currently, up to two output images can be previewed simultaneously. |
| -rotation | 0: rotate 0 degrees, 1: rotate 90 degrees, 2: rotate 180 degrees, 3: rotate 270 degrees, 4: unsupported rotation, 17 use gdma rotate 90 degrees, 18 use gdma rotate 180 degrees, 19 use gdma rotate 270 degrees | Specify the rotation angle of the preview display window. only the first output image window supports the vo rotation function, all output image window supports gdma rotation function. |

Example:

`./sample_vicap.elf -conn 3 -dev 0 -sensor 19 -chn 0 -ow 800 -oh 480 -rotation 1`

Explanation: Bind ov5647@1920x1080 to vicap device 0, enable vicap device output channel 0, and display 800x480 through the screen.

### 2.2 DMA_demo

#### 2.2.1 DMA_demo Introduction

##### 2.2.1.1 Non-Binding Mode

DMA channels 0-3 are GDMA, and 4-7 are SDMA.

- Channel 0 continuously inputs an image with a resolution of 1920x1080, 8bit, YUV400, single-channel mode, rotates 90 degrees, and outputs, comparing with golden data.
- Channel 1 continuously inputs an image with a resolution of 1280x720, 8bit, YUV420, dual-channel mode, rotates 180 degrees, and outputs, comparing with golden data.
- Channel 2 continuously inputs an image with a resolution of 1280x720, 10bit, YUV420, triple-channel mode, x-mirror, y-mirror, and outputs, comparing with golden data.
- Channel 4 is in 1D mode, cyclically transmitting a segment of data, and compares with golden data after transmission.
- Channel 5 is in 2D mode, cyclically transmitting a segment of data, and compares with golden data after transmission.

##### 2.2.1.2 Binding Mode

Use VVI as DMA simulated input, bind channel 0 of VVI device 0 to DMA channel 0, and bind channel 1 of VVI device 0 to DMA channel 1. VVI inputs a 640x320, YUV400, 8bit image rotated 90° to channel 0 every second, and a 640x320, YUV400, 8bit image rotated 180° to channel 1.

#### 2.2.2 Feature Description

Includes DMA device attribute configuration, channel attribute configuration, graphic input, output, release, pipeline binding, and other functions.

#### 2.2.3 Dependency Resources

None

#### 2.2.4 Usage Instructions

##### 2.2.4.1 Compilation

Refer to the `README.md` in the release SDK package for software compilation.

##### 2.2.4.2 Execution

1. Non-binding mode demo run

`/sdcard/app/sample_dma.elf`

Test information will be displayed on the screen, and input `q` to end the run.

1. Binding mode demo run

`/sdcard/app/sample_dma_bind.elf`

Test information will be displayed on the screen, and input `q` to end the run.

### 2.3 USB_demo

#### 2.3.1 USB_demo Introduction

The USB demo currently has four functions debugged:

As a device, it simulates a USB drive and simulates a mouse and keyboard.

As a host, it connects to a USB drive and connects to a mouse and keyboard.

#### 2.3.2 Feature Description

The USB demo functions are originally integrated into the Linux system.

#### 2.3.3 Dependency Resources

Type-C cable, Type-C to Type-A adapter.

#### 2.3.4 Usage Instructions

##### 2.3.4.1 Simulate USB Drive as Device

```shell
# Allocate a memory space as the disk space for the simulated USB drive.
[root@canaan / ]#gadget-storage-mem.sh
2+0 records in
2+0 records out
mkfs.fat 4.1 (2017-01-24)
[ 1218.882053] Mass Storage Function, version: 2009/09/11
[ 1218.887308] LUN: removable file: (no medium)
[ 1218.895464] dwc2 91500000.usb-otg: bound driver configfs-gadget
[root@canaan / ]#[ 1219.019554] dwc2 91500000.usb-otg: new device is high-speed
[ 1219.056629] dwc2 91500000.usb-otg: new address 5

## Use the FAT partition of SD/eMMC as the disk space for the simulated USB drive.
[root@canaan ~ ]#gadget-storage.sh
[  359.995510] Mass Storage Function, version: 2009/09/11
[  360.000762] LUN: removable file: (no medium)
[  360.013138] dwc2 91500000.usb-otg: bound driver configfs-gadget
[root@canaan ~ ]#[  360.136809] dwc2 91500000.usb-otg: new device is high-speed
[  360.173543] dwc2 91500000.usb-otg: new address 43
```

Connect the USB port of the development board, and the Type-C connects to the PC. The PC will display the USB drive connection.

##### 2.3.4.2 Connect USB Drive as Host

The USB port of the K230 development board connects to a USB drive through a Type-C to Type-A adapter.

##### 2.3.4.3 Simulate Mouse and Keyboard as Device

The USB port of the K230 development board connects to another computer device via Type-C for testing.

```shell
[root@canaan / ]#gadget-hid.sh

[root@canaan / ]#hid_gadget_test /dev/hidg0 mouse
# Input the corresponding operations as prompted, such as -123 -123, and you can see the mouse pointer move on the PC.

[root@canaan / ]#hid_gadget_test /dev/hidg1 keyboard
# Input the corresponding operations as prompted, and you can see similar keyboard inputs on the PC. For example, a b c --return
```

##### 2.3.4.4 Connect Mouse and Keyboard as Host

The USB port of the K230 development board connects to a mouse or keyboard through a Type-C to Type-A adapter.

```shell
# Use the following command to determine the event corresponding to the input device. If the K230 development board is not connected to a screen, the event corresponding to the connected mouse and keyboard will change.
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
# Click or move the mouse, and corresponding information will be displayed on the serial port.

[root@canaan / ]$ test_keyboard /dev/input/event2
# Press different keys on the keyboard, and corresponding information will be displayed on the serial port.
```

### 2.4 FFT Demo

#### 2.4.1 Demo Introduction

This demo is used to verify the usage of the FFT API and test the FFT functionality. The code can be found in `src/big/mpp/userapps/sample/sample_fft/`.

#### 2.4.2 Feature Description

First, perform FFT calculation, then perform IFFT calculation.

#### 2.4.3 Dependency Resources

None

#### 2.4.4 Usage Instructions

##### 2.4.4.1 Compilation

> Please refer to the `README.md` in the release SDK package.

##### 2.4.4.2 Execution

1. After the system is up, execute the following commands on the main core command line:

   ```bash
   cd /sdcard/app; ./sample_fft.elf
   ```

   The main core serial port will output the following content:

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
