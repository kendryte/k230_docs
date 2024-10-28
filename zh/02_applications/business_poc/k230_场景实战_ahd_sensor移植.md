# K230 ahd sensor 移植参考

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

本文档主要描述k230 sdk如何适配ahd sensor 和 对应的ahd 转mipi 的芯片使用，本次介绍需要用到的k230 芯片模块比较多、大家可以根据自己的需求做对应的裁剪。

### 模块

本次demo 使用的模块如下：

- vicap ：这个是将接受到的 mipi 输出存储到ddr 当中，mipi 输出的格式是yuv444的。
- 2d ： 这个是格式转换模块，可以将yuv444的图像转换成yuv420、rgb888 plane。
- dw：这个模块是做任意比例缩放。
- gdma ： 这个模块可以进行图像旋转和mirror。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期 |
| --- | --- | --- | --- |
| V1.0 | 初版 | zs | 2024/10/23 |

## 1. ahd sensor介绍

ahd 即Analog High Definition，意思为模拟高清。AHD摄像头即模拟高清摄像头，传输信号为高清模拟信号，本次用的是xs9950 芯片将ahd 转换成mipi。

### 1.1 硬件连接介绍

需要将三路ahd 的sensor 接到xs9950芯片上、每一路的xs9950 分别接到 k230 的三路 mipi 上，需要注意的是iic的引脚电压、xs9950 的复位信号和 pwd 信号是否需要接入到k230中。

### 1.2 rtt kernel 修改介绍

目前在k230 sdk 当中已经有了三路xs9950 的驱动drive，里边的默认配置都是使用720p 25fps 的 ahd sensor 输入，具体的代码在k230_sdk/src/big/mpp/kernel/sensor/src 中，具体的文件如下：

- xs9950_csi0_drv.c
- xs9950_csi1_drv.c
- xs9950_csi2_drv.c

每个driver 对应的是接到mipi 的csi0 和 csi1 和 csi2 三个接口上。driver 的部分修改只需要关注下边几部分，本次以 xs9950_csi0_drv.c 为例：

reset 的 gpio 控制需要改成你接到 k230 的gpio。

```sh
static int xs9950_power_rest(k_s32 on)
{
    #define VICAP_XS9950_RST_GPIO     (0)  //24// 

    kd_pin_mode(VICAP_XS9950_RST_GPIO, GPIO_DM_OUTPUT);

    if (on) {
        kd_pin_write(VICAP_XS9950_RST_GPIO, GPIO_PV_HIGH); // GPIO_PV_LOW  GPIO_PV_HIGH
        rt_thread_mdelay(100);
        kd_pin_write(VICAP_XS9950_RST_GPIO, GPIO_PV_LOW); // GPIO_PV_LOW  GPIO_PV_HIGH
        rt_thread_mdelay(100);
        kd_pin_write(VICAP_XS9950_RST_GPIO, GPIO_PV_HIGH); // GPIO_PV_LOW  GPIO_PV_HIGH
    } else {
        kd_pin_write(VICAP_XS9950_RST_GPIO, GPIO_PV_LOW); // GPIO_PV_LOW  GPIO_PV_HIGH
    }
    rt_thread_mdelay(1);

    return 0;
}
```

iic 的选择需要你连接到k230上对应的iic name。

```sh
struct sensor_driver_dev xs9950_csi0_sensor_drv = {
    .i2c_info = {
        .i2c_bus = NULL,
        .i2c_name = "i2c3",   //"i2c0", //"i2c3",
        .slave_addr = 0x30,
        .reg_addr_size = SENSOR_REG_VALUE_16BIT,
        .reg_val_size = SENSOR_REG_VALUE_8BIT,
    },
    .
    .
}
```

### 1.3 rtt 用户态代码介绍

本次的介绍是三路ahd输入三路显示，具体的pipe 流程如下：
第一路 ：

- vicap（dev0 chn0）-> 2d(dev0 chn0) -> dw (dev0 chn0) -> gdma(dev0 chn0) -> vo(dev0, chn1)

第二路 ：

- vicap（dev1 chn0）-> 2d(dev0 chn1) -> dw (dev1 chn0) -> gdma(dev0 chn1) -> vo(dev0, chn2)

第三路 ：

- vicap（dev2 chn0）-> 2d(dev0 chn2) -> dw (dev2 chn0) -> gdma(dev0 chn2) -> vo(dev0, chn3)

这个的代码比较多、我会按照每个模块的方式做不同的初始化，本次代码流程是三路ahd的720p输入, 通过vicap采集yuv444的图像发送给2d，2d 将yuv444的图像转化成yuv420发送给dw，dw 将图像缩放到640x360 的大小在送给gdma，gdma 旋转90度在推送给屏幕显示，本次的屏幕是采用的720x1280 的屏幕。

所有的宏定义如下：

```sh
#define ISP_CHN0_WIDTH              (1280)
#define ISP_CHN0_HEIGHT             (720)
#define VICAP_OUTPUT_BUF_NUM        10
#define VENC_BUF_NUM                6
#define NONAI_2D_BUF_NUM            6

#define TOTAL_ENABLE_2D_CH_NUMS     6
#define NONAI_2D_RGB_CH             4
#define NONAI_2D_BIND_CH_0          0
#define NONAI_2D_BIND_CH_1          1
#define NONAI_2D_BIND_CH_2          2

#define DW200_CHN0_INPUT_WIDTH 1280
#define DW200_CHN0_INPUT_HEIGHT 720
#define DW200_CHN0_OUTPUT_WIDTH 640 //960
#define DW200_CHN0_OUTPUT_HEIGHT 360//540
#define DW200_CHN0_VB_NUM 4

#define DW200_CHN1_INPUT_WIDTH 1280
#define DW200_CHN1_INPUT_HEIGHT 720
#define DW200_CHN1_OUTPUT_WIDTH 640//960
#define DW200_CHN1_OUTPUT_HEIGHT 360 //540
#define DW200_CHN1_VB_NUM 4

#define DW200_CHN2_INPUT_WIDTH 1280
#define DW200_CHN2_INPUT_HEIGHT 720
#define DW200_CHN2_OUTPUT_WIDTH 640 //960
#define DW200_CHN2_OUTPUT_HEIGHT 360//540
#define DW200_CHN2_VB_NUM 4
#define GDMA_BUF_NUM 6
```

