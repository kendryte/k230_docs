# K230 FFT API Reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any explicit or implicit statements or guarantees regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is only for use as a reference guide.

Due to product version upgrades or other reasons, the contents of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the Company's written permission, no unit or individual may excerpt, copy any part or all of the content of this document, and may not disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the API of K230 FFT, including the usage of the API and the introduction of test programs.

### Target Audience

This document (this guide) is mainly suitable for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
| ------------ | ----------- |
| FFT          | Fast Fourier Transform, a fast algorithm for discrete Fourier transform |
| IFFT         | Inverse Fast Fourier Transform, the inverse of the fast Fourier transform |

### Revision Record

| Document Version | Modification Description | Modifier | Date       |
| ---------------- | ------------------------ | -------- | ---------- |
| V1.0             | Initial Version          | Wang Jianxin | 2023-08-08 |

## 1. Introduction to K230 FFT

The FFT module of K230 is mainly used for hardware acceleration of FFT and IFFT calculations. Its features are as follows:

- Supports 64, 128, 256, 512, 1024, 2048, 4096-point FFT and IFFT calculations.
- Supports int16 calculation precision, i.e., the real and imaginary parts of the input and output are in int16 format.
- Supports standard AXI4 slave interface, with parameter configuration and data transfer using this interface.
- The input supports RIRI...., RRRR.... (pure real part), RRRR...IIII... format arrangement, and the output supports RIRI...., RRRR...IIII... format arrangement.
- Uses radix-2 time decimation calculation method, with only one butterfly operator inside.
- Uses single clock domain design, with the bus clock also serving as the operation clock to save cross-clock domain overhead.
- The calculation time for 4096-point FFT/IFFT is controlled within 1ms, including the total overhead of data transfer, calculation, and interrupt interaction.
- Supports interrupt mask and raw interrupt query.

## 2. API Reference

The K230 FFT module mainly provides the following APIs:

- [kd_mpi_fft_or_ifft](#21-kd_mpi_fft_or_ifft)
- [kd_mpi_fft_args_init](#22-kd_mpi_fft_args_init)
- [kd_mpi_fft_args_2_array](#23-kd_mpi_fft_args_2_array)
- [kd_mpi_fft](#24-kd_mpi_fft)
- [kd_mpi_ifft](#25-kd_mpi_ifft)

### 2.1 kd_mpi_fft_or_ifft

**Description**:

Core function for FFT or IFFT calculation.

**Syntax**:

```c
int kd_mpi_fft_or_ifft(k_fft_args_st * fft_args);
```

**Parameters**:

| Parameter | Description                               | Input/Output |
| --------- | ----------------------------------------- | ------------ |
| fft_args  | FFT parameters [k_fft_args_st](#31-k_fft_args_st) | Input/Output |

**Return Value**:

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| Non-zero     | Failure     |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_fft_api.h
- Library file: libfft.a

**Notes**:

None

**Example**:

```c
int kd_mpi_fft(int point, k_fft_input_mode_e im, k_fft_out_mode_e om,
               k_u32 timeout, k_u16 shift,
               short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0;
    k_fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE, im, om, timeout, shift, rx_in, iy_in, &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out); ERET(ret);
    return 0;
}
```

**Related Topics**:

None

### 2.2 kd_mpi_fft_args_init

**Description**:

Initialization of fft_args (helper function)

**Syntax**:

```c
int kd_mpi_fft_args_init(int point, k_fft_mode_e mode, k_fft_input_mode_e im,
                         k_fft_out_mode_e om, k_u32 timeout, k_u16 shift,
                         short *real, short *imag, k_fft_args_st *fft_args);
```

**Parameters**:

| Parameter | Description                                        | Input/Output |
| --------- | -------------------------------------------------- | ------------ |
| point     | Number of points, valid values are 64, 128, 256, 512, 1024, 2048, 4096 | Input      |
| mode      | [k_fft_mode_e](#32-k_fft_mode_e) FFT_MODE IFFT_MODE | Input      |
| im        | [k_fft_input_mode_e](#33-k_fft_input_mode_e) Input mode | Input      |
| om        | [k_fft_out_mode_e](#34-k_fft_out_mode_e) Output mode | Input      |
| timeout   | Timeout                                            | Input      |
| shift     | Offset                                             | Input      |
| rx_input  | Input real data                                    | Input      |
| iy_input  | Input imaginary data                               | Input      |
| fft_args  | [k_fft_args_st](#31-k_fft_args_st) Variable to be filled | Output     |

**Return Value**:

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| Non-zero     | Failure     |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_fft_api.h
- Library file: libfft.a

**Notes**:

None

**Example**:

```c++
int kd_mpi_fft(int point, k_fft_input_mode_e im, k_fft_out_mode_e om,
               k_u32 timeout, k_u16 shift,
               short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0;
    k_fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE, im, om, timeout, shift, rx_in, iy_in, &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out); ERET(ret);
    return 0;
}
```

**Related Topics**:

None

### 2.3 kd_mpi_fft_args_2_array

**Description**:

Convert FFT output to array (helper function, convenient for printing).

**Syntax**:

```c
int kd_mpi_fft_args_2_array(k_fft_args_st * fft_args, short *rx, short *iy);
```

**Parameters**:

| Parameter | Description                               | Input/Output |
| --------- | ----------------------------------------- | ------------ |
| fft_args  | [k_fft_args_st](#31-k_fft_args_st) Structure | Input      |
| rx_out    | Real data                                 | Output      |
| iy_out    | Imaginary data                            | Output      |

**Return Value**:

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| Non-zero     | Failure     |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_fft_api.h
- Library file: libfft.a

**Notes**:

None

**Example**:

```c++
int kd_mpi_fft(int point, fft_input_mode_e im, fft_out_mode_e om,
               k_u32 timeout, k_u16 shift, k_u16 dma_ch,
               short *rx_in, short *iy_in, short *rx_out, short *iy_out)
{
    int ret = 0;
    fft_args_st fft_args;
    ret = kd_mpi_fft_args_init(point, FFT_MODE, im, om, timeout, shift, dma_ch, rx_in, iy_in, &fft_args); ERET(ret);
    ret = kd_mpi_fft_or_ifft(&fft_args); ERET(ret);
    ret = kd_mpi_fft_args_2_array(&fft_args, rx_out, iy_out); ERET(ret);
    return 0;
}
```

**Related Topics**:

None

### 2.4 kd_mpi_fft

**Description**:

FFT calculation.

The core functions kd_mpi_fft_args_init, kd_mpi_fft_or_ifft, and kd_mpi_fft_args_2_array are encapsulated together for convenience of use.

**Syntax**:

```c
int kd_mpi_fft(int point, k_fft_input_mode_e im, k_fft_out_mode_e om,
               k_u32 timeout, k_u16 shift,
               short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

**Parameters**:

| Parameter   | Description                                        | Input/Output |
| ----------- | -------------------------------------------------- | ------------ |
| point_num   | Number of points, valid values are 64, 128, 256, 512, 1024, 2048, 4096 | Input      |
| im          | [fft_input_mode_e](#33-k_fft_input_mode_e) Input mode | Input      |
| om          | [fft_out_mode_e](#34-k_fft_out_mode_e) Output mode | Input      |
| timeout     | Timeout                                            | Input      |
| shift       | Offset                                             | Input      |
| rx_input    | Input real data                                    | Input      |
| iy_input    | Input imaginary data                               | Input      |
| rx_out      | Computed result real data                          | Output     |
| iy_out      | Computed result imaginary data                     | Output     |

**Return Value**:

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| Non-zero     | Failure     |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_fft_api.h
- Library file: libfft.a

**Notes**:

None

**Example**:

```c
static int fft_test(int point)
{
    test_build_fft_org_data(point, i_real, i_imag);

    //soft_fft_ifft_calc(point);
    clock_gettime(CLOCK_MONOTONIC, &begin_time);
    kd_mpi_fft(point, RIRI, RR_II_OUT, 0, 0x555, i_real, i_imag, o_h_real, o_h_imag);
    clock_gettime(CLOCK_MONOTONIC, &fft_end);
    kd_mpi_ifft(point, RIRI, RR_II_OUT, 0, 0xaaa, o_h_real, o_h_imag, o_h_ifft_real, o_h_ifft_imag);
    clock_gettime(CLOCK_MONOTONIC, &ifft_end);
    display_calc_result(point);

    return 0;
}
```

**Related Topics**:

None

### 2.5 kd_mpi_ifft

**Description**:

IFFT calculation.

The core functions kd_mpi_fft_args_init, kd_mpi_fft_or_ifft, and kd_mpi_fft_args_2_array are encapsulated together for convenience of use.

**Syntax**:

```c
int kd_mpi_ifft(int point, k_fft_input_mode_e im, k_fft_out_mode_e om,
                k_u32 timeout, k_u16 shift,
                short *rx_in, short *iy_in, short *rx_out, short *iy_out);
```

**Parameters**:

| Parameter   | Description                                        | Input/Output |
| ----------- | -------------------------------------------------- | ------------ |
| point_num   | Number of points, valid values are 64, 128, 256, 512, 1024, 2048, 4096 | Input      |
| im          | [fft_input_mode_e](#33-k_fft_input_mode_e) Input mode | Input      |
| om          | [fft_out_mode_e](#34-k_fft_out_mode_e) Output mode | Input      |
| timeout     | Timeout                                            | Input      |
| shift       | Offset                                             | Input      |
| dma_ch      | DMA channel, valid values are 0-3; other values are invalid | Input      |
| rx_input    | Input real data                                    | Input      |
| iy_input    | Input imaginary data                               | Input      |
| rx_out      | Computed result real data                          | Output     |
| iy_out      | Computed result imaginary data                     | Output     |

**Return Value**:

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success     |
| Non-zero     | Failure     |

**Chip Differences**:

None

**Requirements**:

- Header file: mpi_fft_api.h
- Library file: libfft.a

**Notes**:

None

**Example**:

```c++
static int fft_test(int point)
{
    test_build_fft_org_data(point, i_real, i_imag);

    //soft_fft_ifft_calc(point);
    clock_gettime(CLOCK_MONOTONIC, &begin_time);
    kd_mpi_fft(point, RIRI, RR_II_OUT, 0, 0x555, i_real, i_imag, o_h_real, o_h_imag);
    clock_gettime(CLOCK_MONOTONIC, &fft_end);
    kd_mpi_ifft(point, RIRI, RR_II_OUT, 0, 0xaaa, o_h_real, o_h_imag, o_h_ifft_real, o_h_ifft_imag);
    clock_gettime(CLOCK_MONOTONIC, &ifft_end);
    display_calc_result(point);

    return 0;
}
```

**Related Topics**:

None

## 3. Data Structures

The data types related to this functional module are defined as follows:

- [k_fft_args_st](#31-k_fft_args_st)
- [k_fft_mode_e](#32-k_fft_mode_e)
- [k_fft_input_mode_e](#33-k_fft_input_mode_e)
- [k_fft_out_mode_e](#34-k_fft_out_mode_e)

### 3.1 k_fft_args_st

**Description**: FFT ioctl parameters

**Definition**:

```c
typedef union
{
    struct {
        volatile fft_point_e point:3; //2:0  0:64;1:128;2:256;3:512;4:1024;5:2048;6:4096
        volatile k_fft_mode_e mode:1;  //3 0:fft 1:ifft
        volatile k_fft_input_mode_e im:2; //5:4 0:RIRI....;1:RRRR.... (pure real part);2:RRRR...IIII..
        volatile k_fft_out_mode_e om:1; //6 0:RIRI....;1:RRRR...IIII...
        volatile k_u64 fft_intr_mask : 1;//7 0:not mask intr; 1:mask intr
        volatile k_u16 shift:12; //19:8  [11] Enable right shift for the 12th stage.....[0] Enable right shift for the 1st stage
        volatile k_u32 fft_disable_cg : 1;//20 Clock gating disable signal, write 1 to disable FFT clock gating
        volatile k_u32 reserv : 11 ;//31:21
        volatile k_u32 time_out:32;//63:32 Indicates the timeout threshold for FFT module calculation after FFT is enabled; writing 0 means that the FFT timeout interrupt function does not exist
    }__attribute__ ((packed));
    volatile k_u64 cfg_value;
} __attribute__ ((packed)) k_fft_cfg_reg_st;

typedef struct {
    k_fft_cfg_reg_st reg;
    k_char rsv[4];
    k_u64 data[FFT_MAX_POINT*4/8]; // input and output;
} k_fft_args_st;
```

**Members**:

| **Member Name** | **Description**       |
| --------------- | --------------------- |
| reg             | Configuration register value for FFT |
| data            | Input and output data for FFT |

**Notes**:

None

### 3.2 k_fft_mode_e

**Description**: FFT ioctl parameters

**Definition**:

```c
typedef enum  {
    FFT_MODE = 0,
    IFFT_MODE,
} k_fft_mode_e;
```

**Members**:

| **Member Name** | **Description** |
| --------------- | --------------- |
| FFT_MODE        | FFT             |
| IFFT_MODE       | IFFT            |

**Notes**:

None

### 3.3 k_fft_input_mode_e

**Description**: FFT ioctl parameters

**Definition**:

```c
typedef enum {
    RIRI = 0,
    RRRR,
    RR_II,
} k_fft_input_mode_e;
```

**Members**:

| **Member Name** | **Description**       |
| --------------- | --------------------- |
| RIRI            | RIRI format data      |
| RRRR            | Pure real part data   |
| RR_II           | RR_II format data     |

**Notes**:

None

### 3.4 k_fft_out_mode_e

**Description**: FFT ioctl parameters

**Definition**:

```c
typedef enum {
    RIRI_OUT = 0,
    RR_II_OUT,
} k_fft_out_mode_e;
```

**Members**:

| **Member Name** | **Description**      |
| --------------- | -------------------- |
| RIRI_OUT        | RIRI format data     |
| RR_II_OUT       | RR_II format data    |

**Notes**:

None
