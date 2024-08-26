# K230 AI Practical - HHB Neural Network Model Deployment Tool

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright ©2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase should be governed by the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. Some or all of the products, services, or features described in this document may not fall within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for guidance and reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document is a user manual for using HHB on the K230 hardware platform, guiding users on how to compile models on HHB to generate C code, how to use the K230 cross-compilation toolchain to compile programs, and how to run them on the board.

### Target Audience

This document (this guide) is mainly intended for the following personnel:

- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description                          |
| ------------ | ------------------------------------ |
| HHB          | Heterogeneous Honey Badger           |
| SHL          | Structure of Heterogeneous Library   |

### Revision History

| Document Version | Description  | Author | Date       |
| ---------------- | ------------ | ------ | ---------- |
| V1.0             | Initial Draft | Zhang Yang | 2023/6/25  |

## 1. Overview

To deploy and run the HHB program on the K230 RTT, the following steps are required:

- Compile the model to generate C code based on the HHB development environment.
- Use the K230 RTT cross-compilation toolchain to compile the C code.
- Run the executable program on the board.

### 1.1 HHB

HHB (Heterogeneous Honey Badger) is a neural network model deployment toolset provided by T-Head for the Xuantie chip platform. It includes a series of tools needed for deployment, such as compilation optimization, performance analysis, process debugging, and result simulation.

HHB's features and characteristics:

- Supports models in formats corresponding to Caffe, TensorFlow, ONNX, and TFLite.
- Supports data types such as 8/16-bit fixed-point and 16/32-bit floating-point.
- Supports symmetric and asymmetric fixed-point quantization, as well as channel quantization.
- Optimizes the network structure of the model before deployment.
- Compiles and generates binaries executable on the Wujian SoC platform.
- Supports behavioral simulation on the host.
- Provides a multi-component toolset for secondary development.
- Offers both traditional Unix command-line and Python interfaces.

HHB supports various business algorithms for speech and vision and can import models from different training frameworks such as PyTorch and TensorFlow.

