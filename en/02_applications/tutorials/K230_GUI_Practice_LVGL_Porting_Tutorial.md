# K230 GUI Practical - LVGL Porting Tutorial

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within your purchase or usage scope. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for guidance reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Target Audience

This document (this guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
| --- | --- |
| DRM | Direct Rendering Manager |
| KMS | Kernel Mode Setting |
| GUI | Graphical User Interface |

### Revision History

| Document Version | Modification Description | Modifier | Date |
| --- | --- | --- | --- |
| V1.0 | Initial Version | Wang Quan | 2023/06/25 |

## K230 GUI Practical

LVGL is a popular free and open-source embedded graphics library that can be used for graphical user interface (GUI) development in embedded systems.

### Hardware Environment

- K230-USIP-LP3-EVB-V1.1
- Matching LCD module

### Overview

K230 uses DRM as the display driver. DRM (Direct Rendering Manager) is a subsystem in the Linux kernel that supports complex GPU operations such as hardware-accelerated graphics rendering, compared to the outdated Framebuffer. LVGL can use the interfaces provided by libdrm for GUI rendering.

The LVGL component has already been ported in the SDK, and a runnable demo is compiled by default, located at `/usr/bin/lvgl_demo_widgets`. After booting, enter the command `lvgl_demo_widgets` in the Linux terminal on the small core to experience it.

### LVGL Source Code Location

The SDK already includes the ported LVGL, located at `src/little/buildroot-ext/package/lvgl`. During the buildroot compilation process of the SDK, the source code is placed in the directory `output/k230_evb_defconfig/little/buildroot-ext/build/lvgl-v8.3.7`, which contains the LVGL source package pulled from GitHub as well as the porting files under the src path mentioned earlier. The directory structure is as follows:

```sh
.
├── lv_conf.h
├── lv_drivers
│   ├── display
│   │   ├── drm.c
│   │   └── drm.h
│   ├── indev
│   │   ├── AD_touch.c
│   │   ├── AD_touch.h
│   │   ├── evdev.c
│   │   ├── evdev.h
│   │   ├── keyboard.h
│   │   ├── libinput.c
│   │   ├── libinput_drv.h
│   │   ├── mouse.h
│   │   └── mousewheel.h
│   └── lv_drivers.mk
├── lv_drv_conf.h
├── main.c
├── Makefile
└── mouse_cursor_icon.c
```

### LVGL's DRM Driver

After the DRM driver is successfully loaded in the Linux kernel, the following node will appear: `/dev/dri/card0`.

#### DRM Configuration

In the header file `src/little/buildroot-ext/package/lvgl/port_src/lv_drv_conf.h`:

- Configure the macro definition `#define USE_DRM 1` to enable the DRM display driver.
- Configure the macro definition `#define DRM_CARD "/dev/dri/card0"` to specify the DRM driver node.

#### Introduction to DRM Driver Source Code

The DRM driver program of LVGL is located at `src/little/buildroot-ext/package/lvgl/port_src/lv_drivers/display/drm.c`.
To operate DRM, the file node needs to be opened first.
The following functions are mainly used in LVGL:

- drm_init()        DRM initialization.
- drm_get_sizes()   Get display resolution information.
- drm_flush()       Display drawing callback interface.

During DRM initialization, DRM resources are automatically obtained, including the connect id, plane id, crtc id, etc., and the corresponding supported plane is automatically matched according to the color format selected in the configuration file.

The DRM driver enables double buffering by default, but without hardware acceleration, the double buffering refresh rate is low. You can comment out the following code to refresh in single buffering mode for better display performance:

```c
void drm_flush(lv_disp_drv_t *disp_drv, const lv_area_t *area, lv_color_t *color_p)
{
    ...
    if (!drm_dev.cur_bufs[0])
        drm_dev.cur_bufs[1] = &drm_dev.drm_bufs[1];
    else
        drm_dev.cur_bufs[1] = drm_dev.cur_bufs[0];
    drm_dev.cur_bufs[0] = fbuf;
    ...
}
```

### Using LVGL

The main program file of LVGL is located at `src/little/buildroot-ext/package/lvgl/port_src/main.c`.

#### LVGL Configuration

The LVGL configuration file is located at: `src/little/buildroot-ext/package/lvgl/port_src/lv_conf.h`.

Here are a few common configuration items:

- `#define LV_COLOR_DEPTH 32`           Set color depth.
- `#define LV_COLOR_SCREEN_TRANSP 1`    Set screen transparency.
- `#define LV_DPI_DEF 300`              Set screen DPI.
- `#define LV_USE_PERF_MONITOR 1`       Display fps and CPU usage for debugging.
- `#define LV_USE_MEM_MONITOR 1`        Display memory usage for debugging.
- `#define LV_USE_DEMO_WIDGETS 1`       Enable LVGL widgets demo.

#### Main Steps to Use LVGL

1. Initialize LVGL:

    `lv_init();`

1. Initialize display driver:

    ```c
    drm_init();
    drm_get_sizes(&lcd_w, &lcd_h, &lcd_dpi);
    printf("lcd w,h,dpi:%d,%d,%d \n", lcd_w, lcd_h, lcd_dpi);

    uint32_t draw_buf_size = lcd_w * lcd_h * sizeof(lv_color_t) / 4; /*1/4 screen sized buffer has the same performance */
    static lv_disp_draw_buf_t disp_buf;
    lv_color_t *buf_2_1 = malloc(draw_buf_size);
    lv_color_t *buf_2_2 = malloc(draw_buf_size);
    lv_disp_draw_buf_init(&disp_buf, buf_2_1, buf_2_2, draw_buf_size);

    /*Initialize and register a display driver*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.draw_buf   = &disp_buf;
    disp_drv.flush_cb   = drm_flush;
    disp_drv.hor_res    = lcd_w;
    disp_drv.ver_res    = lcd_h;
    disp_drv.screen_transp = 1;
    lv_disp_drv_register(&disp_drv);
    ```

1. Touch driver:

    ```c
    evdev_init();
    static lv_indev_drv_t indev_drv_1;
    lv_indev_drv_init(&indev_drv_1); /*Basic initialization*/
    indev_drv_1.type = LV_INDEV_TYPE_POINTER;

    /*This function will be called periodically (by the library) to get the mouse position and state*/
    indev_drv_1.read_cb = evdev_read;
    lv_indev_t *mouse_indev = lv_indev_drv_register(&indev_drv_1);
    ```

1. Demo example:

    `lv_demo_widgets();`

For more detailed usage of LVGL, please refer to the LVGL official website: `https://lvgl.io`, API documentation, and examples: `https://docs.lvgl.io/8.3/index.html`.

You can also use LVGL's drag-and-drop UI editor SquareLine Studio to simplify development: `https://squareline.io`.

### Compilation

Execute `make` in the root directory of the SDK to compile everything by default.

### Running lv_demo_widgets

```sh
lvgl_demo_widgets
```

After executing the above command, the configuration interface will be displayed on the LCD screen, and related configurations can be made through the touch screen, as shown below:

![Display Content](../../../zh/02_applications/tutorials/images/lvgl_demo_widgets.png)

Of course, LVGL application development can also be done as an independent project rather than compiled in the SDK. You can refer to the `https://github.com/lvgl/lv_port_linux_frame_buffer` project to replace the porting files from the SDK, then configure the K230 cross-compilation toolchain and the corresponding libdrm reference.
