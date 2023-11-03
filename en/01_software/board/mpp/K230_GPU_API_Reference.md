# K230 GPU API reference

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

This document describes the usage guide for the K230 chip 2.5D GPU module.

### Reader

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| Abbreviation | Full name                  |
|------|-----------------------|
| GPU  | Graphics Process Unit |
| BLIT | Bit Block Transfer    |
| CLUT | Color Look Up Table   |

### Revision history

| Version version number | Modify the description | Author | date       |
|------------|----------|--------|------------|
| V1.0       | Initial | Huang Ziyi | 2023/04/06 |
| V1.1       | Adjust the formatting | Huang Ziyi | 2023/05/06 |

## 1. Function introduction

This module is mainly used to accelerate the drawing of vector graphics, which can be used to draw menus and other pages, etc., and supports accelerating some LVGL drawing. The GPU has a series of drawing instructions, write the drawing instructions to memory, submit the address and the total length of the instructions to the GPU, and start drawing. This module supports polygon, quadratic Bezier, cubic Bezier and ellipse fill drawing, linear gradient fill, color lookup table, image compositing and blending, and BLIT.

## 2. Data flow

The GPU software driver section includes the device /dev/vg_lite and its kernel module driver vg_lite.ko, as well as the user-mode library libvg_lite.so, libvg_lite.so opens /dev/vg_lite the device and interacts with the kernel-state driver through ioctl() and mmap(). The kernel-state drive is mainly implemented by vg_lite_hal.c, vg_lite functions in .c perform actual register operations by calling functions in vg_lite_hal.c through vg_lite_kernel functions.

Note: The driver does not check the physical address in the drawing instruction, and calling the VGLite API can indirectly read and write all physical addresses of DDR memory.

## 3. Software Interface

The software interface is detailed in the header file vg_lite.h in the package.

### 3.1 Main Types and Definitions

#### 3.1.1 Parameter types

| name             | Type definition               | meaning                                                                                                                                                                                                                        |
|------------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Int32_t          | Int                    | 32-bit signed integer                                                                                                                                                                                                              |
| uint32_t         | Unsigned int           | 32-bit unsigned integer                                                                                                                                                                                                              |
| VG_LITE_S8       | enum vg_lite_format_t  | 8-bit signed integer coordinates                                                                                                                                                                                                           |
| VG_LITE_S16      | enum vg_lite_format_t  | 16-bit signed integer coordinates                                                                                                                                                                                                          |
| VG_LITE_S32      | enum vg_lite_format_t  | 32-bit signed integer coordinates                                                                                                                                                                                                          |
| vg_lite_float_t  | float                  | Single-precision floating-point number                                                                                                                                                                                                                |
| vg_lite_color_t  | uint32_t               | 32-bit color values Color values specify the colors used in various functions. The color is formed with an 8-bit RGBA channel. The red channel is in the bottom 8 bits of the color value, followed by the green and blue channels. The alpha channel is in the top 8 bits of the color value. For the L8 target format, RGB colors are converted to L8 by using the default ITU-R BT.709 conversion rules. |

#### 3.1.2 Error Type vg_lite_error_t

| enumerate                       | description                 |
|----------------------------|----------------------|
| VG_LITE_GENERIC_IO         | Unable to communicate with kernel driver   |
| VG_LITE_INVALID_ARGUMENT   | Illegal parameters             |
| VG_LITE_MULTI_THREAD_FAIL  | Multithreaded error           |
| VG_LITE_NO_CONTEXT         | No context error         |
| VG_LITE_NOT_SUPPORT        | Feature not supported           |
| VG_LITE_OUT_OF_MEMORY      | No allotable drive heap memory |
| VG_LITE_OUT_OF_RESOURCES   | No system heap memory to allocate |
| VG_LITE_SUCCESS            | succeed                 |
| VG_LITE_TIMEOUT            | Timeout                 |
| VG_LITE_ALREADY_EXISTS     | Object already exists           |
| VG_LITE_NOT_ALIGNED        | Data alignment error         |

#### 3.1.3 Feature Enumeration

| enumerate                              | description          |
|-----------------------------------|---------------|
| gcFEATURE_BIT_VG_BORDER_CULLING   | Border clipping      |
| gcFEATURE_BIT_VG_GLOBAL_ALPHA     | Global Alpha     |
| gcFEATURE_BIT_VG_IM_FASTCLEAR     | Fast purge      |
| gcFEATURE_BIT_VG_IM_INDEX_FORMAT  | Color index      |
| gcFEATURE_BIT_VG_PE_PREMULTIPLY   | Alpha channel premultiplication |
| gcFEATURE_BIT_VG_RADIAL_GRADIENT  | Radial grayscale      |
| gcFEATURE_BIT_VG_RGBA2_FORMAT     | RGBA2222 format  |

### 3.2 GPU control