上边主要是定义了一些输出和输入的size和每个模块对应vb大小的定义。

#### 1.3.1 vb

vb 的代码如下：

```sh
static int sample_vb_init(void)
{
    k_s32 ret;
    k_vb_config config;
    k_vb_pool_config pool_config;
    k_vb_supplement_config supplement_config;
    k_u32 pool_id;

    memset(&config, 0, sizeof(config));
    memset(&pool_config, 0, sizeof(pool_config));
    config.max_pool_cnt = 64;

    // for vo install plane data
    config.comm_pool[0].blk_cnt = 5;
    config.comm_pool[0].blk_size = PRIVATE_POLL_SZE;          // osd0 - 3 argb 320 x 240
    config.comm_pool[0].mode = VB_REMAP_MODE_NOCACHE;           //VB_REMAP_MODE_NOCACHE;

    k_u16 sride = ISP_CHN0_WIDTH;
    //VB for YUV444 output for dev0
    config.comm_pool[1].blk_cnt = VICAP_OUTPUT_BUF_NUM;
    config.comm_pool[1].mode = VB_REMAP_MODE_NOCACHE;
    config.comm_pool[1].blk_size = VICAP_ALIGN_UP((sride * ISP_CHN0_HEIGHT * 3), 0x1000);

    //VB for YUV444 output for dev1
    config.comm_pool[2].blk_cnt = VICAP_OUTPUT_BUF_NUM;
    config.comm_pool[2].mode = VB_REMAP_MODE_NOCACHE;
    config.comm_pool[2].blk_size = VICAP_ALIGN_UP((sride * ISP_CHN0_HEIGHT * 3 ), 0x1000);

    //VB for YUV444 output for dev2
    config.comm_pool[3].blk_cnt = VICAP_OUTPUT_BUF_NUM;
    config.comm_pool[3].mode = VB_REMAP_MODE_NOCACHE;
    config.comm_pool[3].blk_size = VICAP_ALIGN_UP((sride * ISP_CHN0_HEIGHT * 3 ), 0x1000);

    //VB for nonai_2d
    config.comm_pool[4].blk_cnt = NONAI_2D_BUF_NUM;
    config.comm_pool[4].mode = VB_REMAP_MODE_NOCACHE;
    config.comm_pool[4].blk_size = VICAP_ALIGN_UP((ISP_CHN0_WIDTH * ISP_CHN0_HEIGHT * 3), 0x1000);

    // DW output vb CHN 0 vb mem = 11,059,200
    config.comm_pool[5].blk_cnt = DW200_CHN0_VB_NUM;
    config.comm_pool[5].blk_size = VICAP_ALIGN_UP((DW200_CHN0_OUTPUT_WIDTH * DW200_CHN0_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[5].mode = VB_REMAP_MODE_NOCACHE;

    config.comm_pool[6].blk_cnt = DW200_CHN1_VB_NUM;
    config.comm_pool[6].blk_size = VICAP_ALIGN_UP((DW200_CHN1_OUTPUT_WIDTH * DW200_CHN1_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[6].mode = VB_REMAP_MODE_NOCACHE;

    config.comm_pool[7].blk_cnt = DW200_CHN2_VB_NUM;
    config.comm_pool[7].blk_size = VICAP_ALIGN_UP((DW200_CHN1_OUTPUT_WIDTH * DW200_CHN1_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[7].mode = VB_REMAP_MODE_NOCACHE;

    // for gdma chn0 
    config.comm_pool[8].blk_cnt = GDMA_BUF_NUM;
    config.comm_pool[8].blk_size = VICAP_ALIGN_UP((DW200_CHN0_OUTPUT_WIDTH * DW200_CHN0_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[8].mode = VB_REMAP_MODE_NOCACHE;

    // for gdma chn 1
    config.comm_pool[9].blk_cnt = GDMA_BUF_NUM;
    config.comm_pool[9].blk_size = VICAP_ALIGN_UP((DW200_CHN1_OUTPUT_WIDTH * DW200_CHN1_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[9].mode = VB_REMAP_MODE_NOCACHE;

     // for gdma chn 1
    config.comm_pool[10].blk_cnt = GDMA_BUF_NUM;
    config.comm_pool[10].blk_size = VICAP_ALIGN_UP((DW200_CHN2_OUTPUT_WIDTH * DW200_CHN2_OUTPUT_HEIGHT * 3), 0x1000);
    config.comm_pool[10].mode = VB_REMAP_MODE_NOCACHE;


    ret = kd_mpi_vb_set_config(&config);
    if (ret) {
        printf("vb_set_config failed ret:%d\n", ret);
        return ret;
    }

    memset(&supplement_config, 0, sizeof(supplement_config));
    supplement_config.supplement_config |= VB_SUPPLEMENT_JPEG_MASK;

    ret = kd_mpi_vb_set_supplement_config(&supplement_config);
    if (ret) {
        printf("vb_set_supplement_config failed ret:%d\n", ret);
        return ret;
    }

    ret = kd_mpi_vb_init();
    if (ret) {
        printf("vb_init failed ret:%d\n", ret);
        return ret;
    }

    memset(&pool_config, 0, sizeof(pool_config));
    pool_config.blk_cnt = PRIVATE_POLL_NUM;
    pool_config.blk_size = PRIVATE_POLL_SZE;
    pool_config.mode = VB_REMAP_MODE_NONE;
    pool_id = kd_mpi_vb_create_pool(&pool_config);          // osd0 - 3 argb 320 x 240

    g_vo_pool_id = pool_id;

    return ret;
}
```

```sh
#define GDMA_BUF_NUM 6
#define DW200_CHN1_VB_NUM 4
#define DW200_CHN0_VB_NUM 4
#define DW200_CHN2_VB_NUM 4
#define NONAI_2D_BUF_NUM            6
#define VICAP_OUTPUT_BUF_NUM        10
```

