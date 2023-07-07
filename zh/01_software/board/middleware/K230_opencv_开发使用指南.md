# K230 OpenCV开发指南

![cover](images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](images/logo.png)、“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## 目录

[TOC]

## 前言

### 概述

本文档主要介绍K230 OpenCV。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明                                                        |
|------|-------------------------------------------------------------|
| OpenCV  | Open Source Computer Vision Library                                |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | 初版     | 算法部 | 2023-05-30 |

## 1.OpenCV简介

OpenCV的全称是Open Source Computer Vision Library，是一个跨平台的计算机视觉库。OpenCV是由英特尔公司发起并参与开发，以BSD许可证授权发行，可以在商业和研究领域中免费使用。OpenCV可用于开发实时的图像处理、计算机视觉以及模式识别程序。
嘉楠科技提供了针对K230优化的升级版OpenCV加速库，相比于原始版本OpenCV，可大幅减少OpenCV算子的推理时间。对比示例如下：

| 算子名称 |K230+原始版OpenCV | K230+升级版OpenCV |
| ---    |  ---      | ---             |
| 计算积分图(inter) |   34.5ms | 7.7ms |
| 仿射变换 (warpaffine) |  391.1ms |34.7ms  |

注意：
>上述算子推理时间均在K230大核+1.6GHZ的条件下测试。
>计算积分图(inter)算子：输入图像为1280x1080灰度图；积分图类型为32位浮点数。
>仿射变换 (warpaffine)算子：输入图像为1280x1080灰度图；顺时针旋转15度，缩放0.6倍；目标图像为1280x1080灰度图；

此外，SDK中已包含预先交叉编译好的升级版OpenCV加速库(位于`k230_sdk/src/big/utils/lib/opencv/`路径下)，用户直接使用该静态库编译自己的可执行程序即可。

## 2.测试用例编译示例

本节讲解如何通过SDK中预设的OpenCV静态库，来进行可执行程序的编译。SDK的已包含多个基于OpenCV实现的可执行程序编译示例(位于`k230_sdk/src/big/utils/examples/opencv/`路径下)，本节基于这些示例来进行讲解。该路径下的目录结构说明如下：

```text
|-- 1_opencv_calcHist              # OpenCV示例1
|   |-- CMakeLists.txt             # OpenCV示例1的CMake配置文件
|   `-- opencv_calcHist.cpp        # OpenCV示例1的源码
|-- 2_opencv_threshold             # OpenCV示例2
|   |-- CMakeLists.txt             # OpenCV示例2的CMake配置文件
|   `-- opencv_threshold.cpp       # OpenCV示例2的源码
|-- 3_opencv_findContours
|   |-- CMakeLists.txt
|   `-- opencv_findContours.cpp
|-- 4_opencv_features2d
|   |-- CMakeLists.txt
|   `-- opencv_features2d.cpp
|-- 5_opencv_objdetect
|   |-- CMakeLists.txt
|   `-- opencv_objdetect.cpp
|-- CMakeLists.txt               # 总体CMake配置文件
|-- build_app.sh                 # 总体编译脚本
|-- cmake                        # 默认CMaek配置
|   |-- Riscv64.cmake
|   `-- link.lds
`-- resources                    # OpenCV示例所需的所有输入图片及数据
    |-- 1.bmp
    ...
    |-- a.jpg
