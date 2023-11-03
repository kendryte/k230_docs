# K230 Video Output API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## Preface

### Overview

This document mainly introduces the functions and usage of the video output system control module, and the functions and usage of other modules will be discussed in special documents.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate                     |
|------|--------------------------|
| VO | Video output             |
| DSI  | Display Serial Interface |

### Revision history

| Document version number | Modify the description | Author     | date       |
|------------|----------|------------|------------|
| V1.0       | Initial edition     | System Software Department | 2023-03-10 |

## 1. Overview

VO (Video Output) module actively reads video and graphics data from the corresponding location in memory, and outputs video and graphics through the corresponding display device. Display/write-back devices, video layers, and graphics layer conditions supported by the chip.

LAYER SUPPORT:

|            | LAYER0             | LAYER1             | LAYER2                    |
|------------|--------------------|--------------------|---------------------------|
| Input format   | YUV420 NV12        | YUV420 NV12        | YUV420 NV12 YUV422 NV16 ? |
| Maximum resolution | 1920x1080          | 1920x1080          | 1920x1080                 |
| Overlay display   | Supports configurable overlay order | Supports configurable overlay order | Supports configurable overlay order        |
| Rotation   | √                  | √                  | -                         |
| Scaler     | √                  | -                  | -                         |
| Mirror     | √                  | √                  | -                         |
| Gray       | √                  | √                  | -                         |
| Independent switch   | √                  | √                  | √                         |

OSD layer support

|                    | OSD0                                                      | OSD1                                                      | OSD2                                                      | OSD3                                                      |
|--------------------|-----------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|-----------------------------------------------------------|
| Input format           | RGB888 RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888 RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888 RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  | RGB888 RGB565 ARGB8888 Monochrome-8-bit RGB4444 RGB1555  |
| Maximum resolution         | 1920x1080                                                 | 1920x1080                                                 | 1920x1080                                                 | 1920x1080                                                 |
| Overlay display           | Supports configurable overlay order                                        | Supports configurable overlay order                                        | Supports configurable overlay order                                        | Supports configurable overlay order                                        |
| ARGB 265 grade ALPHA | √                                                         | √                                                         | √                                                         | √                                                         |
| Independent switch           | √                                                         | √                                                         | √                                                         | √                                                         |

### 1.1 Hardware Description

This hardware introduction is based on EVBLP3

#### 1.1.1 MIPI interface

The hardware pins on EVBLP3 are as follows:

![The image contains an illustrated description that has been automatically generated](../../../../zh/01_software/board/mpp/images/d7197713d3821fdd3e5c0f2b10dfd5b1.png)

- screen touch is I2C4  (SCL: GPIO7, SDA GPIO8)
- screen touch rst：gpio29， int：gpio30
- screen rst：gpio9，backlight：gpio31
- The pins of MIPI correspond one-to-one with the pins of the screen

#### 1.1.2 Physical drawings

![Image contains game console, electronics, circuit description has been automatically generated](../../../../zh/01_software/board/mpp/images/69dbfc0ef3144c90f5978f1019482030.png)

- Figure 1 is the MIPI interface, using a flexible cable
- Figure 2 is the MIPI signal test point, including four data lines and one CLK line

### 1.2 Software Description

Video output software configuration is divided into 3 parts configuration: phy configuration, DSI configuration, VO configuration,

#### 1.2.1 PHY configuration process

The frequency of PHY needs to configure three parameters, calculate PLL, configure VOCs, configure FREQ, according to these three parameters can determine the frequency of TXPHY, each parameter is calculated as follows.

##### 1.2.1.1 Calculate the PLL of PHY

The data rate is given by twice the PLL output clock phase frequency: data rate (Gbps) = PLL Fout(GHz) \* 2, and the output frequency is a function of the input reference frequency and the multiplier/divider ratio. The PLL for calculating PHY is divided into 4 ranges to do calculations, different frequencies correspond to different frequencies, which can be determined in the following ways:

| M      | m+2 |
|--------|-----|
| N      | n+1 |
| Fclkin | 24M |

For：

![Text, letter description is automatically generated](../../../../zh/01_software/board/mpp/images/e99b3eec46b58875ae936ea4ab23d86b.png)

However in this need to follow the following restrictions:

![The image contains a text description that has been automatically generated](../../../../zh/01_software/board/mpp/images/cfd696fc1b6157fbf0220a4f1545a963.png)

For：

![Text, letter description is automatically generated](../../../../zh/01_software/board/mpp/images/e0df5cfd79b26cd1c688cb8f82000188.png)

For：

![Text, letter description is automatically generated](../../../../zh/01_software/board/mpp/images/fb853b016887c1d58cc45f4507d9276c.png)

![The Text description is automatically generated](../../../../zh/01_software/board/mpp/images/9cd0c8d3bd975f1f19a5eec9b846d00b.png)

For：

![The text Medium confidence description has been automatically generated](../../../../zh/01_software/board/mpp/images/659e3d039a5c3c623b3ffd6fb24ee777.png)

Each of the above for corresponds to a PLL level, and different levels correspond to different calculation formulas and limits, and the calculation example is as follows:

Example：

The rate of mipi is 445.5M: so the rate of pll is 222.75M, and the second formula should be selected, calculated as follows

222750000 = 1M / 2N = (m+2) / 2(n+1) \* 24000000 , the finishing formula is as follows:

222.75n + 198.75 = 12m is calculated by excel as follows:

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/8ff8dac9c9f9b815001733e37e44e4cc.png)