If not specifically stated, then before calling any API function, the application must [initialize](#3212-vg_lite_init) the GPU implicit (global) context by calling the vg_lite_init, which will populate the feature table, reset the fast purge buffer, reset the synthetic target buffer, and allocate command and subdivision buffers.

The GPU driver **only supports one current context and one thread to issue commands to the GPU**. GPU drivers do not support multiple concurrent contexts running simultaneously in multiple threads/processes because GPU kernel drivers do not support context switching. A GPU application can only use one context to issue commands to the GPU hardware at any one time. If a GPU application needs to switch contexts, it should call[vg_lite_close to close the current context in the current thread](#3213-vg_lite_close), and then the vg_lite_init can be called[vg_lite_init](#3212-vg_lite_init)to initialize a new context in the current thread or in another thread/process.

If there is no special description, all functions return[vg_lite_error_t](#312-error-type-vg_lite_error_t).

#### 3.2.1 Context initialization and control functions

##### 3.2.1.1 vg_lite_set_command_buffer_size

- description

    This function is optional. If you need to modify the size of the command buffer, you must call it before vg_lite_init. The command buffer size defaults to 64KB, which does not mean that a frame of commands must be less than 64KB, when the buffer is full, the render will be submitted directly to empty the buffer, and a larger buffer means a lower frequency of render commits, which can reduce the overhead of system calls.

- parameter

| Parameter name | description           | Input/output |
|----------|----------------|-----------|
| size     | Command buffer length | input      |

##### 3.2.1.2 vg_lite_init

- description

    This function initializes the memory and data structures required for the GPU plot/fill function, allocating memory for command buffers and patch buffers of the specified size. The width and height of the insert buffer must be multiples of 16. Sliced windows can be specified based on the amount of memory available in the system and the required performance. A smaller window can have a smaller memory footprint, but may result in lower performance. The smallest window available for tessellation is 16x16. If the height or width is less than 0, no insert buffer is created and can be used in cases where there is only padding.

    If this will be the first context to access the hardware, the hardware will be opened and initialized. If you need to initialize a new context, you must call vg_lite_close to close the current context. Otherwise, the vg_lite_init returns an error.

- parameter

| Parameter name            | description                                                                                                               | Input/output |
|---------------------|--------------------------------------------------------------------------------------------------------------------|-----------|
| tessellation_width  | Slice window width. Must be an integer multiple of 16, the minimum is 16, the maximum cannot be greater than the frame width, if 0 means that tessellation is not used, then the GPU will only run blit. | input      |
| tessellation_height | Insert window height. Must be an integer multiple of 16, the minimum is 16, the maximum cannot be greater than the frame width, if 0 means that tessellation is not used, then the GPU will only run blit. | input      |

##### 3.2.1.3 vg_lite_close

- description

    Deletes all resources and frees all memory previously initialized by vg_lite_init functions. If this is the only active context, it also automatically shuts down the hardware.

##### 3.2.1.4 vg_lite_finish

- description

    This function explicitly submits the command buffer to the GPU and waits for it to complete.

##### 3.2.1.5 vg_lite_flush

- description

    This function explicitly commits the command buffer to the GPU without waiting for it to complete.

#### 3.2.2 Pixel buffers

##### 3.2.2.1 Memory alignment requirements

###### 3.2.2.1.1 Source image alignment requirements

GPU hardware requires rasterized images to be a multiple of 16 pixels. This requirement applies to all image formats. Therefore, users need to pad arbitrary image widths into multiples of 16 pixels for the GPU hardware to work correctly.

The byte alignment requirements for pixels depend on the specific pixel format.

| Image format                    | Bits per pixel | Alignment requirements | Supported as a source image | Supported as a target image |
|-----------------------------|--------------|----------|----------------|------------------|
| VG_LITE_INDEX1              | 1            | 8B       | be             | not               |
| VG_LITE_INDEX2              | 2            | 8B       | be             | not               |
| VG_LITE_INDEX4              | 4            | 8B       | be             | not               |
| VG_LITE_INDEX8              | 8            | 16B      | be             | not               |
| VG_LITE_A4                  | 4            | 8B       | be             | not               |
| VG_LITE_A8                  | 8            | 16B      | be             | be               |
| VG_LITE_L8                  | 8            | 16B      | be             | be               |
| VG_LITE_ARGB2222 group          | 8            | 16B      | be             | be               |
| VG_LITE_RGB565 group            | 16           | 32B      | be             | be               |
| VG_LITE_ARGB1555 group          | 16           | 32B      | be             | be               |
| VG_LITE_ARGB4444 group          | 16           | 32B      | be             | be               |
| VG_LITE_ARGB8888/XRGB8888 group | 32           | 64B      | be             | be               |

###### 3.2.2.1.2 Render target buffer alignment requirements

GPU hardware requires pixel buffers to be in multiples of 16 pixels. This requirement applies to all image formats. Therefore, the user needs to align arbitrary pixel buffer widths to multiples of 16 pixels for the GPU hardware to work correctly. The byte alignment requirements for pixels depend on the specific pixel format.

See Table 2: Image Source Alignment Summary later in this document.

The start address alignment requirements for pixel buffers depend on whether the buffer layout format is tiled or linear (vg_lite_buffer_layout_t enum).

\- If the format is tiled (4x4 tile), the start address and stride need to be 64 bytes aligned.

- If the format is linear, there is no alignment requirement for the start address and stride.

##### 3.2.2.2 Pixel caching

The GPU includes two fully associative caches. Each cache has 8 rows and 64 bytes each. In this case, a cache line can hold a 4x4 pixel tile or a 16x1 pixel row.

#### 3.2.3 Enumeration Types

##### 3.2.3.1 vg_lite_buffer_format_t

- This enumeration type specifies the color format to use for the buffer.

   Note: For a summary of the alignment requirements of image formats, see [Memory alignment requirements](#3221-memory-alignment-requirements) after numeric descriptions.

| vg_lite_buffer_format_t | description                          | Supported as a source | Support as a target | Alignment (bytes) |
|-------------------------|-------------------------------|------------|--------------|--------------|
| VG_LITE_ABGR8888        | 8bits per channel, alpha in lower 8bits | be         | be           | 64           |
| VG_LITE_ARGB8888        |                               | be         | be           | 64           |
| VG_LITE_BGRA8888        |                               | be         | be           | 64           |
| VG_LITE_RGBA8888        |                               | be         | be           | 64           |
| VG_LITE_BGRX8888        |                               | be         | be           | 64           |
| VG_LITE_RGBX8888        |                               | be         | be           | 64           |
| VG_LITE_XBGR8888        |                               | be         | be           | 64           |
| VG_LITE_XRGB8888        |                               | be         | be           | 64           |
| VG_LITE_ABGR1555        |                               | be         | be           | 32           |
| VG_LITE_ARGB1555        |                               | be         | be           | 32           |
| VG_LITE_BGRA5551        |                               | be         | be           | 32           |
| VG_LITE_RGBA5551        |                               | be         | be           | 32           |
| VG_LITE_BGR565          |                               | be         | be           | 32           |
| VG_LITE_RGB565          |                               | be         | be           | 32           |
| VG_LITE_ABGR4444        |                               | be         | be           | 32           |
| VG_LITE_ARGB4444        |                               | be         | be           | 32           |
| VG_LITE_BGRA4444        |                               | be         | be           | 32           |
| VG_LITE_RGBA4444        |                               | be         | be           | 32           |
| VG_LITE_A4              | 4bits alpha, 无RGB            | be         | not           | 8            |
| VG_LITE_A8              | 8bits alpha, 无RGB            | be         | be           | 16           |
| VG_LITE_ABGR2222        |                               | be         | be           | 16           |
| VG_LITE_ARGB2222        |                               | be         | be           | 16           |
| VG_LITE_BGRA2222        |                               | be         | be           | 16           |
| VG_LITE_RGBA2222        |                               | be         | be           | 16           |
| VG_LITE_INDEX_1         | 1-bit index format                | be         | not           | 8            |
| VG_LITE_INDEX_2         | 2-bit index format                 | be         | not           | 8            |
| VG_LITE_INDEX_4         | 4-bit index format                 | be         | not           | 8            |
| VG_LITE_INDEX_8         | 8-bit index format                 | be         | not           | 8            |

##### 3.2.3.2 vg_lite_buffer_image_mode_t

- Specifies how the image is rendered to the buffer.

| enumerate                        | description                 |
|-----------------------------|----------------------|
| VG_LITE_NORMAL_IMAGE_MODE   | An image drawn in blend mode |
| VG_LITE_NONE_IMAGE_MODE     | Image input is ignored       |
| VG_LITE_MULTIPLY_IMAGE_MODE | The image is multiplied by the drawing color   |

##### 3.2.3.3 vg_lite_buffer_layout_t

- Specifies the layout of buffer data in memory.

| enumerate           | description                                                                                    |
|----------------|-----------------------------------------------------------------------------------------|
| VG_LITE_LINEAR | Linear (scanline) layout. Note: This layout has no alignment requirements for buffers.                                |
| VG_LITE_TILED  | The data is organized into 4x4 pixel inserts. Note: For this layout, the start address and span of the buffer need to be 64 bytes aligned. |

##### 3.2.3.4 vg_lite_buffer_transparency_mode_t

- Specifies the transparency mode of a buffer.

| enumerate                      | description                                                                                                                                           |
|---------------------------|------------------------------------------------------------------------------------------------------------------------------------------------|
| VG_LITE_IMAGE_OPAQUE      | Opaque images: All image pixels are copied to VG PE for rasterization.                                                                                        |
| VG_LITE_IMAGE_TRANSPARENT | Transparent images: Only non-transparent image pixels are copied into VG PE. Note: This mode only works if the image mode is VG_LITE_NORMAL_IMAGE_MODE or VG_LITE_MULTIPLY_IMAGE_MODE. |

#### 3.2.4 Structures

##### 3.2.4.1 vg_lite_buffer_t

- This structure defines the buffer layout of the image or memory data used by the GPU.

| field               | type                               | description           |
|--------------------|------------------------------------|----------------|
| width              | int32_t                            | Buffer pixel width |
| height             | int32_t                            | Buffer pixel height |
| stride             | int32_t                            | The number of bytes in a row   |
| tiled              | vg_lite_buffer_layout_t            | Linear or tiled     |
| format             | vg_lite_buffer_format_t            | Color type       |
| handle             | void \*                            | Memory handle       |
| memory             | void \*                            | The mapped virtual address |
| address            | uint32_t                           | Physical address       |
| .yuv                | N/A                                | N/A            |
| image_mode         | vg_lite_buffer_image_mode_t        | BLIT mode       |
| transparency_mode  | vg_lite_buffer_transparency_mode_t | Transparent mode       |

#### 3.2.5 Functions

##### 3.2.5.1 vg_lite_allocate

- description

    This function is used to allocate memory before using the buffer in the blit or draw function.

   In order for the hardware to access some memory, such as the source image or destination buffer, it needs to be allocated first. The provided[vg_lite_buffer_t](#3241-vg_lite_buffer_t)structure needs to be initialized with the size (width and height) and format of the requested buffer. If stride is set to 0, this function will fill it in. The only input parameter to this function is a pointer to the buffer structure. If the structure has all the required information, appropriate memory is allocated for the buffer.

   This function will call the kernel to actually allocate memory. [Memory](#3241-vg_lite_buffer_t)handles, logical addresses, and hardware addresses in vg_lite_buffer_t structures are populated by the kernel.

- parameter

    [vg_lite_buffer_t](#3241-vg_lite_buffer_t) \*buffer: A pointer to the buffer that holds the size and format of the allocated buffer.

##### 3.2.5.2 vg_lite_free

- description

    This function is used to cancel a previously allocated buffer and free the memory of the buffer.

- parameter

    [vg_lite_buffer_t](#3241-vg_lite_buffer_t) \*buffer: A pointer to the structure of the buffer being filled by the vg_lite_allocate.

##### 3.2.5.3 vg_lite_buffer_upload

- description

    This function uploads pixel data to GPU memory. Note that the format of the data (pixels) to be uploaded must be the same as described in the buffer object. The input data memory buffer should contain enough data to upload to the GPU buffer pointed to by the input parameter "buffer".

- parameter

    vg_lite_buffer_t \*buffer: A pointer to the structure of the buffer being filled by the vg_lite_allocate.

    uint8_t \*data\[3\]: A pointer to pixel data.

    uint32_t stride\[3\]: The row span of pixel data.

##### 3.2.5.4 vg_lite_map

- description

    This function is used to map memory appropriately for a particular buffer. It will be used to properly translate the physical address of the buffer required by the GPU.

   If you want to use a frame buffer directly as the destination buffer, you need to wrap it with a[vg_lite_buffer_t](#3241-vg_lite_buffer_t)structure and call the kernel to map the provided logical or physical address into hardware-accessible memory. For example, if you know the logical address of the frame buffer, set[the memory field of the vg_lite_buffer_t structure with this address](#3241-vg_lite_buffer_t)and call this function. If you know the physical address, set the memory field to NULL, and then program the address field with the physical address.

- parameter

   vg_lite_buffer_t \*buffer: A pointer to the structure of the buffer being filled [by the vg_lite_allocate](#3251-vg_lite_allocate).

##### 3.2.5.5 vg_lite_unmap

- description

    This function unmaps the buffer and frees any memory resources allocated by the previous call vg_lite_map.

- parameter

   vg_lite_buffer_t \*buffer: A pointer to the structure of the buffer being filled [by the vg_lite_map](#3254-vg_lite_map).

##### 3.2.5.6 vg_lite_set_CLUT

- description

    This function sets the color lookup table (CLUT) for indexed color images in context. Once CLUT is set (not empty), the image pixel color used for index format image rendering will be obtained from the color lookup table (CLUT) based on the color index value of the pixel.

- parameter

    uint32_t count: The count of colors in the color lookup table.

    For INDEX_1, there can be up to 2 colors in the table.

    For INDEX_2, there can be up to 4 colors in the table.

    For INDEX_4, there can be up to 16 colors in the table.

    For INDEX_8, there can be up to 256 colors in the table.

    uint32_t \*colors: The color lookup table (CLUT) pointed to by the pointer will be stored in context and programmed into the command buffer if needed. CLUT does not take effect until the command buffer is committed to hardware. The color is in ARGB format, with A in the highest position.

    Note: The driver does not validate CLUT content from the application.

### 3.3 Matrix

#### 3.3.1 Structs

##### 3.3.1.1 vg_lite_matrix_t

- description

    A 3x3 floating-point number matrix is defined.

#### 3.3.2 Functions

##### 3.3.2.1 vg_lite_identity

- description

    Set the matrix as the identity matrix.

- parameter

   vg_lite_matrix_t \*matrix: A pointer to the [vg_lite_matrix_t](#3311-vg_lite_matrix_t)structure that will be loaded into the identity matrix.

##### 3.3.2.2 vg_lite_perspective

- description

    Perform a perspective transformation on the matrix.

- parameter

    vg_lite_float_t px: Perspective transformation matrix.

    vg_lite_float_t py: of the perspective transformation matrix

   vg_lite_matrix_t \*matrix: A pointer to the vg_lite_matrix_t structure that will be transformed by perspective[](#3311-vg_lite_matrix_t).

##### 3.3.2.3 vg_lite_rotate

- description

    Performs a rotational transformation of the matrix at a specified angle.

- parameter

    vg_lite_float_t degrees: The number of degrees of rotation of the matrix (in the system of angles), with positive numbers representing clockwise rotation.

   vg_lite_matrix_t \*matrix: A pointer to the vg_lite_matrix_t structure that will be rotated[](#3311-vg_lite_matrix_t).

##### 3.3.2.4 vg_lite_scale

- description

    Scale the matrix vertically and horizontally.

- parameter

    vg_lite_float_t scale_x: Horizontal scaling factor.

    vg_lite_float_t scale_y: Vertical scaling factor.

   vg_lite_matrix_t \*matrix: A pointer to the vg_lite_matrix_t structure that will be scaled[](#3311-vg_lite_matrix_t).

##### 3.3.2.5 vg_lite_translate

- description

    Transform the matrix by translation.

- parameter

    vg_lite_float_t x: Horizontal translation.

    vg_lite_float_t y: Vertical translation.

   vg_lite_matrix_t \*matrix: A pointer to the vg_lite_matrix_t structure that will be translated[](#3311-vg_lite_matrix_t).

### 3.4 BLITs for synthesis and mixing

#### 3.4.1 Enumeration Types

##### 3.4.1.1 vg_lite_blend_t

This enumeration defines some of the mixed modes supported by VGLite API functions. S and D represent the source and destination color channels, and Sa and Da represent the source and destination alpha channels.

Colors are displayed with 100% and 50% opacity.

| vg_lite_blend_t        | description                     |
|------------------------|--------------------------|
| VG_LITE_BLEND_ADDITIVE | S+D                      |
| VG_LITE_BLEND_DST_IN   | Sa\*D                    |
| VG_LITE_BLEND_DST_OVER | (1-Da)\*S+D              |
| VG_LITE_BLEND_MULTIPLY | S\*(1-Da)+D\*(1-Sa)+S\*D |
| VG_LITE_BLEND_NONE     | S                        |
| VG_LITE_BLEND_SCREEN   | S+D-S\*D                 |
| VG_LITE_BLEND_SRC_IN   | Da\*S                    |
| VG_LITE_BLEND_SRC_OVER | S+(1-Sa)\*D              |
| VG_LITE_BLEND_SUBTRACT | D\*(1-Sa)                |

##### 3.4.1.2 vg_lite_filter_t

Specify the sample filtering mode in blit and draw APIs.

| vg_lite_filter_t          | description                                          |
|---------------------------|-----------------------------------------------|
| VG_LITE_FILTER_POINT      | Only the most recent image pixels are taken.                          |
| VG_LITE_FILTER_LINEAR     | Use linear interpolation along horizontal lines.                      |
| VG_LITE_FILTER_BI_LINEAR  | Use a 2x2 box around the image pixels and interpolate. |

##### 3.4.1.3 vg_lite_global_alpha_t

Specifies the global alpha mode in blit APIs.

| vg_lite_global_alpha_t  | description                                                   |
|-------------------------|--------------------------------------------------------|
| VG_LITE_NORMAL          | Use the original src/dst alpha value.                            |
| VG_LITE_GLOBAL          | Replace the original src/dst alpha value with the global src/dst alpha value. |
| VG_LITE_SCALED          | Multiply the global src/dst alpha value with the original src/dst alpha value.       |

#### 3.4.2 Structures

##### 3.4.2.1 vg_lite_rectangle_t

The structure defines the organization of a rectangle of data.

| field    | type     | description                |
|---------|----------|---------------------|
| x       | int32_t  | x coordinate, with the upper left corner as the origin |
| and       | int32_t  | Y coordinates, upper left corner is the origin |
| width   | int32_t  | width                |
| height  | int32_t  | height                |

##### 3.4.2.2 vg_lite_point_t

This structure defines a 2D point.

| field | type     | description  |
|------|----------|-------|
| x    | int32_t  | X coordinate |
| and    | int32_t  | Y coordinates |

##### 3.4.2.3 vg_lite_point4_t

This structure defines four two-dimensional points that make up the polygon. These points are defined by structural vg_lite_point_t.

| field              | type          | description        |
|-------------------|---------------|-------------|
| vg_lite_point\[4\]  | int32_t each  | Array of 4 points |

#### 3.4.3 Functions

##### 3.4.3.1 vg_lite_blit

- description

    BLIT functions. BLIT operations are performed through a source buffer and a destination buffer. The source and destination buffer structures are defined with vg_lite_buffer_t structures. BLIT copies the source image to the destination buffer with a specified matrix, which can include translation, rotation, scaling, and perspective correction. Note that overlay sampling antialiasing is not supported vg_lite_buffer_t, so the edges of the destination buffer may not be smooth, especially the rotation matrix. Path rendering can be used to achieve high-quality overlay sample anti-aliasing (16X, 4X) rendering.

- parameter

   vg_lite_buffer_t \*target: Points to the vg_lite_buffer_t struct that defines the destination buffer. For more information about the valid target color formats for the BLIT function, see [Source Image Alignment Requirements](#32211-source-image-alignment-requirements).

   vg_lite_buffer_t \*source: A vg_lite_buffer_t struct that points to the source buffer. [All color formats in vg_lite_buffer_format_t](#3231-vg_lite_buffer_format_t)enumeration are valid source formats for the blit function.

    vg_lite_matrix_t \*matrix: Points to a vg_lite_matrix_t structure that defines a 3x3 transformation matrix from source pixels to destination pixels. If the matrix is NULL, an identity matrix is assumed, which means that the source pixel will be copied directly to the (0,0) position of the destination pixel.

    vg_lite_blend_t blend: Specifies one of the hardware-supported blending modes to apply to each image pixel. If blending is not required, set this value to VG_LITE_BLEND_NONE. Note: If the "matrix" parameter is specified as rotation or perspective, and the "blend" parameter is specified as VG_LITE_BLEND_NONE, VG_LITE_BLEND_SRC_IN, or VG_LITE_BLEND_DST_IN, the driver overrides the application's settings for BLIT operations and the transparency mode is always set to TRANSPARENT. This is due to some limitations of GPU hardware.

    vg_lite_color_t color: If not zero, this color value is used as the blend color. Before blending occurs, blending colors are multiplied by each source pixel. If you don't need to blend colors, set the color parameter to 0.

    vg_lite_filter_t filter: Specifies the type of filtering mode. All formats in the vg_lite_filter_t enumeration are valid formats for this function.

##### 3.4.3.2 vg_lite_blit_rect

- description

    BLIT rectangle function.

- parameter

    vg_lite_buffer_t \*target: 参考vg_lite_blit。

    vg_lite_buffer_t \*source: 参考vg_lite_blit。

    uint32_t \*rect: Specifies the rectangular area to BLIT.

    vg_lite_matrix_t \*matrix: Reference vg_lite_blit.

    vg_lite_blend_t \*blend: Reference vg_lite_blit.

    vg_lite_color_t color: Reference vg_lite_blit.

    vg_lite_filter_t filter: 参考vg_lite_blit。

##### 3.4.3.3 vg_lite_get_transform_matrix

- description

    This function obtains a 3x3 homogeneous transformation matrix from the source and target coordinates.

- parameter

    vg_lite_point4_t src: A pointer to a set of four two-dimensional points that make up the source polygon.

    vg_lite_point4_t dst: A pointer to a set of four two-dimensional points that make up the target polygon.

    vg_lite_matrix_t \*mat: Output parameter pointing to a 3x3 homogeneous matrix that converts the source polygon to the target polygon.

##### 3.4.3.4 vg_lite_clear

- description

    This function performs a clear operation, clearing/filling the specified pixel buffer (the entire buffer or part of the rectangle in the buffer) with an explicit color.

- parameter

    vg_lite_buffer_t \*target: 参考vg_lite_blit。

    vg_lite_rectangle_t \*rectangle: A pointer to the vg_lite_rectangle_t structure that specifies the area to fill. If the rectangle is NULL, the entire destination buffer is filled with the specified color.

    vg_lite_color_t color: The color of the fill, as specified in the vg_lite_color_t enumeration, which is the color value used to fill the buffer. If the buffer is in L8 format, the RGBA color will be converted to a luminance value.

#### 3.4.4 Global Alpha Function

##### 3.4.4.1 vg_lite_set_image_global_alpha

- description

    This function will set the image/source global alpha and return a status error code.

- parameter

    vg_lite_global_alpha_t alpha_mode: 全局Alpha模式,参见[vg_lite_global_alpha_t](#3413-vg_lite_global_alpha_t).

    uint32_t alpha_value: The Image/Source global alpha value to set.

##### 3.4.4.2 vg_lite_set_dest_global_alpha

- description

    This function will set the target global alpha and return a status error code.

- parameter

    vg_lite_global_alpha_t alpha_mode: 全局Alpha模式,参见[vg_lite_global_alpha_t](#3413-vg_lite_global_alpha_t).

    uint32_t alpha_value: The target global alpha value to set.

### 3.5 Vector Path Control

#### 3.5.1 Enumeration Types

##### 3.5.1.1 vg_lite_quality_t

Specifies the level of hardware-assisted antialiasing.

| vg_lite_quality_t  | description                                                 |
|--------------------|------------------------------------------------------|
| VG_LITE_HIGH       | High quality: 16x coverage sampling anti-aliasing                         |
| *VG_LITE_UPPER*    | *High quality: 8x coverage sampling anti-aliasing (removed from June 2020).* |
| VG_LITE_MEDIUM     | Medium quality: 4x coverage sampling anti-aliasing                        |
| VG_LITE_LOW        | Low quality: No anti-aliasing                                     |

#### 3.5.2 Structs

##### 3.5.2.1 vg_lite_hw_memory

This structure simply records the kernel's memory allocation information.

| field      | type      | description                                                                                            |
|-----------|-----------|-------------------------------------------------------------------------------------------------|
| handle    | void \*   | GPU memory object handle                                                                                 |
| memory    | void \*   | Logical address                                                                                        |
| address   | uint32_t  | GPU memory address                                                                                     |
| bytes     | uint32_t  | size                                                                                            |
| property  | uint32_t  | The 0th bit is used to indicate the path upload. 0: Disables path data upload (always embedded in command buffer). 1: Enable automatic path data upload. |

##### 3.5.2.2 vg_lite_path_t

The structure describes the vector path data.

Path data consists of opcodes and coordinates. The format of opcodes is always VG_LITE_S8. For details on opcodes, refer to the section on [vector path opcodes](#354-vector-path-opcodes) in this document.

| field             | type                   | description                                               |
|------------------|------------------------|----------------------------------------------------|
| bounding_box\[4\]  | vg_lite_float_t        | The bounding box of the path. \[0\] Left \[1\] Top \[2\] Right \[3\] Bottom |
| quality          | vg_lite_quality_t      | Enumeration type of path quality, anti-aliasing level                     |
| format           | enum vg_lite_format_t  | The enumeration type of the coordinate format                                 |
| uploaded         | vg_lite_hw_memory_t    | A structure with path data that has been uploaded to GPU-addressable memory        |
| path_length      | int32_t                | The number of bytes of the path                                       |
| path             | void \*                | Path data pointer                                       |
| path_changed     | int32_t                | 0: unchanged; 1: Change.                                |

About the alignment of coordinate formats with data.

| vg_lite_format_t  | Path data alignment |
|-------------------|--------------|
| VG_LITE_S8        | 8 bit        |
| VG_LITE_S16       | 2 bytes      |
| VG_LITE_S32       | 4 bytes      |

###### 3.5.2.2.1 Special description of path objects

- The end order has no effect because it is boundary-aligned.
- Multiple consecutive opcodes should be packaged at the size of the specified data format. For example, for VG_LITE_S16 packed in 2 bytes, for VG_LITE_S32 packed in 4 bytes. Since opcodes are 8 bits (1 byte), for 16-bit (2-byte) or 32-bit (4-byte) data types:

...

\<opcode1_that_needs_data \>, the opcode is 8 bits.

\<align_to_data_size\> (alignment data).

\< data for opcode1\>\<align_to_data_size\>\<data_for_opcode1\>

\<opcode2_that_doesnt_need_data\> \<opcode2_that_doesnt_need_data\>

\<opcode3_that_needs_data\>\</p\>\<p\>\<p\>

\<align_to_data_size

\<data_for_opcode3\> \<data_for_opcode3\>

...

The path data in the array should always be 1, 2, or 4 bytes aligned, depending on the format. For example, for a 32-bit (4-byte) data type.

...

\<opcode1_that_needs_data \>\<opcode1_that_needs_data\>?

\<pad to 4 bytes

\<4 byte data_for_opcode1\> (4 bytes).

\<opcode2_that_doesnt_need_data\> \<opcode2_that_doesnt_need_data\>

\<opcode3_that_needs_data\>

\<pad to 4 bytes

\<4 bytes data_for_opcode3\>

...

For float types, using the IEEE754 encoding specification, the opcode is still an 8-bit signed integer and may require special handling by the software.

#### 3.5.3 Functions

##### 3.5.3.1 vg_lite_path_calc_length

- description

    This function calculates the buffer length (in bytes) of the path command. The application can allocate a buffer to use as a command buffer based on the buffer length calculated by this function.

- parameter

    uint8_t \*cmd: A pointer to an array of opcodes used to build the path.

    uint32_t count: The number of opcodes.

    vg_lite_format_t format: Coordinate data format, all formats available for vg_lite_format_t are valid formats for this function.

##### 3.5.3.2 vg_lite_path_append

- description

    This function assembles the command buffer for the path, and this function makes the final GPU command for the path based on the input opcode (cmd) and coordinates (data).

- parameter

    vg_lite_path_t \*path: A pointer to the vg_lite_path_t struct with the path definition.

    uint8_t \*cmd: A pointer to an array of opcodes used to build the path.

    void \*data: A pointer to the coordinate data array used to build the path.

    uint32_t seg_count: Number of opcodes.

##### 3.5.3.3 vg_lite_init_path

- description

    This function initializes a path definition with the specified value.

- parameter

    vg_lite_path_t \*path: A pointer to the vg_lite_path_t structure of the path object to initialize with the specified member value.

    vg_lite_format_t data_format: Coordinate data format. All formats in the vg_lite_format_t enumeration are valid formats for the function.

    vg_lite_quality_t quality: The quality of the path object. All formats in the vg_lite_quality_t enumeration are valid formats for this function.

    uint32_t path_length: The length of the path data in bytes.

    void \*path_data: A pointer to path data.

    vg_lite_float_t min_x, vg_lite_float_t min_y, vg_lite_float_t max_x, vg_lite_float_t max_y: Minimum and maximum x and y values that specify the bounding box of the path.

##### 3.5.3.4 vg_lite_init_arc_path

- description

    This function initializes an arc path definition with the specified value.

- parameter

    vg_lite_path_t \*path: Reference vg_lite_init_path.

    vg_lite_format_t data_format: vg_lite_init_path reference.

    vg_lite_quality_t quality: 参考vg_lite_init_path。

    uint32_t path_length: vg_lite_init_path reference.

    void \*path_data: Reference vg_lite_init_path.

    vg_lite_float_t min_x, vg_lite_float_t min_y, vg_lite_float_t max_x, vg_lite_float_t max_y: vg_lite_init_path reference.

##### 3.5.3.5 vg_lite_upload_path

- description

    This function is used to upload the path to GPU memory.

    Under normal circumstances, the GPU driver copies any path data into a command buffer structure during runtime. If there are a lot of paths to render, this does take some time. In addition, in embedded systems, path data usually does not change, so it makes sense to upload path data to GPU memory in a form that can be directly accessed by the GPU. This function will prompt the driver to allocate a buffer that will contain the path data and the data for the head and foot of the required command buffer for the GPU to access this data directly. When the path is finished, call vg_lite_clear_path to free the buffer.

- parameter

    vg_lite_path_t \*path: A pointer to vg_lite_path_t struct that contains the path to upload.

##### 3.5.3.6 vg_lite_clear_path

- description

    This function will clear and reset the path member values. If the path has already been uploaded, it will free the GPU memory allocated when the path was uploaded.

- parameter

    vg_lite_path_t \*path: A pointer to the vg_lite_path_t path definition to clear.

#### 3.5.4 Vector Path Opcodes

The following opcodes are path drawing commands that can be used for vector path data.

A path operation is submitted to the GPU in the form of \[opcode\|coordinates\]. Operation codes are stored in the form of VG_LITE_S8, while coordinates are specified by vg_lite_format_t.

| Opcode | parameter                               | description                                                                                                                                                                                                                   |
|--------|------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 0x00   | None                               | END. Finish, closing all open paths.                                                                                                                                                                                        |
| 0x02   | (x,y)                              | MOVE. Move to a given vertex. Close all open paths. = =                                                                                                                                                         |
| 0x03   | (Δx,Δy)                            | MOVE_REL. Move to a given relative point. Close all open paths. =+Δ =+Δ                                                                                                                                   |
| 0x04   | (x,y)                              | LINE. Draw a straight line to a given vertex. (,,,) = =                                                                                                                                               |
| 0x05   | (Δx,Δy)                            | LINE_REL. Draw a straight line to the vertices at opposite positions. =+Δ =+Δ (,,,) = =                                                                                                               |
| 0x06   | (cx,cy) (x,y)                      | QUAD. Draws a quadric to a given endpoint using the specified control points. (,,,,,) = =                                                                                                                 |
| 0x07   | (Δcx,Δcy)  (Δx,Δy)                 | QUAD_REL. Draws a quadric to the endpoint of a given relative position using the specified relative control point. = +Δ =+Δ = +Δ =+Δ (,,,,,) = =                                         |
| 0x08   | (cx1,cy1) (cx2,cy2) (x,y)          | CUBIC. Draws a cubic curve to a given endpoint using the specified control points. (,,1,1,2,2,,) = =                                                                                                       |
| 0x09   | (Δcx1,Δcy1)  (Δcx2,Δcy2)  (Δx,Δy)  | CUBIC_REL. Draws a cubic curve to the endpoint of a given relative position using the specified control point. 1= +Δ1 1=+Δ1 2=+Δ2 2=+Δ2 =+Δ =+Δ (,,1,1,2,2,,) = =  |
| 0x0A   | (rh,rv,rot,x,y)                    | SCCWARC. Draw a small CCW arc to the given endpoint using the specified radius and rotation angle. (,,,,) = =                                                                                                            |
| 0x0B   | (rh,rv,rot,x,y)                    | SCCWARC_REL. Draw a small CCW arc towards the given opposite endpoints using the specified radius and rotation angle. =+Δ =+Δ (ℎ,,,,) = =                                                                            |
| 0x0C   | (rh,rv,rot,x,y)                    | SCWARC. Draw a small CW arc to the given endpoint using the specified radius and rotation angle. (ℎ,,,,) = =                                                                                                               |
| 0x0D   | (rh,rv,rot,x,y)                    | SCWARC_REL. Draw a small CW arc to a given opposite endpoint using the specified radius and rotation angle. =+Δ =+Δ (ℎ,,,,) = =                                                                               |
| 0x0E   | (rh,rv,rot,x,y)                    | LCCWARC. Draw a large CCW arc towards a given endpoint using the specified radius and rotation angle. (ℎ,,,,) = =                                                                                                            |
| 0x0F   | (rh,rv,rot,x,y)                    | LCCWARC_REL. Draw a large CCW arc towards a given opposite endpoint using the specified radius and rotation angle. =+Δ =+Δ (ℎ,,,,) = =                                                                            |
| 0x10   | (rh,rv,rot,x,y)                    | LCWARC. Draw a large CW arc to the given endpoint using the specified radius and rotation angle. (ℎ,,,,) = =                                                                                                               |
| 0x11   | (rh,rv,rot,x,y)                    | LCWARC_REL. Draw a large CW arc to a given relative endpoint using the specified radius and rotation angle. =+Δ =+Δ (ℎ,,,,) = =                                                                               |

### 3.6 Vector-based drawing operations

#### 3.6.1 Enumeration Types

##### 3.6.1.1 vg_lite_fill_t

This enumeration is used to specify the padding rule to use. For drawing any path, the hardware supports non-zero and parity fill rules.

To determine whether any point is contained within an object, imagine drawing a line from that point in any direction to infinity so that the line does not cross any vertices of the path. For each edge crossed by the line, add 1 to the counter if the edge crosses from left to right, as seen by an observer walking from the line to infinity; subtract 1 if the edge crosses from right to left. This way, each area of the plane gets an integer value.

The non-zero fill rule says that if the resulting sum is not equal to zero, then a point is within the shape. The even/odd rule says that if the sum of the results is odd, then a point is inside the shape, regardless of the sign.

| vg_lite_fill_t        | description                                                             |
|-----------------------|------------------------------------------------------------------|
| VG_LITE_FILL_NON_ZERO | Non-zero fill rules. If a pixel intersects at least one path pixel, it is drawn. |
| VG_LITE_FILL_EVEN_ODD | Even fill rules. If a pixel intersects an odd number of path pixels, it is drawn.   |

##### 3.6.1.2 vg_lite_pattern_mode_t

Defines how areas outside the image pattern are filled onto the path.

| vg_lite_pattern_mode_t  | description                                     |
|-------------------------|------------------------------------------|
| VG_LITE_PATTERN_COLOR   | Fills the outside of the pattern by color.                   |
| VG_LITE_PATTERN_PAD     | The color of the pattern border is expanded to fill the area outside the pattern. |

#### 3.6.2 Structures

##### v3.6.2.1 g_lite_color_ramp_t

This structure defines the end point of the radial gradient. Five parameters provide the offset and color of the stop. Each stop is defined by a set of floating-point values that specify the offset as well as the sRGBA color and alpha values. The values of the color channel exist as non-multiplying (R, G, B, ALPHA) quadrilaterals. All parameters are in the range of \[0,1\]. Red, green, blue, α values \[0,1\] are mapped to 8-bit pixel values \[0,255\].

The maximum number of defined radial gradient stops is MAX_COLOR_RAMP_STOPS, which is 256.

| field   | type             | description                    |
|--------|------------------|-------------------------|
| stop   | vg_lite_float_t  | The offset of the color stop      |
| red    | vg_lite_float_t  | The offset of the red stop      |
| green  | vg_lite_float_t  | The offset of the green stop      |
| blue   | vg_lite_float_t  | The offset of the blue stop      |
| alpha  | vg_lite_float_t  | The offset of the alpha channel stop |

##### 3.6.2.2 vg_lite_linear_gradient_t

This structure defines the organization of linear gradients in VGLite data. A linear gradient is applied to fill the path. It will generate a 256x1 image depending on the settings.

| field                  | type              | description                           |
|-----------------------|-------------------|--------------------------------|
| colors\[VLC_MAX_GRAD\]  | uint32_t          | An array of colors for the gradient                 |
| count                 | uint32_t          | Number of colors                       |
| stops\[VLC_MAX_GRAD\]   | uint32_t          | Number of color levels, from 0 to 255               |
| matrix                | vg_lite_matrix_t  | A matrix structure that converts the gradient color slope   |
| image                 | vg_lite_buffer_t  | An image object structure that represents the color slope. |

The VLC_MAX_GRAD is the largest of 16, VLC_GRADBUFFER_WIDTH the maximum is 256.

#### 3.6.3 Functions

##### 3.6.3.1 vg_lite_draw

- description

    Perform hardware-accelerated 2D vector drawing operations.

    The size of the insert buffer can be specified at initialization time, and the size will be adjusted by the kernel to the minimum alignment required by the hardware. If you make the insert buffer smaller, less memory will be allocated, but a path may be delivered to the hardware multiple times, because the hardware will walk the target with the provided insert window size, so performance may be degraded. It is good practice to set the size of the insert buffer to the most common path size. For example, if all you do is render fonts up to 24pt, you can set the insert buffer to 24x24.

- parameter

    vg_lite_buffer_t \*target: A pointer to the vg_lite_buffer_t struct of the destination buffer. All color formats in vg_lite_buffer_format_t enumerations are valid target formats for drawing functions.

   vg_lite_path_t \*path: A pointer to vg_lite_path_t structure that contains data that describes the path to draw. For details on opcodes, refer to the section on [vector path opcodes](#354-vector-path-opcodes) in this file.

    vg_lite_fill_t fill_rule: Specifies the enumeration value of the vg_lite_fill_t for the path's fill rule.

    vg_lite_matrix_t \*matrix: A pointer to vg_lite_matrix_t structure that defines the affine transformation matrix of the path. If the matrix is NULL, an identity matrix is assumed. Note: Nonaffine transformations are not supported vg_lite_draw, so the perspective transformation matrix has no effect on the path.

    vg_lite_blend_t Blend: Selects a hardware-supported blend mode in the vg_lite_blend_t enumeration to apply to each drawn pixel. If blending is not required, set this value to VG_LITE_BLEND_NONE, which is 0.

    vg_lite_color_t color: The color applied to each pixel drawn by the path.

##### 3.6.3.2 vg_lite_draw_gradient

- description

    This function is used to fill the path with a gradient color according to the specified fill rule. The specified path is transformed according to the selected matrix and filled with a gradient.

- parameter

    vg_lite_buffer_t \*target: 参照vg_lite_draw.

    vg_lite_path_t \*path: See vg_lite_draw.

    vg_lite_fill_t fill_rule: See vg_lite_draw.

    vg_lite_matrix_t \*matrix: See vg_lite_draw.

    vg_lite_linear_gradient_t \*grad: A pointer to vg_lite_linear_gradient_t struct that contains values to fill the path.

    vg_lite_blend_t blend: See vg_lite_draw.

##### 3.6.3.3 vg_lite_draw_pattern

- description

    This function fills a path with an image pattern. The path is transformed according to the specified matrix and filled with the converted image pattern.

- parameter

    vg_lite_buffer_t \*target: 参照vg_lite_draw.

    vg_lite_path_t \*path: See vg_lite_draw.

    vg_lite_fill_t fill_rule: See vg_lite_draw.

    vg_lite_matrix_t \*matrix0: A pointer to the vg_lite_matrix_t struct, which defines the 3x3 transformation matrix of the path. If the matrix is NULL, an identity matrix is assumed.

    vg_lite_buffer_t \*source: A pointer to the vg_lite_buffer_t structure that describes the source of the image pattern.

    vg_lite_matrix_t \*matrix1: A pointer to a vg_lite_matrix_t structure that defines a 3x3 transformation from source pixel to destination pixel. If the matrix is NULL, an identity matrix is assumed, which means that the source pixel will be copied directly to the 0,0 position of the destination pixel.

    vg_lite_blend_t blend: See vg_lite_draw.

    vg_lite_pattern_mode_t pattern mode: Specifies vg_lite_pattern_mode_t value that defines how to fill the area outside the image pattern.

    vg_lite_color_t pattern_color: Specify a 32bpp ARGB color (vg_lite_color_t) that is applied to the fill outside the image pattern area when the pattern_mode value is VG_LITE_PATTERN_COLOR.

    vg_lite_filter_t filter: Specifies the type of filter. All formats in the vg_lite_filter_t enumeration are valid formats for this function. A value of zero (0) indicates VG_LITE_FILTER_POINT.

#### 3.6.4 Linear gradient initialization and control functions

##### 3.6.4.1 vg_lite_init_grad

- description

    This function initializes the internal buffer of the linear gradient object with default settings for rendering.

- parameter

    vg_lite_linear_gradient_t \*grad: A pointer to vg_lite_linear_gradient_t structure that defines the gradient to be initialized. Use the default values.

##### 3.6.4.2 vg_lite_set_grad

- description

    This function is used to set the value of a vg_lite_linear_gradient_t structure member.

    Note: In cases where the input parameters are incomplete or invalid, the default gradient color is set using the following rules.

  1. If no valid stop is specified (for example, due to an empty input array, out-of-range, or out-of-order check), a stop of 0 with (R, G, B, α) color (0.0, 0\.0, 0\.0, 1\.0) (opaque black) and a stop 1 with color (1\.0, 1\.0, 1\.0) (opaque white) are implicitly defined.
  1. If at least one valid stop is specified, but no stop with offset 0 is defined, an implied stop is added with an offset of 0 and the same color as the first user-defined stop.
  1. If at least one valid stop is specified, but no stop with an offset of 1 is defined, an implicit stop is added with an offset of 1 and the same color as the last user-defined stop.

- parameter

    vg_lite_linear_gradient_t \*grad: A pointer to the vg_lite_linear_gradient_t struct to set.

    uint32_t count: The count of colors in a linear gradient. The maximum patch count is defined by the VLC_MAX_GRAD, which is 16.

    uint32_t \*colors: Specifies the color array of the gradient, ARGB8888 format, with alpha in the highest position.

    uint32_t \*stops: A pointer to the offset at which the gradient stops.

##### 3.6.4.3 vg_lite_update_grad

- description

    This function is used to update or generate the value of an image object that will be rendered. vg_lite_linear_gradient_t object has an image buffer that renders the gradient pattern. The image buffer is created or updated with the appropriate gradient parameters.

- parameter

    vg_lite_linear_gradient_t \*grad: A pointer to the vg_lite_linear_gradient_t struct that contains the updated values to use to render the object.

##### 3.6.4.4 vg_lite_get_grad_matrix

- description

    This function is used to get a pointer to the transformation matrix of the gradient object, which allows the application to manipulate the matrix to facilitate the correct rendering of the gradient path.

- parameter

    vg_lite_linear_gradient_t \*grad: A pointer to vg_lite_linear_gradient_t struct that contains the matrix to retrieve.

##### 3.6.4.5 vg_lite_clear_grad

- description

    This function is used to clear the value of a linear gradient object, freeing memory in the image buffer.

- parameter

    vg_lite_linear_gradient_t \*grad: A pointer to the vg_lite_linear_gradient_t structure to clean.

## 4. Constraints

The GPU driver **only supports one current context and one thread to issue commands to the GPU**. **GPU drivers do not support multiple** concurrent contexts running simultaneously in multiple threads/processes because GPU kernel drivers do not support context switching. A GPU application can only use one context to issue commands to the GPU hardware at any one time. If a GPU application needs to switch contexts, it should call[vg_lite_close to close the current context in the current thread](#3213-vg_lite_close), and then the vg_lite_init can be called to[](#3212-vg_lite_init)initialize a new context in the current thread or in another thread/process.

## 5. Performance recommendations and best practices

### 5.1 Cache vs Non-cache

When loading the vg_lite.ko module, you can configure whether to turn off cache (cache is enabled by default) through the cache parameter, the driver will refresh the CPU cache (D-cache and L2-cache) before submitting the command to the GPU hardware in cache mode, and set the command buffer and graphics memory to non-cache when mapped to the user-mode address space in non-cache mode. In general, cache mode has better performance, and the CPU is faster to write command buffer and read graphics memory.

At present, flushing the cache uses the dcache.cipa directive, which can only flash one cache line at a time, that is, 64Bytes, for larger buffers such as 1920x1080@ARGB32, it takes about 129600 loops, most of which are missed, which will bring some performance overhead, and if you use the dcache.ciall directive you can flush all caches, but may affect other processes so they are not used.

### 5.2 Memory Usage

vg_lite.ko modules take up about 130KB of memory after loading, and hardly take up more space except command buffer and video memory, and each memory allocated by the vg_lite_hal_allocate_contiguous requires corresponding page table resources and a node size of 64B in addition to the memory itself.

### 5.3 Drawing Process

Use the VGLite API to operate

1. Call[vg_lite_init](#3212-vg_lite_init)initialize the GPU
1. If GPU memory is required, call[vg_lite_allocate](#3251-vg_lite_allocate)allocation and mapping
1. Draw using the API
1. Call[vg_lite_finish](#3214-vg_lite_finish)or[vg_lite_flush](#3215-vg_lite_flush)commit command to render and wait for the drawing to finish
1. Before the process ends, the calling[vg_lite_close](#3213-vg_lite_close)shuts down the GPU

## 6. Examples

The K230 SDK includes several GPU examples, the source code is placed  in `src/little/buildroot-ext/package/vg_lite/test/samples`, open BR2_PACKAGE_VG_LITE_DEMOS in buildroot to build and add to the generated system image (open by default).

### 6.1 tiger

This is an example of drawing a tiger image, which is generated in the current directory when run `tiger.png`.

![tiger.png](../../../../zh/01_software/board/mpp/images/tiger.png)

### 6.2 linear degrees

This is an example of an image with a linear gradient that, when run, is generated in the current directory `linearGrad.png`.

![lineardegree.png](../../../../zh/01_software/board/mpp/images/linearGrad.png)

### 6.3 imgIndex

This is an example that uses a color lookup table that, when run, generates , and in the current directory `imgIndex1.png``imgIndex2.png` `imgIndex4.png`, `imgIndex8.png`each with a different number of color indexes.

![imgIndex1.png](../../../../zh/01_software/board/mpp/images/imgIndex1.png)

![imgIndex2.png](../../../../zh/01_software/board/mpp/images/imgIndex2.png)

![imgIndex4.png](../../../../zh/01_software/board/mpp/images/imgIndex4.png)

![imgIndex8.png](../../../../zh/01_software/board/mpp/images/imgIndex8.png)

### 6.4 vglite_drm

Here is an example of GPU + DRM display linkage,

Note: Since the video output driver under Linux does not**include**initialization, you need to make sure that the screen is already in use before running, for example, it can be run on a big core`sample_vo.elf 3`.

### 6.5 vglite_cube

This is an example of a GPU + DRM display linkage, drawing a constantly rotating cube on the screen.

Note: Since the video output driver under Linux does not**include**initialization, you need to make sure that the screen is already in use before running, for example, it can be run on a big core`sample_vo.elf 3`.
