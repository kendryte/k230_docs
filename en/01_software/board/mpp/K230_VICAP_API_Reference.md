# K230 VICAP API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No part of this document may be excerpted, copied, or disseminated in any form without prior written permission from the Company.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly guides application developers on how to obtain image data through the VICAP module and describes the basic functions of various module APIs.

### Intended Audience

This document (this guide) is primarily intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
|              |             |

### Revision History

| Document Version | Modification Description                                                                                                           | Modifier       | Date       |
|------------------|------------------------------------------------------------------------------------------------------------------------------------|----------------|------------|
| V1.0             | Initial version                                                                                                                    | Chenggen Wang  | 2023/4/4   |
| V1.1             | Modified VICAP overview 2, added API and data type navigation                                                                      | Zhongxiang Zhao| 2023/4/6   |
| V1.2             | Removed ISP related interfaces, added API and data type descriptions, separated sensor interface from libvicap library to libsensor library, added ov9286 infrared/scatter type, updated VICAP description, updated document format | Shidong Guo, Chenggen Wang | 2023/4/26 |

## 1. Overview

### 1.1 Overview

The VICAP subsystem is responsible for video image input capture and processing in the K230 SOC. It processes signals output by the sensor in real-time to obtain restored and enhanced digital images that are closer to what the human eye sees in reality. It mainly includes MIPI RxDphy, MIPI CSI, ISP, and DW. MIPI is used to receive high-speed differential signals from the sensor and convert them to the DVP interface for ISP processing; ISP is used for image information processing; DW is used for fisheye correction and multi-channel resize output.

This document mainly describes the application programming interface of the VICAP module, which provides application developers with operational interfaces and configuration parameters for capturing video image data through the VICAP module.

### 1.2 Function Description

#### 1.2.1 VICAP

The VICAP module is an abstract description of the entire image acquisition and processing unit.

The VICAP hardware consists of four major modules: Sensor, VI, ISP, and Dewarp (as shown in Figure 1-1). It supports up to 3 sensors simultaneously. The MCM module inside the ISP implements time-division multiplexing management of multiple sensors. The output data of multiple sensors is written to DDR through the Memory Interface's Write interface of the MCM, and then read and loaded into the ISP Pipeline for processing.

![Diagram automatically generated](../../../../zh/01_software/board/mpp/images/745a46d8e083d93521d0c5233bdaccdd.png)

Figure 1-1 VICAP Hardware Architecture Diagram

The VICAP software architecture is shown in Figure 1-2, from top to bottom: Application Interface Layer, Media Interface Layer, System Framework Layer, Driver Layer, and Hardware Layer.

- Application Interface Layer: Provides API interfaces in the form of kd_mapi_vicap_xxx and usage instructions. It further encapsulates the functional interfaces provided by each sub-module of the Media Interface Layer to simplify the application development process.
- Media Interface Layer: This layer consists of various sub-modules of VICAP, each providing its own media interface API encapsulation.
- Framework Layer: Responsible for the control and management of the entire system software functions and business logic of VICAP. It integrates and unifies the interfaces and functions provided by each sub-module to form a complete VICAP system control logic and process.
- Driver Layer: A collection of kernel driver functions for various hardware modules of VICAP.
- Hardware Layer: A collection of specific hardware modules of VICAP, including sensors.

![GUI, Text, Application automatically generated](../../../../zh/01_software/board/mpp/images/250b6c36cbd4447bd8c734548fc3b890.png)

#### 1.2.2 Sensor

The Sensor module is one of the data sources for VICAP image capture, responsible for configuring the operating parameters and working modes of the image sensor unit.

The K230 platform supports a variety of sensor interface types. We will use the current most commonly used MIPI CSI interface sensor as an example. The hardware connection diagram between the sensor and the main control platform is as follows:

![Diagram automatically generated](../../../../zh/01_software/board/mpp/images/e20100e34c268ad615e69966cb28e5a6.png)

Figure 1-3

The main control sends configuration register control to the sensor through the I2C interface, and the sensor sends image data to the main control SOC through the MIPI CSI interface.

The system architecture of the Sensor module is shown in Figure 1-4:

![GUI, Application, Email automatically generated](../../../../zh/01_software/board/mpp/images/camera_sensor_arch.png)

Figure 1-4 Sensor System Architecture Diagram

From top to bottom: Media Interface Layer, Hardware Driver Layer, and Hardware Layer

- Media Interface Layer: Provides kd_mpi_sensor_xxx interfaces for external modules to operate and access sensor devices.
- Driver Layer: This layer mainly includes two parts: sensor_dev and sensor_drv.
  - sensor_dev: Responsible for registering device driver files and providing the implementation process of file operation interfaces. By registering device file nodes /dev/sensorxx, it allows user-space programs to access the kernel driver.
  - sensor_drv: Specific sensor hardware driver, encapsulating operations on the sensor into a unified interface.
- Hardware Layer: Sensor module hardware, supporting up to three hardware sensors simultaneously in the current system.

## 2. API Reference

### 2.1 VICAP

This functional module provides the following APIs:

