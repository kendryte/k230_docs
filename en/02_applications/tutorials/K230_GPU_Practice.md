# K230 GPU in action - VGLite paints cool graphics

![cover](../../../zh/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document focuses on drawing vector graphics with the K230 GPU.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | Full name                  |
|------|-----------------------|
| GPU  | Graphics Process Unit |
| SVG | Scalable Vector Graphics |
| DRM | Direct Rendering Manager |

### Revision history

| Document version number | Modify the description | Author     | date       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | Initial | Huang Ziyi | 2023-06-20 |

## Concept introduction

### Vector graphics basics

Vector graphics are images represented by mathematical equation-based geometric elements such as points, lines, or polygons, and unlike bitmaps that use pixels to represent images, vector graphics can be infinitely enlarged without distortion. SVG is a typical vector graphics format, itself is an XML text file, describing the location of various elements, open through the browser to see the rendered effect, if you don't understand the VGLite API used by the K230 GPU, you can see it as a weakened version of SVG.

The K230 GPU supports a wide range of 2D elements

- straight line
- Quadratic Bezier curve
- Cubic Bezier curve
- Circular curve (of course, it can also be fitted with cubic Bézier curve)

Note: **These graphics are lines, and the GPU cannot draw lines directly, only closed shapes enclosed by these lines.**

### GPU foundation

On the K230 SDK's small-core Linux, the GPU is mainly interacted with by calling the VGLite API. VGLite internally maintains a command queue for the GPU, which is submitted to the GPU hardware for rendering when it needs to complete the draw, or when the queue is full. The length of the command queue defaults to 65536, and you can call the `vg_lite_set_command_buffer_size` function to modify it.

Note: The VGLite API **does not support use in a multithreaded context, if your application uses multithreading, make sure that only one thread will use the VGLite API**.

The K230 GPU is a memory-to-memory device that does not have its own display output capabilities, and can be used with DRM if a display is required.

## Use the VGLite API

### Development environment preparation

The VGLite API mainly consists of two parts, header files and library files, where the location of header files is in

```text
<K230 SDK>/src/little/buildroot-ext/package/vg_lite/inc/vg_lite.h
```

After the K230 SDK is fully compiled, the library files are placed in

```text
<K230 SDK>/output/k230_evb_defconfig/little/buildroot-ext/target/usr/lib/libvg_lite.so
```

#### make

Put the source file of the code into `src` the directory, create a Makefile and  paste the following content into it, set`K230SDK` the environment variable to the path where the K230 SDK is stored (or change the first line to the path to store the K230 SDK`/path/to/k230_sdk`), you can use the command to build, `make`after the build is completed, the executable file will be generated in the same directory of the Makefile and copied to the little core Run it on linux, or you can use `make install` copy it to the K230 SDK,  build the image in the K230 SDK directory, and then flash it to an SD card or eMMC to boot.

```Makefile
K230SDK ?= /path/to/k230_sdk
BIN := test-vglite

CC := "$(K230SDK)/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc"
CXX := "$(K230SDK)/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-g++"

CFLAGS += -I"$(K230SDK)/src/little/buildroot-ext/package/vg_lite/inc" -I"$(K230SDK)/output/k230_evb_defconfig/little/buildroot-ext/host/riscv64-buildroot-linux-gnu/sysroot/usr/include"
CFLAGS += -L"$(K230SDK)/output/k230_evb_defconfig/little/buildroot-ext/target/usr/lib"
CFLAGS += -lvg_lite -lvg_lite_util -ldrm
CFLAGS += -Wall -g

CXXFLAGS := $(CFLAGS)

SRCDIR := ./src
OBJDIR := ./objs
SRCS := $(wildcard $(SRCDIR)/*.c) $(wildcard $(SRCDIR)/*.cpp)
OBJS := $(patsubst $(SRCDIR)/%.c,$(OBJDIR)/%.o,$(filter %.c, $(SRCS))) \
        $(patsubst $(SRCDIR)/%.cpp,$(OBJDIR)/%.o,$(filter %.cpp, $(SRCS)))
DEPS := $(patsubst $(SRCDIR)/%.c,$(OBJDIR)/%.d,$(filter %.c, $(SRCS))) \
        $(patsubst $(SRCDIR)/%.cpp,$(OBJDIR)/%.d,$(filter %.cpp, $(SRCS)))

all: $(BIN)

$(OBJDIR):
	mkdir -p $(OBJDIR)

$(BIN): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.c | $(OBJDIR)
	$(CC) $(CFLAGS) -MMD -c $< -o $@

$(OBJDIR)/%.o: $(SRCDIR)/%.cpp | $(OBJDIR)
	$(CXX) $(CXXFLAGS) -MMD -c $< -o $@

-include $(DEPS)

clean:
	rm -rf $(OBJDIR) $(BIN)

install:
	cp $(BIN) "$(K230SDK)/output/k230_evb_defconfig/little/buildroot-ext/target/usr/bin"

uninstall:
	rm "$(K230SDK)/output/k230_evb_defconfig/little/buildroot-ext/target/usr/bin/$(BIN)"

.PHONY: all clean install

```

#### CMake

Put the source file of the code into `src` the directory,  create a `CMakeLists.txt` file and paste the following content into it, modify the third line`/path/to/k230_sdk` to the directory where the K230 SDK is stored, you can use cmake to build.

```CMakeLists.txt
cmake_minimum_required(VERSION 3.0)
project(test-vglite)
set(K230SDK /path/to/k230_sdk)

set(CMAKE_C_COMPILER "${K230SDK}/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-gcc")
set(CMAKE_CXX_COMPILER "${K230SDK}/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0/bin/riscv64-unknown-linux-gnu-g++")
set(CMAKE_C_FLAGS "-Wall")
set(CMAKE_CXX_FLAGS "-Wall")

include_directories(
    "${K230SDK}/output/k230_evb_defconfig/little/buildroot-ext/host/riscv64-buildroot-linux-gnu/sysroot/usr/include"
    "${K230SDK}/src/little/buildroot-ext/package/vg_lite/inc"
)

link_directories("${K230SDK}/output/k230_evb_defconfig/little/buildroot-ext/target/usr/lib")
link_libraries(vg_lite vg_lite_util drm)

file(GLOB SOURCES "src/*.c" "src/*.cpp")

add_executable(${PROJECT_NAME} ${SOURCES})

install(TARGETS ${PROJECT_NAME} DESTINATION "${K230SDK}/output/k230_evb_defconfig/little/buildroot-ext/target/usr/bin")

```

### display

The K230 EVB has a 1080x1920 display, which can be displayed with DRM on small-core Linux, and allowing the GPU driver to load DRM dumb buffer can reduce memory copies and achieve efficient rendering. The relevant code of GPU+DRM can refer `vglite_drm` to  this demo, and readers can add `drm.c` it to their own programs.

It should be noted that as of K230 SDK v0.8, the DRM driver on linux still**cannot**work independently, and it needs to rely on the configuration of the SoC video output module, which can be completed by executing on the big core `sample_vo.elf 3` .

Secondly, the color format enumeration  of DRM `vg_lite_buffer_format_t` is not exactly consistent with , for example, represents red in the `VGLITE_BGRA8888` lower 8 bits and alpha in the upper 8 bits of 32-bit color, corresponding to the DRM `DRM_FORMAT_ARGB8888` in .

![vglite_drm demo run results](../../../zh/02_applications/tutorials/images/gpu-1.jpg)

As shown in the figure vglite_drm The correct color displayed on the screen after running: R(255)G(128)B(16)

Generally speaking, in order to achieve synchronous display, two buffers will be needed for ping-pong alternating display, but in order to simplify the demo code, only one is used here, and readers can achieve vertical synchronization of double buffers for continuous rendering.

## drawing

### Some preparation

First of all, you need to initialize VGLite, call `vg_lite_init` to complete, it  has two parameters `tessellation_width` and  , for rendering the size of the window, the `tessellation_height`larger the more efficient, if it is 0 means that the vector drawing function is not used, only BLIT, usually set to the size of the maximum buffer.

Rendering requires buffers, which can be imported from DRM dumb, like the following

```c
vg_lite_buffer_t buffer;
int buf_fd;
memset(&buffer, 0, sizeof(buffer));
buf_fd = drm_get_dmabuf_fd(0);
if (buf_fd < 0) {
    perror("get fd");
    return buf_fd;
}
memset(&buffer, 0, sizeof(buffer));
buffer.width = width;
buffer.height = height;
buffer.format = VG_LITE_ARGB8888;
buffer.stride = buffer.width * 4;
if (vg_lite_from_dma_buf(buf_fd, &buffer.address)) {
    perror("import dma-buf");
    return -1;
}
```

Off-screen buffers can also be allocated from the GPU driver, as shown below

```c
vg_lite_buffer_t buffer;
memset(&buffer, 0, sizeof(buffer));
buffer.width = width;
buffer.height = height;
buffer.format = VG_LITE_ARGB8888;
if (vg_lite_allocate(&buffer)) {
    return -1;
}
```

Obviously, it is simpler to allocate off-screen buffers, only need to configure the resolution and pixel format, and importing from DRM dumb also needs to calculate the stride (the number of bytes in a row), of course, the advantage of importing from DRM dumb is that it can be directly used for display, of course, the buffer allocated from the driver can also be imported into DRM for display.

### polygon

With buffer, you can start drawing. A polygon consists of multiple straight lines, in the case of a triangle, you first need to determine the coordinates of the three vertices of the triangle, for example, the`(0,0) (0,1) (1,0)` whole process is as follows

1. Move the brush to`(0,0)`
1. Draw a line to`(0,1)`
1. Draw a line to`(1,0)`
1. Draw a line to`(0,0)`
1. Close the graph

Consulting the K230 GPU API reference can see that the mobile opcode is 2, the straight opcode is 4, and the closed path opcode is 0, using the first data format, the array can be constructed `path_data` as follows

```c
uint8_t path_data[] = {
    2, 0, 0, // 移动到 (0,0)
    4, 0, 1, // 直线到 (0,1)
    4, 1, 0, // 直线到 (1,0)
    4, 0, 0, // 直线到 (0,0)
0};
```

Only path_data is not enough, the parameters required for rendering are path, and the path contains information such as data formats in addition to path_data, and the format of the data can be specified as the following:

1. 8-bit signed integer
1. 16-bit signed integer
1. 32-bit signed integer
1. 32-bit floating-point number

Performance decreases from top to bottom, but even 8-bit signed integers do not mean that only the pixel range of -128 to 127 can be covered, because a matrix transformation is also required to calculate the final coordinates.

Now construct the path and draw to the buffer

```c
vg_lite_path_t path = {
    .bounding_box = {0., 1., 1., 0.}, // 图形的包围盒
    .quality = VG_LITE_HIGH, // 渲染质量
    .format = VG_LITE_S8, // 考虑到坐标很简单，所以 8bit 足够
    .uploaded = 0, // 路径没有被上传过 GPU，所以用0
    .path_length = sizeof(path_data), // 路径数据长度，以字节为单位
    .path = path_data, // 路径数据就放在这了
    .path_changed = 1, // 用来表示路径被更新过
    .pdata_internal = 0 // 表示路径数据不是由驱动分配的
};
```

With the above variables, you can perform rendering, following the steps

1. Emptying the buffer, i.e. filling it with a monochrome color, can be done using `vg_lite_clear`
1. A transformation matrix, about the matrix can refer to affine transformation related content, here directly use a scaling matrix, the image is enlarged 100 times, so that the final length of 1 straight line will use 100 pixels in the image
1. Call `vg_lite_draw` to "render" path to buffer
1. Finally, use Submit `vg_lite_finish` Rendering

To facilitate error handling, use `CHECK_ERROR` macros to wrap the function that returns `vg_lite_error_t`

```c
vg_lite_matrix_t matrix;
CHECK_ERROR(vg_lite_clear(&buffer, NULL, 0xffff0000)); // 使用蓝色填充整个 buffer
vg_lite_identity(&matrix); // 初始化为单位矩阵
vg_lite_translate(buffer.width / 2., buffer.height / 2., &matrix); // 移动到 buffer 中间位置
vg_lite_scale(100., 100., &matrix); // x y 方向都放d大100倍
CHECK_ERROR(vg_lite_draw(
    &buffer, &path,
    VG_LITE_FILL_NON_ZERO, //  填充规则，像素只要被覆盖就会被绘制
    &matrix,
    VG_LITE_BLEND_NONE, // 颜色混合规则，None 表示忽略透明度直接覆盖
    0xff0000ff // RGBA 颜色，这个值表示不透明的红色
));
CHECK_ERROR(vg_lite_finish()); // 提交到 GPU
```

The complete reference code can be viewed in vglite_drm, and below is the plotted effect.

![A simple triangle to draw](../../../zh/02_applications/tutorials/images/gpu-2.jpg)

It is easy to see that the coordinate system is right in the positive x direction and the following is the positive direction of y, which is also the coordinate system used by SVG.

It should be noted that I just said that `vg_lite_draw` "rendering" is in quotation marks, because there is  no real rendering, just write rendering instructions`vg_lite_finish`, and the final rendering needs to be called, which is good for performance, and can be called many times in actual use`vg_lite_draw`, and then executed before the final actual display`vg_lite_finish`, because is a system call, there is a certain overhead, and `vg_lite_finish` `vg_lite_draw` No, it can be executed quickly.

When the rendering is completed, the result can be displayed to the screen or saved as a picture, you need to pay attention to the CPU to read the data when saving the picture, so you need to make sure that `vg_lite_buffer_t::memory` it  is readable, if the reader uses the above DRM code to create `vg_lite_buffer_t` , then it cannot be read without mapping DRM dumb.

### curve

The K230 GPU supports three curves, which are:

1. Quadratic Bezier curve
1. Cubic Bezier curve
1. Elliptic curve

Of course, elliptic curves can be fitted with cubic Bezier curves, which can essentially be regarded as the same curve type, as in the case of drawing polygons, only need to modify the opcode and data.

Below we try to change the base edge of the triangle just drawn to a quadratic Bezier curve, and place the midpoint `(1,1)`at the place, draw a pattern with approximately rounded corners, and change the above `path_data` to

```c
uint8_t path_data[] = {
    2, 0, 0,
    4, 0, 1,
    6, 1, 1, 1, 0, // 二次贝塞尔曲线，控制点(1,1)，画到(1,0)
    4, 0, 0,
0};
```

Of course, to get a better view of the curve, we turned the zoom factor larger, say 500x, and made the displacement smaller so that the pattern is approximately in the center of the screen

```c
vg_lite_translate(buffer.width / 2., buffer.height / 2., &matrix);
vg_lite_scale(500., 500., &matrix);
```

The final pattern is drawn like this

![A sector with approximately rounded corners](../../../zh/02_applications/tutorials/images/gpu-3.jpg)

### Bitmap fill

When not satisfied with monochrome filling, you can use bitmap to fill, bitmap files will be rendered to the target location, of course, bitmaps must also be `vg_lite_buffer_t` ,  if you need to load from local JPEG/PNG files, then it is recommended to use off-screen buffer to store pixel content, with `vg_lite_blit` or  to `vg_lite_draw_pattern` render.

### Gradient

For the implementation of VGLite, the gradient itself is a special bitmap filling, `linear_grad` the related function will allocate a 1x256 buffer for BLIT, of course, the user can not care about the above details, take it to use, refer to `linearGrad` the  demo, the specific process can be divided into the following calls

1. `vg_lite_init_grad` Initialize a gradient
1. `vg_lite_set_grad` Set color and stop center, up to 16 stop center is supported
1. `vg_lite_update_grad` Update the gradient
1. `vg_lite_get_grad_matrix` Gets the transformation matrix pointer for the gradient
1. Adjustments to the transformation matrix, such as rotation and scaling, have a default length of 256 pixels from left to right, which is required for gradients in other directions
1. `vg_lite_draw_gradient` Draw a gradient
