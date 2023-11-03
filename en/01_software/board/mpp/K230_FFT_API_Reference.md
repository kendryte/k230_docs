# K230 FFT API Reference

![cover](../../../../zh/01_software/board/ai/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/ai/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the API of K230 FFT, including API usage and test program introduction.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation    | illustrate |
| ----    | ---- |
| FFT | Fast Fourier Transform, a fast algorithm for discrete Fourier transforms |
| IFFT | Inverse fast Fourier transform |

### Revision history

| Version  | Description | Author     | date       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | Initial edition     | Wang Jianxin       | 2023-08-08 |

## 1. Introduction to the K230 FFT

The FFT module of K230 is mainly used for hardware-accelerated FFT and IFFT calculations, and its characteristics are as follows:

Support 64, 128, 256, 512, 1024, 2048, 4096 point FFT, IFFT calculation.
Support int16 calculation accuracy, that is, the real and imaginary parts of the input and output are in INT16 format.
Supports the standard AXI4 slave interface, which is used for parameter configuration and data migration.
Input support RIRI...., RRRR...., RRRR... IIII... Format arrangement, output support RIRI...., RRRR... IIII... Format arrangement.
Using the basis 2-time decimation calculation method, there is only one butterfly operator inside.
With a single-clock domain design, the bus clock is also used as an arithmetic clock to save overhead across clock domains.
The calculation time of 4096-point FFT/IFFT is controlled within 1ms, including the total overhead of data migration, calculation, and interrupt interaction.
Supports interrupt mask and raw interrupt query.

## 2. API Reference

The k230 FFT module mainly provides the following APIs:

- [kd_mpi_fft_or_ifft](#21-kd_mpi_fft_or_ifft)
- [kd_mpi_fft_args_init](#22-kd_mpi_fft_args_init)
- [kd_mpi_fft_args_2_array](#23-kd_mpi_fft_args_2_array)
- [kd_mpi_fft](#24-kd_mpi_fft)
- [kd_mpi_ifft](#25-kd_mpi_ifft)

### 2.1 kd_mpi_fft_or_ifft

【Description】

FFT or IFFT computes core functions.

【SYNOPSIS】

```c
int kd_mpi_fft_or_ifft(k_fft_args_st * fft_args);
```

【Parameters】

| Parameter name | description                                         | Input/output |
| -------- | -------------------------------------------- | --------- |
| fft_args |   [k_fft_args_st](#31-k_fft_args_st) | Input/output |

【Return value】

| Return value | description   |
| ------ | ------ |
| 0      | Succeed. |
| other   | fail   |

【Differences】

None

【Requirement】

- Header file: mpi_fft_api.h
- Library file: libfft.a

【Note】

None

【Example】

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

【See Also】

None

### 2.2 kd_mpi_fft_args_init

【Description】

fft_args initialization (helper functions)

【SYNOPSIS】

```c
int kd_mpi_fft_args_init( int point,  k_fft_mode_e mode,  k_fft_input_mode_e im,
                          k_fft_out_mode_e om,    k_u32 timeout ,    k_u16 shift,
                          short *real, short *imag, k_fft_args_st *fft_args );
```

【Parameters】

| Parameter name | description                                                    | Input/output |
| -------- | ------------------------------------------------------- | --------- |
| point    | Points, valid values are 64, 128, 256, 512, 1024, 2048, 4096       | input      |
| mode     | [k_fft_mode_e](#32-k_fft_mode_e)  FFT_MODE IFFT_MODE  | input      |
| in       | [k_fft_input_mode_e](#33-k_fft_input_mode_e)  Input Mode | input      |
| to       | [k_fft_out_mode_e](#34-k_fft_out_mode_e)      | input      |
| time_out | Timeout                                                | input      |
| shift    | offset                                                    | input      |
| rx_input | Enter real data                                            | input      |
| iy_input | Enter imaginary data                                            | input      |
| fft_args | [k_fft_args_st](#31-k_fft_args_st) Variables to populate        | output      |

【Return value】

| Return value | description   |
| ------ | ------ |
| 0      | Succeed. |
| other   | fail   |

【Differences】

None

【Requirement】

- Header file: mpi_fft_api.h
- Library file: libfft.a

【Note】

None

【Example】

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

【See Also】

None

### 2.3 kd_mpi_fft_args_2_array

【Description】

Convert FFT output to arrays (auxiliary functions for easy printing).

【SYNOPSIS】

```c
int kd_mpi_fft_args_2_array(k_fft_args_st * fft_args, short *rx, short *iy);
```

【Parameters】

| Parameter name | description                                       | Input/output |
| -------- | ------------------------------------------ | --------- |
| fft_args | [k_fft_args_st](#31-k_fft_args_st)  | input      |
| rx_out   | Real data                                   | output      |
| iy_out   | Imaginary data                                   | output      |

【Return value】

| Return value | description   |
| ------ | ------ |
| 0      | Succeed. |
| other   | fail   |

【Differences】

None

【Requirement】

- Header file: mpi_fft_api.h
- Library file: libfft.a

【Note】

None

【Example】

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

【See Also】

None

### 2.4 kd_mpi_fft

【Description】

FFT calculation,

The core is kd_mpi_fft_args_init, kd_mpi_fft_or_ifft, and kd_mpi_fft_args_2_arra three functions packaged together for easy use.

【SYNOPSIS】

```c
int kd_mpi_fft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

【Parameters】

| Parameter name        | description                          | Input/output |
|-----------------|-------------------------------|-----------|
| point_num   | Points, valid values are 64, 128, 256, 512, 1024, 2048, 4096 | input      |
| in          | [fft_input_mode_e](#33-k_fft_input_mode_e)  Input Mode | input    |
| to | [fft_out_mode_e](#34-k_fft_out_mode_e)  | input |
| time_out | Timeout | input |
| shift | offset | input |
| rx_input | Enter real data | input |
| iy_input | Enter imaginary data | input |
| rx_out | Calculate the resulting real data | output |
| iy_out | Calculation results: imaginary data | output |

【Return value】

| Return value  | description                            |
|---------|---------------------------------|
| 0       | Succeed.                          |
| other    | fail |

【Differences】

None

【Requirement】

- Header file: mpi_fft_api.h
- Library file: libfft.a

【Note】

None

【Example】

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

【See Also】

None

### 2.5 kd_mpi_ifft

【Description】

IFFT calculation

The core is kd_mpi_fft_args_init, kd_mpi_fft_or_ifft, and kd_mpi_fft_args_2_arra three functions packaged together for easy use.

【SYNOPSIS】

```c
int kd_mpi_ifft(int point , k_fft_input_mode_e im,  k_fft_out_mode_e om,
                k_u32 timeout , k_u16 shift ,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

【Parameters】

| Parameter name  | description                                                | Input/output |
| --------- | --------------------------------------------------- | --------- |
| point_num | Points, valid values are 64, 128, 256, 512, 1024, 2048, 4096   | input      |
| in        | [fft_input_mode_e](#33-k_fft_input_mode_e)  Input Mode | input      |
| to        | [fft_out_mode_e](#34-k_fft_out_mode_e)       | input      |
| time_out  | Timeout                                            | input      |
| shift     | offset                                                | input      |
| dma_ch    | DMA channels 0-3 are valid; other values are illegal                        | input      |
| rx_input  | Enter real data                                        | input      |
| iy_input  | Enter imaginary data                                        | input      |
| rx_out    | Calculate the resulting real data                                    | output      |
| iy_out    | Calculation results: imaginary data                                    | output      |

【Return value】

| Return value | description   |
| ------ | ------ |
| 0      | Succeed. |
| other   | fail   |

【Differences】

None

【Requirement】

- Header file: mpi_fft_api.h
- Library file: libfft.a

【Note】

None

【Example】

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

【See Also】

None

## 3. Data structure

The relevant data types for this function module are defined as follows:

- [k_fft_args_st](#31-k_fft_args_st)
- [k_fft_mode_e](#32-k_fft_mode_e)
- [k_fft_input_mode_e](#33-k_fft_input_mode_e)
- [k_fft_out_mode_e](#34-k_fft_out_mode_e)

### 3.1 k_fft_args_st

【Description】FFT IOCTL parameter

【Definition】

```c
typedef union
{
    struct {
        volatile fft_point_e point:3; //2:0  0:64;1:128;2:256;3:512;4:1024;5:2048;6:4096
        volatile k_fft_mode_e mode:1;  //3 0:fft 1:ifft
        volatile k_fft_input_mode_e im:2; //5:4 0:RIRI....;1:RRRR...;2:RRRR...IIII..
        volatile k_fft_out_mode_e om:1; //6 0:RIRI....;1:RRRR...IIII...
        volatile k_u64 fft_intr_mask : 1;//7 0:not mask intr; 1:mask intr
        volatile k_u16 shift:12; //19:8
        volatile k_u32 fft_disable_cg : 1;//20 write 1 disable fft clock gating
        volatile k_u32 reserv : 11 ;//31:21
        volatile k_u32 time_out:32;//63:32
    }__attribute__ ((packed));
    volatile k_u64 cfg_value;
} __attribute__ ((packed)) k_fft_cfg_reg_st;


typedef struct {
    k_fft_cfg_reg_st reg;
    k_char rsv[4];
    k_u64 data[FFT_MAX_POINT*4/8]; // input and output;
}k_fft_args_st;
```

【Members】

| **Member Name** | **Description**          |
| ------------ | ----------------- |
| reg          | The configuration register value of the FFT |
| data         | Input and output data of FFT |

【Note】

None

### 3.2 k_fft_mode_e

【Description】FFT IOCTL parameter

【Definition】

```c
typedef enum  {
    FFT_MODE = 0,
    IFFT_MODE,
}k_fft_mode_e;
```

【Members】

| **Member Name** | **** Description|
| ------------ | -------- |
| FFT_MODE     | fft      |
| IFFT_MODE    | ifft     |

【Note】

None

### 3.3 k_fft_input_mode_e

【Description】FFT IOCTL parameter

【Definition】

```c
typedef enum {
    RIRI = 0,
    RRRR,
    RR_II,
} k_fft_input_mode_e;
```

【Members】

| **Member Name** | **Description**       |
| ------------ | -------------- |
| RI         | RIRI format data   |
| RRRR         | RRRR solid data |
| RR_II        | RR_II format data  |

【Note】

none

### 3.4 k_fft_out_mode_e

【Description】FFT IOCTL parameter

【Definition】

```c
typedef enum {
    RIRI_OUT = 0,
    RR_II_OUT,
} k_fft_out_mode_e;
```

【Members】

| **Member Name** | **Description**      |
| ------------ | ------------- |
| RIRI_OUT     | RIRI format data  |
| RR_II_OUT    | RR_II format data |

【Note】

None
