# K230 Fancy POC introduction

![cover](../../images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

## K230 Fancy POC

### Overview

The K230 Fancy Poc collection includes projects such as multimodal_chat_robot, meta_human, meta_hand and finger_reader, which aims to provide customers with POC construction process ideas.

### Hardware environment

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1/CanMV-K230 (supported by default)

### Source code location

The source code path is located in`src/reference/fancy_poc` and the directory structure is as follows:

```shell
.
├── build_app.sh
├── cmake
├── CMakeLists.txt
├── finger_reader
├── meta_hand
├── meta_human
├── multimodal_chat_robot
└── version
```

### Compile and run the program

- Enter the src/reference/fancy_poc
- Executing build_app.sh script generates all required executables in the k230_bin folder
- Copy the executable program you need from the k230_bin to run it on the K230 board
