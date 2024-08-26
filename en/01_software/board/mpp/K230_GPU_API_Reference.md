# K230 GPU API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase should be subject to the commercial contracts and terms of Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not make any explicit or implicit representations or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document describes the usage guide for the 2.5D GPU module of the K230 chip.

### Intended Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviations

| Abbreviation | Full Name              |
|--------------|------------------------|
| GPU          | Graphics Processing Unit |
| BLIT         | Bit Block Transfer     |
| CLUT         | Color Look Up Table    |

### Revision History

| Version Number | Description   | Modified By | Date       |
|----------------|---------------|-------------|------------|
| V1.0           | Official Release | Huang Ziyi | 2023/04/06 |
| V1.1           | Format Adjustment | Huang Ziyi | 2023/05/06 |

## 1. Function Introduction

This module is mainly used to accelerate the drawing of vector graphics, which can be used to draw menus and other pages and supports the acceleration of some lvgl drawings. The GPU has a series of drawing instructions. After writing the drawing instructions into memory and submitting the address and total length of the instructions to the GPU, drawing can begin. This module supports the filled drawing of polygons, quadratic Bezier curves, cubic Bezier curves, and elliptical curves, supports linear gradient fills, supports color lookup tables, supports image composition and blending, and supports BLIT.

## 2. Data Flow

The GPU software driver part includes the device /dev/vg_lite and its kernel module driver vg_lite.ko, as well as the user-space function library libvg_lite.so. libvg_lite.so will open the /dev/vg_lite device and interact with the kernel space driver through ioctl() and mmap(). The kernel space driver is mainly implemented by vg_lite_hal.c. The functions in vg_lite.c call the functions in vg_lite_hal.c through the vg_lite_kernel function to perform actual register operations.

Note: The driver does not check the physical addresses in the drawing instructions. Calling the VGLite API can indirectly read and write all physical addresses in DDR memory.

## 3. Software Interface

The software interface is detailed in the header file vg_lite.h in the software package.

### 3.1 Main Types and Definitions

#### 3.1.1 Parameter Types

| Name            | Type Definition         | Meaning                                                                                                                                                                                                                   |
|-----------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Int32_t         | int                     | 32-bit signed integer                                                                                                                                                                                                     |
| uint32_t        | Unsigned int            | 32-bit unsigned integer                                                                                                                                                                                                   |
| VG_LITE_S8      | enum vg_lite_format_t   | 8-bit signed integer coordinate                                                                                                                                                                                            |
| VG_LITE_S16     | enum vg_lite_format_t   | 16-bit signed integer coordinate                                                                                                                                                                                           |
| VG_LITE_S32     | enum vg_lite_format_t   | 32-bit signed integer coordinate                                                                                                                                                                                           |
| vg_lite_float_t | float                   | Single precision floating-point number                                                                                                                                                                                     |
| vg_lite_color_t | uint32_t                | 32-bit color value. The color value specifies the color used in various functions. The color is formed by 8-bit RGBA channels. The red channel is in the lowest 8 bits of the color value, followed by green and blue channels. The alpha channel is in the highest 8 bits of the color value. For the L8 target format, the RGB color is converted to L8 using the default ITU-R BT.709 conversion rules. |

#### 3.1.2 Error Types vg_lite_error_t

| Enumeration                  | Description                |
|------------------------------|----------------------------|
| VG_LITE_GENERIC_IO           | Unable to communicate with the kernel driver |
| VG_LITE_INVALID_ARGUMENT     | Invalid argument           |
| VG_LITE_MULTI_THREAD_FAIL    | Multi-thread error         |
| VG_LITE_NO_CONTEXT           | No context error           |
| VG_LITE_NOT_SUPPORT          | Function not supported     |
| VG_LITE_OUT_OF_MEMORY        | No allocatable driver heap memory |
| VG_LITE_OUT_OF_RESOURCES     | No allocatable system heap memory |
| VG_LITE_SUCCESS              | Success                    |
| VG_LITE_TIMEOUT              | Timeout                    |
| VG_LITE_ALREADY_EXISTS       | Object already exists      |
| VG_LITE_NOT_ALIGNED          | Data alignment error       |

#### 3.1.3 Functional Enumerations

| Enumeration                    | Description               |
|--------------------------------|---------------------------|
| gcFEATURE_BIT_VG_BORDER_CULLING | Border culling            |
| gcFEATURE_BIT_VG_GLOBAL_ALPHA   | Global Alpha              |
| gcFEATURE_BIT_VG_IM_FASTCLEAR  | Fast clear                |
| gcFEATURE_BIT_VG_IM_INDEX_FORMAT | Color index               |
| gcFEATURE_BIT_VG_PE_PREMULTIPLY | Alpha channel premultiplication |
| gcFEATURE_BIT_VG_RADIAL_GRADIENT | Radial gradient           |
| gcFEATURE_BIT_VG_RGBA2_FORMAT  | RGBA2222 format           |

### 3.2 GPU Control

