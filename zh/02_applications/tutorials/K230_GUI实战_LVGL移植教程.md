# K230 GUI实战 - LVGL移植教程

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| --- | --- |
| DRM | Direct Rendering Manager |
| KMS | Kernel Mode Setting
| GUI | Graphical User Interface

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期 |
| --- | --- | --- | --- |
| V1.0 | 初版 | 王权 | 2023/06/25 |

## K230 GUI实战

LVGL是流行的免费开源嵌入式图形库，可以用于嵌入式系统的图形用户界面(GUI)开发。

### 硬件环境

- K230-USIP-LP3-EVB-V1.1
- 配套的LCD模组

### 概述

k230使用DRM作为显示驱动，DRM(Direct Rendering Manager) 是 Linux 内核中的一个子系统，相比过时的Framebuffer 可以支持复杂的 GPU 操作，如硬件加速的图形渲染。lvgl可以基于libdrm提供的接口进行GUI的绘制。

SDK中已经移植好lvgl组件，且默认编译了一个可以运行的demo，位于`/usr/bin/lvgl_demo_widgets`。开机后在小核linux终端输入命令`lvgl_demo_widgets`回车即可体验。

### lvgl源码位置

SDK中已经包含移植好的lvgl，路径位于`src/little/buildroot-ext/package/lvgl`。在SDK的buildroot编译过程中会将源码放置于目录`output/k230_evb_defconfig/little/buildroot-ext/build/lvgl-v8.3.7`下，该目录包含了从github拉取的lvgl源码包以及前面所说的src路径下的移植文件。目录结构如下：

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

### lvgl的DRM驱动

linux内核中DRM驱动加载成功后会出现以下节点`/dev/dri/card0`。

#### DRM配置相关

在头文件`src/little/buildroot-ext/package/lvgl/port_src/lv_drv_conf.h`中

- 配置宏定义`define USE_DRM 1`来使能DRM显示驱动  
- 配置宏定义`define DRM_CARD  "/dev/dri/card0"`指定DRM驱动节点

#### DRM驱动源码具体介绍
  
lvgl的drm驱动程序位于`src/little/buildroot-ext/package/lvgl/port_src/lv_drivers/display/drm.c`。
对DRM的操作需要先open该文件节点。  
lvgl使用中主要用到以下几个函数：

- drm_init()        drm初始化。
- drm_get_sizes()   获取显示器分辨率信息。
- drm_flush()       显示绘制回调接口。

drm初始化过程中会自动获取DRM的资源，包括获知connect id, plane id, crtc id等，会根据配置文件中选定的颜色格式自动匹配对应支持的plane。

该drm驱动默认开启了双buffer，但目前在没有硬件加速的情况下，双缓冲刷新率低，可以注释掉下面代码以单缓冲方式刷新，显示效果会更好：

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

### lvgl的使用

lvgl的主程序文件位于`src/little/buildroot-ext/package/lvgl/port_src/main.c`

#### lvgl配置相关

lvgl配置文件位于：`src/little/buildroot-ext/package/lvgl/port_src/lv_conf.h`

以下是几个常用的配置项:

- `#define LV_COLOR_DEPTH 32`           设置颜色深度
- `#define LV_COLOR_SCREEN_TRANSP 1`    设置屏幕透明
- `#define LV_DPI_DEF 300`              设置屏幕DPI
- `#define LV_USE_PERF_MONITOR 1`       显示fps以及cpu占用率，用于调试
- `#define LV_USE_MEM_MONITOR 1`        显示内存占用，用于调试
- `#define LV_USE_DEMO_WIDGETS  1`      启用lvgl widgets demo

#### lvgl使用的主要步骤

1. LVGL初始化:

    `lv_init();`

1. 显示驱动初始化:

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

1. 触摸驱动：

    ``` c
    evdev_init();
    static lv_indev_drv_t indev_drv_1;
    lv_indev_drv_init(&indev_drv_1); /*Basic initialization*/
    indev_drv_1.type = LV_INDEV_TYPE_POINTER;

    /*This function will be called periodically (by the library) to get the mouse position and state*/
    indev_drv_1.read_cb = evdev_read;
    lv_indev_t *mouse_indev = lv_indev_drv_register(&indev_drv_1);
    ```

1. demo例程:

    `lv_demo_widgets();`

关于lvgl更详细的用法请参考lvgl官网:`https://lvgl.io`，API文档以及例程：`https://docs.lvgl.io/8.3/index.html`。

也可以使用lvgl的拖放式UI编辑器SquareLine Studio来简化开发:`https://squareline.io`。

### 编译

在SDK根目录下执行`make`默认全部编译。

### 运行lv_demo_widgets

 ```sh
lvgl_demo_widgets
 ```

执行完上述命令，会在LCD屏幕上显示配置界面，可以通过触摸屏进行相关配置，具体如下所示：

![显示内容](images/lvgl_demo_widgets.png)

当然lvgl应用程序开发也可以作为一个独立项目而不是在SDK中进行编译，可以参考`https://github.com/lvgl/lv_port_linux_frame_buffer`项目将SDK中的移植文件替换进去，然后配置K230的交叉编译工具链以及对应libdrm引用即可。
