# K230 OpenCV Sensor Usage

![cover](../../../../zh/images/canaan-cover.png)

© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliates. All or part of the products, services, or features described in this document may not be within your purchase or usage scope. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended only as a usage guide reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No unit or individual may excerpt, copy, or disseminate any part or all of this document in any form without the written permission of the Company.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the method of using OpenCV to call the onboard camera on the K230 at the big core RTT end.

### Target Audience

This document (this guide) is mainly suitable for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                                       |
|--------------|---------------------------------------------------|
| OpenCV       | Open Source Computer Vision Library               |

### Revision History

| Document Version | Description | Author | Date       |
|------------------|-------------|--------|------------|
| V1.0             | Initial Version | Zhao Zhongxiang | 2024-03-22 |

## 1. Environment Setup

In `k230_sdk/src/big/mpp/userapps/src`

```shell
git clone https://github.com/opencv/opencv.git
```

You can also download OpenCV first and place it in

`k230_sdk/src/big/mpp/userapps/src/opencv`

Put the patch in `k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0`

```shell
cp k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0 k230_sdk/src/big/mpp/userapps/src/opencv/patch -r
```

Copy v4.6.0 to the patch folder.

Execute the following command in the root directory of OpenCV to apply the patch:

```shell
git am ./patch/*.patch
```

Ignore the warnings.

## 2. Compiling OpenCV

First, confirm the toolchain path in the `build.sh` path. After applying the patch, `build.sh` should be correct.

Then, create a folder named `build`, and execute the following commands in the `build` directory:

```shell
source ../build.sh
make -j
make install
```

During the compilation process, if no warning messages appear in the terminal, the compilation is successful. The compiled product will be in `build/install`, which is the OpenCV library file for the rt-smart platform.

## 3. Compiling Examples

Modify `k230_sdk/src/big/mpp/userapps/sample/Makefile`

Change

```shell
#@cd opencv_camera_test; make || exit 1
```

to

```shell
@cd opencv_camera_test; make || exit 1
```

In the `k230_sdk` directory, execute:

```shell
make mpp-apps
```

In `k230_sdk/src/big/mpp/userapps/sample/elf`, the `opencv_camera_test.elf` file will be generated.

Transfer `opencv_camera_test.elf` to the board via SCP, NFS, or by directly copying it to a TF card.

On the big core, execute:

```shell
./opencv_camera_test.elf -D 101 -m 0 -d 0 -s 24 -c 0 -f 0 -W 1920 -H 1080
```

The captured images from the ov5647 will be displayed on the HDMI screen.
