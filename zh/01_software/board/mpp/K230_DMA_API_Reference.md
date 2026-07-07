# K230 DMA API参考

## 概述

### 概述

GSDMA：DMA 全称 Direct Memory Access，即直接存储器访问，将数据从一个地址空间复制到另一个地址空间，提供在存储器和存储器之间的高速数据传输。GDMA 全称 Graphic Direct Memory Access，负责将内存中的图像复制到另一块内存中，同时可以完成图像的旋转和镜像等功能。SDMA 全称 System Direct Memory Access，负责将内存中的数据复制到另一块内存中，即传统意义上的 DMA。

软件代码将 GSDMA 硬件的各个功能以 API 的方式提供给使用者使用，帮助用户快速实现图像传输、旋转、镜像、2D 功能及数据传输功能。同时实现了模块状态信息统计等功能。

### 功能描述

将 dma 硬件抽象为一个设备，八个通道，其中，通道 0\~3 是 gdma 通道，通道 4\~7 是 sdma 通道。

#### gdma

用户通过 gdma 来实现图像的旋转镜像工作，主要调用流程如下：

1. 进行 dma 设备属性的配置；
1. 启动 dma 设备。在调用此函数以后驱动会自动申请 VB 空间作为目的地址的数据缓冲区；
1. 进行 gdma 通道属性的配置；
1. 启动 gdma 通道；
1. 用户在用户态申请 VB 空间作为源数据的数据缓冲区，调用 kd_mpi_dma_send_frame 发送数据的源地址给 gdma；
1. 驱动会将源地址中的数据传输到步骤二中申请的目的地址数据缓冲区中；
1. 用户调用 kd_mpi_dma_get_frame 获取目的地址中的数据地址。

#### sdma

用户通过 sdma 来实现数据搬移工作，主要调用流程如下：

1. 进行 dma 设备属性的配置；
1. 启动 dma 设备。在调用此函数以后驱动会自动申请 VB 空间作为目的地址的数据缓冲区；
1. 进行 sdma 通道属性的配置；
1. 启动 sdma 通道；
1. 用户在用户态申请 VB 空间作为源数据的数据缓冲区，调用 kd_mpi_dma_send_frame 发送数据的源地址给 sdma；
1. 驱动会将源地址中的数据传输到步骤二中申请的目的地址数据缓冲区中；
1. 用户调用 kd_mpi_dma_get_frame 获取目的地址中的数据地址。

## API 参考

### DMA 使用

该功能模块提供以下API：

