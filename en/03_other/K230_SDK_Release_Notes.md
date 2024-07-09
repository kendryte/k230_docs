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
| 29 | K230 SDK V1.5     | gc2053           | Added gc2053 driver                                                                                                                |         |
