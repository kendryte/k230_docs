# K230 DPU API reference

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

This document mainly introduces the use of K230 DPU software, including the use of DPU API and demo introduction.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate                                           |
|------|------------------------------------------------|
| DPU  | Depth Process Unit               |
| LCN  | Local Contrast Normalization|

### Revision history

| Document version number | Modify the description                                                                                                                                | Author | date      |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------|--------|-----------|
| v1.0       | Initial                                                                                                                                   | Liu Suntao | 2023/3/30 |
| v1.1       | Added  interface function  [kd_mpi_dpu_set_processed_ref_image](#217-kd_mpi_dpu_set_processed_ref_image); Added module debugging information. | Liu Suntao | 2023/4/20 |
| V1.2       | Added configurable functionality of buffer                             | Liu Suntao | 2023/5/31 |

## 1. Overview

### 1.1 Overview

The DPU is mainly responsible for the depth calculation of 3D structured light, providing depth information for 3D face recognition.

### 1.2 Function Description

#### 1.2.1 Binding mode invokes the process

The first step is to initialize vb pool. The last step is to release vb pool.

![Illustrative, Schematic description is automatically generated](../../../../zh/01_software/board/mpp/images/b85b814d3911bf8b3802ba97751ff941.png)

#### 1.2.2 Invoke the process in unbound mode

The first step is to initialize vb pool. The last step is to release vb pool.

![The Illustrative description has been automatically generated](../../../../zh/01_software/board/mpp/images/dca3cfa887a526c493abced31b59afd2.png)

## 2. API Reference

### 2.1 DPU usage

This function module provides the following APIs:

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

【Description】

Initialize the DPU device

【Syntax】

k_s32 kd_mpi_dpu_init(k_dpu_init_t \*init);

【Parameters】

| Parameter name | description                           | Input/output |
|----------|--------------------------------|-----------|
| init     | Initializes the structure pointer for the DPU device.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None.

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

None

【Example】

None

【See Also】

[k_dpu_init_t](#311-k_dpu_init_t)

#### 2.1.2 kd_mpi_dpu_delete

【Description】

Delete the DPU device that has been initialized.

【Syntax】

k_s32 kd_mpi_dpu_delete();

【Parameters】

| Parameter name | description | Input/output |
|----------|------|-----------|
| None       | None   | None        |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

This function can only be called after the DPU device is initialized.

【Example】

None

【See Also】

None

#### 2.1.3 kd_mpi_dpu_parse_file

【Description】

Extract DPU configuration parameters from the DPU configuration file.

【Syntax】

k_s32 kd_mpi_dpu_parse_file(const k_char \*param_path, k_dpu_dev_param_t \*param, k_dpu_lcn_param_t \*lcn_param, k_dpu_ir_param_t \*ir_param, k_dpu_user_space_t \*g_temp_space);

【Parameters】

| Parameter name     | description                                                                       | Input/output |
|--------------|----------------------------------------------------------------------------|-----------|
| param_path   | The path to the configuration file                                                             | input      |
| param        | The structure pointer for DPU device parameters in which extracted from the configuration file are saved.   | output      |
| lcn_param    | The structure pointer for LCN channel parameters in which extracted from the configuration file are saved. | output      |
| ir_param     | The structure pointer for IR channel parameters in which extracted from the configuration file are saved.  | output      |
| g_temp_space | The structure pointer for template diagram in which extracted from the configuration file are saved.     | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- DPU device parameters include long-period parameters and short-period parameters.
- The channel parameters, lcn_param and ir_param, are subsets of DPU device parameters and can be ignored if DPU device parameters have already been configured. If you need to change the parameters in both channel parameter structs, you can either change the channel parameter and call kd_mpi_dpu_set_chn_attr later to make the change take effect, or you can change the device parameter and call kd_mpi_dpu_set_dev_attr later to make the change take effect. If only the channel parameters are changed, calling kd_mpi_dpu_set_chn_attr is more efficient.
- The template diagram structure contains the virtual and physical addresses of the template diagram parsed from the configuration file, as well as the size of the template diagram.

【Example】

None

【See Also】

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)

#### 2.1.4 kd_mpi_dpu_set_dev_attr

【Description】

Configure DPU device properties.

【Syntax】

k_s32 kd_mpi_dpu_set_dev_attr(k_dpu_dev_attr_t \*attr);

【Parameters】

| Parameter name | description         | Input/output |
|----------|--------------|-----------|
| attr     | DPU device properties | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- This function can be called to configure DPU device properties only after the DPU device has been initialized.
- When you first configure DPU device properties, you should configure the tytz_temp_recfg and align_depth_recfg in ATTR as K_TRUE so that the DPU loads the corresponding parameters. When changing the DPU device properties later, if the corresponding long-period parameters are not changed, configuring these two members to K_FALSE can save the time for the DPU to load the long-period parameters again.

【Example】

None

【See Also】

[k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)

#### 2.1.5 kd_mpi_dpu_get_dev_attr

【Description】

Gets the dpu device properties.

【Syntax】

k_s32 kd_mpi_dpu_set_dev_attr(k_dpu_dev_attr_t \*attr);

【Parameters】

| Parameter name | description         | Input/output |
|----------|--------------|-----------|
| attr     | DPU device properties | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

None

【Example】

None

【See Also】

[k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)

#### 2.1.6 kd_mpi_dpu_set_ref_image

【Description】

Configure the DPU reference image.

【Syntax】

k_s32 kd_mpi_dpu_set_ref_image(const k_char \*ref_path);

【Parameters】

| Parameter name | description       | Input/output |
|----------|------------|-----------|
| ref_path | Reference image path | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- You need to call this function after configuring the dpu device properties to configure the reference graph.

【Example】

None

【See Also】

None

#### 2.1.7 kd_mpi_dpu_set_processed_ref_image

【Description】

Configure the DPU reference picture after offline processing.

【Syntax】

k_s32 kd_mpi_dpu_set_processed_ref_image(const k_char \*ref_path);

【Parameters】

| Parameter name | description               | Input/output |
|----------|--------------------|-----------|
| ref_path | The path of the processed reference picture | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- You need to call this function to configure the reference picture after configuring the dpu device properties, the configured reference picture needs to be processed offline, and calling this function can save [](#216-kd_mpi_dpu_set_ref_image) about 70ms time compared to kd_mpi_dpu_set_ref_image.

【Example】

None

【See Also】

None

#### 2.1.8 kd_mpi_dpu_set_template_image

【Description】

Configure the DPU template image

【Syntax】

k_s32 kd_mpi_dpu_set_template_image(k_dpu_user_space_t \*temp_space);

【Parameters】

| Parameter name   | description           | Input/output |
|------------|----------------|-----------|
| temp_space | Template diagram structure. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- You need to call this function after configuring the dpu device properties to configure the template image.
- temp_space needs to be [](#213-kd_mpi_dpu_parse_file) passed in as a parameter at kd_mpi_dpu_parse_file time to get the template image information from the configuration file.

【Example】

None

【See Also】

[k_dpu_user_space_t](#315-k_dpu_user_space_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 2.1.9 kd_mpi_dpu_start_dev

【Description】

Start the DPU device

【Syntax】

k_s32 kd_mpi_dpu_start_dev();

【Parameters】

| Parameter name | description | Input/output |
|----------|------|-----------|
| None       | None   | None        |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.1.10 kd_mpi_dpu_set_chn_attr

【Description】

Configure DPU channel properties

【Syntax】

k_s32 kd_mpi_dpu_set_chn_attr(k_dpu_chn_lcn_attr_t \*lcn_attr, k_dpu_chn_ir_attr_t \*ir_attr);

【Parameters】

| Parameter name | description             | Input/output |
|----------|------------------|-----------|
| lcn_attr | Speckle channel properties. | input      |
| ir_attr  | IR channel properties. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- There are currently two channels for DPU devices: 0 and 1. Indicate the respective input and output channels for speckle and IR by configuring lcn_attr-\>chn_num and ir_attr-\>chn_num if IR channels are turned on.
- This function should be called to configure channel properties after the DPU device kd_mpi_dpu_start_dev is first started [](#219-kd_mpi_dpu_start_dev) , where the speckle channel must be configured, and the IR channel can be left unconfigured if not enabled (configured as NULL).
- If you only need to change the properties of one channel during operation, you can pass only the structure parameters of the channel, and the parameters of the other channel can be NULL. It is also possible to pass in parameters for both channels at the same time. If the parameters of both channels are NULL, the configuration will not take effect.

【Example】

None

【See Also】

[k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)
[k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t)

#### 2.1.11 kd_mpi_dpu_get_chn_attr

【Description】

Gets the DPU channel properties.

【Syntax】

k_s32 kd_mpi_dpu_get_chn_attr(k_dpu_chn_lcn_attr_t \*lcn_attr, k_dpu_chn_ir_attr_t \*ir_attr);

【Parameters】

| Parameter name | description             | Input/output |
|----------|------------------|-----------|
| lcn_attr | Speckle channel properties. | output      |
| ir_attr  | IR channel properties. | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

None

【Example】

None

【See Also】

[k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)
[k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t)

#### 2.1.12 kd_mpi_dpu_start_chn

【Description】

Start the DPU channel

【Syntax】

k_s32 kd_mpi_dpu_start_chn(k_u32 chn_num);

【Parameters】

| Parameter name | description   | Input/output |
|----------|--------|-----------|
| chn_num  | Channel number | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- The channel number should be 0 or 1.

【Example】

None

【See Also】

None

#### 2.1.13 kd_mpi_dpu_stop_chn

【Description】

Stop the DPU channel

【Syntax】

k_s32 kd_mpi_dpu_stop_chn(k_u32 chn_num);

【Parameters】

| Parameter name | description   | Input/output |
|----------|--------|-----------|
| chn_num  | Channel number | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- The channel number should be 0 or 1.

【Example】

None

【See Also】

None

#### 2.1.14 kd_mpi_dpu_send_frame

【Description】

In unbound mode, one frame of data is sent to the DPU.

【Syntax】

k_s32 kd_mpi_dpu_send_frame(k_u32 chn_num, k_u64 addr, k_s32 s32_millisec);

【Parameters】

| Parameter name     | description                                                                                                                                                                                        | Input/output |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num      | Channel number                                                                                                                                                                                      | input      |
| addr         | The physical address where the data is sent                                                                                                                                                                          | input      |
| s32_millisec | Waiting time. When this parameter is set to -1, blocking mode will not be returned until the send is successful; when this parameter is set to 0, non-blocking mode, send success immediately returns zero, send failure immediately returns other values, refer to [dpu error code](#41-dpu-error-code) for specific failure information; | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- If the speckle and IR channels are enabled at the same time, strict cross-input of the IR image and the speckle image is required.

【Example】

None

【See Also】

None

#### 2.1.15 kd_mpi_dpu_get_frame

【Description】

Get one frame from the DPU.

【Syntax】

k_s32 kd_mpi_dpu_get_frame(k_u32 chn_num, k_dpu_chn_result_u \*result, k_s32 s32_millisec);

【Parameters】

| Parameter name     | description                                                                                                                                                                                                     | Input/output |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num      | Channel number                                                                                                                                                                                                   | input      |
| result       | The DPU outputs a resulting federation whose member variables are k_dpu_chn_lcn_result_t and k_dpu_chn_ir_result_t. Which member to choose as the output of the channel is up to the user to decide based on the [configuration of the kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr) . | output      |
| s32_millisec | Waiting time. When this parameter is set to -1, blocking mode will not be returned until the acquisition is successful; When this parameter is set to 0, non-blocking mode, the acquisition success immediately returns zero, and the acquisition failure immediately returns other values, refer to the [dpu error code](#41-dpu-error-code) for specific failure information;              | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- If IR and speckle images are turned on at the same time, pay attention to take away the output results of both channels in time, otherwise the results in the buffer will overflow and the input cannot be continued.

【Example】

None

【See Also】

[k_dpu_chn_result_u](#319-k_dpu_chn_result_u)
[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[k_dpu_disp_out_t](#3112-k_dpu_disp_out_t)
[k_dpu_depth_out_t](#3113-k_dpu_depth_out_t)
[k_dpu_ir_out_t](#3114-k_dpu_ir_out_t)
[k_dpu_qlt_out_t](#3115-k_dpu_qlt_out_t)

#### 2.1.16 kd_mpi_dpu_release_frame

【Description】

In unbound mode, release the results that have already been obtained.

【Syntax】

k_s32 kd_mpi_dpu_release_frame();

【Parameters】

None

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Differences】

None

【Requirement】

- Header file: mpi_dpu_api.h
- Library file: libdpu.a

【Note】

- This function releases the frame, and the first generated result is released first. The current dpu buffer is 3, please release the result from [kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame) as soon as possible.

【Example】

None

【See Also】

None

## 3. Data Type

### 3.1 Common Data Types

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

【Description】

The DPU device initializes the structure

【Definition】

```c
typedef struct {
    k_u32 start_num;
    k_u32 buffer_num;
} k_dpu_init_t;
```

【Members】

| Member name  | description                                                |
|-----------|-----------------------------------------------------|
| start_num | The DPU device start frame number (that is the first frame calculated by the DPU).   |
| buffer_num| The number of DPU cache buffers, at least 1                    |

【Note】

None

【See Also】

[kd_mpi_dpu_init](#211-kd_mpi_dpu_init)

#### 3.1.2 k_dpu_dev_param_t

【Description】

DPU device parameter structure.

【Definition】

```c
typedef struct
{
    k_dpu_long_parameter_t lpp;
    k_dpu_short_parameter_t spp;
} k_dpu_dev_param_t;
```

【Members】

| Member name | description                 |
|----------|----------------------|
| Page      | DPU long-period parameter structure |
| spp      | DPU short-period parameter structure |

【Note】

- When you need to change the value in the long-period parameter, you should use the virtual address member variable.

【See Also】

[k_dpu_long_parameter_t](#321-k_dpu_long_parameter_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.3 k_dpu_lcn_param_t

【Description】

Speckle image channel parameter structure.

【Definition】

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

【Members】
| Member name                    | description                                                                 |
|-----------------------------|---------------------------------------------------------------------|
| matching_length_left_p0     | Coarse search: parallax calculation to the left search range, value: 0~256, integer                        |
| matching_length_right_p0    | Coarse search: parallax calculation to the right search range, value: 0~256, integer                        |
| image_check_match_threshold | Speckle image quality evaluation: template matching threshold, value range: 0.0~1.0, floating-point type: 0.01 accuracy       |
| depth_p1                    | Parallax to depth: depth numerical calculation coefficient P1, value range: 0.0~50000.0, floating point type: 0.01 accuracy |
| depth_p2                    | Parallax to depth: depth numerical calculation coefficient P2, value range: -5.0~100.0, floating-point type: 0.01 accuracy  |
| depth_precision             | Parallax to depth: depth numerical accuracy (multiple), value range: 0.0~100.0, floating-point type: 0.1 accuracy  |

【Note】

- This channel structure parameter is a subset of the device structure parameters, if you have configured device parameters and the channel parameters are the same as the device parameters, you can not configure the channel parameters.

【See Also】

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.4 k_dpu_ir_param_t

【Description】

IR channel parameter structure.

【Definition】

```c
typedef struct {
    float depth_k1;
    float depth_k2;
    float tz;
} k_dpu_ir_param_t;
```

【Members】
| Member name | description |
|---|---|
| depth_k1 | Directly corresponds exactly to one register. Three-images alignment: depth numerical calculation coefficient k1, value range: 2e-4~1e-2, floating point type: 1e-5 accuracy |
| depth_k2 | Directly corresponds exactly to one register. Three-images alignment: depth numerical calculation coefficient k2, value range: 0.5~1.5, floating point type: 0.001 accuracy |
| tz | Directly corresponds exactly to one register. Three-images alignment: projector z direction offset (mm), value range: -5.0~5.0, floating point type: 0.001 accuracy |

【Note】

- This channel structure parameter is a subset of the device structure parameters, if you have configured device parameters and the channel parameters are the same as the device parameters, you can not configure the channel parameters.

【See Also】

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.5 k_dpu_user_space_t

【Description】

The user gets the template diagram structure parameters.

【Definition】

```c
typedef struct {
    k_bool used;
    k_u32 size;
    k_u64 phys_addr;
    void *virt_addr;
} k_dpu_user_space_t;
```

【Members】

| Member name  | description                   |
|-----------|------------------------|
| used      | Users don't need attention         |
| size      | The size of the template graph that the user gets |
| phys_addr | The physical address of the template diagram       |
| virt_addr | The virtual address of the template diagram       |

【Note】

None

【See Also】

[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)

#### 3.1.6 k_dpu_dev_attr_t

【Description】

Configure the DPU device property structure.

【Definition】

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

【Members】

| Member name          | description                                                                                                                     |
|-------------------|--------------------------------------------------------------------------------------------------------------------------|
| mode              | DPU operating modes, including bonded and unbounded modes.                                                                                 |
| tytz_temp_recfg   | Whether to update the load SAD temperature compensation parameter and the TyTz line compensation calculation arithmetic. A bit of K_FALSE indicates no update, and a bit of K_TRUE indicates an update. |
| align_depth_recfg | Whether to update the parameters of the three-plot alignment/turn depth calculation are updated. A bit of K_FALSE indicates no update, and a bit of K_TRUE indicates an update.                 |
| ir_never_open     | VB pools are configured when the DPU device is started until it is released when the DPU device is paused. Its size is initialized when the device is started, so there is space for five parts: depth/parity map, IR output, quality inspection, thickness column parallax, and initial determinant difference when starting the device. Users can use dev_param.spp.flag_align to choose whether to enable three-graph alignment during the usage period.  If there is no IR output throughout the life cycle, there is no need to reserve space for IR. A configuration of K_TRUE indicates that no space is required for IR output, and a configuration of K_FALSE indicates that space is required for IR output. |
| param_valid       | When the user configures a DPU device property, this member is set to an arbitrary nonzero value that is returned in the output of the corresponding effective frame when the device property takes effect.    |
| dev_param         | DPU device parameter structure.                                                                                                     |

【Note】

- When you first configure DPU device properties, you should configure tytz_temp_recfg and align_depth_recfg to K_TRUE so that the DPU loads the corresponding parameters.

【See Also】

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)

#### 3.1.7 k_dpu_chn_lcn_attr_t

【Description】

Configure the speckle channel attribute structure

【Definition】

```c
typedef struct {
    k_u8 param_valid;
    k_s32 chn_num;
    k_dpu_lcn_param_t lcn_param;
} k_dpu_chn_lcn_attr_t;
```

【Members】

| Member name    | description                                                                                                                                                         |
|-------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| param_valid | When the user configures the speckle channel property, this member is set to an arbitrary nonzero value that is returned in the output of the corresponding effective frame when the device property takes effect.                                       |
| chn_num     | Channel number. The current DPU device has a total of two channels, the user can set this channel number to 0 or 1, and the speckle channel will be input and output in the corresponding channel. If the IR channel is enabled, this channel number should be different from the IR channel number. |
| lcn_param   | Speckle channel parameters.                                                                                                                                             |

【Note】

None

【See Also】

[kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr)

#### 3.1.8 k_dpu_chn_ir_attr_t

【Description】

Configure the IR channel property structure

【Definition】

```c
typedef struct {
    k_u8 param_valid;
    k_s32 chn_num;
    k_dpu_ir_param_t ir_param;
} k_dpu_chn_ir_attr_t;
```

【Members】

| Member name    | description                                                                                                                                   |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------|
| param_valid | When the user configures the speckle channel property, this member is set to an arbitrary nonzero value that is returned in the output of the corresponding effective frame when the device property takes effect.                 |
| chn_num     | Channel number. The current DPU device has a total of two channels, the user can set this channel number to 0 or 1, and the IR channel will be input and output in the corresponding channel. This channel number should be different from the speckle image channel number. |
| ir_param    | IR channel parameters.                                                                                                                       |

【Note】

None

【See Also】

[kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr)

#### 3.1.9 k_dpu_chn_result_u

【Description】

Gets the federation of DPU output

【Definition】

```c
typedef union {
    k_dpu_chn_lcn_result_t lcn_result;
    k_dpu_chn_ir_result_t ir_result;
} k_dpu_chn_result_u;
```

【Members】

| Member name   | description                                                                        |
|------------|-----------------------------------------------------------------------------|
| lcn_result | The speckle image channel outputs the resulting structure. [k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t) |
| ir_result  | The IR channel outputs the resulting structure. [k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)   |

【Note】

- Which member the user selects as output needs to be selected based on the user's own configuration. In [kd_mpi_dpu_set_chn_attr](#2110-kd_mpi_dpu_set_chn_attr) user configures the correspondence between the channel number and the channel type.

【See Also】

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.10 k_dpu_chn_lcn_result_t

【Description】

The structure of the DPU scatter image channel output result

【Definition】

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

【Members】

| Member name  | description                                                                                                                                                                                                                   |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pts       | Timestamp, valid in bound mode.                                                                                                                                                                                               |
| disp_out  | The disparity plot outputs the resulting structure.                                                                                                                                                                                                 |
| depth_out | The depth image outputs the resulting structure.                                                                                                                                                                                                 |
| qlt_out   | Quality inspection output result structure. Includes quality test results, thickness_column parallax (initial resolution) results, and initial determinant difference results.                                                                                                                            |
| flag      | This structure is used to mark the frame at which the user-configured parameters took effect. The struct contains param_valid variables in [k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t)、[k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t)、[k_dpu_chn_ir_attr_t](#318-k_dpu_chn_ir_attr_t). |

【Note】

None

【See Also】

[k_dpu_disp_out_t](#3112-k_dpu_disp_out_t)
[k_dpu_depth_out_t](#3113-k_dpu_depth_out_t)
[k_dpu_qlt_out_t](#3115-k_dpu_qlt_out_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.11 k_dpu_chn_ir_result_t

【Description】

A structure in which the DPU IR channel outputs the results

【Definition】

```c
typedef struct {
    k_u32 time_ref;
    k_u64 pts;
    k_dpu_ir_out_t ir_out;
    k_dpu_param_flag_t flag;
} k_dpu_chn_ir_result_t;
```

【Members】

| Member name | description                                                                                                                                                                                                                   |
|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| pts      | Timestamp, valid in bound mode.                                                                                                                                                                                               |
| ir_out   | The IR image outputs the resulting structure.                                                                                                                                                                                                 |
| flag     | This structure is used to mark the frame at which the user-configured parameters took effect. The struct contains [param_valid variables in k_dpu_dev_attr_t](#316-k_dpu_dev_attr_t), [k_dpu_chn_lcn_attr_t](#317-k_dpu_chn_lcn_attr_t), k_dpu_chn_ir_attr_t[](#318-k_dpu_chn_ir_attr_t). |

【Note】

None

【See Also】

[k_dpu_ir_out_t](#3114-k_dpu_ir_out_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.12 k_dpu_disp_out_t

【Description】

The structure of the parallax plot output result

【Definition】

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 disp_phys_addr;
    k_u64 disp_virt_addr;
} k_dpu_disp_out_t;
```

【Members】

| Member name       | description                                                   |
|----------------|--------------------------------------------------------|
| valid          | K_TRUE: indicates that the output result is valid; K_FALSE: indicates that the output result is invalid. |
| length         | Output result length.                                         |
| disp_phys_addr | The disparity plot outputs the resulting physical address.                               |
| disp_virt_addr | The parallax plot outputs the resulting virtual address.                               |

【Note】

None

【See Also】

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.13 k_dpu_depth_out_t

【Description】

The structure of the depth image output result

【Definition】

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 depth_phys_addr;
    k_u64 depth_virt_addr;
} k_dpu_depth_out_t;
```

【Members】

| Member name        | description                                                   |
|-----------------|--------------------------------------------------------|
| valid           | K_TRUE: indicates that the output result is valid; K_FALSE: indicates that the output result is invalid. |
| length          | Output result length.                                         |
| depth_phys_addr | The depth image outputs the physical address of the result.                               |
| depth_virt_addr | The depth image outputs the virtual address.                               |

【Note】

None

【See Also】

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.14 k_dpu_ir_out_t

【Description】

The structure of the IR output result

【Definition】

```c
typedef struct {
    k_bool valid;
    k_u32 length;
    k_u64 ir_phys_addr;
    k_u64 ir_virt_addr;
} k_dpu_ir_out_t;
```

【Members】

| Member name     | description                                                   |
|--------------|--------------------------------------------------------|
| valid        | K_TRUE: indicates that the output result is valid; K_FALSE: indicates that the output result is invalid. |
| length       | Output result length.                                         |
| ir_phys_addr | The IR output results physical address.                               |
| ir_virt_addr | The IR output results virtual address.                               |

【Note】

None

【See Also】

[k_dpu_chn_ir_result_t](#3111-k_dpu_chn_ir_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

#### 3.1.15 k_dpu_qlt_out_t

【Description】

The structure of the quality inspection output

【Definition】

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

【Members】

| Member name                | description                                                   |
|-------------------------|--------------------------------------------------------|
| valid                   | K_TRUE: indicates that the output result is valid; K_FALSE: indicates that the output result is invalid. |
| qlt_length              | Quality inspection output length.                                 |
| sad_disp_length         | The parallax (initial resolution) output length of the thickness column.                 |
| init_sad_disp_length    | The initial determinant difference outputs the resulting length.                             |
| qlt_phys_addr           | The physical address of the quality inspection output result.                             |
| qlt_virt_addr           | The virtual address of the quality inspection output results.                             |
| sad_disp_phys_addr      | The parallax (initial resolution) output of the resulting physical address.             |
| sad_disp_virt_addr      | The parallax (initial resolution) output of the resulting virtual address.             |
| init_sad_disp_phys_addr | The initial determinant difference outputs the resulting physical address.                         |
| init_sad_disp_virt_addr | The initial determinant difference outputs the resulting virtual address.                         |

【Note】

None

【See Also】

[k_dpu_chn_lcn_result_t](#3110-k_dpu_chn_lcn_result_t)
[kd_mpi_dpu_get_frame](#2115-kd_mpi_dpu_get_frame)

### 3.2 Long and short period parameter types

This module has the following data types:

- [k_dpu_long_parameter_t](#321-k_dpu_long_parameter_t)
- [k_dpu_short_parameter_t](#322-k_dpu_short_parameter_t)

#### 3.2.1 k_dpu_long_parameter_t

【Description】

DPU long-period parameter structure

【Definition】

There are too many long-period parameter members to be shown here, see the struct k_dpu_long_parameter_t in k_dpu_comm.h in K230_SDK.

【Note】

- When you need to change the value in the long-period parameter, you should use the virtual address member variable.

【See Also】

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_parse_file](#213-kd_mpi_dpu_parse_file)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)

#### 3.2.2 k_dpu_short_parameter_t

【Description】

DPU short-period parameter structure

【Definition】

There are too many short-period parameter members to be shown here, see the struct k_dpu_short_parameter_t in k_dpu_comm.h in K230_SDK.

【Note】

None

【See Also】

[k_dpu_dev_param_t](#312-k_dpu_dev_param_t)
[kd_mpi_dpu_set_dev_attr](#214-kd_mpi_dpu_set_dev_attr)
[kd_mpi_dpu_get_dev_attr](#215-kd_mpi_dpu_get_dev_attr)

## 4. Error codes

### 4.1 dpu error code

Table 41

| Error code    | Macro definitions                  | description                         |
|-------------|-------------------------|------------------------------|
| 0xa00118001 | K_ERR_DPU_INVALID_DEVID | Invalid device number                 |
| 0xa00118002 | K_ERR_DPU_INVALID_CHNID | Invalid channel number                 |
| 0xa00118003 | K_ERR_DPU_ILLEGAL_PARAM | Parameter error                     |
| 0xa00118004 | K_ERR_DPU_EXIST         | The DPU device already exists             |
| 0xa00118005 | K_ERR_DPU_UNEXIST       | The DPU device does not exist               |
| 0xa00118006 | K_ERR_DPU_NULL_PTR      | Null pointer error                   |
| 0xa00118007 | K_ERR_DPU_NOT_CONFIG    | DPU has not been configured                 |
| 0xa00118008 | K_ERR_DPU_NOT_SUPPORT   | Unsupported features                 |
| 0xa00118009 | K_ERR_DPU_NOT_PERM      | Operation is not allowed                   |
| 0xa0011800c | K_ERR_DPU_NOMEM         | Failed to allocate memory, such as low system memory |
| 0xa0011800d | K_ERR_DPU_NOBUF         | BUFF is insufficient                    |
| 0xa0011800e | K_ERR_DPU_BUF_EMPTY     | BUFF is empty                    |
| 0xa0011800f | K_ERR_DPU_BUF_FULL      | BUFF is full                    |
| 0xa00118010 | K_ERR_DPU_NOTREADY      | The device is not ready                   |
| 0xa00118011 | K_ERR_DPU_BADADDR       | Wrong address                   |
| 0xa00118012 | K_ERR_DPU_BUSY          | The DPU is in a busy state               |

## 5. Debugging information

### 5.1 Overview

The debug information uses the PROC file system, which can reflect the current operating status of the system in real time, and the recorded information can be used for problem location and analysis

【File Directory】

/proc/

【Document List】

| File name  | description                        |
|-----------|-----------------------------|
| umap/dpu  | Record some information about the current DPU module |

### 5.2 Debugging Information

【Debugging Information】

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

【Channel selection information】

| parameter           | **Description**                              |
|----------------|---------------------------------------|
| downScale      | Whether the coarse search is resolution reduced                    |
| align          | Whether the three diagrams are aligned                          |
| align_ir       | Whether the IR is aligned                        |
| align_rgbCoord | Whether parallax values are aligned to the color plot coordinate system        |
| depthout       | Whether to output a depth image                        |
| denoise        | Whether the parallax image is denoised                        |
| median_p0      | Whether the coarse search is filtered for medians                    |
| median_denoise | Whether parallax denoising internal median filtering              |
| median_post    | Whether parallax post-processing/three-plot alignment disparity plot median filtering |
| median_ir      | Whether the three figures are aligned and the IR median value is filtered            |
| check          | Whether the object speckle image quality inspection and initial search      |

【Image size information】

| parameter           | **Description**                           |
|----------------|------------------------------------|
| width_speckle  | Number of pixels in the original speckle/IR width        |
| height_speckle | Number of pixels in the height of the original speckle/IR        |
| width_color    | The number of pixels in the width of the original color image               |
| height_color   | The number of pixels in the height of the original color image               |
| width_output   | Output the number of pixels in parallax image/depth image/IR width |
| height_output  | Output parallax image/depth image/IR image height number of pixels |

【Result length information】

| parameter             | **Description**                         |
|------------------|----------------------------------|
| sad_disp_x       | The length for column parallax (initial resolution) result |
| init_sad_disp_xy | The length for initial row and column parallax output result         |
| quanlity_check   | The length for Quality checking result                 |
| ir               | The length for IR result                   |
| disp/depth       | The length for Parallax plot/depth plot result            |

The commissioning information needs to be viewed during the operation of the DPU, and after the DPU finishes running, all current information will be reset to zero.

## 6. Demo description

### 6.1 Introduction to dpu demo

DPU demo implements two modes: bound and unbound. Enter /bin/sample_dpu.elf in msh to execute unbound mode, which ends after running ten frames; enter /bin/sample_dpu.elf BOUND in msh to execute binding mode, using vvi as the input data of the analog superior to the DPU, and displaying information after the dpu calculation is completed.

### 6.2 Feature 说明

The demo includes functions such as initializing and deleting the DPU, parsing parameters from configuration files, configuring device properties, configuring channel properties, starting and pausing devices, starting and pausing channels, input and output data, pipeline binding, etc.

#### 6.2.1 Unbound Mode

Complete the initialization of the dpu device by calling the API, parse the parameters from the configuration file, configure the device properties according to the parsing parameters, call the API to set the reference graph and template image, start the dpu device, configure the speckle image and IR image channel properties, start the channel, loop through the input of ten frames and compare the results and stop, stop the channel, stop the device, delete the device.

#### 6.2.2 Binding Mode

Complete the initialization of the dpu device by calling the API, parse the parameters from the configuration file, bind the vvi and dpu channels, configure the device properties according to the parsing parameters, call the API to set the reference graph and template graph, start the dpu device, configure the speckle image and IR image channel properties, start the dpu channel, start the vvi channel, and the vvi is constantly input data to the DPU as the simulated superior data. The user enters e to stop the channel and device later.

#### 6.2.3 Compilation and Execution

For compilation and execution, refer to the document "K230 SDK Demo User Guide".