上边是所有模块的vb 定义，gdma 分配了6个、三路dw 每路分配了4个、三路vicap 每路分配了10个，这个可以根据内存做自己的裁剪、饿哦的这个是1g 的ddr 、所以分配的比较多。如果你裁剪了某个模块，对应的内存可以去掉。

#### 1.3.2 vicap

vicap 代码初始化如下：

```sh
static int sample_vicap_init(k_vicap_dev dev_chn, k_vicap_sensor_type type)
{
    k_vicap_dev vicap_dev;
    k_vicap_chn vicap_chn;
    k_vicap_dev_attr dev_attr;
    k_vicap_chn_attr chn_attr;
    k_vicap_sensor_info sensor_info;
    k_vicap_sensor_type sensor_type;
    k_s32 ret = 0;

    memset(&dev_attr, 0 ,sizeof(dev_attr));
    memset(&chn_attr, 0 ,sizeof(chn_attr));
    memset(&sensor_info, 0 ,sizeof(sensor_info));

    sensor_type = type;
    vicap_dev = dev_chn;

    memset(&sensor_info, 0, sizeof(k_vicap_sensor_info));
    ret = kd_mpi_vicap_get_sensor_info(sensor_type, &sensor_info);
    if (ret) {
        printf("sample_vicap, the sensor type not supported!\n");
        return ret;
    }

    memset(&dev_attr, 0, sizeof(k_vicap_dev_attr));
    dev_attr.acq_win.h_start = 0;
    dev_attr.acq_win.v_start = 0;
    dev_attr.acq_win.width = ISP_CHN0_WIDTH;
    dev_attr.acq_win.height = ISP_CHN0_WIDTH;
    dev_attr.mode = VICAP_WORK_ONLY_MCM_MODE;
    dev_attr.buffer_num = VICAP_OUTPUT_BUF_NUM;
    dev_attr.buffer_size = VICAP_ALIGN_UP((ISP_CHN0_WIDTH * ISP_CHN0_HEIGHT * 3), VICAP_ALIGN_1K);
    dev_attr.pipe_ctrl.data = 0xFFFFFFFF;
    dev_attr.pipe_ctrl.bits.af_enable = 0;
    dev_attr.pipe_ctrl.bits.ahdr_enable = 0;
    dev_attr.dw_enable = K_FALSE;

    dev_attr.cpature_frame = 0;
    memcpy(&dev_attr.sensor_info, &sensor_info, sizeof(k_vicap_sensor_info));

    ret = kd_mpi_vicap_set_dev_attr(vicap_dev, dev_attr);
    if (ret) {
        printf("sample_vicap, kd_mpi_vicap_set_dev_attr failed.\n");
        return ret;
    }

    memset(&chn_attr, 0, sizeof(k_vicap_chn_attr));

    //set chn0 output yuv444
    chn_attr.out_win.h_start = 0;
    chn_attr.out_win.v_start = 0;
    chn_attr.out_win.width = ISP_CHN0_WIDTH;
    chn_attr.out_win.height = ISP_CHN0_HEIGHT;
    chn_attr.crop_win = dev_attr.acq_win;
    chn_attr.scale_win = chn_attr.out_win;
    chn_attr.crop_enable = K_FALSE;
    chn_attr.scale_enable = K_FALSE;
    // chn_attr.dw_enable = K_FALSE;
    chn_attr.chn_enable = K_TRUE;

    chn_attr.pix_format = PIXEL_FORMAT_YUV_SEMIPLANAR_444;
    chn_attr.buffer_size = VICAP_ALIGN_UP((ISP_CHN0_WIDTH * ISP_CHN0_HEIGHT * 3), VICAP_ALIGN_1K);


    chn_attr.buffer_num = VICAP_OUTPUT_BUF_NUM;//at least 3 buffers for isp
    vicap_chn = VICAP_CHN_ID_0;

    // printf("sample_vicap ...kd_mpi_vicap_set_chn_attr, buffer_size[%d]\n", chn_attr.buffer_size);
    ret = kd_mpi_vicap_set_chn_attr(vicap_dev, vicap_chn, chn_attr);
    if (ret) {
        printf("sample_vicap, kd_mpi_vicap_set_chn_attr failed.\n");
        return ret;
    }

    // printf("sample_vicap ...kd_mpi_vicap_init\n");
    ret = kd_mpi_vicap_init(vicap_dev);
    if (ret) {
        printf("sample_vicap, kd_mpi_vicap_init failed.\n");
        return ret;
    }

    return ret;
}
```

这部分是vicap的初始化代码、参数介绍如下：

- dev 的 参数是 VICAP_DEV_ID_0， VICAP_DEV_ID_1， VICAP_DEV_ID_2，
- type 的参数是：XS9950_MIPI_CSI0_1280X720_30FPS_YUV422， XS9950_MIPI_CSI1_1280X720_30FPS_YUV422， XS9950_MIPI_CSI2_1280X720_30FPS_YUV422

参考示例如下，下边的是三路的初始化，你也可以用其中的一路或者两路：

```sh
ret = sample_vicap_init(VICAP_DEV_ID_0, XS9950_MIPI_CSI0_1280X720_30FPS_YUV422);
if(ret < 0)
{
    printf("vicap VICAP_DEV_ID_0 init failed \n");
    goto vicap_init_error;
}

ret = sample_vicap_init(VICAP_DEV_ID_1, XS9950_MIPI_CSI1_1280X720_30FPS_YUV422);
if(ret < 0)
{
    printf("vicap VICAP_DEV_ID_1 init failed \n");
    goto vicap_init_error;
}

ret = sample_vicap_init(VICAP_DEV_ID_2, XS9950_MIPI_CSI2_1280X720_30FPS_YUV422);
if(ret < 0)
{
    printf("vicap VICAP_DEV_ID_2 init failed \n");
    goto vicap_init_error;
}
```

开始或者停止vicap的代码如下：

