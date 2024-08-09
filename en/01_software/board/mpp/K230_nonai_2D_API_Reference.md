# K230 nonai 2D API Reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Canaan Creative (Beijing) Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Canaan Creative (Beijing) Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the CSC function and usage of nonai 2d.

### Intended Audience

This document (this guide) is mainly for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                       |
|--------------|-----------------------------------|
| CSC          | color space convert               |
| VENC         | video encoder                     |

### Revision History

| Document Version | Modification Description | Author | Date       |
|------------------|--------------------------|--------|------------|
| V1.0       | Initial version | Longyiluo | 2024.02.02  |
| V1.1       | Add functional description and error correction | Longyiluo | 2024.07.01  |

## 1. Overview

### 1.1 Overview

Nonai 2D hardware can implement OSD, border and CSC functions. This article only describes the CSC function, OSD and border APIs have not been implemented of this article yet. If there is a need in the future, they can be added.

The VENC module implements overlay OSD and border on encoded images by the nonai 2D hardware, which cannot be used alone and only be used with encoded images. Please refer to sections 1.2.1.4 and 2.1.14 to 2.1.29 of the K230_video_codec_API Reference.

### 1.2 Function Description

Implement the conversion between RGB and YUV as a module of MPP. It can participate in system binding function, and also can perform single frame processing without binding.

Supports conversion of the following image formats:

PIXEL_FORMAT_YUV_SEMIPLANAR_420

PIXEL_FORMAT_YVU_PLANAR_420

PIXEL_FORMAT_YUV_PACKAGE_444

PIXEL_FORMAT_YVU_PLANAR_444

PIXEL_FORMAT_RGB_565

PIXEL_FORMAT_RGB_888

PIXEL_FORMAT_RGB_888_PLANAR

Sample code：

```c
k_nonai_2d_chn_attr attr_2d;
k_video_frame_info input;
k_video_frame_info output;
int ch = 0;

attr_2d.mode = K_NONAI_2D_CALC_MODE_CSC;
attr_2d.dst_fmt = PIXEL_FORMAT_YUV_SEMIPLANAR_420;
kd_mpi_nonai_2d_create_chn(ch, &attr_2d);
kd_mpi_nonai_2d_start_chn(ch);

input.v_frame.pixel_format = PIXEL_FORMAT_RGB_888;
kd_mpi_nonai_2d_send_frame(ch, &input, 1000);
kd_mpi_nonai_2d_get_frame(ch, &output, 1000);

kd_mpi_nonai_2d_stop_chn(ch);
kd_mpi_nonai_2d_destroy_chn(ch);
```

## 2. API Reference

