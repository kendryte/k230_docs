# K230 Fancy POC Introduction

![cover](../../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference as a usage guide only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy any part or all of the content of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## K230 Fancy POC

### Overview

The K230 Fancy POC collection includes projects such as multimodal_chat_robot, meta_human, meta_hand, and finger_reader. This project aims to provide customers with a POC (Proof of Concept) construction process.

### Hardware Environment

- `CanMV-K230-V1.x / CanMV-K230-V2.x / K230-UNSIP-LPx-EVB-V1.x`

### Source Code Location

The source code path is located at `k230_sdk/src/reference/fancy_poc`, with the directory structure as follows:

```shell
.
├── ai_scale
├── build_app.sh
├── cmake
├── CMakeLists.txt
├── face_recognition
├── finger_reader
├── housekeeper
├── meta_hand
├── meta_human
├── multimodal_chat_robot
└── version
```

### Compiling and Running the Program

#### a. Self-compiled Board Image

- Ensure that you have built the docker container and image according to the [K230 SDK official instructions](https://github.com/kendryte/k230_sdk).
- Navigate to k230_sdk/src/reference/fancy_poc.
- Execute build_app.sh, which will generate the corresponding large core and small core files in the k230_sdk/src/reference/fancy_poc/k230_bin directory.
- Select the POC executable file you want to reference from the k230_bin directory and copy it to the development board. (Refer to each POC's readme for the corresponding executable program).
- For the kmodel and other binary files required for each POC on the board, refer to the src/download.sh in the POC directory for download and use.

#### b. Direct Download of Official Board Image

1. Ensure that you have built the docker container according to the [K230 SDK official instructions](https://github.com/kendryte/k230_sdk).
1. Download the image from the [official resource library](https://developer.canaan-creative.com/resource).
1. Prepare the environment:

```bash
cd k230_sdk
make prepare_sourcecode # (If previously executed, please ignore)
make mpp
# Execute different commands based on the model of the development board
# If the model is CanMV-K230-V1.x, execute the following command
make CONF=k230_canmv_defconfig prepare_memory
# If the model is CanMV-K230-V2.x, execute the following command
make CONF=k230_canmv_v2_defconfig prepare_memory
# If the model is K230-xxx-xxx-EVB-V1.x, execute the following command
make CONF=k230_evb_defconfig prepare_memory
cd k230_sdk/src/reference/fancy_poc
```

- Execute build_app.sh, which will generate the corresponding large core and small core files in the k230_sdk/src/reference/fancy_poc/k230_bin directory.
- Select the POC executable file you want to reference from the k230_bin directory and copy it to the development board. (Refer to each POC's readme for the corresponding executable program).
- For the kmodel and other binary files required for each POC on the board, refer to the src/download.sh in the POC directory for download and use.