- [kd_mpi_vicap_get_sensor_info](#211-kd_mpi_vicap_get_sensor_info)
- [kd_mpi_vicap_set_dev_attr](#212-kd_mpi_vicap_set_dev_attr)
- [kd_mpi_vicap_get_dev_attr](#213-kd_mpi_vicap_get_dev_attr)
- [kd_mpi_vicap_set_chn_attr](#214-kd_mpi_vicap_set_chn_attr)
- [kd_mpi_vicap_get_chn_attr](#215-kd_mpi_vicap_get_chn_attr)
- [kd_mpi_vicap_init](#216-kd_mpi_vicap_init)
- [kd_mpi_vicap_deinit](#217-kd_mpi_vicap_deinit)
- [kd_mpi_vicap_start_stream](#218-kd_mpi_vicap_start_stream)
- [kd_mpi_vicap_stop_stream](#219-kd_mpi_vicap_stop_stream)
- [kd_mpi_vicap_dump_frame](#2110-kd_mpi_vicap_dump_frame)
- [kd_mpi_vicap_dump_release](#2111-kd_mpi_vicap_dump_release)
- [kd_mpi_vicap_set_vi_drop_frame](#2112-kd_mpi_vicap_set_vi_drop_frame)
- [kd_mpi_vicap_set_mclk](#2113-kd_mpi_vicap_set_mclk)
- [kd_mpi_vicap_set_dump_reserved](#2114-kd_mpi_vicap_set_dump_reserved)
- [kd_mpi_vicap_set_slave_enable](#2115-kd_mpi_vicap_set_slave_enable)
- [kd_mpi_vicap_set_slave_attr](#2116-kd_mpi_vicap_set_slave_attr)
- [kd_mpi_vicap_3d_mode_crtl](#2117-kd_mpi_vicap_3d_mode_crtl)

#### 2.1.1 kd_mpi_vicap_get_sensor_info

[Description]

Get sensor configuration information based on the specified sensor configuration type.

[Syntax]

k_s32 kd_mpi_vicap_get_sensor_info(k_vicap_sensor_type sensor_type, k_vicap_sensor_info \*sensor_info)

[Parameters]

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| sensor_type        | Sensor configuration type | Input         |
| sensor_info        | Sensor configuration information | Output     |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

[Requirements]

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

[Note]

Application developers need to first call this API to get sensor configuration information based on the sensor configuration type they need to use, and then call subsequent interfaces to initialize other VICAP modules based on the configuration information.

[Example]

None.

[Related Topics]

#### 2.1.2 kd_mpi_vicap_set_dev_attr

[Description]

Set VICAP device attributes.

[Syntax]

k_s32 kd_mpi_vicap_set_dev_attr(k_vicap_dev dev_num, k_vicap_dev_attr dev_attr)

[Parameters]

| **Parameter Name** | **Description**      | **Input/Output** |
|--------------------|----------------------|------------------|
| dev_num            | VICAP device number  | Input            |
| dev_attr           | VICAP device attributes | Input          |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

[Requirements]

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

[Note]

None.

[Example]

None.

[Related Topics]

#### 2.1.3 kd_mpi_vicap_get_dev_attr

[Description]

Get VICAP device attributes.

[Syntax]

k_s32 kd_mpi_vicap_get_dev_attr(k_vicap_dev dev_num, k_vicap_dev_attr \*dev_attr)

[Parameters]

| **Parameter Name** | **Description**      | **Input/Output** |
|--------------------|----------------------|------------------|
| dev_num            | VICAP device number  | Input            |
| dev_attr           | VICAP device attributes | Output         |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

[Requirements]

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

[Note]

None.

[Example]

None.

[Related Topics]

#### 2.1.4 kd_mpi_vicap_set_chn_attr

[Description]

Set VICAP channel attributes.

[Syntax]

k_s32 kd_mpi_vicap_set_chn_attr(k_vicap_dev dev_num, k_vicap_chn chn_num, k_vicap_chn_attr chn_attr)

[Parameters]

| **Parameter Name** | **Description**          | **Input/Output** |
|--------------------|--------------------------|------------------|
| dev_num            | VICAP device number      | Input            |
| chn_num            | VICAP output channel number | Input        |
| chn_attr           | VICAP output channel attributes | Input |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

[Requirements]

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

[Note]

None.

[Example]

None.

[Related Topics]

#### 2.1.5 kd_mpi_vicap_get_chn_attr

[Description]

Get VICAP channel attributes.

[Syntax]

k_s32 kd_mpi_vicap_get_chn_attr(k_vicap_dev dev_num, k_vicap_chn chn_num, k_vicap_chn_attr \*chn_attr)

[Parameters]

| **Parameter Name** | **Description**          | **Input/Output** |
|--------------------|--------------------------|------------------|
| dev_num            | VICAP device number      | Input            |
| chn_num            | VICAP output channel number | Input        |
| chn_attr           | VICAP output channel attributes | Output |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

[Requirements]

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

[Note]

None.

[Example]

None.

[Related Topics]

#### 2.1.6 kd_mpi_vicap_init

[Description]

VICAP device initialization.

[Syntax]

k_s32 kd_mpi_vicap_init(k_vicap_dev dev_num)

[Parameters]

| **Parameter Name** | **Description**    | **Input/Output** |
|--------------------|--------------------|------------------|
| dev_num            | VICAP device number | Input           |

[Return Value]

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

[Chip Differences]

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

Before using this interface, you need to call `kd_mpi_vicap_set_dev_attr` to set the device attributes, and then call `kd_mpi_vicap_set_chn_attr` to set the output channel attributes.

**Example**:

None

**Related Topics**:

#### 2.1.7 kd_mpi_vicap_deinit

**Description**:

Deinitialize the VICAP device.

**Syntax**:

```c
k_s32 kd_mpi_vicap_deinit(k_vicap_dev dev_num)
```

**Parameters**:

| **Parameter Name** | **Description**    | **Input/Output** |
|--------------------|--------------------|------------------|
| dev_num            | VICAP device number | Input           |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.1.8 kd_mpi_vicap_start_stream

**Description**:

Start the VICAP device output data stream.

**Syntax**:

```c
k_s32 kd_mpi_vicap_start_stream(k_vicap_dev dev_num)
```

**Parameters**:

| **Parameter Name** | **Description**    | **Input/Output** |
|--------------------|--------------------|------------------|
| dev_num            | VICAP device number | Input           |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.1.9 kd_mpi_vicap_stop_stream

**Description**:

Stop the VICAP device data stream output.

**Syntax**:

```c
k_s32 kd_mpi_vicap_stop_stream(k_vicap_dev dev_num)
```

**Parameters**:

| **Parameter Name** | **Description**    | **Input/Output** |
|--------------------|--------------------|------------------|
| dev_num            | VICAP device number | Input           |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.1.10 kd_mpi_vicap_dump_frame

**Description**:

Dump VICAP data based on the specified device and output channel.

**Syntax**:

```c
k_s32 kd_mpi_vicap_dump_frame(k_vicap_dev dev_num, k_vicap_chn chn_num, k_vicap_dump_format format,
k_video_frame_info *vf_info, k_u32 milli_sec)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| dev_num            | VICAP device number    | Input            |
| chn_num            | VICAP output channel number | Input        |
| format             | Dump data type         | Input            |
| vf_info            | Dump frame information | Output           |
| milli_sec          | Timeout duration       | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.1.11 kd_mpi_vicap_dump_release

**Description**:

Release the dumped data frame.

**Syntax**:

```c
k_s32 kd_mpi_vicap_dump_release(k_vicap_dev dev_num, k_vicap_chn chn_num, const k_video_frame_info *vf_info)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| dev_num            | VICAP device number    | Input            |
| chn_num            | VICAP output channel number | Input        |
| vf_info            | Dump frame information | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.1.12 kd_mpi_vicap_set_vi_drop_frame

**Description**:

Set hardware frame drop.

**Syntax**:

```c
k_s32 kd_mpi_vicap_set_vi_drop_frame(k_vicap_csi_num csi, k_vicap_drop_frame *frame, k_bool enable)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| csi                | VICAP device number    | Input            |
| frame              | Structure, see below   |                  |
| m                  | Drop n frames every m frames | Input      |
| n                  | Drop n frames every m frames | Input      |
| mode               | HDR mode               | Input            |
| enable             | Enable or disable      | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

#### 2.1.13 kd_mpi_vicap_set_mclk

**Description**:

Set MCLK frequency.

**Syntax**:

```c
k_s32 kd_mpi_vicap_set_mclk(k_vicap_mclk_id id, k_vicap_mclk_sel sel, k_u8 mclk_div, k_u8 mclk_en)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| id                 | MCLK ID                | Input            |
| sel                | Clock source           | Input            |
| mclk_div           | Division factor        | Input            |
| mclk_en            | Enable or disable      | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

#### 2.1.14 kd_mpi_vicap_set_dump_reserved

**Description**:

Set whether to enable fast dump mode.

**Syntax**:

```c
void kd_mpi_vicap_set_dump_reserved(k_vicap_dev dev_num, k_vicap_chn chn_num, k_bool reserved)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| dev_num            | VICAP device number    | Input            |
| chn_num            | VICAP output channel number | Input        |
| reserved           | Enable fast dump mode  | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

#### 2.1.15 kd_mpi_vicap_set_slave_enable

**Description**:

Enable slave mode.

**Syntax**:

```c
k_s32 kd_mpi_vicap_set_slave_enable(k_vicap_slave_id id, k_vicap_slave_enable *enable)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| id                 | Slave mode ID          | Input            |
| enable             | Enable or disable slave mode | Input      |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

#### 2.1.16 kd_mpi_vicap_set_slave_attr

**Description**:

Set slave mode parameters.

**Syntax**:

```c
k_s32 kd_mpi_vicap_set_slave_attr(k_vicap_slave_id id, k_vicap_slave_info *info)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| id                 | Slave mode ID          | Input            |
| info               | Slave mode parameters  | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

#### 2.1.17 kd_mpi_vicap_3d_mode_crtl

**Description**:

Enable 3D mode.

**Syntax**:

```c
k_s32 kd_mpi_vicap_3d_mode_crtl(k_bool enable)
```

**Parameters**:

| **Parameter Name** | **Description**        | **Input/Output** |
|--------------------|------------------------|------------------|
| enable             | Enable 3D mode         | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

### 2.2 Sensor

This functional module provides the following APIs:

- [kd_mpi_sensor_open](#221-kd_mpi_sensor_open)
- [kd_mpi_sensor_close](#222-kd_mpi_sensor_close)
- [kd_mpi_sensor_power_set](#223-kd_mpi_sensor_power_set)
- [kd_mpi_sensor_id_get](#224-kd_mpi_sensor_id_get)
- [kd_mpi_sensor_init](#225-kd_mpi_sensor_init)
- [kd_mpi_sensor_reg_read](#226-kd_mpi_sensor_reg_read)
- [kd_mpi_sensor_reg_write](#227-kd_mpi_sensor_reg_write)
- [kd_mpi_sensor_mode_get](#228-kd_mpi_sensor_mode_get)
- [kd_mpi_sensor_mode_set](#229-kd_mpi_sensor_mode_set)
- [kd_mpi_sensor_stream_enable](#2210-kd_mpi_sensor_stream_enable)
- [kd_mpi_sensor_again_set](#2211-kd_mpi_sensor_again_set)
- [kd_mpi_sensor_again_get](#2212-kd_mpi_sensor_again_get)
- [kd_mpi_sensor_dgain_set](#2213-kd_mpi_sensor_dgain_set)
- [kd_mpi_sensor_dgain_get](#2214-kd_mpi_sensor_dgain_get)
- [kd_mpi_sensor_intg_time_set](#2215-kd_mpi_sensor_intg_time_set)
- [kd_mpi_sensor_intg_time_get](#2216-kd_mpi_sensor_intg_time_get)
- [kd_mpi_sensor_otpdata_get](#2217-kd_mpi_sensor_otpdata_get)
- [kd_mpi_sensor_otpdata_set](#2218-kd_mpi_sensor_otpdata_set)

#### 2.2.1 kd_mpi_sensor_open

**Description**:

Open the sensor device based on the sensor device name.

**Syntax**:

```c
k_s32 kd_mpi_sensor_open(const char *sensor_name)
```

**Parameters**:

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| sensor_name        | Sensor device name    | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| Positive value   | Success. Returns device descriptor |
| Negative value   | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.2 kd_mpi_sensor_close

**Description**:

Close the sensor device.

**Syntax**:

```c
k_s32 kd_mpi_sensor_close (k_s32 fd)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.3 kd_mpi_sensor_power_set

**Description**:

Set the sensor power state.

**Syntax**:

```c
k_s32 kd_mpi_sensor_power_set(k_s32 fd, k_bool on)
```

**Parameters**:

| **Parameter Name** | **Description**                                      | **Input/Output** |
|--------------------|------------------------------------------------------|------------------|
| fd                 | Sensor device file descriptor                        | Input            |
| on                 | Set sensor power state, K_TRUE: power on, K_FALSE: power off | Input          |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.4 kd_mpi_sensor_id_get

**Description**:

Get the sensor ID.

**Syntax**:

```c
k_s32 kd_mpi_sensor_id_get(k_s32 fd, k_u32 *sensor_id)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| sensor_id          | Acquired sensor ID          | Output           |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.5 kd_mpi_sensor_init

**Description**:

Initialize the sensor.

**Syntax**:

```c
k_s32 kd_mpi_sensor_init(k_s32 fd, k_sensor_mode mode)
```

**Parameters**:

| **Parameter Name** | **Description**                                    | **Input/Output** |
|--------------------|----------------------------------------------------|------------------|
| fd                 | Sensor device file descriptor                      | Input            |
| mode               | Initialize sensor configuration registers based on the specified sensor mode | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.6 kd_mpi_sensor_reg_read

**Description**:

Read the content of the sensor register.

**Syntax**:

```c
k_s32 kd_mpi_sensor_reg_read(k_s32 fd, k_u32 reg_addr, k_u32 *reg_val)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| reg_addr           | Sensor register address     | Input            |
| reg_val            | Content of the read register | Output           |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.7 kd_mpi_sensor_reg_write

**Description**:

Write content to the sensor register.

**Syntax**:

```c
k_s32 kd_mpi_sensor_reg_write(k_s32 fd, k_u32 reg_addr, k_u32 reg_val)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| reg_addr           | Sensor register address     | Input            |
| reg_val            | Content to write to the sensor register | Input      |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.8 kd_mpi_sensor_mode_get

**Description**:

Get the sensor mode configuration.

**Syntax**:

```c
k_s32 kd_mpi_sensor_mode_get(k_s32 fd, k_sensor_mode *mode)
```

**Parameters**:

| **Parameter Name** | **Description**                      | **Input/Output** |
|--------------------|--------------------------------------|------------------|
| fd                 | Sensor device file descriptor        | Input            |
| mode               | Acquired sensor mode configuration parameters | Output    |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.9 kd_mpi_sensor_mode_set

**Description**:

Set the sensor mode configuration.

**Syntax**:

```c
k_s32 kd_mpi_sensor_mode_set(k_s32 fd, k_sensor_mode mode)
```

**Parameters**:

| **Parameter Name** | **Description**                | **Input/Output** |
|--------------------|---------------------------------|------------------|
| fd                 | Sensor device file descriptor   | Input            |
| mode               | Sensor mode configuration parameters | Input        |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.10 kd_mpi_sensor_stream_enable

**Description**:

Set the sensor mode configuration.

**Syntax**:

```c
k_s32 kd_mpi_sensor_stream_enable(k_s32 fd, k_s32 enable)
```

**Parameters**:

| **Parameter Name** | **Description**                                         | **Input/Output** |
|--------------------|---------------------------------------------------------|------------------|
| fd                 | Sensor device file descriptor                           | Input            |
| enable             | Set sensor stream output state, 0: disable output, non-0: enable output | Input          |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.11 kd_mpi_sensor_again_set

**Description**:

Set the sensor analog gain.

**Syntax**:

```c
k_s32 kd_mpi_sensor_again_set(k_s32 fd, k_sensor_gain gain)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| gain               | Gain configuration parameters | Input          |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.12 kd_mpi_sensor_again_get

**Description**:

Get the sensor analog gain.

**Syntax**:

```c
k_s32 kd_mpi_sensor_again_get(k_s32 fd, k_sensor_gain *gain)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| gain               | Gain configuration parameters | Output         |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.13 kd_mpi_sensor_dgain_set

**Description**:

Set the sensor digital gain.

**Syntax**:

```c
k_s32 kd_mpi_sensor_dgain_set(k_s32 fd, k_sensor_gain gain)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| gain               | Gain configuration parameters | Input          |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.14 kd_mpi_sensor_dgain_get

**Description**:

Get the sensor digital gain.

**Syntax**:

```c
k_s32 kd_mpi_sensor_dgain_get(k_s32 fd, k_sensor_gain *gain)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| gain               | Gain configuration parameters | Output         |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.15 kd_mpi_sensor_intg_time_set

**Description**:

Set the sensor integration time.

**Syntax**:

```c
k_s32 kd_mpi_sensor_intg_time_set(k_s32 fd, k_sensor_intg_time time)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| time               | Integration time configuration parameters | Input      |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.16 kd_mpi_sensor_intg_time_get

**Description**:

Get the sensor integration time.

**Syntax**:

```c
k_s32 kd_mpi_sensor_intg_time_get(k_s32 fd, k_sensor_intg_time *time)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| time               | Integration time configuration parameters | Output     |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.17 kd_mpi_sensor_otpdata_get

**Description**:

Get the sensor OTP data.

**Syntax**:

```c
k_s32 kd_mpi_sensor_otpdata_get(k_s32 fd, void *otp_data)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| otp_data           | OTP data                     | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

#### 2.2.18 kd_mpi_sensor_otpdata_set

**Description**:

Set the sensor OTP data.

**Syntax**:

```c
k_s32 kd_mpi_sensor_otpdata_set(k_s32 fd, void *otp_data)
```

**Parameters**:

| **Parameter Name** | **Description**             | **Input/Output** |
|--------------------|-----------------------------|------------------|
| fd                 | Sensor device file descriptor | Input          |
| otp_data           | OTP data                     | Input            |

**Return Value**:

| **Return Value** | **Description**               |
|------------------|-------------------------------|
| 0                | Success.                      |
| Non-zero         | Failure, refer to error code. |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_sensor_api.h
- Library file: libsensor.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

## 3. Data Types

### 3.1 VICAP

The related data types for this functional module are defined as follows:

- [k_vicap_sensor_type](#311-k_vicap_sensor_type)
- [k_vicap_dev](#312-k_vicap_dev)
- [k_vicap_chn](#313-k_vicap_chn)
- [k_vicap_csi_num](#314-k_vicap_csi_num)
- [k_vicap_mipi_lanes](#315-k_vicap_mipi_lanes)
- [k_vicap_csi_data_type](#316-k_vicap_csi_data_type)
- [k_vicap_data_source](#317-k_vicap_data_source)
- [k_vicap_vi_dvp_port](#318-k_vicap_vi_dvp_port)
- [k_vicap_vi_flash_mode](#319-k_vicap_vi_flash_mode)
- [k_vicap_img_window](#3110-k_vicap_img_window)
- [k_vicap_work_mode](#3111-k_vicap_work_mode)
- [k_vicap_sensor_info](#3112-k_vicap_sensor_info)
- [k_vicap_dump_format](#3113-k_vicap_dump_format)
- [k_vicap_dev_attr](#3114-k_vicap_dev_attr)
- [k_vicap_chn_attr](#3115-k_vicap_chn_attr)

### 3.1.1 k_vicap_sensor_type

**Description**: Definition of sensor types supported by the current system.

**Definition**:

```c
typedef enum {
    OV_OV9732_MIPI_1280X720_30FPS_10BIT_LINEAR = 0,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_IR = 1,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_SPECKLE = 2,
    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_IR = 3,
    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_SPECKLE = 4,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_IR_SPECKLE = 5,
    OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_IR_SPECKLE = 6,
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
    OV_OV5647_MIPI_CSI1_1920X1080_30FPS_10BIT_LINEAR = 27,
    OV_OV5647_MIPI_CSI2_1920X1080_30FPS_10BIT_LINEAR = 28,
    XS9922B_MIPI_CSI0_1280X720_30FPS_YUV422_DOL3 = 29,
    XS9950_MIPI_CSI0_1280X720_30FPS_YUV422 = 30,
    XS9950_MIPI_CSI1_1280X720_30FPS_YUV422 = 31,
    XS9950_MIPI_CSI2_1280X720_30FPS_YUV422 = 32,
    XS9950_MIPI_CSI0_1920X1080_30FPS_YUV422 = 33,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_SPECKLE_V2 = 34,
    OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_IR_V2 = 35,
    OV_OV9732_MIPI_1280X720_30FPS_10BIT_MCLK_16M_LINEAR_V2 = 36,
    OV_OV5647_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR_V2 = 37,
    OV_OV5647_MIPI_CSI1_1920X1080_30FPS_10BIT_LINEAR_V2 = 38,
    OV_OV5647_MIPI_CSI2_1920X1080_30FPS_10BIT_LINEAR_V2 = 39,
    GC2053_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR = 40,
    SENSOR_TYPE_MAX,
} k_vicap_sensor_type;
```

**Members**:

| **Member Name**                                      | **Description**                                                                 |
|------------------------------------------------------|---------------------------------------------------------------------------------|
| OV_OV9732_MIPI_1280X720_30FPS_10BIT_LINEAR           | OV9732 1-lane 10-bit 720P 30fps linear output configuration, external crystal 16M, connected to CSI0 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_IR        | OV9286 2-lane 10-bit 720P 30fps linear output configuration for IR image, external crystal 25M, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_LINEAR_SPECKLE   | OV9286 2-lane 10-bit 720P 30fps linear output configuration for speckle image, external crystal 25M, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_IR        | OV9286 2-lane 10-bit 720P 60fps linear output configuration for IR image, external crystal 25M, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_60FPS_10BIT_LINEAR_SPECKLE   | OV9286 2-lane 10-bit 720P 60fps linear output configuration for speckle image, external crystal 25M, connected to CSI1 |
| IMX335_MIPI_2LANE_RAW12_1920X1080_30FPS_LINEAR       | IMX335 12-bit 2-lane 1080P 30fps linear output, external crystal 24M, connected to CSI0 |
| IMX335_MIPI_2LANE_RAW12_2592X1944_30FPS_LINEAR       | IMX335 12-bit 2-lane full resolution 30fps linear output, external crystal 24M, connected to CSI0 |
| IMX335_MIPI_4LANE_RAW12_2592X1944_30FPS_LINEAR       | IMX335 12-bit 4-lane full resolution 30fps linear output, external crystal 24M, connected to CSI0 |
| IMX335_MIPI_2LANE_RAW12_1920X1080_30FPS_MCLK_7425_LINEAR | IMX335 12-bit 2-lane 1080P 30fps linear output, chip output 74.25M clock, connected to CSI0 |
| IMX335_MIPI_2LANE_RAW12_2592X1944_30FPS_MCLK_7425_LINEAR | IMX335 12-bit 2-lane full resolution 30fps linear output, chip output 74.25M clock, connected to CSI0 |
| IMX335_MIPI_4LANE_RAW12_2592X1944_30FPS_MCLK_7425_LINEAR | IMX335 12-bit 4-lane full resolution 30fps linear output, chip output 74.25M clock, connected to CSI0 |
| IMX335_MIPI_4LANE_RAW10_2XDOL                        | IMX335 10-bit 4-lane full resolution 15fps 2DOL output, external crystal 24M, connected to CSI0 |
| IMX335_MIPI_4LANE_RAW10_3XDOL                        | IMX335 10-bit 4-lane full resolution 15fps 3DOL output, external crystal 24M, connected to CSI0 |
| SC_SC035HGS_MIPI_1LANE_RAW10_640X480_120FPS_LINEAR   | SC035 10-bit 1-lane 640x480 120fps linear output, external crystal 24M, connected to CSI2 |
| SC_SC035HGS_MIPI_1LANE_RAW10_640X480_60FPS_LINEAR    | SC035 10-bit 1-lane 640x480 60fps linear output, external crystal 24M, connected to CSI2 |
| SC_SC035HGS_MIPI_1LANE_RAW10_640X480_30FPS_LINEAR    | SC035 10-bit 1-lane 640x480 30fps linear output, external crystal 24M, connected to CSI2 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_SPECKLE | OV9286 2-lane 10-bit 720P 30fps linear output configuration for speckle image, chip output 25M clock, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_IR | OV9286 2-lane 10-bit 720P 30fps linear output configuration for IR image, chip output 25M clock, connected to CSI1 |
| OV_OV9732_MIPI_1280X720_30FPS_10BIT_MCLK_16M_LINEAR  | OV9732 1-lane 10-bit 720P 30fps linear output configuration, chip output 16M clock, connected to CSI0 |
| OV_OV5647_MIPI_1920X1080_30FPS_10BIT_LINEAR          | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, external crystal 25M, connected to CSI2 |
| OV_OV5647_MIPI_2592x1944_10FPS_10BIT_LINEAR          | OV5647 2-lane 10-bit full resolution 10fps linear output configuration, external crystal 25M, connected to CSI2 |
| OV_OV5647_MIPI_640x480_60FPS_10BIT_LINEAR            | OV5647 2-lane 10-bit 640x480 60fps linear output configuration, external crystal 25M, connected to CSI2 |
| OV_OV5647_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR     | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, chip output 25M clock, connected to CSI0 |
| SC_SC201CS_MIPI_1LANE_RAW10_1600X1200_30FPS_LINEAR   | SC201 1-lane 10-bit 1600x1200 30fps linear output, crystal 27M, connected to CSI1 |
| SC_SC201CS_SLAVE_MODE_MIPI_1LANE_RAW10_1600X1200_30FPS_LINEAR | SC201 1-lane 10-bit slave mode 1600x1200 30fps linear output, crystal 27M, connected to CSI1 |
| OV_OV5647_MIPI_CSI1_1920X1080_30FPS_10BIT_LINEAR     | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, external crystal 25M, connected to CSI1 |
| OV_OV5647_MIPI_CSI2_1920X1080_30FPS_10BIT_LINEAR     | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, external crystal 25M, connected to CSI2 |
| XS9950_MIPI_CSI0_1280X720_30FPS_YUV422               | XS9950 2-lane YUV422 720P 25fps linear output, analog camera, connected to CSI0 |
| XS9950_MIPI_CSI1_1280X720_30FPS_YUV422               | XS9950 2-lane YUV422 720P 25fps linear output, analog camera, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_SPECKLE_V2 | OV9286 2-lane 10-bit 720P 30fps linear output configuration for speckle image, chip output 25M clock, connected to CSI1 |
| OV_OV9286_MIPI_1280X720_30FPS_10BIT_MCLK_25M_LINEAR_IR_V2 | OV9286 2-lane 10-bit 720P 30fps linear output configuration for IR image, chip output 25M clock, connected to CSI1 |
| OV_OV9732_MIPI_1280X720_30FPS_10BIT_MCLK_16M_LINEAR_V2 | OV9732 1-lane 10-bit 720P 30fps linear output configuration, chip output 16M clock, connected to CSI2 |
| OV_OV5647_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR_V2  | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, external crystal 25M, connected to CSI0 |
| OV_OV5647_MIPI_CSI1_1920X1080_30FPS_10BIT_LINEAR_V2  | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, external crystal 25M, connected to CSI1 |
| OV_OV5647_MIPI_CSI2_1920X1080_30FPS_10BIT_LINEAR_V2  | OV5647 2-lane 10-bit 1080P 30fps linear output configuration, chip output 25M clock, connected to CSI2 |
| GC2053_MIPI_CSI0_1920X1080_30FPS_10BIT_LINEAR        | GC2053 2-lane 10-bit 1080P 30fps linear output configuration, chip output 16M clock, connected to CSI0 |

**Notes**:

1. This list needs to be maintained by sensor driver developers. Application developers use the sensor types defined here to open specific types of sensor devices.

### 3.1.2 k_vicap_dev

**Description**: Definition of VICAP device IDs.

**Definition**:

```c
typedef enum {
    VICAP_DEV_ID_0 = 0,
    VICAP_DEV_ID_1 = 1,
    VICAP_DEV_ID_2 = 2,
    VICAP_DEV_ID_MAX,
} k_vicap_dev;
```

**Members**:

| **Member Name**   | **Description**   |
|-------------------|-------------------|
| VICAP_DEV_ID_0    | VICAP Device 0    |
| VICAP_DEV_ID_1    | VICAP Device 1    |
| VICAP_DEV_ID_2    | VICAP Device 2    |

### 3.1.3 k_vicap_chn

**Description**: Definition of VICAP output channel numbers.

**Definition**:

```c
typedef enum {
    VICAP_CHN_ID_0 = 0,
    VICAP_CHN_ID_1 = 1,
    VICAP_CHN_ID_2 = 2,
    VICAP_CHN_ID_MAX,
} k_vicap_chn;
```

**Members**:

| **Member Name**   | **Description**       |
|-------------------|-----------------------|
| VICAP_CHN_ID_0    | VICAP output channel 0 |
| VICAP_CHN_ID_1    | VICAP output channel 1 |
| VICAP_CHN_ID_2    | VICAP output channel 2 |

### 3.1.4 k_vicap_csi_num

**Description**: Definition of VICAP CSI numbers.

**Definition**:

```c
typedef enum {
    VICAP_CSI0 = 1,
    VICAP_CSI1 = 2,
    VICAP_CSI2 = 3,
} k_vicap_csi_num;
```

**Members**:

| **Member Name** | **Description** |
|-----------------|-----------------|
| VICAP_CSI0      | CSI0            |
| VICAP_CSI1      | CSI1            |
| VICAP_CSI2      | CSI2            |

**Notes**:

The CSI number to which the sensor is connected is determined by the hardware physical connection.

### 3.1.5 k_vicap_mipi_lanes

**Description**: Definition of VICAP MIPI lane numbers.

**Definition**:

```c
typedef enum {
    VICAP_MIPI_1LANE = 0,
    VICAP_MIPI_2LANE = 1,
    VICAP_MIPI_4LANE = 3,
} k_vicap_mipi_lanes;
```

**Members**:

| **Member Name**     | **Description** |
|---------------------|-----------------|
| VICAP_MIPI_1LANE    | 1 lane          |
| VICAP_MIPI_2LANE    | 2 lanes         |
| VICAP_MIPI_4LANE    | 4 lanes         |

**Notes**:

The number of MIPI lanes used by the sensor is determined by the hardware physical connection. When using 4 lanes, a maximum of two sensors can be connected.

### 3.1.6 k_vicap_csi_data_type

**Description**: Definition of VICAP MIPI data types.

**Definition**:

```c
typedef enum {
    VICAP_CSI_DATA_TYPE_RAW8 = 0x2A,
    VICAP_CSI_DATA_TYPE_RAW10 = 0x2B,
    VICAP_CSI_DATA_TYPE_RAW12 = 0x2C,
    VICAP_CSI_DATA_TYPE_RAW14 = 0x2D,
} k_vicap_csi_data_type;
```

**Members**:

| **Member Name**              | **Description** |
|------------------------------|-----------------|
| VICAP_CSI_DATA_TYPE_RAW8     | RAW8            |
| VICAP_CSI_DATA_TYPE_RAW10    | RAW10           |
| VICAP_CSI_DATA_TYPE_RAW12    | RAW12           |
| VICAP_CSI_DATA_TYPE_RAW14    | RAW14           |

**Notes**:

None

### 3.1.7 k_vicap_data_source

**Description**: Definition of VICAP data sources.

**Definition**:

```c
typedef enum {
    VICAP_SOURCE_CSI0 = 0, /**< VICAP acquire data from the CSI0 */
    VICAP_SOURCE_CSI1 = 1, /**< VICAP acquire data from the CSI1 */
    VICAP_SOURCE_CSI1_FS_TR0 = 2, /**< VICAP acquire data from the CSI1 for flash trigger 0 */
    VICAP_SOURCE_CSI1_FS_TR1 = 3, /**< VICAP acquire data from the CSI1 for flash trigger 1 */
    VICAP_SOURCE_CSI2 = 4, /**< VICAP acquire data from the CSI2 */
} k_vicap_data_source;
```

**Members**:

| **Member Name**             | **Description**                            |
|-----------------------------|--------------------------------------------|
| VICAP_SOURCE_CSI0           | VICAP data source is CSI0                  |
| VICAP_SOURCE_CSI1           | VICAP data source is CSI1                  |
| VICAP_SOURCE_CSI1_FS_TR0    | VICAP data source is CSI1 Flash trigger 0  |
| VICAP_SOURCE_CSI1_FS_TR1    | VICAP data source is CSI1 Flash trigger 1  |
| VICAP_SOURCE_CSI2           | VICAP data source is CSI2                  |

**Notes**:

None

### 3.1.8 k_vicap_vi_dvp_port

**Description**: Definition of VICAP VI DVP port numbers.

**Definition**:

```c
typedef enum {
    VICAP_VI_DVP_PORT0 = 0,
    VICAP_VI_DVP_PORT1 = 1,
    VICAP_VI_DVP_PORT2 = 2,
    VICAP_VI_DVP_PORT_MAX,
} k_vicap_vi_dvp_port;
```

**Members**:

| **Member Name**       | **Description** |
|-----------------------|-----------------|
| VICAP_VI_DVP_PORT0    | DVP port 0      |
| VICAP_VI_DVP_PORT1    | DVP port 1      |
| VICAP_VI_DVP_PORT2    | DVP port 2      |

**Notes**:

1. By default, port 0 corresponds to CSI0, port 1 corresponds to CSI1, and port 2 corresponds to CSI2.
1. Only port 0 supports HDR sensors. When using HDR mode, it must be bound to DVP port 0.
1. To change the port mapping relationship, binding operations are required.

### 3.1.9 k_vicap_vi_flash_mode

**Description**: Definition of VICAP flash light control modes.

**Definition**:

```c
typedef enum {
    VICAP_FLASH_FOLLOW_STROBE = 0,
    VICAP_FLASH_FOLLOW_STROBE_BASE_PWM = 1,
    VICAP_FLASH_NORMAL_PWM = 2,
    VICAP_FLASH_DISABLE = 3, /**< disable flash light */
} k_vicap_vi_flash_mode;
```

**Members**:

| **Member Name**                       | **Description**                    |
|---------------------------------------|------------------------------------|
| VICAP_FLASH_FOLLOW_STROBE             | Controlled by strobe signal        |
| VICAP_FLASH_FOLLOW_STROBE_BASE_PWM    | Controlled by strobe signal based on PWM mode |
| VICAP_FLASH_NORMAL_PWM                | Controlled by PWM signal           |
| VICAP_FLASH_DISABLE                   | Disabled                           |

**Notes**:

None

### 3.1.10 k_vicap_img_window

**Description**: Definition of VICAP image window.

**Definition**:

```c
typedef struct {
    k_u16 h_start;
    k_u16 v_start;
    k_u16 width;
    k_u16 height;
} k_vicap_img_window;
```

**Members**:

| **Member Name** | **Description**     |
|-----------------|---------------------|
| h_start         | Horizontal start position |
| v_start         | Vertical start position   |
| width           | Image width         |
| height          | Image height        |

### 3.1.11 k_vicap_work_mode

**Description**: Definition of VICAP work modes.

**Definition**:

```c
typedef enum {
    VICAP_WORK_ONLINE_MODE,
    VICAP_WORK_OFFLINE_MODE,
    VICAP_WORK_ONLY_MCM_MODE,
} k_vicap_work_mode;
```

**Members**:

| **Member Name**            | **Description** |
|----------------------------|-----------------|
| VICAP_WORK_ONLINE_MODE     | Online mode     |
| VICAP_WORK_OFFLINE_MODE    | Offline mode    |
| VICAP_WORK_ONLY_MCM_MODE   | Only work in MCM mode |

**Notes**:

When supporting multiple camera inputs, it must be specified as offline mode. When configuring VICAP_WORK_ONLY_MCM_MODE, the dumped image can only use the YUV444 format.

### 3.1.12 k_vicap_sensor_info

**Description**: VICAP sensor configuration information.

**Definition**:

```c
typedef struct {
    const char *sensor_name;
    k_vicap_csi_num csi_num; /**< CSI number that the sensor connects to */
    k_vicap_mipi_lanes mipi_lanes; /**< MIPI lanes that the sensor connects to */
    k_vicap_data_source source_id; /**< Source ID that the sensor uses */
    k_bool is_3d_sensor;
    k_vicap_mipi_phy_freq phy_freq;
    k_vicap_csi_data_type data_type;
    k_vicap_hdr_mode hdr_mode;
    k_vicap_vi_flash_mode flash_mode;
    k_vicap_sensor_type sensor_type;
} k_vicap_sensor_info;
```

**Members**:

| **Member Name** | **Description**                             |
|-----------------|---------------------------------------------|
| sensor_name     | Sensor name                                 |
| csi_num         | CSI number to which the sensor is connected |
| mipi_lanes      | Number of MIPI lanes used by the sensor     |
| source_id       | VICAP data source ID used by the sensor     |
| is_3d_sensor    | Whether it is a 3D sensor                   |
| phy_freq        | PHY frequency                               |
| data_type       | MIPI CSI data type                          |
| hdr_mode        | HDR mode                                    |
| flash_mode      | Flash light configuration mode              |
| sensor_type     | Sensor configuration type                   |

### 3.1.13 k_vicap_dump_format

**Description**: VICAP dump data frame format.

**Definition**:

```c
typedef enum {
    VICAP_DUMP_YUV = 0,
    VICAP_DUMP_RGB = 1,
    VICAP_DUMP_RAW = 2,
    VICAP_DUMP_YUV444 = 3,
} k_vicap_dump_format;
```

**Members**:

| **Member Name**   | **Description**    |
|-------------------|--------------------|
| VICAP_DUMP_YUV    | Dump YUV data      |
| VICAP_DUMP_RGB    | Dump RGB data      |
| VICAP_DUMP_RAW    | Dump RAW data      |
| VICAP_DUMP_YUV444 | Dump YUV444 data   |

### 3.1.14 k_vicap_dev_attr

**Description**: VICAP device attributes.

**Definition**:

```c
typedef struct {
    k_vicap_window acq_win;
    k_vicap_work_mode mode;
    k_vicap_isp_pipe_ctrl pipe_ctrl;
    k_u32 capture_frame;
    k_vicap_sensor_info sensor_info;
    k_bool dw_enable;
    k_u32 buffer_num;
    k_u32 buffer_size;
    k_vicap_mirror mirror;
} k_vicap_dev_attr;
```

**Members**:

| **Member Name**  | **Description**                                                                 |
|------------------|---------------------------------------------------------------------------------|
| acq_win          | Image capture window                                                            |
| mode             | VICAP work mode. When supporting multiple camera inputs, it must be specified as offline mode. |
| pipe_ctrl        | ISP pipeline control switch                                                     |
| capture_frame    | Number of frames to capture, range \[0,1023\], 0: continuous capture             |
| sensor_info      | Sensor configuration information                                                |
| dw_enable        | Dewarp enable (refer to [K230_SDK_Dewarp Usage Guide.md](../../pc/dewarp/K230_SDK_Dewarp_Guide.md)) |
| buffer_num       | Number of buffers for receiving sensor data in offline mode                     |
| buffer_size      | Buffer size for receiving sensor data in offline mode                           |
| mirror           | Sensor mirror function                                                          |

**Notes**:

For low-memory application scenarios, it is recommended to disable the 3DNR module to reduce memory usage. To disable, set `pipe_ctrl.bits.dnr3_enable` to 0 when setting device attributes.

### 3.1.15 k_vicap_chn_attr

**Description**: VICAP channel attributes.

**Definition**:

```c
typedef struct {
    k_vicap_window out_win;
    k_vicap_window crop_win;
    k_vicap_window scale_win;
    k_bool crop_enable;
    k_bool scale_enable;
    k_bool chn_enable;
    k_pixel_format pix_format;
    k_u32 buffer_num;
    k_u32 buffer_size;
    k_u8 alignment;
} k_vicap_chn_attr;
```

**Members**:

| **Member Name** | **Description**                 |
|-----------------|---------------------------------|
| out_win         | Output window size              |
| crop_win        | Crop window size                |
| scale_win       | Scale window size               |
| crop_enable     | Crop enable                     |
| scale_enable    | Scale enable                    |
| chn_enable      | Channel enable                  |
| pix_format      | Output pixel format             |
| buffer_num      | Number of buffers used by the channel |
| buffer_size     | Buffer size                     |
| alignment       | Buffer alignment method         |

### 3.1.16 k_vicap_mirror

**Description**: VICAP sensor mirror function.

**Definition**:

```c
typedef enum {
    VICAP_MIRROR_NONE = 0,
    VICAP_MIRROR_HOR = 1,
    VICAP_MIRROR_VER = 2,
    VICAP_MIRROR_BOTH = 3,
} k_vicap_mirror;
```

**Members**:

| **Member Name**   | **Description**           |
|-------------------|---------------------------|
| VICAP_MIRROR_NONE | No mirror for the sensor  |
| VICAP_MIRROR_HOR  | Horizontal mirror for the sensor |
| VICAP_MIRROR_VER  | Vertical mirror for the sensor   |
| VICAP_MIRROR_BOTH | Horizontal and vertical mirror for the sensor |

**Notes**:

None

### 3.2 Sensor

The related data type definitions of this functional module are as follows:

- [k_sensor_bayer_pattern](#321-k_sensor_bayer_pattern)
- [k_sensor_exp_frame_type](#322-k_sensor_exp_frame_type)
- [k_sensor_exposure_param](#323-k_sensor_exposure_param)
- [k_sensor_intg_time](#324-k_sensor_intg_time)
- [k_sensor_gain](#325-k_sensor_gain)
- [k_sensor_size](#326-k_sensor_size)
- [k_sensor_ae_info](#327-k_sensor_ae_info)
- [k_sensor_mode](#328-k_sensor_mode)
- [k_sensor_otp_date](#329-k_sensor_otp_date)

### 3.2.1 k_sensor_bayer_pattern

**Definition**: Definition of Bayer pattern output by the sensor.

```c
typedef enum {
    BAYER_RGGB = 0,
    BAYER_GRBG = 1,
    BAYER_GBRG = 2,
    BAYER_BGGR = 3,
    BAYER_BUTT
} k_sensor_bayer_pattern;
```

**Members**:

| **Member Name** | **Description** |
|-----------------|-----------------|
| BAYER_RGGB      | RGGB pattern    |
| BAYER_GRBG      | GRBG pattern    |
| BAYER_GBRG      | GBRG pattern    |
| BAYER_BGGR      | BGGR pattern    |

### 3.2.2 k_sensor_exp_frame_type

**Description**:

**Definition**:

```c
typedef enum {
    SENSOR_EXPO_FRAME_TYPE_1FRAME = 0,
    SENSOR_EXPO_FRAME_TYPE_2FRAMES = 1,
    SENSOR_EXPO_FRAME_TYPE_3FRAMES = 2,
    SENSOR_EXPO_FRAME_TYPE_4FRAMES = 3,
    SENSOR_EXPO_FRAME_TYPE_MAX
} k_sensor_exp_frame_type;
```

**Members**:

| **Member Name**                | **Description**            |
|--------------------------------|----------------------------|
| SENSOR_EXPO_FRAME_TYPE_1FRAME  | Linear mode, single-frame exposure |
| SENSOR_EXPO_FRAME_TYPE_2FRAMES | 2-frame HDR exposure mode  |
| SENSOR_EXPO_FRAME_TYPE_3FRAMES | 3-frame HDR exposure mode  |
| SENSOR_EXPO_FRAME_TYPE_4FRAMES | 4-frame HDR exposure mode  |

### 3.2.3 k_sensor_exposure_param

**Description**: Definition of sensor exposure parameters.

**Definition**:

```c
typedef struct {
    k_u8 exp_frame_type;
    float gain[SENSOR_EXPO_FRAME_TYPE_MAX];
    float exp_time[SENSOR_EXPO_FRAME_TYPE_MAX];
} k_sensor_exposure_param;
```

**Members**:

| **Member Name** | **Description** |
|-----------------|-----------------|
| exp_frame_type  | Exposure type   |
| gain            | Exposure gain   |
| exp_time        | Exposure time   |

### 3.2.4 k_sensor_intg_time

**Description**: Definition of sensor exposure time.

**Definition**:

```c
typedef struct {
    k_u8 exp_frame_type;
    float intg_time[SENSOR_EXPO_FRAME_TYPE_MAX];
} k_sensor_intg_time;
```

**Members**:

| **Member Name** | **Description**       |
|-----------------|-----------------------|
| exp_frame_type  | Exposure type         |
| intg_time       | Integration time      |

### 3.2.5 k_sensor_gain

**Description**: Definition of exposure gain.

**Definition**:

```c
typedef struct {
    k_u8 exp_frame_type;
    float gain[SENSOR_EXPO_FRAME_TYPE_MAX];
} k_sensor_gain;
```

**Members**:

| **Member Name** | **Description** |
|-----------------|-----------------|
| exp_frame_type  | Exposure type   |
| gain            | Exposure gain   |

### 3.2.6 k_sensor_size

**Description**: Definition of sensor-supported image sizes.

**Definition**:

```c
typedef struct {
    k_u32 bounds_width;
    k_u32 bounds_height;
    k_u32 top;
    k_u32 left;
    k_u32 width;
    k_u32 height;
} k_sensor_size;
```

**Members**:

| **Member Name** | **Description** |
|-----------------|-----------------|
| bounds_width    | Boundary width  |
| bounds_height   | Boundary height |
| top             | Top boundary    |
| left            | Left boundary   |
| width           | Width           |
| height          | Height          |

### 3.2.7 k_sensor_ae_info

**Description**: AE parameter configuration.

**Definition**:

```c
typedef struct {
    k_u16 frame_length;
    k_u16 cur_frame_length;
    float one_line_exp_time;
    k_u32 gain_accuracy;
    float min_gain;
    float max_gain;
    float integration_time_increment;
    float gain_increment;
    k_u16 max_long_integration_line;
    k_u16 min_long_integration_line;
    k_u16 max_integration_line;
    k_u16 min_integration_line;
    k_u16 max_vs_integration_line;
    k_u16 min_vs_integration_line;
    float max_long_integration_time;
    float min_long_integration_time;
    float max_integration_time;
    float min_integration_time;
    float max_vs_integration_time;
    float min_vs_integration_time;
    float cur_long_integration_time;
    float cur_integration_time;
    float cur_vs_integration_time;
    float cur_long_gain;
    float cur_long_again;
    float cur_long_dgain;
    float cur_gain;
    float cur_again;
    float cur_dgain;
    float cur_vs_gain;
    float cur_vs_again;
    float cur_vs_dgain;
    k_sensor_gain_info long_gain;
    k_sensor_gain_info gain;
    k_sensor_gain_info vs_gain;
    k_sensor_gain_info a_long_gain;
    k_sensor_gain_info a_gain;
    k_sensor_gain_info a_vs_gain;
    k_sensor_gain_info d_long_gain;
    k_sensor_gain_info d_gain;
    k_sensor_gain_info d_vs_gain;
    k_u32 max_fps;
    k_u32 min_fps;
    k_u32 cur_fps;
    k_sensor_auto_fps afps_info;
    k_u32 hdr_ratio;
} k_sensor_ae_info;
```

**Members**:

| **Member Name**               | **Description**                     |
|-------------------------------|-------------------------------------|
| frame_length                  | Frame length                        |
| cur_frame_length              | Current frame length                |
| one_line_exp_time             | Line exposure time (unit: s)        |
| gain_accuracy                 | Gain accuracy                       |
| min_gain                      | Minimum gain                        |
| max_gain                      | Maximum gain                        |
| integration_time_increment    | Integration time increment          |
| gain_increment                | Gain increment                      |
| max_long_integration_line     | Maximum long frame integration line |
| min_long_integration_line     | Minimum long frame integration line |
| max_integration_line          | Maximum mid frame integration line  |
| min_integration_line          | Minimum mid frame integration line  |
| max_vs_integration_line       | Maximum short frame integration line|
| min_vs_integration_line       | Minimum short frame integration line|
| max_long_integration_time     | Maximum long frame integration time |
| min_long_integration_time     | Minimum long frame integration time |
| max_integration_time          | Maximum mid frame integration time  |
| min_integration_time          | Minimum mid frame integration time  |
| max_vs_integration_time       | Maximum short frame integration time|
| min_vs_integration_time       | Minimum short frame integration time|
| cur_long_integration_time     | Current long frame integration time |
| cur_integration_time          | Current frame integration time      |
| cur_vs_integration_time       | Current short frame integration time|
| cur_long_gain                 | Current long frame gain             |
| cur_long_again                | Current long frame analog gain      |
| cur_long_dgain                | Current long frame digital gain     |
| cur_gain                      | Current frame gain                  |
| cur_again                     | Current frame analog gain           |
| cur_dgain                     | Current frame digital gain          |
| cur_vs_gain                   | Current short frame gain            |
| cur_vs_again                  | Current short frame analog gain     |
| cur_vs_dgain                  | Current short frame digital gain    |
| long_gain                     | Long frame gain                     |
| gain                          | Mid frame gain                      |
| vs_gain                       | Short frame gain                    |
| a_long_gain                   | Long frame analog gain              |
| a_gain                        | Mid frame analog gain               |
| a_vs_gain                     | Short frame analog gain             |
| d_long_gain                   | Long frame digital gain             |
| d_gain                        | Mid frame digital gain              |
| d_vs_gain                     | Short frame digital gain            |
| max_fps                       | Maximum frame rate                  |
| min_fps                       | Minimum frame rate                  |
| cur_fps                       | Current frame rate                  |
| hdr_ratio                     | HDR ratio                           |

### 3.2.8 k_sensor_mode

**Description**: Sensor mode parameters.

**Definition**:

```c
typedef struct {
    k_u32 index;
    k_vicap_sensor_type sensor_type;
    k_sensor_size size;
    k_u32 fps;
    k_u32 hdr_mode;
    k_u32 stitching_mode;
    k_u32 bit_width;
    k_u32 bayer_pattern;
    k_sensor_mipi_info mipi_info;
    k_sensor_ae_info ae_info;
    k_sensor_reg_list *reg_list;
} k_sensor_mode;
```

**Members**:

| **Member Name** | **Description**                 |
|-----------------|----------------------------------|
| index           | Current mode index              |
| sensor_type     | Sensor configuration type       |
| size            | Sensor size for the current mode|
| fps             | Frame rate                      |
| hdr_mode        | HDR mode                        |
| stitching_mode  | HDR stitching mode              |
| bit_width       | Output data width               |
| bayer_pattern   | Bayer pattern                   |
| mipi_info       | MIPI parameter information      |
| ae_info         | AE parameter information        |
| reg_list        | Register configuration list for the current mode |
| otp_type        | OTP type: sensor-specific and user-specific |
| otp_date        | OTP data                        |

### 3.2.9 k_sensor_otp_date

**Description**: Sensor OTP parameters.

**Definition**:

```c
typedef struct {
    k_u8 otp_type;
    k_u8 otp_date[20];
} k_sensor_otp_date;
```

**Members**:

| **Member Name** | **Description**                 |
|-----------------|----------------------------------|
| otp_type        | OTP type: sensor-specific and user-specific |
| otp_date        | OTP data                        |

## 4. MAPI

This functional module provides the following APIs:

- [kd_mapi_vicap_get_sensor_fd]
- [kd_mapi_vicap_get_sensor_info]
- [kd_mapi_vicap_set_dev_attr]
- [kd_mapi_vicap_set_chn_attr]
- [kd_mapi_vicap_start]
- [kd_mapi_vicap_stop]
- [kd_mapi_vicap_dump_frame]
- [kd_mapi_vicap_release_frame]
- [kd_mapi_vicap_set_vi_drop_frame]
- [kd_mapi_vicap_set_mclk]
- [kd_mapi_vicap_tuning]
- [kd_mapi_isp_ae_get_roi]
- [kd_mapi_isp_ae_set_roi]
- [kd_mapi_sensor_otpdata_get]

### 4.1 API

#### 4.1.1 kd_mapi_vicap_get_sensor_fd

**Description**:

Get the file descriptor for the specified sensor.

**Syntax**:

```c
k_s32 kd_mapi_vicap_get_sensor_fd(k_vicap_sensor_attr *sensor_attr)
```

**Parameters**:

| **Parameter Name** | **Description** | **Input/Output** |
|--------------------|-----------------|------------------|
| sensor_attr        | Sensor attributes | Input & Output  |

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.2 kd_mapi_vicap_get_sensor_info

**Description**:

Get sensor configuration information based on the specified sensor configuration type. Refer to [kd_mpi_vicap_get_sensor_info](#211-kd_mpi_vicap_get_sensor_info). Put `sensor_type` into `sensor_info.sensor_type`, usage is the same.

**Syntax**:

```c
k_s32 kd_mapi_vicap_get_sensor_info(k_vicap_sensor_info *sensor_info)
```

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.3 kd_mapi_vicap_set_dev_attr

**Description**:

Set VICAP device attributes. Refer to [kd_mpi_vicap_set_dev_attr](#212-kd_mpi_vicap_set_dev_attr). Put `dev_num` into `dev_info.vicap_dev`, usage is the same.

**Syntax**:

```c
k_s32 kd_mapi_vicap_set_dev_attr(k_vicap_dev_set_info dev_info)
```

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.4 kd_mapi_vicap_set_chn_attr

**Description**:

Set VICAP channel attributes. Refer to [kd_mpi_vicap_set_chn_attr](#214-kd_mpi_vicap_set_chn_attr). Put `dev_num` into `chn_info.vicap_dev`, and `chn_num` into `chn_info.vicap_chn`, usage is the same.

**Syntax**:

```c
k_s32 kd_mapi_vicap_set_chn_attr(k_vicap_chn_set_info chn_info)
```

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.5 kd_mapi_vicap_start

**Description**:

[kd_mpi_vicap_init](#216-kd_mpi_vicap_init) + [kd_mpi_vicap_start_stream](#218-kd_mpi_vicap_start_stream)

**Syntax**:

```c
k_s32 kd_mapi_vicap_start(k_vicap_dev vicap_dev)
```

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.6 kd_mapi_vicap_stop

**Description**:

[kd_mpi_vicap_stop_stream](#219-kd_mpi_vicap_stop_stream) + [kd_mpi_vicap_deinit](#217-kd_mpi_vicap_deinit)

**Syntax**:

```c
k_s32 kd_mapi_vicap_stop(k_vicap_dev vicap_dev)
```

**Return Value**:

| **Return Value** | **Description**       |
|------------------|-----------------------|
| 0                | Success               |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.7 kd_mapi_vicap_dump_frame

**Description**:

Dump VICAP data based on the specified device and output channel. Refer to [kd_mpi_vicap_dump_frame](#2110-kd_mpi_vicap_dump_frame).

**Syntax**:

```c
k_s32 kd_mapi_vicap_dump_frame(k_vicap_dev dev_num, k_vicap_chn chn_num, k_vicap_dump_format format, k_video_frame_info *vf_info, k_u32 milli_sec)
```

**Parameters**:

| **Parameter Name** | **Description**     | **Input/Output** |
|--------------------|---------------------|------------------|
| dev_num            | VICAP device number | Input            |
| chn_num            | VICAP output channel number | Input      |
| format             | Dump data type      | Input            |
| vf_info            | Dump frame information | Output       |
| milli_sec          | Timeout duration    | Input            |

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.8 kd_mapi_vicap_release_frame

**Description**:

Release the dumped data frame. Refer to [kd_mpi_vicap_dump_release](#2111-kd_mpi_vicap_dump_release).

**Syntax**:

```c
k_s32 kd_mapi_vicap_release_frame(k_vicap_dev dev_num, k_vicap_chn chn_num, const k_video_frame_info *vf_info)
```

**Parameters**:

| **Parameter Name** | **Description**     | **Input/Output** |
|--------------------|---------------------|------------------|
| dev_num            | VICAP device number | Input            |
| chn_num            | VICAP output channel number | Input      |
| vf_info            | Dump frame information | Input         |

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.9 kd_mapi_vicap_set_vi_drop_frame

**Description**:

Set hardware frame dropping. Refer to [kd_mpi_vicap_set_vi_drop_frame](#419-kd_mapi_vicap_set_vi_drop_frame).

**Syntax**:

```c
k_s32 kd_mapi_vicap_set_vi_drop_frame(k_vicap_csi_num csi, k_vicap_drop_frame *frame, k_bool enable)
```

**Parameters**:

| **Parameter Name** | **Description**     | **Input/Output** |
|--------------------|---------------------|------------------|
| csi                | VICAP device number | Input            |
| frame              | Structure, see below|                  |
| m                  | Drop n frames every m frames | Input |
| n                  | Drop n frames every m frames | Input |
| mode               | HDR mode            | Input            |
| enable             | Enable or disable   | Input            |

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.10 kd_mapi_vicap_set_mclk

**Description**:

Set the MCLK frequency. Refer to [kd_mpi_vicap_set_mclk](#2113-kd_mpi_vicap_set_mclk).

**Syntax**:

```c
k_s32 kd_mapi_vicap_set_mclk(k_vicap_mclk_id id, k_vicap_mclk_sel sel, k_u8 mclk_div, k_u8 mclk_en)
```

**Parameters**:

| **Parameter Name** | **Description**     | **Input/Output** |
|--------------------|---------------------|------------------|
| id                 | MCLK ID             | Input            |
| sel                | Clock source        | Input            |
| mclk_div           | Division factor     | Input            |
| mclk_en            | Enable or disable   | Input            |

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.11 kd_mapi_vicap_tuning

**Description**:

Handle commands sent by the tuning client.

**Syntax**:

```c
k_s32 kd_mapi_vicap_tuning(char* string, k_u32 size, char** response, k_u32* response_len)
```

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_vicap_api.h
- Library file: libmapi.a

#### 4.1.12 kd_mapi_isp_ae_get_roi

**Description**:

Get AE ROI configuration.

**Syntax**:

```c
k_s32 kd_mapi_isp_ae_get_roi(k_vicap_dev dev_num, k_isp_ae_roi *ae_roi)
```

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_isp_api.h
- Library file: libmapi.a

#### 4.1.13 kd_mapi_isp_ae_set_roi

**Description**:

Set AE ROI.

**Syntax**:

```c
k_s32 kd_mapi_isp_ae_set_roi(k_vicap_dev dev_num, k_isp_ae_roi ae_roi)
```

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_isp_api.h
- Library file: libmapi.a

#### 4.1.14 kd_mapi_sensor_otpdata_get

**Description**:

Get sensor OTP data.

**Syntax**:

```c
k_s32 kd_mapi_sensor_otpdata_get(k_s32 sensor_type, k_sensor_otp_date *otp_data)
```

**Return Value**:

| **Return Value** | **Description**            |
|------------------|-----------------------------|
| 0                | Success                     |
| Non-zero         | Failure, refer to error code definitions |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_isp_api.h
- Library file: libmapi.a

## 5. Error Codes

Table 41 VICAP API Error Codes

| Error Code  | Macro Definition            | Description                                 |
|-------------|------------------------------|---------------------------------------------|
| 0xA0158001  | K_ERR_VICAP_INVALID_DEVID    | Device ID out of valid range                |
| 0xA0158002  | K_ERR_VICAP_INVALID_CHNID    | Channel ID out of valid range               |
| 0xA0158003  | K_ERR_VICAP_ILLEGAL_PARAM    | Parameter out of valid range                |
| 0xA0158004  | K_ERR_VICAP_EXIST            | Attempt to create an already existing device, channel, or resource |
| 0xA0158005  | K_ERR_VICAP_UNEXIST          | Attempt to use or destroy a non-existent device, channel, or resource |
| 0xA0158006  | K_ERR_VICAP_NULL_PTR         | Null pointer in function parameters         |
| 0xA0158007  | K_ERR_VICAP_NOT_CONFIG       | Not configured before use                   |
| 0xA0158008  | K_ERR_VICAP_NOT_SUPPORT      | Unsupported parameter or function           |
| 0xA0158009  | K_ERR_VICAP_NOT_PERM         | Operation not allowed, such as trying to modify static configuration parameters |
| 0xA015800C  | K_ERR_VICAP_NOMEM            | Memory allocation failure, such as insufficient system memory |
| 0xA015800D  | K_ERR_VICAP_NOBUF            | Buffer allocation failure, such as requesting a data buffer that is too large |
| 0xA015800E  | K_ERR_VICAP_BUF_EMPTY        | No data in the buffer                       |
| 0xA015800F  | K_ERR_VICAP_BUF_FULL         | Data buffer full                            |
| 0xA0158010  | K_ERR_VICAP_NOTREADY         | System not initialized or relevant module not loaded |
| 0xA0158011  | K_ERR_VICAP_BADADDR          | Address out of valid range                  |
| 0xA0158012  | K_ERR_VICAP_BUSY             | VICAP system busy                           |

## 6. Debug Information

For VICAP memory management and system binding debug information, refer to the "K230 System Control API Reference".
