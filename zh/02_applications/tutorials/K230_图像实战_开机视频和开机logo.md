# K230 图像实战 - 开机视频和开机logo

## 概述

本文将讲解如何通过视频解码在k230 evb开发板上实现开机视频和开机logo。
视频解码模块支持H.264/H.265/MJPEG解码，屏幕显示最大分辨率为1920x1080，可旋转。

## 环境准备

### 硬件环境

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1
- Typec USB线，用于供电。
- SD卡
- 屏幕及连线
- 摄像头子板（IMX335）

### 软件环境

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

## 源码位置

SDK中包含一个用户态解码demo，路径位于`k230_sdk/src/big/mpp/userapps/sample/sample_vdec`。编译生成的可执行文件在`k230_sdk/src/big/mpp/userapps/sample/elf/sample_vdec.elf`，默认没有加载到大核镜像中，需要按照执行方式章节修改Makefile才能在大核启动后的`/mnt`目录中生成可执行文件。

## 源码解析

1. `sample_vb_init`：配置vb pool cnt，并初始化vb。
1. `vb_create_pool`：配置vb总各个pool的block大小和个数。
1. `kd_mpi_vdec_create_chn`：创建解码通道。
1. `kd_mpi_vdec_start_chn`：开启解码通道。
1. `sample_vdec_bind_vo`：将解码绑定到vo。
1. `input_thread`：从文件中读取数据，并调用`kd_mpi_vdec_send_stream`将数据送给VPU。
1. `output_thread`：从VPU获取解码数据。

## 程序执行

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