The resulting m = 295 and n = 15.

Configure the m and n in the PLL are integer values, if all the values are not integers, you need to add 1 and subtract 1 from the values of m and n, push back to see which frequency you need to be the closest, and then verify whether it is available, you can't repeat the above operation.

##### 1.2.1.2 Configure VOC for PHY

The VOC configured with PHY can be queried according to the table:

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/174b1b96f4a280ab5350f4ed5452d43f.png)

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/8e1970bbd7ffb862547feaf8a59cab48.png)

Example：

The rate of mipi is 445.5M: so the rate of the pll is 222.75M, and VOC = 010111 = 0x17

##### 1.2.1.3 Configure FreQ

The FREQ of the configured PHY can be queried according to the table:

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/95941399975cca1c16253927129d8e19.png)

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/22628c5b4acf510370e51188734fe172.png)

![The table description is automatically generated](../../../../zh/01_software/board/mpp/images/4a233637850b4e84b5208317666c4314.png)

Example：

The rate of mipi is 445.5M: the rate of pll is 222.75M, freq selects 0100101, when configuring this, you need to set the highest bit \[7\] = 1, all freq = 10100101 = 0xa5

#### 1.2.2 Configuration of DSI

DSI (Display Serial Interface) is part of a consortium of MIPI-defined communication protocols, mainly digital controllers that implement all protocol functions defined in the MIPI DSI specification, including bidirectional PHYs with two and four channels.

DSI mainly configures the screen in the software to display functions with timing and sending commands.

##### 1.2.2.1 Configure the timing of the display

Each manufacturer's screen will have a set of timing for screen control, mainly including the control timing of the frame and the control timing of a line, as shown in the following figure:

![The Illustrative description has been automatically generated](../../../../zh/01_software/board/mpp/images/01cabbb3d5c1dc60d0baa95a0f87104f.png)

![Illustrative, Schematic description is automatically generated](../../../../zh/01_software/board/mpp/images/507a7bd277508dc177ebb0c4cfb49b9e.png)

These parameters are also used in DSI, and the configured timing and screen are consistent.

##### 1.2.2.2 DSI send command

DSI needs to enter LP mode before sending commands, and the APIs required are as follows:

- [kd_mpi_dsi_set_lp_mode_send_cmd](#226-kd_mpi_dsi_set_lp_mode_send_cmd)
- [kd_mpi_dsi_send_cmd](#223-kd_mpi_dsi_send_cmd)

The data sent is sent in 8 bits, and the long or short packet will be automatically selected according to the quantity.

##### 1.2.2.3 DSI's self-test mode

The DSI self-test mode will send the data of the color bar according to the self-configured DSI timing to be sent, so that it does not rely on VO to read data from the DDR, and the test mode is shown as follows:

![Background pattern The medium confidence description has been automatically generated](../../../../zh/01_software/board/mpp/images/25246d8f3ff85d6e9b1de1b03369fbb3.png)

The 24-bit interface is used between DSI and vo, so the configured color bar is the effect shown above, and the use method only needs to enable the color bar after configuring DSI, and the API is as follows

- [kd_mpi_dsi_set_test_pattern](#225-kd_mpi_dsi_set_test_pattern)

#### 1.2.3 Configuration of VO

VO (video output) is mainly VO (Video Output) module actively read video and graphics data from the corresponding position of memory, and output video and graphics through the corresponding display device, VO This part contains two configurations, one is the configuration of the time, the other is the configuration of the video layer

##### 1.2.3.1 VO timing configuration

The timing configuration of VO and the timing configuration of DSI use the same configuration parameters, and the specific rows and columns are the same, just see the introduction of DSI timing

##### 1.2.3.2 Layer configuration for VO

The VO layer currently supports 3 layers and 4 OSD layers. The layer  can only display the image format of the YUV (the features supported by layer0 and layer1 are shown in the diagram).

##### 1.2.3.3 Configuration of the write-back function of VO

VO also supports the write-back function, which can verify whether the VO configuration is correct, and after the VO configuration is completed, the data will be written back to DDR to facilitate verification of whether the VO configuration is abnormal

#### 1.2.4 Debugging method of VO module

##### 1.2.4.1 Test method for screens

- You can enter the self-test mode through the LP command configuration screen to see if the resulting image is normal
- Read the screen registers with the LP command to see if they are returned

##### 1.2.4.2 Test methods for DSI

- After configuring DSI, let the screen enter the self-test mode, measure the signal to see that it is normal, and you can also see whether the screen produces a color bar image
- Check the PHY's err status register to see if there is an err status, which can be viewed through proc

##### 1.2.4.3 Test methods for VO

- After the VO configuration is completed, turn on the writeback function to check whether it is consistent with the configuration requirements
- Read the err status register of DSI to see if there is underflow and overflow in the data transfer between VO and dsi, and if so, try again with the appropriate timing

## 2. API Reference

### 2.1 TXPHY

This function module provides the following APIs:

- [kd_mpi_set_mipi_phy_attr](#211-kd_mpi_set_mipi_phy_attr)

#### 2.1.1 kd_mpi_set_mipi_phy_attr

【Description】

Set the frequency of PHY

【Syntax】

k_s32 kd_mpi_set_mipi_phy_attr(k_vo_mipi_phy_attr \*attr)

【Parameters】

| Parameter name | description               | Input/output |
|----------|--------------------|-----------|
| attr     | Description of the frequency structure of the PHY | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

### 2.2 CIO

This function module provides the following APIs:

- [kd_mpi_dsi_set_attr](#221-kd_mpi_dsi_set_attr)
- [kd_mpi_dsi_enable](#222-kd_mpi_dsi_enable)
- [kd_mpi_dsi_send_cmd](#223-kd_mpi_dsi_send_cmd)
- [kd_mpi_dsi_read_pkg](#224-kd_mpi_dsi_read_pkg)
- [kd_mpi_dsi_set_test_pattern](#225-kd_mpi_dsi_set_test_pattern)
- [kd_mpi_dsi_set_lp_mode_send_cmd](#226-kd_mpi_dsi_set_lp_mode_send_cmd)

#### 2.2.1 kd_mpi_dsi_set_attr

【Description】

Configure the DSI property parameters

【Syntax】

k_s32 kd_mpi_dsi_set_attr(k_display_mode \*ATTR)【Parameters】

| Parameter name | description         | Input/output |
|----------|--------------|-----------|
| attr     | DSI property parameter | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.2.2 kd_mpi_dsi_enable

【Description】

Open DSI

【Syntax】

k_s32 kd_mpi_dsi_enable(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.2.3 kd_mpi_dsi_send_cmd

【Description】

DSI sends  command

【Syntax】

k_s32 kd_mpi_dsi_send_cmd(k_u8 \*data, k_s32 cmd_len)

【Parameters】

| Parameter name | description       | Input/output |
|----------|------------|-----------|
| data     | Data sent | input      |
| cmd_len  | Data length   | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.2.4 kd_mpi_dsi_read_pkg

【Description】

DSI read command

【Syntax】

k_s32 kd_mpi_dsi_read_pkg(k_u8 \*rx_buf, k_s32 cmd_len)

【Parameters】

| Parameter name | description       | Input/output |
|----------|------------|-----------|
| rx_buf,  | Accepted data | input      |
| cmd_len  | Data length   | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.2.5 kd_mpi_dsi_set_test_pattern

【Description】

Configure DSI to enter self-test mode

【Syntax】

k_s32 kd_mpi_dsi_set_test_pattern(void)

【Parameters】、

not

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.2.6 kd_mpi_dsi_set_lp_mode_send_cmd

【Description】

Configure DSI to enter LP Mode to send commands

【Syntax】

k_s32 kd_mpi_dsi_set_lp_mode_send_cmd(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

### 2.3 VO

- [kd_mpi_vo_init](#231-kd_mpi_vo_init)
- [kd_mpi_vo_set_dev_param](#232-kd_mpi_vo_set_dev_param)
- [kd_mpi_vo_enable_video_layer](#233-kd_mpi_vo_enable_video_layer)
- [kd_mpi_vo_disable_video_layer](#234-kd_mpi_vo_disable_video_layer)
- [kd_mpi_vo_enable](#235-kd_mpi_vo_enable)
- [kd_mpi_vo_chn_insert_frame](#236-kd_mpi_vo_chn_insert_frame)
- [kd_mpi_vo_chn_dump_frame](#237-kd_mpi_vo_chn_dump_frame)
- [kd_mpi_vo_chn_dump_release](#238-kd_mpi_vo_chn_dump_release)
- [kd_mpi_vo_osd_enable](#239-kd_mpi_vo_osd_enable)
- [kd_mpi_vo_osd_disable](#2310-kd_mpi_vo_osd_disable)
- [kd_mpi_vo_set_video_osd_attr](#2311-kd_mpi_vo_set_video_osd_attr)
- [kd_mpi_vo_set_wbc_attr](#2312-kd_mpi_vo_set_wbc_attr)
- [kd_mpi_vo_enable_wbc](#2313-kd_mpi_vo_enable_wbc)
- [kd_mpi_vo_disable_wbc](#2314-kd_mpi_vo_disable_wbc)
- [kd_display_reset](#2315-kd_display_reset)
- [kd_display_set_backlight](#2316-kd_display_set_backlight)
- [kd_mpi_vo_set_user_sync_info](#2317-kd_mpi_vo_set_user_sync_info)
- kd_mpi_vo_draw_frame

#### 2.3.1 kd_mpi_vo_init

【Description】

VO initializes the default parameters

【Syntax】

k_s32 kd_mpi_vo_init(void);

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.2 kd_mpi_vo_set_dev_param

【Description】

DSI sends the command

【Syntax】

k_s32 kd_mpi_vo_set_dev_param(k_vo_pub_attr \*attr)

【Parameters】

| Parameter name | description                             | Input/output |
|----------|----------------------------------|-----------|
| attr     | Video output device public property structure pointer. | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.3 kd_mpi_vo_enable_video_layer

【Description】

Configure layer layer property parameters

【Syntax】

k_s32 kd_mpi_vo_enable_video_layer([k_vo_layer](#315-k_vo_layer) layer)

【Parameters】

| Parameter name | description                                                 | Input/output |
|----------|------------------------------------------------------|-----------|
| layer    | Video output video layer number Value range [0 – K_MAX_VO_LAYER_NUM] |  input     |
| attr     | Video layer property structure pointer                                 | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.4 kd_mpi_vo_disable_video_layer

【Description】

Turn off the video layer

【Syntax】

k_s32 kd_mpi_vo_disable_video_layer([k_vo_layer](#315-k_vo_layer) layer)

【Parameters】

| Parameter name | description                                                 | Input/output |
|----------|------------------------------------------------------|-----------|
| layer    | Video output video layer number Value range [0 – K_MAX_VO_LAYER_NUM] | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file:
- Library file:

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.5 kd_mpi_vo_enable

【Description】

Open VO

【Syntax】

k_u8 kd_mpi_vo_enable(void);

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file:
- Library file:

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.6 kd_mpi_vo_chn_insert_frame

【Description】

Insert frames into VO's channel

【Syntax】

k_s32 kd_mpi_vo_chn_insert_frame(k_u32 chn_num, [k_video_frame_info](#3119-k_video_frame_info) \*vf_info)

【Parameters】

| Parameter name | description                 | Input/output |
|----------|----------------------|-----------|
| chn_num  | Number of channels             | input      |
| vf_info  | The structure pointer for the video frame. | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_video_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.7 kd_mpi_vo_chn_dump_frame

【Description】

Grab one frame of data from VO's channel

【Syntax】

k_s32 kd_mpi_vo_chn_dump_frame(k_u32 chn_num, [k_video_frame_info](#3119-k_video_frame_info) \*vf_info, k_u32 timeout_ms);

【Parameters】

| Parameter name   | description               | Input/output |
|------------|--------------------|-----------|
| chn_num    | Channel ID             | input      |
| vf_info    | The structure pointer for the video frame | input      |
| timeout_ms | Timeout           | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_video_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.8 kd_mpi_vo_chn_dump_release

【Description】

Release the grab frame

【Syntax】

k_s32 kd_mpi_vo_chn_dump_release(k_u32 chn_num, const [k_video_frame_info](#3119-k_video_frame_info) \*vf_info);

【Parameters】

| Parameter name | description               | Input/output |
|----------|--------------------|-----------|
| chn_num  | Channel ID             | input      |
| vf_info  | The structure pointer for the video frame | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_video_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.9 kd_mpi_vo_osd_enable

【Description】

Open the OSD layer

【Syntax】

k_s32 kd_mpi_vo_osd_enable([k_vo_osd](#314-k_vo_osd) layer)

【Parameters】

| Parameter name | description                                               | Input/output |
|----------|----------------------------------------------------|-----------|
| layer    | Video output video layer number Value range [0 – K_MAX_VO_OSD_NUM] | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.10 kd_mpi_vo_osd_disable

【Description】

Turn off the OSD layer

【Syntax】

k_s32 kd_mpi_vo_osd_disable([k_vo_osd](#314-k_vo_osd) layer)

【Parameters】

| Parameter name | description                                               | Input/output |
|----------|----------------------------------------------------|-----------|
| layer    | Video output video layer number Value range [0 – K_MAX_VO_OSD_NUM] | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.11 kd_mpi_vo_set_video_osd_attr

【Description】

Set OSD layer properties

【Syntax】

k_s32 kd_mpi_vo_set_video_osd_attr([k_vo_osd](#314-k_vo_osd) layer, [k_vo_video_osd_attr](#3118-k_vo_video_osd_attr) \*attr)

【Parameters】

| Parameter name       | description                                               | Input/output |
|----------------|----------------------------------------------------|-----------|
| layer          | Video output video layer number Value range [0 – K_MAX_VO_OSD_NUM] | input      |
| OSD layer property parameters | OSD layer property parameters                                     | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.12 kd_mpi_vo_set_wbc_attr

【Description】

Set the write-back property

【Syntax】

k_s32 kd_mpi_vo_set_wbc_attr([k_vo_wbc_attr](#3112-k_vo_wbc_attr) \*attr)

【Parameters】

| Parameter name | description               | Input/output |
|----------|--------------------|-----------|
| attr     | The writeback property parameter | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.13 kd_mpi_vo_enable_wbc

【Description】

使能writeback

【Syntax】

k_s32 kd_mpi_vo_enable_wbc(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.14 kd_mpi_vo_disable_wbc

【Description】

Close writeback

【Syntax】

k_s32 kd_mpi_vo_disable_wbc(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.15 kd_display_reset

【Description】

Reset the video output subsystem

【Syntax】

k_s32 kd_display_reset(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.16 kd_display_set_backlight

【Description】

Reset the screen and turn on the backlight

【Syntax】

k_s32 kd_display_set_backlight(void)

【Parameters】

none

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.17 kd_mpi_vo_set_user_sync_info

【Description】

Set the user interface timing information to configure the clock source, clock size, and clock division ratio

【Syntax】

k_s32 kd_mpi_vo_set_user_sync_info([k_vo_user_sync_info](#318-k_vo_user_sync_info) \*sync_info)

【Parameters】

| Parameter name | description            | Input/output |
| -------- | --------------- | --------- |
| pre_div  | Number of user crossovers      | input      |
| clk_en   | Crossover enable enable |           |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.18 kd_mpi_vo_draw_frame

【Description】

Picture frame

【Syntax】

k_s32 kd_mpi_vo_draw_frame([k_vo_draw_frame](#3115-k_vo_draw_frame) \*frame)

【Parameters】

| Parameter name | description           | Input/output |
|----------|----------------|-----------|
| frame    | Property parameters for the picture frame | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h
- Library file: libvo.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.19 kd_mpi_get_connector_info

【Description】

Gets the data structure of the Connecor connector by connection type

【Syntax】

k_s32 kd_mpi_get_connector_info([k_connector_type](#3120-k_connector_type) connector_type, [k_connector_info](#3125-k_connector_info) \*connector_info)

【Parameters】

| Parameter name        | description           | Input/output |
|----------------|----------------|-----------|
| connector_type | The type of connector    | input      |
| connector_info | The data structure of the connector | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h k_connector_comm.h
- Library file: libvo.a libconnector.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.20 kd_mpi_connector_open

【Description】

Gets the data structure of the Connecor connector by connection type

【Syntax】

k_s32 kd_mpi_connector_open(const char \*connector_name)

【Parameters】

| Parameter name        | description           | Input/output |
|----------------|----------------|-----------|
| connector_name | The device node of the connector    | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| fd     | Successfully returns the ID of the open fd             |
| Less than 0   | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h k_connector_comm.h
- Library file: libvo.a libconnector.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.21 kd_mpi_connector_power_set

【Description】

Power on the connector

【Syntax】

k_s32 kd_mpi_connector_power_set(k_s32 fd, k_bool is)

【Parameters】

| Parameter name        | description           | Input/output |
|----------------|----------------|-----------|
| fd             | The device node of the connector    | input      |
| on             | Switch of connector device    | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h k_connector_comm.h
- Library file: libvo.a libconnector.a

【Note】

none

【Example】

none

【See Also】

none

#### 2.3.22 kd_mpi_connector_init

【Description】

vo connector init

【Syntax】

k_s32 kd_mpi_connector_init(k_s32 fd, [k_connector_info](#3125-k_connector_info) info)

【Parameters】

| Parameter name        | description           | Input/output |
|----------------|----------------|-----------|
| fd             | The device node of the connector    | input      |
| info           | Parameters for connector initialization    | input      |

【Return value】

| Return value | description               |
|--------|--------------------|
| 0      | Succeed.             |
| Non-0    | For failures, see Error codes. |

【Differences】

none

【Requirement】

- Header file: mpi_vo_api.h k_vo_comm.h k_connector_comm.h
- Library file: libvo.a libconnector.a

【Note】

none

【Example】

none

【See Also】

none

## 3. Data Type

### 3.1 VO

#### 3.1.1 k_vo_intf_sync

【Description】

Define the resolution and frame rate in the video

【Definition】

typedef enum {
&emsp;K_VO_OUT_1080P30,
&emsp;K_VO_OUT_1080P60,
} k_vo_intf_sync;

【Members】

| Member name               | description                                           |
|------------------------|------------------------------------------------|
| K_VO_OUT_1080P30       | 1080 represents 1920x1080 PIX. 30 means 30fps      |
| K_VO_OUT_1080P60       | 1080 represents 1920x1080 PIX. 60 means 60fps      |
| K_VO_OUT_1080x1920P30  | 1080x1920 represents 1080x1920 PIX. 30 means 30fps |
| K_VO_OUT_11080x1920P60 | 1080x1920 represents 1080x1920 PIX. 60 means 60fps |

【Note】

none

【See Also】

#### 3.1.2 k_vo_intf_type

【Description】

Define the resolution and frame rate in the video

【Definition】

typedef enum {
&emsp;K_VO_INTF_MIPI = 0,
} k_vo_intf_type;

【Members】

| Member name       | description      |
|----------------|-----------|
| K_VO_INTF_MIPI | MIPI interface |

【Note】

none

【See Also】

#### 3.1.3 k_pixel_format

【Description】

The data formats supported by the layer in the display, only the supported data formats are listed in the structure below, not all data formats

【Definition】

typedef enum {
&emsp;PIXEL_FORMAT_YVU_PLANAR_420,
&emsp;PIXEL_FORMAT_YVU_PLANAR_422,
&emsp;PIXEL_FORMAT_RGB_565,
&emsp;PIXEL_FORMAT_RGB_888,
&emsp;PIXEL_FORMAT_ARGB_8888,
&emsp;PIXEL_FORMAT_ARGB_4444,
&emsp;PIXEL_FORMAT_ARGB_1555,
&emsp;PIXEL_FORMAT_RGB_MONOCHROME_8BPP,
} k_pixel_format;

【Members】

| Member name                         | description        |
|----------------------------------|-------------|
| PIXEL_FORMAT_YVU_PLANAR_420      | YUV420 NV12 |
| PIXEL_FORMAT_YVU_PLANAR_422      | YUV422 NV16 |
| PIXEL_FORMAT_RGB_565             | RGB565      |
| PIXEL_FORMAT_RGB_888             | RGB888      |
| PIXEL_FORMAT_RGB_MONOCHROME_8BPP |  8 BIT RGB  |
| PIXEL_FORMAT_ARGB_8888           | ARGB8888    |
| PIXEL_FORMAT_ARGB_4444           | ARGB4444    |
| PIXEL_FORMAT_ARGB_1555           | ARGB1444    |

【Note】

none

【See Also】

none

#### 3.1.4 k_vo_osd

【Description】

The number of OSDs and the number of each OSD

【Definition】

typedef enum {
&emsp;K_VO_OSD0,
&emsp;K_VO_OSD1,
&emsp;K_VO_OSD2,
&emsp;K_VO_OSD3,
&emsp;K_MAX_VO_OSD_NUM,
} k_vo_osd;

【Members】

| Member name         | description                |
|------------------|---------------------|
| K_VO_OSD0        | OSD 0          |
| K_VO_OSD1        | OSD 1          |
| K_VO_OSD2        | OSD 2          |
| K_VO_OSD3        | OSD 3          |
| K_MAX_VO_OSD_NUM |  OSD layer maximum number flag |

【Note】

none

【See Also】

none

#### 3.1.5 k_vo_layer

【Description】

The number of layers and the number of each layer

【Definition】

typedef enum {
&emsp;K_VO_LYAER0 = 0,
&emsp;K_VO_LYAER1,
&emsp;K_VO_LYAER2,
&emsp;K_MAX_VO_LAYER_NUM,
} k_vo_layer;

Members】

| Member name           | description                  |
|--------------------|-----------------------|
| K_VO_LYAER0        | Layer 0            |
| K_VO_LYAER1        | Layer 1            |
| K_VO_LYAER2        | Layer 2            |
| K_VO_LYAER3        | Layer 3            |
| K_MAX_VO_LAYER_NUM |  Maximum number of layers flag |

【Note】

none

【See Also】

none

#### 3.1.6 k_vo_rotation

【Description】

Features supported by Layer rotation

【Definition】

typedef enum {
&emsp;K_ROTATION_0 = (0x01L \<\< 0),
&emsp;K_ROTATION_90 = (0x01L \<\< 1),
&emsp;K_ROTATION_180 = (0x01L \<\< 2),
&emsp;K_ROTATION_270 = (0x01L \<\< 3),
} k_vo_rotation;

【Note】

none

【See Also】

none

#### 3.1.7 k_vo_mirror_mode

【Description】

Features supported by Layer mirror.

【Definition】

typedef enum {
&emsp;K_VO_MIRROR_NONE = (0x01L \<\< 4),
&emsp;K_VO_MIRROR_HOR = (0x01L \<\< 5),
&emsp;K_VO_MIRROR_VER = (0x01L \<\< 6),
&emsp;K_VO_MIRROR_BOTH = (0x01L \<\< 7),
} k_vo_mirror_mode;

【Members】

| Member name         | description                    |
|------------------|-------------------------|
| K_VO_MIRROR_NONE | Layer no mirror     |
| K_VO_MIRROR_HOR  | Layer horizontal mirror |
| K_VO_MIRROR_VER  | Layer vertical mirror |
| K_VO_MIRROR_BOTH | Layer does vertical and horizontal mirrors |

【Note】

none

【See Also】

none

#### 3.1.8 k_vo_user_sync_info

【Description】

User-defined clock crossover.

【Definition】

typedef struct {
&emsp;k_u32 ext_div;
&emsp;k_u32 dev_div;
&emsp;k_u32 clk_en;
} k_vo_user_sync_info;

【Members】

| Member name | description             |
|----------|------------------|
| ext_div; | CLKEXT crossover      |
| dev_div  | Clk crossover         |
| clk_en   | Display clock enable |

【Note】

none

【See Also】

none

#### 3.1.9 k_vo_point

【Description】

Define the coordinate information structure.

【Definition】

typedef struct {
&emsp;k_u32 x;
&emsp;k_u32 y;
}k_vo_point;

【Members】

| Member name | description   |
|----------|--------|
| x        | abscissa |
| y       | ordinate |

【Note】

none

【See Also】

none

#### 3.1.10 k_vo_size

【Description】

Defines the size information structure.

【Definition】

typedef struct {
&emsp;k_u32 width;
&emsp;k_u32 height;
} k_vo_size;

【Members】

| Member name | description |
|----------|------|
| width    | width |
| height   | height |

【Note】

none

【See Also】

none

#### 3.1.11 k_vo_video_layer_attr

【Description】

Define the display layer layer properties

【Definition】

typedef struct {
&emsp;k_point display_rect;
&emsp;k_size img_size;
&emsp;k_pixel_format pixel_format;
&emsp;k_u32 stride;
&emsp;k_u32 uv_swap_en;
&emsp;k_u32 alptha_tpye;
} k_vo_video_layer_attr;

【Members】

| Member name      | description                                                                                                                                                            |
|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------|
| display_rect; | The starting position of the OSD layer                                                                                                                                             |
| img_size      | Image resolution structure, that is, the size of the composite picture                                                                                                                              |
| pixel_format  | Supported data formats for the video layer                                                                                                                                            |
| stride        | Stride of images                                                                                                                                                    |
| uv_swap_en    | UV swap                                                                                                                                                         |
| alptha_tpye   | The type of Alptha that is used only in the OSD layer. It is divided into fixed alpha (which can be divided into 256 levels), R in RGB as the alpha channel, G in RGB as the alpha channel, B in RGB as the alpha channel, and alpha channel as alpha |

【Note】

alptha_tpye is only used for the OSD layer

【See Also】

none

#### 3.1.12 k_vo_wbc_attr

【Description】

Define the writeback property.

【Definition】

typedef struct {
&emsp;[k_vo_size](#3110-k_vo_size) target_size;
&emsp;[k_pixel_format](#313-k_pixel_format) pixel_format;
&emsp;k_u32 stride;
&emsp;k_u32 y_phy_addr;
} k_vo_wbc_attr;

【Members】

| Member name       | description       |
|---------------|------------|
| target_size   | The target size for write-back  |
| pixel_format  | The format of the data that is written back |
| pixel_format  | data format   |
| stride;       | Stride written back   |
| y_addr        | The physical address of the image write-back    |

【Note】

y_addr Space needs to be allocated

【See Also】

none

#### 3.1.13 k_vo_pub_attr

【Description】

Configure the public properties of the video output device.

【Definition】

typedef struct {
&emsp;k_u32 bg_color;
&emsp;[k_vo_intf_type](#312-k_vo_intf_type) intf_type;
&emsp;[k_vo_intf_sync](#311-k_vo_intf_sync) intf_sync;
&emsp;[k_vo_display_resolution](#3116-k_vo_display_resolution) \*sync_info;
&emsp;} k_vo_pub_attr;

【Members】

|           |                          |
|-----------|--------------------------|
| Member name  | description                     |
| bg_color  | Background color                   |
| type      | Interface type, currently only MIPI is supported |
| intf_sync | Resolution and frame rate in the video     |
| sync_info | The timing of the image output           |

【Note】

none

【See Also】

none

#### 3.1.14 k_vo_scaler_attr

【Description】

Define the scaler property

【Definition】

typedef struct{
&emsp;k_size in_size;
&emsp;k_size out_size;
&emsp;k_u32 stride;
}k_vo_scaler_attr;

【Members】

| Member name | description               |
|----------|--------------------|
| in_size  | The dimensions entered         |
| out_size | The dimensions of the output         |
| stride   | stride       |
| y_addr   | The physical address of the image write-back |

【Note】

none

【See Also】

none

#### 3.1.15 k_vo_draw_frame

【Description】

Defines the properties of the frame

【Definition】

typedef struct {
&emsp;k_u32 draw_en;
&emsp;k_u32 line_x_start;
&emsp;k_u32 line_y_start;
&emsp;k_u32 line_x_end;
&emsp;k_u32 line_y_end;
&emsp;k_u32 frame_num;
}k_vo_draw_frame;

【Members】

| Member name     | description                     |
|--------------|--------------------------|
| draw_en      | Picture frame enabled                 |
| line_x_start | The start in the X direction             |
| line_y_start | The start of the y direction         |
| line_x_end   | The end point in the X direction          |
| line_y_end   | The end point in the y direction          |
| frame_num    | num sign in the current box [0 - 16] |

【Note】

none

【See Also】

none

#### 3.1.16 k_vo_display_resolution

【Description】

Display timing。

【Definition】

typedef struct{
&emsp;k_u32 PCLK;
&emsp;k_u32 phyclk;
&emsp;k_u32 htotal;
&emsp;k_u32 hdisplay;
&emsp;k_u32 hsync_len;
&emsp;k_u32 hback_porch;
&emsp;k_u32 hfront_porch;
&emsp;k_u32 vtotal;
&emsp;k_u32 vdisplay;
&emsp;k_u32 vsync_len;
&emsp;k_u32 vback_porch;
&emsp;k_u32 vfront_porch;
} k_vo_display_resolution;

【Members】

| Member name     | description               |
|--------------|--------------------|
| pclk         | The pix clk frequency of VO  |
| phyclk       |  The frequency of D-Phy      |
| htotal       | The total pixels of a row       |
| hdisplay     | The number of valid pixels per row |
| hsync_len    | The number of pixels that the row synchronizes   |
| hback_porch  | The number of pixels on the back porch |
| hfront_porch | The number of pixels on the front porch |
| vtotal       | Total number of rows             |
| vdisplay     | The number of rows valid for one frame     |
| vsync_len    | The number of pixels in which the frame is synchronized   |
| vback_porch  | The number of rows on the back porch   |
| vfront_porch | The number of rows on the front porch   |

【Note】

none

【See Also】

none

#### 3.1.17 k_vo_mipi_phy_attr

【Description】

A structure that defines the MIPI PHY frequency

【Definition】

typedef struct {
&emsp;k_u32 n;
&emsp;k_u32 m;
&emsp;k_u32 voc;
&emsp;k_u32 phy_lan_num;
&emsp;k_u32 hs_freq;
}k_vo_mipi_phy_attr;

【Members】

| Member name    | description           |
|-------------|----------------|
| n           | Pll coefficient       |
| m           | Pll coefficient       |
| voc         | Pll coefficient       |
| hs_freq     | The frequency range of Phy |
| phy_lan_num | The number of LANs for Phy |

【Note】

none

【See Also】

none

#### 3.1.18 k_vo_video_osd_attr

【Description】

Configure the public properties of the OSD layer.

【Definition】

typedef struct {
&emsp;[k_vo_point](#3110-k_vo_size) display_rect;
&emsp;[k_vo_size](#3110-k_vo_size) img_size;
&emsp;[k_pixel_format](#313-k_pixel_format) pixel_format;
&emsp;k_u32 stride;
&emsp;k_u8 global_alptha;
} k_vo_video_osd_attr;

【Members】

| Member name      | description       |
|---------------|------------|
| display_rect  | Location information   |
| img_size      | Valid size |
| pixel_format  | data format   |
| stride;       | Stride     |
| global_alptha | transparency     |

【Note】

none

【See Also】

none

#### 3.1.19 k_video_frame_info

【Description】

One frame of information.

【Definition】

typedef struct {
&emsp;k_video_frame v_frame;
&emsp;k_u32 pool_id;
&emsp;k_mod_id mod_id;
} k_video_frame_info;

【Members】

| Member name | description        |
|----------|-------------|
| v_frame  | Information of the frame |
| pool_id  | VB Party ID  |
| mod_id   | The ID of the video frame |

【Note】

none

【See Also】

none

#### 3.1.20 k_connector_type

【Description】

The type of connection screen.

【Definition】

typedef enum {
&emsp;HX8377_V2_MIPI_4LAN_1080X1920_30FPS;
&emsp;LT9611_MIPI_4LAN_1920X1080_30FPS;
} k_connector_type;

【Members】

| Member name | description                                           |
|----------|-----------------------------------------------|
| v_frame  | Information about the frame                                      |
| HX8377_V2_MIPI_4LAN_1080X1920_30FPS  | HX8377 Screen initialization  |
| LT9611_MIPI_4LAN_1920X1080_30FPS   | HDMI 1080p initialization |

【Note】

none

【See Also】

none

#### 3.1.21 k_dsi_lan_num

【Description】

The number of lanes for DSI.

【Definition】

typedef enum {
&emsp;K_DSI_1LAN = 0,
&emsp;K_DSI_2LAN = 1,
&emsp;K_DSI_4LAN = 3,
} k_dsi_lan_num;

【Members】

| Member name | description        |
|----------|-------------|
| K_DSI_1LAN  | 1-line mode    |
| K_DSI_2LAN  | 2-wire mode |
| K_DSI_4LAN   | 4-wire mode |

【Note】

none

【See Also】

none

#### 3.1.22 k_dsi_work_mode

【Description】

The operating mode of DSI

【Definition】

typedef enum{
&emsp;K_BURST_MODE = 0,
&emsp;K_NON_BURST_MODE_WITH_SYNC_EVENT = 1,
&emsp;K_NON_BURST_MODE_WITH_PULSES = 2,
} k_dsi_work_mode;

【Members】

| Member name | description        |
|----------|-------------|
| K_BURST_MODE  | DSI works in Brust Mode    |
| K_NON_BURST_MODE_WITH_SYNC_EVENT  | DSi work in Non Brust Event Mode |
| K_NON_BURST_MODE_WITH_PULSES   | DSI work in Non Brust Pulses Mode |

【Note】

none

【See Also】

none

#### 3.1.23 k_vo_dsi_cmd_mode

【Description】

The pattern in which DSI sends commands.

【Definition】

typedef enum {
&emsp;K_VO_LP_MODE,
&emsp;K_VO_HS_MODE,
} k_vo_dsi_cmd_mode;

【Members】

| Member name | description        |
|----------|-------------|
| K_VO_LP_MODE  | LP mode sends commands    |
| K_VO_HS_MODE  | HS mode sends commands |

【Note】

none

【See Also】

none

#### 3.1.24 k_connectori_phy_attr

【Description】

Connector Connector Configuration PHY information.

【Definition】

typedef struct {
&emsp;k_u32 n;
&emsp;k_u32 m;
&emsp;k_u32 voc;
&emsp;k_u32 hs_freq;
} k_connectori_phy_attr;

【Members】

| Member name | description        |
|----------|-------------|
| n        | Pll coefficient    |
| m        | Pll coefficient    |
| voc      | Pll coefficient    |
| hs_freq  | The frequency range of Phy |

【Note】

none

【See Also】

none

#### 3.1.25 k_connector_info

【Description】

Information about the connector.

【Definition】

typedef struct {
&emsp;const char *connector_name;
&emsp;k_u32 screen_test_mode;
&emsp;k_u32 dsi_test_mode;
&emsp;k_u32 bg_color;
&emsp;k_u32 intr_line;
&emsp;[k_dsi_lan_num](#3121-k_dsi_lan_num) lan_num;
&emsp;[k_dsi_work_mode](#3122-k_dsi_work_mode) work_mode;
&emsp;[k_vo_dsi_cmd_mode](#3123-k_vo_dsi_cmd_mode) cmd_mode;
&emsp;[k_connectori_phy_attr](#3124-k_connectori_phy_attr) phy_attr;
&emsp;[k_vo_display_resolution](#3116-k_vo_display_resolution) resolution;
&emsp;[k_connector_type](#3120-k_connector_type) type;
} k_connector_info;

【Members】

| Member name | description        |
|----------|-------------|
| connector_name | connector name |
| screen_test_mode | screen test mode |
| dsi_test_mode | dsi test mode |
| bg_color | background color |
| intr_line | Break line number |
| work_mode | dsi work mode |
| phy_attr | Parameters of mipi phy |
| lan_num | mipi lan num |
| resolution | Parameters of display |
| type | connector type |

【Note】

none

【See Also】

none

## 4. Error codes

Table 41 VO API error codes

| Error code   | Macro definitions                 | description           |
|------------|------------------------|----------------|
| 0xa00b8006 | K_ERR_VO_NULL_PTR      | Parameter null pointer error |
| 0xa00b8001 | K_ERR_VO_INVALID_DEVID | Invalid dev id     |
| 0xa00b8002 | K_ERR_VO_INVALID_CHNID | Invalid chn id    |
| 0xa00b8005 | K_ERR_VO_UNEXIST       | The video cache does not exist |
| 0xa00b8004 | K_ERR_VO_EXIST         | Video cache exists   |
| 0xa00b8003 | K_ERR_VO_ILLEGAL_PARAM | The parameter setting is invalid   |
| 0xa00b8010 | K_ERR_VO_NOTREADY      | VO is not ready     |
| 0xa00b8012 | K_ERR_VO_BUSY          | The system is busy         |
| 0xa00b8007 | K_ERR_VO_NOT_CONFIG    | Configuration is not allowed     |
| 0xa00b8008 | K_ERR_VO_NOT_SUPPORT   | Unsupported operations   |
| 0xa00b8009 | K_ERR_VO_NOT_PERM      | Operation is not allowed     |
| 0xa00b800c | K_ERR_VO_NOMEM         | Failed to allocate memory   |
| 0xa00b800d | K_ERR_VO_NOBUF         | No buffs       |
| 0xa00b800e | K_ERR_VO_BUF_EMPTY     | Buf is empty       |
| 0xa00b800f | K_ERR_VO_BUF_FULL      | Buf is full       |
| 0xa00b8011 | K_ERR_VO_BADADDR       | Wrong address     |
| 0xa00b8012 | K_ERR_VO_BUSY          | The system is busy         |