```sh
static k_s32 sample_vicap_stream(k_vicap_dev vicap_dev, k_bool en)
{
    k_s32 ret = 0;
    if(en)
    {
        ret = kd_mpi_vicap_start_stream(vicap_dev);
        if (ret) {
            printf("sample_vicap, kd_mpi_vicap_start_stream failed.\n");
            return ret;
        }
    }
    else
    {
        ret = kd_mpi_vicap_stop_stream(vicap_dev);
        if (ret) {
            printf("sample_vicap, stop stream failed.\n");
            return ret;
        }
        ret = kd_mpi_vicap_deinit(vicap_dev);
        if (ret) {
            printf("sample_vicap, kd_mpi_vicap_deinit failed.\n");
        }
    }
    return ret;
}
```

参数解释如下：

- vicap_dev 和上边的dev一样
- en ：开 和 关

使用方法如下，这个是开启三路代码

```sh
sample_vicap_stream(VICAP_DEV_ID_0, K_TRUE);
sample_vicap_stream(VICAP_DEV_ID_1, K_TRUE);
sample_vicap_stream(VICAP_DEV_ID_2, K_TRUE);
```

#### 1.3.3 2d

2d 的初始化代码如下，这个是初始化了6路2d、三路用于和bind做显示测的处理，另外三路是用于将yuv444转换成rgb888 plane 去做ai 使用：

```sh
static k_s32 nonai_2d_init()
{
    int i;
    k_s32 ret = 0;
    k_nonai_2d_chn_attr attr_2d;

    for(i = 0; i < TOTAL_ENABLE_2D_CH_NUMS; i++)
    {
        attr_2d.mode = K_NONAI_2D_CALC_MODE_CSC;
        if(i == NONAI_2D_RGB_CH)
        {
            attr_2d.dst_fmt = PIXEL_FORMAT_RGB_888_PLANAR;
        }
        else
        {
            attr_2d.dst_fmt = PIXEL_FORMAT_YUV_SEMIPLANAR_420;
        }
        // kd_mpi_nonai_2d_init(i, &attr_2d);
        ret = kd_mpi_nonai_2d_create_chn(i, &attr_2d);
        if(ret != 0 )
            printf("kd_mpi_nonai_2d_create_chn failed \n");
        // kd_mpi_nonai_2d_start(i);
        ret = kd_mpi_nonai_2d_start_chn(i);
        if(ret != 0 )
            printf("kd_mpi_nonai_2d_start_chn failed \n");
    }

    return K_SUCCESS;
}
```

2d的代码的退出代码如下：

```sh
static k_s32 nonai_2d_exit()
{
    int ret = 0;
    int i;

    for(i = 0; i < TOTAL_ENABLE_2D_CH_NUMS; i++)
    {
        kd_mpi_nonai_2d_stop_chn(i);
        kd_mpi_nonai_2d_destroy_chn(i);
    }

    ret = kd_mpi_nonai_2d_close();
    CHECK_RET(ret, __func__, __LINE__);

    return K_SUCCESS;
}
```

### 1.3.4 gdma

gdma 的初始化代码如下：

```sh
static k_s32 dma_dev_attr_init(void)
{
    k_dma_dev_attr_t dev_attr;

    dev_attr.burst_len = 0;
    dev_attr.ckg_bypass = 0xff;
    dev_attr.outstanding = 7;

    int ret = kd_mpi_dma_set_dev_attr(&dev_attr);
    if (ret != K_SUCCESS)
    {
        printf("set dma dev attr error\r\n");
        return ret;
    }

    ret = kd_mpi_dma_start_dev();
    if (ret != K_SUCCESS)
    {
        printf("start dev error\r\n");
        return ret;
    }

    return ret;
}

static void gdma_init(k_u8 chn, k_u8 rot, k_pixel_format pix, k_u32 width, k_u32 height)
{
    k_u8 gdma_rotation = rot;
    k_pixel_format pix_format = pix;//PIXEL_FORMAT_YVU_SEMIPLANAR_420;
    k_dma_chn_attr_u gdma_attr;
    k_u8 ret = 0;

    memset(&gdma_attr, 0, sizeof(gdma_attr));
    gdma_attr.gdma_attr.buffer_num = 3;//GDMA_BUF_NUM;
    gdma_attr.gdma_attr.rotation = gdma_rotation;
    gdma_attr.gdma_attr.x_mirror = K_FALSE;
    gdma_attr.gdma_attr.y_mirror = K_FALSE;
    gdma_attr.gdma_attr.width = width;
    gdma_attr.gdma_attr.height = height;
    gdma_attr.gdma_attr.work_mode = DMA_BIND;
    gdma_attr.gdma_attr.src_stride[0] = width;
    if (gdma_rotation == DEGREE_180) {
        gdma_attr.gdma_attr.dst_stride[0] = width;
    } else {
        gdma_attr.gdma_attr.dst_stride[0] = height;
    }
    if (pix_format == PIXEL_FORMAT_RGB_888) {
        gdma_attr.gdma_attr.pixel_format = DMA_PIXEL_FORMAT_RGB_888;
        gdma_attr.gdma_attr.src_stride[0] *= 3;
        gdma_attr.gdma_attr.dst_stride[0] *= 3;
    } else {
        gdma_attr.gdma_attr.pixel_format = DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_8BIT;
        gdma_attr.gdma_attr.src_stride[1] = gdma_attr.gdma_attr.src_stride[0];
        gdma_attr.gdma_attr.dst_stride[1] = gdma_attr.gdma_attr.dst_stride[0];
    }

    ret = kd_mpi_dma_set_chn_attr(chn, &gdma_attr);
    if (ret != K_SUCCESS) {
        printf("set chn attr error\r\n");
    }
    ret = kd_mpi_dma_start_chn(chn);
    if (ret != K_SUCCESS) {
        printf("start chn error\r\n");
    }
}
```

参数解释如下：

- chn 通道： 0，1，2，3
- rot ：旋转的格式，0，90，180，360.
- width，输入的宽度， height 输入的高度， pix 输入的数据格式

使用方法如下：

```sh
dma_dev_attr_init();
gdma_init(0, DEGREE_90, PIXEL_FORMAT_YVU_SEMIPLANAR_420, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);
gdma_init(1, DEGREE_90, PIXEL_FORMAT_YVU_SEMIPLANAR_420, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);
gdma_init(2, DEGREE_90, PIXEL_FORMAT_RGB_888, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);
```