- [kd_mpi_nonai_2d_create_chn](#21-kd_mpi_nonai_2d_create_chn)
- [kd_mpi_nonai_2d_destroy_chn](#22-kd_mpi_nonai_2d_destory_chn)
- [kd_mpi_nonai_2d_start_chn](#23-kd_mpi_nonai_2d_start_chn)
- [kd_mpi_nonai_2d_stop_chn](#24-kd_mpi_nonai_2d_stop_chn)
- [kd_mpi_nonai_2d_get_frame](#25-kd_mpi_nonai_2d_get_frame)
- [kd_mpi_nonai_2d_release_frame](#26-kd_mpi_nonai_2d_release_frame)
- [kd_mpi_nonai_2d_send_frame](#27-kd_mpi_nonai_2d_send_frame)

### 2.1 kd_mpi_nonai_2d_create_chn

【Description】

Create a channel.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_create_chn(k_u32 chn_num, const k_nonai_2d_chn_attr *attr);
```

【Parameters】

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input      |
| attr     | Pointer to encoding channel attributes. | Input      |

【Return Value】

| Return Value | Description |
|---|---|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files:mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

None.

【Example】

None.

【Related Topics】

None.

### 2.2 kd_mpi_nonai_2d_destory_chn

【Description】

销毁通道.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_destory_chn(k_u32 chn_num);
```

【Parameters】

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input      |

【Return Value】

| Return Value | Description                          |
|---|---|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- Must call kd_mpi_nonai_2d_stop_chn to stop receiving images before destroying, otherwise returns failure.

【Example】

None.

【Related Topics】

None.

### 2.3 kd_mpi_nonai_2d_start_chn

【Description】

Start to receive input images.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_start_chn(k_u32 chn_num);
```

【Parameters】

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- If the channel is not created, it returns failure K_ERR_NONAI_2D_UNEXIST.
- If the channel has already started receiving images and calls this interface again without stopping, it returns operation not allowed.
- The channel starts receiving images for processing only after starting reception.

【Example】

None.

【Related Topics】

None.

### 2.4 kd_mpi_nonai_2d_stop_chn

【Description】

Stop to receive input images.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_stop_chn(k_u32 chn_num);
```

【Parameters】

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- If the channel is not created, it returns failure.
- This interface does not check if the reception is already stopped, allowing repeated stops without returning an error.
- This interface is used to stop receiving images, and must be called before destroying or resetting the channel.
- Calling this interface only stops receiving raw data, the stream buffer will not be cleared.

【Example】

None.

【Related Topics】

None.

### 2.5 kd_mpi_nonai_2d_get_frame

【Description】

Get the processed image

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_get_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

【Parameters】

| Parameter Name  | Description | Input/Output |
|---|---|---|
| chn_num | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input |
| frame    | Pointer to the frame structure. | Output |
| milli_sec | Timeout for getting the frame. Value range: [-1, +∞] -1：Blocking. 0：Non-blocking. >0：Timeout | Input |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- If the channel is not created, it returns failure.
- If `frame` is null, it returns K_ERR_NONAI_2D_NULL_PTR.
- If `milli_sec` is less than -1, it returns K_ERR_NONAI_2D_ILLEGAL_PARAM.

【Example】

None.

【Related Topics】

None.

### 2.6 kd_mpi_nonai_2d_release_frame

【Description】

Release the frame buffer.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_release_frame(k_u32 chn_num, k_video_frame_info *frame);
```

【Parameters】

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input |
| frame   | Pointer to the frame structure. | Output |

【Return Value】

| Return Value | Description |
|---|---|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- If the channel is not created, it returns error code K_ERR_NONAI_2D_UNEXIST.
- If `frame` is null, it returns error code K_ERR_NONAI_2D_NULL_PTR.

【Example】

None.

【Related Topics】

None.

### 2.7 kd_mpi_nonai_2d_send_frame

【Description】

Support users to send raw images for 2D calculation.

【Syntax】

```c
k_s32 kd_mpi_nonai_2d_send_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

【Parameters】

| Parameter Name  | Description | Input/Output |
|---|---|---|
| chn_num | channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS]. | Input |
| frame | Pointer to the raw image information structure, refer to "K230 System Control API Reference".  | Input |
| milli_sec | Timeout for sending the frame. Value range: [-1, +∞] -1：Blocking. 0：Non-blocking. >0：Timeout | Input |

【Return Value】

| Return Value | Description |
|---|---|
| 0      | Success.                        |
| Non-zero    | Failure, see [Error Codes](#5. Error Codes). |

【Chip Differences】

None.

【Requirements】

- Header files: mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- Library files: libvenc.a

【Notes】

- This interface supports users sending images to the channel.
- If `milli_sec` is less than -1, it returns K_ERR_NONAI_2D_ILLEGAL_PARAM.
- When calling this interface to send images, users need to ensure that the channel is created and started to receive input images.

【Example】

None.

【Related Topics】

None.

## 3. Data Types

The related data type definitions for this module are as follows:

### 3.1 K_NONAI_2D_MAX_CHN_NUMS

【Description】

 Defines the maximum number of channels.

【Definition】

```c
#define K_NONAI_2D_MAX_CHN_NUMS  24
```

【Notes】

None.

【Related Data Types and Interfaces】

None.

### 3.2 k_nonai_2d_calc_mode

【Description】

Definition 2D calculation modes.

【Definition】

```c
typedef enum
{
​     K_NONAI_2D_CALC_MODE_CSC = 0,    /* Color space conversion */
​     K_NONAI_2D_CALC_MODE_OSD,      /* On Screen Display */
​     K_NONAI_2D_CALC_MODE_BORDER,     /* Draw border */
​     K_NONAI_2D_CALC_MODE_OSD_BORDER,   /* OSD first, then draw border */
​     K_NONAI_2D_CALC_MODE_BUTT
} k_nonai_2d_calc_mode;
```

【Members】

| Members name | Description                  |
| -------- | --------------------- |
| mode     | 2D calculation modes |

【Notes】

At present, only CSC mode is supported, and other modes have not been implemented yet.

【Related Data Types and Interfaces】

None.

### 3.3 k_nonai_2d_chn_attr

【Description】

Definition channel attributes.

【Definition】

```c
typedef struct
{
​      k_pixel_format dst_fmt;     /* Format of output image */
​      k_nonai_2d_calc_mode mode;
} k_nonai_2d_chn_attr;
```

【Members】

| Members name | Description                  |
| -------- | --------------------- |
| dst_fmt  | output format. Refer to "K230 System Control API Reference". |
| mode     | 2D calculation modes, Refer to section 3.2 |

【Notes】

【Related Data Types and Interfaces】

None.

### 3.4 k_nonai_2d_color_gamut

【Description】

Definition the color type, the default is BT601.

【Definition】

```c
typedef enum
{
​     NONAI_2D_COLOR_GAMUT_BT601 = 0,
​     NONAI_2D_COLOR_GAMUT_BT709,
​     NONAI_2D_COLOR_GAMUT_BT2020,
​     NONAI_2D_COLOR_GAMUT_BUTT
} k_nonai_2d_color_gamut;
```

【Notes】

None.

【Related Data Types and Interfaces】

None.

## 4. MAPI

### 4.1 Overview

MAPI is called on the small core to create nonai_2d channels.

- [kd_mpi_nonai_2d_init](#42-kd_mapi_nonai_2d_init)
- [kd_mpi_nonai_2d_deinit](#43-kd_mapi_nonai_2d_deinit)
- [kd_mpi_nonai_2d_start](#44-kd_mapi_nonai_2d_start)
- [kd_mpi_nonai_2d_stop](#45-kd_mapi_nonai_2d_stop)

### 4.2 kd_mapi_nonai_2d_init

【Description】

Initial channel

【Syntax】

```c
k_s32 kd_mapi_nonai_2d_init(k_u32 chn_num, k_nonai_2d_chn_attr * attr)
```

【Parameters】

| Parameter Name          | Description                                                   | Input/Output |
| ----------------- | ------------------------------------------------------ | --------- |
| chn_num           | NONAI_2D channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS] | Input      |
| pst_nonai_2d_attr | NONAI_2D channel attributs                   | Input      |

【Return Value】

| Return Value | Description               |
|--------|--------------------|
| 0      | Success               |
| Non-zero    | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None .

【Requirements】

Header files: mapi_nonai_2d_api.h、k_nonai_2d_comm.h
Library files: libmapi.a libipcmsg.a libdatafifo.a

【Notes】

- Before calling this interface, `kd_mapi_sys_init()` and `kd_mapi_media_init()` need to be successfully initialized. See the "SYS MAPI" section for details.
- Reinitialization returns success.

【Example】

None.

【Related Topics】

None.

### 4.3 kd_mapi_nonai_2d_deinit

【Description】

Deinitializes the channel.

【Syntax】

```c
k_s32 kd_mapi_nonai_2d_deinit(k_u32 chn_num)
```

【Parameters】

| Parameter Name | Description                                                   | Input/Output |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS] | Input      |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success                          |
| Non-zero    | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None .

【Requirements】

Header files: mapi_nonai_2d_api.h、k_nonai_2d_comm.h
Library files: libmapi.a libipcmsg.a libdatafifo.a

【Notes】

None.

【Example】

None.

【Related Topics】

None.

### 4.4 kd_mapi_nonai_2d_start

【Description】

Start channel.

【Syntax】

```c
k_s32 kd_mapi_nonai_2d_start(k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                                   | Input/Output |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS] | Input      |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success                          |
| Non-zero    | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None .

【Requirements】

Header files: mapi_nonai_2d_api.h、k_nonai_2d_comm.h
Library files: libmapi.a libipcmsg.a libdatafifo.a

【Notes】

None.

【Example】

None.

【Related Topics】

### 4.5 kd_mapi_nonai_2d_stop

【Description】

Stop channel.

【Syntax】

```c
k_s32 kd_mapi_nonai_2d_stop(k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                                   | Input/Output |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D channel number. Value range:[0, K_NONAI_2D_MAX_CHN_NUMS] | Input      |

【Return Value】

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success                          |
| Non-zero    | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: mapi_nonai_2d_api.h、k_nonai_2d_comm.h
Library files: libmapi.a libipcmsg.a libdatafifo.a

【Notes】

None.

【Example】

None.

【Related Topics】

## 5. Error Codes

Table 41 Encoding API Error Codes
| Error Code | Macro Definition             | Description                                         |
| ---------- | ---------------------------- | -------------------------------------------- |
| 0xa0188001 | K_ERR_NONAI_2D_INVALID_DEVID | Device ID out of valid range                        |
| 0xa0188002 | K_ERR_NONAI_2D_INVALID_CHNID | Channel ID out of valid range                       |
| 0xa0188003 | K_ERR_NONAI_2D_ILLEGAL_PARAM | Parameters out of valid range                             |
| 0xa0188004 | K_ERR_NONAI_2D_EXIST         | Attempt to create an existing device, channel, or resource |
| 0xa0188005 | K_ERR_NONAI_2D_UNEXIST       | Attempt to use or destroy a non-existent device, channel, or resource |
| 0xa0188006 | K_ERR_NONAI_2D_NULL_PTR      | Null pointer in function parameter             |
| 0xa0188007 | K_ERR_NONAI_2D_NOT_CONFIG    | Not configured before use                      |
| 0xa0188008 | K_ERR_NONAI_2D_NOT_SUPPORT   | Unsupported parameter or function              |
| 0xa0188009 | K_ERR_NONAI_2D_NOT_PERM      | Operation not allowed, such as trying to modify static configuration parameters |
| 0xa018800c | K_ERR_NONAI_2D_NOMEM         | Memory allocation failure, such as insufficient system memory |
| 0xa018800d | K_ERR_NONAI_2D_NOBUF         | Buffer allocation failure, such as requested data buffer too large |
| 0xa018800e | K_ERR_NONAI_2D_BUF_EMPTY     | No data in the buffer                          |
| 0xa018800f | K_ERR_NONAI_2D_BUF_FULL      | Data in the buffer is full                     |
| 0xa0188010 | K_ERR_NONAI_2D_NOTREADY      | System not initialized or corresponding module not loaded |
| 0xa0188011 | K_ERR_NONAI_2D_BADADDR       | Address out of valid range                     |
| 0xa0188012 | K_ERR_NONAI_2D_BUSY          | NONAI_2D system busy                               |

## 6. Debug Information

For multimedia memory management and system binding debug information, please refer to the "K230 System Control API Reference".