- [kd_mpi_dma_set_dev_attr](#kd_mpi_dma_set_dev_attr)
- [kd_mpi_dma_get_dev_attr](#kd_mpi_dma_get_dev_attr)
- [kd_mpi_dma_start_dev](#kd_mpi_dma_start_dev)
- [kd_mpi_dma_stop_dev](#kd_mpi_dma_stop_dev)
- [kd_mpi_dma_set_chn_attr](#kd_mpi_dma_set_chn_attr)
- [kd_mpi_dma_get_chn_attr](#kd_mpi_dma_get_chn_attr)
- [kd_mpi_dma_start_chn](#kd_mpi_dma_start_chn)
- [kd_mpi_dma_stop_chn](#kd_mpi_dma_stop_chn)
- [kd_mpi_dma_send_frame](#kd_mpi_dma_send_frame)
- [kd_mpi_dma_get_frame](#kd_mpi_dma_get_frame)
- [kd_mpi_dma_release_frame](#kd_mpi_dma_release_frame)

#### kd_mpi_dma_set_dev_attr

【描述】

配置 dma 设备属性

【语法】

k_s32 kd_mpi_dma_set_dev_attr(k_dma_dev_attr_t \*attr);

【参数】

| 参数名称 | 描述                      | 输入/输出 |
|----------|---------------------------|-----------|
| attr     | dma 设备属性结构体指针。  | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无。

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

无

【举例】

无

【相关主题】

[k_dma_dev_attr_t](#k_dma_dev_attr_t)

#### kd_mpi_dma_get_dev_attr

【描述】

获取已经配置的 dma 设备属性。

【语法】

k_s32 kd_mpi_dma_get_dev_attr(k_dma_dev_attr_t \*attr);

【参数】

| 参数名称 | 描述                   | 输入/输出 |
|----------|------------------------|-----------|
| attr     | dma 设备属性结构体指针 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

需要在配置 dma 设备属性之后才可以获取 dma 设备属性。

【举例】

无

【相关主题】

[k_dma_dev_attr_t](#k_dma_dev_attr_t)

#### kd_mpi_dma_start_dev

【描述】

启动 dma 设备。

【语法】

k_s32 kd_mpi_dma_start_dev();

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|------|-----------|
| 无       | 无   | 无        |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 需要配置 dma 设备属性之后才可以调用此函数启动 dma

【举例】

无

【相关主题】

无

#### kd_mpi_dma_stop_dev

【描述】

停止 dma 设备。

【语法】

kd_mpi_dma_stop_dev();

【参数】

| 参数名称 | 描述 | 输入/输出 |
|----------|------|-----------|
| 无       | 无   | 无        |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 只有启动 dma 设备之后才可以调用此函数来停止 dma 设备。

【举例】

无

【相关主题】

无

#### kd_mpi_dma_set_chn_attr

【描述】

配置 dma 通道属性。

【语法】

k_s32 kd_mpi_dma_set_chn_attr(k_u8 chn_num, k_dma_chn_attr_u \*attr);

【参数】

| 参数名称 | 描述                                                                                                                             | 输入/输出 |
|----------|----------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | 通道号                                                                                                                           | 输入      |
| attr     | dma 通道属性，该参数是一个联合体，可以选择配置 gdma 通道属性，也可以选择配置 sdma 通道属性。通道 0\~3 是 gdma，通道 4\~7 是 sdma | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

无

【举例】

无

【相关主题】

[k_dma_chn_attr_u](#k_dma_chn_attr_u)

#### kd_mpi_dma_get_chn_attr

【描述】

获取已经配置的 dma 通道属性。

【语法】

k_s32 kd_mpi_dma_get_chn_attr(k_u8 chn_num, k_dma_chn_attr_u \*attr);

【参数】

| 参数名称 | 描述                                                                                                                             | 输入/输出 |
|----------|----------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | 通道号                                                                                                                           | 输入      |
| attr     | dma 通道属性，该参数是一个联合体，可以选择获取 gdma 通道属性，也可以选择获取 sdma 通道属性。通道 0\~3 是 gdma，通道 4\~7 是 sdma | 输出      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 需要在配置 dma 通道属性之后才可以获取 dma 通道属性。

【举例】

无

【相关主题】

[k_dma_chn_attr_u](#k_dma_chn_attr_u)

#### kd_mpi_dma_start_chn

【描述】

启动 dma 通道。

【语法】

k_s32 kd_mpi_dma_start_chn(k_u8 chn_num);

【参数】

| 参数名称 | 描述     | 输入/输出 |
|----------|----------|-----------|
| chn_num  | 通道号。 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 只有在配置启动 dma 设备，配置 dma 通道属性之后才可以启动 dma 通道。

【举例】

无

【相关主题】

无

#### kd_mpi_dma_stop_chn

【描述】

暂停 dma 通道

【语法】

k_s32 kd_mpi_dma_stop_chn(k_u8 chn_num);

【参数】

| 参数名称 | 描述     | 输入/输出 |
|----------|----------|-----------|
| chn_num  | 通道号。 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 只有启动 dma 通道之后才可以调用此函数来停止 dma 通道。

【举例】

无

【相关主题】

无

#### kd_mpi_dma_send_frame

【描述】

从用户空间发送数据到目的地址。

【语法】

k_s32 kd_mpi_dma_send_frame(k_u8 chn_num, k_video_frame_info \*df_info, k_s32 millisec);

【参数】

| 参数名称 | 描述                                                                                                                                                                  | 输入/输出 |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | 通道号。                                                                                                                                                              | 输入      |
| df_info  | 发送数据的地址信息。                                                                                                                                                  | 输入      |
| millisec | 等待时间。 当此参数设置为 -1 时，阻塞； 当此参数设置为 0 时，非阻塞； 当此参数设置为大于 0 的值时，会等待相应时间直到成功发送数据，如果超时后仍未成功发送，返回失败。 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

无

【举例】

无

【相关主题】

[k_video_frame_info](#k_video_frame_info)

#### kd_mpi_dma_get_frame

【描述】

获取 dma 搬运后的数据。

【语法】

k_s32 kd_mpi_dma_get_frame(k_u8 chn_num, k_video_frame_info \*df_info, k_s32 millisec);

【参数】

| 参数名称 | 描述                                                                                                                                                                  | 输入/输出 |
|----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| chn_num  | 通道号。                                                                                                                                                              | 输入      |
| df_info  | 获取数据的地址信息。                                                                                                                                                  | 输出      |
| millisec | 等待时间。 当此参数设置为 -1 时，阻塞； 当此参数设置为 0 时，非阻塞； 当此参数设置为大于 0 的值时，会等待相应时间知道成功获取数据，如果超时后仍未成功发送，返回失败。 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

无

【举例】

无

【相关主题】

[k_video_frame_info](#k_video_frame_info)

#### kd_mpi_dma_release_frame

【描述】

释放获取的 dma 数据。

【语法】

k_s32 kd_mpi_dma_release_frame(k_u8 chn_num, k_video_frame_info \*df_info);

【参数】

| 参数名称 | 描述           | 输入/输出 |
|----------|----------------|-----------|
| chn_num  | 通道号。       | 输入      |
| df_info  | 要释放的数据。 | 输入      |

【返回值】

| 返回值 | 描述                 |
|--------|----------------------|
| 0      | 成功                 |
| 非0    | 失败，其值参见错误码 |

【芯片差异】

无

【需求】

- 头文件：mpi_dma_api.h
- 库文件：libdma.a

【注意】

- 当前设计中 dma 输出 buffer 为 3，如果获取 3 帧数据都没有调用此函数进行释放，那么无法继续输入数据。因此，用户应该在获取数据，使用完之后及时释放。

【举例】

无

【相关主题】

[k_video_frame_info](#k_video_frame_info)

## 数据类型

### 公共数据类型

#### DMA_MAX_DEV_NUMS

【说明】

DMA 最大设备数

【定义】

```c
#define DMA_MAX_DEV_NUMS (1)
```

【注意事项】

无

【相关数据类型及接口】

无

#### DMA_MAX_CHN_NUMS

【说明】

DMA 最大通道数

【定义】

\#define DMA_MAX_CHN_NUMS (8)

【注意事项】

无

【相关数据类型及接口】

无

#### k_dma_mode_e

【说明】

定义 dma 工作模式。

【定义】

```c
typedef enum
{
    DMA_BIND,
    DMA_UNBIND,
} k_dma_mode_e;
```

【成员】

| 成员名称 | 描述       |
|----------|------------|
| BIND     | 绑定模式。 |
| UNBIND   | 非绑定模式 |

【注意事项】

无

【相关数据类型及接口】

[k_gdma_chn_attr_t](#k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#k_sdma_chn_attr_t)

#### k_dma_dev_attr_t

【说明】

定义 dma 设备属性。

【定义】

```c
typedef struct
{
    k_u8 burst_len;
    k_u8 outstanding;
    k_bool ckg_bypass;
} k_dma_dev_attr_t;
```

【成员】

| 成员名称    | 描述                     |
|-------------|--------------------------|
| burst_len   | 配置 dma 的 burst length |
| outstanding | 配置 dma outstanding     |
| ckg_bypass  | 配置 clock gate bypass   |

【注意事项】

无

【相关数据类型及接口】

[kd_mpi_dma_set_dev_attr](#kd_mpi_dma_set_dev_attr)
[kd_mpi_dma_get_dev_attr](#kd_mpi_dma_get_dev_attr)

#### k_dma_chn_attr_u

【说明】

定义 dma 通道属性。

【定义】

```c
typedef union
{
    k_gdma_chn_attr_t gdma_attr;
    k_sdma_chn_attr_t sdma_attr;
} k_dma_chn_attr_u;
```

【成员】

| 成员名称   | 描述                   |
|------------|------------------------|
| gdma_attr  | gdma 通道属性          |
| sdma_attr  | sdma 通道属性          |
| ckg_bypass | 配置 clock gate bypass |

【注意事项】

无

【相关数据类型及接口】

[k_gdma_chn_attr_t](#k_gdma_chn_attr_t)
[k_sdma_chn_attr_t](#k_sdma_chn_attr_t)
[kd_mpi_dma_set_chn_attr](#kd_mpi_dma_set_chn_attr)
[kd_mpi_dma_get_chn_attr](#kd_mpi_dma_get_chn_attr)

#### k_video_frame_info

【说明】

定义 dma 数据地址。

【定义】

```c
typedef struct
{
    k_video_frame v_frame;  /**< Video picture frame */
    k_u32 pool_id;          /**< VB pool ID */
    k_mod_id mod_id;        /**< Logical unit for generating video frames */
} k_video_frame_info;
```

【成员】

| 成员名称 | 描述                     |
|----------|--------------------------|
| v_frame  | 时间戳，绑定模式下有效。 |
| pool_id  | 数据 vb 池的 pool id。   |
| mod_id   | 模块 id                  |

【注意事项】

无

【相关数据类型及接口】

[kd_mpi_dma_send_frame](#kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#kd_mpi_dma_get_frame)
[kd_mpi_dma_release_frame](#kd_mpi_dma_release_frame)

#### k_video_frame

【说明】

定义 dma 数据地址。使用公用的数据结构 k_video_frame，只使用到了其中的一部分成员。

【定义】

```c
typedef struct
{
    k_u64 phys_addr[3];
    k_u64 virt_addr[3];
    k_u32 time_ref;
    k_u64 pts;
} k_video_frame;
```

【成员】

| 成员名称  | 描述                                                                                                                                         |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------|
| phys_addr | 图像的物理地址，如果是单通道图像，只需配置第一个物理地址；如果是双通道图像，只需配置前两个物理地址；如果是三通道图像，需要配置三个物理地址。 |
| virt_addr | 图像的虚拟地址，如果是单通道图像，只需配置第一个虚拟地址；如果是双通道图像，只需配置前两个虚拟地址；如果是三通道图像，需要配置三个虚拟地址。 |
| time_ref  | 透传的帧号，在绑定模式下，由前级输入                                                                                                         |
| pts       | 透传的时间戳，在绑定模式下，由前级输入                                                                                                       |

【注意事项】

无

【相关数据类型及接口】

[kd_mpi_dma_send_frame](#kd_mpi_dma_send_frame)
[kd_mpi_dma_get_frame](#kd_mpi_dma_get_frame)

### gdma 通道数据类型

该模块有如下数据类型

- [GDMA_MAX_CHN_NUMS](#gdma_max_chn_nums)
- [k_gdma_rotation_e](#k_gdma_rotation_e)
- [k_pixel_format_dma_e](#k_pixel_format_dma_e)
- [k_gdma_chn_attr_t](#k_gdma_chn_attr_t)

#### GDMA_MAX_CHN_NUMS

【说明】

GDMA 最大通道数

【定义】

```c
define GDMA_MAX_CHN_NUMS (4)
```

【注意事项】

无

【相关数据类型及接口】

无

#### k_gdma_rotation_e

【说明】

定义 gdma 通道旋转角度。

【定义】

```c
typedef enum
{
    DEGREE_0,       /**< Rotate 0 degrees */
    DEGREE_90,      /**< Rotate 90 degrees */
    DEGREE_180,     /**< Rotate 180 degrees */
    DEGREE_270,     /**< Rotate 270 degrees */
} k_gdma_rotation_e;
```

【注意事项】

无

【相关数据类型及接口】

[k_gdma_chn_attr_t](#k_gdma_chn_attr_t)

#### k_pixel_format_dma_e

【说明】

定义 gdma 图像格式。

【定义】

```c
typedef enum
{
    DMA_PIXEL_FORMAT_RGB_444 = 0,
    DMA_PIXEL_FORMAT_RGB_555,
    DMA_PIXEL_FORMAT_RGB_565,
    DMA_PIXEL_FORMAT_RGB_888,

    DMA_PIXEL_FORMAT_BGR_444,
    DMA_PIXEL_FORMAT_BGR_555,
    DMA_PIXEL_FORMAT_BGR_565,
    DMA_PIXEL_FORMAT_BGR_888,

    DMA_PIXEL_FORMAT_ARGB_1555,
    DMA_PIXEL_FORMAT_ARGB_4444,
    DMA_PIXEL_FORMAT_ARGB_8565,
    DMA_PIXEL_FORMAT_ARGB_8888,

    DMA_PIXEL_FORMAT_ABGR_1555,
    DMA_PIXEL_FORMAT_ABGR_4444,
    DMA_PIXEL_FORMAT_ABGR_8565,
    DMA_PIXEL_FORMAT_ABGR_8888,

    DMA_PIXEL_FORMAT_YVU_PLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_420_16BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_444_8BIT,
    DMA_PIXEL_FORMAT_YVU_PLANAR_444_10BIT,

    DMA_PIXEL_FORMAT_YUV_PLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YUV_PLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YUV_PLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YVU_SEMIPLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_8BIT,
    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_10BIT,
    DMA_PIXEL_FORMAT_YUV_SEMIPLANAR_420_16BIT,

    DMA_PIXEL_FORMAT_YUV_400_8BIT,
    DMA_PIXEL_FORMAT_YUV_400_10BIT,
    DMA_PIXEL_FORMAT_YUV_400_12BIT,
    DMA_PIXEL_FORMAT_YUV_400_16BIT,

    DMA_PIXEL_FORMAT_YUV_PACKED_444_8BIT,
    DMA_PIXEL_FORMAT_YUV_PACKED_444_10BIT,

    /* SVP data format */
    DMA_PIXEL_FORMAT_BGR_888_PLANAR,
} k_pixel_format_dma_e;
```

#### k_gdma_chn_attr_t

【说明】

定义 gdma 通道属性。

【定义】

```c
typedef struct
{
    k_u8 buffer_num;
    k_gdma_rotation_e rotation;
    k_bool x_mirror;
    k_bool y_mirror;
    k_u16 width;
    k_u16 height;
    k_u16 src_stride[3];
    k_u16 dst_stride[3];
    k_dma_mode_e work_mode;
    k_pixel_format_dma_e pixel_format;
} k_gdma_chn_attr_t;
```

【成员】

| 成员名称     | 描述                                                                                                                                                                                                                     |
|--------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| buffer_num   | gdma 通道 buffer 数量，至少为 1。 |
| rotation     | gdma 通道旋转角度。                                                                                                                                                                                                      |
| x_mirror     | gdma 通道是否进行水平镜像                                                                                                                                                                                                |
| y_mirror     | gdma 通道是否进行垂直镜像                                                                                                                                                                                                |
| width        | gdma 通道宽度，以像素为单位。                                                                                                                                                                                            |
| height       | gdma 通道高度，以像素为单位。                                                                                                                                                                                            |
| src_stride   | gdma 源数据 stride。如果图像格式是单通道模式，只需配置`src_stride[0]`；如果图像格式是双通道模式，需要配置`src_stride[0]`，`src_stride[1]`；如果图像格式是三通道模式，需要配置 `src_stride[0]`，`src_stride[1]`，`src_stride[2]`。  |
| dst_stride   | gdma目的数据 stride。如果图像格式是单通道模式，只需配置`dst_stride[0]`；如果图像格式是双通道模式，需要配置`dst_stride[0]`，`dst_stride[1]`；如果图像格式是三通道模式，需要配置 `dst_stride[0]`，`dst_stride[1]`，`dst_stride[2]`。 |
| work_mode    | 工作模式，可以选择绑定模式或者非绑定模式。                                                                                                                                                                               |
| pixel_format | 图像格式。                                                                                                                                                                                                               |

【注意事项】

- 无。

【相关数据类型及接口】

- [kd_mpi_dma_set_chn_attr](#kd_mpi_dma_set_chn_attr)
- [kd_mpi_dma_get_chn_attr](#kd_mpi_dma_get_chn_attr)

### sdma 通道数据类型

本模块有如下数据类型

- [SDMA_MAX_CHN_NUMS](#sdma_max_chn_nums)
- [k_sdma_data_mode_e](#k_sdma_data_mode_e)
- [k_sdma_chn_attr_t](#k_sdma_chn_attr_t)

#### SDMA_MAX_CHN_NUMS

【说明】

SDMA 最大通道数

【定义】

```c
#define SDMA_MAX_CHN_NUMS (4)
```

【注意事项】

无

【相关数据类型及接口】

无

#### k_sdma_data_mode_e

【说明】

定义 sdma 通道传输数据的模式

【定义】

```c
typedef enum
{
    DIMENSION1,
    DIMENSION2,
} k_sdma_data_mode_e;
```

【成员】

| 成员名称   | 描述              |
|------------|-------------------|
| DIMENSION1 | 一维 dma 传输模式 |
| DIMENSION1 | 二维 dma 传输模式 |

【注意事项】

无

【相关数据类型及接口】

[k_sdma_chn_attr_t](#k_sdma_chn_attr_t)

#### k_sdma_chn_attr_t

【说明】

定义 sdma 通道属性。

【定义】

```c
typedef struct
{
    k_u8 buffer_num;
    k_u32 line_size;
    k_u16 line_num;
    k_u16 line_space;
    k_sdma_data_mode_e data_mode;
    k_dma_mode_e work_mode;
} k_sdma_chn_attr_t;
```

【成员】

| 成员名称   | 描述                                                                       |
|------------|----------------------------------------------------------------------------|
| buffer_num | sdma 通道 buffer 数量，至少为 1。                                      |
| line_size  | 对于 1d 模式来说，是传输数据的总长度；对于 2d 模式来说，是单行数据的长度。 |
| line_num   | 对于 1d 模式来说，此成员无效；对于 2d 模式来说，是传输的行的个数。         |
| line_space | 对于 1d 模式来说，此成员无效；对于 2d 模式来说，是行与行之间的间隔。       |
| data_mode  | sdma 传输数据的模式，包括 1d 模式和 2d 模式。                              |
| work_mode  | 工作模式，可以选择绑定模式或者非绑定模式。                                 |

【注意事项】

无

【相关数据类型及接口】

[k_dma_chn_attr_u](#k_dma_chn_attr_u)

## 错误码

### dma 错误码

表 41

| 错误代码    | 宏定义                  | 描述                         |
|-------------|-------------------------|------------------------------|
| 0xa0148001 | K_ERR_DMA_INVALID_DEVID | 无效的设备号                 |
| 0xa0148002 | K_ERR_DMA_INVALID_CHNID | 无效的通道号                 |
| 0xa0148003 | K_ERR_DMA_ILLEGAL_PARAM | 参数错误                     |
| 0xa0148004 | K_ERR_DMA_EXIST         | DMA 设备已经存在             |
| 0xa0148005 | K_ERR_DMA_UNEXIST       | DMA 设备不存在               |
| 0xa0148006 | K_ERR_DMA_NULL_PTR      | 空指针错误                   |
| 0xa0148007 | K_ERR_DMA_NOT_CONFIG    | 尚未配置 DMA                 |
| 0xa0148008 | K_ERR_DMA_NOT_SUPPORT   | 不支持的功能                 |
| 0xa0148009 | K_ERR_DMA_NOT_PERM      | 操作不允许                   |
| 0xa014800c | K_ERR_DMA_NOMEM         | 分配内存失败，如系统内存不足 |
| 0xa014800d | K_ERR_DMA_NOBUF         | BUFF 不足                    |
| 0xa014800e | K_ERR_DMA_BUF_EMPTY     | BUFF 为空                    |
| 0xa014800f | K_ERR_DMA_BUF_FULL      | BUFF 已满                    |
| 0xa0148010 | K_ERR_DMA_NOTREADY      | 设备未就绪                   |
| 0xa0148011 | K_ERR_DMA_BADADDR       | 错误的地址                   |
| 0xa0148012 | K_ERR_DMA_BUSY          | DMA 处与忙状态               |

## 调试信息

### 概述

调试信息采用了 proc 文件系统，可实时反映当前系统的运行状态，所记录的信息可供问题定位及分析时使用

【文件目录】

/proc/

【文件清单】

| 文件名称  | 描述                        |
|-----------|-----------------------------|
| umap/dma  | 记录当前 dma 模块的使用情况 |

### 系统绑定

#### 系统绑定调试信息

【调试信息】

```shell
msh /\>cat /proc/umap/dma
-------------------------------dma dev attr info---------------------------------
DevId burst_len outstanding ckg_bypass
0 0 0 0

-------------------------------dma chn 0\~3 attr info-------------------------------
ChnId rotation x_mirror y_mirror width height work_mode
0 0 false false 0 0 BIND
1 0 false false 0 0 BIND
2 0 false false 0 0 BIND
3 0 false false 0 0 BIND

-------------------------------dma chn 4\~7 attr info-------------------------------
ChnId line_size line_num line_space data_mode work_mode
4 0 0 0 1 DIMENSION BIND
5 0 0 0 1 DIMENSION BIND
6 0 0 0 1 DIMENSION BIND
7 0 0 0 1 DIMENSION BIND
```

【调试信息分析】

记录当前 dma 模块的使用情况

【设备参数说明】

| 参数        | **描述**         |
|-------------|------------------|
| DevId       | 设备号           |
| burst_len   | dma burst length |
| outstanding | dma outstanding  |

【gdma 通道参数说明】

| 参数      | **描述**               |
|-----------|------------------------|
| ChnId     | 通道号                 |
| rotation  | 旋转度数               |
| x_mirror  | 是否进行了水平镜像     |
| y_mirror  | 是否进行了垂直镜像     |
| width     | 图像宽度，以像素为单位 |
| height    | 图像高度，以像素为单位 |
| work_mode | 工作模式               |

【sdma 通道参数说明】

| 参数       | **描述**                                                                   |
|------------|----------------------------------------------------------------------------|
| ChnId      | 通道号                                                                     |
| line_size  | 对于 1d 模式来说，是传输数据的总长度；对于 2d 模式来说，是单行数据的长度。 |
| ine_num    | 对于 1d 模式来说，此成员无效；对于 2d 模式来说，是传输的行的个数。         |
| line_space | 对于 1d 模式来说，此成员无效；对于 2d 模式来说，是行与行之间的间隔。       |
| data_mode  | sdma 传输数据的模式，包括 1d 模式和 2d 模式                                |
| work_mode  | 工作模式，可以选择绑定模式或者非绑定模式。                                 |

## demo 描述

### 非绑定模式 demo

非绑定模式 demo 位于 /bin/sample_dma.elf，执行 /bin/sample_dma.elf 后开始循环运行，按 e + 回车结束运行。

demo 主要实现了以下功能：

- 使用通道 0 搬运分辨率为 1920\*1080，8bit，YUV400 单通道的图像，gdma 旋转 90 度后输出；
- 使用通道 1 搬运分辨率为 1280\*720，8bit，YUV420 双通道的图像，gdma 旋转 180 度后输出；
- 使用通道 2 搬运分辨率为 1280\*720，10bit，YUV420 三通道的图像，gdma 进行水平和垂直镜像后输出；
- 使用通道 4 搬运数据，sdma 使用 1d 模式搬运；
- 使用通道 5 搬运数据，sdma 使用 2d 模式搬运。

### 绑定模式 demo

绑定模式 demo 位于 /bin/sample_dma_bind.elf，执行 /bin/sample_dma_bind.elf 后开始循环运行，按 e + 回车结束运行。

demo 主要实现了以下功能：

- 以 vvi 模块作为 gsdma 前级绑定的模拟输入，实现绑定功能的测试；
- 两个通道分别输入分辨率为 640\*320，8bit，YUV400 单通道的图像，gdma 分别旋转 90 度和 180 度后输出。
