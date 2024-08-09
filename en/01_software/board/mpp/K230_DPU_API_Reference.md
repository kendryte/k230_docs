# K230 DPU API Reference

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

This document primarily introduces the usage of K230 DPU software, including the usage of DPU API and demo introductions.

### Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                                |
|--------------|--------------------------------------------|
| DPU          | Depth Process Unit                         |
| LCN          | Local Contrast Normalization               |

### Revision History

| Document Version | Modification Description                                                                 | Author | Date       |
|------------------|------------------------------------------------------------------------------------------|----------|------------|
| v1.0             | Initial version                                                                          | Liu Suntao | 2023/3/30  |
| v1.1             | Added the interface function for setting the reference image after offline processing [kd_mpi_dpu_set_processed_ref_image](#217-kd_mpi_dpu_set_processed_ref_image); added module debugging information. | Liu Suntao | 2023/4/20  |
| V1.2             | Added configurable buffer functionality                                                  | Liu Suntao | 2023/5/31  |

## 1. Overview

### 1.1 Overview

The DPU is mainly responsible for the depth calculation of 3D structured light, providing depth information for 3D facial recognition.

### 1.2 Function Description

#### 1.2.1 Binding Mode Call Process

![Diagram](../../../../zh/01_software/board/mpp/images/b85b814d3911bf8b3802ba97751ff941.png)

#### 1.2.2 Non-Binding Mode Call Process

![Diagram](../../../../zh/01_software/board/mpp/images/dca3cfa887a526c493abced31b59afd2.png)

## 2. API Reference

### 2.1 DPU Usage

This module provides the following APIs:

- [kd_mpi_dpu_init](#211-kd_mpi_dpu_init)
- [kd_mpi_dpu_delete](#212-kd_mpi_dpu_delete)
- [kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)
- [kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)
- [kd_mpi_dpu_get_dev_attr](#215-kd_mpi_dpu_get_dev_attr)
- [kd_mpi_dpu_set_ref_image](#216-kd_mpi_dpu_set_ref_image)
- [kd_mpi_dpu_set_processed_ref_image](#217-kd_mpi_dpu_set_processed_ref_image)
- [kd_mpi_dpu_set_template_image](#218-kd_mpi_dpu_set_template_image)
- [kd_mpi_dpu_start_dev](#219-kd_mpi_dpu_start_dev)
- [kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr)
- [kd_mpi_dpu_get_chn_attr](#2111-kd_mpi_dpu_get_chn_attr)
- [kd_mpi_dpu_start_chn](#2112-kd_mpi_dpu_start_chn)
- [kd_mpi_dpu_stop_chn](#2113-kd_mpi_dpu_stop_chn)
- [kd_mpi_dpu_send_frame](#2114-kd_mpi_dpu_send_frame)
- [kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)
- [kd_mpi_dpu_release_frame](#2116-kd_mpi_dpu_release_frame)

#### 2.1.1 kd_mpi_dpu_init

**Description**:

Initialize the DPU device.

**Syntax**:

```c
k_s32 kd_mpi_dpu_init(k_dpu_init_t *init);
```

**Parameters**:

| Parameter Name | Description                    | Input/Output |
|----------------|--------------------------------|--------------|
| init           | Pointer to the structure for initializing the DPU device. | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_dpu_init_t](#311-k_dpu_init_t)

#### 2.1.2 kd_mpi_dpu_delete

**Description**:

Delete the initialized DPU device.

**Syntax**:

```c
k_s32 kd_mpi_dpu_delete();
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| None           | None        | None         |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

This function should be called after the DPU device has been initialized.

**Example**:

None

**Related Topics**:

None

#### 2.1.3 kd_mpi_dpu_parse_file

**Description**:

Parse DPU configuration parameters from the DPU configuration file.

**Syntax**:

```c
k_s32 kd_mpi_dpu_parse_file(const k_char *param_path, k_dpu_dev_param_t *param, k_dpu_lcn_param_t *lcn_param, k_dpu_ir_param_t *ir_param, k_dpu_user_space_t *g_temp_space);
```

**Parameters**:

| Parameter Name | Description                                                                                     | Input/Output |
|----------------|-------------------------------------------------------------------------------------------------|--------------|
| param_path     | Path to the configuration file                                                                  | Input        |
| param          | Pointer to the structure for DPU device parameters, the parsed device parameters are stored here | Output       |
| lcn_param      | Pointer to the structure for LCN channel parameters, the parsed channel parameters are stored here | Output       |
| ir_param       | Pointer to the structure for IR channel parameters, the parsed channel parameters are stored here | Output       |
| g_temp_space   | Pointer to the template image structure, the parsed template image's starting address is stored here | Output       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- DPU device parameters include long-cycle and short-cycle parameters.
- lcn_param and ir_param are subsets of DPU device parameters. If the DPU device parameters are already configured, these two channel parameters can be ignored. If you need to change the parameters in these two channel parameter structures, you can either change the channel parameters and then call kd_mpi_dpu_set_chn_attr to make the changes effective, or change the device parameters and then call kd_mpi_dpu_set_dev_attr to make the changes effective. If only the channel parameters are changed, calling kd_mpi_dpu_set_chn_attr is more efficient.
- The template image structure contains the virtual and physical addresses of the parsed template image, as well as the size of the template image.

**Example**:

None

**Related Topics**:

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)

#### 2.1.4 kd_mpi_dpu_set_dev_attr

**Description**:

Configure DPU device attributes.

**Syntax**:

```c
k_s32 kd_mpi_dpu_set_dev_attr(k_dpu_dev_attr_t *attr);
```

**Parameters**:

| Parameter Name | Description     | Input/Output |
|----------------|-----------------|--------------|
| attr           | DPU device attributes | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- This function should be called after the DPU device has been initialized to configure DPU device attributes.
- When configuring DPU device attributes for the first time, attr's tytz_temp_recfg and align_depth_recfg should be set to K_TRUE to load the corresponding parameters into the DPU. For subsequent changes to DPU device attributes, if the long-cycle parameters have not changed, setting these two members to K_FALSE can save the time for the DPU to reload the long-cycle parameters.

**Example**:

None

**Related Topics**:

[k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)

#### 2.1.5 kd_mpi_dpu_get_dev_attr

**Description**:

Get DPU device attributes.

**Syntax**:

```c
k_s32 kd_mpi_dpu_get_dev_attr(k_dpu_dev_attr_t *attr);
```

**Parameters**:

| Parameter Name | Description     | Input/Output |
|----------------|-----------------|--------------|
| attr           | DPU device attributes | Output      |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)

#### 2.1.6 kd_mpi_dpu_set_ref_image

**Description**:

Configure DPU reference image.

**Syntax**:

```c
k_s32 kd_mpi_dpu_set_ref_image(const k_char *ref_path);
```

**Parameters**:

| Parameter Name | Description    | Input/Output |
|----------------|----------------|--------------|
| ref_path       | Reference image path | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- This function should be called after configuring DPU device attributes to configure the reference image.

**Example**:

None

**Related Topics**:

None

#### 2.1.7 kd_mpi_dpu_set_processed_ref_image

**Description**:

Configure the offline processed DPU reference image.

**Syntax**:

```c
k_s32 kd_mpi_dpu_set_processed_ref_image(const k_char *ref_path);
```

**Parameters**:

| Parameter Name | Description          | Input/Output |
|----------------|----------------------|--------------|
| ref_path       | Processed reference image path | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- This function should be called after configuring DPU device attributes to configure the reference image. The configured reference image should be pre-processed offline, and calling this function can save about 70ms compared to [kd_mpi_dpu_set_ref_image](#216-kd_mpi_dpu_set_ref_image).

**Example**:

None

**Related Topics**:

None

#### 2.1.8 kd_mpi_dpu_set_template_image

**Description**:

Configure DPU template image.

**Syntax**:

```c
k_s32 kd_mpi_dpu_set_template_image(k_dpu_user_space_t *temp_space);
```

**Parameters**:

| Parameter Name | Description      | Input/Output |
|----------------|------------------|--------------|
| temp_space     | Template image structure. | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- This function should be called after configuring DPU device attributes to configure the template image.
- temp_space should be passed as a parameter during [kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file) to obtain template image information from the configuration file.

**Example**:

None

**Related Topics**:

[k_dpu_user_space_t](#315-k_dpu_user_space_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 2.1.9 kd_mpi_dpu_start_dev

**Description**:

Start the DPU device.

**Syntax**:

```c
k_s32 kd_mpi_dpu_start_dev();
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| None           | None        | None         |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

None

**Example**:

None

**Related Topics**:

None

#### 2.1.10 kd_mpi_dpu_set_chn_attr

**Description**:

Configure DPU channel attributes.

**Syntax**:

```c
k_s32 kd_mpi_dpu_set_chn_attr(k_dpu_chn_lcn_attr_t *lcn_attr, k_dpu_chn_ir_attr_t *ir_attr);
```

**Parameters**:

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| lcn_attr       | Speckle image channel attributes. | Input       |
| ir_attr        | Infrared image channel attributes. | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- The current DPU device has two channels: 0 and 1. Configure `lcn_attr->chn_num` and `ir_attr->chn_num` (if the infrared image channel is enabled) to specify the input and output channels for the speckle and infrared images, respectively.
- After initially starting the DPU device [kd_mpi_dpu_start_dev](#219-kd_mpi_dpu_start_dev), this function should be called to configure channel attributes. The speckle image channel must be configured, while the infrared image channel can be left unconfigured (set to NULL) if it is not enabled.
- During operation, if only one channel's attributes need to be changed, only the structure for that channel needs to be passed in, and the other channel's parameter can be NULL. Both channels' parameters can also be passed in simultaneously. If both channels' parameters are NULL, the configuration will not take effect.

**Example**:

None

**Related Topics**:

[k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)
[k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t)

#### 2.1.11 kd_mpi_dpu_get_chn_attr

**Description**:

Get DPU channel attributes.

**Syntax**:

```c
k_s32 kd_mpi_dpu_get_chn_attr(k_dpu_chn_lcn_attr_t *lcn_attr, k_dpu_chn_ir_attr_t *ir_attr);
```

**Parameters**:

| Parameter Name | Description           | Input/Output |
|----------------|-----------------------|--------------|
| lcn_attr       | Speckle image channel attributes. | Output      |
| ir_attr        | Infrared image channel attributes. | Output      |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

None

**Example**:

None

**Related Topics**:

[k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)
[k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t)

#### 2.1.12 kd_mpi_dpu_start_chn

**Description**:

Start the DPU channel.

**Syntax**:

```c
k_s32 kd_mpi_dpu_start_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn_num        | Channel number | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- The channel number should be 0 or 1.

**Example**:

None

**Related Topics**:

None

#### 2.1.13 kd_mpi_dpu_stop_chn

**Description**:

Stop the DPU channel.

**Syntax**:

```c
k_s32 kd_mpi_dpu_stop_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|----------------|-------------|--------------|
| chn_num        | Channel number | Input       |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- The channel number should be 0 or 1.

**Example**:

None

**Related Topics**:

None

#### 2.1.14 kd_mpi_dpu_send_frame

**Description**:

In non-binding mode, send a frame of data to the DPU.

**Syntax**:

```c
k_s32 kd_mpi_dpu_send_frame(k_u32 chn_num, k_u64 addr, k_s32 s32_millisec);
```

**Parameters**:

| Parameter Name | Description                                                                                                                                                                                        | Input/Output |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                                                                                                     | Input        |
| addr           | Physical address of the data to be sent                                                                                                                                                            | Input        |
| s32_millisec   | Wait time. When this parameter is set to -1, it is blocking mode, and it will return only after the sending is successful; when this parameter is set to 0, it is non-blocking mode, and it will return immediately if the sending is successful, and return other values immediately if the sending fails. For detailed failure information, refer to [DPU error codes](#41-dpu-error-codes). | Input        |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- If both speckle and infrared image channels are enabled, the infrared and speckle images must be strictly interleaved when inputting.

**Example**:

None

**Related Topics**:

None

#### 2.1.15 kd_mpi_dpu_get_frame

**Description**:

Get a frame of data from the DPU.

**Syntax**:

```c
k_s32 kd_mpi_dpu_get_frame(k_u32 chn_num, k_dpu_chn_result_u *result, k_s32 s32_millisec);
```

**Parameters**:

| Parameter Name | Description                                                                                                                                                                                                     | Input/Output |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------|
| chn_num        | Channel number                                                                                                                                                                                                  | Input        |
| result         | DPU output result union, its member variables are `k_dpu_chn_lcn_result_t` and `k_dpu_chn_ir_result_t`. The user should decide which member to use as the output result for this channel based on the configuration in [kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr). | Output       |
| s32_millisec   | Wait time. When this parameter is set to -1, it is blocking mode, and it will return only after the fetching is successful; when this parameter is set to 0, it is non-blocking mode, and it will return immediately if the fetching is successful, and return other values immediately if the fetching fails. For detailed failure information, refer to [DPU error codes](#41-dpu-error-codes).  | Input        |

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- If both infrared and speckle image channels are enabled, make sure to retrieve the output results from both channels in a timely manner, otherwise the results in the buffer will overflow, causing an inability to continue inputting.

**Example**:

None

**Related Topics**:

[k_dpu_chn_result_u](#319-k_dpu_chn_result_u)
[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[k_dpu_disp_out_t](#3112-k_dpu_disp_out_t)
[k_dpu_depth_out_t](#3113-k_dpu_depth_out_t)
[k_dpu_ir_out_t](#3114-k_dpu_ir_out_t)
[k_dpu_qlt_out_t](#3115-k_dpu_qlt_out_t)

#### 2.1.16 kd_mpi_dpu_release_frame

**Description**:

In non-binding mode, release the obtained result.

**Syntax**:

k_s32 kd_mpi_dpu_release_frame();

**Parameters**:

None

**Return Value**:

| Return Value | Description            |
|--------------|------------------------|
| 0            | Success                |
| Non-zero     | Failure, see error code |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

**Notes**:

- This function will release the data in the buffer sequentially, with the earliest generated result being released first. The DPU buffer is currently set to 3, so please release the result obtained from [kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame) as soon as possible after use.

**Example**:

None

**Related Topics**:

None

## 3. Data Types

### 3.1 public data types

This module has the following data types:

- [k_dpu_init_t](#311-k_dpu_init_t)
- [k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
- [k_dpu_lcn_param_t](#313-k_dpu_lcn_param_t)
- [k_dpu_ir_param_t](#314-k_dpu_ir_param_t)
- [k_dpu_user_space_t](#315-k_dpu_user_space_t)
- [k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)
- [k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)
- [k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t)
- [k_dpu_chn_result_u](#319-k_dpu_chn_result_u)
- [k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
- [k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
- [k_dpu_disp_out_t](#3112-k_dpu_disp_out_t)
- [k_dpu_depth_out_t](#3113-k_dpu_depth_out_t)
- [k_dpu_ir_out_t](#3114-k_dpu_ir_out_t)
- [k_dpu_qlt_out_t](#3115-k_dpu_qlt_out_t)

#### 3.1.1 k_dpu_init_t

**Description**:

Initialize the data structure of DPU device

**Definition**:

```c
typedef struct {
    k_u32 start_num;
    k_u32 buffer_num;
} k_dpu_init_t;
```

**Members**:

| Member Name  | Description                                                |
|-----------|-----------------------------------------------------|
| start_num | Start frame number of DPU   |
| buffer_num| Count of DPU caching buffer, at least 1                  |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dpu_init](#211-kd_mpi_dpu_init)

#### 3.1.2 k_dpu_dev_param_t

**Description**:

DPU device parameter structure.

**Definition**:

```c
typedef struct
{
    k_dpu_long_parameter_t lpp;
    k_dpu_short_parameter_t spp;
} k_dpu_dev_param_t;
```

**Members**:

| Member Name | Description                 |
|----------|----------------------|
| lpp      | DPU Long Period Parameter Structure  |
| spp      | DPU Short Period Parameter Structure |

**Notes**:

- When the user needs to change the values in the long period parameters, they should use the virtual address member variable.

**Related Data Types and Interfaces**:

[k_dpu_long_parameter_t](#321-k_dpu_long_parameter_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.3 k_dpu_lcn_param_t

**Description**:

structure parameters of speckle image channel.

**Definition**:

```c
typedef struct {
    k_u8 matching_length_left_p0;
    k_u8 matching_length_right_p0;

    float image_check_match_threshold;
    float depth_p1;
    float depth_p2;
    float depth_precision;
} k_dpu_lcn_param_t;
```

**Members**:

| Member Name                 | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| matching_length_left_p0     | Coarse search: range of disparity calculation to the left, value: 0~256, integer |
| matching_length_right_p0    | Coarse search: range of disparity calculation to the right, value: 0~256, integer |
| image_check_match_threshold | Speckle image quality evaluation: template matching threshold, range: 0.0~1.0, float: 0.01 precision |
| depth_p1                    | Disparity to depth: depth value calculation coefficient p1, range: 0.0~50000.0, float: 0.01 precision |
| depth_p2                    | Disparity to depth: depth value calculation coefficient p2, range: -5.0~100.0, float: 0.01 precision |
| depth_precision             | Disparity to depth: depth value precision (multiplier), range: 0.0~100.0, float: 0.1 precision |

**Notes**:

- This channel structure parameter is a subset of the device structure parameters. If the device parameters have already been configured and the channel parameters are the same as the device parameters, the channel parameters do not need to be configured.

**Related Data Types and Interfaces**:

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.4 k_dpu_ir_param_t

**Description**:

Infrared image channel parameter structure.

**Definition**:

```c
typedef struct {
    float depth_k1;
    float depth_k2;
    float tz;
} k_dpu_ir_param_t;
```

**Members**:

| Member Name | Description |
|-------------|-------------|
| depth_k1    | Directly corresponds to a register. Tri-image alignment: depth value calculation coefficient k1, range: 2e-4~1e-2, float: 1e-5 precision |
| depth_k2    | Directly corresponds to a register. Tri-image alignment: depth value calculation coefficient k2, range: 0.5~1.5, float: 0.001 precision |
| tz          | Directly corresponds to a register. Tri-image alignment: projector z-direction offset (millimeters), range: -5.0~5.0, float: 0.001 precision |

**Notes**:

- This channel structure parameter is a subset of the device structure parameters. If the device parameters have already been configured and the channel parameters are the same as the device parameters, the channel parameters do not need to be configured.

**Related Data Types and Interfaces**:

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.5 k_dpu_user_space_t

**Description**:

User template image structure parameters.

**Definition**:

```c
typedef struct {
    k_bool used;
    k_u32 size;
    k_u64 phys_addr;
    void *virt_addr;
} k_dpu_user_space_t;
```

**Members**:

| Member Name  | Description                   |
|--------------|-------------------------------|
| used         | Not relevant to the user      |
| size         | Size of the user template image |
| phys_addr    | Physical address of the template image |
| virt_addr    | Virtual address of the template image |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.6 k_dpu_dev_attr_t

**Description**:

Configuration structure for DPU device attributes.

**Definition**:

```c
typedef struct {
    k_dpu_mode_e mode;
    k_bool tytz_temp_recfg;
    k_bool align_depth_recfg;
    k_bool ir_never_open;
    k_u32 param_valid;
    k_dpu_dev_param_t dev_param;
} k_dpu_dev_attr_t;
```

**Members**:

| Member Name          | Description                                                                                                                     |
|----------------------|---------------------------------------------------------------------------------------------------------------------------------|
| mode                 | DPU operating mode, including binding mode and non-binding mode.                                                                |
| tytz_temp_recfg      | Whether to update and load SAD temperature compensation parameters and TyTz row compensation calculations. When this flag is K_FALSE, it indicates no update; when K_TRUE, it indicates an update. |
| align_depth_recfg    | Whether to update and load tri-image alignment/depth calculation parameters. When this flag is K_FALSE, it indicates no update; when K_TRUE, it indicates an update. |
| ir_never_open        | The vb pool is configured when the DPU device is started and released when the DPU device is paused. Its size is initialized when the device is started, so space is reserved for depth/disparity images, infrared output, quality check, coarse and fine column disparity, and initial row-column disparity. Users can choose whether to enable tri-image alignment during the usage cycle via dev_param.spp.flag_align. If there will be no infrared image output during the entire usage cycle, there is no need to reserve space for infrared images. Configuring as K_TRUE indicates no need to reserve space for infrared image output, configuring as K_FALSE indicates the need to reserve space. |
| param_valid          | When configuring DPU device attributes, set this member to any non-zero value. When the device attributes take effect, the output result of the corresponding frame will return this arbitrary value. |
| dev_param            | DPU device parameter structure.                                                                                                  |

**Notes**:

- When configuring the DPU device attributes for the first time, tytz_temp_recfg and align_depth_recfg should be set to K_TRUE to load the corresponding parameters into the DPU.

**Related Data Types and Interfaces**:

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)

#### 3.1.7 k_dpu_chn_lcn_attr_t

**Description**:

Configuration structure for speckle image channel attributes.

**Definition**:

```c
typedef struct {
    k_u8 param_valid;
    k_s32 chn_num;
    k_dpu_lcn_param_t lcn_param;
} k_dpu_chn_lcn_attr_t;
```

**Members**:

| Member Name    | Description                                                                                         |
|----------------|-----------------------------------------------------------------------------------------------------|
| param_valid    | When configuring speckle image channel attributes, set this member to any non-zero value. When the device attributes take effect, the output result of the corresponding frame will return this arbitrary value. |
| chn_num        | Channel number. The current DPU device has two channels. Users can set this channel number to 0 or 1. The speckle image channel will input and output on the corresponding channel. If the infrared image channel is enabled, this channel number should be different from the infrared image channel number. |
| lcn_param      | Speckle image channel parameters.                                                                   |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr)

#### 3.1.8 k_dpu_chn_ir_attr_t

**Description**:

Configuration structure for infrared image channel attributes.

**Definition**:

```c
typedef struct {
    k_u8 param_valid;
    k_s32 chn_num;
    k_dpu_ir_param_t ir_param;
} k_dpu_chn_ir_attr_t;
```

**Members**:

| Member Name    | Description                                                                                       |
|----------------|---------------------------------------------------------------------------------------------------|
| param_valid    | When configuring infrared image channel attributes, set this member to any non-zero value. When the device attributes take effect, the output result of the corresponding frame will return this arbitrary value. |
| chn_num        | Channel number. The current DPU device has two channels. Users can set this channel number to 0 or 1. The infrared image channel will input and output on the corresponding channel. This channel number should be different from the speckle image channel number. |
| ir_param       | Infrared image channel parameters.                                                                |

**Notes**:

None

**Related Data Types and Interfaces**:

[kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr)

#### 3.1.9 k_dpu_chn_result_u

**Description**:

Union for obtaining DPU output results.

**Definition**:

```c
typedef union {
    k_dpu_chn_lcn_result_t lcn_result;
    k_dpu_chn_ir_result_t ir_result;
} k_dpu_chn_result_u;
```

**Members**:

| Member Name   | Description                                                                        |
|---------------|------------------------------------------------------------------------------------|
| lcn_result    | Speckle image channel output result structure. [k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t) |
| ir_result     | Infrared image channel output result structure. [k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)   |

**Notes**:

- Users should choose which member to use as the output result based on their own configuration. In [kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr), users configure the mapping between channel numbers and channel types.

**Related Data Types and Interfaces**:

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.10 k_dpu_chn_lcn_result_t

**Description**:

Structure for DPU speckle image channel output results.

**Definition**:

```c
typedef struct {
    k_u32 time_ref;
    k_u64 pts;
    k_dpu_disp_out_t disp_out;
    k_dpu_depth_out_t depth_out;
    k_dpu_qlt_out_t qlt_out;
    k_dpu_param_flag_t flag;
} k_dpu_chn_lcn_result_t;
```

**Members**:

| Member Name  | Description                                                                                                                                                                                                                   |
|--------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pts          | Timestamp, valid in binding mode.                                                                                                                                                                                              |
| disp_out     | Disparity image output result structure.                                                                                                                                                                                       |
| depth_out    | Depth image output result structure.                                                                                                                                                                                           |
| qlt_out      | Quality check output result structure. Includes quality check results, coarse and fine column disparity (initial resolution) results, and initial row-column disparity results.                                               |
| flag         | This structure is used to mark which frame the user-configured parameters take effect. The structure includes the param_valid variables from [k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t), [k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t), and [k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t). |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_disp_out_t](#3112-k_dpu_disp_out_t)
[k_dpu_depth_out_t](#3113-k_dpu_depth_out_t)
[k_dpu_qlt_out_t](#3115-k_dpu_qlt_out_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.11 k_dpu_chn_ir_result_t

**Description**:

Structure for DPU infrared image channel output results.

**Definition**:

```c
typedef struct {
    k_u32 time_ref;
    k_u64 pts;
    k_dpu_ir_out_t ir_out;
    k_dpu_param_flag_t flag;
} k_dpu_chn_ir_result_t;
```

**Members**:

| Member Name | Description                                                                                                                                                                                                                   |
|-------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pts         | Timestamp, valid in binding mode.                                                                                                                                                                                              |
| ir_out      | Infrared image output result structure.                                                                                                                                                                                        |
| flag        | This structure is used to mark which frame the user-configured parameters take effect. The structure includes the param_valid variables from [k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t), [k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t), and [k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t). |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_ir_out_t](#3114-k_dpu_ir_out_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.12 k_dpu_disp_out_t

**Description**:

Structure for disparity image output results.

**Definition**:

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 disp_phys_addr;
    k_u64 disp_virt_addr;
} k_dpu_disp_out_t;
```

**Members**:

| Member Name       | Description                                                   |
|-------------------|---------------------------------------------------------------|
| valid             | K_TRUE: indicates the output result is valid; K_FALSE: indicates the output result is invalid. |
| length            | Length of the output result.                                   |
| disp_phys_addr    | Physical address of the disparity image output result.         |
| disp_virt_addr    | Virtual address of the disparity image output result.          |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.13 k_dpu_depth_out_t

**Description**:

Structure for depth image output results.

**Definition**:

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 depth_phys_addr;
    k_u64 depth_virt_addr;
} k_dpu_depth_out_t;
```

**Members**:

| Member Name        | Description                                                   |
|--------------------|---------------------------------------------------------------|
| valid              | K_TRUE: indicates the output result is valid; K_FALSE: indicates the output result is invalid. |
| length             | Length of the output result.                                   |
| depth_phys_addr    | Physical address of the depth image output result.             |
| depth_virt_addr    | Virtual address of the depth image output result.              |

### Translation

|

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.14 k_dpu_ir_out_t

**Description**:

Structure for infrared image output results.

**Definition**:

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 ir_phys_addr;
    k_u64 ir_virt_addr;
} k_dpu_ir_out_t;
```

**Members**:

| Member Name  | Description                                         |
|--------------|------------------------------------------------------|
| valid        | K_TRUE: indicates the output result is valid; K_FALSE: indicates the output result is invalid. |
| length       | Length of the output result.                         |
| ir_phys_addr | Physical address of the infrared image output result. |
| ir_virt_addr | Virtual address of the infrared image output result.  |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.15 k_dpu_qlt_out_t

**Description**:

Structure for quality check output results.

**Definition**:

```c
typedef struct {
    k_bool valid;
    k_u32 qlt_length;
    k_u32 sad_disp_length;
    k_u32 init_sad_disp_length;
    k_u64 qlt_phys_addr;
    k_u64 qlt_virt_addr;
    k_u64 sad_disp_phys_addr;
    k_u64 sad_disp_virt_addr;
    k_u64 init_sad_disp_phys_addr;
    k_u64 init_sad_disp_virt_addr;
} k_dpu_qlt_out_t;
```

**Members**:

| Member Name             | Description                                         |
|-------------------------|-----------------------------------------------------|
| valid                   | K_TRUE: indicates the output result is valid; K_FALSE: indicates the output result is invalid. |
| qlt_length              | Length of the quality check output result.           |
| sad_disp_length         | Length of the coarse and fine column disparity (initial resolution) output result. |
| init_sad_disp_length    | Length of the initial row-column disparity output result. |
| qlt_phys_addr           | Physical address of the quality check output result. |
| qlt_virt_addr           | Virtual address of the quality check output result.  |
| sad_disp_phys_addr      | Physical address of the coarse and fine column disparity (initial resolution) output result. |
| sad_disp_virt_addr      | Virtual address of the coarse and fine column disparity (initial resolution) output result. |
| init_sad_disp_phys_addr | Physical address of the initial row-column disparity output result. |
| init_sad_disp_virt_addr | Virtual address of the initial row-column disparity output result. |

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

### 3.2 Long and Short Cycle Parameter Types

This module includes the following data types:

- [k_dpu_long_parameter_t](#321-k_dpu_long_parameter_t)
- [k_dpu_short_parameter_t](#322-k_dpu_short_parameter_t)

#### 3.2.1 k_dpu_long_parameter_t

**Description**:

DPU long cycle parameter structure.

**Definition**:

The long cycle parameter has too many members to display here. Refer to the structure `k_dpu_long_parameter_t` in `k_dpu_comm.h` in the K230_SDK.

**Notes**:

- When users need to change the values in the long cycle parameters, they should use the virtual address member variable.

**Related Data Types and Interfaces**:

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)

#### 3.2.2 k_dpu_short_parameter_t

**Description**:

DPU short cycle parameter structure.

**Definition**:

The short cycle parameter has too many members to display here. Refer to the structure `k_dpu_short_parameter_t` in `k_dpu_comm.h` in the K230_SDK.

**Notes**:

None

**Related Data Types and Interfaces**:

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)
[kd_mpi_dpu_get_dev_attr](#215-kd_mpi_dpu_get_dev_attr)

## 4. Error Codes

### 4.1 DPU Error Codes

Table 41

| Error Code   | Macro Definition           | Description                    |
|--------------|----------------------------|--------------------------------|
| 0xa00118001  | K_ERR_DPU_INVALID_DEVID    | Invalid device ID              |
| 0xa00118002  | K_ERR_DPU_INVALID_CHNID    | Invalid channel ID             |
| 0xa00118003  | K_ERR_DPU_ILLEGAL_PARAM    | Invalid parameter              |
| 0xa00118004  | K_ERR_DPU_EXIST            | DPU device already exists      |
| 0xa00118005  | K_ERR_DPU_UNEXIST          | DPU device does not exist      |
| 0xa00118006  | K_ERR_DPU_NULL_PTR         | Null pointer error             |
| 0xa00118007  | K_ERR_DPU_NOT_CONFIG       | DPU not configured             |
| 0xa00118008  | K_ERR_DPU_NOT_SUPPORT      | Unsupported function           |
| 0xa00118009  | K_ERR_DPU_NOT_PERM         | Operation not permitted        |
| 0xa0011800c  | K_ERR_DPU_NOMEM            | Memory allocation failed, e.g., insufficient system memory |
| 0xa0011800d  | K_ERR_DPU_NOBUF            | Insufficient buffer            |
| 0xa0011800e  | K_ERR_DPU_BUF_EMPTY        | Buffer empty                   |
| 0xa0011800f  | K_ERR_DPU_BUF_FULL         | Buffer full                    |
| 0xa00118010  | K_ERR_DPU_NOTREADY         | Device not ready               |
| 0xa00118011  | K_ERR_DPU_BADADDR          | Invalid address                |
| 0xa00118012  | K_ERR_DPU_BUSY             | DPU is busy                    |

## 5. Debug Information

### 5.1 Overview

Debug information uses the proc file system to reflect the current running state of the system in real-time. The recorded information can be used for problem localization and analysis.

### File Directory

/proc/

### File List

| File Name  | Description                   |
|------------|-------------------------------|
| umap/dpu   | Records some information about the current DPU module |

### 5.2 Debug Information

### Debug Information

```shell
----------------------DPU Device Information----------------------
--------------------Pathway Switch Information--------------------
downScale: false align: false
align_ir: false align_rgbCoord: false
depthout: false denoise: false
median_p0: false median_denoise: false
median_post: false median_ir: false
check: false

----------------------Image Size Information----------------------
width_speckle: 0 height_speckle: 0
width_color: 0 height_color: 0
width_output: 0 height_output: 0

---------------------Result Length Information--------------------
sad_disp_x: 0 init_sad_disp_xy: 0
quanlity_check: 0 ir: 0
disp/depth: 0

----------------------------Frame Count---------------------------
from open to close, dpu has send 0 frames
```

### Pathway Selection Information

| Parameter       | **Description**                              |
|-----------------|----------------------------------------------|
| downScale       | Whether to downscale for coarse search       |
| align           | Whether to align three images                |
| align_ir        | Whether to align infrared images             |
| align_rgbCoord  | Whether to align disparity values to the color image coordinate system |
| depthout        | Whether to output depth maps                 |
| denoise         | Whether to denoise disparity maps            |
| median_p0       | Whether to apply median filtering in coarse search |
| median_denoise  | Whether to apply internal median filtering for disparity denoising |
| median_post     | Whether to apply post-processing median filtering for disparity/three-image alignment |
| median_ir       | Whether to apply median filtering for three-image aligned infrared images |
| check           | Whether to perform quality check and initial search for object speckle images |

### Image Size Information

| Parameter       | **Description**                              |
|-----------------|----------------------------------------------|
| width_speckle   | Width in pixels of the original speckle/infrared image |
| height_speckle  | Height in pixels of the original speckle/infrared image |
| width_color     | Width in pixels of the original color image  |
| height_color    | Height in pixels of the original color image |
| width_output    | Width in pixels of the output disparity/depth/infrared image |
| height_output   | Height in pixels of the output disparity/depth/infrared image |

### Result Length Information

| Parameter           | **Description**                              |
|---------------------|----------------------------------------------|
| sad_disp_x          | Length of the coarse and fine column disparity (initial resolution) result |
| init_sad_disp_xy    | Length of the initial row-column disparity output result |
| quanlity_check      | Length of the quality check result           |
| ir                  | Length of the infrared image result          |
| disp/depth          | Length of the disparity/depth image result   |

Debug information needs to be viewed during DPU operation. After DPU stops running, all current information will be reset to zero.

## 6. Demo Description

### 6.1 DPU Demo Introduction

The DPU demo implements both binding and non-binding modes. In the msh, input `/bin/sample_dpu.elf` to execute the non-binding mode, which ends after running ten frames. Input `/bin/sample_dpu.elf BOUND` to execute the binding mode, where VVI simulates the upper layer continuously inputting data to the DPU, and the DPU displays information after computation.

### 6.2 Feature Description

The demo includes functions such as initializing and deleting the DPU, parsing parameters from the configuration file, configuring device attributes, configuring channel attributes, starting and pausing the device, starting and pausing the channel, input and output data, and pipeline binding.

#### 6.2.1 Non-binding Mode

By calling the API, the DPU device is initialized, parameters are parsed from the configuration file, device attributes are configured based on the parsed parameters, the API is called to set the reference image and template image, the DPU device is started, speckle and infrared image channel attributes are configured, the channel is started, ten frames are looped through and the results are compared, then the channel is stopped, the device is stopped, and the device is deleted.

#### 6.2.2 Binding Mode

By calling the API, the DPU device is initialized, parameters are parsed from the configuration file, VVI and DPU channels are bound, device attributes are configured based on the parsed parameters, the API is called to set the reference image and template image, the DPU device is started, speckle and infrared image channel attributes are configured, the DPU channel is started, the VVI channel is started, and VVI continuously inputs data to the DPU as the simulated upper layer. The user inputs 'e' to stop the channel and device.

#### 6.2.3 Compilation and Execution

Refer to the document "K230 SDK Demo Usage Guide" for compilation and execution.
