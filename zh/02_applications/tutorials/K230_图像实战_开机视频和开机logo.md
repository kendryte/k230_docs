# K230 图像实战 - 开机视频和开机logo

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

## 概述

本文将讲解如何通过视频解码在k230 evb开发板上实现开机视频和开机logo。
视频解码模块支持H.264/H.265/MJPEG解码，屏幕显示最大分辨率为1920x1080，可旋转。

## 1. 环境准备

### 1.1 硬件环境

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1
- Typec USB线，用于供电。
- SD卡
- 屏幕及连线
- 摄像头子板（IMX335）

### 1.2 软件环境

k230_sdk中提供了工具链，分别在如下路径。

- 大核rt-samrt工具链

``` shell
k230_sdk/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu
```

- 小核linux工具链

``` shell
k230_sdk/toolchain/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0
```

也可通过以下链接下载工具链

``` shell
wget https://download.rt-thread.org/rt-smart/riscv64/riscv64-unknown-linux-musl-rv64imafdcv-lp64d-20230222.tar.bz2
wget https://occ-oss-prod.oss-cn-hangzhou.aliyuncs.com/resource//1659325511536/Xuantie-900-gcc-linux-5.10.4-glibc-x86_64-V2.6.0-20220715.tar.gz
```

## 2. 源码位置

SDK中包含一个用户态解码demo，路径位于`k230_sdk/src/big/mpp/userapps/sample/sample_vdec`。编译生成的可执行文件在`k230_sdk/src/big/mpp/userapps/sample/elf/sample_vdec.elf`，默认没有加载到大核镜像中，需要按照执行方式章节修改Makefile才能在大核启动后的`/mnt`目录中生成可执行文件。

## 源码解析

1. `sample_vb_init`：配置vb pool cnt，并初始化vb。
1. `vb_create_pool`：配置vb总各个pool的block大小和个数。
1. `kd_mpi_vdec_create_chn`：创建解码通道。
1. `kd_mpi_vdec_start_chn`：开启解码通道。
1. `sample_vdec_bind_vo`：将解码绑定到vo。
1. `input_thread`：从文件中读取数据，并调用`kd_mpi_vdec_send_stream`将数据送给VPU。
1. `output_thread`：从VPU获取解码数据。

## 3. 程序执行

1. 修改`k230_sdk/Makefile`中`mpp-apps`的编译脚本。
   将

   ```sh
   cp userapps/sample/fastboot_elf/* $(RTSMART_SRC_DIR)/userapps/root/bin/; \
   ```

   改为

    ```sh
    cp userapps/sample/elf/sample_vdec.elf $(RTSMART_SRC_DIR)/userapps/root/bin/; \
    ```

1. 将需要显示的H.264/H.265/MJPEG/JPEG文件拷贝到`k230_sdk/src/big/rt-smart/userapps/root/bin`目录中

1. 修改`k230_sdk/src/big/rt-smart/init.sh`为如下命令：

    ```sh
    /bin/sample_vdec -i <filename> [-t <sec>]
    ```

    - `<filename>`为上一步中拷贝的视频文件
    - `-t`仅在显示图片时使用，为显示图片的时间。

1. 在`k230_sdk`目录下执行`make`命令。
1. 将编译生成的`k230_sdk/output/k230_evb_defconfig/images/sysimage-sdcard.img`烧写到SD卡中，EVB板拨码开关全拨到OFF(从SD卡启动)，即可实现开机显示视频。

显示效果如下：
![boot_logo](images/boot_logo.png)
