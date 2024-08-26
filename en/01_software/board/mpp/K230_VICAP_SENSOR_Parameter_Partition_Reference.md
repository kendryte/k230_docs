# K230 VICAP SENSOR Parameter Partition Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for use as a reference guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified without notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy any part or all of the content of this document, nor may it be disseminated in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly guides image tuning and application developers on how to create VICAP debugging parameter files for use in SPI NOR FLASH mode.

### Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers
- Image Tuning Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
|              |             |

### Revision Record

| Document Version | Modification Description | Modifier | Date |
|------------------|--------------------------|----------|------|
| V1.0             | Initial version          | Shidong Guo | 2023/10/07 |

## 1. Overview

### 1.1 Overview

In the real-time processing of signals output by the sensor by the ISP, tuning parameters and calibration parameters play a key role in the ISP processing method and image restoration and enhancement. The SDK uses default calibration xml, auto json, and manual json files as tuning and calibration parameter configurations imported at runtime by VICAP. In the fast start mode, the default parameter import method is time-consuming, so a parameter partition import configuration scheme is provided.

This document mainly describes the method of creating parameter partitions and how VICAP uses these partitions.

## 2. Production Process Reference

### 2.1 Flowchart

The production flowchart is as follows:

![isp param](../../../../zh/01_software/board/mpp/images/ISP_param.png)

Figure 2-1 Parameter Partition Production Flowchart

The production steps are as follows:

- [Step 1, Convert Header File](#221-convert-header-file)
- [Step 2, Convert Binary File](#222-convert-binary-file)
- [Step 3, Usage Method](#223-usage-method)
- [Precautions](#224-precautions)

### 2.2 Production Steps

#### 2.2.1 Convert Header File

Take sensor: IMX335, resolution: 2592x1944 as an example

Copy the parameter file to the directory for converting header files

```shell
cp k230_sdk/src/big/mpp/userapps/src/sensor/config/imx335-2592x1944.xml k230_sdk/src/big/mpp/userapps/src/vicap/src/isp/sdk/t_frameworks/t_database_c/calibration_data/
cp k230_sdk/src/big/mpp/userapps/src/sensor/config/imx335-2592x1944_auto.json k230_sdk/src/big/mpp/userapps/src/vicap/src/isp/sdk/t_frameworks/t_database_c/calibration_data/
cp k230_sdk/src/big/mpp/userapps/src/sensor/config/imx335-2592x1944_manual.json k230_sdk/src/big/mpp/userapps/src/vicap/src/isp/sdk/t_frameworks/t_database_c/calibration_data/
```

Navigate to the conversion operation directory (tool source code and script storage directory)

```shell
cd k230_sdk/src/big/mpp/userapps/src/vicap/src/isp/sdk/t_frameworks/t_database_c/calibration_data/
```

Execute the conversion header file tool *parse_convert.py*, parse and convert the three copied configuration files into a parameter header file (it is recommended to use python3.x for the conversion tool)

![parse_convert](../../../../zh/01_software/board/mpp/images/parse_convert.png)

```shell
python parse_convert.py -s imx335 -x imx335-2592x1944.xml -a imx335-2592x1944_auto.json -m imx335-2592x1944_manual.json > imx335_2592x1944_param_data.h
```

```c
#ifndef __IMX335_CALIBRATION_H__
#define __IMX335_CALIBRATION_H__

#include "isp_database.h"
#include "k_autoconf_comm.h"
static const TUNING_PARAM_T database_tuning_param =
{
    /* calib data */
    ...
    /* auto data */
    ...
    /* manual data */
    ...
    /* dewarp data */
    ...
    /* version_info */
}
#endif
```

After conversion, a structure similar to the above will be obtained, consisting of five parts:

calib data, auto data, manual data are generated by parsing the specified external configuration files

dewarp data needs to be replaced in the structure according to actual configuration, refer to [dewarp parameter configuration](#2224-dewarp-parameter-configuration)

version info is automatically generated by the conversion tool, describing the sensor name and creation date

#### 2.2.2 Convert Binary File

The binary file is composed of four files: header, configuration parameters, padding, and dewarp parameters. Considering the actual allocation size of the parameter partition, it is recommended to add up to three sets of configuration files.

- [Step 1, Header Production](#2221-header-production)
- [Step 2, Configuration Parameter Binary File Production](#2222-configuration-parameter-binary-file-production)
- [Step 3, Padding File Production](#2223-padding-generation)
- [Step 4, Dewarp Parameter Configuration](#2224-dewarp-parameter-configuration)
- [Step 5, Merging Files](#2225-merging-files)
- [Others, Scripted Production Method (Recommended)](#2226-scripted-production-of-binary-files)

##### 2.2.2.1 Header Production

Modify the definitions of FILENAME_00, FILENAME_01, FILENAME_02 in *gen_database_param_bin_calib_header.c*, as shown below:

```c
#define FILENAME_00 "imx335-2592x1944"
#define FILENAME_01 "ov9732-1280x720"
#define FILENAME_02 "ov9286-1280x720"
```

The format requirement is the sensor name corresponding to the driver - width x height. For example, if the configuration of imx335-2592x1944 corresponds to the sensor name imx335 and the resolution is 2592x1944 in the driver, then modify FILENAME_0X to "imx335-2592x1944". This definition will serve as the verification header when using the parameter partition. If the verification header does not match, the default method of loading configuration files will be used, and corresponding warning messages will be printed in the log. The name defined by the verification header must be unique and cannot be duplicated.

Up to three verification headers can be added. Once the order is fixed, the order of the parameter partition must also be synchronized with the verification header. The synchronization method is referred to in the subsequent [Binary File Production](#2222-configuration-parameter-binary-file-production).

After modifying the definition, compile the source code into an executable program and execute it to obtain the header: sensor_cfg_calib_header.bin

```shell
gcc -o main_header gen_database_param_bin_calib_header.c
./main_header 
# Obtain sensor_cfg_calib_header.bin
```

##### 2.2.2.2 Configuration Parameter Binary File Production

Modify the DATABASE_SELECT definition in *gen_database_param_bin.c*, and create different configuration binary files by passing in different parameters during external compilation, as shown below:

```c
#if DATABASE_SELECT == 0
#include "imx335_2592x1944_param_data.h"
#elif DATABASE_SELECT == 1
#include "ov9732_param_data.h"
#elif DATABASE_SELECT == 2
#include "ov9286_param_data.h"
// will append new header file to convert bin, you can make DATABASE_SELECT++, build need add flag "-DDATABASE_SELECT=?, ?:0, 1, 2..."
#endif
```

The number of DATABASE_SELECT determines the order of different sensor configuration parameters. This order needs to be synchronized with the header. In the example, imx335_2592x1944_param_data.h, ov9732_param_data.h, and ov9286_param_data.h are generated by three sets of xml and json files.

Compile the source code and execute

```shell
DATABASE_CURRENT_DIR=$PWD
DATABASE_CFLAGS="-I$DATABASE_CURRENT_DIR/../include \
 -I$DATABASE_CURRENT_DIR/../../t_common_c/include/  \
 -I$DATABASE_CURRENT_DIR/../../t_json_c/include/    \
 -I$DATABASE_CURRENT_DIR/../../t_mxml_c/mxml-3.3.1/ \
 -I$DATABASE_CURRENT_DIR/../../../../../../../../../include/comm"
gcc -o main_01 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=0
gcc -o main_02 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=1
gcc -o main_03 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=2
$DATABASE_CURRENT_DIR/main_01 0
$DATABASE_CURRENT_DIR/main_02 1
$DATABASE_CURRENT_DIR/main_03 2 
# Obtain files sensor_cfg_00.bin (imx335), sensor_cfg_01.bin (ov9732), sensor_cfg_02.bin (ov9286)
```

Compile multiple executable programs and execute them. The 0, 1, 2 parameters passed in during execution are the sequence numbers in the generated binary file names.

##### 2.2.2.3 Padding Generation

The purpose of the padding file is to align the subsequent dewarp parameters for ease of use. The length of the padding will vary based on the total length of the header and parameter structure, and it is automatically generated by the script.

##### 2.2.2.4 Dewarp Parameter Configuration

The parameter partition defines the basic parameters of the dewarp LUT table. Based on this parameter, the correct dewarp corresponding LUT file can be found when using the partition.

```c
typedef struct {
    uint8_t has_lut;
    uint64_t lut_offset;
    uint8_t split_enable;
    uint16_t split_horizon_line;
    uint16_t split_vertical_line_up;
    uint16_t split_vertical_line_down;
} DEWARP_SPLIT_T;
```

has_lut: Indicates whether there is a dewarp LUT file. Setting this member to 0 means that dewarp parameters are not needed. Setting it to 1 means that dewarp parameters are needed.

lut_offset: When has_lut is set to 1, this member is effective. The value corresponds to the offset of the dewarp parameter in the parameter partition. The specific calculation method is parameter partition base address + header size + parameter structure size + padding size. The parameter partition base address is defined as *CONFIG_MEM_SENSOR_CFG_BASE* in k_autoconf_comm.h. This definition varies with different compiled hardware. It can be calculated by the *gen_database.sh* script provided by the SDK. The execution will print the result:

![calc_isp_param_data_size](../../../../zh/01_software/board/mpp/images/calc_isp_param_data_size.png)

Figure 2-2 Parameter Partition Automatically Calculates Dewarp Offset

split_enable: Default set to 0

split_horizon_line: Default 8191

split_vertical_line_up: Default 8191

split_vertical_line_down: Default 8191

The dewarp parameter file needs to specify the path in the production script, refer to the subsequent sections

The following examples show the configuration when using dewarp and not using dewarp

```c
// Configuration using dewarp
/* dewarp data */
{
    /* has_lut */
    1,
    /* lut_offset */
    CONFIG_MEM_SENSOR_CFG_BASE + 426528, // 426528 is calculated by the script
    /* split_enable */
    0,
    /* split_horizon_line */
    8191,
    /* split_vertical_line_up */
    8191,
    /* split_vertical_line_down */
    8191,
},

// Configuration not using dewarp
/* dewarp data */
{
    /* has_lut */
    0,
    /* lut_offset */
    0,
    /* split_enable */
    0,
    /* split_horizon_line */
    8191,
    /* split_vertical_line_up */
    8191,
    /* split_vertical_line_down */
    8191,
},

```

##### 2.2.2.5 Merging Files

The files produced by steps 2.2.2.1 - 2.2.2.4 are as follows:
| **Filename**                | **Description**          |
|-----------------------------|--------------------------|
| sensor_cfg_calib_header.bin | Header file              |
| sensor_cfg_0X.bin           | Configuration parameter files |
| padding.bin                 | File for alignment       |
| imx335-2592x1944.bin        | Dewarp parameter file, refer to the dewarp usage guide for generation method |

Merge the above files to get the final binary file *sensor_cfg.bin* for the parameter partition.

```shell
cat sensor_cfg_calib_header.bin \
    sensor_cfg_00.bin sensor_cfg_01.bin \
    sensor_cfg_02.bin \
    padding.bin \
    ../../../../../../../sensor/dewarp/imx335-2592x1944.bin > sensor_cfg.bin
```

In order, the last merged file is the dewarp parameter file generated in k230_sdk/src/big/mpp/userapps/src/sensor/dewarp. If new dewarp parameter files are added, they can be appended at the end in sequence.

##### 2.2.2.6 Scripted Production of Binary Files

The SDK provides a semi-automated script *gen_database.sh* that links processes 2.2.2.1 - 2.2.2.5. After completing the source code definitions for header, dewarp, and parameter parsing, users can execute this script to produce the binary file, or even compile the SDK directly without manually executing the script.

```shell
#!/bin/sh
DATABASE_CURRENT_DIR=$PWD
DATA_SAVE_PATH=../../../../../../../../../../../../tools/gen_image_cfg/data/
DATABASE_CFLAGS="-I$DATABASE_CURRENT_DIR/../include \
 -I$DATABASE_CURRENT_DIR/../../t_common_c/include/  \
 -I$DATABASE_CURRENT_DIR/../../t_json_c/include/    \
 -I$DATABASE_CURRENT_DIR/../../t_mxml_c/mxml-3.3.1/ \
 -I$DATABASE_CURRENT_DIR/../../../../../../../../../include/comm"

DATABASE_SELECT 0: imx335 2592x1944, 1: ov9732 1280x720, 2: ov9286 1280x720, ...
echo -n

gcc -o main_01 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=0
gcc -o main_02 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=1
gcc -o main_03 gen_database_param_bin.c $DATABASE_CFLAGS -DDATABASE_SELECT=2

gcc -o main_header gen_database_param_bin_calib_header.c

$DATABASE_CURRENT_DIR/main_header
$DATABASE_CURRENT_DIR/main_01 0
$DATABASE_CURRENT_DIR/main_02 1
$DATABASE_CURRENT_DIR/main_03 2

rm $DATABASE_CURRENT_DIR/main_header
rm $DATABASE_CURRENT_DIR/main_01
rm $DATABASE_CURRENT_DIR/main_02
rm $DATABASE_CURRENT_DIR/main_03

FILE_LENGTH=$(wc -c < sensor_cfg_calib_header.bin)
FILE_LENGTH=$(expr $FILE_LENGTH + $(wc -c < sensor_cfg_00.bin))
FILE_LENGTH=$(expr $FILE_LENGTH + $(wc -c < sensor_cfg_01.bin))
FILE_LENGTH=$(expr $FILE_LENGTH + $(wc -c < sensor_cfg_02.bin))
PADDING_LENGTH=$(expr 16 - $FILE_LENGTH % 16)
dd if=/dev/zero of=padding.bin bs=1 count=$PADDING_LENGTH
echo "The first LUT offset is "$(expr $PADDING_LENGTH + $FILE_LENGTH)

cat sensor_cfg_calib_header.bin\
    sensor_cfg_00.bin sensor_cfg_01.bin\
    sensor_cfg_02.bin\
    padding.bin\
    ../../../../../../../sensor/dewarp/imx335-2592x1944.bin > sensor_cfg.bin

```

##### 2.2.2.6 Applying Parameter Partition

After creating the binary file, it needs to be placed in the parameter partition storage location. This operation is completed by the SDK compilation script and does not require user intervention. You only need to create the file in k230_sdk/src/big/mpp/userapps/src/vicap/src/isp/sdk/t_frameworks/t_database_c/calibration_data/ for it to be automatically included during compilation.

#### 2.2.3 Usage Method

After completing the correct production process, use the API provided by VICAP.

**Note**: VICAP configuration parameter parsing modes

**Definition**:

```c
typedef enum {
    VICAP_DATABASE_PARSE_XML_JSON = 0,
    VICAP_DATABASE_PARSE_HEADER = 1,
} k_vicap_database_parse_mode;
```

**Members**:

| **Member Name**               | Value | **Description**                          |
|-------------------------------|-------|------------------------------------------|
| VICAP_DATABASE_PARSE_XML_JSON  | 0     | Use xml, auto json, manual json mode     |
| VICAP_DATABASE_PARSE_HEADER    | 1     | Use parameter partition loading mode     |

**Notes**:
Only 0 and 1 are validated internally, other values are invalid.

**Description**: VICAP sets parameter loading mode

**Description**:

Set different VICAP devices to load ISP parameters based on dev_num, default is 0.

**Syntax**:

k_s32 kd_mpi_vicap_set_database_parse_mode(k_vicap_dev dev_num, k_vicap_database_parse_mode parse_mode)

**Parameters**:

| **Parameter Name** | **Description** | **Input/Output** |
|--------------------|-----------------|------------------|
| dev_num            | VICAP device number | Input       |
| parse_mode         | Parameter loading mode | Input   |

**Return Value**:

| **Return Value** | **Description**            |
|------------------|----------------------------|
| Positive Value   | Success. Returns device descriptor |
| Negative Value   | Failure, refer to error codes.     |

**Chip Differences**:

None.

**Requirements**:

- Header file: mpi_vicap_api.h
- Library file: libvicap.a

**Note**:

Must be called before kd_mpi_vicap_init.

**Example**:

```c
typedef enum {
    VICAP_DEV_ID_0 = 0,
    VICAP_DEV_ID_1 = 1,
    VICAP_DEV_ID_2 = 2,
    VICAP_DEV_ID_MAX,
} k_vicap_dev;

int ret = 0;
k_vicap_dev vicap_dev = VICAP_DEV_ID_0;
ret = kd_mpi_vicap_set_database_parse_mode(vicap_dev, VICAP_DATABASE_PARSE_HEADER);
if (ret) {
    printf("kd_mpi_vicap_set_database_parse_mode failed, %d\n", ret);
    return ret;
}
```

#### 2.2.4 Precautions

1. When generating the parameter header file, the dewarp structure is default. Fill in based on actual conditions and calculate the offset. The offset can be automatically calculated by executing *gen_database.sh* and then filled into the corresponding position.
1. *gen_database_param_bin.c* uses the gcc -D compilation option to define the value of DATABASE_SELECT to determine which set of header files to include and convert into parameter files. The order must match the sequence number defined in the header.
1. The parameter partition function is currently only used in SPI NOR FLASH mode. Other modes do not have parameter partitions, and even if loaded, they cannot be used.
1. In the header production source code, the definition format for FILENAME_0X is: sensor_name-width x height. This header will be verified internally when used by VICAP. VICAP uses a concatenation method to generate the verification header for comparison. The verification header format is the sensor_name used in the driver configuration - input width x input height.
1. The conversion tool and calibration xml, auto json, manual json, and VICAP versions must match. Different versions are not compatible.
1. When using parameter partitions, VICAP will automatically verify the parameter partition based on the current sensor configuration and the set parsing mode. If the verification is successful, it will extract the parameters for loading without additional user settings. If the verification header comparison fails, it will automatically switch back to the default configuration parameter parsing mode.