Unless otherwise specified, the application must initialize the GPU implicit (global) context by calling [vg_lite_init](#3212-vg_lite_init) before calling any API functions. This function will fill the feature table, reset the fast clear buffer, reset the composition target buffer, and allocate command and tessellation buffers.

The GPU driver **only supports one current context and one thread to issue commands to the GPU**. The GPU driver does not support multiple concurrent contexts running in multiple threads/processes because the GPU kernel driver does not support context switching. GPU applications can only use one context to issue commands to the GPU hardware at any time. If the GPU application needs to switch contexts, it should call [vg_lite_close](#3213-vg_lite_close) to close the current context in the current thread and then call [vg_lite_init](#3212-vg_lite_init) to initialize a new context in the current thread or other threads/processes.

Unless otherwise specified, all functions return [vg_lite_error_t](#312-error-types-vg_lite_error_t).

#### 3.2.1 Context Initialization and Control Functions

##### 3.2.1.1 vg_lite_set_command_buffer_size

- Description

    This function is optional. If you need to change the size of the command buffer, it must be called before vg_lite_init. The default size of the command buffer is 64KB. This does not mean that the commands of a frame must be smaller than 64KB. When the buffer is full, rendering will be submitted directly to clear the buffer. A larger buffer means lower frequency rendering submissions, which can reduce system call overhead.

- Parameters

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| size           | Command buffer size | Input        |

##### 3.2.1.2 vg_lite_init

- Description

    This function initializes the memory and data structures required for GPU drawing/filling functions, allocates memory for the command buffer and tessellation buffer of the specified size. The width and height of the tessellation buffer must be multiples of 16. The tessellation window can be specified according to the amount of available memory in the system and the required performance. A smaller window can have less memory usage but may result in lower performance. The minimum window that can be used for tessellation is 16x16. If the height or width is less than 0, then the tessellation buffer will not be created, which can be used for fill-only cases.

    If this will be the first context to access the hardware, the hardware will be opened and initialized. If a new context needs to be initialized, vg_lite_close must be called to close the current context. Otherwise, vg_lite_init will return an error.

- Parameters

| Parameter Name      | Description                                                                                                             | Input/Output |
|---------------------|-------------------------------------------------------------------------------------------------------------------------|--------------|
| tessellation_width  | Tessellation window width. Must be a multiple of 16, the minimum is 16, the maximum cannot be greater than the frame width. If it is 0, it means no tessellation is used, then the GPU will only run blit. | Input        |
| tessellation_height | Tessellation window height. Must be a multiple of 16, the minimum is 16, the maximum cannot be greater than the frame width. If it is 0, it means no tessellation is used, then the GPU will only run blit. | Input        |

##### 3.2.1.3 vg_lite_close

- Description

    Deletes all resources and frees all memory previously initialized by the vg_lite_init function. If this is the only active context, it will also automatically close the hardware.

##### 3.2.1.4 vg_lite_finish

- Description

    This function explicitly submits the command buffer to the GPU and waits for its completion.

##### 3.2.1.5 vg_lite_flush

- Description

    This function explicitly submits the command buffer to the GPU without waiting for its completion.

#### 3.2.2 Pixel Buffer

##### 3.2.2.1 Memory Alignment Requirements

###### 3.2.2.1.1 Source Image Alignment Requirements

The GPU hardware requires that the width of the rasterized image be a multiple of 16 pixels. This requirement applies to all image formats. Therefore, the user needs to pad any image width to a multiple of 16 pixels for the GPU hardware to work correctly.

The byte alignment requirements for pixels depend on the specific pixel format.

| Image Format                   | Bits Per Pixel | Alignment Requirement | Supported as Source Image | Supported as Target Image |
|--------------------------------|----------------|------------------------|----------------------------|----------------------------|
| VG_LITE_INDEX1                 | 1              | 8B                     | Yes                        | No                         |
| VG_LITE_INDEX2                 | 2              | 8B                     | Yes                        | No                         |
| VG_LITE_INDEX4                 | 4              | 8B                     | Yes                        | No                         |
| VG_LITE_INDEX8                 | 8              | 16B                    | Yes                        | No                         |
| VG_LITE_A4                     | 4              | 8B                     | Yes                        | No                         |
| VG_LITE_A8                     | 8              | 16B                    | Yes                        | Yes                        |
| VG_LITE_L8                     | 8              | 16B                    | Yes                        | Yes                        |
| VG_LITE_ARGB2222               | 8              | 16B                    | Yes                        | Yes                        |
| VG_LITE_RGB565                 | 16             | 32B                    | Yes                        | Yes                        |
| VG_LITE_ARGB1555               | 16             | 32B                    | Yes                        | Yes                        |
| VG_LITE_ARGB4444               | 16             | 32B                    | Yes                        | Yes                        |
| VG_LITE_ARGB8888/XRGB8888      | 32             | 64B                    | Yes                        | Yes                        |

###### 3.2.2.1.2 Render Target Buffer Alignment Requirements

The GPU hardware requires that the width of the pixel buffer be a multiple of 16 pixels. This requirement applies to all image formats. Therefore, the user needs to align any pixel buffer width to a multiple of 16 pixels for the GPU hardware to work correctly. The byte alignment requirements for pixels depend on the specific pixel format.

Refer to the alignment requirements summary table 2: Image Source Alignment Summary later in this document.

The starting address alignment requirements for the pixel buffer depend on whether the buffer layout format is tiled or linear (vg_lite_buffer_layout_t enum).

- If the format is tiled (4x4 tiled), the starting address and stride need to be 64-byte aligned.

- If the format is linear, the starting address and stride have no alignment requirements.

##### 3.2.2.2 Pixel Cache

The GPU includes two fully associative caches. Each cache has 8 lines, and each line has 64 bytes. In this case, a cache line can hold a 4x4 pixel tile or a 16x1 pixel line.

#### 3.2.3 Enumeration Types

##### 3.2.3.1 vg_lite_buffer_format_t

- This enumeration type specifies the color format used for the buffer.

    Note: For a summary of image format alignment requirements, see the [Memory Alignment Requirements](#3221-memory-alignment-requirements) after the numerical descriptions.

| vg_lite_buffer_format_t | Description                       | Supported as Source | Supported as Target | Alignment (Bytes) |
|-------------------------|-----------------------------------|---------------------|---------------------|-------------------|
| VG_LITE_ABGR8888        | 8 bits per channel, alpha in low 8 bits | Yes                 | Yes                 | 64                |
| VG_LITE_ARGB8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_BGRA8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_RGBA8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_BGRX8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_RGBX8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_XBGR8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_XRGB8888        |                                   | Yes                 | Yes                 | 64                |
| VG_LITE_ABGR1555        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_ARGB1555        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_BGRA5551        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_RGBA5551        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_BGR565          |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_RGB565          |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_ABGR4444        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_ARGB4444        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_BGRA4444        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_RGBA4444        |                                   | Yes                 | Yes                 | 32                |
| VG_LITE_A4              | 4 bits alpha, no RGB              | Yes                 | No                  | 8                 |
| VG_LITE_A8              | 8 bits alpha, no RGB              | Yes                 | Yes                 | 16                |
| VG_LITE_ABGR2222        |                                   | Yes                 | Yes                 | 16                |
| VG_LITE_ARGB2222        |                                   | Yes                 | Yes                 | 16                |
| VG_LITE_BGRA2222        |                                   | Yes                 | Yes                 | 16                |
| VG_LITE_RGBA2222        |                                   | Yes                 | Yes                 | 16                |
| VG_LITE_INDEX_1         | 1-bit index format                | Yes                 | No                  | 8                 |
| VG_LITE_INDEX_2         | 2-bit index format                | Yes                 | No                  | 8                 |
| VG_LITE_INDEX_4         | 4-bit index format                | Yes                 | No                  | 8                 |
| VG_LITE_INDEX_8         | 8-bit index format                | Yes                 | No                  | 8                 |

##### 3.2.3.2 vg_lite_buffer_image_mode_t

- Specifies how the image is rendered to the buffer.

| Enumeration               | Description             |
|---------------------------|-------------------------|
| VG_LITE_NORMAL_IMAGE_MODE | Image drawn with blend mode |
| VG_LITE_NONE_IMAGE_MODE   | Image input is ignored  |
| VG_LITE_MULTIPLY_IMAGE_MODE | Image multiplied with draw color |

##### 3.2.3.3 vg_lite_buffer_layout_t

- Specifies the buffer data layout in memory.

| Enumeration      | Description                                                                                   |
|------------------|-----------------------------------------------------------------------------------------------|
| VG_LITE_LINEAR   | Linear (scanline) layout. Note: This layout has no alignment requirements for the buffer.     |
| VG_LITE_TILED    | Data is organized into 4x4 pixel tiles. Note: For this layout, the buffer's starting address and stride need to be aligned to 64 bytes. |

##### 3.2.3.4 vg_lite_buffer_transparency_mode_t

- Specifies the transparency mode of a buffer.

| Enumeration                | Description                                                                                     |
|----------------------------|-------------------------------------------------------------------------------------------------|
| VG_LITE_IMAGE_OPAQUE       | Opaque image: All image pixels are copied to the VG PE for rasterization.                       |
| VG_LITE_IMAGE_TRANSPARENT  | Transparent image: Only non-transparent image pixels are copied to the VG PE. Note: This mode is only effective when the image mode is VG_LITE_NORMAL_IMAGE_MODE or VG_LITE_MULTIPLY_IMAGE_MODE. |

#### 3.2.4 Structures

##### 3.2.4.1 vg_lite_buffer_t

- This structure defines the buffer layout for images or memory data used by the GPU.

| Field              | Type                               | Description           |
|--------------------|------------------------------------|-----------------------|
| width              | int32_t                            | Buffer width in pixels|
| height             | int32_t                            | Buffer height in pixels|
| stride             | int32_t                            | Bytes per row         |
| tiled              | vg_lite_buffer_layout_t            | Linear or tiled       |
| format             | vg_lite_buffer_format_t            | Color type            |
| handle             | void \*                            | Memory handle         |
| memory             | void \*                            | Mapped virtual address|
| address            | uint32_t                           | Physical address      |
| yuv                | N/A                                | N/A                   |
| image_mode         | vg_lite_buffer_image_mode_t        | Blit mode             |
| transparency_mode  | vg_lite_buffer_transparency_mode_t | Transparency mode     |

#### 3.2.5 Functions

##### 3.2.5.1 vg_lite_allocate

- Description

    This function allocates memory for a buffer before it can be used in blit or draw functions.

    To allow hardware access to some memory, such as source images or target buffers, it needs to be allocated first. The provided [vg_lite_buffer_t](#3241-vg_lite_buffer_t) structure needs to be initialized with the size (width and height) and format of the requested buffer. If the stride is set to 0, this function will fill it in. The only input parameter to this function is a pointer to the buffer structure. If the structure has all the required information, appropriate memory will be allocated for the buffer.

    This function will call the kernel to actually allocate memory. The memory handle, logical address, and hardware address in the [vg_lite_buffer_t](#3241-vg_lite_buffer_t) structure will be filled in by the kernel.

- Parameters

    [vg_lite_buffer_t](#3241-vg_lite_buffer_t) \*buffer: Pointer to the buffer structure holding the size and format of the allocated buffer.

##### 3.2.5.2 vg_lite_free

- Description

    This function deallocates a previously allocated buffer, freeing the memory for that buffer.

- Parameters

    [vg_lite_buffer_t](#3241-vg_lite_buffer_t) \*buffer: Pointer to the buffer structure filled in by vg_lite_allocate.

##### 3.2.5.3 vg_lite_buffer_upload

- Description

    This function uploads pixel data to GPU memory. Note that the format of the data (pixels) to be uploaded must be the same as described in the buffer object. The input data memory buffer should contain enough data to upload to the GPU buffer pointed to by the input parameter "buffer".

- Parameters

    vg_lite_buffer_t \*buffer: Pointer to the buffer structure filled in by vg_lite_allocate.

    uint8_t \*data\[3\]: Pointer to the pixel data.

    uint32_t stride\[3\]: Row stride of the pixel data.

##### 3.2.5.4 vg_lite_map

- Description

    This function is used to import DMABUF into the GPU for use. Before calling, configure the buffer's width, height, format, stride, and memory properties. For specific usage, refer to the vglite_drm example.

- Parameters

    vg_lite_buffer_t \*buffer: Pointer to the buffer structure filled in by [vg_lite_allocate](#3251-vg_lite_allocate).

    vg_lite_map_flag_t flag: Currently only supports VG_LITE_MAP_DMABUF.

    int32_t fd: DMABUF fd.

##### 3.2.5.5 vg_lite_unmap

- Description

    This function unmaps the buffer and frees any memory resources previously allocated by vg_lite_map.

- Parameters

    vg_lite_buffer_t \*buffer: Pointer to the buffer structure filled in by [vg_lite_map](#3254-vg_lite_map).

##### 3.2.5.6 vg_lite_set_CLUT

- Description

    This function sets the color lookup table (CLUT) for indexed color images in the context state. Once the CLUT is set (non-null), the image pixel colors used for rendering indexed format images will be obtained from the color lookup table (CLUT) based on the pixel's color index value.

- Parameters

    uint32_t count: Number of colors in the color lookup table.

    For INDEX_1, the table can have up to 2 colors.

    For INDEX_2, the table can have up to 4 colors.

    For INDEX_4, the table can have up to 16 colors.

    For INDEX_8, the table can have up to 256 colors.

    uint32_t \*colors: Pointer to the color lookup table (CLUT) to be stored in the context and programmed into the command buffer when needed. The CLUT will not take effect until the command buffer is submitted to the hardware. Colors are in ARGB format, with A in the highest bit.

    Note: The driver does not verify the CLUT content from the application.

### 3.3 Matrix

#### 3.3.1 Structures

##### 3.3.1.1 vg_lite_matrix_t

- Description

    Defines a 3x3 floating-point matrix.

#### 3.3.2 Functions

##### 3.3.2.1 vg_lite_identity

- Description

    Sets the matrix to the identity matrix.

- Parameters

    vg_lite_matrix_t \*matrix: Pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t) structure to be loaded with the identity matrix.

##### 3.3.2.2 vg_lite_perspective

- Description

    Applies a perspective transformation to the matrix.

- Parameters

    vg_lite_float_t px: Perspective transformation matrix value.

    vg_lite_float_t py: Perspective transformation matrix value.

    vg_lite_matrix_t \*matrix: Pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t) structure to be perspective transformed.

##### 3.3.2.3 vg_lite_rotate

- Description

    Applies a rotation transformation to the matrix by the specified angle.

- Parameters

    vg_lite_float_t degrees: Degree of rotation (in degrees), positive for clockwise rotation.

    vg_lite_matrix_t \*matrix: Pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t) structure to be rotated.

##### 3.3.2.4 vg_lite_scale

- Description

    Applies vertical and horizontal scaling to the matrix.

- Parameters

    vg_lite_float_t scale_x: Horizontal scaling factor.

    vg_lite_float_t scale_y: Vertical scaling factor.

    vg_lite_matrix_t \*matrix: Pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t) structure to be scaled.

##### 3.3.2.5 vg_lite_translate

- Description

    Applies a translation transformation to the matrix.

- Parameters

    vg_lite_float_t x: Horizontal translation.

    vg_lite_float_t y: Vertical translation.

    vg_lite_matrix_t \*matrix: Pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t) structure to be translated.

### 3.4 BLITs for Composition and Blending

#### 3.4.1 Enumeration Types

##### 3.4.1.1 vg_lite_blend_t

This enumeration defines the blending modes supported by some VGLite API functions. S and D represent source and destination color channels, Sa and Da represent source and destination alpha channels.

Colors are displayed at 100% and 50% opacity.

| vg_lite_blend_t        | Description                |
|------------------------|----------------------------|
| VG_LITE_BLEND_ADDITIVE | S + D                      |
| VG_LITE_BLEND_DST_IN   | Sa * D                     |
| VG_LITE_BLEND_DST_OVER | (1 - Da) * S + D           |
| VG_LITE_BLEND_MULTIPLY | S \* (1 - Da) + D \* (1 - Sa) + S * D |
| VG_LITE_BLEND_NONE     | S                          |
| VG_LITE_BLEND_SCREEN   | S + D - S * D              |
| VG_LITE_BLEND_SRC_IN   | Da * S                     |
| VG_LITE_BLEND_SRC_OVER | S + (1 - Sa) * D           |
| VG_LITE_BLEND_SUBTRACT | D * (1 - Sa)               |

##### 3.4.1.2 vg_lite_filter_t

Specifies the sample filter mode in blit and draw APIs.

| vg_lite_filter_t       | Description                                |
|------------------------|--------------------------------------------|
| VG_LITE_FILTER_POINT   | Samples the nearest image pixel.           |
| VG_LITE_FILTER_LINEAR  | Uses linear interpolation along the scanline. |
| VG_LITE_FILTER_BI_LINEAR | Uses a 2x2 box around the image pixel and interpolates. |

##### 3.4.1.3 vg_lite_global_alpha_t

Specifies the global alpha mode in blit APIs.
| vg_lite_global_alpha_t  | Description                                                   |
|-------------------------|---------------------------------------------------------------|
| VG_LITE_NORMAL          | Uses the original src/dst alpha values.                       |
| VG_LITE_GLOBAL          | Replaces the original src/dst alpha values with global src/dst alpha values. |
| VG_LITE_SCALED          | Multiplies the global src/dst alpha values with the original src/dst alpha values. |

#### 3.4.2 Structures

##### 3.4.2.1 vg_lite_rectangle_t

This structure defines the organization of a rectangle's data.

| Field  | Type     | Description                     |
|--------|----------|---------------------------------|
| x      | int32_t  | x-coordinate, origin at top-left|
| y      | int32_t  | y-coordinate, origin at top-left|
| width  | int32_t  | Width                           |
| height | int32_t  | Height                          |

##### 3.4.2.2 vg_lite_point_t

This structure defines a 2D point.

| Field | Type     | Description |
|-------|----------|-------------|
| x     | int32_t  | X-coordinate|
| y     | int32_t  | Y-coordinate|

##### 3.4.2.3 vg_lite_point4_t

This structure defines four 2D points that form a polygon. These points are defined by the vg_lite_point_t structure.

| Field            | Type         | Description   |
|------------------|--------------|---------------|
| vg_lite_point\[4\] | int32_t each | Array of 4 points |

#### 3.4.3 Functions

##### 3.4.3.1 vg_lite_blit

- Description

    BLIT function. The BLIT operation is performed through a source buffer and a target buffer. The source and target buffer structures are defined using the vg_lite_buffer_t structure. The BLIT copies the source image to the target buffer using a specified matrix, which can include translation, rotation, scaling, and perspective correction. Note that the vg_lite_buffer_t does not support oversampling anti-aliasing, so the edges of the target buffer may not be smooth, especially with a rotation matrix. Path rendering can be used to achieve high-quality oversampled anti-aliasing (16X, 4X) rendering effects.

- Parameters

    vg_lite_buffer_t \*target: Pointer to the vg_lite_buffer_t structure defining the target buffer. For valid target color formats for the blit function, see [Source Image Alignment Requirements](#32211-source-image-alignment-requirements).

    vg_lite_buffer_t \*source: Pointer to the vg_lite_buffer_t structure defining the source buffer. All color formats in the [vg_lite_buffer_format_t](#3231-vg_lite_buffer_format_t) enumeration are valid source formats for the blit function.

    vg_lite_matrix_t \*matrix: Pointer to a vg_lite_matrix_t structure defining the 3x3 transformation matrix from source pixels to target pixels. If the matrix is NULL, it is assumed to be an identity matrix, meaning the source pixels will be directly copied to the (0,0) position of the target pixels.

    vg_lite_blend_t blend: Specifies one of the blending modes supported by the hardware to be applied to each image pixel. If no blending is required, set this value to VG_LITE_BLEND_NONE. Note: If the "matrix" parameter is specified for rotation or perspective, and the "blend" parameter is specified as VG_LITE_BLEND_NONE, VG_LITE_BLEND_SRC_IN, or VG_LITE_BLEND_DST_IN, the driver will override the application's settings for the BLIT operation, and the transparency mode will always be set to TRANSPARENT. This is due to some limitations of the GPU hardware.

    vg_lite_color_t color: If non-zero, this color value is used as the blend color. The blend color is multiplied with each source pixel before blending occurs. If you do not need a blend color, set the color parameter to 0.

    vg_lite_filter_t filter: Specifies the type of filtering mode. All formats in the vg_lite_filter_t enumeration are valid formats for this function.

##### 3.4.3.2 vg_lite_blit_rect

- Description

    BLIT rectangle function.

- Parameters

    vg_lite_buffer_t \*target: Refer to vg_lite_blit.

    vg_lite_buffer_t \*source: Refer to vg_lite_blit.

    uint32_t \*rect: Specifies the rectangular area to BLIT.

    vg_lite_matrix_t \*matrix: Refer to vg_lite_blit.

    vg_lite_blend_t \*blend: Refer to vg_lite_blit.

    vg_lite_color_t color: Refer to vg_lite_blit.

    vg_lite_filter_t filter: Refer to vg_lite_blit.

##### 3.4.3.3 vg_lite_get_transform_matrix

- Description

    This function obtains a 3x3 homogeneous transformation matrix from source coordinates and destination coordinates.

- Parameters

    vg_lite_point4_t src: Pointer to a set of four 2D points forming the source polygon.

    vg_lite_point4_t dst: Pointer to a set of four 2D points forming the destination polygon.

    vg_lite_matrix_t \*mat: Output parameter, pointer to a 3x3 homogeneous matrix that transforms the source polygon to the destination polygon.

##### 3.4.3.4 vg_lite_clear

- Description

    This function performs a clear operation, clearing/filling the specified pixel buffer (either the entire buffer or a rectangular portion of the buffer) with a specified color.

- Parameters

    vg_lite_buffer_t \*target: Refer to vg_lite_blit.

    vg_lite_rectangle_t \*rectangle: Pointer to a vg_lite_rectangle_t structure specifying the area to fill. If this rectangle is NULL, the entire target buffer will be filled with the specified color.

    vg_lite_color_t color: The fill color, as specified in the vg_lite_color_t enumeration, which is the color value used to fill the buffer. If the buffer is in L8 format, the RGBA color will be converted to a luminance value.

#### 3.4.4 Global Alpha Functions

##### 3.4.4.1 vg_lite_set_image_global_alpha

- Description

    This function sets the image/source global alpha and returns a status error code.

- Parameters

    vg_lite_global_alpha_t alpha_mode: Global Alpha mode, see [vg_lite_global_alpha_t](#3413-vg_lite_global_alpha_t).

    uint32_t alpha_value: The global Alpha value to set for the image/source.

##### 3.4.4.2 vg_lite_set_dest_global_alpha

- Description

    This function sets the destination global alpha and returns a status error code.

- Parameters

    vg_lite_global_alpha_t alpha_mode: Global Alpha mode, see [vg_lite_global_alpha_t](#3413-vg_lite_global_alpha_t).

    uint32_t alpha_value: The global Alpha value to set for the destination.

### 3.5 Vector Path Control

#### 3.5.1 Enumeration Types

##### 3.5.1.1 vg_lite_quality_t

Specifies the level of hardware-assisted anti-aliasing.

| vg_lite_quality_t  | Description                                           |
|--------------------|-------------------------------------------------------|
| VG_LITE_HIGH       | High quality: 16x coverage sampling anti-aliasing     |
| *VG_LITE_UPPER*    | *High quality: 8x coverage sampling anti-aliasing (discontinued as of June 2020).* |
| VG_LITE_MEDIUM     | Medium quality: 4x coverage sampling anti-aliasing    |
| VG_LITE_LOW        | Low quality: No anti-aliasing                         |

#### 3.5.2 Structures

##### 3.5.2.1 vg_lite_hw_memory

This structure simply records the kernel's memory allocation information.

| Field     | Type      | Description                                                                                     |
|-----------|-----------|-------------------------------------------------------------------------------------------------|
| handle    | void \*   | GPU memory object handle                                                                        |
| memory    | void \*   | Logical address                                                                                 |
| address   | uint32_t  | GPU memory address                                                                              |
| bytes     | uint32_t  | Size                                                                                            |
| property  | uint32_t  | Bit 0 indicates path upload. 0: Disable path data upload (always embedded in command buffer). 1: Enable automatic path data upload. |

##### 3.5.2.2 vg_lite_path_t

This structure describes vector path data.

Path data consists of opcodes and coordinates. The format of the opcodes is always VG_LITE_S8. For detailed information about the opcodes, refer to the section on [Vector Path OpCodes](#354-vector-path-opcodes) in this document.

| Field             | Type                   | Description                                           |
|-------------------|------------------------|-------------------------------------------------------|
| bounding_box\[4\] | vg_lite_float_t        | Bounding box of the path. \[0\] Left \[1\] Top \[2\] Right \[3\] Bottom |
| quality           | vg_lite_quality_t      | Enumeration type for path quality, anti-aliasing level |
| format            | enum vg_lite_format_t  | Enumeration type for coordinate format                |
| uploaded          | vg_lite_hw_memory_t    | Structure with path data uploaded to GPU-addressable memory |
| path_length       | int32_t                | Length of the path in bytes                           |
| path              | void \*                | Pointer to the path data                              |
| path_changed      | int32_t                | 0: Unchanged; 1: Changed.                             |

Regarding coordinate format and data alignment.

| vg_lite_format_t  | Path Data Alignment |
|-------------------|---------------------|
| VG_LITE_S8        | 8 bit               |
| VG_LITE_S16       | 2 bytes             |
| VG_LITE_S32       | 4 bytes             |

###### 3.5.2.2.1 Special Notes on Path Objects

- Endianness does not matter as it is boundary-aligned.
- Multiple consecutive opcodes should be packed according to the specified data format size. For example, for VG_LITE_S16 pack by 2 bytes, for VG_LITE_S32 pack by 4 bytes. Since opcodes are 8-bit (1 byte), for 16-bit (2 bytes) or 32-bit (4 bytes) data types:

...

\<opcode1_that_needs_data\>, opcode is 8-bit.

\<align_to_data_size\> (align to data size).

\<data_for_opcode1\> \<align_to_data_size\> \<data_for_opcode1\>

\<opcode2_that_doesnt_need_data\> \<opcode2_that_doesnt_need_data\>

\<opcode3_that_needs_data\>

\<align_to_data_size\>

\<data_for_opcode3\> \<data_for_opcode3\>

...

The path data in the array should always be aligned to 1, 2, or 4 bytes, depending on the format. For example, for 32-bit (4 bytes) data type:

...

\<opcode1_that_needs_data\> \<opcode1_that_needs_data\>

\<pad to 4 bytes\>

\<4 byte data_for_opcode1\> (4 bytes).

\<opcode2_that_doesnt_need_data\> \<opcode2_that_doesnt_need_data\>

\<opcode3_that_needs_data\>

\<pad to 4 bytes\>

\<4 byte data_for_opcode3\>

...

For float types, use IEEE754 encoding specification, while the opcode remains an 8-bit signed integer, special handling by software may be required.

#### 3.5.3 Functions

##### 3.5.3.1 vg_lite_path_calc_length

- Description

    This function calculates the buffer length (in bytes) for path commands. Applications can allocate a buffer as a command buffer using the length calculated by this function.

- Parameters

    uint8_t \*cmd: Pointer to the array of opcodes used to build the path.

    uint32_t count: Number of opcodes.

    vg_lite_format_t format: Coordinate data format, all formats available in vg_lite_format_t are valid formats for this function.

##### 3.5.3.2 vg_lite_path_append

- Description

    This function assembles the command buffer for the path. It creates the final GPU command for the path based on the input opcodes (cmd) and coordinates (data).

- Parameters

    vg_lite_path_t \*path: Pointer to the vg_lite_path_t structure with the path definition.

    uint8_t \*cmd: Pointer to the array of opcodes used to build the path.

    void \*data: Pointer to the array of coordinate data used to build the path.

    uint32_t seg_count: Number of opcodes.

##### 3.5.3.3 vg_lite_init_path

- Description

    This function initializes a path definition with specified values.

- Parameters

    vg_lite_path_t \*path: Pointer to the vg_lite_path_t structure for the path object to be initialized with specified member values.

    vg_lite_format_t data_format: Coordinate data format. All formats in the vg_lite_format_t enumeration are valid formats for this function.

    vg_lite_quality_t quality: Quality of the path object. All formats in the vg_lite_quality_t enumeration are valid formats for this function.

    uint32_t path_length: Length of the path data in bytes.

    void \*path_data: Pointer to the path data.

    vg_lite_float_t min_x, vg_lite_float_t min_y, vg_lite_float_t max_x, vg_lite_float_t max_y: Minimum and maximum x and y values specifying the bounding box of the path.

##### 3.5.3.4 vg_lite_init_arc_path

- Description

    This function initializes an arc path definition with specified values.
- Parameters

    vg_lite_path_t \*path: Refer to vg_lite_init_path.

    vg_lite_format_t data_format: Refer to vg_lite_init_path.

    vg_lite_quality_t quality: Refer to vg_lite_init_path.

    uint32_t path_length: Refer to vg_lite_init_path.

    void \*path_data: Refer to vg_lite_init_path.

    vg_lite_float_t min_x, vg_lite_float_t min_y, vg_lite_float_t max_x, vg_lite_float_t max_y: Refer to vg_lite_init_path.

##### 3.5.3.5 vg_lite_upload_path

- Description

    This function is used to upload a path to GPU memory.

    Normally, the GPU driver copies any path data into a command buffer structure during runtime. If there are many paths to render, this can take some time. Additionally, in embedded systems, path data typically does not change, so it makes sense to upload the path data in a format that the GPU can directly access. This function prompts the driver to allocate a buffer that will contain the path data and the necessary command buffer header and footer data, allowing the GPU to directly access this data. After the path is used, call vg_lite_clear_path to release this buffer.

- Parameters

    vg_lite_path_t \*path: Pointer to the vg_lite_path_t structure containing the path to upload.

##### 3.5.3.6 vg_lite_clear_path

- Description

    This function clears and resets the path member values. If the path has been uploaded, it will release the GPU memory allocated during the path upload.

- Parameters

    vg_lite_path_t \*path: Pointer to the vg_lite_path_t path definition to clear.

#### 3.5.4 Vector Path OpCodes

The following opcodes are the path drawing commands available for vector path data.

A path operation is submitted to the GPU in the form of [opcode | coordinates]. The opcode is stored in VG_LITE_S8 format, while the coordinates are specified by vg_lite_format_t.

| Opcode | Parameters                           | Description                                                                                                                                                                                                                   |
|--------|--------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | None                                 | END. Finish and close all open paths.                                                                                                                                                                                          |
| 0x02   | (x,y)                                | MOVE. Move to the given vertex. Close all open paths.  𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                                                                         |
| 0x03   | (Δx,Δy)                              | MOVE_REL. Move to the given relative point. Close all open paths.  𝑠𝑡𝑎𝑟𝑡𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦                                                                                                                                   |
| 0x04   | (x,y)                                | LINE. Draw a line to the given vertex.  𝐿𝑖𝑛𝑒(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                                                               |
| 0x05   | (Δx,Δy)                              | LINE_REL. Draw a line to the vertex at the relative position.  𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝐿𝑖𝑛𝑒(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                               |
| 0x06   | (cx,cy) (x,y)                        | QUAD. Draw a quadratic curve to the given endpoint using the specified control point.  𝑄𝑢𝑎𝑑(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑐𝑥,𝑐𝑦,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                                 |
| 0x07   | (Δcx,Δcy)  (Δx,Δy)                   | QUAD_REL. Draw a quadratic curve to the endpoint at the relative position using the specified relative control point.  𝑐𝑥= 𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑐𝑥 𝑐𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑐𝑦 𝑥= 𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝑄𝑢𝑎𝑑(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑐𝑥,𝑐𝑦,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                         |
| 0x08   | (cx1,cy1) (cx2,cy2) (x,y)            | CUBIC. Draw a cubic curve to the given endpoint using the specified control points.  𝐶𝑢𝑏𝑖𝑐(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑐𝑥1,𝑐𝑦1,𝑐𝑥2,𝑐𝑦2,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                       |
| 0x09   | (Δcx1,Δcy1)  (Δcx2,Δcy2)  (Δx,Δy)    | CUBIC_REL. Draw a cubic curve to the endpoint at the relative position using the specified control points.  𝑐𝑥1= 𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑐𝑥1 𝑐𝑦1=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑐𝑦1 𝑐𝑥2=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑐𝑥2 𝑐𝑦2=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑐𝑦2 𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝐶𝑢𝑏𝑖𝑐(𝑠𝑡𝑎𝑟𝑡𝑥,𝑠𝑡𝑎𝑟𝑡𝑦,𝑐𝑥1,𝑐𝑦1,𝑐𝑥2,𝑐𝑦2,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦  |
| 0x0A   | (rh,rv,rot,x,y)                      | SCCWARC. Draw a small counter-clockwise arc to the given endpoint using the specified radii and rotation angle.  𝑺𝑪𝑪𝑾𝑨𝑹𝑪(𝒓𝒉,𝒓𝒗,𝒓𝒐𝒕,𝒙,𝒚) 𝒔𝒕𝒂𝒓𝒕𝒙=𝒙 𝒔𝒕𝒂𝒓𝒕𝒚=𝒚                                                                                                            |
| 0x0B   | (rh,rv,rot,x,y)                      | SCCWARC_REL. Draw a small counter-clockwise arc to the given relative endpoint using the specified radii and rotation angle.  𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝑆𝐶𝐶𝑊𝐴𝑅𝐶(𝑟ℎ,𝑟𝑣,𝑟𝑜𝑡,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                            |
| 0x0C   | (rh,rv,rot,x,y)                      | SCWARC. Draw a small clockwise arc to the given endpoint using the specified radii and rotation angle.  𝑆𝐶𝑊𝐴𝑅𝐶(𝑟ℎ,𝑟𝑣,𝑟𝑜𝑡,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                               |
| 0x0D   | (rh,rv,rot,x,y)                      | SCWARC_REL. Draw a small clockwise arc to the given relative endpoint using the specified radii and rotation angle.  𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝑆𝐶𝑊𝐴𝑅𝐶(𝑟ℎ,𝑟𝑣,𝑟𝑜𝑡,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                               |
| 0x0E   | (rh,rv,rot,x,y)                      | LCCWARC. Draw a large counter-clockwise arc to the given endpoint using the specified radii and rotation angle.  𝐿𝐶𝐶𝑊𝐴𝑅𝐶(𝑟ℎ,𝑟𝑣,𝑟𝑜𝑡,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                                                            |
| 0x0F   | (rh,rv,rot,x,y)                      | LCCWARC_REL. Draw a large counter-clockwise arc to the given relative endpoint using the specified radii and rotation angle.  𝑥=𝑠𝑡𝑎𝑟𝑡𝑥+Δ𝑥 𝑦=𝑠𝑡𝑎𝑟𝑡𝑦+Δ𝑦 𝐿𝐶𝐶𝑊𝐴𝑅𝐶(𝑟ℎ,𝑟𝑣,𝑟𝑜𝑡,𝑥,𝑦) 𝑠𝑡𝑎𝑟𝑡𝑥=𝑥 𝑠𝑡𝑎𝑟𝑡𝑦=𝑦                                                                            |
| 0x10   | (rh,rv,rot,x,y)                      | LCWARC. Draw a large clockwise arc to the given endpoint using the specified radii and rotation angle. LCWARC(rh, rv, rot, x, y) startx = x starty = y|
| 0x11   | (rh, rv, rot, x, y)                  | LCWARC_REL. Draw a large clockwise arc to the given relative endpoint using the specified radii and rotation angle.  x = startx + Δx y = starty + Δy LCWARC(rh, rv, rot, x, y) startx = x starty = y                                                                 |

### 3.6 Vector-Based Drawing Operations

#### 3.6.1 Enumerations

##### 3.6.1.1 vg_lite_fill_t

This enumeration is used to specify the fill rule to use. For drawing any path, the hardware supports both non-zero and even-odd fill rules.

To determine whether any given point is inside an object, imagine drawing a line from that point to infinity in any direction, making sure the line does not intersect any vertices of the path. For every edge the line crosses, add 1 to a counter if the edge crosses from left to right, as seen by an observer walking along the line towards infinity; subtract 1 if the edge crosses from right to left. This way, each region of the plane will have an integer value.

The non-zero fill rule says that if the resulting sum is not zero, the point is inside the shape. The even-odd rule says that if the resulting sum is odd, the point is inside the shape, regardless of the sign.

| vg_lite_fill_t        | Description                                                              |
|-----------------------|--------------------------------------------------------------------------|
| VG_LITE_FILL_NON_ZERO | Non-zero fill rule. A pixel is drawn if it intersects at least one path pixel. |
| VG_LITE_FILL_EVEN_ODD | Even-odd fill rule. A pixel is drawn if it intersects an odd number of path pixels. |

##### 3.6.1.2 vg_lite_pattern_mode_t

Defines how areas outside the image pattern are filled onto the path.

| vg_lite_pattern_mode_t  | Description                                     |
|-------------------------|-------------------------------------------------|
| VG_LITE_PATTERN_COLOR   | Fill the outside of the pattern with color.     |
| VG_LITE_PATTERN_PAD     | Extend the color of the pattern border to fill the area outside the pattern. |

#### 3.6.2 Structures

##### 3.6.2.1 vg_lite_color_ramp_t

This structure defines stop points for radial gradients. Five parameters provide the offset and color for each stop point. Each stop point is defined by a set of floating-point values that specify the offset and sRGBA color and alpha values. The color channel values are in non-premultiplied (R, G, B, alpha) form. All parameters are in the range \[0,1\]. Red, green, blue, and alpha values \[0,1\] are mapped to 8-bit pixel values \[0,255\].

The maximum number of stops defining a radial gradient is MAX_COLOR_RAMP_STOPS, which is 256.

| Field  | Type             | Description                    |
|--------|------------------|--------------------------------|
| stop   | vg_lite_float_t  | Offset of the color stop       |
| red    | vg_lite_float_t  | Red offset of the color stop   |
| green  | vg_lite_float_t  | Green offset of the color stop |
| blue   | vg_lite_float_t  | Blue offset of the color stop  |
| alpha  | vg_lite_float_t  | Alpha channel offset of the color stop |

##### 3.6.2.2 vg_lite_linear_gradient_t

This structure defines the organization of linear gradients in VGLite data. Linear gradients are applied to fill paths. It will generate a 256x1 image based on the settings.

| Field                  | Type              | Description                           |
|-----------------------|-------------------|---------------------------------------|
| colors\[VLC_MAX_GRAD\]  | uint32_t          | Array of gradient colors              |
| count                 | uint32_t          | Number of colors                      |
| stops\[VLC_MAX_GRAD\]   | uint32_t          | Number of stops, from 0 to 255        |
| matrix                | vg_lite_matrix_t  | Matrix structure that transforms gradient color slopes |
| image                 | vg_lite_buffer_t  | Image object structure representing the color slopes |

The maximum for VLC_MAX_GRAD is 16, and the maximum for VLC_GRADBUFFER_WIDTH is 256.

#### 3.6.3 Functions

##### 3.6.3.1 vg_lite_draw

- Description

    Perform hardware-accelerated 2D vector drawing operations.

    The size of the tile buffer can be specified at initialization, and this size will be adjusted by the kernel to the minimum alignment required by the hardware. If you make the tile buffer smaller, less memory will be allocated, but a path may be sent to the hardware multiple times, as the hardware will walk the target with the provided tile window size, potentially reducing performance. A good practice is to set the tile buffer size to the most common path size. For example, if you are only rendering fonts up to 24pt, you can set the tile buffer to 24x24.

- Parameters

    vg_lite_buffer_t \*target: Pointer to the vg_lite_buffer_t structure of the target buffer. All color formats in the vg_lite_buffer_format_t enumeration are valid target formats for the drawing function.

    vg_lite_path_t \*path: Pointer to the vg_lite_path_t structure containing the path data to draw. For details on opcodes, refer to the section on [Vector Path OpCodes](#354-Vector Path OpCodes) in this document.

    vg_lite_fill_t fill_rule: Enumeration value of vg_lite_fill_t specifying the fill rule for the path.

    vg_lite_matrix_t \*matrix: Pointer to the vg_lite_matrix_t structure defining the affine transformation matrix for the path. If the matrix is NULL, it is assumed to be an identity matrix. Note: vg_lite_draw does not support non-affine transformations, so perspective transformation matrices have no effect on the path.

    vg_lite_blend_t blend: Select a blend mode supported by the hardware from the vg_lite_blend_t enumeration, applied to each drawn pixel. If blending is not needed, set this value to VG_LITE_BLEND_NONE, which is 0.

    vg_lite_color_t color: Color applied to each pixel of the path drawing.

##### 3.6.3.2 vg_lite_draw_gradient

- Description

    This function is used to fill a path with gradient colors according to the specified fill rule. The specified path will be transformed according to the selected matrix and filled with the gradient.

- Parameters

    vg_lite_buffer_t \*target: Refer to vg_lite_draw.

    vg_lite_path_t \*path: Refer to vg_lite_draw.

    vg_lite_fill_t fill_rule: Refer to vg_lite_draw.

    vg_lite_matrix_t \*matrix: Refer to vg_lite_draw.

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure containing the values used to fill the path.

    vg_lite_blend_t blend: Refer to vg_lite_draw.

##### 3.6.3.3 vg_lite_draw_pattern

- Description

    This function fills a path with an image pattern. The path will be transformed according to the specified matrix and filled with the transformed image pattern.

- Parameters

    vg_lite_buffer_t \*target: Refer to vg_lite_draw.

    vg_lite_path_t \*path: Refer to vg_lite_draw.

    vg_lite_fill_t fill_rule: Refer to vg_lite_draw.

    vg_lite_matrix_t \*matrix0: Pointer to the vg_lite_matrix_t structure that defines the 3x3 transformation matrix for the path. If the matrix is NULL, it is assumed to be an identity matrix.

    vg_lite_buffer_t \*source: Pointer to the vg_lite_buffer_t structure describing the source of the image pattern.

    vg_lite_matrix_t \*matrix1: Pointer to the vg_lite_matrix_t structure that defines the 3x3 transformation from source pixels to target pixels. If the matrix is NULL, it is assumed to be an identity matrix, meaning source pixels will be copied directly to position 0,0 of the target pixels.

    vg_lite_blend_t blend: Refer to vg_lite_draw.

    vg_lite_pattern_mode_t pattern_mode: Specify a vg_lite_pattern_mode_t value that defines how the area outside the image pattern is filled.

    vg_lite_color_t pattern_color: Specify a 32bpp ARGB color (vg_lite_color_t) applied to the area outside the image pattern when the pattern_mode value is VG_LITE_PATTERN_COLOR.

    vg_lite_filter_t filter: Specify the type of filter. All formats in the vg_lite_filter_t enumeration are valid formats for this function. A value of zero (0) indicates VG_LITE_FILTER_POINT.

#### 3.6.4 Linear Gradient Initialization and Control Functions

##### 3.6.4.1 vg_lite_init_grad

- Description

    This function initializes the internal buffer of the linear gradient object with default settings for rendering.

- Parameters

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure that defines the gradient to be initialized. Use default values.

##### 3.6.4.2 vg_lite_set_grad

- Description

    This function sets the values of the vg_lite_linear_gradient_t structure members.

    Note: In cases where the input parameters are incomplete or invalid, the following rules are used to set default gradient colors.

  1. If no valid stop points are specified (e.g., due to an empty input array, out-of-range, or out-of-order stop points), a 0 stop point with (R, G, B, α) color (0.0, 0.0, 0.0, 1.0) (opaque black) and a 1 stop point with color (1.0, 1.0, 1.0) (opaque white) are implicitly defined.
  1. If at least one valid stop point is specified but no stop point with offset 0 is defined, an implicit stop point with offset 0 and the same color as the first user-defined stop point is added.
  1. If at least one valid stop point is specified but no stop point with offset 1 is defined, an implicit stop point with offset 1 and the same color as the last user-defined stop point is added.

- Parameters

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure to be set.

    uint32_t count: Number of colors in the linear gradient. The maximum number of color stops is defined by VLC_MAX_GRAD, which is 16.

    uint32_t \*colors: Array of colors specifying the gradient, in ARGB8888 format, with Alpha in the highest bit.

    uint32_t \*stops: Pointer to the array of gradient stop offsets.

##### 3.6.4.3 vg_lite_update_grad

- Description

    This function updates or generates the values of the image object to be rendered. The vg_lite_linear_gradient_t object has an image buffer used to render the gradient pattern. This image buffer will be created or updated according to the corresponding gradient parameters.

- Parameters

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure containing the values to be updated for the rendering object.

##### 3.6.4.4 vg_lite_get_grad_matrix

- Description

    This function retrieves the pointer to the transformation matrix of the gradient object, allowing the application to manipulate the matrix to facilitate the correct rendering of gradient-filled paths.

- Parameters

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure containing the matrix to be retrieved.

##### 3.6.4.5 vg_lite_clear_grad

- Description

    This function clears the values of the linear gradient object and frees the memory of the image buffer.

- Parameters

    vg_lite_linear_gradient_t \*grad: Pointer to the vg_lite_linear_gradient_t structure to be cleared.

## 4. Constraints

The GPU driver **supports only one current context and one thread issuing commands to the GPU**. The GPU driver **does not support** multiple concurrent contexts running in multiple threads/processes, as the GPU kernel driver does not support context switching. A GPU application can only use one context to issue commands to the GPU hardware at any time. If a GPU application needs to switch contexts, it should call [vg_lite_close](#3213-vg_lite_close) to close the current context in the current thread, and then call [vg_lite_init](#3212-vg_lite_init) to initialize a new context in the current thread or another thread/process.

## 5. Performance Tips and Best Practices

### 5.1 Cache vs Non-cache

When loading the vg_lite.ko module, you can configure whether to disable the cache through the cached parameter (cache is enabled by default). In cache mode, the driver will refresh the CPU cache (D-cache and L2-cache) before submitting commands to the GPU hardware. In non-cache mode, the command buffer and video memory will be mapped to the user space address as non-cache. Generally, cache mode provides better performance, as the CPU can write to the command buffer and read from video memory faster.

Currently, cache refreshing uses the dcache.cipa instruction, which can only refresh one cache line (64 bytes) at a time. For larger buffers, such as 1920x1080@ARGB32, it requires approximately 129,600 iterations, most of which are misses, resulting in some performance overhead. Using the dcache.ciall instruction can refresh all caches, but it might affect other processes, so it is not used.

### 5.2 Memory Usage

After loading the vg_lite.ko module, it occupies about 130KB of memory. Besides the command buffer and video memory, it hardly occupies any more space. Each memory allocation by vg_lite_hal_allocate_contiguous requires corresponding page table resources and a 64B node in addition to the memory itself.

### 5.3 Drawing Process

Using VGLite API for operations:

1. Call [vg_lite_init](#3212-vg_lite_init) to initialize the GPU.
1. If GPU video memory is needed, call [vg_lite_allocate](#3251-vg_lite_allocate) to allocate and map it.
1. Use the API to draw.
1. Call [vg_lite_finish](#3214-vg_lite_finish) or [vg_lite_flush](#3215-vg_lite_flush) to submit commands for rendering and wait for the drawing to complete.
1. Before the process ends, call [vg_lite_close](#3213-vg_lite_close) to close the GPU.

## 6. Examples

The K230 SDK contains multiple GPU examples. The source code is located in `src/little/buildroot-ext/package/vg_lite/test/samples`. To build and add them to the generated system image, enable BR2_PACKAGE_VG_LITE_DEMOS in buildroot (enabled by default).

### 6.1 tiger

This is an example that draws an image of a tiger. After running, it generates `tiger.png` in the current directory.

![tiger.png](../../../../zh/01_software/board/mpp/images/tiger.png)

### 6.2 linearGrad

This is an example of a linear gradient image. After running, it generates `linearGrad.png` in the current directory.

![linearGrad.png](../../../../zh/01_software/board/mpp/images/linearGrad.png)

### 6.3 imgIndex

This is an example using a color lookup table. After running, it generates `imgIndex1.png`, `imgIndex2.png`, `imgIndex4.png`, and `imgIndex8.png` in the current directory, each using a different number of color indices.

![imgIndex1.png](../../../../zh/01_software/board/mpp/images/imgIndex1.png)

![imgIndex2.png](../../../../zh/01_software/board/mpp/images/imgIndex2.png)

![imgIndex4.png](../../../../zh/01_software/board/mpp/images/imgIndex4.png)

![imgIndex8.png](../../../../zh/01_software/board/mpp/images/imgIndex8.png)

### 6.4 vglite_drm

This is an example of GPU + DRM display linkage.

Note: Since the video output driver under Linux does **not include** initialization functionality, you need to ensure the screen is already in use before running, for example, by running `sample_vo.elf 3` on the main core.

### 6.5 vglite_cube

This is another example of GPU + DRM display linkage, drawing a continuously rotating cube on the screen.

Note: Since the video output driver under Linux does **not include** initialization functionality, you need to ensure the screen is already in use before running, for example, by running `sample_vo.elf 3` on the main core.
