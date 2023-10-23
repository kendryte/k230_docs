# K230 Camera Sensor适配指南

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

本文档主要描述K230平台Camera Sensor框架以及如何新增支持一款新的Camera Sensor。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
| ---- | ---- |
|      |      |
|      |      |

### 修订记录

| 文档版本号 | 修改说明  | 修改者 | 日期  |
|---|---|---|---|
| V1.0       | 初版 | 汪成根 | 2023-05-30 |
|            |          |        |            |
|            |          |        |            |

## 1. 概述

本文档主要描述K230平台Camera Sensor基本框架以及如何新增支持一款新的Camera Sensor。

K230平台支持多种接口类型的sensor，我们以当前最常用的MIPI CSI接口Sensor为例进行说明。Sensor与主控平台的硬件连接示意图如下：

![camera sensor连接示意图](images/e20100e34c268ad615e69966cb28e5a6.png)

主控通过I2C接口下发配置寄存器控制sensor的工作方式，sensor通过MIPI CSI接口将图像数据发送至主控SOC。

## 2. Camera Sensor框架

### 2.1 框架简介

Camera Sensor框架如图2-1所示，最底层是sensor驱动层

![camera sensor框架](images/camera_sensor_arch.png)

图2-1 camera sensor框架

从上到下依次是：媒体接口层，驱动层以及硬件层

- 媒体接口层：该层对上提供kd_mpi_sensor_xxx接口给外部模块操作和访问sensor设备，对下通过ioctl操作具体的sensor设备
- 驱动层：该层包括sensor公共操作接口具体的sensor设备驱动。公共操作接口主要是ioctl操作命令和sensor i2c读写接口，sensor驱动主要提供设备节点以及操作接口的实现。这部分也是sensor适配的主要工作。
- 硬件层：对应各个具体的sensor硬件

## 3. Sensor适配准备工作

用户在适配新的sensor之前需要做以下一些准备工作：

1. 从正规渠道获取 Sensor datasheet、初始化序列。
1. 查看 Sensor datasheet 和相关应用手册，特别关注 Sensor 曝光、增益控制方法，不同模式下曝光和增益的限制，长曝光实现方法，黑电平值，bayer 数据输出顺序等。
1. 跟 Sensor 厂家索要所需模式初始化序列，了解各序列的数据数率，Sensor 输出总的宽高，精确的帧率是多少等。
1. 确认 Sensor 控制接口是 I2C、SPI 还是其他接口，Sensor 的设备地址可以通过硬件设置。对于多个摄像头的场景，sensor 尽量不要复用 I2C 总线。不同场景的Sensor IO 电平可能是 1.8V 或者 3.3V，设计时需要保保证 sensor 的 IO 电平与SOC 对应的 GPIO 供电电压一致。如 sensor 电平是 1.8V，则用于 sensor 控制的GPIO，如 Reset，I2C，PRDN，需要使用 1.8V 供电。
1. 确认 Sensor 输出数据接口和协议类型。当前仅支持MIPI CSI接口。
1. 确认 wdr mode 是 VC、DT 或者 DOL 等。
1. 确认不同时序是否需要图像裁剪。

## 4. Sensor适配示例

本节将按照如何增加支持一个新的camera sensor的步骤来进行详细描述。

这里以ov9732驱动作为示例进行说明，对应的驱动文件源码路径如下：

```shell
src/big/mpp/kernel/sensor/src/ov9732_drv.c
```

### 4.1 定义支持的sensor类型

系统支持的Sensor类型是由如下枚举变量定义：

