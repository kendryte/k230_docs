# K230 GUI in Action - LVGL Porting Tutorial

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Reader object

This document is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate |
| --- | --- |
| DRM | Direct Rendering Manager |
| KMS | Kernel Mode Setting
| GUI | Graphical User Interface

### Revision history

| Document version number | Modify the description | Author | date |
| --- | --- | --- | --- |
| V1.0 | Initial edition | Author | 2023/06/25 |

## K230 GUI in action

LVGL is a popular free and open source embedded graphics library that can be used for graphical user interface (GUI) development of embedded systems.

### Hardware environment

- K230-USIP-LP3-EVB-V1.1
- LCD screen

### Overview

The k230 uses DRM as a display driver, DRM (Direct Rendering Manager) is a subsystem in the Linux kernel that can support complex GPU operations such as hardware-accelerated graphics rendering compared to the outdated Framebuffer. lvgl can draw GUIs based on the interface provided by libdrm.

The lvgl component has been ported to the SDK, and a runnable demo has been compiled by default, which is /usr/bin/lvgl_demo_widgets.

### LVGL source location

The SDK already contains the ported LVGL at the path src/little/buildroot-ext/package/lvgl. during the buildroot compilation of the SDK, the source code will be placed in a directory output/k230_evb_defconfig/little/buildroot-ext/build/lvgl-v8.3.7 that contains the lvgl source code package pulled from GitHub and the ported files under the src path mentioned above. The directory structure is as follows:

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

### lvgl DRM driver

After the DRM driver in the Linux kernel is successfully loaded, the following device nodes will appear /dev/dri/card0.

#### DRM configuration related

in the header file src/little/buildroot-ext/package/lvgl/port_src/lv_drv_conf.h

- Configure macro definitions to enable DRM display drivers

    `define USE_DRM 1`

- The configuration macro definition specifies the DRM driver node

    `define DRM_CARD  "/dev/dri/card0"`

#### Specific introduction to DRM driver source code

LVGL's DRM driver is located src/little/buildroot-ext/package/lvgl/port_src/lv_drivers/display/drm.c
to operate on DRM, you need to open the file node first.
The following functions are mainly used in the use of LVGL:

- drm_init() DRM initialization.
- drm_get_sizes() to get monitor resolution information.
- drm_flush() displays the drawing callback interface.

DRM resources will be automatically obtained during the drm initialization process, including connect id, plane id, crtc id, etc., and will automatically match the corresponding supported plane according to the color format selected in the configuration file.

The DRM driver has double buffer enabled by default, but in the absence of hardware acceleration, the double buffer refresh rate is low, you can comment out the following code to refresh in single buffering, the display effect will be better:

``` c
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

### Use of LVGL

LVGL's main program file is located at: src/little/buildroot-ext/package/lvgl/port_src/main.c

#### LVGL configuration related

The LVGL configuration file is located at: src/little/buildroot-ext/package/lvgl/port_src/lv_conf.h

The following are a few commonly used configuration items:

| Macro | description |
| --- | --- |
| #define LV_COLOR_DEPTH 32 | Set the color depth |
| #define LV_COLOR_SCREEN_TRANSP 1 | Set screen transparency |
| #define LV_DPI_DEF 300 | Set the screen DPI |
| #define LV_USE_PERF_MONITOR 1 | Displays FPS and CPU usage for debugging |
| #define LV_USE_MEM_MONITOR 1 | Displays memory usage for debugging |
| #define LV_USE_DEMO_WIDGETS  1 | compile lvgl widgets demo |

#### The main steps used by LVGL

1. LVGL initialization:

    `lv_init();`

1. Display driver initialization:

    ``` c
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

1. Touch Drive:

    ``` c
    evdev_init();
    static lv_indev_drv_t indev_drv_1;
    lv_indev_drv_init(&indev_drv_1); /*Basic initialization*/
    indev_drv_1.type = LV_INDEV_TYPE_POINTER;

    /*This function will be called periodically (by the library) to get the mouse position and state*/
    indev_drv_1.read_cb = evdev_read;
    lv_indev_t *mouse_indev = lv_indev_drv_register(&indev_drv_1);
    ```

1. Demo routine:

    `lv_demo_widgets();`

For more detailed usage of lvgl, please refer to the lvgl website <https://lvgl.io>,
API documentation and examples: <https://docs.lvgl.io/8.3/index.html>

It is also possible to use LVGL's drag-and-drop UI editor, SquareLine Studio, to simplify development: <https://squareline.io>

### compile

Perform default compilation all in the root directory of the SDK make.

### Run lv_demo_widgets

 ```sh
lvgl_demo_widgets
 ```

After executing the above command, the configuration interface will be displayed on the LCD screen, and the relevant configuration can be made through the touch screen, as follows:

![Display content](../../../zh/02_applications/tutorials/images/lvgl_demo_widgets.png)

Of course, lvgl application development can also be compiled as a standalone project instead of in the SDK, you can refer to the <https://github.com/lvgl/lv_port_linux_frame_buffer> project to replace the port files in the SDK, and then configure the K230 cross-compilation toolchain and the corresponding libdrm reference.