首先初始化gdma 的dev、然后在初始化chn，这块需要注意的是第二个参数的格式不要选错了，还有就是你的这个尺寸必须是和你上一级的bind 的尺寸一致，否则就会出问题

退出代码：

```sh
static void gdma_exit(k_u8 gdma_chn)
{
    k_u8 ret = 0 ;
    ret = kd_mpi_dma_stop_chn(gdma_chn);
    if (ret != K_SUCCESS) {
        printf("stop chn error\r\n");
    }

}
```

使用方法如下，下边是三路退出的代码：

```sh
gdma_exit(0);
gdma_exit(1);
gdma_exit(2);
```

### 1.3.5 dw

dw 的初始化代码如下：

```sh
{
    k_s32 ret = 0;
    struct k_dw_settings dw0_settings;
    struct k_dw_settings dw1_settings;
    struct k_dw_settings dw2_settings;

    memset(&dw0_settings, 0, sizeof(struct k_dw_settings));
    memset(&dw1_settings, 0, sizeof(struct k_dw_settings));
    memset(&dw2_settings, 0, sizeof(struct k_dw_settings));

#if DW_DEV0_USE_RGB
    dw0_settings.vdev_id = DEWARP_DEV_ID;
    dw0_settings.input.width = DW200_CHN0_INPUT_WIDTH;
    dw0_settings.input.height = DW200_CHN0_INPUT_HEIGHT;
    dw0_settings.input.format = K_DW_PIX_YUV420SP;
    dw0_settings.input.bit10 = K_FALSE;
    dw0_settings.input.alignment = K_FALSE;
    dw0_settings.output_enable_mask = 1;

    dw0_settings.output[0].width = DW200_CHN0_OUTPUT_WIDTH;
    dw0_settings.output[0].height = DW200_CHN0_OUTPUT_HEIGHT;
    dw0_settings.output[0].format = K_DW_PIX_RGB888;
    dw0_settings.output[0].alignment = 0;
    dw0_settings.output[0].bit10= K_FALSE;
    dw0_settings.crop[0].bottom = 0;
    dw0_settings.crop[0].left = 0;
    dw0_settings.crop[0].right = 0;
    dw0_settings.crop[0].top = 0;
#else
    dw0_settings.vdev_id = DEWARP_DEV_ID;
    dw0_settings.input.width = DW200_CHN0_INPUT_WIDTH;
    dw0_settings.input.height = DW200_CHN0_INPUT_HEIGHT;
    dw0_settings.input.format = K_DW_PIX_YUV420SP;
    dw0_settings.input.bit10 = K_FALSE;
    dw0_settings.input.alignment = K_FALSE;
    dw0_settings.output_enable_mask = 1;

    dw0_settings.output[0].width = DW200_CHN0_OUTPUT_WIDTH;
    dw0_settings.output[0].height = DW200_CHN0_OUTPUT_HEIGHT;
    dw0_settings.output[0].format = K_DW_PIX_YUV420SP;
    dw0_settings.output[0].alignment = 0;
    dw0_settings.output[0].bit10= K_FALSE;
    dw0_settings.crop[0].bottom = 0;
    dw0_settings.crop[0].left = 0;
    dw0_settings.crop[0].right = 0;
    dw0_settings.crop[0].top = 0;
#endif

#if DW_DEV1_USE_RGB
    dw1_settings.vdev_id = DEWARP_DEV_ID + 1;
    dw1_settings.input.width = DW200_CHN1_INPUT_WIDTH;
    dw1_settings.input.height = DW200_CHN1_INPUT_HEIGHT;
    dw1_settings.input.format = K_DW_PIX_YUV420SP;
    dw1_settings.input.bit10 = K_FALSE;
    dw1_settings.input.alignment = K_FALSE;
    dw1_settings.output_enable_mask = 1;

    dw1_settings.output[0].width = DW200_CHN1_OUTPUT_WIDTH;
    dw1_settings.output[0].height = DW200_CHN1_OUTPUT_HEIGHT;
    dw1_settings.output[0].format = K_DW_PIX_RGB888;
    dw1_settings.output[0].alignment = 0;
    dw1_settings.output[0].bit10= K_FALSE;
    dw1_settings.crop[0].bottom = 0;
    dw1_settings.crop[0].left = 0;
    dw1_settings.crop[0].right = 0;
    dw1_settings.crop[0].top = 0;
#else
    dw1_settings.vdev_id = DEWARP_DEV_ID + 1;
    dw1_settings.input.width = DW200_CHN1_INPUT_WIDTH;
    dw1_settings.input.height = DW200_CHN1_INPUT_HEIGHT;
    dw1_settings.input.format = K_DW_PIX_YUV420SP;
    dw1_settings.input.bit10 = K_FALSE;
    dw1_settings.input.alignment = K_FALSE;
    dw1_settings.output_enable_mask = 1;

    dw1_settings.output[0].width = DW200_CHN1_OUTPUT_WIDTH;
    dw1_settings.output[0].height = DW200_CHN1_OUTPUT_HEIGHT;
    dw1_settings.output[0].format = K_DW_PIX_YUV420SP;
    dw1_settings.output[0].alignment = 0;
    dw1_settings.output[0].bit10= K_FALSE;
    dw1_settings.crop[0].bottom = 0;
    dw1_settings.crop[0].left = 0;
    dw1_settings.crop[0].right = 0;
    dw1_settings.crop[0].top = 0;
#endif

    dw2_settings.vdev_id = DEWARP_DEV_ID + 2;
    dw2_settings.input.width = DW200_CHN2_INPUT_WIDTH;
    dw2_settings.input.height = DW200_CHN2_INPUT_HEIGHT;
    dw2_settings.input.format = K_DW_PIX_YUV420SP;
    dw2_settings.input.bit10 = K_FALSE;
    dw2_settings.input.alignment = K_FALSE;
    dw2_settings.output_enable_mask = 1;

    dw2_settings.output[0].width = DW200_CHN2_OUTPUT_WIDTH;
    dw2_settings.output[0].height = DW200_CHN2_OUTPUT_HEIGHT;
    dw2_settings.output[0].format = K_DW_PIX_RGB888;
    dw2_settings.output[0].alignment = 0;
    dw2_settings.output[0].bit10= K_FALSE;
    dw2_settings.crop[0].bottom = 0;
    dw2_settings.crop[0].left = 0;
    dw2_settings.crop[0].right = 0;
    dw2_settings.crop[0].top = 0;

    ret = kd_mpi_dw_init(&dw0_settings);
    if(ret)
    {
        printf("kd_mpi_dw_init init o failed \n");
    }

    ret = kd_mpi_dw_init(&dw1_settings);
    if(ret)
    {
        printf("kd_mpi_dw_init init o failed \n");
    }

    ret = kd_mpi_dw_init(&dw2_settings);
    if(ret)
    {
        printf("kd_mpi_dw_init init o failed \n");
    }

    return ret ;
}
```