```c
typedef enum {
    OV_OV9732_MIPI_1280X720_30FPS_10BIT_LINEAR = 0,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_IR = 1,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_SPECKLE = 2,

    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_IR = 3,
    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_SPECKLE = 4,

    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_IR_SPECKLE = 5,
    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_IR_SPECKLE  = 6,

    IMX335_MIPI_2LANE_RAW12_1920X1080_30FPS_LINEAR = 7,
    IMX335_MIPI_2LANE_RAW12_2592X1944_30FPS_LINEAR = 8,
    IMX335_MIPI_4LANE_RAW12_2592X1944_30FPS_LINEAR = 9,
    IMX335_MIPI_2LANE_RAW12_1920X1080_30FPS_MCLK_7425_LINEAR = 10,
    IMX335_MIPI_2LANE_RAW12_2592X1944_30FPS_MCLK_7425_LINEAR = 11,
    IMX335_MIPI_4LANE_RAW12_2592X1944_30FPS_MCLK_7425_LINEAR = 12,

    IMX335_MIPI_4LANE_RAW10_2XDOL = 13,
    IMX335_MIPI_4LANE_RAW10_3XDOL = 14,

    SC_SC035HGS_MIPI_1LANE_RAW10_640X480_120FPS_LINEAR = 15,
    SC_SC035HGS_MIPI_1LANE_RAW10_640X480_60FPS_LINEAR = 16,
    SC_SC035HGS_MIPI_1LANE_RAW10_640X480_30FPS_LINEAR = 17,

    OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_SPECKLE = 18,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_IR = 19,
    OV_OV9732_MIPI_1280X720_30FPS_10BIT_MCLK_16M_LINEAR = 20,

    OV_OV5647_MIPI_1920X1080_30FPS_10BIT_LINEAR = 21,
    OV_OV5647_MIPI_2592x1944_10FPS_10BIT_LINEAR = 22,
    OV_OV5647_MIPI_640x480_60FPS_10BIT_LINEAR = 23,
    OV_OV5647_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR = 24,

    SC_SC201CS_MIPI_1LANE_RAW10_1600X1200_30FPS_LINEAR = 25,
    SC_SC201CS_SLAVE_MODE_MIPI_1LANE_RAW10_1600X1200_30FPS_LINEAR = 26,
} k_vicap_sensor_type;
```

用户需要增加新的sensor支持类型时，首先需要在这里增加对应类型的定义，**该类型是应用程序获取sensor配置的唯一标志**

### 4.2 sensor驱动适配

sensor驱动适配在整个环节中最重要的环节，用户可以通过拷贝现有的sensor驱动文件来修改，其中关于sensor的AE相关寄存器配置和计算方式需要查看对应的手册或者寻求专业人事协助。

#### 4.2.1 定义sensor寄存器配置列表

sensor寄存器配置由数据类型 k_sensor_reg_list 定义：

```c
typedef struct {
    k_u16 reg_addr;
    k_u8  reg_val;
} k_sensor_reg_list;
```

以下是ov9732的寄存器配置列表

```c
static k_sensor_reg_list ov9732_mipi2lane_720p_30fps_linear[] = {
    {0x0103, 0x01},
    {0x0100, 0x00},

    ......

    {0x400b, 0xc0},
    {REG_NULL, 0x00},
};
```

#### 4.2.2 定义sensor支持的模式

sensor的模式参数由数据类型k_sensor_mode 定义

```c
typedef struct {
    k_u32 index;
    k_vicap_sensor_type sensor_type;
    k_sensor_size size;
    k_u32 fps;
    k_u32 hdr_mode;
    k_u32 stitching_mode;
    k_u32 bit_width;
    k_sensor_data_compress compress;
    k_u32 bayer_pattern;
    k_sensor_mipi_info mipi_info;
    k_sensor_ae_info ae_info;
    k_sensor_reg_list *reg_list;
} k_sensor_mode;
```

以下是ov9732的支持的模式

```c
static k_sensor_mode ov9732_mode_info[] = {
    ......

    {
        .index = 2,
        .sensor_type = OV_OV9732_MIPI_1280X720_30FPS_10BIT_LINEAR,
        .size = {
            .bounds_width = 1280,
            .bounds_height = 720,
            .top = 0,
            .left = 0,
            .width = 1280,
            .height = 720,
        },
        .fps = 30000,
        .hdr_mode = SENSOR_MODE_LINEAR,
        .bit_width = 10,
        .bayer_pattern = BAYER_BGGR,
        .mipi_info = {
            .csi_id = 0,
            .mipi_lanes = 1,
            .data_type = 0x2B, //RAW10
        },
        .reg_list = ov9732_mipi2lane_720p_30fps_linear,
    },

}
```

#### 4.2.3 实现sensor操作接口

sensor的操作接口由数据类型k_sensor_function定义，用户根据实际情况实现相关的操作接口，不是所有接口都必须实现。

