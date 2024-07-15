# K230 debian ubuntu 说明

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

本文档主要介绍了K230 canmv板子的debian和ubuntu镜像下载及制作方法。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称               | 说明                                                   |
|--------------------|--------------------------------------------------------|
| gcc | GNU Compiler Collection |
| dhcp | Dynamic Host Configuration Protocol |

### 修订记录

| 文档版本号 | 修改说明 | 修改者     | 日期     |
|------------|----------|------------|----------|
| V1.0       | 初版     | SDK 部 | 2023-12-28 |

## 1.镜像说明

镜像请从[嘉楠开发者社区](https://developer.canaan-creative.com/resource) 下载，在嘉楠开发者社区网站的k230/images下面可以找到debian和ubuntu相关文件。

1.1). 类似xxxx_debian_sdcard_x.x.img.gz文件是k230 的debian镜像压缩包：

使用的是trixie/sid (debian13)版本，启动时会看到Welcome to Debian GNU/Linux trixie/sid!  打印。

1.2) 类似xxxx_ubuntu_sdcard_x.x.img.gz 文件是k230 ubuntu镜像压缩包：

使用的时Ubuntu 23.10 版本，启动会会看到Welcome to Ubuntu 23.10! 打印；

1.3) debian13.ext4.tar.gz 是k230 debian根文件系统。

1.4). ubuntu23_rootfs.ext4.gz是k230 ubuntu根文件系统

> 说明1：最开头的标识是板子名称，比如canmv/k230_evb等
>
> 说明2：烧录时需要先解压缩文件
>
> 说明3：网口不稳定如果找不到网口，重启下板子,

## 2 k230 debian根文件系统制作及验证

### 2.1 环境

我是在ubuntu21.04系统下制作的debian根文件系统（其他系统应该也可以），制作时需要root权限；

```bash
wangjianxin@v:~/t$ lsb_release  -a
 No LSB modules are available.
 Distributor ID: Ubuntu
 Description:    Ubuntu 21.04
 Release:        21.04
 Codename:       hirsute
```

### 2.2 debian rootfs制作

参考下面命令构建debian 根文件系统；

```Bash
sudo rm -rf debian13
sudo apt-get update
sudo apt install qemu-user-static binfmt-support debootstrap debian-ports-archive-keyring systemd-container rsync wget
sudo debootstrap --arch=riscv64  unstable debian13 https://mirrors.aliyun.com/debian/
sudo chroot debian13/
echo "root:root" | chpasswd

cat >>/etc/network/interfaces <<EOF
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
EOF
apt-get install -y  net-tools ntpdate
ntpdate ntp.ntsc.ac.cn
exit
sudo  mkfs.ext4 -d debian13  -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit debian13.ext4 1G
tar -czvf debian13.ext4.tar.gz debian13.ext4
#debian13.ext4.tar.gz 是debian的ext4格式根文件系统压缩包
```

### 2.3 镜像制作

1).下载k230 sdk并进行编译：备注：sdk编译相关问题请[参考](../../zh/01_software/board/K230_SDK_使用说明.md#4-sdk-编译)

```Bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
#编译后生成的目标文件是output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img
```

2).把debian13.ext4.tar.gz 解压缩到output/k230_canmv_only_linux_defconfig/images/ 目录下面

```Bash
tar -xvf debian13.ext4.tar.gz  -C output/k230_canmv_only_linux_defconfig/images/
```

3).k230_sdk 代码进行如下修改：

```Bash
#在board/common/gen_image_cfg/genimage-sdcard.cfg 添加如下内容：
 partition debian { 
        image = "debian13.ext4" 
 }
#把board/common/env/default.env里面bootcmd修改为如下
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

4).修改完后执行如下命令

```Bash
make build-image
```

5).烧录到tf卡，并重启设备

把output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img 文件烧录到tf卡，把tf卡插入设备并重启设备。烧录方法可以[参考](../../zh/01_software/board/K230_SDK_使用说明.md#5-sdk-镜像烧写)。

备注：网口不稳定，如果找不到网口，请重启设备试下。

### 2.3 gcc验证

备注：网口不稳定，如果没有找到网口请重启试下。

主要命令：

```bash
dhclient
date -s 20231027
apt-get update
apt-get install gcc
apt-get install ssh
apt-get install parted;parted /dev/mmcblk1 print; parted /dev/mmcblk1 resizepart 3 16G;resize2fs /dev/mmcblk1p3
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

## 3 k230 ubuntu23系统制作及验证

### 3.1 环境

制作k230 ubuntu23需要ubuntu23的操作系统，我是使用如下dockerfile建的ubuntu系统，

构建命令：docker build -t ubuntu23:v1 . -f  Dockerfile23

