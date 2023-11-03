# K230 DMA API reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the design of the K230 GSDMA software, including the GSDMA driver framework and software implementation.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate                         |
|------|------------------------------|
| GDMA | Graphic Direct Memory Access |
| SDMA | System Direct Memory Access  |

### Revision history

| Document version number | Modify the description                                                  | Author | date      |
|------------|-----------------------------------------------------------|--------|-----------|
| V1.0       | Initial                                                     | Liu Suntao | 2023/3/7  |
| V1.1       | Modified some descriptions of binding modes; Added function interface description to release frame number. | Liu Suntao | 2023/3/31 |
| V1.2       | Replaced the data structure of the image address; Added frame number transparent transmission function.           | Liu Suntao | 2023/4/26 |
| V1.3       | Added configurable functionality of buffer                             | Liu Suntao | 2023/5/31 |

## 1. Overview

### 1.1 Overview

GSDMA: DMA stands for Direct Memory Access, which copies data from one address space to another, providing high-speed data transfer between memory and memory. GDMA stands for Graphic Direct Memory Access, which is responsible for copying images in memory to another piece of memory, while completing functions such as rotating and mirroring images. SDMA stands for System Direct Memory Access, which is responsible for copying data from memory to another piece of memory, which is DMA in the traditional sense.

The software code provides the various functions of the GSDMA hardware to the user in the form of APIs, helping the user quickly realize image transmission, rotation, mirroring, 2D functions and data transmission functions. At the same time, the functions of module status information statistics are realized.

### 1.2 Function Description

DMA hardware is a device, eight channels, where channel 0\~3 is the GDMA channel and channel 4\~7 is the SDMA channel.

#### 1.2.1 gdma

Users use GDMA to rotate and mirror images, and the main call process is as follows:

1. Configure DMA device properties;
1. Start the DMA device. After calling this function, the driver automatically requests VB space as the data buffer for the destination address;
1. Configure GDMA channel properties;
1. Start the GDMA channel;
1. The user requests VB space as a data buffer for the source data in user mode, and calls kd_mpi_dma_send_frame to send the source address of the data to gdma;
1. The driver will transfer the data from the source address to the destination address data buffer requested in Step 2.
1. The user calls kd_mpi_dma_get_frame to get the data address in the destination address.

#### 1.2.2 SDMA

Users use SDMA to migrate data, and the main call process is as follows:

1. Configure DMA device properties;
1. Start the DMA device. After calling this function, the driver automatically requests VB space as the data buffer for the destination address;
1. Configure SDMA channel properties;
1. Start the SDMA channel;
1. The user requests VB space as a data buffer for the source data in user mode, and calls kd_mpi_dma_send_frame to send the source address of the data to sdma;
1. The driver will transfer the data from the source address to the destination address data buffer requested in Step 2.
1. The user calls kd_mpi_dma_get_frame to get the data address in the destination address.

## 2. API Reference

### 2.1 DMA Use

This function module provides the following APIs:

- [kd_mpi_dma_set_dev_attr](#211-kd_mpi_dma_set_dev_attr)
- [kd_mpi_dma_get_dev_attr](#212-kd_mpi_dma_get_dev_attr)
- [kd_mpi_dma_start_dev](#213-kd_mpi_dma_start_dev)
- [kd_mpi_dma_stop_dev](#214-kd_mpi_dma_stop_dev)
- [kd_mpi_dma_set_chn_attr](#215-kd_mpi_dma_set_chn_attr)
- [kd_mpi_dma_get_chn_attr](#216-kd_mpi_dma_get_chn_attr)
- [kd_mpi_dma_start_chn](#217-kd_mpi_dma_start_chn)
- [kd_mpi_dma_stop_chn](#218-kd_mpi_dma_stop_chn)
- [kd_mpi_dma_send_frame](#219-kd_mpi_dma_send_frame)
- [kd_mpi_dma_get_frame](#2110-kd_mpi_dma_get_frame)
- [kd_mpi_dma_release_frame](#2111-kd_mpi_dma_release_frame)

#### 2.1.1 kd_mpi_dma_set_dev_attr

【Description】

Configure DMA device properties

【Syntax】

k_s32 kd_mpi_dma_set_dev_attr(k_dma_dev_attr_t \*attr);

【Parameters】

| Parameter name | description                      | Input/output |
|----------|---------------------------|-----------|
| attr     | DMA device property structure pointer.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

None.

【Example】

None.

【See Also】

[k_dma_dev_attr_t](#314-k_dma_dev_attr_t)

#### 2.1.2 kd_mpi_dma_get_dev_attr

【Description】

Gets the configured DMA device properties.

【Syntax】

k_s32 kd_mpi_dma_get_dev_attr(k_dma_dev_attr_t \*attr);

【Parameters】

| Parameter name | description                   | Input/output |
|----------|------------------------|-----------|
| attr     | DMA device property structure pointer | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

DMA device properties cannot be obtained until you configure them.

【Example】

None.

【See Also】

[k_dma_dev_attr_t](#314-k_dma_dev_attr_t)

#### 2.1.3 kd_mpi_dma_start_dev

【Description】

Start the DMA device.

【Syntax】

k_s32 kd_mpi_dma_start_dev();

【Parameters】

| Parameter name | description | Input/output |
|----------|------|-----------|
| not       | not   | not        |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- DMA device properties need to be configured before this function can be called to start DMA

【Example】

None.

【See Also】

None.

#### 2.1.4 kd_mpi_dma_stop_dev

【Description】

Stop the DMA device.

【Syntax】

kd_mpi_dma_stop_dev();

【Parameters】

| Parameter name | description | Input/output |
|----------|------|-----------|
| not       | not   | not        |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- You can call this function to stop the DMA device only after you start it.

【Example】

none

【See Also】

None.

#### 2.1.5 kd_mpi_dma_set_chn_attr

【Description】

Configure DMA channel properties.

【Syntax】

k_s32 kd_mpi_dma_set_chn_attr(k_u8 chn_num, k_dma_chn_attr_u \*attr);

【Parameters】

| Parameter name | description                                                                                                                             | Input/output |
|----------|----------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | Channel number                                                                                                                           | input      |
| attr     | DMA channel properties, which are a federation and can optionally configure either GDMA channel properties or SDMA channel properties. Channel 0\~3 is GDMA, and channel 4\~7 is SDMA | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

None.

【Example】

None.

【See Also】

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

#### 2.1.6 kd_mpi_dma_get_chn_attr

【Description】

Gets the configured DMA channel properties.

【Syntax】

k_s32 kd_mpi_dma_get_chn_attr(k_u8 chn_num, k_dma_chn_attr_u \*attr);

【Parameters】

| Parameter name | description                                                                                                                             | Input/output |
|----------|----------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | Channel number                                                                                                                           | input      |
| attr     | DMA channel properties, which are a federation that can optionally get either GDMA channel properties or SDMA channel properties. Channel 0\~3 is GDMA, and channel 4\~7 is SDMA | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- DMA channel properties cannot be obtained until you configure them.

【Example】

None.

【See Also】

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

#### 2.1.7 kd_mpi_dma_start_chn

【Description】

Start the DMA channel.

【Syntax】

k_s32 kd_mpi_dma_start_chn(k_u8 chn_num);

【Parameters】

| Parameter name | description     | Input/output |
|----------|----------|-----------|
| chn_num  | Channel number. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- You can start a DMA channel only after you configure the boot DMA device and configure the DMA channel properties.

【Example】

None.

【See Also】

None.

#### 2.1.8 kd_mpi_dma_stop_chn

【Description】

Pause the DMA channel

【Syntax】

k_s32 kd_mpi_dma_stop_chn(k_u8 chn_num);

【Parameters】

| Parameter name | description     | Input/output |
|----------|----------|-----------|
| chn_num  | Channel number. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- You can call this function to stop a DMA channel only after you start it.

【Example】

none

【See Also】

None.

#### 2.1.9 kd_mpi_dma_send_frame

【Description】

Send data from user space to the destination address.

【Syntax】

k_s32 kd_mpi_dma_send_frame(k_u8 chn_num, k_video_frame_info \*df_info, k_s32 millisec);

【Parameters】

| Parameter name | description                                                                                                                                                                  | Input/output |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | Channel number.                                                                                                                                                              | input      |
| df_info  | The address information where the data is sent.                                                                                                                                                  | input      |
| millisec | Waiting time. When this parameter is set to -1, blocking; when this parameter is set to 0, it is non-blocking; when this parameter is set to a value greater than 0, it waits for the appropriate amount of time until the data is successfully sent, and returns a failure if it is not sent successfully after the timeout. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

None.

【Example】

None.

【See Also】

[k_video_frame_info](#316-k_video_frame_info)

#### 2.1.10 kd_mpi_dma_get_frame

【Description】

Gets the data after DMA is moved.

【Syntax】

k_s32 kd_mpi_dma_get_frame(k_u8 chn_num, k_video_frame_info \*df_info, k_s32 millisec);

【Parameters】

| Parameter name | description                                                                                                                                                                  | Input/output |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | Channel number.                                                                                                                                                              | input      |
| df_info  | Obtain the address information for the data.                                                                                                                                                  | output      |
| millisec | Waiting time. When this parameter is set to -1, blocking; when this parameter is set to 0, it is non-blocking; when this parameter is set to a value greater than 0, it waits for the corresponding time to know that the data was successfully obtained, and if it is not sent successfully after the timeout, it returns a failure. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

None.

【Example】

None.

【See Also】

[k_video_frame_info](#316-k_video_frame_info)

#### 2.1.11 kd_mpi_dma_release_frame

【Description】

Release the acquired DMA data.

【Syntax】

k_s32 kd_mpi_dma_release_frame(k_u8 chn_num, k_video_frame_info \*df_info);

【Parameters】

| Parameter name | description           | Input/output |
|----------|----------------|-----------|
| chn_num  | Channel number.       | input      |
| df_info  | The data to be released. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dma_api.h
- Library file: libdma.a

【Note】

- In the current design, the DMA output buffer is 3, and if 3 frames of data are not called to release it, the input data cannot continue. Therefore, the user should release the data in time after it is obtained.

【Example】

None.

【See Also】

[k_video_frame_info](#316-k_video_frame_info)

## 3 Data type

### 3.1 Common Data Types

#### 3.1.1 DMA_MAX_DEV_NUMS

【Description】

DMA maximum number of devices

【Definition】

```c
#define DMA_MAX_DEV_NUMS (1)
```

【Note】

None.

【See Also】

None.

#### 3.1.2 DMA_MAX_CHN_NUMS

【Description】

DMA maximum number of channels

【Definition】

\#define DMA_MAX_CHN_NUMS (8)

【Note】

None.

【See Also】

None.

#### 3.1.3 k_dma_mode_e

【Description】

Define the DMA operating mode.

【Definition】

```c
typedef enum
{
    DMA_BIND,
    DMA_UNBIND,
} k_dma_mode_e;
```

【Members】

| Member name | description       |
|----------|------------|
| BIND     | Binding mode. |
| UNBIND   | Unbound mode |

【Note】

None.

【See Also】

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

#### 3.1.4 k_dma_dev_attr_t

【Description】

Define DMA device properties.

【Definition】

```c
typedef struct
{
    k_u8 burst_len;
    k_u8 outstanding;
    k_bool ckg_bypass;
} k_dma_dev_attr_t;
```

【Members】

| Member name    | description                     |
|-------------|--------------------------|
| burst_len   | Configure the burst length of DMA |
| outstanding | 配置 dma outstanding     |
| ckg_bypass  | 配置 clock gate bypass   |

【Note】

None.

【See Also】

[kd_mpi_dma_set_dev_attr](#211-kd_mpi_dma_set_dev_attr)
[kd_mpi_dma_get_dev_attr](#212-kd_mpi_dma_get_dev_attr)

#### 3.1.5 k_dma_chn_attr_u

【Description】

Define DMA channel properties.

【Definition】

```c
typedef union
{
    k_gdma_chn_attr_t gdma_attr;
    k_sdma_chn_attr_t sdma_attr;
} k_dma_chn_attr_u;
```

【Members】

| Member name   | description                   |
|------------|------------------------|
| gdma_attr  | GDMA channel properties          |
| sdma_attr  | SDMA channel properties          |
| ckg_bypass | Set clock gate bypass |

【Note】

None.

【See Also】

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)
[kd_mpi_dma_set_chn_attr](#215-kd_mpi_dma_set_chn_attr)
[kd_mpi_dma_get_chn_attr](#216-kd_mpi_dma_get_chn_attr)

#### 3.1.6 k_video_frame_info

【Description】

Define the DMA data address.

【Definition】

```c
typedef struct
{
    k_video_frame v_frame;  /**< Video picture frame */
    k_u32 pool_id;          /**< VB pool ID */
    k_mod_id mod_id;        /**< Logical unit for generating video frames */
} k_video_frame_info;
```

【Members】

| Member name | description                     |
|----------|--------------------------|
| v_frame  | Timestamp, valid in bound mode. |
| pool_id  | Pool ID of the data VB pool.   |
| mod_id   | Module ID                  |

【Note】

None.

【See Also】

[kd_mpi_dma_send_frame](#219-kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#2110-kd_mpi_dma_get_frame)
[kd_mpi_dma_release_frame](#2111-kd_mpi_dma_release_frame)

#### 3.1.7 k_video_frame

【Description】

Define the DMA data address. The common data structure k_video_frame used, only a subset of its members are used.

【Definition】

```c
typedef struct
{
    k_u64 phys_addr[3];
    k_u64 virt_addr[3];
    k_u32 time_ref;
    k_u64 pts;
} k_video_frame;
```

【Members】

| Member name  | description                                                                                                                                         |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| phys_addr | The physical address of the image, if it is a single-channel image, only the first physical address needs to be configured; if it is a dual-channel image, only the first two physical addresses need to be configured; if it is a three-channel image, you need to configure three physical addresses. |
| virt_addr | The virtual address of the image, if it is a single-channel image, you only need to configure the first two virtual addresses, if it is a dual-channel image, you only need to configure the first two virtual addresses; if it is a three-channel image, you need to configure three virtual addresses. |
| time_ref  | The frame number transmitted through, in binding mode, is entered by the pre-stage                                                                                                         |
| pts       | The passthrough timestamp, in binding mode, is entered by the predecessor                                                                                                       |

【Note】

None.

【See Also】

[kd_mpi_dma_send_frame](#219-kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#2110-kd_mpi_dma_get_frame)

### 3.2 GDMA channel data type

The module has the following data types

- [GDMA_MAX_CHN_NUMS](#321-gdma_max_chn_nums)
- [k_gdma_rotation_e](#322-k_gdma_rotation_e)
- [k_pixel_format_dma_e](#323-k_pixel_format_dma_e)
- [k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)

#### 3.2.1 GDMA_MAX_CHN_NUMS

【Description】

GDMA maximum number of channels

【Definition】

```c
define GDMA_MAX_CHN_NUMS (4)
```

【Note】

None.

【See Also】

None.

#### 3.2.2 k_gdma_rotation_e

【Description】

Defines the GDMA channel rotation angle.

【Definition】

```c
typedef enum
{
    DEGREE_0,       /**< Rotate 0 degrees */
    DEGREE_90,      /**< Rotate 90 degrees */
    DEGREE_180,     /**< Rotate 180 degrees */
    DEGREE_270,     /**< Rotate 270 degrees */
} k_gdma_rotation_e;
```

【Note】

None.

【See Also】

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)

#### 3.2.3 k_pixel_format_dma_e

【Description】

Defines the GDMA image format.

【Definition】

```c
typedef enum
{
    DMA_PIXEL_FORMAT_RGB_444 = 0,
    DMA_PIXEL_FORMAT_RGB_555,
    DMA_PIXEL_FORMAT_RGB_565,
    DMA_PIXEL_FORMAT_RGB_888,

    DMA_PIXEL_FORMAT_BGR_444,
    DMA_PIXEL_FORMAT_BGR_555,
    DMA_PIXEL_FORMAT_BGR_565,
    DMA_PIXEL_FORMAT_BGR_888,

    DMA_PIXEL_FORMAT_ARGB_1555,
    DMA_PIXEL_FORMAT_ARGB_4444,
    DMA_PIXEL_FORMAT_ARGB_8565,
    DMA_PIXEL_FORMAT_ARGB_8888,

    DMA_PIXEL_FORMAT_ABGR_1555,
    DMA_PIXEL_FORMAT_ABGR_4444,
    DMA_PIXEL_FORMAT_ABGR_8565,
    DMA_PIXEL_FORMAT_ABGR_8888,

    DMA_PIXEL_FORMAT_YVU_PLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_420_16BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_444_8BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_444_10BIT,

    DMA_PIXEL_FORMAT_YUV_PLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YUV_PLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YUV_PLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YUV_400_8BIT,
    DMA_PIXEL_FORMAT_YUV_400_10BIT,
    DMA_PIXEL_FORMAT_YUV_400_12BIT,
    DMA_PIXEL_FORMAT_YUV_400_16BIT,

    DMA_PIXEL_FORMAT_YUV_PACKED_444_8BIT,
    DMA_PIXEL_FORMAT_YUV_PACKED_444_10BIT,

    /* SVP data format */
    DMA_PIXEL_FORMAT_BGR_888_PLANAR,
} k_pixel_format_dma_e;
```

#### 3.2.4 k_gdma_chn_attr_t

【Description】

Define GDMA channel properties.

【Definition】

```c
typedef struct
{
    k_u8 buffer_num;
    k_gdma_rotation_e rotation;
    k_bool x_mirror;
    k_bool y_mirror;
    k_u16 width;
    k_u16 height;
    k_u16 src_stride[3];
    k_u16 dst_stride[3];
    k_dma_mode_e work_mode;
    k_pixel_format_dma_e pixel_format;
} k_gdma_chn_attr_t;
```

【Members】

| Member name     | description                                                                                                                                                                                                                     |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| buffer_num   | The number of GDMA channel buffers, at least 1. |
| rotation     | GDMA channel rotation angle.                                                                                                                                                                                                      |
| x_mirror     | Whether the GDMA channel is horizontally mirrored                                                                                                                                                                                                |
| y_mirror     | Whether the GDMA channel is mirrored vertically                                                                                                                                                                                                |
| width        | GDMA channel width, in pixels.                                                                                                                                                                                            |
| height       | GDMA channel height, in pixels.                                                                                                                                                                                            |
| src_stride   | GDMA source data stride. If the image format is single-channel mode, only configuration is required; if the image format is dual-channel mode, `src_stride[0]` configuration is `src_stride[0]`required; `src_stride[1]`if the image format is three-channel mode, configuration `src_stride[0]`is required.`src_stride[1]``src_stride[2]`  |
| dst_stride   | Data for GDMA purposes Stride. If`dst_stride[0]` the image format is single-channel mode, only configuration is required; if the image format is dual-channel mode, `dst_stride[0]` configuration is required; `dst_stride[1]`if the image format is three-channel mode, configuration `dst_stride[0]`is required.`dst_stride[1]``dst_stride[2]` |
| work_mode    | Working mode, you can choose bound mode or unbound mode.                                                                                                                                                                               |
| pixel_format | Image format.                                                                                                                                                                                                               |

【Note】

- None.

【See Also】

- [kd_mpi_dma_set_chn_attr](#215-kd_mpi_dma_set_chn_attr)
- [kd_mpi_dma_get_chn_attr](#216-kd_mpi_dma_get_chn_attr)

### 3.3 SDMA channel data type

This module has the following data types

- [SDMA_MAX_CHN_NUMS](#331-sdma_max_chn_nums)
- [k_sdma_data_mode_e](#332-k_sdma_data_mode_e)
- [k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

#### 3.3.1 SDMA_MAX_CHN_NUMS

【Description】

SDMA maximum number of channels

【Definition】

```c
#define SDMA_MAX_CHN_NUMS (4)
```

【Note】

None.

【See Also】

None.

#### 3.3.2 k_sdma_data_mode_e

【Description】

Defines the mode in which SDMA channels transmit data

【Definition】

```c
typedef enum
{
    DIMENSION1,
    DIMENSION2,
} k_sdma_data_mode_e;
```

【Members】

| Member name   | description              |
|------------|-------------------|
| DIMENSION1 | One-dimensional DMA transfer mode |
| DIMENSION1 | 2D DMA transmission mode |

【Note】

None.

【See Also】

[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

#### 3.3.3 k_sdma_chn_attr_t

【Description】

Define SDMA channel properties.

【Definition】

```c
typedef struct
{
    k_u8 buffer_num;
    k_u32 line_size;
    k_u16 line_num;
    k_u16 line_space;
    k_sdma_data_mode_e data_mode;
    k_dma_mode_e work_mode;
} k_sdma_chn_attr_t;
```

【Members】

| Member name   | description                                                                       |
|------------|----------------------------------------------------------------------------|
| buffer_num | The number of SDMA channel buffers, at least 1.                                      |
| line_size  | The total length of the transmitted data for 1D mode and a single line of data for 2D mode. |
| line_num   | This member is not valid for 1D mode; for 2D mode, the number of rows transferred.         |
| line_space | This member is not valid for 1D mode; for 2D mode, it is the interval between rows.       |
| data_mode  | SDMA's modes for transferring data, including 1D mode and 2D mode.                              |
| work_mode  | Working mode, you can choose bound mode or unbound mode.                                 |

【Note】

None.

【See Also】

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

## 4. Error codes

### 4.1 DMA error code

Table 41

| Error code    | Macro definitions                  | description                         |
|-------------|-------------------------|------------------------------|
| 0xa00148001 | K_ERR_DMA_INVALID_DEVID | Invalid device number                 |
| 0xa00148002 | K_ERR_DMA_INVALID_CHNID | Invalid channel number                 |
| 0xa00148003 | K_ERR_DMA_ILLEGAL_PARAM | Parameter error                     |
| 0xa00148004 | K_ERR_DMA_EXIST         | The DMA device already exists             |
| 0xa00148005 | K_ERR_DMA_UNEXIST       | The DMA device does not exist               |
| 0xa00148006 | K_ERR_DMA_NULL_PTR      | Null pointer error                   |
| 0xa00148007 | K_ERR_DMA_NOT_CONFIG    | DMA has not been configured                 |
| 0xa00148008 | K_ERR_DMA_NOT_SUPPORT   | Unsupported features                 |
| 0xa00148009 | K_ERR_DMA_NOT_PERM      | Operation is not allowed                   |
| 0xa0014800c | K_ERR_DMA_NOMEM         | Failed to allocate memory, such as low system memory |
| 0xa0014800d | K_ERR_DMA_NOBUF         | BUFF is insufficient                    |
| 0xa0014800e | K_ERR_DMA_BUF_EMPTY     | BUFF is empty                    |
| 0xa0014800f | K_ERR_DMA_BUF_FULL      | BUFF is full                    |
| 0xa00148010 | K_ERR_DMA_NOTREADY      | The device is not ready                   |
| 0xa00148011 | K_ERR_DMA_BADADDR       | Wrong address                   |
| 0xa00148012 | K_ERR_DMA_BUSY          | DMA is in a busy state               |

## 5. Debugging information

### 5.1 Overview

The debug information uses the PROC file system, which can reflect the current operating status of the system in real time, and the recorded information can be used for problem location and analysis

【File Directory】

/proc/

【Document List】

| File name  | description                        |
|-----------|-----------------------------|
| umap/dma  | Record the current usage of the DMA module |

### 5.2 System Binding

#### 5.2.1 System binding debugging information

【Debugging Information】

```shell
msh /\>cat /proc/umap/dma
-------------------------------dma dev attr info---------------------------------
DevId burst_len outstanding ckg_bypass
0 0 0 0

-------------------------------dma chn 0\~3 attr info-------------------------------
ChnId rotation x_mirror y_mirror width height work_mode
0 0 false false 0 0 BIND
1 0 false false 0 0 BIND
2 0 false false 0 0 BIND
3 0 false false 0 0 BIND

-------------------------------dma chn 4\~7 attr info-------------------------------
ChnId line_size line_num line_space data_mode work_mode
4 0 0 0 1 DIMENSION BIND
5 0 0 0 1 DIMENSION BIND
6 0 0 0 1 DIMENSION BIND
7 0 0 0 1 DIMENSION BIND
```

【Debugging Information Analysis】

Record the current usage of the DMA module

【Equipment parameter description】

| parameter        | **Description**         |
|-------------|------------------|
| DevId       | Device number           |
| burst_len   | dma burst length |
| outstanding | dma outstanding  |

【GDMA channel parameter description】

| parameter      | **Description**               |
|-----------|------------------------|
| ChnId     | Channel number                 |
| rotation  | The degree of rotation               |
| x_mirror  | Whether horizontal mirroring is performed     |
| y_mirror  | Whether vertical mirroring is performed     |
| width     | Image width, in pixels |
| height    | Image height, in pixels |
| work_mode | Working mode               |

【SDMA channel parameter description】

| parameter       | **Description**                                                                   |
|------------|----------------------------------------------------------------------------|
| ChnId      | Channel number                                                                     |
| line_size  | The total length of the transmitted data for 1D mode and a single line of data for 2D mode. |
| ine_num    | This member is not valid for 1D mode; for 2D mode, the number of rows transferred.         |
| line_space | This member is not valid for 1D mode; for 2D mode, it is the interval between rows.       |
| data_mode  | SDMA's modes for transferring data, including 1D mode and 2D mode                                |
| work_mode  | Working mode, you can choose bound mode or unbound mode.                                 |

## 6. Demo description

### 6.1 Unbound mode demo

The unbound mode demo is located at /bin/sample_dma.elf, start cyclic running after executing /bin/sample_dma.elf, and press e + Enter to end the run.

The demo mainly implements the following functions:

- Use channel 0 to transport images with a resolution of 1920\*1080, 8bit, YUV400 single-channel, and output after gdma rotation of 90 degrees;
- Use channel 1 to carry images with a resolution of 1280\*720, 8bit, YUV420 dual-channel, and output after gdma rotation of 180 degrees;
- Use channel 2 to carry images with a resolution of 1280\*720, 10bit, YUV420 three-channel, and output after horizontal and vertical mirroring by gdma;
- Use channel 4 to move data, and SDMA is handled using 1D mode;
- Use channel 5 to move data, and SDMA is handled using 2D mode.

### 6.2 Binding mode demo

The binding mode demo is located at /bin/sample_dma_bind.elf, and after executing /bin/sample_dma_bind.elf, start the loop run, and press e + enter to end the run.

The demo mainly implements the following functions:

- The VVI module is used as the analog input of GSDMA pre-binding to realize the test of binding function;
- The two channels input the image with a resolution of 640\*320, 8bit, YUV400 single-channel, and the gdma is rotated 90 degrees and 180 degrees respectively.