```c
typedef struct {
    k_s32 (*sensor_power) (void *ctx, k_s32 on);
    k_s32 (*sensor_init) (void *ctx, k_sensor_mode mode);
    k_s32 (*sensor_get_chip_id)(void *ctx, k_u32 *chip_id);
    k_s32 (*sensor_get_mode)(void *ctx, k_sensor_mode *mode);
    k_s32 (*sensor_set_mode)(void *ctx, k_sensor_mode mode);
    k_s32 (*sensor_enum_mode)(void *ctx, k_sensor_enum_mode *enum_mode);
    k_s32 (*sensor_get_caps)(void *ctx, k_sensor_caps *caps);
    k_s32 (*sensor_conn_check)(void *ctx, k_s32 *conn);
    k_s32 (*sensor_set_stream)(void *ctx, k_s32 enable);
    k_s32 (*sensor_get_again)(void *ctx, k_sensor_gain *gain);
    k_s32 (*sensor_set_again)(void *ctx, k_sensor_gain gain);
    k_s32 (*sensor_get_dgain)(void *ctx, k_sensor_gain *gain);
    k_s32 (*sensor_set_dgain)(void *ctx, k_sensor_gain gain);
    k_s32 (*sensor_get_intg_time)(void *ctx, k_sensor_intg_time *time);
    k_s32 (*sensor_set_intg_time)(void *ctx, k_sensor_intg_time time);
    k_s32 (*sensor_get_exp_parm)(void *ctx, k_sensor_exposure_param *exp_parm);
    k_s32 (*sensor_set_exp_parm)(void *ctx, k_sensor_exposure_param exp_parm);
    k_s32 (*sensor_get_fps)(void *ctx, k_u32 *fps);
    k_s32 (*sensor_set_fps)(void *ctx, k_u32 fps);
    k_s32 (*sensor_get_isp_status)(void *ctx, k_sensor_isp_status *staus);
    k_s32 (*sensor_set_blc)(void *ctx, k_sensor_blc blc);
    k_s32 (*sensor_set_wb)(void *ctx, k_sensor_white_balance wb);
    k_s32 (*sensor_get_tpg)(void *ctx, k_sensor_test_pattern *tpg);
    k_s32 (*sensor_set_tpg)(void *ctx, k_sensor_test_pattern tpg);
    k_s32 (*sensor_get_expand_curve)(void *ctx, k_sensor_compand_curve *curve);
    k_s32 (*sensor_get_otp_data)(void *ctx, void *data);
} k_sensor_function;
```

以下是ov9732的支持的模式

```c
    .sensor_func = {
        .sensor_power = ov9732_sensor_power_on,
        .sensor_init = ov9732_sensor_init,
        .sensor_get_chip_id = ov9732_sensor_get_chip_id,
        .sensor_get_mode = ov9732_sensor_get_mode,
        .sensor_set_mode = ov9732_sensor_set_mode,
        .sensor_enum_mode = ov9732_sensor_enum_mode,
        .sensor_get_caps = ov9732_sensor_get_caps,
        .sensor_conn_check = ov9732_sensor_conn_check,
        .sensor_set_stream = ov9732_sensor_set_stream,
        .sensor_get_again = ov9732_sensor_get_again,
        .sensor_set_again = ov9732_sensor_set_again,
        .sensor_get_dgain = ov9732_sensor_get_dgain,
        .sensor_set_dgain = ov9732_sensor_set_dgain,
        .sensor_get_intg_time = ov9732_sensor_get_intg_time,
        .sensor_set_intg_time = ov9732_sensor_set_intg_time,
        .sensor_get_exp_parm = ov9732_sensor_get_exp_parm,
        .sensor_set_exp_parm = ov9732_sensor_set_exp_parm,
        .sensor_get_fps = ov9732_sensor_get_fps,
        .sensor_set_fps = ov9732_sensor_set_fps,
        .sensor_get_isp_status = ov9732_sensor_get_isp_status,
        .sensor_set_blc = ov9732_sensor_set_blc,
        .sensor_set_wb = ov9732_sensor_set_wb,
        .sensor_get_tpg = ov9732_sensor_get_tpg,
        .sensor_set_tpg = ov9732_sensor_set_tpg,
        .sensor_get_expand_curve = ov9732_sensor_get_expand_curve,
        .sensor_get_otp_data = ov9732_sensor_get_otp_data,
    },
```

