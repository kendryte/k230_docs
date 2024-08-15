# K230 SDK Release Notes

! [cover](../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company makes no explicit or implicit representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is only for guidance and reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

! [logo](../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or distribute any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the content related to the release of K230 SDK V1.6.0, including the supported hardware, features, usage restrictions, etc., of the current version.

### Target Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation        | Description                                             |
|---------------------|---------------------------------------------------------|
| K230 USIP LP3 EVB   | Development board with K230 chip in USIP package form and LPDDR3 |
| VENC                | Video Encoder                                           |
| VDEC                | Video Decoder                                           |
| VICAP               | Video Input Capture                                     |
| VO                  | Video Output                                            |
| AI                  | Audio Input                                             |
| AO                  | Audio Output                                            |
| AENC                | Audio Encoder                                           |
| ADEC                | Audio Decoder                                           |
| NonAI-2D            | 2D graphics acceleration module, supports OSD overlay, frame drawing, CSC transformation, etc. |
| MCM                 | Multi Camera Management                                 |

## 1. Version Information

| Product   | Version  | Release Date |
|-----------|----------|--------------|
| K230 SDK  | V1.6.0   | 2024-6-14    |

## 2. Supported Hardware

The K230 platform supports mainboards like K230 USIP LP3 EVB and CanMV-K230. For specific hardware information, refer to the documentation directory: [00_hardware](../00_hardware).

## 3. Version Usage Restrictions

The current SDK's memory layout on USIP LP3 EVB and CanMV-K230 is as shown below:

! [EVB](../../zh/03_other/images/70c84709960aa37885bfaabcc29d0538.jpg)

Figure-1 SDK Memory Layout

You can configure the memory regions for each module by entering `make menuconfig` under the k230_sdk directory and selecting `Memory->Configuration`. Currently, configuring the memory for parameter areas and inter-core communication areas is not supported.

## 4. Version Feature Statistics

### 4.1 Multimedia

| ID | Supported Version | Feature Summary      | Feature Description                                                                      | Remarks |
|----|-------------------|----------------------|------------------------------------------------------------------------------------------|---------|
| 1  | K230 SDK V0.5     | venc                 | H264/H265/JPEG encoding                                                                  |         |
| 2  | K230 SDK V0.5     | vdec                 | H264/H265/JPEG decoding                                                                  |         |
| 3  | K230 SDK V0.5     | vicap bind venc      | vicap input bound to venc output                                                         |         |
| 4  | K230 SDK V0.5     | vdec bind vo         | vdec bound to vo for image output                                                        |         |
| 5  | K230 SDK V0.5     | venc_2d              | OSD overlay after encoding                                                               |         |
| 6  | K230 SDK V0.5     | nonai_2d             | OSD overlay                                                                              |         |
| 7  | K230 SDK V0.5     | i2s audio input      | Sampling precision (16/24/32), sampling rate (8k-192k), timestamp (us), dual-channel, configurable samples per frame. |        |
| 8  | K230 SDK V0.5     | pdm audio input      | Sampling precision (16/24), sampling rate (8k-192k), oversampling (32/64/128), single/dual-channel, timestamp (us), configurable samples per frame. |        |
| 9  | K230 SDK V0.5     | i2s audio output     | Sampling precision (16/24/32), sampling rate (8k-192k), dual-channel, configurable samples per frame. |        |
| 10 | K230 SDK V0.5     | built-in audio codec | Supports adc, dac, sampling precision (16/24), sampling rate (8k-192k)                    |         |
| 11 | K230 SDK V0.5     | ai(i2s) bind ao(i2s) | ai bound to ao, i2s audio capture to i2s audio output loopback                            |         |
| 12 | K230 SDK V0.5     | ai(pdm) bind ao(i2s) | ai bound to ao, pdm audio capture to i2s audio output loopback                            |         |
| 13 | K230 SDK V0.6     | venc                 | Multi-channel encoding, rotation, and mirroring                                          |         |
| 14 | K230 SDK V0.6     | venc_2d              | Frame drawing                                                                            |         |
| 15 | K230 SDK V0.6     | venc MAPI            | VI->VENC->save file on small core                                                        |         |
| 16 | K230 SDK V0.6     | aenc                 | Audio encoding, built-in g711a/u                                                         |         |
| 17 | K230 SDK V0.6     | adec                 | Audio decoding, built-in g711a/u                                                         |         |
| 18 | K230 SDK V0.6     | ai bind aenc         | ai bound to aenc, collecting encoded data                                                |         |
| 19 | K230 SDK V0.6     | adec bind ao         | adec bound to ao, playing decoded audio output                                           |         |
| 20 | K230 SDK V0.6     | audio 3a             | AEC (Echo Cancellation), ANS (Noise Suppression), AGC (Automatic Gain Control)            |         |
| 21 | K230 SDK V0.7     | venc gop             | Supports setting encoding GOP                                                            |         |
| 22 | K230 SDK V0.7     | venc mirror          | Supports setting encoding horizontal and vertical flip                                   |         |
| 23 | K230 SDK V0.7     | venc idr             | Supports enabling/disabling encoding IDR frames                                          |         |
| 24 | K230 SDK V0.7     | venc multi channel   | mapi_venc_2-channel h264 encoding                                                        |         |
| 25 | K230 SDK V0.7     | audio i2s mapi       | mapi-audio_i2S captures audio, encodes it, and passes it to the main core                |         |
| 26 | K230 SDK V0.7     | audio enc mapi       | mapi-audio_small core encodes the file, passes it to the main core for decoding and playback |        |
| 27 | K230 SDK V0.7     | audio volume         | Adds interface for digital and analog volume control of the built-in audio codec.        |         |
| 28 | K230 SDK V0.7     | mapi rtsp            | mapi-network transmission-rtsp audio and video streaming                                 |         |
| 29 | K230 SDK V0.8     | mapi vdec            | Small core video encoded file passed to the main core for decoding and playback          |         |
| 30 | K230 SDK V0.8     | venc mpi             | deblock, sao, entropy: enable/disable                                                    |         |
| 31 | K230 SDK V0.8     | vdec mpi             | Supports downscale                                                                      |         |
| 32 | K230 SDK V0.8     | dpu demo             | Screen display depth map: vicap->dma->dpu->vo                                            |         |
| 32 | K230 SDK V0.8     | Voice intercom demo  | Adds voice intercom demo                                                                 |         |
| 33 | K230 SDK V0.9     | Cat-eye poc          | Remote cat-eye, realizing visual intercom, voice change, recording, human detection, and snapshot functions. |        |
| 34 | K230 SDK V1.0     | Cat-eye poc          | 1. Adds UI control on the cat-eye device side. 2. Adds local cat-eye voice intercom functionality. 3. Changes the mobile phone recording feature to be implemented on the device side, always recording. 4. |        |
| 34 | K230 SDK V1.0 | Cat-eye poc| Added playback function on the cat-eye device side. | |
| 35 | K230 SDK V1.2 | Cat-eye poc | Changed to nor flash boot | |
| 35 | K230 SDK V1.3 | Depth camera poc | Added depth camera poc function, cat-eye poc changed to SD card boot | |
| 36 | K230 SDK V1.4 | nonai_2d API | Added nonai_2d CSC function mpi and mapi | |
| 37 | K230 SDK V1.4 | YUV Sensor Demo | Added YUV sensor demo, 3-way YUV sensor input, 3-way streaming and display | |

### 4.2 Image

| ID | Supported Version | Feature Summary  | Feature Description                                                                                                                | Remarks |
|----|-------------------|------------------|------------------------------------------------------------------------------------------------------------------------------------|---------|
| 1  | K230 SDK V0.5     | vicap            | Supports sensor image capture (OV9732, OV9286)                                                                                     |         |
| 2  | K230 SDK V0.5     | AE               | Supports AE auto exposure                                                                                                          |         |
| 3  | K230 SDK V0.5     | vicap bind vo    | vicap bound to vo for image output                                                                                                |         |
| 4  | K230 SDK V0.5     | GPU drawing      | Vector drawing and filling (lines, quadratic Bezier curves, cubic Bezier curves, elliptical curves), linear gradient, color lookup table, image composition/blending, BLIT |         |
| 5  | K230 SDK V0.5     | Image tuning     | Tuning tool connects to the development board via network or serial port for image tuning. Black level correction, lens shading correction, color calibration, AWB, CAC, gamma |         |
| 6  | K230 SDK V0.5     | display bind     | Supports vo and vicap, vo and vdec binding                                                                                        |         |
| 7  | K230 SDK V0.5     | display          | Supports OSD and YUV display, supports frame dump function, supports configurable DSI and vo timing, supports frame insertion function |         |
| 8  | K230 SDK V0.6     | Image tuning     | Tuning tool can configure sensor registers                                                                                        |         |
| 9  | K230 SDK V0.6     | Timestamp, frame number | Supports timestamp and frame number                                                                                                |         |
| 10 | K230 SDK V0.6     | ISP+KPU Demo     | Face detection linkage demo                                                                                                        |         |
| 11 | K230 SDK V0.7     | dewarp           | Added dewarp function for distortion correction                                                                                    |         |
| 12 | K230 SDK V0.7     | Face AE          | Added FaceAE function and corresponding FaceAE demo                                                                                |         |
| 13 | K230 SDK V0.7     | Added Imx335     | Added Imx335 sensor driver and demo                                                                                                |         |
| 14 | K230 SDK V0.8     | Added DRM        | Added DRM driver and demo for Linux small core                                                                                     |         |
| 15 | K230 SDK V0.8     | Added LVGL       | Added LVGL and demo for Linux small core                                                                                           |         |
| 16 | K230 SDK V0.8     | Fast start APP   | Fast start APP sensor changed to Imx335 (with crystal oscillator)                                                                  |         |
| 17 | K230 SDK V0.9     | mcm              | Supports up to three sensors                                                                                                       |         |
| 18 | K230 SDK V0.9     | display mapi     | Added video output MAPI                                                                                                            |         |
| 19 | K230 SDK V1.0     | Debug-Dump sensor raw | Supports dumping sensor raw data                                                                                                   |         |
| 20 | K230 SDK V1.0     | Debug-Frame count statistics | Supports total input and output frame count statistics                                                                              |         |
| 21 | K230 SDK V1.0     | dewarp-Split screen | Supports 2, 4 split screen output                                                                                                  |         |
| 22 | K230 SDK V1.0     | HDR              | Supports HDR function, supports Imx335 2dol HDR                                                                                    |         |
| 23 | K230 SDK V1.1     | MAPI             | Added vicap MAPI                                                                                                                   |         |
| 24 | K230 SDK V1.1     | HDR frequency change | Supports HDR frequency change                                                                                                      |         |
| 25 | K230 SDK V1.1     | Parameter export | Supports exporting isp dewarp parameters                                                                                           |         |
| 26 | K230 SDK V1.2     | Added dictionary pen POC | Added dictionary pen POC                                                                                                           |         |
| 27 | K230 SDK V1.3     | Added three-camera demo | Added demo for Canmv-K230 board with three cameras (ov5647) working simultaneously                                                |         |
| 28 | K230 SDK V1.4     | Vicap MCM only mode | Vicap MCM only mode adapted for YUV sensor                                                                                         |         |
| 29 | K230 SDK V1.4     | linear mode supports adaptive | linear mode supports adaptive                                                                                                      |         |
| 30 | K230 SDK V1.5     | GC2053           | Added GC2053 driver                                                                  |         |

### 4.3 Platform

| ID | Supported Version | Function Overview | Function Description                                                                 | Remarks |
|----|-------------------|-------------------|--------------------------------------------------------------------------------------|---------|
| 1  | K230 SDK V0.5     | Boot Peripherals  | Supports eMMC, 1/4 wire SD card                                                      |         |
| 2  | K230 SDK V0.5     | Big Core DPU Driver | Image input, output driver development; Basic functions, e.g., read parameters, support dynamic update of long-cycle parameters, output buffer, timestamp, algorithm, etc.; support pipeline binding |         |
| 3  | K230 SDK V0.5     | Small Core UBOOT  | DDR training, disk driver (eMMC, SD, SPI 1 wire); supports PUFs and gzip decompression |         |
| 4  | K230 SDK V0.5     | Small Core SPI Driver | 1 wire                                                                              |         |
| 5  | K230 SDK V0.5     | Small Core SDIO Driver | Supports SDIO0/1 connecting SDCard                                                   |         |
| 6  | K230 SDK V0.5     | Small Core USB (UVC) Driver | Supports UVC driver (K230 chip as slave)                                             |         |
| 7  | K230 SDK V0.5     | Small Core GPIO Driver | Supports each IO as a separate logical resource allocation; supports IO and interrupt |         |
| 8  | K230 SDK V0.5     | Small Core Disk and File System | Supports SDIO0/1 connecting SDCard, supports SDIO0/1 connecting eMMC; supports ext2/3/4, FAT32 file system |         |
| 9  | K230 SDK V0.5     | I2C Driver        | Big and small core I2C bus driver                                                    |         |
| 10 | K230 SDK V0.5     | UART Driver       | Big and small core UART driver                                                       |         |
| 11 | K230 SDK V0.5     | UVC Basic Demo    | UVC camera, using the board as a camera                                              |         |
| 12 | K230 SDK V0.5     | GSDMA (Big Core Driver) | Supports using GDMA for image transfer, through configuration of channel attributes to achieve image rotation and mirroring, transfer multiple image formats (e.g., YUV400, YUV420, YUV444), transfer images with multiple pixel bit widths (e.g., 8bit, 10bit, 16bit); supports using SDMA for data transfer, supports 1D mode and 2D mode transfer; supports pipeline binding |         |
| 13 | K230 SDK V0.6     | Big Core GPIO Driver | Supports independent configuration and use of IO functions, independent configuration and triggering of interrupts, added hardware mutex lock to ensure mutual exclusion of register access |         |
| 14 | K230 SDK V0.6     | Boot Peripherals  | Supports SPI NOR flash image generation and boot                                      |         |
| 15 | K230 SDK V0.6     | UBOOT SPI NOR Flash Driver | Supports 8-wire DMA                                                                  |         |
| 16 | K230 SDK V0.6     | Big Core ADC Driver | Supports ADC voltage reading                                                         |         |
| 17 | K230 SDK V0.7     | Big and Small Core WDT Driver | Supports watchdog reset SOC                                                          |         |
| 18 | K230 SDK V0.7     | Big Core SPI Driver | Supports SPI single-wire mode, supports NAND flash                                    |         |
| 19 | K230 SDK V0.7     | Small Core SPI Driver | Supports SPI single-wire, 8-wire mode, supports NOR flash                             |         |
| 20 | K230 SDK V0.7     | Quick Boot        | SDK defaults to quick boot, non-quick boot version can disable CONFIG_QUICK_BOOT macro via make menuconfig; quick boot version UBOOT will not enter command line |         |
| 21 | K230 SDK V0.7     | Secure Image      | SDK defaults to not generating secure image, can configure CONFIG_GEN_SECURITY_IMG via make menuconfig to generate secure image |         |
| 22 | K230 SDK V0.7     | UVC Basic Demo    | Added support for H264 format, currently has bugs, can only run for a short time      |         |
| 23 | K230 SDK V0.7     | DPU, GSDMA        | Buffer quantity configurable                                                         |         |
| 24 | K230 SDK V0.8     | Big Core Timer, RTC, PWM | Added timer driver and demo for big core; added PWM driver and demo for big core; added RTC driver and demo for big core |         |
| 25 | K230 SDK V0.8     | SPI NAND Support  | Small core (UBOOT, Linux) supports 4-wire SPI NAND driver, SDK supports boot from SPI NAND |         |
| 26 | K230 SDK V0.8     | UVC Basic Demo    | UVC supports IMX335 camera, UVC supports MJPEG format                                 |         |
| 27 | K230 SDK V0.8     | SPI NOR Adds Face Feature and Other Parameter Partitions | SPI NOR adds face feature, AI model, calibration parameters, big core app, speckle, quick boot parameters and other parameter partitions; when booting from SPI NOR, UBOOT will parse and load each partition data |         |
| 28 | K230 SDK V0.9     | Small Core PWM Driver | Supports small core PWM driver                                                       |         |
| 29 | K230 SDK V0.9     | Small Core ADC Driver | Supports small core ADC driver                                                       |         |
| 30 | K230 SDK V0.9     | Supports K230D Development Board | SDK supports K230D development board (SD card boot)                                   |         |
| 31 | K230 SDK V0.9     | OTA               | Supports OTA upgrade                                                                 |         |
| 32 | K230 SDK V1.0     | Big Core FFT      | Supports FFT driver                                                                  |         |
| 33 | K230 SDK V1.0.1   | Supports CanMV-K230 Development Board | SDK supports CanMV-K230 development board (SD card boot)                              |         |
| 34 | K230 SDK V1.1     | Small Core WiFi Driver | Small core supports AP6256 driver                                                    |         |
| 35 | K230 SDK V1.1     | Small Core Tri-Color LED Driver | Small core supports I2S interface WS2812 driver                                       |         |
| 36 | K230 SDK V1.1     | Small Core SPI LCD Driver | Small core supports SPI interface ST7735S 0.96-inch LCD screen driver                 |         |
| 37 | K230 SDK V1.1     | Burntool V2       | Removed full image burning page, added loader_sip.bin support for SIP burning, for details see [K230_SDK_Burntool Usage Guide.md](../01_software/pc/burntool/K230_SDK_Burntool_User_Guide.md  ) |         |
| 38 | K230 SDK V1.1     | USB Port Usage    | USB1 fixed as host mode, can connect USB-ETH or U disk and other peripherals, connect pin 3 and pin 4 of J5 header on EVB with jumper cap to enable power supply to peripherals; USB0 used for USB gadget testing and USB upgrade, no longer connect pin 1 and pin 2 of J5 header on EVB with jumper cap |         |
| 39 | K230 SDK V1.2     | CanMV WiFi AP6212 | CanMV supports AP6212                                                                |         |
| 40 | K230 SDK V1.2     | CanMV Only Linux  | CanMV adds configuration for running vector Linux on big core (k230_canmv_only_linux_defconfig) |         |
| 41 | K230 SDK V1.3     | Added Debian and Ubuntu Release Images | Added Debian and Ubuntu release images for CanMV                                       |         |
| 42 | K230 SDK V1.3     | OTA               | Buildroot adds swupdate OTA upgrade function, supports dual partition switch upgrade (requires dual partition boot scheme) | Refer to description in k230_sdk/tools/ota/README |
| 43 | K230 SDK V1.5     | USB to Ethernet   | Fixed instability issue of USB to Ethernet network                                    |         |
| 44 | K230 SDK V1.5     | Touch Control     | Added touch control for LCD screen                                                   |         |
| 45 | K230 SDK V1.5     | CanMV 2.0         | Supports CanMV-K230-V2.0 board                                                       |         |
| 46 | K230 SDK V1.6     | 01Studio-CanMV-K230 | Supports 01Studio-CanMV-K230 board                                                   |         |
| 47 | K230 SDK V1.6     | Supports RTT Only System | Supports RTT only single system                                                      |         |

### 4.4 Architecture

| ID | Supported Version | Function Overview | Function Description                                                                 | Remarks |
|----|-------------------|-------------------|--------------------------------------------------------------------------------------|---------|
| 1  | K230 SDK V0.5     | Multimedia Memory Management | Multimedia memory management driver, MPI, MAPI; video buffer pool driver, MPI, MAPI   |         |
| 2  | K230 SDK V0.5     | Log Management    | Multimedia log management driver, MPI, MAPI                                          |         |
| 3  | K230 SDK V0.5     | System Binding    | Multimedia system binding driver, MPI                                                |         |
| 4  | K230 SDK V0.5     | Big Core Multimedia Debugging | Provides proc file system for debugging                                              |         |
| 5  | K230 SDK V0.5     | Inter-Core Communication | Inter-core communication driver                                                      |         |
| 6  | K230 SDK V0.5     | Inter-Core Control Communication | IPCMSG library                                                                      |         |
| 7  | K230 SDK V0.5     | Inter-Core Data Communication | DATAFIFO library                                                                     |         |
| 8  | K230 SDK V0.5     | Shared File System | sharefs                                                                              | Small core as server, big core as client |
| 9  | K230 SDK V0.5     | System Control    | Big and small core clock power and reset driver                                      |         |
| 10 | K230 SDK V0.5     | KPU               | KPU driver                                                                           |         |
| 11 | K230 SDK V0.5     | Big Core System Debugging | JTAG debugging; local serial port                                                    |         |
| 12 | K230 SDK V0.5     | Small Core System Debugging | JTAG debugging, serial port debugging, network port debugging, CPU usage statistics and analysis, performance debugging methods, debugging and log output ports (physical serial port), kernel and exception information output, dump, debug version | perf is not configured by default in the kernel and buildroot |
| 13 | K230 SDK V0.7     | Software SHA256   | Added software implementation of SHA256 under big core MPP                            |         |
| 14 | K230 SDK V0.7     | OTP Read/Write Function | Added OTP read/write function in big core rt-smart, added OTP read function in small core Linux |         |
| 15 | K230 SDK V0.7     | Tsensor Read Function | Added Tsensor read function in big core rt-smart, added Tsensor read function in small core Linux, used to read chip junction temperature |         |
| 16 | K230 SDK V0.7     | TRNG Read Function | Added TRNG read function in small core Linux                                          |         |
| 17 | K230 SDK V0.7     | Quick Start Demo  | Added quick start face detection demo for big core                                    |         |
| 18 | K230 SDK V0.7     | PMU Function      | Added PMU standby and wake-up function for small core Linux                           |         |
| 19 | K230 SDK V0.8     | Door Lock POC     | Added POC door lock function in big core, added UI function in small core, register and recognize faces via UI interface or SD card |         |
| 20 | K230 SDK V0.9     | Door Lock POC     | Supports ov9286, face detection and recognition (including IR and speckle liveness detection, speckle includes DPU depth extraction) |         |
| 21 | K230 SDK V0.9     | Encryption/Decryption | Added AES-GCM encryption/decryption function for small core Linux                     |         |
| 22 | K230 SDK V0.9     | Power Consumption Control | Added chip clock/power domain management in uboot, added power consumption control for CPU1, DPU, VPU, KPU, and display in big core rt-smart, added power consumption control for display in small core Linux |         |
| 23 | K230 SDK V1.0     | Door Lock POC     | Added face feature encryption/decryption function                                     |         |
| 24 | K230 SDK V1.0     | SH256 Driver      | Added hardware SH256 driver for both big and small cores                              |         |
| 25 | K230 SDK V1.1     | Big Core Encryption/Decryption Driver | Added hardware AES-GCM driver and SM4-ECB/CBC/CFB/OFB/CTR driver for big core |         |
| 26 | K230 SDK V1.2     | Door Lock OTA Function | Added door lock OTA function                                                          |         |
| 27 | K230 SDK V1.3     | OTP Space Adjustment | Adjusted the OTP space operated by SDK, users can read/write 768 bytes. The remaining space is reserved for chip manufacturers |         |

### 4.5 Others

| ID | Supported Version | Function Overview | Function Description                                                                 | Remarks |
|----|-------------------|-------------------|--------------------------------------------------------------------------------------|---------|
| 1  | K230 SDK V0.5     | AI Demo           | Provides three AI demos: door_lock, object_detect, image_classify                     |         |
| 2  | K230 SDK V0.5     | AiW4211LV10 WiFi Driver | Supports network data communication; supports control command sending                |         |
| 3  | K230 SDK V0.6     | AiW4211LV10 WiFi Firmware | Firmware compatible with commands and network configuration, supports reconnection after disconnection, supports K230 level detection and wake-up |         |
| 4  | K230 SDK V0.6     | Touch Screen Support | Touch screen support                                                                 |         |
| 5  | K230 SDK V0.7     | Software Image    | SDK compilation will generate demo executable files, but by default not packaged into the image; secure image files are not generated by default, can be manually configured |         |
| 6  | K230 SDK V0.7     | Toolchain         | Big core toolchain version updated to: riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230420.tar.bz2 |         |
| 7  | K230 SDK V0.8     | Software Image    | When packaging Emmc/Sdcard images, the big core demos will be packaged into the small core/sharefs |         |
| 8  | K230 SDK V0.8     | Demo              | Modified related demos to adapt to different camera modules, such as encoding/UVC. Specific usage can be found in the "K230 SDK Demo Usage Guide" |         |