```

首先，运行`build_app.sh`文件：

```shell
./build_app.sh
```

在终端中出现如下提示，说明可执行程序编译成功：

```shell
Install the project...
-- Install configuration: "Release"
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/opencv/out/bin/1_opencv_calcHist.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/opencv/out/bin/2_opencv_threshold.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/opencv/out/bin/3_opencv_findContours.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/opencv/out/bin/4_opencv_features2d.elf
-- Installing: /data/zhanglimin/code_kmodel_export_build_inference_k230/k230_sdk/src/big/utils/examples/opencv/out/bin/5_opencv_objdetect.elf
```

最后，在`k230_sdk/src/big/utils/examples/opencv/out/bin`文件夹中即包含了编译好的所有elf文件：

- `1_opencv_calcHist.elf`
- `2_opencv_threshold.elf`
- `3_opencv_findContours.elf`
- `4_opencv_features2d.elf`
- `5_opencv_objdetect.elf`

## 3.测试用例运行示例

注意：
>所有测试用例运行所需的输入图像数据，均位于SDK的`k230_sdk/src/big/utils/examples/opencv/resources`路径下。

### 3.1 opencv_calcHist

`1_opencv_calcHist`测试用例的运行方式如下：

```text
msh /sharefs/bin_opencv>./1_opencv_calcHist.elf
```

`1_opencv_calcHist`测试用例的运行结果示例如下：

![test_opencv_calcHist](images/test_opencv_calcHist.png)

其中，左侧为原图像，右侧为3个channel的像素直方图信息。

### 3.2 opencv_threshold

`2_opencv_threshold`测试用例的运行方式如下：

```text
msh /sharefs/bin_opencv>./2_opencv_threshold.elf
```

`2_opencv_threshold`测试用例的运行结果示例如下：
![test_opencv_threshold](images/test_opencv_threshold.png)

其中，左侧为原图像，右侧为阈值化后的图像。

### 3.3 opencv_findContours

`3_opencv_findContours`测试用例的运行方式如下：

```text
msh /sharefs/bin_opencv>./3_opencv_findContours.elf
```

`3_opencv_findContours`测试用例的运行结果示例如下：
![test_opencv_findContours](images/test_opencv_findContours.png)

其中，左侧为原图像，右侧为处理后的轮廓信息图。

### 3.4 opencv_features2d

`4_opencv_features2d`测试用例的运行方式如下：

```text
msh /sharefs/bin_opencv>./4_opencv_features2d.elf
```

`4_opencv_features2d`测试用例的运行结果示例如下：
![test_opencv_features2d](images/test_opencv_features2d.png)
其中，左侧为原图像，右侧为处理后的特征提取结果图。

### 3.5 opencv_objdetect

`5_opencv_objdetect`测试用例的运行方式如下：

```text
msh /sharefs/bin_opencv>./5_opencv_objdetect.elf
```

`5_opencv_objdetect`测试用例的运行结果示例如下：
![test_opencv_objdetect](images/test_opencv_objdetect.png)

其中，左侧为原图像，右侧为眼睛和人脸的目标检测结果图。

## 4.原始版本OpenCV库的交叉编译及使用

注意：
>在第1~3章节中，均基于嘉楠科技提供的K230 加速版OpenCV库进行讲解。若用户希望使用原生的OpenCV库进行应用程序的开发，那可以参考本节内容：首先，通过交叉编译得到原始版本OpenCV的静态库；然后，基于原始版本OpenCV的静态库，进行可执行程序的编译。

### 4.1 下载OpenCV源码

首先，使用Github获取OpenCV仓库，由于OpenCV来自于Github，因此克隆速度慢为正常现象，请耐心等待：

```shell
git clone https://github.com/opencv/opencv.git
```

OpenCV中存在着很多版本，这里我们选用最新的版本4.6.0:

```shel
# 切换为v4.6.0分支
git checkout tags/4.6.0 -b v4.6.0-branch
```

### 4.2 应用patch补丁包

patch补丁包在SDK中的路径为：`k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0`。

首先，在OpenCV根目录下新建`patch`文件夹，并将补丁包放入`patch`文件夹中。放置好的目录结构示例如下：

```text
|-- 3rdparty
|-- patch # opencv 的 补 丁 包
| |-- 0001-****.patch
| |-- 0002-****.patch
| |-- 0003-****.patch
...
| |-- 0011-****.patch
| |-- 0017-****.patch
| |-- 0018-****.patch
|-- CMakeLists.txt
...
|-- include
|-- modules
|-- platforms
|-- samples
```

然后，在OpenCV根目录下执行以下命令应用补丁：

``` shell
git am ./patch/*.patch
```

此时，打完补丁的OpenCV目录结构示例如下：

```text
|-- 3rdparty
|-- patch
|-- CMakeLists.txt
...
|-- apps
|-- build.sh
|-- cmake
|-- data
|-- doc
|-- include
|-- modules
|-- platforms
| |-- android
...
| |-- rt_smart
| | `-- riscv64-gcc.toolchain.cmake # rt_smart平台的编译配置文件
| |-- scripts
| |-- semihosting
| |-- wince
| |-- winpack_dldt
| `-- winrt
|-- samples
`-- version
```

### 4.3 交叉编译OpenCV静态库

首先，检查`build.sh`文件中的工具链路径是否正确：

```shell
# 注意：`toolchain_path` 会随开发者具体环境不同，路径前缀会有所不同，仅供参考。
toolchain_path=~/.tools/gnu_gcc/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin
c_compiler=${toolchain_path}/riscv64-unknown-linux-musl-gcc
cxx_compiler=${toolchain_path}/riscv64-unknown-linux-musl-g++

cmake .. -G "Unix Makefiles" -DCMAKE_TOOLCHAIN_FILE="../platforms/rt_smart/riscv64-rvv-gcc.toolchain.cmake" \
-DCMAKE_C_COMPILER=$c_compiler \
-DCMAKE_CXX_COMPILER=$cxx_compiler
```

然后，创建文件夹`build`，在`build`目录中执行以下命令即可：

``` shell
source ../build.sh
make -j$(nproc)
make install
```

在编译过程中，若终端未出现告警信息，则说明编译成功，编译完成的产物在`build/install`中，其中包含了原始版本OpenCV的静态库文件。

### 4.4 编译可执行程序

本小节通过对第2节中的测试用例进行修改，来说明如何基于原始版本OpenCV库来实现可执行程序的编译。
首先，把原始版本的OpenCV库拷贝到`k230_sdk/src/big/utils/lib/`下并将文件夹命名为`opencv_rtt`。
然后，删除加速版OpenCV库，并将原始版本OpenCV库进行软链接：

```shell
cd k230_sdk/src/big/utils/lib/opencv_rtt
rm opencv
ln -s opencv_rtt opencv
```

然后，修改各个示例文件夹内(例如`1_opencv_calcHist`文件夹)下`CMakeLists.txt`文件，对链接的静态库内容进行修改，删除对`csi_cv`库的链接：

```shell
# 加速版OpenCV库，采用如下链接设置
target_link_libraries(${bin} opencv_imgcodecs opencv_imgproc opencv_core libjpeg-turbo libopenjp2 libpng libtiff libwebp zlib csi_cv)
# 原始版OpenCV库，改为如下链接设置
target_link_libraries(${bin} opencv_imgcodecs opencv_imgproc opencv_core libjpeg-turbo libopenjp2 libpng libtiff libwebp zlib)
```

最后，其余步骤（如程序的编译及运行）均与加速版本OpenCV保持一致。
