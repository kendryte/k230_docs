# K230 DMA API Reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for usage guidance and reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or distribute any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the design of the K230 GSDMA software, including the GSDMA driver framework and software implementation.

### Intended Audience

This document (this guide) is mainly for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                       |
|--------------|-----------------------------------|
| GDMA         | Graphic Direct Memory Access      |
| SDMA         | System Direct Memory Access       |

### Revision History

| Document Version | Modification Description                                       | Author | Date       |
|------------------|----------------------------------------------------------------|----------|------------|
| V1.0             | Initial version                                                | Liu Suntao | 2023/3/7  |
| V1.1             | Modified some descriptions of binding mode; added function interface description for frame number release. | Liu Suntao | 2023/3/31 |
| V1.2             | Replaced the data structure of the image address; added frame number passthrough function. | Liu Suntao | 2023/4/26 |
| V1.3             | Added configurable buffer functionality                        | Liu Suntao | 2023/5/31 |

## 1. Overview

### 1.1 Overview

GSDMA: DMA stands for Direct Memory Access, which copies data from one address space to another, providing high-speed data transfer between memory and memory. GDMA stands for Graphic Direct Memory Access, responsible for copying images in memory to another memory area, and can also perform image rotation and mirroring functions. SDMA stands for System Direct Memory Access, responsible for copying data in memory to another memory area, which is the traditional DMA.

The software code provides the various functions of the GSDMA hardware in the form of APIs to users, helping them quickly achieve image transfer, rotation, mirroring, 2D functions, and data transfer functions. It also implements module status information statistics and other functions.

### 1.2 Function Description

Abstract the DMA hardware as a device with eight channels, where channels 0 to 3 are GDMA channels, and channels 4 to 7 are SDMA channels.

#### 1.2.1 GDMA

Users can achieve image rotation and mirroring work through GDMA, and the main call flow is as follows:

1. Configure DMA device attributes;
1. Start the DMA device. After calling this function, the driver will automatically request VB space as the data buffer for the destination address;
1. Configure GDMA channel attributes;
1. Start the GDMA channel;
1. Users request VB space in user mode as the data buffer for the source data, and call `kd_mpi_dma_send_frame` to send the source address of the data to GDMA;
1. The driver will transfer the data from the source address to the data buffer of the destination address requested in step two;
1. Users call `kd_mpi_dma_get_frame` to get the data address in the destination address.

#### 1.2.2 SDMA

Users can achieve data transfer work through SDMA, and the main call flow is as follows:

1. Configure DMA device attributes;
1. Start the DMA device. After calling this function, the driver will automatically request VB space as the data buffer for the destination address;
1. Configure SDMA channel attributes;
1. Start the SDMA channel;
1. Users request VB space in user mode as the data buffer for the source data, and call `kd_mpi_dma_send_frame` to send the source address of the data to SDMA;
1. The driver will transfer the data from the source address to the data buffer of the destination address requested in step two;
1. Users call `kd_mpi_dma_get_frame` to get the data address in the destination address.

## 2. API Reference

### 2.1 DMA Usage

This functional module provides the following APIs:

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

**Description**:

Configure DMA device attributes

**Syntax**:

```c
k_s32 kd_mpi_dma_set_dev_attr(k_dma_dev_attr_t *attr);
```

**Parameters**:

| Parameter Name | Description                      | Input/Output |
|----------------|----------------------------------|--------------|
| attr           | Pointer to DMA device attribute structure. | Input       |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_dma_dev_attr_t](#314-k_dma_dev_attr_t)

#### 2.1.2 kd_mpi_dma_get_dev_attr

**Description**:

Get the configured DMA device attributes.

**Syntax**:

```c
k_s32 kd_mpi_dma_get_dev_attr(k_dma_dev_attr_t *attr);
```

**Parameters**:

| Parameter Name | Description                   | Input/Output |
|----------------|-------------------------------|--------------|
| attr           | Pointer to DMA device attribute structure | Input       |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You need to configure DMA device attributes before you can get DMA device attributes.

**Example**:

None

**Related Topics**:

[k_dma_dev_attr_t](#314-k_dma_dev_attr_t)

#### 2.1.3 kd_mpi_dma_start_dev

**Description**:

Start the DMA device.

**Syntax**:

```c
k_s32 kd_mpi_dma_start_dev();
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| None           | None        | None         |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You need to configure DMA device attributes before you can call this function to start DMA.

**Example**:

None

**Related Topics**:

None

#### 2.1.4 kd_mpi_dma_stop_dev

**Description**:

Stop the DMA device.

**Syntax**:

```c
kd_mpi_dma_stop_dev();
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| None           | None        | None         |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You can only call this function to stop the DMA device after starting the DMA device.

**Example**:

None

**Related Topics**:

None

#### 2.1.5 kd_mpi_dma_set_chn_attr

**Description**:

Configure DMA channel attributes.

**Syntax**:

```c
k_s32 kd_mpi_dma_set_chn_attr(k_u8 chn_num, k_dma_chn_attr_u *attr);
```

**Parameters**:

| Parameter Name | Description                                                                                                                               | Input/Output |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                                            | Input        |
| attr           | DMA channel attributes, this parameter is a union, you can choose to configure GDMA channel attributes or SDMA channel attributes. Channels 0-3 are GDMA, channels 4-7 are SDMA | Input        |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

#### 2.1.6 kd_mpi_dma_get_chn_attr

**Description**:

Get the configured DMA channel attributes.

**Syntax**:

```c
k_s32 kd_mpi_dma_get_chn_attr(k_u8 chn_num, k_dma_chn_attr_u *attr);
```

**Parameters**:

| Parameter Name | Description                                                                                                                               | Input/Output |
|----------------|-------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                                            | Input        |
| attr           | DMA channel attributes, this parameter is a union, you can choose to get GDMA channel attributes or SDMA channel attributes. Channels 0-3 are GDMA, channels 4-7 are SDMA | Output       |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You need to configure DMA channel attributes before you can get DMA channel attributes.

**Example**:

None

**Related Topics**:

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

#### 2.1.7 kd_mpi_dma_start_chn

**Description**:

Start the DMA channel.

**Syntax**:

```c
k_s32 kd_mpi_dma_start_chn(k_u8 chn_num);
```

**Parameters**:

| Parameter Name | Description  | Input/Output |
|----------------|--------------|--------------|
| chn_num        | Channel number | Input        |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You can only start the DMA channel after configuring and starting the DMA device and configuring the DMA channel attributes.

**Example**:

None

**Related Topics**:

None

#### 2.1.8 kd_mpi_dma_stop_chn

**Description**:

Pause the DMA channel.

**Syntax**:

```c
k_s32 kd_mpi_dma_stop_chn(k_u8 chn_num);
```

**Parameters**:

| Parameter Name | Description  | Input/Output |
|----------------|--------------|--------------|
| chn_num        | Channel number | Input        |

**Return Value**:

| Return Value | Description         |
|--------------|---------------------|
| 0            | Success             |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

You can only call this function to stop the DMA channel after starting the DMA channel.

**Example**:

None

**Related Topics**:

None

#### 2.1.9 kd_mpi_dma_send_frame

**Description**:

Send data from user space to the destination address.

**Syntax**:

```c
k_s32 kd_mpi_dma_send_frame(k_u8 chn_num, k_video_frame_info *df_info, k_s32 millisec);
```

**Parameters**:

| Parameter Name | Description                                                                                                    | Input/Output |
|----------------|----------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                 | Input        |
| df_info        | Address information of the data to be sent                                                                     | Input        |
| millisec       | Waiting time. When this parameter is set to -1, it is blocking; when set to 0, it is non-blocking; when set to a value greater than 0, it will wait for the corresponding time until the data is successfully sent. If it times out and still fails to send, it returns a failure. | Input        |

**Return Value**:

| Return Value | Description          |
|--------------|----------------------|
| 0            | Success              |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_video_frame_info](#316-k_video_frame_info)

#### 2.1.10 kd_mpi_dma_get_frame

**Description**:

Get the data transferred by DMA.

**Syntax**:

```c
k_s32 kd_mpi_dma_get_frame(k_u8 chn_num, k_video_frame_info *df_info, k_s32 millisec);
```

**Parameters**:

| Parameter Name | Description                                                                                                                                                                  | Input/Output |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                                                                               | Input        |
| df_info        | Address information for getting the data                                                                                                                                     | Output       |
| millisec       | Waiting time. When this parameter is set to -1, it is blocking; when set to 0, it is non-blocking; when set to a value greater than 0, it will wait for the corresponding time until the data is successfully obtained. If it times out and still fails to send, it returns a failure. | Input        |

**Return Value**:

| Return Value | Description          |
|--------------|----------------------|
| 0            | Success              |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_video_frame_info](#316-k_video_frame_info)

#### 2.1.11 kd_mpi_dma_release_frame

**Description**:

Release the obtained DMA data.

**Syntax**:

```c
k_s32 kd_mpi_dma_release_frame(k_u8 chn_num, k_video_frame_info *df_info);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| chn_num        | Channel number     | Input        |
| df_info        | Data to be released | Input        |

**Return Value**:

| Return Value | Description          |
|--------------|----------------------|
| 0            | Success              |
| Non-zero     | Failure, see error codes for details |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dma_api.h
- Library file: libdma.a

**Notes**:

- In the current design, the DMA output buffer is 3. If you obtain 3 frames of data without calling this function to release them, you cannot continue to input data. Therefore, users should release the data promptly after obtaining and using it.

**Example**:

None

**Related Topics**:

[k_video_frame_info](#316-k_video_frame_info)

## 3 Data Types

### 3.1 Common Data Types

#### 3.1.1 DMA_MAX_DEV_NUMS

**Description**:

Maximum number of DMA devices

**Definition**:

```c
#define DMA_MAX_DEV_NUMS (1)
```

**Notes**:

None

**Related Data Types and Interfaces**:

None

#### 3.1.2 DMA_MAX_CHN_NUMS

**Description**:

Maximum number of DMA channels

**Definition**:

```c
#define DMA_MAX_CHN_NUMS (8)
```

**Notes**:

None

**Related Data Types and Interfaces**:

None

#### 3.1.3 k_dma_mode_e

**Description**:

Defines the DMA working mode.

**Definition**:

```c
typedef enum
{
    DMA_BIND,
    DMA_UNBIND,
} k_dma_mode_e;
```

**Members**:

| Member Name | Description        |
|-------------|--------------------|
| BIND        | Binding mode       |
| UNBIND      | Non-binding mode   |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

#### 3.1.4 k_dma_dev_attr_t

**Description**:

Defines the DMA device attributes.

**Definition**:

```c
typedef struct
{
    k_u8 burst_len;
    k_u8 outstanding;
    k_bool ckg_bypass;
} k_dma_dev_attr_t;
```

**Members**:

| Member Name | Description                  |
|-------------|------------------------------|
| burst_len   | Configures the DMA burst length |
| outstanding | Configures the DMA outstanding |
| ckg_bypass  | Configures the clock gate bypass |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dma_set_dev_attr](#211-kd_mpi_dma_set_dev_attr)
[kd_mpi_dma_get_dev_attr](#212-kd_mpi_dma_get_dev_attr)

#### 3.1.5 k_dma_chn_attr_u

**Description**:

Defines the DMA channel attributes.

**Definition**:

```c
typedef union
{
    k_gdma_chn_attr_t gdma_attr;
    k_sdma_chn_attr_t sdma_attr;
} k_dma_chn_attr_u;
```

**Members**:

| Member Name | Description         |
|-------------|---------------------|
| gdma_attr   | GDMA channel attributes |
| sdma_attr   | SDMA channel attributes |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)
[kd_mpi_dma_set_chn_attr](#215-kd_mpi_dma_set_chn_attr)
[kd_mpi_dma_get_chn_attr](#216-kd_mpi_dma_get_chn_attr)

#### 3.1.6 k_video_frame_info

**Description**:

Defines the DMA data address.

**Definition**:

```c
typedef struct
{
    k_video_frame v_frame;  /**< Video picture frame */
    k_u32 pool_id;          /**< VB pool ID */
    k_mod_id mod_id;        /**< Logical unit for generating video frames */
} k_video_frame_info;
```

**Members**:

| Member Name | Description                         |
|-------------|-------------------------------------|
| v_frame     | Timestamp, valid in binding mode    |
| pool_id     | Pool ID of the data VB pool         |
| mod_id      | Module ID                           |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dma_send_frame](#219-kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#2110-kd_mpi_dma_get_frame)
[kd_mpi_dma_release_frame](#2111-kd_mpi_dma_release_frame)

#### 3.1.7 k_video_frame

**Description**:

Defines the DMA data address. Uses the common data structure k_video_frame, only part of the members are used.

**Definition**:

```c
typedef struct
{
    k_u64 phys_addr[3];
    k_u64 virt_addr[3];
    k_u32 time_ref;
    k_u64 pts;
} k_video_frame;
```

**Members**:

| Member Name | Description                                                                                                                                 |
|-------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| phys_addr   | Physical address of the image. If it is a single-channel image, only configure the first physical address; if it is a dual-channel image, configure the first two physical addresses; if it is a three-channel image, configure all three physical addresses. |
| virt_addr   | Virtual address of the image. If it is a single-channel image, only configure the first virtual address; if it is a dual-channel image, configure the first two virtual addresses; if it is a three-channel image, configure all three virtual addresses. |
| time_ref    | Frame number for passthrough, valid in binding mode                                                                                          |
| pts         | Timestamp for passthrough, valid in binding mode                                                                                            |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dma_send_frame](#219-kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#2110-kd_mpi_dma_get_frame)

### 3.2 GDMA Channel Data Types

This module has the following data types:

- [GDMA_MAX_CHN_NUMS](#321-gdma_max_chn_nums)
- [k_gdma_rotation_e](#322-k_gdma_rotation_e)
- [k_pixel_format_dma_e](#323-k_pixel_format_dma_e)
- [k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)

#### 3.2.1 GDMA_MAX_CHN_NUMS

**Description**:

Maximum number of GDMA channels

**Definition**:

```c
#define GDMA_MAX_CHN_NUMS (4)
```

**Notes**:

None

**Related Data Types and Interfaces**:

None

#### 3.2.2 k_gdma_rotation_e

**Description**:

Defines the GDMA channel rotation angle.

**Definition**:

```c
typedef enum
{
    DEGREE_0,       /**< Rotate 0 degrees */
    DEGREE_90,      /**< Rotate 90 degrees */
    DEGREE_180,     /**< Rotate 180 degrees */
    DEGREE_270,     /**< Rotate 270 degrees */
} k_gdma_rotation_e;
```

**Notes**:

None

**Related Data Types and Interfaces**:

[k_gdma_chn_attr_t](#324-k_gdma_chn_attr_t)

#### 3.2.3 k_pixel_format_dma_e

**Description**:

Defines the GDMA image format.

**Definition**:

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

**Description**:

Defines the GDMA channel attributes.

**Definition**:

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

**Members**:

| Member Name  | Description                                                                                                                                                                                                                     |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| buffer_num   | Number of GDMA channel buffers, at least 1.                                                                                                                                                                                     |
| rotation     | GDMA channel rotation angle.                                                                                                                                                                                                    |
| x_mirror     | Whether the GDMA channel performs horizontal mirroring.                                                                                                                                                                         |
| y_mirror     | Whether the GDMA channel performs vertical mirroring.                                                                                                                                                                           |
| width        | GDMA channel width, in pixels.                                                                                                                                                                                                  |
| height       | GDMA channel height, in pixels.                                                                                                                                                                                                 |
| src_stride   | GDMA source data stride. If the image format is single-channel mode, configure `src_stride[0]` only; if it is dual-channel mode, configure `src_stride[0]` and `src_stride[1]`; if it is three-channel mode, configure `src_stride[0]`, `src_stride[1]`, and `src_stride[2]`. |
| dst_stride   | GDMA destination data stride. If the image format is single-channel mode, configure `dst_stride[0]` only; if it is dual-channel mode, configure `dst_stride[0]` and `dst_stride[1]`; if it is three-channel mode, configure `dst_stride[0]`, `dst_stride[1]`, and `dst_stride[2]`. |
| work_mode    | Work mode, can choose binding mode or non-binding mode.                                                                                                                                                                         |
| pixel_format | Image format.                                                                                                                                                                                                                   |

**Notes**:

None

**Related Data Types and Interfaces**:

- [kd_mpi_dma_set_chn_attr](#215-kd_mpi_dma_set_chn_attr)
- [kd_mpi_dma_get_chn_attr](#216-kd_mpi_dma_get_chn_attr)

### 3.3 SDMA Channel Data Types

This module has the following data types:

- [SDMA_MAX_CHN_NUMS](#331-sdma_max_chn_nums)
- [k_sdma_data_mode_e](#332-k_sdma_data_mode_e)
- [k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

#### 3.3.1 SDMA_MAX_CHN_NUMS

**Description**:

Maximum number of SDMA channels

**Definition**:

```c
#define SDMA_MAX_CHN_NUMS (4)
```

**Notes**:

None

**Related Data Types and Interfaces**:

None

### 3.3.2 k_sdma_data_mode_e

**Description**:

Defines the data transfer mode of the SDMA channel.

**Definition**:

```c
typedef enum
{
    DIMENSION1,
    DIMENSION2,
} k_sdma_data_mode_e;
```

**Members**:

| Member Name | Description              |
|-------------|--------------------------|
| DIMENSION1  | 1D DMA transfer mode     |
| DIMENSION2  | 2D DMA transfer mode     |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_sdma_chn_attr_t](#333-k_sdma_chn_attr_t)

### 3.3.3 k_sdma_chn_attr_t

**Description**:

Defines the attributes of the SDMA channel.

**Definition**:

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

**Members**:

| Member Name | Description                                                                 |
|-------------|----------------------------------------------------------------------------|
| buffer_num  | Number of SDMA channel buffers, at least 1.                                 |
| line_size   | For 1D mode, it is the total length of the transfer data; for 2D mode, it is the length of a single line of data. |
| line_num    | For 1D mode, this member is invalid; for 2D mode, it is the number of lines to transfer. |
| line_space  | For 1D mode, this member is invalid; for 2D mode, it is the space between lines. |
| data_mode   | SDMA data transfer mode, includes 1D mode and 2D mode.                     |
| work_mode   | Work mode, can choose binding mode or non-binding mode.                     |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dma_chn_attr_u](#315-k_dma_chn_attr_u)

## 4. Error Codes

### 4.1 DMA Error Codes

Table 41

| Error Code   | Macro Definition           | Description                   |
|--------------|----------------------------|-------------------------------|
| 0xa00148001  | K_ERR_DMA_INVALID_DEVID    | Invalid device ID             |
| 0xa00148002  | K_ERR_DMA_INVALID_CHNID    | Invalid channel ID            |
| 0xa00148003  | K_ERR_DMA_ILLEGAL_PARAM    | Illegal parameter             |
| 0xa00148004  | K_ERR_DMA_EXIST            | DMA device already exists     |
| 0xa00148005  | K_ERR_DMA_UNEXIST          | DMA device does not exist     |
| 0xa00148006  | K_ERR_DMA_NULL_PTR         | Null pointer error            |
| 0xa00148007  | K_ERR_DMA_NOT_CONFIG       | DMA not configured            |
| 0xa00148008  | K_ERR_DMA_NOT_SUPPORT      | Unsupported function          |
| 0xa00148009  | K_ERR_DMA_NOT_PERM         | Operation not permitted       |
| 0xa0014800c  | K_ERR_DMA_NOMEM            | Memory allocation failed, e.g., insufficient system memory |
| 0xa0014800d  | K_ERR_DMA_NOBUF            | Insufficient buffer           |
| 0xa0014800e  | K_ERR_DMA_BUF_EMPTY        | Buffer is empty               |
| 0xa0014800f  | K_ERR_DMA_BUF_FULL         | Buffer is full                |
| 0xa00148010  | K_ERR_DMA_NOTREADY         | Device not ready              |
| 0xa00148011  | K_ERR_DMA_BADADDR          | Invalid address               |
| 0xa00148012  | K_ERR_DMA_BUSY             | DMA is busy                   |

## 5. Debug Information

### 5.1 Overview

Debug information uses the proc file system, which can reflect the current system running status in real-time. The recorded information can be used for problem localization and analysis.

**File Directory**:

/proc/

**File List**:

| File Name  | Description                 |
|------------|-----------------------------|
| umap/dma   | Records the current usage of the DMA module |

### 5.2 System Binding

#### 5.2.1 System Binding Debug Information

**Debug Information**:

```shell
msh />cat /proc/umap/dma
-------------------------------dma dev attr info---------------------------------
DevId burst_len outstanding ckg_bypass
0 0 0 0

-------------------------------dma chn 0~3 attr info-------------------------------
ChnId rotation x_mirror y_mirror width height work_mode
0 0 false false 0 0 BIND
1 0 false false 0 0 BIND
2 0 false false 0 0 BIND
3 0 false false 0 0 BIND

-------------------------------dma chn 4~7 attr info-------------------------------
ChnId line_size line_num line_space data_mode work_mode
4 0 0 0 1 DIMENSION BIND
5 0 0 0 1 DIMENSION BIND
6 0 0 0 1 DIMENSION BIND
7 0 0 0 1 DIMENSION BIND
```

**Debug Information Analysis**:

Records the current usage of the DMA module.

**Device Parameter Description**:

| Parameter    | **Description**:          |
|--------------|--------------------------|
| DevId        | Device ID                |
| burst_len    | DMA burst length         |
| outstanding  | DMA outstanding          |

**GDMA Channel Parameter Description**:

| Parameter   | **Description**:            |
|-------------|----------------------------|
| ChnId       | Channel ID                 |
| rotation    | Rotation degree            |
| x_mirror    | Whether horizontal mirroring is applied |
| y_mirror    | Whether vertical mirroring is applied   |
| width       | Image width in pixels       |
| height      | Image height in pixels      |
| work_mode   | Work mode                   |

**SDMA Channel Parameter Description**:

| Parameter   | **Description**:                                                                 |
|-------------|---------------------------------------------------------------------------------|
| ChnId       | Channel ID                                                                       |
| line_size   | For 1D mode, it is the total length of the transfer data; for 2D mode, it is the length of a single line of data. |
| line_num    | For 1D mode, this member is invalid; for 2D mode, it is the number of lines to transfer. |
| line_space  | For 1D mode, this member is invalid; for 2D mode, it is the space between lines. |
| data_mode   | SDMA data transfer mode, includes 1D mode and 2D mode.                           |
| work_mode   | Work mode, can choose binding mode or non-binding mode.                          |

## 6. Demo Description

### 6.1 Non-binding Mode Demo

The non-binding mode demo is located at /bin/sample_dma.elf. After executing /bin/sample_dma.elf, it starts running in a loop. Press 'e' + Enter to stop running.

The demo mainly implements the following functions:

- Use channel 0 to transfer an image with a resolution of 1920x1080, 8-bit, YUV400 single channel, and output it after GDMA rotates it by 90 degrees.
- Use channel 1 to transfer an image with a resolution of 1280x720, 8-bit, YUV420 dual channel, and output it after GDMA rotates it by 180 degrees.
- Use channel 2 to transfer an image with a resolution of 1280x720, 10-bit, YUV420 triple channel, and output it after GDMA performs horizontal and vertical mirroring.
- Use channel 4 to transfer data using SDMA in 1D mode.
- Use channel 5 to transfer data using SDMA in 2D mode.

### 6.2 Binding Mode Demo

The binding mode demo is located at /bin/sample_dma_bind.elf. After executing /bin/sample_dma_bind.elf, it starts running in a loop. Press 'e' + Enter to stop running.

The demo mainly implements the following functions:

- Use the VVI module as the front-end bound simulated input for GSDMA to test the binding function.
- Two channels respectively input images with a resolution of 640x320, 8-bit, YUV400 single channel, and output them after GDMA rotates them by 90 degrees and 180 degrees respectively.