上边一共是初始了三路dw 的代码，dw 的功能是将图像缩放、这里边我写了两种数据格式的缩放、一个是输入是yuv、输出是yuv 的，另外一个是输入是yuv、输出是rgb 的。具体的可以看上边的程序。注意如下：

- 输入只需要关注input.width 和 input.height 。
- 输出要关注output[0].width 和 output[0].height 、output[0].format 。
- 这个的初始化必须是在vicap 初始化之后、否则会出问题。

下边的是退出的程序

```sh
static void dw_exit(void)
{
    kd_mpi_dw_exit(DEWARP_DEV_ID);
    kd_mpi_dw_exit(DEWARP_DEV_ID + 1);
    kd_mpi_dw_exit(DEWARP_DEV_ID + 2);
}
```

### 1.3.6 display

display 的初始化主要也是包括两部分、时序的初始化和图层的初始化，具体代码如下

```sh
static k_s32 sample_connector_init(k_connector_type type)
{
    k_u32 ret = 0;
    k_s32 connector_fd;
    k_connector_type connector_type = type;
    k_connector_info connector_info;

    memset(&connector_info, 0, sizeof(k_connector_info));

    //connector get sensor info
    ret = kd_mpi_get_connector_info(connector_type, &connector_info);
    if (ret) {
        printf("sample_vicap, the sensor type not supported!\n");
        return ret;
    }

    connector_fd = kd_mpi_connector_open(connector_info.connector_name);
    if (connector_fd < 0) {
        printf("%s, connector open failed.\n", __func__);
        return K_ERR_VO_NOTREADY;
    }

    // set connect power
    kd_mpi_connector_power_set(connector_fd, K_TRUE);
    // connector init
    kd_mpi_connector_init(connector_fd, connector_info);

    return 0;
}

static void sample_vo_init(k_connector_type type)
{
    osd_info osd;
    layer_info info;

    memset(&info, 0, sizeof(info));
    memset(&osd, 0, sizeof(osd));

    sample_connector_init(type);

#if  DW_DEV0_USE_RGB
         // osd0 init
        osd.act_size.width = DW200_CHN0_OUTPUT_WIDTH ;
        osd.act_size.height = DW200_CHN0_OUTPUT_HEIGHT;
        osd.offset.x = 0;
        osd.offset.y = 0;
        osd.global_alptha = 0xff;// 0x7f;
        osd.format = PIXEL_FORMAT_RGB_888;
        sample_vo_creat_osd_test(K_VO_OSD2, &osd);
#else
        info.act_size.width = DW200_CHN0_OUTPUT_HEIGHT;//DW200_CHN0_OUTPUT_WIDTH ;
        info.act_size.height = DW200_CHN0_OUTPUT_WIDTH;//DW200_CHN0_OUTPUT_HEIGHT;
        info.format = PIXEL_FORMAT_YVU_PLANAR_420;
        info.func = 0;////K_ROTATION_90;
        info.global_alptha = 0xff;
        info.offset.x = 0;//(1080-w)/2,
        info.offset.y = 0;//(1920-h)/2;
        vo_creat_layer_test(K_VO_LAYER1, &info);
#endif
        
#if DW_DEV1_USE_RGB
         // osd0 init
        osd.act_size.width = DW200_CHN1_OUTPUT_WIDTH ;
        osd.act_size.height = DW200_CHN1_OUTPUT_HEIGHT;
        osd.offset.x = DW200_CHN1_OUTPUT_WIDTH ;//960;
        osd.offset.y = 0;
        osd.global_alptha = 0xff;// 0x7f;
        osd.format = PIXEL_FORMAT_RGB_888;
        sample_vo_creat_osd_test(K_VO_OSD1, &osd);
#else
        // layer2 init
        info.act_size.width = DW200_CHN1_OUTPUT_HEIGHT;//DW200_CHN1_OUTPUT_WIDTH ;
        info.act_size.height = DW200_CHN1_OUTPUT_WIDTH; //DW200_CHN1_OUTPUT_HEIGHT;
        info.format = PIXEL_FORMAT_YVU_PLANAR_420;
        info.func = 0;////K_ROTATION_90;
        info.global_alptha = 0xff;
        info.offset.x = DW200_CHN1_OUTPUT_HEIGHT + 50;//(1080-w)/2,
        info.offset.y = 0;//(1920-h)/2;
        vo_creat_layer_test(K_VO_LAYER2, &info);
#endif

         // osd0 init
        osd.act_size.width = DW200_CHN2_OUTPUT_HEIGHT ;
        osd.act_size.height = DW200_CHN2_OUTPUT_WIDTH;
        osd.offset.x = 0;
        osd.offset.y = DW200_CHN2_OUTPUT_WIDTH;//540;
        osd.global_alptha = 0xff;// 0x7f;
        osd.format = PIXEL_FORMAT_RGB_888;
        sample_vo_creat_osd_test(K_VO_OSD0, &osd);

}
```

这块主要是配置显示相关的代码，type 这个参数是已经支持的屏幕或者hdmi 的connector 的type，具体的看k_connector_comm.h 中已经支持的参数，剩下的就是配置图层了、目前显示部分大核支持两个layer（显示yuv）、4个osd（显示rgb），所以三个sensor 的显示采用了配置两个layer 和 一个osd， 最后的那个osd 是用来给ai 画字使用的，不用在这个pipe 中关系。在这里边主要是配置plane的尺寸和位置信息还有格式。

