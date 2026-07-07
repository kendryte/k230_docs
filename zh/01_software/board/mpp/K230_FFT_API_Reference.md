# K230 FFT API参考

## k230 fft介绍

K230 的FFT模块主要用于硬件加速FFT、IFFT的计算，其特性如下：

支持64、128、256、512、1024、2048、4096点fft、ifft计算。
支持int16计算精度，即输入输出的实部、虚部均为int16格式。
支持标准的axi4 slave接口，参数配置与数据搬移均使用该接口。
输入支持RIRI....、RRRR....（纯实部）、RRRR...IIII...格式排列，输出支持RIRI....、RRRR...IIII...格式排列。
采用基2-时间抽取的计算方式，内部只有一个蝶形算子。
采用单时钟域设计，总线时钟同时做为运算时钟，以节省跨时钟域的开销。
4096点fft/ifft的计算时长控制在1ms以内，包括数据搬移、计算、中断交互的总开销。
支持中断mask、原始中断查询。

## API 参考

k230 FFT模块主要提供了以下 API：

- [kd_mpi_fft_or_ifft](#kd_mpi_fft_or_ifft)
- [kd_mpi_fft_args_init](#kd_mpi_fft_args_init)
- [kd_mpi_fft_args_2_array](#kd_mpi_fft_args_2_array)
- [kd_mpi_fft](#kd_mpi_fft)
- [kd_mpi_ifft](#kd_mpi_ifft)

### kd_mpi_fft_or_ifft

【描述】

fft或ifft计算核心函数。

【语法】

```c
int kd_mpi_fft_or_ifft(k_fft_args_st * fft_args);
```

【参数】

| 参数名称 | 描述                                         | 输入/输出 |
| -------- | -------------------------------------------- | --------- |
| fft_args | fft参数  [k_fft_args_st](#k_fft_args_st) | 输入/输出 |

【返回值】

| 返回值 | 描述   |
| ------ | ------ |
| 0      | 成功。 |
| 非 0   | 失败   |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

```c
int kd_mpi_fft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0 ;
    k_fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE , im, om, \
                 timeout,  shift,   rx_in, iy_in , &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out);ERET(ret);
    return 0;
}
```

【相关主题】

无

### kd_mpi_fft_args_init

【描述】

fft_args初始化(辅助函数)

【语法】

```c
int kd_mpi_fft_args_init( int point,  k_fft_mode_e mode,  k_fft_input_mode_e im,
                          k_fft_out_mode_e om,    k_u32 timeout ,    k_u16 shift,
                          short *real, short *imag, k_fft_args_st *fft_args );
```

【参数】

| 参数名称 | 描述                                                    | 输入/输出 |
| -------- | ------------------------------------------------------- | --------- |
| point    | 点数，有效值为64、128、256、512、1024、2048、4096       | 输入      |
| mode     | [k_fft_mode_e](#k_fft_mode_e)  FFT_MODE  IFFT_MODE  | 输入      |
| im       | [k_fft_input_mode_e](#k_fft_input_mode_e)  输入模式 | 输入      |
| om       | [k_fft_out_mode_e](#k_fft_out_mode_e) 输出模式      | 输入      |
| time_out | 超时时间                                                | 输入      |
| shift    | 偏移                                                    | 输入      |
| rx_input | 输入实数数据                                            | 输入      |
| iy_input | 输入虚数数据                                            | 输入      |
| fft_args | [k_fft_args_st](#k_fft_args_st) 要填充的变量        | 输出      |

【返回值】

| 返回值 | 描述   |
| ------ | ------ |
| 0      | 成功。 |
| 非 0   | 失败   |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

```c++
int kd_mpi_fft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0 ;
    k_fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE , im, om, \
                 timeout,  shift,   rx_in, iy_in , &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out);ERET(ret);
    return 0;
}
```

【相关主题】

无

### kd_mpi_fft_args_2_array

【描述】

把fft输出转换成数组(辅助函数,方便打印)。

【语法】

```c
int kd_mpi_fft_args_2_array(k_fft_args_st * fft_args, short *rx, short *iy);
```

【参数】

| 参数名称 | 描述                                       | 输入/输出 |
| -------- | ------------------------------------------ | --------- |
| fft_args | [k_fft_args_st](#k_fft_args_st) 结构体 | 输入      |
| rx_out   | 实数数据                                   | 输出      |
| iy_out   | 虚数数据                                   | 输出      |

【返回值】

| 返回值 | 描述   |
| ------ | ------ |
| 0      | 成功。 |
| 非 0   | 失败   |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

```c++
int kd_mpi_fft(int point , fft_input_mode_e im,  fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,          k_u16 dma_ch,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0 ;
    fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE , im, om, \
                 timeout,  shift, dma_ch,  rx_in, iy_in , &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out);ERET(ret);
    return 0;
}
```

【相关主题】

无

### kd_mpi_fft

【描述】

fft计算,

核心是kd_mpi_fft_args_init,   kd_mpi_fft_or_ifft,  kd_mpi_fft_args_2_arra三个函数封装到一起，方便使用。

【语法】

```c
int kd_mpi_fft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| point_num   | 点数，有效值为64、128、256、512、1024、2048、4096 | 输入      |
| im          | [fft_input_mode_e](#k_fft_input_mode_e)  输入模式 | 输入    |
| om | [fft_out_mode_e](#k_fft_out_mode_e) 输出模式 | 输入 |
| time_out | 超时时间 | 输入 |
| shift | 偏移 | 输入 |
| rx_input | 输入实数数据 | 输入 |
| iy_input | 输入虚数数据 | 输入 |
| rx_out | 计算结果实数数据 | 输出 |
| iy_out | 计算结果虚数数据 | 输出 |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败 |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

```c
static int fft_test(int point)
{

    test_build_fft_org_data(point, i_real, i_imag);

    //soft_fft_ifft_calc(point);
    clock_gettime(CLOCK_MONOTONIC, &begain_time);
    kd_mpi_fft(point,   RIRI,RR_II_OUT, 0, 0x555,  i_real, i_imag, o_h_real, o_h_imag);
    clock_gettime(CLOCK_MONOTONIC, &fft_end);
    kd_mpi_ifft(point,  RIRI,RR_II_OUT, 0, 0xaaa,  o_h_real, o_h_imag, o_h_ifft_real, o_h_ifft_imag);
    clock_gettime(CLOCK_MONOTONIC, &ifft_end);
    display_calc_result(point);

    return 0;
}
```

【相关主题】

无

### kd_mpi_ifft

【描述】

ifft计算

核心是kd_mpi_fft_args_init,   kd_mpi_fft_or_ifft,  kd_mpi_fft_args_2_arra三个函数封装到一起，方便使用。

【语法】

```c
int kd_mpi_ifft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

【参数】

| 参数名称  | 描述                                                | 输入/输出 |
| --------- | --------------------------------------------------- | --------- |
| point_num | 点数，有效值为64、128、256、512、1024、2048、4096   | 输入      |
| im        | [fft_input_mode_e](#k_fft_input_mode_e)  输入模式 | 输入      |
| om        | [fft_out_mode_e](#k_fft_out_mode_e) 输出模式      | 输入      |
| time_out  | 超时时间                                            | 输入      |
| shift     | 偏移                                                | 输入      |
| dma_ch    | dma通道  0-3有效；其他值非法                        | 输入      |
| rx_input  | 输入实数数据                                        | 输入      |
| iy_input  | 输入虚数数据                                        | 输入      |
| rx_out    | 计算结果实数数据                                    | 输出      |
| iy_out    | 计算结果虚数数据                                    | 输出      |

【返回值】

| 返回值 | 描述   |
| ------ | ------ |
| 0      | 成功。 |
| 非 0   | 失败   |

【芯片差异】

无

【需求】

- 头文件：mpi_fft_api.h
- 库文件：libfft.a

【注意】

无

【举例】

```c++
static int fft_test(int point)
{

    test_build_fft_org_data(point, i_real, i_imag);

    //soft_fft_ifft_calc(point);
    clock_gettime(CLOCK_MONOTONIC, &begain_time);
    kd_mpi_fft(point,   RIRI,RR_II_OUT, 0, 0x555,  i_real, i_imag, o_h_real, o_h_imag);
    clock_gettime(CLOCK_MONOTONIC, &fft_end);
    kd_mpi_ifft(point,  RIRI,RR_II_OUT, 0, 0xaaa,  o_h_real, o_h_imag, o_h_ifft_real, o_h_ifft_imag);
    clock_gettime(CLOCK_MONOTONIC, &ifft_end);
    display_calc_result(point);

    return 0;
}
```

【相关主题】

无

## 数据结构

该功能模块的相关数据类型定义如下：

- [k_fft_args_st](#k_fft_args_st)
- [k_fft_mode_e](#k_fft_mode_e)
- [k_fft_input_mode_e](#k_fft_input_mode_e)
- [k_fft_out_mode_e](#k_fft_out_mode_e)

### k_fft_args_st

【说明】fft ioctl 参数

【定义】

```c
typedef union
{
    struct {
        volatile fft_point_e point:3; //2:0  0:64;1:128;2:256;3:512;4:1024;5:2048;6:4096
        volatile k_fft_mode_e mode:1;  //3 0:fft 1:ifft
        volatile k_fft_input_mode_e im:2; //5:4 0:RIRI....;1:RRRR....（纯实部）;2:RRRR...IIII..
        volatile k_fft_out_mode_e om:1; //6 0:RIRI....;1:RRRR...IIII...
        volatile k_u64 fft_intr_mask : 1;//7 0:not mask intr; 1:mask intr
        volatile k_u16 shift:12; //19:8  [11]第12级右移使能.....[0]第一级右移使能
        volatile k_u32 fft_disable_cg : 1;//20 clock gating disable使能信号，write 1 disable fft clock gating
        volatile k_u32 reserv : 11 ;//31:21
        volatile k_u32 time_out:32;//63:32 表示fft使能后FFT模块计算超时的门限；该值写0表示不存在FFT超时上报中断功能
    }__attribute__ ((packed));
    volatile k_u64 cfg_value;
} __attribute__ ((packed)) k_fft_cfg_reg_st;


typedef struct {
    k_fft_cfg_reg_st reg;
    k_char rsv[4];
    k_u64 data[FFT_MAX_POINT*4/8]; // input and output;
}k_fft_args_st;
```

【成员】

| **成员名称** | **描述**          |
| ------------ | ----------------- |
| reg          | fft的配置寄存器值 |
| data         | fft的输入输出数据 |

【注意事项】

无

### k_fft_mode_e

【说明】fft ioctl 参数

【定义】

```c
typedef enum  {
    FFT_MODE = 0,
    IFFT_MODE,
}k_fft_mode_e;
```

【成员】

| **成员名称** | **描述** |
| ------------ | -------- |
| FFT_MODE     | fft      |
| IFFT_MODE    | ifft     |

【注意事项】

无

### k_fft_input_mode_e

【说明】fft ioctl 参数

【定义】

```c
typedef enum {
    RIRI = 0,
    RRRR,
    RR_II,
} k_fft_input_mode_e;
```

【成员】

| **成员名称** | **描述**       |
| ------------ | -------------- |
| RIRI         | RIRI格式数据   |
| RRRR         | RRRR纯实部数据 |
| RR_II        | RR_II格式数据  |

【注意事项】

无

### k_fft_out_mode_e

【说明】fft ioctl 参数

【定义】

```c
typedef enum {
    RIRI_OUT = 0,
    RR_II_OUT,
} k_fft_out_mode_e;
```

【成员】

| **成员名称** | **描述**      |
| ------------ | ------------- |
| RIRI_OUT     | RIRI格式数据  |
| RR_II_OUT    | RR_II格式数据 |

【注意事项】

无
