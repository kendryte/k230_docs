# K230 Video Encoding and Decoding API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliated companies. All or part of the products, services, or features described in this document may not be within the scope of your purchase or usage. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for guidance and reference.

The content of this document may be updated or modified periodically without any notice due to product version upgrades or other reasons.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Canaan Creative Information Technology Co., Ltd. and its affiliated companies. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy any part or all of the content of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the functions and usage of the video encoding and decoding module.

### Target Audience

This document (guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
|              |             |
|              |             |

### Revision History

| Document Version | Author | Date       | Modification Description |
|------------------|----------|------------|--------------------------|
| V1.0             | System Software Department | 2023.03.10 | Initial version |
| V1.1             | System Software Department | 2023.03.31 | 1. Added 2D mode setting/getting interfaces kd_mpi_venc_set_2d_mode, kd_mpi_venc_get_2d_mode 2. Modified 2D parameter setting/getting interfaces kd_mpi_venc_set_2d_osd_param, kd_mpi_venc_get_2d_osd_param 3. Added interface for setting image format conversion coefficients in 2D computation kd_mpi_venc_set_2d_set_custom_coef 4. Removed pic_format attribute from encoder attribute structure k_venc_attr |
| V1.1.1           | System Software Department | 2023.04.11 | 1. Added encoding image rotation setting/getting interfaces kd_mpi_venc_set_rotaion, kd_mpi_venc_get_rotaion 2. Added 2D border attribute setting/getting interfaces kd_mpi_venc_set_2d_border_param, kd_mpi_venc_get_2d_border_param 3. Deleted 2D computation attribute structure `k_venc_2d_attr` 4. Added description of OSD background layer format 5. Added some MAPI function interfaces and data types, specifically in Chapter 4 MAPI |
| V1.2             | System Software Department | 2023.04.27 | 1. Modified line width parameter of 2D border structure k_venc_2d_border_attr 2. Modified 2D user-defined conversion coefficient API name kd_mpi_venc_set_2d_custom_coef 3. Modified conversion coefficient parameter type of kd_mpi_venc_set_2d_custom_coef 4. Added interface for getting conversion coefficients kd_mpi_venc_get_2d_custom_coef 5. Added color gamut setting/getting interfaces kd_mpi_venc_set_2d_color_gamut, kd_mpi_venc_get_2d_color_gamut 6. Modified rotation angle parameter of kd_mpi_venc_set_rotaion 7. Modified input format description of JPEG in video encoding function |
| V1.2.1           | System Software Department | 2023-04-28 | 1. Added GOP attribute in k_venc_chn_attr |
| V1.2.2           | System Software Department | 2023-05-24 | 1. Added image flip setting/getting interfaces kd_mpi_venc_set_mirror, kd_mpi_venc_get_mirror 2. Added IDR frame enable interface kd_mpi_venc_enable_idr |
| V1.3             | System Software Department | 2023-05-25 | 1. Added IDR frame enable interface in MAPI kd_mapi_venc_request_idr |
| V1.3.1           | System Software Department | 2023-06-14 | 1. Added mpi setting for decoding output downscaled image kd_mpi_vdec_set_downscale |
| V1.3.2           | System Software Department | 2023-06-19 | 1. Modified kd_mapi_venc_request_idr 2. Added kd_mpi_venc_request_idr, kd_mapi_venc_enable_idr 3. Added H.265 SAO setting/getting interfaces kd_mpi_venc_set_h265_sao, kd_mpi_venc_get_h265_sao 4. Added deblocking setting/getting interfaces kd_mpi_venc_set_dblk, kd_mpi_venc_get_dblk 5. Added ROI interfaces kd_mpi_venc_set_roi_attr, kd_mpi_venc_get_roi_attr |
| V1.3.3           | System Software Department | 2023-06-20 | 1. Added H.264/H.265 entropy coding mode setting/getting interfaces kd_mpi_venc_set_h264_entropy, kd_mpi_venc_get_h264_entropy, kd_mpi_venc_set_h265_entropy, kd_mpi_venc_get_h265_entropy 2. Renamed k_venc_rotation enumeration to k_rotation 3. Added decoding rotation setting interface kd_mpi_vdec_set_rotation |
| V1.3.4           | System Software Department | 2023-06-30 | Modified data types supported by encoding, decoding, and 2D |

## 1. Overview

### 1.1 Overview

The video encoding and decoding module supports H.264, H.265, and JPEG encoding and decoding. The VENC module implements 2D computation and encoding functions, which can be enabled simultaneously or used separately. The VDEC module implements decoding functions.

VENC, VENC+2D, and VDEC support system binding, while 2D computation alone does not support system binding.

### 1.2 Function Description

#### 1.2.1 Video Encoding

![encode flow](../../../../zh/01_software/board/mpp/images/9f7f41ea96a97ae9bf514535f6af1622.jpeg)

Figure 1-1 Encoding Data Flow Diagram

The typical encoding process includes receiving the input image, masking and overlaying the image content, encoding the image, and outputting the code stream.

The encoding module consists of the VENC receiving channel, encoding channel, 2D receiving channel, and 2D computation module. The encoding and 2D computation capabilities are shown in the table below.

The green arrows in the encoding data flow diagram indicate the process of 2D computation alone. The blue arrows indicate the process of encoding alone. The purple arrows indicate the process of 2D computation followed by encoding.

Table 1-1 Encoding Capabilities

| | H264 | HEVC | JPEG |
|---|---|---|---|
| Input Format | YUV420 NV12 8bit, ARGB8888, BGRA8888 | YUV420 NV12 8bit, ARGB8888, BGRA8888 | YUV420 NV12 8bit, YUV422 UYVY 8bit, ARGB8888, BGRA8888 |
| Output Format | YUV420 H.264 Baseline Profile(BP); H.264 Main Profile(MP); H.264 High Profile(HP); H.264 High 10 Profile(HP) | YUV420 HEVC (H.265) Main; HEVC (H.265) Main 10 Profile | YUV420 and YUV422 JPEG baseline sequential |
| Maximum Resolution | 3840x2160 | 3840x2160 | 8192x8192 |
| Bitrate Control Mode | CBR/VBR/FIXQP | CBR/VBR/FIXQP | FIXQP |
| GOP | I/P frames | I/P frames | - |
| Encoding Channels | 4 channels | 4 channels | 4 channels |

Note: H264/HEVC/JPEG share 4 channels.

Table 1-2 2D Computation Capabilities

| Video Input Format | Video Output Format | Overlay Data Format | Maximum Resolution |
|--------------------|---------------------|---------------------|--------------------|
| I420/NV12/ARGB8888/BGRA8888 | Same as input format | ARGB8888/ARGB4444/ARGB1555 | 3840x2160 |

##### 1.2.1.1 Encoding Channel

The encoding channel serves as the basic container, storing various user settings and managing various internal resources of the encoding channel. The encoding channel completes the functions of image overlay and encoding. The 2D module performs image overlay computation, and the encoder module performs image encoding. Both can be used separately or in conjunction.

![encode channel](../../../../zh/01_software/board/mpp/images/d8ea12750bef3150afebf98c8a4563fd.jpeg)

Figure 1-2 Encoding Channel

##### 1.2.1.2 Bitrate Control

The bitrate controller manages the control of the encoding bitrate.

From an information theory perspective, the lower the compression ratio of an image, the higher the quality of the compressed image; the higher the compression ratio, the lower the quality of the compressed image. Under varying scene conditions, if stable image quality is pursued, the encoding bitrate will fluctuate significantly; if stable encoding bitrate is pursued, the image quality will fluctuate significantly.

H264/H265 encoding supports CBR, VBR, and FIXQP bitrate control modes.

MJPEG only supports FIXQP mode.

###### 1.2.1.2.1 CBR

(Constant Bit Rate) Fixed bitrate. Ensures stable encoding bitrate within the bitrate statistics time.

###### 1.2.1.2.2 VBR

(Variable Bit Rate) Allows bitrate fluctuations within the bitrate statistics time to ensure stable image quality.

###### 1.2.1.2.3 FIXQP

Fixed QP value. Within the bitrate statistics time, all macroblock QP values of the encoded image are the same, using the user-set image QP value.

##### 1.2.1.3 GOP Structure

This module only supports I-frames and P-frames.

##### 1.2.1.4 2D Computation

The 2D computation module can achieve OSD overlay on image data. The OSD mode can achieve overlay of 8 regions, with no overlap between regions. Supported OSD formats are: ARGB4444/ARGB1555/ARGB8888.

###### 1.2.1.4.1 2D Conversion Coefficient Calculation

During OSD overlay computation, if the input video format is YUV, the OSD layer needs to perform RGB to YUV conversion. The kernel has a set of default conversion coefficients. If the user needs to customize a set of 12-bit conversion coefficients, they can be obtained from the RGB to YUV conversion formula.

The known RGB to YUV conversion formula is as follows:

![osd formula](../../../../zh/01_software/board/mpp/images/osd_formula.png)

The coefficients in the 3x3 matrix are obtained by multiplying by 256 and rounding to the nearest integer, and the values in the 3x1 matrix are the corresponding conversion coefficients.

For example, for BT709 LIMITED, the RGB to YUV conversion formula is:

Y = 0.1826\*R + 0.6142\*G + 0.0620\*B + 16

U = -0.1007\*R - 0.3385\*G + 0.4392\*B + 128

V = 0.4392\*R - 0.3990\*G - 0.0402\*B + 128

The conversion coefficients are: { 47, 157, 16, 16, -26, -86, 112, 128, 112, -102, -10, 128 }

###### 1.2.1.4.2 2D Conversion Coefficient Configuration

2D conversion coefficients can be configured through the user-defined coefficient interface [kd_mpi_venc_set_2d_custom_coef](#2120-kd_mpi_venc_set_2d_custom_coef) and the color gamut configuration interface [kd_mpi_venc_set_2d_color_gamut](#2122-kd_mpi_venc_set_2d_color_gamut). Either interface can be used for configuration. If neither interface is called before the computation starts, the default coefficients will be used for color gamut conversion.

##### 1.2.1.5 Limitations

Encoding operations have the following limitations:

1. If the input data format is YUV420, the physical starting address of the image data for each component (Y, U, V) must be 4k aligned.
1. If the input data format is NV12, the physical starting address of the image data for Y and UV must be 4k aligned.

2D operations have the following limitations:

1. The physical starting address of the source and destination images in DDR must be 8-byte aligned.
1. The dimensions of the image, OSD, and frame in the overlay and frame operations must be even numbers.
1. The src and dst addresses of video data in overlay and frame operations must be the same.

Decoding operations have the following limitations:

1. The physical starting address of the input data for each frame must be 4k aligned.

##### 1.2.1.6 Typical Encoding Application Example

![venc sample flow](../../../../zh/01_software/board/mpp/images/e57bfe4e5657980663f22e7cdef1f182.jpeg)

Figure 1-3 Typical Encoding Application Scenario Flow Diagram

### 1.2.2 Video Decoding

Table 12 VPU Decoding Capabilities

| | H264 | HEVC | JPEG |
|:--|:--|:--|:--|
| Input Format | H.264 Baseline; H.264 Main; H.264 High; H.264 High10; supports interlaced stream | HEVC (H.265) Main/Main10 | JPEG, baseline sequential |
| Output Format | YUV420 NV12 | YUV420 NV12 | YUV422 UYVY, YUV420 NV12 |
| Decoding Channels | 4 channels | 4 channels | 4 channels |

Note: H264/HEVC/JPEG share 4 channels.

VDEC supports streaming mode:

- Streaming Mode (K_VDEC_SEND_MODE_STREAM): Users can send any length of code stream to the decoder each time, and the decoder will internally complete the identification process of one frame of the code stream. Note that for H.264/H.265, the end of the current frame code stream can only be identified after receiving the next frame code stream, so in this sending mode, if you input one frame of H.264/H.265 code stream, you cannot expect the image decoding to start immediately.

#### 1.2.2.1 Typical Decoding Application Example

![vdec sample flow](../../../../zh/01_software/board/mpp/images/e49f8a05613f3b2524e3dc075009146e.jpeg)

Figure 1-3 Typical Encoding Application Scenario Flow Diagram

## 2. API Reference

### 2.1 Video Encoding

This functional module provides the following APIs:

- [kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn): Create an encoding channel.
- [kd_mpi_venc_destory_chn](#212-kd_mpi_venc_destory_chn): Destroy an encoding channel.
- [kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn): Start the encoding channel to receive input images.
- [kd_mpi_venc_stop_chn](#214-kd_mpi_venc_stop_chn): Stop the encoding channel from receiving input images.
- [kd_mpi_venc_query_status](#215-kd_mpi_venc_query_status): Query the status of the encoding channel.
- [kd_mpi_venc_get_stream](#216-kd_mpi_venc_get_stream): Get the encoded stream.
- [kd_mpi_venc_release_stream](#217-kd_mpi_venc_release_stream): Release the stream buffer.
- [kd_mpi_venc_send_frame](#218-kd_mpi_venc_send_frame): Support users to send raw images for encoding.
- [kd_mpi_venc_set_rotation](#219-kd_mpi_venc_set_rotation): Set the rotation angle of the encoded image.
- [kd_mpi_venc_get_rotation](#2110-kd_mpi_venc_get_rotation): Get the rotation angle of the encoded image.
- [kd_mpi_venc_set_mirror](#2111-kd_mpi_venc_set_mirror): Set the rotation angle of the encoded image.
- [kd_mpi_venc_get_mirror](#2112-kd_mpi_venc_get_mirror): Get the mirroring method of the encoded image.
- [kd_mpi_venc_enable_idr](#2113-kd_mpi_venc_enable_idr): Enable IDR frame, generating IDR frames according to the GOP interval.
- [kd_mpi_venc_set_2d_mode](#2114-kd_mpi_venc_set_2d_mode): Set the 2D computation mode.
- [kd_mpi_venc_get_2d_mode](#2115-kd_mpi_venc_get_2d_mode): Get the 2D computation mode.
- [kd_mpi_venc_set_2d_osd_param](#2116-kd_mpi_venc_set_2d_osd_param): Set the region attributes of OSD in 2D computation.
- [kd_mpi_venc_get_2d_osd_param](#2117-kd_mpi_venc_get_2d_osd_param): Get the region attributes of the specified index OSD in 2D computation.
- [kd_mpi_venc_set_2d_border_param](#2118-kd_mpi_venc_set_2d_border_param): Set the frame attributes in 2D computation.
- [kd_mpi_venc_get_2d_border_param](#2119-kd_mpi_venc_get_2d_border_param): Get the frame attributes in 2D computation.
- [kd_mpi_venc_set_2d_custom_coef](#2120-kd_mpi_venc_set_2d_custom_coef): Set the image format conversion coefficients in 2D computation.
- [kd_mpi_venc_get_2d_custom_coef](#2121-kd_mpi_venc_get_2d_custom_coef): Get the image format conversion coefficients in 2D computation.
- [kd_mpi_venc_set_2d_color_gamut](#2122-kd_mpi_venc_set_2d_color_gamut): Set the color gamut for 2D computation.
- [kd_mpi_venc_get_2d_color_gamut](#2123-kd_mpi_venc_get_2d_color_gamut): Get the color gamut for 2D computation.
- [kd_mpi_venc_attach_2d](#2124-kd_mpi_venc_attach_2d): Associate 2D computation with VENC.
- [kd_mpi_venc_detach_2d](#2125-kd_mpi_venc_detach_2d): Disassociate 2D computation from VENC.
- [kd_mpi_venc_send_2d_frame](#2126-kd_mpi_venc_send_2d_frame): Send a frame of data to the 2D module.
- [kd_mpi_venc_get_2d_frame](#2127-kd_mpi_venc_get_2d_frame): Get the result of 2D computation.
- [kd_mpi_venc_start_2d_chn](#2128-kd_mpi_venc_start_2d_chn): Start the 2D channel to receive input images.
- [kd_mpi_venc_stop_2d_chn](#2129-kd_mpi_venc_stop_2d_chn): Stop the 2D channel from receiving input images.
- [kd_mpi_venc_request_idr](#2130-kd_mpi_venc_request_idr): Request an IDR frame, generating an IDR frame immediately after calling.
- [kd_mpi_venc_set_h265_sao](#2131-kd_mpi_venc_set_h265_sao): Set the Sao attributes for the H.265 channel.
- [kd_mpi_venc_get_h265_sao](#2132-kd_mpi_venc_get_h265_sao): Get the Sao attributes for the H.265 channel.
- [kd_mpi_venc_set_dblk](#2133-kd_mpi_venc_set_dblk): Enable deblocking for the codec channel.
- [kd_mpi_venc_get_dblk](#2134-kd_mpi_venc_get_dblk): Get the deblocking status of the codec channel.
- [kd_mpi_venc_set_roi_attr](#2135-kd_mpi_venc_set_roi_attr): Set the ROI attributes for the H.264/H.265 channel.
- [kd_mpi_venc_get_roi_attr](#2136-kd_mpi_venc_get_roi_attr): Get the ROI attributes for the H.264/H.265 channel.
- [kd_mpi_venc_set_h264_entropy](#2137-kd_mpi_venc_set_h264_entropy): Set the entropy encoding mode for the H.264 codec channel.
- [kd_mpi_venc_get_h264_entropy](#2138-kd_mpi_venc_get_h264_entropy): Get the entropy encoding mode for the H.264 codec channel.
- [kd_mpi_venc_set_h265_entropy](#2139-kd_mpi_venc_set_h265_entropy): Set the entropy encoding mode for the H.265 codec channel.
- [kd_mpi_venc_get_h265_entropy](#2140-kd_mpi_venc_get_h265_entropy): Get the entropy encoding mode for the H.265 codec channel.

#### 2.1.1 kd_mpi_venc_create_chn

**Description**:

Create an encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_create_chn(k_u32 chn_num, const [k_venc_chn_attr](#3115-k_venc_chn_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Encoding channel information. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| attr     | Pointer to encoding channel attributes. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5. Error Codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- The encoder supports channel width and height as shown in the table below:

| H.264/H.265 | JPEG   |       |        |      |     |      |     |
|-------------|--------|-------|--------|------|-----|------|-----|
| WIDTH       | HEIGHT | WIDTH | HEIGHT |      |     |      |     |
| MAX         | MIN    | MAX   | MIN    | MAX  | MIN | MAX  | MIN |
| 4096        | 128    | 4096  | 64     | 8192 | 128 | 8192 | 64  |

**Examples**:

None.

**Related Topics**:

None.

#### 2.1.2 kd_mpi_venc_destory_chn

**Description**:

Destroy an encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_destory_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5. Error Codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- Must stop receiving images before destroying, otherwise returns failure.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_stop_chn](#214-kd_mpi_venc_stop_chn)

#### 2.1.3 kd_mpi_venc_start_chn

**Description**:

Start the encoding channel to receive input images.

**Syntax**:

```c
k_s32 kd_mpi_venc_start_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5. Error Codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If the channel is not created, it returns failure K_ERR_VENC_UNEXIST.
- If the channel has already started receiving images and calls this interface again without stopping, it returns operation not allowed.
- The encoder starts receiving images for encoding only after starting reception.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn)
[kd_mpi_venc_stop_chn](#214-kd_mpi_venc_stop_chn)

#### 2.1.4 kd_mpi_venc_stop_chn

**Description**:

Stop the encoding channel from receiving input images.

**Syntax**:

```c
k_s32 kd_mpi_venc_stop_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5. Error Codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If the channel is not created, it returns failure.
- This interface does not check if the reception is already stopped, allowing repeated stops without returning an error.
- This interface is used to stop receiving images for encoding, and must be called before destroying or resetting the encoding channel.
- Calling this interface only stops receiving raw data for encoding, the stream buffer will not be cleared.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_destory_chn](#212-kd_mpi_venc_destory_chn)

#### 2.1.5 kd_mpi_venc_query_status

**Description**:

Query the status of the encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_query_status(k_u32 chn_num, [k_venc_chn_status](#3115-k_venc_chn_attr) *status);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| status   | Pointer to the status of the encoding channel. | Output |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5. Error Codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Examples**:

None.

**Related Topics**:

None.
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If the channel is not created, it returns failure.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn)

#### 2.1.6 kd_mpi_venc_get_stream

**Description**:

Get the encoded stream.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_stream(k_u32 chn_num, [k_venc_stream](#3123-k_venc_stream) *stream, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| stream  | Pointer to the stream structure. | Output |
| milli_sec | Timeout for getting the stream. Value range: [-1, +∞) -1: Blocking. 0: Non-blocking. Greater than 0: Timeout | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If the channel is not created, it returns failure.
- If `stream` is null, it returns K_ERR_VENC_NULL_PTR.
- If `milli_sec` is less than -1, it returns K_ERR_VENC_ILLEGAL_PARAM.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn)
[kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn)

#### 2.1.7 kd_mpi_venc_release_stream

**Description**:

Release the stream buffer.

**Syntax**:

```c
k_s32 kd_mpi_venc_release_stream(k_u32 chn_num, [k_venc_stream](#3123-k_venc_stream) *stream);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| stream  | Pointer to the stream structure. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If the channel is not created, it returns error code K_ERR_VENC_UNEXIST.
- If `stream` is null, it returns error code K_ERR_VENC_NULL_PTR.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn)
[kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn)

#### 2.1.8 kd_mpi_venc_send_frame

**Description**:

Support users to send raw images for encoding.

**Syntax**:

```c
k_s32 kd_mpi_venc_send_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Encoding channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| frame   | Pointer to the raw image information structure, refer to "K230 System Control API Reference". | Input |
| milli_sec | Timeout for sending the image. Value range: [-1, +∞) -1: Blocking. 0: Non-blocking. Greater than 0: Timeout. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface supports users sending images to the encoding channel.
- If `milli_sec` is less than -1, it returns K_ERR_VENC_ILLEGAL_PARAM.
- When calling this interface to send images, users need to ensure that the encoding channel is created and started to receive input images.

**Examples**:

None.

**Related Topics**:

[kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn)
[kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn)

#### 2.1.9 kd_mpi_venc_set_rotation

**Description**:

Set the rotation angle of the encoded image.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_rotation(k_u32 chn_num, const [k_rotation](#3112-k_rotation) rotation);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| rotation | Rotation angle enumeration. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.10 kd_mpi_venc_get_rotation

**Description**:

Get the rotation angle of the encoded image.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_rotation(k_u32 chn_num, [k_rotation](#3112-k_rotation) *rotation);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [VENC_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| rotation | Pointer to the rotation angle enumeration. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.11 kd_mpi_venc_set_mirror

**Description**:

Set the mirroring method of the encoded image.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_mirror(k_u32 chn_num, const [k_venc_mirror](#3113-k_venc_mirror) mirror);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Channel number. Value range: [0, VENC_MAX_CHN_NUM). | Input |
| mirror  | Mirroring method enumeration. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.12 kd_mpi_venc_get_mirror

**Description**:

Get the mirroring method of the encoded image.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_mirror(k_u32 chn_num, [k_venc_mirror](#3113-k_venc_mirror) *mirror);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Channel number. Value range: [0, VENC_MAX_CHN_NUM). | Input |
| mirror  | Pointer to the mirroring method enumeration. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.13 kd_mpi_venc_enable_idr

**Description**:

Enable IDR frame.

**Syntax**:

```c
k_s32 kd_mpi_venc_enable_idr(k_u32 chn_num, const k_bool idr_enable);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num   | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| idr_enable | Enable IDR frame. 0: Disable. 1: Enable. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface needs to be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.14 kd_mpi_venc_set_2d_mode

**Description**:

Set the 2D computation mode.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_2d_mode(k_u32 chn_num, const [k_venc_2d_calc_mode](#318-k_venc_2d_calc_mode) mode);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| mode    | 2D computation mode enumeration. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- Currently, the computation mode does not support K_VENC_2D_CALC_MODE_CSC mode.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.15 kd_mpi_venc_get_2d_mode

**Description**:

Get the 2D computation mode.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_mode(k_u32 chn_num, [k_venc_2d_calc_mode](#318-k_venc_2d_calc_mode) *mode);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| mode    | Pointer to the 2D computation mode enumeration. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- Currently, the computation mode does not support K_VENC_2D_CALC_MODE_CSC mode.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.16 kd_mpi_venc_set_2d_osd_param

**Description**:

Set the region attributes of OSD in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_2d_osd_param(k_u32 chn_num, k_u8 index, const [k_venc_2d_osd_attr](#3125-k_venc_2d_osd_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| index    | OSD region index. Value range: [0, [K_VENC_MAX_2D_OSD_REGION_NUM](#312-k_venc_max_2d_osd_region_num)). | Input |
| attr     | Pointer to OSD attributes. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If there are n overlay regions, the index values should be set to 0~n-1 respectively.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.17 kd_mpi_venc_get_2d_osd_param

**Description**:

Get the region attributes of the OSD with the specified index in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_osd_param(k_u32 chn_num, k_u8 index, const [k_venc_2d_osd_attr](#3125-k_venc_2d_osd_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| index    | OSD region index. Value range: [0, [K_VENC_MAX_2D_OSD_REGION_NUM](#312-k_venc_max_2d_osd_region_num)). | Input |
| attr     | Pointer to OSD attributes. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.18 kd_mpi_venc_set_2d_border_param

**Description**:

Set the border attributes in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_2d_border_param(k_u32 chn_num, k_u8 index, const [k_venc_2d_border_attr](#3126-k_venc_2d_border_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| index    | Border index. Value range: [0, [K_VENC_MAX_2D_BORDER_NUM](#313-k_venc_max_2d_border_num)). | Input |
| attr     | Pointer to border attributes. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- If there are n borders, the index values should be set to 0~n-1 respectively.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.19 kd_mpi_venc_get_2d_border_param

**Description**:

Get the border attributes in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_border_param(k_u32 chn_num, k_u8 index, [k_venc_2d_border_attr](#3126-k_venc_2d_border_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| index    | Border index. Value range: [0, [K_VENC_MAX_2D_BORDER_NUM](#313-k_venc_max_2d_border_num)). | Input |
| attr     | Pointer to border attributes. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.20 kd_mpi_venc_set_2d_custom_coef

**Description**:

Set the image format conversion coefficients in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_2d_custom_coef(k_u32 chn_num, const k_s16 *coef);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| coef     | Pointer to conversion coefficients. Refer to [2D Conversion Coefficient Calculation](#12141-2D Conversion Coefficient Calculation). | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- The kernel has a set of default conversion coefficients. If custom conversion coefficients are needed, they can be configured through this interface.
- This interface should be called after setting the computation mode.
- For details on conversion coefficients, refer to [2D Conversion Coefficient Calculation](#12141-2D Conversion Coefficient Calculation).
- When the computation mode is K_VENC_2D_CALC_MODE_BORDER, conversion coefficients are not applicable, and calling this interface will result in an error.

**Example**:

None.

**Related Topics**:

[kd_mpi_venc_set_2d_mode](#2114-kd_mpi_venc_set_2d_mode)

#### 2.1.21 kd_mpi_venc_get_2d_custom_coef

**Description**:

Get the image format conversion coefficients in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_custom_coef(k_u32 chn_num, k_s16 *coef);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| coef     | Pointer to conversion coefficients. Refer to [2D Conversion Coefficient Calculation](#12141-2D Conversion Coefficient Calculation). | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after setting the computation mode.
- When the computation mode is K_VENC_2D_CALC_MODE_BORDER, conversion coefficients are not applicable, and calling this interface will result in an error.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.22 kd_mpi_venc_set_2d_color_gamut

**Description**:

Set the color gamut in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_2d_color_gamut(k_u32 chn_num, const [k_venc_2d_color_gamut](#3114-k_venc_2d_color_gamut) color_gamut);
```

**Parameters**:

| Parameter Name    | Description | Input/Output |
|---|---|---|
| chn_num     | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| color_gamut | Color gamut enumeration. | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- The kernel has a set of default conversion coefficients. If custom conversion coefficients are needed, they can be configured through this interface.
- This interface should be called after setting the computation mode.
- When the computation mode is K_VENC_2D_CALC_MODE_BORDER, color gamut is not applicable, and calling this interface will result in an error.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.23 kd_mpi_venc_get_2d_color_gamut

**Description**:

Get the color gamut in 2D computation.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_color_gamut(k_u32 chn_num, [k_venc_2d_color_gamut](#3114-k_venc_2d_color_gamut) *color_gamut);
```

**Parameters**:

| Parameter Name    | Description | Input/Output |
|---|---|---|
| chn_num     | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| color_gamut | Pointer to color gamut enumeration. | Output |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- The kernel has a set of default conversion coefficients. If custom conversion coefficients are needed, they can be configured through this interface.
- This interface should be called after setting the computation mode.
- When the computation mode is K_VENC_2D_CALC_MODE_BORDER, color gamut is not applicable, and calling this interface will result in an error.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.24 kd_mpi_venc_attach_2d

**Description**:

Attach 2D computation to VENC.

**Syntax**:

```c
k_s32 kd_mpi_venc_attach_2d(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- Currently, binding only supports the mode where the encoding channel number and the 2D computation channel number are the same. Only the first 3 encoding channels support the attach 2D operation.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.25 kd_mpi_venc_detach_2d

**Description**:

Detach 2D computation from VENC.

**Syntax**:

```c
k_s32 kd_mpi_venc_detach_2d(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | 2D computation channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|--------|-------------------------------|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- When calling this interface, users need to ensure that the encoding channel has stopped.

**Example**:

None.

**Related Topics**:

[kd_mpi_venc_stop_chn](#214-kd_mpi_venc_stop_chn)

#### 2.1.26 kd_mpi_venc_send_2d_frame

**Description**:

Send a frame of data to the 2D module.

**Syntax**:

```c
k_s32 kd_mpi_venc_send_2d_frame(k_u32 chn_num, const k_video_frame_info *frame, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | 2D computation channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| frame | Pointer to the original image information structure. Refer to the "K230 System Control API Reference". | Input |
| milli_sec | Timeout for sending the image. Value range: [-1, +∞) -1: Blocking. 0: Non-blocking. > 0: Timeout duration. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface is used only in scenarios involving single 2D computation. For scenarios involving 2D computation followed by encoding, use the VENC interface [kd_mpi_venc_send_frame](#218-kd_mpi_venc_send_frame) to send the image.

**Example**:

None.

**Related Topics**:

[kd_mpi_venc_send_frame](#218-kd_mpi_venc_send_frame)

#### 2.1.27 kd_mpi_venc_get_2d_frame

**Description**:

Get the 2D computation result.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_2d_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | 2D computation channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| frame | Pointer to the output image information structure. Refer to the "K230 System Control API Reference". | Output |
| milli_sec | Timeout for sending the image. Value range: [-1, +∞) -1: Blocking. 0: Non-blocking. > 0: Timeout duration. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface is used only in scenarios involving single 2D computation. For scenarios involving 2D computation followed by encoding, use [kd_mpi_venc_get_stream](#216-kd_mpi_venc_get_stream) to get the encoded stream.

**Example**:

None.

**Related Topics**:

[kd_mpi_venc_get_stream](#216-kd_mpi_venc_get_stream)

#### 2.1.28 kd_mpi_venc_start_2d_chn

**Description**:

Start the 2D channel to receive input images.

**Syntax**:

```c
k_s32 kd_mpi_venc_start_2d_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | 2D computation channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h

**Notes**:

- This interface is used only in scenarios involving single 2D computation. For VENC+2D scenarios, use [kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn).

**Example**:

None.

**Related Topics**:

[kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn)

#### 2.1.29 kd_mpi_venc_stop_2d_chn

**Description**:

Stop the 2D channel from receiving input images.

**Syntax**:

```c
k_s32 kd_mpi_venc_stop_2d_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num | 2D computation channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.30 kd_mpi_venc_request_idr

**Description**:

Request an IDR frame, generating one immediately after the call.

**Syntax**:

```c
k_s32 kd_mpi_venc_request_idr(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.31 kd_mpi_venc_set_h265_sao

**Description**:

Set the Sao attributes for the H.265 channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_h265_sao(k_u32 chn_num, const [k_venc_h265_sao](#3127-k_venc_h265_sao) *h265_sao);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h265_sao | Sao configuration for the H.265 encoding channel. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.32 kd_mpi_venc_get_h265_sao

**Description**:

Get the Sao attributes for the H.265 channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_h265_sao(k_u32 chn_num, [k_venc_h265_sao](#3127-k_venc_h265_sao) *h265_sao);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h265_sao | Sao configuration for the H.265 encoding channel. | Output |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.33 kd_mpi_venc_set_dblk

**Description**:

Enable or disable deblocking for the H.264/H.265 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_dblk(k_u32 chn_num, const k_bool dblk_en);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| dblk_en | Enable or disable deblocking. K_TRUE: Enable. K_FALSE: Disable. Default is enabled. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.34 kd_mpi_venc_get_dblk

**Description**:

Get the deblocking status of the H.264/H.265 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_dblk(k_u32 chn_num, k_bool *dblk_en);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| dblk_en | Enable or disable deblocking. K_TRUE: Enable. K_FALSE: Disable. Default is enabled. | Output |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.35 kd_mpi_venc_set_roi_attr

**Description**:

Set the ROI attributes for the H.264/H.265 channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_roi_attr(k_u32 chn_num, const [k_venc_roi_attr](#3129-k_venc_roi_attr) *roi_attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| roi_attr | ROI attributes for the H.264/H.265 encoding channel. | Input |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.36 kd_mpi_venc_get_roi_attr

**Description**:

Get the ROI attributes for the H.264/H.265 channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_roi_attr(k_u32 chn_num, [k_venc_roi_attr](#3129-k_venc_roi_attr) *roi_attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| roi_attr | ROI attributes for the H.264/H.265 encoding channel. | Output |

**Return Values**:

| Return Value | Description |
|---|---|
| 0      | Success. |
| Non-zero | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.37 kd_mpi_venc_set_h264_entropy

**Description**:

Set the entropy encoding mode for the H.264 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_h264_entropy(k_u32 chn_num, const [k_venc_h264_entropy](#3130-k_venc_h264_entropy) *h264_entropy);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h264_entropy | Entropy encoding mode for the H.264 encoding channel. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.38 kd_mpi_venc_get_h264_entropy

**Description**:

Get the entropy encoding mode for the H.264 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_h264_entropy(k_u32 chn_num, [k_venc_h264_entropy](#3130-k_venc_h264_entropy) *h264_entropy);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h264_entropy | Entropy encoding mode for the H.264 encoding channel. | Output |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.39 kd_mpi_venc_set_h265_entropy

**Description**:

Set the entropy encoding mode for the H.265 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_set_h265_entropy(k_u32 chn_num, const [k_venc_h265_entropy](#3131-k_venc_h265_entropy) *h265_entropy);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h265_entropy | Entropy encoding mode for the H.265 encoding channel. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

- This interface should be called after creating the encoding channel and before starting the encoding channel.

**Example**:

None.

**Related Topics**:

None.

#### 2.1.40 kd_mpi_venc_get_h265_entropy

**Description**:

Get the entropy encoding mode for the H.265 encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_venc_get_h265_entropy(k_u32 chn_num, [k_venc_h265_entropy](#3131-k_venc_h265_entropy) *h265_entropy);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VENC_2D_MAX_CHN_NUM](#311-venc_max_chn_num)). | Input |
| h265_entropy | Entropy encoding mode for the H.265 encoding channel. | Output |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_venc_api.h, k_type.h, k_module.h, k_sys_comm.h, k_venc_comm.h
- Library files: libvenc.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

### 2.2 Video Decoding

This module provides the following APIs:

- [kd_mpi_vdec_create_chn](#221-kd_mpi_vdec_create_chn): Create a video decoding channel.
- [kd_mpi_vdec_destroy_chn](#222-kd_mpi_vdec_destroy_chn): Destroy a video decoding channel.
- [kd_mpi_vdec_start_chn](#223-kd_mpi_vdec_start_chn): Start a video decoding channel.
- [kd_mpi_vdec_stop_chn](#224-kd_mpi_vdec_stop_chn): Stop a video decoding channel.
- [kd_mpi_vdec_query_status](#225-kd_mpi_vdec_query_status): Query the status of the decoding channel.
- [kd_mpi_vdec_send_stream](#226-kd_mpi_vdec_send_stream): Send stream data to the video decoding channel.
- [kd_mpi_vdec_get_frame](#227-kd_mpi_vdec_get_frame): Get the decoded image from the video decoding channel.
- [kd_mpi_vdec_release_frame](#228-kd_mpi_vdec_release_frame): Release the decoded image from the video decoding channel.
- [kd_mpi_vdec_set_downscale](#229-kd_mpi_vdec_set_downscale): Set the downscaling of the output image (specify width and height or by ratio).
- [kd_mpi_vdec_set_rotation](#2210-kd_mpi_vdec_set_rotation): Set the rotation angle of the decoded image.

#### 2.2.1 kd_mpi_vdec_create_chn

**Description**:

Create a video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_create_chn(k_u32 chn_num, const [k_vdec_chn_attr](#323-k_vdec_chn_attr) *attr);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| attr     | Pointer to the decoding channel attributes. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.2 kd_mpi_vdec_destroy_chn

**Description**:

Destroy a video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_destroy_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description  | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.3 kd_mpi_vdec_start_chn

**Description**:

Start a video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_start_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.4 kd_mpi_vdec_stop_chn

**Description**:

Stop a video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_stop_chn(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.5 kd_mpi_vdec_query_status

**Description**:

Query the status of the decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_query_status(k_u32 chn_num, [k_vdec_chn_status](#324-k_vdec_chn_status) *status);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| status   | Pointer to the video decoding channel status structure. | Output |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.6 kd_mpi_vdec_send_stream

**Description**:

Send stream data to the video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_send_stream(k_u32 chn_num, const [k_vdec_stream](#326-k_vdec_stream) *stream, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name  | Description | Input/Output |
|---|---|---|
| chn_num   | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| stream    | Pointer to the decoding stream data. | Input |
| milli_sec | Timeout flag for sending stream. Value range: -1: Blocking. 0: Non-blocking. Positive value: Timeout duration in milliseconds, no upper limit. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.7 kd_mpi_vdec_get_frame

**Description**:

Get the decoded image from the video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_get_frame(k_u32 chn_num, k_video_frame_info *frame_info, [k_vdec_supplement_info](#327-k_vdec_supplement_info) *supplement, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name   | Description | Input/Output |
|---|---|---|
| chn | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| frame_info | Pointer to the decoded image information. Refer to the "K230 System Control API Reference". | Output |
| supplement | Pointer to the decoded image supplementary information. | Output |
| milli_sec  | Timeout flag for sending stream. Value range: -1: Blocking. 0: Non-blocking. Positive value: Timeout duration in milliseconds. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes). |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.
**Positive Value**: Timeout duration, no upper limit, in milliseconds. Dynamic attribute. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes).  |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.8 kd_mpi_vdec_release_frame

**Description**:

Release the decoded image from the video decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_vdec_release_frame(k_u32 chn_num, const k_video_frame_info *frame_info);
```

**Parameters**:

| Parameter Name   | Description | Input/Output |
|---|---|---|
| chn        | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| frame_info | Pointer to the decoded image information obtained by the [kd_mpi_vdec_get_frame](#227-kd_mpi_vdec_get_frame) interface. Refer to the "K230 System Control API Reference". | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes).  |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mpi_vdec_get_frame](#227-kd_mpi_vdec_get_frame)

#### 2.2.9 kd_mpi_vdec_set_downscale

**Description**:

Set the downscaling of the output image (specify width and height or by ratio).

**Syntax**:

```c
k_s32 kd_mpi_vdec_set_downscale(k_u32 chn_num, const [k_vdec_downscale](#3211-k_vdec_downscale) *downscale);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| downscale    | Pointer to the downscaling parameter structure. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes).  |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

Set between kd_mpi_vdec_create_chn and kd_mpi_vdec_start_chn.

**Example**:

None.

**Related Topics**:

None.

#### 2.2.10 kd_mpi_vdec_set_rotation

**Description**:

Set the rotation angle of the decoded image.

**Syntax**:

```c
k_s32 kd_mpi_vdec_set_rotation(k_u32 chn_num, const [k_rotation](#3112-k_rotation) rotation);
```

**Parameters**:

| Parameter Name | Description | Input/Output |
|---|---|---|
| chn_num  | Channel number. Value range: [0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num)). | Input |
| rotation | Rotation angle enumeration. | Input |

**Return Values**:

| Return Value | Description                          |
|--------|-------------------------------|
| 0      | Success.                         |
| Non-zero    | Failure, see [Error Codes](#5-error-codes).  |

**Chip Differences**:

None.

**Requirements**:

- Header files: mpi_vdec_api.h, k_type.h, k_module.h, k_sys_comm.h, k_vdec_comm.h
- Library files: libvdec.a

**Notes**:

Set between kd_mpi_vdec_create_chn and kd_mpi_vdec_start_chn.

**Example**:

None.

**Related Topics**:

None.

## 3. Data Types

### 3.1 Video Encoding

The related data type definitions for this module are as follows:

- [VENC_MAX_CHN_NUM](#311-venc_max_chn_num): Defines the maximum number of channels.
- [K_VENC_MAX_2D_OSD_REGION_NUM](#312-k_venc_max_2d_osd_region_num): Defines the maximum number of 2D OSD regions.
- [K_VENC_MAX_2D_BORDER_NUM](#313-k_venc_max_2d_border_num): Defines the maximum number of 2D borders.
- [K_VENC_2D_COFF_NUM](#314-k_venc_2d_coff_num): Defines the number of 2D CSC conversion coefficients.
- [K_VENC_2D_MAX_CHN_NUM](#315-k_venc_2d_max_chn_num): Defines the number of 2D channels.
- [k_venc_rc_mode](#316-k_venc_rc_mode): Defines the rate control mode for the encoding channel.
- [k_venc_pack_type](#317-k_venc_pack_type): Defines the JPEG stream pack type enumeration.
- [k_venc_2d_calc_mode](#318-k_venc_2d_calc_mode): Defines the calculation mode enumeration for 2D operations.
- [k_venc_2d_src_dst_fmt](#319-k_venc_2d_src_dst_fmt): Defines the input/output data format enumeration for 2D operations.
- [k_venc_2d_osd_fmt](#3110-k_venc_2d_osd_fmt): Defines the OSD layer data format enumeration for 2D operations.
- [k_venc_2d_add_order](#3111-k_venc_2d_add_order): Defines the OSD overlay enumeration for 2D operations.
- [k_rotation](#3112-k_rotation): Defines the rotation angle enumeration.
- [k_venc_mirror](#3113-k_venc_mirror): Defines the mirror mode enumeration.
- [k_venc_2d_color_gamut](#3114-k_venc_2d_color_gamut): Defines the color gamut enumeration for 2D operations.
- [k_venc_chn_attr](#3115-k_venc_chn_attr): Defines the attributes structure for the encoding channel.
- [k_venc_attr](#3116-k_venc_attr): Defines the encoder attributes structure.
- [k_venc_rc_attr](#3117-k_venc_rc_attr): Defines the rate controller attributes structure for the encoding channel.
- [k_venc_cbr](#3118-k_venc_cbr): Defines the CBR attributes structure for H.264/H.265 encoding channels.
- [k_venc_vbr](#3119-k_venc_vbr): Defines the VBR attributes structure for H.264/H.265 encoding channels.
- [k_venc_fixqp](#3120-k_venc_fixqp): Defines the Fixqp attributes structure for H.264/H.265 encoding channels.
- [k_venc_mjpeg_fixqp](#3121-k_venc_mjpeg_fixqp): Defines the Fixqp attributes structure for MJPEG encoding channels.
- [k_venc_chn_status](#3122-k_venc_chn_status): Defines the status structure for the encoding channel.
- [k_venc_stream](#3123-k_venc_stream): Defines the frame stream type structure.
- [k_venc_pack](#3124-k_venc_pack): Defines the frame stream pack structure.
- [k_venc_2d_osd_attr](#3125-k_venc_2d_osd_attr): Defines the 2D overlay attributes structure.
- [k_venc_2d_border_attr](#3126-k_venc_2d_border_attr): Defines the 2D border attributes structure.
- [k_venc_h265_sao](#3127-k_venc_h265_sao): Defines the SAO structure for H.265 protocol encoding channels.
- [k_venc_rect](#3128-k_venc_rect): Defines the rectangle region information structure.
- [k_venc_roi_attr](#3129-k_venc_roi_attr): Defines the ROI information for encoding.
- [k_venc_h264_entropy](#3130-k_venc_h264_entropy): Defines the entropy encoding structure for H.264 protocol encoding channels.
- [k_venc_h265_entropy](#3131-k_venc_h265_entropy): Defines the entropy encoding structure for H.265 protocol encoding channels.

#### 3.1.1 VENC_MAX_CHN_NUM

**Description**:

Defines the maximum number of channels.

**Definition**:

```c
#define VENC_MAX_CHN_NUM 4
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.2 K_VENC_MAX_2D_OSD_REGION_NUM

**Description**:

Defines the maximum number of 2D OSD regions.

**Definition**:

```c
#define K_VENC_MAX_2D_OSD_REGION_NUM 8
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.3 K_VENC_MAX_2D_BORDER_NUM

**Description**:

Defines the maximum number of 2D borders.

**Definition**:

```c
#define K_VENC_MAX_2D_BORDER_NUM 32
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.4 K_VENC_2D_COFF_NUM

**Description**:

Defines the number of 2D CSC conversion coefficients.

**Definition**:

```c
#define K_VENC_2D_COFF_NUM 12
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.5 K_VENC_2D_MAX_CHN_NUM

**Description**:

Defines the number of 2D channels.

**Definition**:

```c
#define K_VENC_2D_MAX_CHN_NUM 3
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.6 k_venc_rc_mode

**Description**:

Defines the rate control mode for the encoding channel.

**Definition**:

```c
typedef enum {
    K_VENC_RC_MODE_CBR = 1,
    K_VENC_RC_MODE_VBR,
    K_VENC_RC_MODE_FIXQP,
    K_VENC_RC_MODE_MJPEG_FIXQP,
    K_VENC_RC_MODE_BUTT,
} k_venc_rc_mode;
```

**Members**:

| Member Name | Description |
|---|---|
| K_VENC_RC_MODE_CBR | H.264/H.265 CBR mode. |
| K_VENC_RC_MODE_VBR | H.264/H.265 VBR mode. |
| K_VENC_RC_MODE_FIXQP | H.264/H.265 Fixqp mode. |
| K_VENC_RC_MODE_MJPEG_FIXQP | MJPEG Fixqp mode. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.7 k_venc_pack_type

**Description**:

Defines the JPEG stream pack type enumeration.

**Definition**:

```c
typedef enum {
    K_VENC_P_FRAME = 1,
    K_VENC_I_FRAME = 2,
    K_VENC_HEADER = 3,
    K_VENC_BUTT
} k_venc_pack_type;
```

**Members**:

| Member Name       | Description     |
|----------------|----------|
| K_VENC_P_FRAME | I frame.     |
| K_VENC_I_FRAME | P frame.     |
| K_VENC_HEADER  | Header.  |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.8 k_venc_2d_calc_mode

**Description**:

Defines the calculation mode enumeration for 2D operations.

**Definition**:

```c
typedef enum {
    K_VENC_2D_CALC_MODE_CSC = 0,
    K_VENC_2D_CALC_MODE_OSD,
    K_VENC_2D_CALC_MODE_BORDER,
    K_VENC_2D_CALC_MODE_OSD_BORDER,
    K_VENC_2D_CALC_MODE_BUTT
} k_venc_2d_calc_mode;
```

**Members**:

| Member Name                       | Description                     |
|--------------------------------|--------------------------|
| K_VENC_2D_CALC_MODE_CSC        | Image format conversion.            |
| K_VENC_2D_CALC_MODE_OSD        | Image overlay.                |
| K_VENC_2D_CALC_MODE_BORDER     | Border drawing.                    |
| K_VENC_2D_CALC_MODE_OSD_BORDER | Image overlay followed by border drawing.  |

**Notes**:

- Currently, K_VENC_2D_CALC_MODE_CSC mode is not supported.

**Related Data Types and Interfaces**:

None.

#### 3.1.9 k_venc_2d_src_dst_fmt

**Description**:

Defines the input/output data format enumeration for 2D operations.

**Definition**:

```c
typedef enum {
    K_VENC_2D_SRC_DST_FMT_YUV420_NV12 = 0,
    K_VENC_2D_SRC_DST_FMT_YUV420_NV21,
    K_VENC_2D_SRC_DST_FMT_YUV420_I420,
    K_VENC_2D_SRC_DST_FMT_ARGB8888 = 4,
    K_VENC_2D_SRC_DST_FMT_ARGB4444,
    K_VENC_2D_SRC_DST_FMT_ARGB1555,
    K_VENC_2D_SRC_DST_FMT_XRGB8888,
    K_VENC_2D_SRC_DST_FMT_XRGB4444,
    K_VENC_2D_SRC_DST_FMT_XRGB1555,
    K_VENC_2D_SRC_DST_FMT_BGRA8888,
    K_VENC_2D_SRC_DST_FMT_BGRA4444,
    K_VENC_2D_SRC_DST_FMT_BGRA5551,
    K_VENC_2D_SRC_DST_FMT_BGRX8888,
    K_VENC_2D_SRC_DST_FMT_BGRX4444,
    K_VENC_2D_SRC_DST_FMT_BGRX5551,
    K_VENC_2D_SRC_DST_FMT_RGB888,
    K_VENC_2D_SRC_DST_FMT_BGR888,
    K_VENC_2D_SRC_DST_FMT_RGB565,
    K_VENC_2D_SRC_DST_FMT_BGR565,
    K_VENC_2D_SRC_DST_FMT_SEPARATE_RGB,
    K_VENC_2D_SRC_DST_FMT_BUTT
} k_venc_2d_src_dst_fmt;
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.10 k_venc_2d_osd_fmt

**Description**:

Defines the enumeration of OSD layer data formats for 2D operations.

**Definition**:

```c
typedef enum {
    K_VENC_2D_OSD_FMT_ARGB8888 = 0,
    K_VENC_2D_OSD_FMT_ARGB4444,
    K_VENC_2D_OSD_FMT_ARGB1555,
    K_VENC_2D_OSD_FMT_XRGB8888,
    K_VENC_2D_OSD_FMT_XRGB4444,
    K_VENC_2D_OSD_FMT_XRGB1555,
    K_VENC_2D_OSD_FMT_BGRA8888,
    K_VENC_2D_OSD_FMT_BGRA4444,
    K_VENC_2D_OSD_FMT_BGRA5551,
    K_VENC_2D_OSD_FMT_BGRX8888,
    K_VENC_2D_OSD_FMT_BGRX4444,
    K_VENC_2D_OSD_FMT_BGRX5551,
    K_VENC_2D_OSD_FMT_RGB888,
    K_VENC_2D_OSD_FMT_BGR888,
    K_VENC_2D_OSD_FMT_RGB565,
    K_VENC_2D_OSD_FMT_BGR565,
    K_VENC_2D_OSD_FMT_SEPARATE_RGB,
    K_VENC_2D_OSD_FMT_BUTT
} k_venc_2d_osd_fmt;
```

**Notes**:

- Currently, only ARGB8888, ARGB4444, and ARGB1555 formats are supported for image overlay.

**Related Data Types and Interfaces**:

None.

#### 3.1.11 k_venc_2d_add_order

**Description**:

Defines the enumeration of OSD overlay order (video, OSD, and background layers) for 2D operations.

**Definition**:

```c
typedef enum {
    /* bottom ------> top */
    K_VENC_2D_ADD_ORDER_VIDEO_OSD = 0,
    K_VENC_2D_ADD_ORDER_OSD_VIDEO,
    K_VENC_2D_ADD_ORDER_VIDEO_BG,
    K_VENC_2D_ADD_ORDER_BG_VIDEO,
    K_VENC_2D_ADD_ORDER_VIDEO_BG_OSD,
    K_VENC_2D_ADD_ORDER_VIDEO_OSD_BG,
    K_VENC_2D_ADD_ORDER_BG_VIDEO_OSD,
    K_VENC_2D_ADD_ORDER_BG_OSD_VIDEO,
    K_VENC_2D_ADD_ORDER_OSD_VIDEO_BG,
    K_VENC_2D_ADD_ORDER_OSD_BG_VIDEO,
    K_VENC_2D_ADD_ORDER_BUTT
} k_venc_2d_add_order;
```

**Members**:

| Member Name                    | Description                                 |
|--------------------------------|---------------------------------------------|
| K_VENC_2D_ADD_ORDER_VIDEO_OSD  | Video at the bottom, OSD at the top.        |
| K_VENC_2D_ADD_ORDER_OSD_VIDEO  | OSD at the bottom, video at the top.        |
| K_VENC_2D_ADD_ORDER_VIDEO_BG   | Video at the bottom, background color on top.|
| K_VENC_2D_ADD_ORDER_BG_VIDEO   | Background color at the bottom, video on top.|
| K_VENC_2D_ADD_ORDER_VIDEO_BG_OSD | Video at the bottom, background color in the middle, OSD at the top. |
| K_VENC_2D_ADD_ORDER_VIDEO_OSD_BG | Video at the bottom, OSD in the middle, background color at the top. |
| K_VENC_2D_ADD_ORDER_BG_VIDEO_OSD | Background color at the bottom, video in the middle, OSD at the top. |
| K_VENC_2D_ADD_ORDER_BG_OSD_VIDEO | Background color at the bottom, OSD in the middle, video at the top. |
| K_VENC_2D_ADD_ORDER_OSD_VIDEO_BG | OSD at the bottom, video in the middle, background color at the top. |
| K_VENC_2D_ADD_ORDER_OSD_BG_VIDEO | OSD at the bottom, background color in the middle, video at the top. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.12 k_rotation

**Description**:

Defines the enumeration of rotation angles for encoding.

**Definition**:

```c
typedef enum {
    K_VPU_ROTATION_0 = 0,
    K_VPU_ROTATION_90 = 1,
    K_VPU_ROTATION_180 = 2,
    K_VPU_ROTATION_270 = 3,
    K_VPU_ROTATION_BUTT
} k_rotation;
```

**Members**:

| Member Name         | Description       |
|---------------------|-------------------|
| K_VPU_ROTATION_0    | No rotation, 0 degrees. |
| K_VPU_ROTATION_90   | Rotate 90 degrees.     |
| K_VPU_ROTATION_180  | Rotate 180 degrees.    |
| K_VPU_ROTATION_270  | Rotate 270 degrees.    |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.13 k_venc_mirror

**Description**:

Defines the enumeration of mirroring methods for encoding.

**Definition**:

```c
typedef enum {
    K_VENC_MIRROR_HORI = 0,
    K_VENC_MIRROR_VERT = 1,
    K_VENC_MIRROR_BUTT
} k_venc_mirror;
```

**Members**:

| Member Name         | Description       |
|---------------------|-------------------|
| K_VENC_MIRROR_HORI  | Horizontal flip.  |
| K_VENC_MIRROR_VERT  | Vertical flip.    |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.14 k_venc_2d_color_gamut

**Description**:

Defines the enumeration of color gamuts for 2D operations.

**Definition**:

```c
typedef enum {
    VENC_2D_COLOR_GAMUT_BT601 = 0,
    VENC_2D_COLOR_GAMUT_BT709,
    VENC_2D_COLOR_GAMUT_BT2020,
    VENC_2D_COLOR_GAMUT_BUTT
} k_venc_2d_color_gamut;
```

**Members**:

| Member Name                   | Description       |
|-------------------------------|-------------------|
| VENC_2D_COLOR_GAMUT_BT601     | BT.601 color gamut. |
| VENC_2D_COLOR_GAMUT_BT709     | BT.709 color gamut. |
| VENC_2D_COLOR_GAMUT_BT2020    | BT.2020 color gamut. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.15 k_venc_chn_attr

**Description**:

Defines the structure of encoding channel attributes.

**Definition**:

```c
typedef struct {
    k_venc_attr venc_attr;
    k_venc_rc_attr rc_attr;
} k_venc_chn_attr;
```

**Members**:

| Member Name  | Description       |
|--------------|-------------------|
| venc_attr    | Encoder attributes. |
| rc_attr      | Rate controller attributes. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.16 k_venc_attr

**Description**:

Defines the structure of encoder attributes.

**Definition**:

```c
typedef struct {
    k_payload_type type;
    k_u32 stream_buf_size;
    k_u32 stream_buf_cnt;
    k_u32 pic_width;
    k_u32 pic_height;
    k_venc_profile profile;
} k_venc_attr;
```

**Members**:

| Member Name       | Description       |
|-------------------|-------------------|
| type              | Encoding protocol type.  |
| stream_buf_size   | Stream buffer size.      |
| stream_buf_cnt    | Number of stream buffers.|
| pic_width         | Encoding image width. Range: `[MIN_WIDTH, MAX_WIDTH]`, in pixels. Must be a multiple of MIN_ALIGN. |
| pic_height        | Encoding image height. Range: `[MIN_HEIGHT, MAX_HEIGHT]`, in pixels. Must be a multiple of MIN_ALIGN. |
| profile           | Encoding profile enumeration. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.17 k_venc_rc_attr

**Description**:

Defines the structure of rate controller attributes for encoding channels.

**Definition**:

```c
typedef struct {
    k_venc_rc_mode rc_mode;
    union {
        k_venc_cbr cbr;
        k_venc_vbr vbr;
        k_venc_fixqp fixqp;
        k_venc_mjpeg_fixqp mjpeg_fixqp;
    };
} k_venc_rc_attr;
```

**Members**:

| Member Name     | Description                                        |
|-----------------|----------------------------------------------------|
| rc_mode         | RC mode.                                           |
| cbr             | CBR attributes for H.264/H.265 encoding channels.  |
| vbr             | VBR attributes for H.264/H.265 encoding channels.  |
| fixqp           | Fixqp attributes for H.264/H.265 encoding channels.|
| mjpeg_fixqp     | Fixqp attributes for MJPEG encoding channels.      |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.1.18 k_venc_cbr

**Description**:

Defines the structure of CBR attributes for H.264/H.265 encoding channels.

**Definition**:

```c
typedef struct {
    k_u32 gop;
    k_u32 stats_time;
    k_u32 src_frame_rate;
    k_u32 dst_frame_rate;
    k_u32 bit_rate;
} k_venc_cbr;
```

**Members**:

| Member Name       | Description                                               |
|-------------------|-----------------------------------------------------------|
| gop               | GOP value.                                                |
| stats_time        | CBR rate statistics time in seconds. Range: `[1, 60]`.    |
| src_frame_rate    | Input frame rate in fps.                                  |
| dst_frame_rate    | Encoder output frame rate in fps.                         |
| bit_rate          | Average bitrate in kbps.                                  |

**Notes**:

- If the set bitrate exceeds the maximum real-time bitrate specified in the chip manual, real-time encoding cannot be guaranteed.

**Related Data Types and Interfaces**:

None.

#### 3.1.19 k_venc_vbr

**Description**:

Defines the structure of VBR attributes for H.264/H.265 encoding channels.

**Definition**:

```c
typedef struct {
    k_u32 gop;
    k_u32 stats_time;
    k_u32 src_frame_rate;
    k_u32 dst_frame_rate;
    k_u32 max_bit_rate;
    k_u32 bit_rate;
} k_venc_vbr;
```

**Members**:

| Member Name       | Description                                               |
|-------------------|-----------------------------------------------------------|
| gop               | GOP value.                                                |
| stats_time        | VBR rate statistics time in seconds. Range: `[1, 60]`.    |
| src_frame_rate    | Input frame rate in fps.                                  |
| dst_frame_rate    | Encoder output frame rate in fps.                         |
| max_bit_rate      | Maximum bitrate in kbps.                                  |
| bit_rate          | Average bitrate in kbps.                                  |

**Notes**:

Refer to [k_venc_cbr](#3118-k_venc_cbr) for details on src_frame_rate and dst_frame_rate.

**Related Data Types and Interfaces**:

None.

### 3.1.20 k_venc_fixqp

**Description**:

Defines the structure for H.264/H.265 encoding channel Fixqp attributes.

**Definition**:

```c
typedef struct {
    k_u32 gop;
    k_u32 src_frame_rate;
    k_u32 dst_frame_rate;
    k_u32 i_qp;
    k_u32 p_qp;
} k_venc_fixqp;
```

**Members**:

| Member Name     | Description                                 |
|-----------------|---------------------------------------------|
| gop             | GOP value.                                  |
| src_frame_rate  | Input frame rate, in fps.                   |
| dst_frame_rate  | Encoder output frame rate, in fps.          |
| i_qp            | QP value for all macroblocks in I-frames. Range: `[0, 51]`.  |
| p_qp            | QP value for all macroblocks in P-frames. Range: `[0, 51]`.  |

**Notes**:

Refer to [k_venc_cbr](#3118-k_venc_cbr) for details on `src_frame_rate` and `dst_frame_rate`.

**Related Data Types and Interfaces**:

None.

### 3.1.21 k_venc_mjpeg_fixqp

**Description**:

Defines the structure for MJPEG encoding channel Fixqp attributes.

**Definition**:

```c
typedef struct {
    k_u32 src_frame_rate;
    k_u32 dst_frame_rate;
    k_u32 q_factor;
} k_venc_mjpeg_fixqp;
```

**Members**:

| Member Name     | Description                                  |
|-----------------|----------------------------------------------|
| src_frame_rate  | Input frame rate, in fps.                    |
| dst_frame_rate  | Encoder output frame rate, in fps.           |
| q_factor        | Q factor for MJPEG encoding. Range: `[1, 99]`. |

**Notes**:

Refer to [k_venc_cbr](#3118-k_venc_cbr) for details on `src_frame_rate` and `dst_frame_rate`.

**Related Data Types and Interfaces**:

None.

### 3.1.22 k_venc_chn_status

**Description**:

Defines the structure for the status of encoding channels.

**Definition**:

```c
typedef struct {
    k_u32 cur_packs;
    k_u64 release_pic_pts;
    k_bool end_of_stream;
} k_venc_chn_status;
```

**Members**:

| Member Name      | Description                        |
|------------------|------------------------------------|
| cur_packs        | Number of stream packets in the current frame. |
| release_pic_pts  | PTS of the released stream's corresponding image. |
| end_of_stream    | End of stream flag.                |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.23 k_venc_stream

**Description**:

Defines the structure for frame stream type.

**Definition**:

```c
typedef struct {
    [k_venc_pack](#3124-k_venc_pack) *pack;
    k_u32 pack_cnt;
} k_venc_stream;
```

**Members**:

| Member Name | Description                     |
|-------------|---------------------------------|
| pack        | Frame stream packet structure.  |
| pack_cnt    | Number of packets in one frame stream. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.24 k_venc_pack

**Description**:

Defines the structure for frame stream packets.

**Definition**:

```c
typedef struct {
    k_u64 phys_addr;
    k_u32 len;
    k_u64 pts;
    [k_venc_pack_type](#317-k_venc_pack_type) type;
} k_venc_pack;
```

**Members**:

| Member Name  | Description                |
|--------------|----------------------------|
| phys_addr    | Physical address of the stream packet. |
| len          | Length of the stream packet. |
| pts          | Timestamp, in microseconds. |
| type         | Data type of the packet.    |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.25 k_venc_2d_osd_attr

**Description**:

Defines the structure for 2D overlay attributes.

**Definition**:

```c
typedef struct {
    k_u16 width;
    k_u16 height;
    k_u16 startx;
    k_u16 starty;
    k_u32 phys_addr[3];
    k_u8 bg_alpha;
    k_u8 osd_alpha;
    k_u8 video_alpha;
    [k_venc_2d_add_order](#3111-k_venc_2d_add_order) add_order;
    k_u32 bg_color;
    [k_venc_2d_osd_fmt](#3110-k_venc_2d_osd_fmt) fmt;
} k_venc_2d_osd_attr;
```

**Members**:

| Member Name    | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| width          | Width of the OSD overlay area.                                              |
| height         | Height of the OSD overlay area.                                             |
| startx         | X offset of the top-left point of the OSD overlay area in the original image.|
| starty         | Y offset of the top-left point of the OSD overlay area in the original image.|
| phys_addr      | Physical address of the OSD image.                                          |
| bg_alpha       | Transparency of the background layer.                                       |
| osd_alpha      | Transparency of the OSD image.                                              |
| video_alpha    | Transparency of the video input image.                                      |
| add_order      | Enumeration of OSD overlay order.                                           |
| bg_color       | Background color of the OSD in YUV444 format. Y: bit0~bit7, U: bit8~bit15, V: bit16~bit23 |
| fmt            | Enumeration of the OSD image format.                                        |

**Notes**:

- The starting address of the source image and the destination image in DDR must be 8-byte aligned.
- Only even dimensions are supported for images and OSD.
- The source and destination addresses for OSD must be the same.

**Related Data Types and Interfaces**:

None.

### 3.1.26 k_venc_2d_border_attr

**Description**:

Defines the structure for 2D border drawing.

**Definition**:

```c
typedef struct {
    k_u16 width;
    k_u16 height;
    k_u16 line_width;
    k_u32 color;
    k_u16 startx;
    k_u16 starty;
} k_venc_2d_border_attr;
```

**Members**:

| Member Name   | Description                                                             |
|---------------|-------------------------------------------------------------------------|
| width         | Width of the border area, including the line width.                     |
| height        | Height of the border area, including the line width.                    |
| line_width    | Line width of the border.                                               |
| color         | Color of the border in YUV444 format. Y: bit0~bit7, U: bit8~bit15, V: bit16~bit23 |
| startx        | X offset of the top-left point of the border area in the original image. |
| starty        | Y offset of the top-left point of the border area in the original image. |

**Notes**:

- The starting address of the source image and the destination image in DDR must be 8-byte aligned.
- Only even dimensions are supported for images and borders.
- The source and destination addresses must be the same.

**Related Data Types and Interfaces**:

None.

### 3.1.27 k_venc_h265_sao

**Description**:

Defines the structure for H.265 protocol encoding channel SAO.

**Definition**:

```c
typedef struct {
    k_u32 slice_sao_luma_flag;
    k_u32 slice_sao_chroma_flag;
} k_venc_h265_sao;
```

**Members**:

| Member Name           | Description                     |
|-----------------------|---------------------------------|
| slice_sao_luma_flag   | Default is 1. Range: 0 or 1.    |
| slice_sao_chroma_flag | Default is 1. Range: 0 or 1.    |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.28 k_venc_rect

**Description**:

Defines the structure for rectangular area information.

**Definition**:

```c
typedef struct {
    k_s32 left;
    k_s32 right;
    k_u32 top;
    k_u32 bottom;
} k_venc_rect;
```

**Members**:

| Member Name | Description     |
|-------------|-----------------|
| left        | Left offset.    |
| right       | Right offset.   |
| top         | Top offset.     |
| bottom      | Bottom offset.  |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.29 k_venc_roi_attr

**Description**:

Defines the structure for encoding region of interest (ROI) information.

**Definition**:

```c
typedef struct {
    k_u32 idx;
    k_bool enable;
    k_bool is_abs_qp;
    k_s32 qp;
    [k_venc_rect](#3128-k_venc_rect) rect;
} k_venc_roi_attr;
```

**Members**:

| Member Name | Description                                                   |
|-------------|---------------------------------------------------------------|
| idx         | Index of the ROI region. Supported index range: `[0, 15]`. Out of range indices are not supported. |
| enable      | Whether to enable this ROI region.                            |
| is_abs_qp   | QP mode of the ROI region. `K_FALSE`: relative QP. `K_TRUE`: absolute QP. |
| qp          | QP value. Range: `[0, 51]`.                                   |
| rect        | ROI region. `left`, `right`, `top`, and `bottom` must be 16-aligned. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.30 k_venc_h264_entropy

**Description**:

Defines the structure for H.264 protocol encoding channel entropy coding.

**Definition**:

```c
typedef struct {
    k_u32 entropy_coding_mode;
    k_u32 cabac_init_idc;
} k_venc_h264_entropy;
```

**Members**:

| Member Name          | Description                                                                                       |
|----------------------|---------------------------------------------------------------------------------------------------|
| entropy_coding_mode  | Entropy coding mode. `0`: CAVLC. `1`: CABAC. Values >= `2` are not meaningful. Baseline does not support CABAC. Default value is `1`. |
| cabac_init_idc       | Range: `[0, 2]`, default value `0`. For specific meanings, refer to the H.264 protocol.           |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.1.31 k_venc_h265_entropy

**Description**:

Defines the structure for H.265 protocol encoding channel entropy coding.

**Definition**:

```c
typedef struct {
    k_u32 cabac_init_flag;
} k_venc_h265_entropy;
```

**Members**:

| Member Name       | Description                                               |
|-------------------|-----------------------------------------------------------|
| cabac_init_flag   | Range: `[0, 1]`, default value `1`. For specific meanings, refer to the H.265 protocol. |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

### 3.2 Video Decoding

The relevant data type definitions for this functional module are as follows:

- [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num): Defines the maximum number of channels.
- [k_vdec_send_mode](#322-k_vdec_send_mode): Defines the structure for decoding channel attributes.
- [k_vdec_chn_attr](#323-k_vdec_chn_attr): Defines the structure for decoding channel attributes.
- [k_vdec_chn_status](#324-k_vdec_chn_status): Defines the structure for channel status.
- [k_vdec_dec_err](#325-k_vdec_dec_err): Defines the structure for decoding error information.
- [k_vdec_stream](#326-k_vdec_stream): Defines the structure for video decoding stream.
- [k_vdec_supplement_info](#327-k_vdec_supplement_info): Defines the structure for output frame supplementary information.

#### 3.2.1 K_VDEC_MAX_CHN_NUM

**Description**:

Defines the maximum number of channels.

**Definition**:

```c
#define K_VDEC_MAX_CHN_NUM 4
```

**Notes**:

None.

**Related Data Types and Interfaces**:

None.

#### 3.2.2 k_vdec_send_mode

**Description**:

Defines the structure for decoding channel attributes.

**Definition**:

```c
typedef enum {
    K_VDEC_SEND_MODE_STREAM = 0,
    K_VDEC_SEND_MODE_FRAME,
    K_VDEC_SEND_MODE_BUTT
} k_vdec_send_mode;
```

**Members**:

| Member Name           | Description                        |
|-----------------------|------------------------------------|
| K_VDEC_SEND_MODE_STREAM | Send stream by stream mode.        |
| K_VDEC_SEND_MODE_FRAME  | Send stream by frame mode, in units of frames. |

**Notes**:

Currently, only stream mode is supported.

**Related Data Types and Interfaces**:

None.

#### 3.2.3 k_vdec_chn_attr

**Description**:

Defines the structure for decoding channel attributes.

**Definition**:

```c
typedef struct {
    k_payload_type type;
    [k_vdec_send_mode](#322-k_vdec_send_mode) mode;
    k_u32 pic_width;
    k_u32 pic_height;
    k_u32 stream_buf_size;
    k_u32 frame_buf_size;
    k_u32 frame_buf_cnt;
    k_pixel_format pic_format;
} k_vdec_chn_attr;
```

**Members**:

| Member Name       | Description                                       |
|-------------------|---------------------------------------------------|
| type              | Enumeration value for decoding protocol type.     |
| mode              | Stream sending mode.                              |
| pic_width         | Maximum width of the decoded image supported by the channel (in pixels). |
| pic_height        | Maximum height of the decoded image supported by the channel (in pixels). |
| stream_buf_size   | Size of the stream buffer.                        |
| frame_buf_size    | Size of the buffer for decoded image frames.      |
| frame_buf_cnt     | Number of frame buffers.                          |
| pic_format        | Enumeration of input data format. Refer to "K230 System Control API Reference". |

**Notes**:

None.

**Related Data Types and Interfaces**:

None.
|

【Notes】

- Currently supported `pic_format` values are: `PIXEL_FORMAT_YUV_SEMIPLANAR_420` and `PIXEL_FORMAT_YVU_PLANAR_420`.

【Related Data Types and Interfaces】

None.

#### 3.2.4 k_vdec_chn_status

【Description】

Defines the structure for channel status.

【Definition】

```c
typedef struct {
    k_payload_type type;
    k_bool is_started;
    k_u32 recv_stream_frames;
    k_u32 dec_stream_frames;
    [k_vdec_dec_err](#325-k_vdec_dec_err) dec_err;
    k_u32 width;
    k_u32 height;
    k_u64 latest_frame_pts;
    k_bool end_of_stream;
} k_vdec_chn_status;
```

【Members】

| Member Name         | Description                                                      |
|---------------------|------------------------------------------------------------------|
| type                | Decoding protocol.                                               |
| is_started          | Whether the decoder has started receiving streams.               |
| recv_stream_frames  | Number of stream frames received in the stream buffer. `-1` indicates invalid. Not applicable in stream mode. |
| dec_stream_frames   | Number of decoded frames in the stream buffer.                   |
| dec_err             | Decoding error information.                                      |
| width               | Image width.                                                     |
| height              | Image height.                                                    |
| latest_frame_pts    | Timestamp of the latest decoded image.                           |
| end_of_stream       | End of stream flag.                                              |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.5 k_vdec_dec_err

【Description】

Defines the structure for decoding error information.

【Definition】

```c
typedef struct {
    k_s32 set_pic_size_err;
    k_s32 format_err;
    k_s32 stream_unsupport;
} k_vdec_dec_err;
```

【Members】

| Member Name          | Description                                                      |
|----------------------|------------------------------------------------------------------|
| set_pic_size_err     | Image width (or height) exceeds the channel's width (or height). |
| format_err           | Unsupported format.                                              |
| stream_unsupport     | Unsupported specification (stream specification does not match the claimed supported specification). |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.6 k_vdec_stream

【Description】

Defines the structure for video decoding stream.

【Definition】

```c
typedef struct {
    k_bool end_of_stream;
    k_u64 pts;
    k_u32 len;
    k_u8 *addr;
} k_vdec_stream;
```

【Members】

| Member Name    | Description                        |
|----------------|------------------------------------|
| end_of_stream  | Whether all streams have been sent. |
| pts            | Timestamp of the stream packet, in microseconds. |
| len            | Length of the stream packet, in bytes. |
| addr           | Address of the stream packet.      |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.7 k_vdec_supplement_info

【Description】

Defines the structure for output frame supplementary information.

【Definition】

```c
typedef struct {
    k_payload_type type;
    k_bool is_valid_frame;
    k_bool end_of_stream;
} k_vdec_supplement_info;
```

【Members】

| Member Name     | Description                        |
|-----------------|------------------------------------|
| type            | Decoding protocol type enumeration. |
| is_valid_frame  | Whether it is a valid frame.       |
| end_of_stream   | End of stream flag.                |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.8 k_vdec_dsl_mode

【Description】

Defines the enumeration for decoding downscale mode.

【Definition】

```c
typedef enum {
    K_VDEC_DSL_MODE_BY_SIZE,
    K_VDEC_DSL_MODE_BY_RATIO,
    K_VDEC_DSL_MODE_BUTT
} k_vdec_dsl_mode;
```

【Members】

| Member Name                | Description              |
|----------------------------|--------------------------|
| K_VDEC_DSL_MODE_BY_SIZE    | Downscale by size.       |
| K_VDEC_DSL_MODE_BY_RATIO   | Downscale by ratio.      |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.9 k_vdec_dsl_size

【Description】

Defines the structure for downscaling size parameters.

【Definition】

```c
typedef struct {
    k_u32 dsl_frame_width;
    k_u32 dsl_frame_height;
} k_vdec_dsl_size;
```

【Members】

| Member Name         | Description              |
|---------------------|--------------------------|
| dsl_frame_width     | Width after downscaling. |
| dsl_frame_height    | Height after downscaling.|

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.10 k_vdec_dsl_ratio

【Description】

Defines the structure for downscaling ratio parameters.

【Definition】

```c
typedef struct {
    k_u8 dsl_ratio_hor;
    k_u8 dsl_ratio_ver;
} k_vdec_dsl_ratio;
```

【Members】

| Member Name       | Description                  |
|-------------------|------------------------------|
| dsl_ratio_hor     | Horizontal downscale ratio.  |
| dsl_ratio_ver     | Vertical downscale ratio.    |

【Notes】

None.

【Related Data Types and Interfaces】

None.

#### 3.2.11 k_vdec_downscale

【Description】

Defines the structure for downscaling.

【Definition】

```c
typedef struct {
    [k_vdec_dsl_mode](#328-k_vdec_dsl_mode) dsl_mode;
    union
    {
        [k_vdec_dsl_size](#329-k_vdec_dsl_size) dsl_size;
        [k_vdec_dsl_ratio](#3210-k_vdec_dsl_ratio) dsl_ratio;
    };
} k_vdec_downscale;
```

【Members】

| Member Name       | Description                        |
|-------------------|------------------------------------|
| dsl_mode          | Downscale mode enumeration.        |
| dsl_size          | Structure for downscale by size.   |
| dsl_ratio         | Structure for downscale by ratio.  |

【Notes】

None.

【Related Data Types and Interfaces】

None.

## 4. MAPI

### 4.1 Video Encoding

#### 4.1.1 Overview

MAPI is called on the small core to obtain VENC stream data.

#### 4.1.2 Encoding Data Flow Diagram

Figure 4-1

![mapi encode channel](../../../../zh/01_software/board/mpp/images/d71726ec1aa4be0868689b0b36beaa4f.png)

A typical encoding process includes receiving input images, encoding the images, cross-core data stream transmission, and stream output.

The encoding module (VENC) in the above figure consists of the VENC receiving channel, encoding channel, 2D receiving channel, and 2D operation module. For details, see [1.2.1 Video Encoding](#121-Video Encoding).

#### 4.1.3 API

The video encoding module mainly provides functions for creating and destroying video encoding channels, starting and stopping the reception of images on encoding channels, setting and getting encoding channel attributes, registering and deregistering callback functions for stream acquisition, etc.

This functional module provides the following MAPI:

[kd_mapi_venc_init](#4131-kd_mapi_venc_init)

[kd_mapi_venc_deinit](#4132-kd_mapi_venc_deinit)

[kd_mapi_venc_registercallback](#4133-kd_mapi_venc_registercallback)

[kd_mapi_venc_unregistercallback](#4134-kd_mapi_venc_unregistercallback)

[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

[kd_mapi_venc_stop](#4136-kd_mapi_venc_stop)

[kd_mapi_venc_bind_vi](#4137-kd_mapi_venc_bind_vi)

[kd_mapi_venc_unbind_vi](#4138-kd_mapi_venc_unbind_vi)

[kd_mapi_venc_request_idr](#4139-kd_mapi_venc_request_idr)

[kd_mapi_venc_enable_idr](#41310-kd_mapi_venc_enable_idr)

##### 4.1.3.1 kd_mapi_venc_init

【Description】

Initializes the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_init(k_u32 chn_num, [k_venc_chn_attr](#3115-k_venc_chn_attr) *pst_venc_attr)
```

【Parameters】

| Parameter Name  | Description                                | Input/Output |
|-----------------|--------------------------------------------|--------------|
| chn_num         | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |
| pst_venc_attr   | Pointer to VENC channel attributes. Static attributes. | Input      |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the error code |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

- Before calling this interface, `kd_mapi_sys_init()` and `kd_mapi_media_init()` need to be successfully initialized. See the "SYS MAPI" section for details.
- Reinitialization returns success.

【Example】

Please refer to the `sample_venc` code.

【Related Topics】

[kd_mapi_venc_deinit](#4132-kd_mapi_venc_deinit)
[k_venc_chn_attr](#3115-k_venc_chn_attr)

##### 4.1.3.2 kd_mapi_venc_deinit

【Description】

Deinitializes the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_deinit(k_u32 chn_num)
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

None.

【Example】

None.

【Related Topics】

[kd_mapi_venc_init](#4131-kd_mapi_venc_init)

##### 4.1.3.3 kd_mapi_venc_registercallback

【Description】

Registers a callback function for the encoding channel to acquire encoding data.

【Syntax】

```c
k_s32 kd_mapi_venc_registercallback(k_u32 chn_num, [kd_venc_callback_s](#4141-kd_venc_callback_s) *pst_venc_cb);
```

【Parameters】

| Parameter Name  | Description                                | Input/Output |
|-----------------|--------------------------------------------|--------------|
| chn_num         | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |
| pst_venc_cb     | Pointer to the encoder callback function structure. | Input      |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

- The callback function structure pointer cannot be null.
- The structure contents must be exactly the same to indicate that the callback function structures are equal.
- Each channel supports up to five callback functions.

【Example】

None.

【Related Topics】

kd_mapi_venc_unregistercallback
kd_venc_callback_s

##### 4.1.3.4 kd_mapi_venc_unregistercallback

【Description】

Unregisters a callback function for the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_unregistercallback(k_u32 chn_num, [kd_venc_callback_s](#4141-kd_venc_callback_s) *pst_venc_cb);
```

【Parameters】

| Parameter Name  | Description                                | Input/Output |
|-----------------|--------------------------------------------|--------------|
| chn_num         | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |
| pst_venc_cb     | Pointer to the encoder callback function structure. | Input      |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

The contents of the `pst_venc_cb` callback function structure must be exactly the same as when it was registered to unregister the callback function.

【Example】

None.

【Related Topics】

[kd_mapi_venc_registercallback](#4133-kd_mapi_venc_registercallback)

##### 4.1.3.5 kd_mapi_venc_start

【Description】

Starts the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_start(k_s32 chn_num ,k_s32 s32_frame_cnt);
```

【Parameters】

| Parameter Name  | Description                                | Input/Output |
|-----------------|--------------------------------------------|--------------|
| chn_num         | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |
| s32_frame_cnt   | Expected number of encoded frames.         | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.
【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

- Scenario 1: In the video stream encoding scenario, `s32_frame_cnt` should be set to `[KD_VENC_LIMITLESS_FRAME_COUNT](#4146-kd_venc_limitless_frame_count)`.
- Scenario 2: In the scenario of single or multiple data encoding, you can only restart after the previous encoding is finished.
- When switching from Scenario 1 to Scenario 2, you need to call the `kd_mapi_venc_stop` interface first.
- When switching from Scenario 2 to Scenario 1, you can call the `kd_mapi_venc_stop` interface first or restart encoding after the current encoding is finished.
- For the encoding completion flag, please refer to `end_of_stream` in [kd_venc_data_s](#4143-kd_venc_data_s).

【Example】

None.

【Related Topics】

[kd_mapi_venc_stop](#4136-kd_mapi_venc_stop)

##### 4.1.3.6 kd_mapi_venc_stop

【Description】

Stops the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_stop(k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

None.

【Example】

None.

【Related Topics】

[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

##### 4.1.3.7 kd_mapi_venc_bind_vi

【Description】

Binds the encoding channel to the input source VI.

【Syntax】

```c
k_s32 kd_mapi_venc_bind_vi(k_s32 src_dev, k_s32 src_chn, k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| src_dev        | Input source Device ID                     | Input        |
| src_chn        | Input source Channel ID                    | Input        |
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

None.

【Example】

None.

【Related Topics】

[kd_mapi_venc_unbind_vi](#4138-kd_mapi_venc_unbind_vi)

##### 4.1.3.8 kd_mapi_venc_unbind_vi

【Description】

Unbinds the input source VI from the encoding channel.

【Syntax】

```c
k_s32 kd_mapi_venc_unbind_vi(k_s32 src_dev, k_s32 src_chn, k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| src_dev        | Input source Device ID                     | Input        |
| src_chn        | Input source Channel ID                    | Input        |
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM)` | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

None.

【Example】

None.

【Related Topics】

[kd_mapi_venc_bind_vi](#4137-kd_mapi_venc_bind_vi)

##### 4.1.3.9 kd_mapi_venc_request_idr

【Description】

Requests an IDR frame, which is generated immediately after the call.

【Syntax】

```c
k_s32 kd_mapi_venc_request_idr(k_s32 chn_num);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM]` | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

None.

【Example】

None.

【Related Topics】

[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

##### 4.1.3.10 kd_mapi_venc_enable_idr

【Description】

Enables IDR frames, generating them according to the GOP interval.

【Syntax】

```c
k_s32 kd_mapi_venc_enable_idr(k_s32 chn_num, k_bool idr_enable);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VENC channel number. Range: `[0, VENC_MAX_CHN_NUM]` | Input       |
| idr_enable     | Whether to enable IDR frames, 0: disable, 1: enable | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_venc_api.h`, `k_venc_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

- This interface should be called after [kd_mpi_venc_create_chn](#211-kd_mpi_venc_create_chn) and before [kd_mpi_venc_start_chn](#213-kd_mpi_venc_start_chn).

【Example】

None.

【Related Topics】

[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

#### 4.1.4 Data Types

The data types related to video encoding are defined as follows:

- [kd_venc_callback_s](#4141-kd_venc_callback_s)
- [pfn_venc_dataproc](#4142-pfn_venc_dataproc)
- [kd_venc_data_s](#4143-kd_venc_data_s)
- [k_venc_data_pack_s](#4144-k_venc_data_pack_s)
- [KD_VENC_MAX_FRAME_PACKCOUNT](#4145-kd_venc_max_frame_packcount)
- [KD_VENC_LIMITLESS_FRAME_COUNT](#4146-kd_venc_limitless_frame_count)

##### 4.1.4.1 kd_venc_callback_s

【Description】

Encoding callback function structure.

【Definition】

```c
typedef struct
{
    [pfn_venc_dataproc](#4142-pfn_venc_dataproc);
    k_u8 *p_private_data;
} kd_venc_callback_s;
```

【Members】

| Member Name     | Description                                |
|-----------------|--------------------------------------------|
| pfn_data_cb     | Callback processing function for obtaining encoded data. |
| p_private_data  | Private data pointer, used as a parameter in `pfn_venc_dataproc`. |

【Notes】

- After this structure is registered and encoding starts, `pfn_data_cb` will be called when there is encoded data. Users obtain encoded data through this function.
- `p_private_data` is optional and can be used by the user.

【Related Data Types and Interfaces】

- [kd_mapi_venc_registercallback](#4133-kd_mapi_venc_registercallback)
- [kd_mapi_venc_unregistercallback](#4134-kd_mapi_venc_unregistercallback)
- [pfn_venc_dataproc](#4142-pfn_venc_dataproc)

##### 4.1.4.2 pfn_venc_dataproc

【Description】

Defines the encoding data callback function.

【Definition】

```c
typedef k_s32 (*pfn_venc_dataproc)(k_u32 chn_num, [kd_venc_data_s](#4144-k_venc_data_pack_s) *p_vstream_data, k_u8 *p_private_data);
```

【Members】

| Member Name     | Description             |
|-----------------|-------------------------|
| chn_num         | Encoding channel handle |
| kd_venc_data_s  | Data pointer            |
| p_private_data  | Private data pointer    |

【Notes】

None.

【Related Data Types and Interfaces】

- [kd_mapi_venc_registercallback](#4133-kd_mapi_venc_registercallback)
- [kd_mapi_venc_unregistercallback](#4134-kd_mapi_venc_unregistercallback)

##### 4.1.4.3 kd_venc_data_s

【Description】

Encoded data packet type.

【Definition】

```c
typedef struct
{
    [k_venc_chn_status](#3122-k_venc_chn_status);
    k_u32 u32_pack_cnt;
    [k_venc_data_pack_s](#4144-k_venc_data_pack_s) astPack[KD_VENC_MAX_FRAME_PACKCOUNT];
} kd_venc_data_s;
```

【Members】

| Member Name   | Description   |
|---------------|---------------|
| status        | Channel status|
| u32_pack_cnt  | Number of packs|
| astPack       | Data packs    |

【Notes】

None.

【Related Data Types and Interfaces】

[pfn_venc_dataproc](#4142-pfn_venc_dataproc)
[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

##### 4.1.4.4 k_venc_data_pack_s

【Description】

Encoded data packet type.

【Definition】

```c
typedef struct
{
    k_char *vir_addr;
    k_u64 phys_addr;
    k_u32 len;
    k_u64 pts;
    k_venc_pack_type type;
} k_venc_data_pack_s;
```

【Members】

| Member Name  | Description           |
|--------------|-----------------------|
| vir_addr     | Virtual address of the data pack |
| phys_addr    | Physical address of the data pack |
| len          | Length of the data pack|
| pts          | Timestamp             |
| type         | Stream pack type      |

【Notes】

Both `vir_addr` and `phys_addr` have one address.

【Related Data Types and Interfaces】

[kd_venc_data_s](#4143-kd_venc_data_s)

##### 4.1.4.5 KD_VENC_MAX_FRAME_PACKCOUNT

【Description】

Defines the maximum number of packs per frame.

【Definition】

```c
#define KD_VENC_MAX_FRAME_PACKCOUNT 12
```

【Notes】

None.

【Related Data Types and Interfaces】

None.

##### 4.1.4.6 KD_VENC_LIMITLESS_FRAME_COUNT

【Description】

Defines unlimited video encoding.

【Definition】

```c
#define KD_VENC_LIMITLESS_FRAME_COUNT -1
```

【Notes】

None.

【Related Data Types and Interfaces】

[kd_mapi_venc_start](#4135-kd_mapi_venc_start)

### 4.2 Video Decoding

#### 4.2.1 API

The video decoding module mainly provides functions for creating and destroying video decoding channels, starting and stopping the reception of images on decoding channels, setting and getting decoding channel attributes, and binding output decoded images to VO.

This functional module provides the following MAPI:

[kd_mapi_vdec_init](#4211-kd_mapi_vdec_init)

[kd_mapi_vdec_deinit](#4212-kd_mapi_vdec_deinit)

[kd_mapi_vdec_start](#4213-kd_mapi_vdec_start)

[kd_mapi_vdec_stop](#4214-kd_mapi_vdec_stop)

[kd_mapi_vdec_bind_vo](#4137-kd_mapi_venc_bind_vi)

[kd_mapi_vdec_unbind_vo](#4138-kd_mapi_venc_unbind_vi)

[kd_mapi_vdec_send_stream](#4139-kd_mapi_venc_request_idr)

[kd_mapi_vdec_query_status](#4218-kd_mapi_vdec_query_status)

##### 4.2.1.1 kd_mapi_vdec_init

【Description】

Initializes the decoding channel.

【Syntax】

```c
k_s32 kd_mapi_vdec_init(k_u32 chn_num, const [k_vdec_chn_attr](#323-k_vdec_chn_attr) *attr);
```

【Parameters】

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |
| attr           | Pointer to VDEC channel attributes. Static attributes. | Input       |

【Return Value】

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the error code |

【Chip Differences】

None.

【Requirements】

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

【Notes】

- Before calling this interface, `kd_mapi_sys_init()` and `kd_mapi_media_init()` need to be successfully initialized. See the "SYS MAPI" section for details.
- Reinitialization returns success.

【Example】

Please refer to the `sample_vdec` code.

【Related Topics】

[kd_mapi_vdec_deinit](#4212-kd_mapi_vdec_deinit)

##### 4.2.1.2 kd_mapi_vdec_deinit

【Description】

Deinitializes the decoding channel.

**Syntax**:

```c
k_s32 kd_mapi_vdec_deinit(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mapi_vdec_init](#4211-kd_mapi_vdec_init)

##### 4.2.1.3 kd_mapi_vdec_start

**Description**:

Starts the decoding channel.

**Syntax**:

```c
k_s32 kd_mapi_vdec_start(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mapi_vdec_stop](#4214-kd_mapi_vdec_stop)

##### 4.2.1.4 kd_mapi_vdec_stop

**Description**:

Stops the decoding channel.

**Syntax**:

```c
k_s32 kd_mapi_vdec_stop(k_u32 chn_num);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mapi_vdec_start](#4213-kd_mapi_vdec_start)

##### 4.2.1.5 kd_mapi_vdec_bind_vo

**Description**:

Binds the decoding channel to the output source VO.

**Syntax**:

```c
k_s32 kd_mapi_vdec_bind_vo(k_s32 chn_num, k_s32 vo_dev, k_s32 vo_chn);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |
| vo_dev         | Output VO device ID                        | Input        |
| vo_chn         | Output VO device channel                   | Input        |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mapi_vdec_unbind_vo](#4216-kd_mapi_vdec_unbind_vo)

##### 4.2.1.6 kd_mapi_vdec_unbind_vo

**Description**:

Unbinds the output source VO from the decoding channel.

**Syntax**:

```c
k_s32 kd_mapi_vdec_unbind_vo(k_s32 chn_num, k_s32 vo_dev, k_s32 vo_chn);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |
| vo_dev         | Output VO device ID                        | Input        |
| vo_chn         | Output VO device channel                   | Input        |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

[kd_mapi_vdec_bind_vo](#4215-kd_mapi_vdec_bind_vo)

##### 4.2.1.7 kd_mapi_vdec_send_stream

**Description**:

Sends stream data for decoding.

**Syntax**:

```c
k_s32 kd_mapi_vdec_send_stream(k_u32 chn_num, [k_vdec_stream](#326-k_vdec_stream) *stream, k_s32 milli_sec);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | VDEC channel number. Range: `[0, VDEC_MAX_CHN_NUM)` | Input       |
| stream         | Pointer to the stream data for decoding    | Input        |
| milli_sec      | Flag for sending stream data. Range: `-1`: Blocking, `0`: Non-blocking, Positive value: Timeout period in milliseconds | Input        |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

##### 4.2.1.8 kd_mapi_vdec_query_status

**Description**:

Queries the status of the decoding channel.

**Syntax**:

```c
k_s32 kd_mapi_vdec_query_status(k_u32 chn_num, k_vdec_chn_status *status);
```

**Parameters**:

| Parameter Name | Description                                | Input/Output |
|----------------|--------------------------------------------|--------------|
| chn_num        | Encoding channel information. Range: `[0, [K_VDEC_MAX_CHN_NUM](#321-k_vdec_max_chn_num))` | Input       |
| status         | Pointer to the video decoding channel status structure | Output      |

**Return Values**:

| Return Value | Description             |
|--------------|-------------------------|
| 0            | Success                 |
| Non-zero     | Failure, the value is the [error code](#5. Error Codes) |

**Chip Differences**:

None.

**Requirements**:

Header files: `mapi_vdec_api.h`, `k_vdec_comm.h`
Library files: `libmapi.a`, `libipcmsg.a`, `libdatafifo.a`

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

## 5. Error Codes

Table 41 Encoding API Error Codes
| Error Code | Macro Definition           | Description                                    |
|------------|----------------------------|------------------------------------------------|
| 0xa0098001 | K_ERR_VENC_INVALID_DEVID   | Device ID out of valid range                   |
| 0xa0098002 | K_ERR_VENC_INVALID_CHNID   | Channel ID out of valid range                  |
| 0xa0098003 | K_ERR_VENC_ILLEGAL_PARAM   | Parameters out of valid range                  |
| 0xa0098004 | K_ERR_VENC_EXIST           | Attempt to create an existing device, channel, or resource |
| 0xa0098005 | K_ERR_VENC_UNEXIST         | Attempt to use or destroy a non-existent device, channel, or resource |
| 0xa0098006 | K_ERR_VENC_NULL_PTR        | Null pointer in function parameter             |
| 0xa0098007 | K_ERR_VENC_NOT_CONFIG      | Not configured before use                      |
| 0xa0098008 | K_ERR_VENC_NOT_SUPPORT     | Unsupported parameter or function              |
| 0xa0098009 | K_ERR_VENC_NOT_PERM        | Operation not allowed, such as trying to modify static configuration parameters |
| 0xa009800c | K_ERR_VENC_NOMEM           | Memory allocation failure, such as insufficient system memory |
| 0xa009800d | K_ERR_VENC_NOBUF           | Buffer allocation failure, such as requested data buffer too large |
| 0xa009800e | K_ERR_VENC_BUF_EMPTY       | No data in the buffer                          |
| 0xa009800f | K_ERR_VENC_BUF_FULL        | Data in the buffer is full                     |
| 0xa0098010 | K_ERR_VENC_NOTREADY        | System not initialized or corresponding module not loaded |
| 0xa0098011 | K_ERR_VENC_BADADDR         | Address out of valid range                     |
| 0xa0098012 | K_ERR_VENC_BUSY            | VENC system busy                               |

Table 42 Decoding API Error Codes
| Error Code | Macro Definition           | Description                                    |
|------------|----------------------------|------------------------------------------------|
| 0xa00a8001 | K_ERR_VDEC_INVALID_DEVID   | Device ID out of valid range                   |
| 0xa00a8002 | K_ERR_VDEC_INVALID_CHNID   | Channel ID out of valid range                  |
| 0xa00a8003 | K_ERR_VDEC_ILLEGAL_PARAM   | Parameters out of valid range                  |
| 0xa00a8004 | K_ERR_VDEC_EXIST           | Attempt to create an existing device, channel, or resource |
| 0xa00a8005 | K_ERR_VDEC_UNEXIST         | Attempt to use or destroy a non-existent device, channel, or resource |
| 0xa00a8006 | K_ERR_VDEC_NULL_PTR        | Null pointer in function parameter             |
| 0xa00a8007 | K_ERR_VDEC_NOT_CONFIG      | Not configured before use                      |
| 0xa00a8008 | K_ERR_VDEC_NOT_SUPPORT     | Unsupported parameter or function              |
| 0xa00a8009 | K_ERR_VDEC_NOT_PERM        | Operation not allowed, such as trying to modify static configuration parameters |
| 0xa00a800c | K_ERR_VDEC_NOMEM           | Memory allocation failure, such as insufficient system memory |
| 0xa00a800d | K_ERR_VDEC_NOBUF           | Buffer allocation failure, such as requested data buffer too large |
| 0xa00a800e | K_ERR_VDEC_BUF_EMPTY       | No data in the buffer                          |
| 0xa00a800f | K_ERR_VDEC_BUF_FULL        | Data in the buffer is full                     |
| 0xa00a8010 | K_ERR_VDEC_NOTREADY        | System not initialized or corresponding module not loaded |
| 0xa00a8011 | K_ERR_VDEC_BADADDR         | Address out of valid range                     |
| 0xa00a8012 | K_ERR_VDEC_BUSY            | VDEC system busy                               |

## 6. Debug Information

For multimedia memory management and system binding debug information, please refer to the "K230 System Control API Reference".