### 1.3.7 bind

这块是大核mpp 最需要关注的一部分，这个的bind 是 保证每个模块走向下一个模块的连接链路，连接的不对整个数据流就全错了。我先介绍一下我目前的三路输出ahd sensor到显示屏幕的流程。

第一路 ：

- vicap（dev0 chn0）-> 2d(dev0 chn0) -> dw (dev0 chn0) -> gdma(dev0 chn0) -> vo(dev0, chn1)

第二路 ：

- vicap（dev1 chn0）-> 2d(dev0 chn1) -> dw (dev1 chn0) -> gdma(dev0 chn1) -> vo(dev0, chn2)

第三路 ：

- vicap（dev2 chn0）-> 2d(dev0 chn2) -> dw (dev2 chn0) -> gdma(dev0 chn2) -> vo(dev0, chn3)

具体的代码如下：

```sh
static void sample_bind()
{
    k_s32 ret;
    k_mpp_chn vi_mpp_chn;
    k_mpp_chn nonai_2d_mpp_chn;
    k_mpp_chn dw_mpp_chn;
    k_mpp_chn vo_mpp_chn;
    k_mpp_chn gdma;

    // pipe 1 
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 0;
    vi_mpp_chn.chn_id = 0;

    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = NONAI_2D_BIND_CH_0;
    ret = kd_mpi_sys_bind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 0;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_bind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 0;
    ret = kd_mpi_sys_bind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = K_VO_LAYER1;
    ret = kd_mpi_sys_bind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    // pipe 2 
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 1;
    vi_mpp_chn.chn_id = 0;
    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = 1;
    ret = kd_mpi_sys_bind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 1;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_bind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 1;
    ret = kd_mpi_sys_bind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = K_VO_LAYER2;
    ret = kd_mpi_sys_bind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

     // pipe 3
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 2;
    vi_mpp_chn.chn_id = 0;
    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = 2;
    ret = kd_mpi_sys_bind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 2;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_bind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 2;
    ret = kd_mpi_sys_bind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = 3;
    ret = kd_mpi_sys_bind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    return;
}
```

这个带啊吗写的很清楚每一极的流程，谁和谁做的bind，每个设备都有自己的dev 和 chn 。解bind 流程和bind 的流程一样

```sh
static void sample_unbind()
{
    k_s32 ret;
    k_mpp_chn vi_mpp_chn;
    k_mpp_chn nonai_2d_mpp_chn;
    k_mpp_chn dw_mpp_chn;
    k_mpp_chn vo_mpp_chn;
    k_mpp_chn gdma;

    // pipe 1 
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 0;
    vi_mpp_chn.chn_id = 0;

    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = NONAI_2D_BIND_CH_0;
    ret = kd_mpi_sys_unbind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 0;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_unbind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 0;
    ret = kd_mpi_sys_unbind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = K_VO_LAYER1;
    ret = kd_mpi_sys_unbind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    // pipe 2 
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 1;
    vi_mpp_chn.chn_id = 0;
    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = 1;
    ret = kd_mpi_sys_unbind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 1;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_unbind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 1;
    ret = kd_mpi_sys_unbind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = K_VO_LAYER2;
    ret = kd_mpi_sys_unbind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

     // pipe 3
    vi_mpp_chn.mod_id = K_ID_VI;
    vi_mpp_chn.dev_id = 2;
    vi_mpp_chn.chn_id = 0;

    nonai_2d_mpp_chn.mod_id = K_ID_NONAI_2D;
    nonai_2d_mpp_chn.dev_id = 0;
    nonai_2d_mpp_chn.chn_id = 2;
    ret = kd_mpi_sys_unbind(&vi_mpp_chn, &nonai_2d_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    dw_mpp_chn.mod_id = K_ID_DW200;
    dw_mpp_chn.dev_id = 2;
    dw_mpp_chn.chn_id = 0;
    ret = kd_mpi_sys_unbind(&nonai_2d_mpp_chn, &dw_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    gdma.mod_id = K_ID_DMA;
    gdma.dev_id = 0;
    gdma.chn_id = 2;
    ret = kd_mpi_sys_unbind(&dw_mpp_chn, &gdma);
    CHECK_RET(ret, __func__, __LINE__);

    vo_mpp_chn.mod_id = K_ID_VO;
    vo_mpp_chn.dev_id = 0;
    vo_mpp_chn.chn_id = 3;
    ret = kd_mpi_sys_unbind(&gdma, &vo_mpp_chn);
    CHECK_RET(ret, __func__, __LINE__);

    return;
}
```

需要注意先关掉每个模块之后在去做解绑。在这块不用哪个模块只需要将哪个模块在bind 当中去掉即可，比如去掉dw ，就可以2d 和 下一级的gdma 做bind ，但是就需要修改gdma 的 size 和数据格式了。

### 1.3.8 main

上边已经讲完了所有的模块和每个模块的初始化，下边就是main的讲解了，代码如下