HHB is based on the open-source project [TVM](https://github.com/apache/tvm), adding rich command-line options to provide command mode; it presets various quantization algorithms to adapt to data types supported by different platforms; and outputs C code calling SHL or directly outputs executable binaries according to different platform characteristics.

![HHB Framework Structure](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6288173861/p668762.png)

For detailed usage, please refer to the [HHB User Manual](https://www.yuque.com/za4k4z/oxlbxl).

### 1.2 SHL

SHL is a set of neural network library APIs provided by T-HEAD for the Xuantie CPU platform. It abstracts the interfaces of various commonly used network layers and provides a series of optimized binary libraries.

SHL's features:

- Reference implementation in C code.
- Provides assembly optimized implementation for the Xuantie series CPUs.
- Supports symmetric quantization and asymmetric quantization.
- Supports data types such as 8-bit fixed-point, 16-bit fixed-point, and 16-bit floating-point.
- Compatible with NCHW and NHWC formats.
- Automatically calls code with [HHB](https://www.yuque.com/za4k4z/oxlbxl).
- Covers different architectures such as CPU and NPU.
- Provides heterogeneous reference implementations.

SHL provides complete interface declarations and reference implementations of the interfaces. Device vendors can complete the optimization of each interface as needed.

For detailed usage, please refer to the [SHL User Manual](https://www.yuque.com/za4k4z/isgz8o/ayilv9).

## 2. HHB Model Compilation

### 2.1 Environment Setup

> Prerequisite: Docker is installed on the local PC.

- Download the hhb-2.2.35 docker image from [HHB](https://xuantie.t-head.cn/community/download?id=4212696449735004160).

- Extract/load/start the docker image.

  ```shell
  tar xzf hhb-2.2.35.docker.tar.gz
  cd hhb-2.2.35.docker/
  docker load < hhb.2.2.35.img.tar
  ./start_hhb.sh
  ```

### 2.2 Model Compilation

The current version of the docker image does not integrate the C908 model compilation. Here, we copy C906 and modify the relevant configuration.

```shell
root@02297217e66d:~# cd /home/example/
root@02297217e66d:/home/example# cp -a c906 c908
root@02297217e66d:/home/example# cd c908/onnx_mobilenetv2/
```

Modify run.sh

- Change the value of the --board parameter (from c906 to c908).
- Add the calibration set parameter (-cd).
- Add quantization parameters (--quantization-scheme).

The modified run.sh content is as follows:

```shell
#!/bin/bash -x

hhb -S --model-file mobilenetv2-12.onnx  --data-scale 0.017 --data-mean "124 117 104" --board c908 --input-name "input" --output-name "output" --input-shape "1 3 224 224" --postprocess save_and_top5 --simulate-data persian_cat.jpg -cd persian_cat.jpg   --quantization-scheme "int8_asym_w_sym" --fuse-conv-relu
```

> Note: Different models may have different compilation parameters, which may cause performance data differences. Users need to understand the meaning of each HHB parameter (hhb -h) or consult T-Head.

Execute run.sh to start compilation.

```shell
root@02297217e66d:/home/example/c908/onnx_mobilenetv2# ./run.sh
+ hhb -S --model-file mobilenetv2-12.onnx --data-scale 0.017 --data-mean '124 117 104' --board c908 --input-name input --output-name output --input-shape '1 3 224 224' --postprocess save_and_top5 --simulate-data persian_cat.jpg -cd persian_cat.jpg --quantization-scheme int8_asym_w_sym --fuse-conv-relu
[2023-06-21 09:02:53] (HHB LOG): Start import model.
[2023-06-21 09:02:55] (HHB LOG): Model import completed!
[2023-06-21 09:02:55] (HHB LOG): Start quantization.
[2023-06-21 09:02:55] (HHB LOG): get calibrate dataset from persian_cat.jpg
[2023-06-21 09:02:55] (HHB LOG): Start optimization.
[2023-06-21 09:02:55] (HHB LOG): Optimization completed!
Calibrating: 100%|###############################################################################################################################################################################################################################| 153/153 [00:14<00:00, 10.66it/s]
[2023-06-21 09:03:10] (HHB LOG): Start conversion to csinn.
[2023-06-21 09:03:10] (HHB LOG): Conversion completed!
[2023-06-21 09:03:10] (HHB LOG): Start operator fusion.
[2023-06-21 09:03:10] (HHB LOG): Operator fusion completed!
[2023-06-21 09:03:10] (HHB LOG): Start operator split.
[2023-06-21 09:03:10] (HHB LOG): Operator split completed!
[2023-06-21 09:03:10] (HHB LOG): Start layout convert.
[2023-06-21 09:03:10] (HHB LOG): Layout convert completed!
[2023-06-21 09:03:10] (HHB LOG): Quantization completed!
[2023-06-21 09:03:14] (HHB LOG): cd hhb_out; qemu-riscv64 -cpu c908v hhb_runtime ./hhb.bm persian_cat.jpg.0.bin
Run graph execution time: 1675.78113ms, FPS=0.60

=== tensor info ===
shape: 1 3 224 224
data pointer: 0x2e0b40

=== tensor info ===
shape: 1 1000
data pointer: 0x325530
The max_value of output: 16.053827
The min_value of output: -8.026914
The mean_value of output: 0.002078
The std_value of output: 11.213154
============ top5: ===========
283: 16.053827
281: 14.920615
282: 12.559759
285: 12.182022
287: 11.520982
```

Finally, the hhb_out directory is generated as follows:

```shell
root@02297217e66d:/home/example/c908/onnx_mobilenetv2# ll hhb_out
total 17940
drwxr-xr-x 2 root root    4096 Jun 21 09:03 ./
drwxr-xr-x 5 root root    4096 Jun 21 09:02 ../
-rw-r--r-- 1 root root 3554304 Jun 21 09:03 hhb.bm
-rwxr-xr-x 1 root root 6140744 Jun 21 09:03 hhb_runtime*
-rw-r--r-- 1 root root  602112 Jun 21 09:03 input.0.bin
-rw-r--r-- 1 root root 2860548 Jun 21 09:03 input.0.tensor
-rw-r--r-- 1 root root    4946 Jun 21 09:03 io.c
-rw-r--r-- 1 root root    1539 Jun 21 09:03 io.h
-rw-r--r-- 1 root root    7410 Jun 21 09:03 main.c
-rw-r--r-- 1 root root   81352 Jun 21 09:03 main.o
-rw-r--r-- 1 root root  112618 Jun 21 09:03 model.c
-rw-r--r-- 1 root root  791576 Jun 21 09:03 model.o
-rw-r--r-- 1 root root 3546112 Jun 21 09:03 model.params
-rw-r--r-- 1 root root  602112 Jun 21 09:03 persian_cat.jpg.0.bin
-rw-r--r-- 1 root root    9534 Jun 21 09:03 persian_cat.jpg.0.bin_output0_1_1000.txt
-rw-r--r-- 1 root root   20086 Jun 21 09:03 process.c
-rw-r--r-- 1 root root    2040 Jun 21 09:03 process.h
```

Copy the hhb_out directory to /mnt and export it to the PC. You will need to re-cross-compile using the K230 RTT toolchain later.

```shell
root@02297217e66d:/home/example/c908/onnx_mobilenetv2# cp -a hhb_out/ /mnt/
```

## 3. Demo

### 3.1 Environment Setup

> Prerequisite: The user has compiled the docker image according to the k230_sdk documentation.

Start the K230 docker image.

```shell
cd /path/to/k230_sdk
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
```

### 3.2 Compile the Demo

We provide an HHB demo in k230_sdk. Users only need to copy the C code compiled by HHB to compile an executable program that can run on the board.

Directory description:

| Directory                                                     | Remarks                                                        |
| ------------------------------------------------------------- | -------------------------------------------------------------- |
| /path/to/k230_sdk/src/big/utils/examples/hhb                  | Users can modify CMakeLists.txt to add demos                   |
| /path/to/k230_sdk/src/big/utils/lib/csi-nn2 and hhb-prebuilt-decode | Precompiled libraries (csi-nn2/jpeg/png/zlib, compiled using musl cross-compilation toolchain) |

Prepare the example:

The mbv2_onnx_int8 directory is the C code generated by the previous HHB. Users need to update it after modifying the model compilation parameters.

Users can also add demos according to their models by modifying CMakeLists.txt.

### Start Compilation

```shell
root@9d2a450436a7:/home/zhangyang/workspace/k230_sdk# cd src/big/utils/examples/hhb/
root@9d2a450436a7:/home/zhangyang/workspace/k230_sdk/src/big/utils/examples/hhb# ./build_app.sh
```

The final generated executable program is `out/bin/mbv2_onnx_int8.elf`.

```shell
root@9d2a450436a7:/home/zhangyang/workspace/k230_sdk/src/big/utils/examples/hhb# ll out/bin/mbv2_onnx_int8.elf 
-rwxr-xr-x 1 root root 1172680 Jun 25 14:37 out/bin/mbv2_onnx_int8.elf*
```

Transfer the relevant files for running `mbv2_onnx_int8` to the `/sharefs` directory of the small core Linux.

```shell
[root@canaan /sharefs/k230/mbv2_onnx_int8 ]#ls -l
total 5560
-rw-r--r--    1 sshd     sshd       3554304 Jun 25  2023 hhb.bm
-rwxr-xr-x    1 sshd     sshd       1172680 Jun 25  2023 mbv2_onnx_int8.elf
-rw-r--r--    1 sshd     sshd        359355 Jun 25  2023 persian_cat.jpg
-rw-r--r--    1 sshd     sshd        602112 Jun 25  2023 persian_cat.jpg.0.bin
```

### 3.3 Running the Demo

- Start the K230, and execute the following commands in the large core RTT serial console.

```shell
msh />cd /sharefs/k230/mbv2_onnx_int8/

msh /sharefs/k230/mbv2_onnx_int8>./mbv2_onnx_int8.elf hhb.bm persian_cat.jpg.0.bin
Run graph execution time: 64.71648ms, FPS=15.45

=== tensor info ===
shape: 1 3 224 224 
data pointer: 0x300170060

=== tensor info ===
shape: 1 1000 
data pointer: 0x300194c80
The max_value of output: 15.581656
The min_value of output: -8.026914
The mean_value of output: 0.008405
The std_value of output: 11.703238
============ top5: ===========
283: 15.581656
281: 14.731747
282: 12.559759
285: 11.709850
287: 11.143245

msh /sharefs/k230/mbv2_onnx_int8>./mbv2_onnx_int8.elf hhb.bm persian_cat.jpg      
Run graph execution time: 64.67589ms, FPS=15.46

=== tensor info ===
shape: 1 3 224 224 
data pointer: 0x300170060

=== tensor info ===
shape: 1 1000 
data pointer: 0x300194c80
The max_value of output: 16.053827
The min_value of output: -8.026914
The mean_value of output: 0.009821
The std_value of output: 12.815542
============ top5: ===========
283: 16.053827
281: 15.109484
282: 13.220798
287: 12.087587
285: 11.804284
```
