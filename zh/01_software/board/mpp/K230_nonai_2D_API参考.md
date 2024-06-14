# K230 nonai 2D API参考

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

### 概述

本文档主要介绍视频编解码模块的功能和用法。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称     | 说明                |
| -------- | ------------------- |
| CSC      | color space convert |
| VENC     | 视频编解码模块      |

### 修订记录

| 文档版本号 | 修改者 | 日期 | 修改说明 |
|---|---|---|---|
| V1.0       | 系统软件部 | 2024.02.02 | 初版  |
|            |            |            |          |

## 1. 概述

### 1.1 概述

nonai 2D硬件能实现OSD，画框和CSC功能，OSD和画框作为VENC的子模块，本文仅仅描述CSC功能。

### 1.2 功能描述

实现RGB和YUV的相互转换

## 2. API参考

- [kd_mpi_nonai_2d_create_chn](#21-kd_mpi_nonai_2d_create_chn)
- [kd_mpi_nonai_2d_destroy_chn](#22-kd_mpi_nonai_2d_destory_chn)
- [kd_mpi_nonai_2d_start_chn](#23-kd_mpi_nonai_2d_start_chn)
- [kd_mpi_nonai_2d_stop_chn](#24-kd_mpi_nonai_2d_stop_chn)
- [kd_mpi_nonai_2d_get_frame](#25-kd_mpi_nonai_2d_get_frame)
- [kd_mpi_nonai_2d_release_frame](#26-kd_mpi_nonai_2d_release_frame)
- [kd_mpi_nonai_2d_send_frame](#27-kd_mpi_nonai_2d_send_frame)

### 2.1 kd_mpi_nonai_2d_create_chn

【描述】

创建通道。

【语法】

```c
k_s32 kd_mpi_nonai_2d_create_chn(k_u32 chn_num, const k_nonai_2d_chn_attr *attr);
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| chn_num  | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入      |
| attr     | 通道属性指针。                                                   | 输入      |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

无。

【举例】

无。

【相关主题】

无。

### 2.2 kd_mpi_nonai_2d_destory_chn

【描述】

销毁通道。

【语法】

```c
k_s32 kd_mpi_nonai_2d_destory_chn(k_u32 chn_num);
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| chn_num  | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入      |

【返回值】

| 返回值 | 描述                          |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 销毁前必须停止接收图像，否则返回失败。

【举例】

无。

【相关主题】

### 2.3 kd_mpi_nonai_2d_start_chn

【描述】

开启接收输入图像。

【语法】

```c
k_s32 kd_mpi_nonai_2d_start_chn(k_u32 chn_num);
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| chn_num | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 如果通道未创建，则返回失败K_ERR_NONAI_2D_UNEXIST。
- 如果通道已经开始接收图像，没有停止接收图像前再一次调用此接口指定接收帧数，返回操作不允许。
- 只有开启接收之后才开始处理帧。

【举例】

无。

【相关主题】

### 2.4 kd_mpi_nonai_2d_stop_chn

【描述】

停止接收输入图像。

【语法】

```c
k_s32 kd_mpi_nonai_2d_stop_chn(k_u32 chn_num);
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| chn_num | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 如果通道未创建，则返回失败。
- 此接口并不判断当前是否停止接收，即允许重复停止接收不返回错误。
- 此接口用于停止接收图像，在通道销毁或复位前必须停止接收图像。
- 调用此接口仅停止接收原始数据，frame buffer并不会被清除。

【举例】

无。

【相关主题】

### 2.5 kd_mpi_nonai_2d_get_frame

【描述】

获取处理后的图像。

【语法】

```c
k_s32 kd_mpi_nonai_2d_get_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

【参数】

| 参数名称  | 描述 | 输入/输出 |
|---|---|---|
| chn_num | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入 |
| frame    | 图像结构体指针. | 输出 |
| milli_sec | 获取图像超时时间。 取值范围： [-1, +∞ ) -1：阻塞。 0：非阻塞。 大于0：超时时间 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 如果通道未创建，返回失败。
- 如果frame为空，返回K_ERR_NONAI_2D_NULL_PTR。
- 如果milli_sec小于-1，返回K_ERR_NONAI_2D_ILLEGAL_PARAM。

【举例】

无。

【相关主题】

### 2.6 kd_mpi_nonai_2d_release_frame

【描述】

释放图像缓存。

【语法】

```c
k_s32 kd_mpi_nonai_2d_release_frame(k_u32 chn_num, k_video_frame_info *frame);
```

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| chn_num  | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入 |
| frame   | 图像结构体指针。 | 输出 |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 如果通道未创建，则返回错误码K_ERR_NONAI_2D_UNEXIST。
- 如果frame为空，则返回错误码K_ERR_NONAI_2D_NULL_PTR。

【举例】

无。

【相关主题】

### 2.7 kd_mpi_nonai_2d_send_frame

【描述】

支持用户发送原始图像进行。

【语法】

```c
k_s32 kd_mpi_nonai_2d_send_frame(k_u32 chn_num, k_video_frame_info *frame, k_s32 milli_sec);
```

【参数】

| 参数名称  | 描述 | 输入/输出 |
|---|---|---|
| chn_num | 通道号。 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS]。 | 输入 |
| frame | 原始图像信息结构指针，参考《K230 系统控制 API参考》。 | 输入 |
| milli_sec | 发送图像超时时间。 取值范围： [-1,+∞ ) -1：阻塞。 0：非阻塞。 \> 0：超时时间。 | 输入 |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败，参见[错误码](#5-错误码)。 |

【芯片差异】

无。

【需求】

- 头文件：mpi_nonai_2d_api.h，k_type.h，k_module.h，k_sys_comm.h，k_nonai_2d_comm.h
- 库文件：libvenc.a

【注意】

- 此接口支持用户发送图像至通道。
- 如果milli_sec小于-1，返回K_ERR_NONAI_2D_ILLEGAL_PARAM。
- 调用该接口发送图像，用户需要保证通道已创建且开启接收输入图像。

【举例】

无。

【相关主题】

## 3. 数据类型

该功能模块的相关数据类型定义如下：

### 3.1 K_NONAI_2D_MAX_CHN_NUMS

【说明】

定义最大通道个数。

【定义】

```c
#define K_NONAI_2D_MAX_CHN_NUMS  24
```

【注意事项】

无。

【相关数据类型及接口】

无。

### 3.2 k_nonai_2d_calc_mode

【说明】

定义通道码率控制器模式。

【定义】

```c
typedef enum
{
​     K_NONAI_2D_CALC_MODE_CSC = 0,    /* Color space conversion */
​     K_NONAI_2D_CALC_MODE_OSD,      /* On Screen Display */
​     K_NONAI_2D_CALC_MODE_BORDER,     /* Draw border */
​     K_NONAI_2D_CALC_MODE_OSD_BORDER,   /* OSD first, then draw border */
​     K_NONAI_2D_CALC_MODE_BUTT
} k_nonai_2d_calc_mode;
```

【成员】

【注意事项】

目前仅仅支持CSC模式

【相关数据类型及接口】

无。

### 3.3 k_nonai_2d_chn_attr

【说明】

定义通道属性。

【定义】

```c
typedef struct
{
​      k_pixel_format dst_fmt;     /* Format of output image */
​      k_nonai_2d_calc_mode mode;
} k_nonai_2d_chn_attr;
```

【成员】

| 成员名称 | 描述                  |
| -------- | --------------------- |
| dst_fmt  | 输出图像的格式        |
| mode     | 2D计算模式，见3.2章节 |

【注意事项】

【相关数据类型及接口】

无。

### 3.4 k_nonai_2d_color_gamut

【说明】

定义CSC的颜色类型，默认是BT601

【定义】

```c
typedef enum
{
​     NONAI_2D_COLOR_GAMUT_BT601 = 0,
​     NONAI_2D_COLOR_GAMUT_BT709,
​     NONAI_2D_COLOR_GAMUT_BT2020,
​     NONAI_2D_COLOR_GAMUT_BUTT
} k_nonai_2d_color_gamut;
```

【成员】

【注意事项】

【相关数据类型及接口】

无。

## 4. MAPI

### 4.1概述

MAPI是在小核调用，用以创建nonai_2d通道。

### 4.2 API

- [kd_mpi_nonai_2d_init](#421-kd_mapi_nonai_2d_init)
- [kd_mpi_nonai_2d_deinit](#422-kd_mapi_nonai_2d_deinit)
- [kd_mpi_nonai_2d_start](#423-kd_mapi_nonai_2d_start)
- [kd_mpi_nonai_2d_stop](#424-kd_mapi_nonai_2d_stop)

#### 4.2.1 kd_mapi_nonai_2d_init

【描述】

初始化通道。

【语法】

```c
k_s32 kd_mapi_nonai_2d_init(k_u32 chn_num, k_nonai_2d_chn_attr * attr)
```

【参数】

| 参数名称          | 描述                                                   | 输入/输出 |
| ----------------- | ------------------------------------------------------ | --------- |
| chn_num           | NONAI_2D 通道号 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS] | 输入      |
| pst_nonai_2d_attr | NONAI_2D 通道属性指针。 静态属性。                     | 输入      |

【返回值】

| 返回值 | 描述               |
|--------|--------------------|
| 0      | 成功               |
| 非0    | 失败，其值为错误码 |

【芯片差异】

无 。

【需求】

头文件：mapi_nonai_2d_api.h、k_nonai_2d_comm.h
库文件：libmapi.a libipcmsg.a libdatafifo.a

【注意】

- 调用该接口前需要先初始化kd_mapi_sys_init ()和kd_mapi_media_init ()成功，详见“SYS MAPI”章节。
- 重复初始化返回成功

【举例】

【相关主题】

#### 4.2.2 kd_mapi_nonai_2d_deinit

【描述】

通道去初始化。

【语法】

```c
k_s32 kd_mapi_nonai_2d_deinit(k_u32 chn_num)
```

【参数】

| 参数名称 | 描述                                                   | 输入/输出 |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D 通道号 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS] | 输入      |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功                          |
| 非0    | 失败，其值为[错误码](#5-错误码) |

【芯片差异】

无 。

【需求】

头文件：mapi_nonai_2d_api.h、k_nonai_2d_comm.h
库文件：libmapi.a libipcmsg.a libdatafifo.a

【注意】

无。

【举例】

无。

【相关主题】

#### 4.2.3 kd_mapi_nonai_2d_start

【描述】

启动通道。

【语法】

```c
k_s32 kd_mapi_nonai_2d_start(k_s32 chn_num);
```

【参数】

| 参数名称 | 描述                                                   | 输入/输出 |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D 通道号 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS] | 输入      |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功                          |
| 非0    | 失败，其值为[错误码](#5-错误码) |

【芯片差异】

无 。

【需求】

头文件：mapi_nonai_2d_api.h、k_nonai_2d_comm.h
库文件：libmapi.a libipcmsg.a libdatafifo.a

【注意】

【举例】

无。

【相关主题】

#### 4.2.4 kd_mapi_nonai_2d_stop

【描述】

停止通道。

【语法】

```c
k_s32 kd_mapi_nonai_2d_stop(k_s32 chn_num);
```

【参数】

| 参数名称 | 描述                                                   | 输入/输出 |
| -------- | ------------------------------------------------------ | --------- |
| chn_num  | NONAI_2D 通道号 取值范围：[0, K_NONAI_2D_MAX_CHN_NUMS] | 输入      |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功                          |
| 非0    | 失败，其值为[错误码](#5-错误码) |

【芯片差异】

无。

【需求】

头文件：mapi_nonai_2d_api.h、k_nonai_2d_comm.h
库文件：libmapi.a libipcmsg.a libdatafifo.a

【注意】

无。

【举例】

无。

【相关主题】

## 5. 错误码

表 41  API 错误码
| 错误代码   | 宏定义                       | 描述                                         |
| ---------- | ---------------------------- | -------------------------------------------- |
| 0xa0098001 | K_ERR_NONAI_2D_INVALID_DEVID | 设备ID超出合法范围                           |
| 0xa0098002 | K_ERR_NONAI_2D_INVALID_CHNID | 通道ID超出合法范围                           |
| 0xa0098003 | K_ERR_NONAI_2D_ILLEGAL_PARAM | 参数超出合法范围                             |
| 0xa0098004 | K_ERR_NONAI_2D_EXIST         | 试图申请或者创建已经存在的设备、通道或者资源 |
| 0xa0098005 | K_ERR_NONAI_2D_UNEXIST       | 试图使用或者销毁不存在的设备、通道或者资源   |
| 0xa0098006 | K_ERR_NONAI_2D_NULL_PTR      | 函数参数中有空指针                           |
| 0xa0098007 | K_ERR_NONAI_2D_NOT_CONFIG    | 使用前未配置                                 |
| 0xa0098008 | K_ERR_NONAI_2D_NOT_SUPPORT   | 不支持的参数或者功能                         |
| 0xa0098009 | K_ERR_NONAI_2D_NOT_PERM      | 该操作不允许，如试图修改静态配置参数         |
| 0xa009800c | K_ERR_NONAI_2D_NOMEM         | 分配内存失败，如系统内存不足                 |
| 0xa009800d | K_ERR_NONAI_2D_NOBUF         | 分配缓存失败，如申请的数据缓冲区太大         |
| 0xa009800e | K_ERR_NONAI_2D_BUF_EMPTY     | 缓冲区中无数据                               |
| 0xa009800f | K_ERR_NONAI_2D_BUF_FULL      | 缓冲区中数据满                               |
| 0xa0098010 | K_ERR_NONAI_2D_NOTREADY      | 系统没有初始化或没有加载相应模块             |
| 0xa0098011 | K_ERR_NONAI_2D_BADADDR       | 地址超出合法范围                             |
| 0xa0098012 | K_ERR_NONAI_2D_BUSY          | NONAI_2D系统忙                               |

## 6. 调试信息

多媒体内存管理和和系统绑定调试信息，请参考《K230 系统控制 API参考》。