```sh
int main(int argc, char *argv[])
{
    int ret;
    k_video_frame_info dump_info;
    k_video_frame_info rgb_vf_info;

    // vb init
    ret = sample_vb_init();
    if(ret) {
        goto vb_init_error;
    }

    // vo init
    sample_vo_init(ILI9881C_MIPI_4LAN_800X1280_60FPS);

    // init 2d 
    nonai_2d_init();

    // init bind 
    sample_bind();

    dma_dev_attr_init();
    gdma_init(0, DEGREE_90, PIXEL_FORMAT_YVU_SEMIPLANAR_420, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);
    gdma_init(1, DEGREE_90, PIXEL_FORMAT_YVU_SEMIPLANAR_420, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);
    gdma_init(2, DEGREE_90, PIXEL_FORMAT_RGB_888, DW200_CHN0_OUTPUT_WIDTH, DW200_CHN0_OUTPUT_HEIGHT);

    // three mcm init
    ret = sample_vicap_init(VICAP_DEV_ID_0, XS9950_MIPI_CSI0_1280X720_30FPS_YUV422);
    if(ret < 0)
    {
        printf("vicap VICAP_DEV_ID_0 init failed \n");
        goto vicap_init_error;
    }

    ret = sample_vicap_init(VICAP_DEV_ID_1, XS9950_MIPI_CSI1_1280X720_30FPS_YUV422);
    if(ret < 0)
    {
        printf("vicap VICAP_DEV_ID_1 init failed \n");
        goto vicap_init_error;
    }

    ret = sample_vicap_init(VICAP_DEV_ID_2, XS9950_MIPI_CSI2_1280X720_30FPS_YUV422);
    if(ret < 0)
    {
        printf("vicap VICAP_DEV_ID_2 init failed \n");
        goto vicap_init_error;
    }

    sample_dw200_init();

    sample_vicap_stream(VICAP_DEV_ID_0, K_TRUE);
    sample_vicap_stream(VICAP_DEV_ID_1, K_TRUE);
    sample_vicap_stream(VICAP_DEV_ID_2, K_TRUE);


    while(exit_flag != 1)
    {
        memset(&dump_info, 0 , sizeof(k_video_frame_info));
        memset(&rgb_vf_info, 0 , sizeof(k_video_frame_info));
        ret = kd_mpi_vicap_dump_frame(VICAP_DEV_ID_0, VICAP_CHN_ID_0, VICAP_DUMP_YUV444, &dump_info, 300);
        if (ret)
        {
            printf("sample_vicap...kd_mpi_vicap_dump_frame failed.\n");
            continue;
        }

        ret = kd_mpi_nonai_2d_send_frame(NONAI_2D_RGB_CH, &dump_info, 1000);
        if (ret)
        {
            printf("sensor 0：kd_mpi_nonai_2d_send_frame ch 4 failed. %d\n", ret);
            ret = kd_mpi_vicap_dump_release(VICAP_DEV_ID_0, VICAP_CHN_ID_0, &dump_info);
            if (ret)
            {
                printf("sensor 0：sample_vicap...kd_mpi_vicap_dump_release failed.\n");
                continue;
            }
        }


        ret = kd_mpi_nonai_2d_get_frame(NONAI_2D_RGB_CH, &rgb_vf_info, 1000);
        if (ret)
        {
            printf("sensor 0：kd_mpi_nonai_2d_get_frame ch 4 failed. %d\n", ret);
            // goto vicap_release;
            ret = kd_mpi_vicap_dump_release(VICAP_DEV_ID_0, VICAP_CHN_ID_0, &dump_info);
            if (ret)
            {
                printf("sensor 0：sample_vicap...kd_mpi_vicap_dump_release failed.\n");
                continue;
            }
        }

        // todo ai 

        ret = kd_mpi_nonai_2d_release_frame(NONAI_2D_RGB_CH, &rgb_vf_info);
        if (ret) {
            printf("sensor 0：kd_mpi_nonai_2d_release_frame ch 4 failed. %d\n", ret);
        }

        ret = kd_mpi_vicap_dump_release(VICAP_DEV_ID_0, VICAP_CHN_ID_0, &dump_info);
        if (ret) {
            printf("sample_vicap...kd_mpi_vicap_dump_release failed.\n");
        }
    }


    sample_vicap_stream(VICAP_DEV_ID_0 , K_FALSE);
    sample_vicap_stream(VICAP_DEV_ID_1 , K_FALSE);
    sample_vicap_stream(VICAP_DEV_ID_2 , K_FALSE); 


    usleep(1000 * 34);

    nonai_2d_exit();

    dw_exit();

    gdma_exit(0);
    gdma_exit(1);

    kd_mpi_vo_disable_video_layer(K_VO_LAYER1);
    kd_mpi_vo_disable_video_layer(K_VO_LAYER2);

    sample_unbind();

    ret = kd_mpi_vb_exit();
    if (ret) {
        printf("fastboot_app, kd_mpi_vb_exit failed.\n");
        return ret;
    }

    return 0;

vicap_init_error:
    for(int i = 0; i < VICAP_DEV_ID_MAX; i++)
    {
        sample_vicap_stream(VICAP_DEV_ID_0 + i, K_FALSE);
    }

vb_init_error:
    return 0;
}
```

while 之前是所有模块的初始话和start、这个需要注意将所有的模块都配置完成之后才可以调用vicap start。在while中的代码完全是为了做ai 使用的，dump 一帧vcaip 的数据、通过2d 转换成rgb888 plane 格式、给ai 做识别、然后再将2d 和vicap 给release 掉即可，最后边就是退出了，整体的代码详见 k230_sdk/src/big/mpp/userapps/sample/ahd_sensor/ 目录。

## 1.4 测试

上边已经讲解完成了所有代码相关的函数，运行只需要将编译好的文件直接执行就行

## 1.5 注意事项

- 第一个就是注意上一级传过来的图像尺寸和数据格式和当前模块对应的尺寸和数据格式是否一致、因为这块做个很多尺寸的变换、比如gdma 的旋转，dw 的缩放都是做了尺寸的改变，2d 的yuv444转换成yuv420，dw 将yuv420 转换成 rgb888 ，如果配置的格式不对和尺寸不对、后边的整个显示都是错误的
- 第二个就是vb 大小和数量，每个模块用的尺寸可能不一样、可以根据不同的尺寸和数据格式计算出大小来申请vb，如果系统的内存不够、就得注意这个问题、根据实验找到一个可以运行的最小子集
- 第三个就是必须先初始化vicap、在初始化dw、在启动vicap 这样的流程，否则会出现dw 运行不正常的问题
- 用户态的线程优先级设置不可以配置比内核的优先级大、因为rtt 的 线程优先级和内核的优先级采用的是一套系统，最好用户的优先级设置25以上（用户态的线程优先级默认是25）
- 目前的显示模式是将三路ahd 都缩放显示到vo 中，这个也可以做原图和缩放图切换的功能，这个的做法是先断掉 2d 和 后边的bind ，deinit 后边的模块， 从新配置后边的模块、然后在bind 。
- vo 更换屏幕只需要更换connector 支持的type 就可以，但是需要注意你配置的图层的尺寸和位置不要超过屏幕的最大尺寸，否则显示会有问题