#### 4.2.4 定义sensor驱动结构体

sensor驱动结构体由 struct sensor_driver_dev 定义，主要包括sensor I2C配置信息，sensor驱动名称以及sensor操作集合

```c
struct sensor_driver_dev {
    k_sensor_i2c_info i2c_info;
    k_u8 *sensor_name;
    k_sensor_function sensor_func;
    k_sensor_mode *sensor_mode;
    k_sensor_ae_info ae_info;
    k_s32 pwd_gpio;
    k_s32 reset_gpio;
};
```

ov9732驱动结构体定义及初始化内容如下：

```c
struct sensor_driver_dev ov9732_sensor_drv = {
    .i2c_info = {
        .i2c_bus = NULL,
        .i2c_name = "i2c1",
        .slave_addr = 0x36,
    },
    .sensor_name = "ov9732",
    .sensor_func = {
        .sensor_power = ov9732_sensor_power_on,
        .sensor_init = ov9732_sensor_init,
        .sensor_get_chip_id = ov9732_sensor_get_chip_id,
        .sensor_get_mode = ov9732_sensor_get_mode,
        .sensor_set_mode = ov9732_sensor_set_mode,
        ......
    },
};
```

#### 4.2.5 更新sensor驱动列表

将上一节定义的sensor驱动结构体添加到sensor_drv_list数组中。
当前系统支持的sensor列表如下：

```c
struct sensor_driver_dev *sensor_drv_list[] = {
    &ov9732_sensor_drv,
    &ov9286_sensor_drv,
    &imx335_sensor_drv,
};
```

### 4.3 更新sensor配置信息列表

sensor配置信息有结构体k_vicap_sensor_info定义：

```shell
typedef struct {
    const char *sensor_name; /*sensor名字*/
    const char *calib_file; /*sensor标定文件名*/
    k_u16 width; /*sensor输出图像宽度*/
    k_u16 height; /*sensor输出图像高度*/
    k_vicap_csi_num csi_num; /*sensor硬件连接使用的CSI总线标号*/
    k_vicap_mipi_lanes mipi_lanes; /*sensor硬件连接使用的MIPI LANE个数*/
    k_vicap_data_source source_id; /*数据源ID*/
    k_bool is_3d_sensor; /*是否为3D sensor*/

    k_vicap_mipi_phy_freq phy_freq; /*MIPI PHY速率*/
    k_vicap_csi_data_type data_type; /*CSI数据类型*/
    k_vicap_hdr_mode hdr_mode; /*HDR模式*/
    k_vicap_vi_flash_mode flash_mode; /*flash模式选择*/
    k_vicap_vi_first_frame_sel first_frame;
    k_u16 glitch_filter;
    k_vicap_sensor_type sensor_type; /*sensor类型*/
} k_vicap_sensor_info;
```

以下是ov9732对应的配置信息：

```shell
const k_vicap_sensor_info sensor_info_list[] = {
    {
        "ov9732",
        "ov9732",
        1920,
        1080,
        VICAP_CSI0,
        VICAP_MIPI_1LANE,
        VICAP_SOURCE_CSI0,
        K_FALSE,
        VICAP_MIPI_PHY_800M,
        VICAP_CSI_DATA_TYPE_RAW10,
        VICAP_LINERA_MODE,
        VICAP_FLASH_DISABLE,
        VICAP_VI_FIRST_FRAME_FS_TR0,
        0,
        OV_OV9732_MIPI_1920X1080_30FPS_10BIT_LINEAR
    },
```

用户每增加一个sensor配置模式，就需要在sensor_info_list这个结构体中增加一项对应模式的配置。

### 4.4 增加sensor配置文件

当前SDK版本sensor配置文件包括xml文件和json文件，文件存放路径如下：

```shell
src/big/mpp/userapps/src/sensor/config/
```

以下是ov9732对应的配置文件：

```shell
ov9732.xml  ov9732_auto.json  ov9732_manual.json
```

对于新增加的sensor，可以通过拷贝修改现有文件实现支持，其中的calibration和tuning参数可以通过相关工具修改导出。