```Bash
#构建ubuntu23.04容器；
#docker build -t ubuntu23:v1 . -f ~/tools/docker/Dockerfile23 
#docker run  --privileged  -u root -it  -v $(pwd):$(pwd)    -w $(pwd) ubuntu23:v1  /bin/bash
FROM ubuntu:23.04
# config for default software install
ARG DEBIAN_FRONTEND=noninteractive
# install 32 bit lib for toolchain
RUN dpkg --add-architecture i386
# config ubuntu apt repo to tsinghua
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
# install software
RUN apt-get update
RUN apt install -y debootstrap  qemu-user-static binfmt-support dpkg-cross
# set default timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

### 3.2 k230 ubuntu根文件系统制作

使用下面脚本制作k230 ubuntu23 root文件系统。

```Bash
docker run  --privileged  -u root -it  -v $(pwd):$(pwd)    -w $(pwd) ubuntu23:v1  /bin/bash

rm -rf ubuntu23_rootfs
debootstrap --arch=riscv64   mantic ubuntu23_rootfs https://mirrors.aliyun.com/ubuntu-ports/
chroot ubuntu23_rootfs /bin/bash

cat >/etc/apt/sources.list <<EOF
deb https://mirrors.aliyun.com/ubuntu-ports mantic main restricted

deb https://mirrors.aliyun.com/ubuntu-ports mantic-updates main restricted

deb https://mirrors.aliyun.com/ubuntu-ports mantic universe
deb https://mirrors.aliyun.com/ubuntu-ports mantic-updates universe

deb https://mirrors.aliyun.com/ubuntu-ports mantic multiverse
deb https://mirrors.aliyun.com/ubuntu-ports mantic-updates multiverse

deb https://mirrors.aliyun.com/ubuntu-ports mantic-backports main restricted universe multiverse

deb https://mirrors.aliyun.com/ubuntu-ports mantic-security main restricted
deb https://mirrors.aliyun.com/ubuntu-ports mantic-security universe
deb https://mirrors.aliyun.com/ubuntu-ports mantic-security multiverse
EOF
echo "root:root" | chpasswd
echo k230>/etc/hostname
exit 

mkfs.ext4  -d ubuntu23_rootfs  -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit ubuntu23_rootfs.ext4 1G
tar -czvf ubuntu23_rootfs.ext4.tar.gz ubuntu23_rootfs.ext4
```

### 3.3 镜像制作及验证

1).下载k230 sdk并进行编译：备注：sdk编译相关问题请[参考](../../zh/01_software/board/K230_SDK_使用说明.md#43-编译-sdk)

```Bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
#编译后生成的目标文件是output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img
```

2).把ubuntu23_rootfs.ext4.tar.gz 解压缩到output/k230_evb_only_linux_defconfig/images/ 目录下面

```Bash
tar -xvf ubuntu23_rootfs.ext4.gz  -C output/k230_canmv_only_linux_defconfig/images/
```

3).k230_sdk 代码进行如下修改：

```Bash
#在board/common/gen_image_cfg/genimage-sdcard.cfg 添加如下内容：
 partition debian { 
        image = "ubuntu23_rootfs.ext4" 
 }
#把board/common/env/default.env里面bootcmd修改为如下
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

4).修改完后执行

```Bash
make build-image
```

5).烧录到tf卡，并重启设备

把output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img 文件烧录到tf卡，把tf卡插入设备并重启设备。烧录方法可以[参考](../../zh/01_software/board/K230_SDK_使用说明.md)。

备注：网口不稳定，如果找不到网口，请重启设备试下。

### 3.4 gcc 验证

主要命令：

```bash
dhcpcd 
date -s "20240507 15:06"
apt-get update
apt-get install gcc
apt-get install ssh
apt-get install parted;parted /dev/mmcblk1 print; parted /dev/mmcblk1 resizepart 3 16G;resize2fs /dev/mmcblk1p3
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

## 4 添加Qt及lxqt支持

### 4.1 安装Qt, lxqt

参考[debian根文件系统制作](#22-debian-rootfs制作)或[ubuntu根文件系统制作](#32-k230-ubuntu根文件系统制作)步骤

```sh
chroot /path/to/rootfs
apt-get install openssh-server
apt-get install libdrm-dev
apt-get install qtbase5-dev qtbase5-examples
apt-get install lxqt
systemctl disable sddm
```

### 4.2运行Qt example

新建QPA输出配置文件，复制以下内容到`kms_config.json`

```json
{
  "device": "/dev/dri/card0",
  "outputs": [
    { "name": "DSI1", "format": "argb8888" }
  ]
}
```

新建QPA环境变量文件，复制以下内容到`env.sh`

```sh
export QT_QPA_PLATFORM=linuxfb
export QT_QPA_FB_DRM=1
export QT_QPA_EGLFS_KMS_CONFIG="/root/kms_config.json"
```

通过以下命令运行Qt example

```sh
source env.sh
/usr/lib/riscv64-linux-gnu/qt5/examples/gui/analogclock/analogclock
```

### 4.3 运行lxqt

目前lxqt只能通过X11Forwarding在pc或其他平台显示，通过ssh -X连接到板子，然后执行`startlxqt`

## 5 参考资料

<https://wiki.debian.org/RISC-V>
<https://github.com/carlosedp/riscv-bringup/blob/master/Ubuntu-Rootfs-Guide.md>
