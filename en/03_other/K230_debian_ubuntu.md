# K230 Debian Ubuntu Instructions

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../zh/03_other/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate all or part of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the download and creation methods of Debian and Ubuntu images for the K230 canmv board.

### Target Audience

This document (this guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
| gcc          | GNU Compiler Collection |
| dhcp         | Dynamic Host Configuration Protocol |

### Revision History

| Document Version | Modification Description | Modifier | Date       |
|------------------|--------------------------|----------|------------|
| V1.0             | Initial version          | SDK Dept | 2023-12-28 |

## 1. Image Description

Please download the images from the [Canaan Developer Community](https://developer.canaan-creative.com/resource). You can find Debian and Ubuntu related files under k230/images on the Canaan Developer Community website.

1.1) Files like xxxx_debian_sdcard_x.x.img.gz are compressed Debian images for the K230:

Using the trixie/sid (Debian 13) version, you will see "Welcome to Debian GNU/Linux trixie/sid!" printed during startup.

1.2) Files like xxxx_ubuntu_sdcard_x.x.img.gz are compressed Ubuntu images for the K230:

Using the Ubuntu 23.10 version, you will see "Welcome to Ubuntu 23.10!" printed during startup.

1.3) debian13.ext4.tar.gz is the K230 Debian root filesystem.

1.4) ubuntu23_rootfs.ext4.gz is the K230 Ubuntu root filesystem.

> Note 1: The prefix indicates the board name, such as canmv/k230_evb, etc.
>
> Note 2: You need to decompress the file before burning it.
>
> Note 3: If the network port is unstable and cannot be found, restart the board.

## 2. Creating and Verifying the K230 Debian Root Filesystem

### 2.1 Environment

I created the Debian root filesystem under the Ubuntu 21.04 system (other systems should also work). Root privileges are required during creation.

```bash
wangjianxin@v:~/t$ lsb_release -a
 No LSB modules are available.
 Distributor ID: Ubuntu
 Description:    Ubuntu 21.04
 Release:        21.04
 Codename:       hirsute
```

### 2.2 Creating the Debian Root Filesystem

Refer to the following commands to build the Debian root filesystem:

```bash
sudo rm -rf debian13
sudo apt-get update
sudo apt install qemu-user-static binfmt-support debootstrap debian-ports-archive-keyring systemd-container rsync wget
sudo debootstrap --arch=riscv64 unstable debian13 https://mirrors.aliyun.com/debian/
sudo chroot debian13/
echo "root:root" | chpasswd

cat >>/etc/network/interfaces <<EOF
auto lo
iface lo inet loopback
auto eth0
iface eth0 inet dhcp
EOF
apt-get install -y net-tools ntpdate
ntpdate ntp.ntsc.ac.cn
exit
sudo mkfs.ext4 -d debian13 -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit debian13.ext4 1G
tar -czvf debian13.ext4.tar.gz debian13.ext4
# debian13.ext4.tar.gz is the compressed package of the Debian ext4 format root filesystem
```

### 2.3 Creating the Image

1) Download the K230 SDK and compile it. Note: For SDK compilation-related issues, please refer to [this guide](../../zh/01_software/board/K230_SDK_使用说明.md#4-sdk-编译).

```bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
# The target file generated after compilation is output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img
```

1) Decompress debian13.ext4.tar.gz to the output/k230_canmv_only_linux_defconfig/images/ directory.

```bash
tar -xvf debian13.ext4.tar.gz -C output/k230_canmv_only_linux_defconfig/images/
```

1) Modify the K230 SDK code as follows:

```bash
# Add the following content to board/common/gen_image_cfg/genimage-sdcard.cfg:
partition debian { 
        image = "debian13.ext4" 
}
# Modify bootcmd in board/common/env/default.env to the following:
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

1) After modification, execute the following command:

```bash
make build-image
```

1) Burn it to the TF card and restart the device.

Burn the output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img file to the TF card, insert the TF card into the device, and restart the device. For the burning method, please refer to [this guide](../../zh/01_software/board/K230_SDK_使用说明.md#5-sdk-镜像烧写).

Note: If the network port is unstable and cannot be found, please restart the device and try again.

### 2.3 GCC Verification

Note: If the network port is unstable and cannot be found, please restart and try again.

Main commands:

```bash
dhclient
date -s 20231027
apt-get update
apt-get install gcc
apt-get install ssh
apt-get install parted; parted /dev/mmcblk1 print; parted /dev/mmcblk1 resizepart 3 16G; resize2fs /dev/mmcblk1p3
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

## 3. Creating and Verifying the K230 Ubuntu 23 System

### 3.1 Environment

Creating the K230 Ubuntu 23 requires an Ubuntu 23 operating system. I used the following Dockerfile to build the Ubuntu system.

Build command: docker build -t ubuntu23:v1 . -f Dockerfile23

```bash
# Build the Ubuntu 23.04 container:
# docker build -t ubuntu23:v1 . -f ~/tools/docker/Dockerfile23 
# docker run --privileged -u root -it -v $(pwd):$(pwd) -w $(pwd) ubuntu23:v1 /bin/bash
FROM ubuntu:23.04 
# Config for default software install
ARG DEBIAN_FRONTEND=noninteractive 
# Install 32-bit lib for toolchain
RUN dpkg --add-architecture i386 
# Config Ubuntu apt repo to Tsinghua
RUN sed -i 's/archive.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.tuna.tsinghua.edu.cn/g' /etc/apt/sources.list 
# Install software
RUN apt-get update
RUN apt install -y debootstrap qemu-user-static binfmt-support dpkg-cross 
# Set default timezone
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
```

### 3.2 Creating the K230 Ubuntu Root Filesystem

Use the following script to create the K230 Ubuntu 23 root filesystem.

```bash
docker run --privileged -u root -it -v $(pwd):$(pwd) -w $(pwd) ubuntu23:v1 /bin/bash

rm -rf ubuntu23_rootfs
debootstrap --arch=riscv64 mantic ubuntu23_rootfs https://mirrors.aliyun.com/ubuntu-ports/
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

mkfs.ext4 -d ubuntu23_rootfs -r 1 -N 0 -m 1 -L "rootfs" -O ^64bit ubuntu23_rootfs.ext4 1G
tar -czvf ubuntu23_rootfs.ext4.tar.gz ubuntu23_rootfs.ext4
```

### 3.3 Creating and Verifying the Image

1) Download the K230 SDK and compile it. Note: For SDK compilation-related issues, please refer to [this guide](../../zh/01_software/board/K230_SDK_使用说明.md#43-编译-sdk).

```bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
# The target file generated after compilation is output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img
```

1) Decompress ubuntu23_rootfs.ext4.tar.gz to the output/k230_evb_only_linux_defconfig/images/ directory.

```bash
tar -xvf ubuntu23_rootfs.ext4.gz -C output/k230_canmv_only_linux_defconfig/images/
```

1) Modify the K230 SDK code as follows:

```bash
# Add the following content to board/common/gen_image_cfg/genimage-sdcard.cfg:
partition debian { 
        image = "ubuntu23_rootfs.ext4" 
}
# Modify bootcmd in board/common/env/default.env to the following:
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

1) After modification, execute:

```bash
make build-image
```

1) Burn it to the TF card and restart the device.

Burn the output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img file to the TF card, insert the TF card into the device, and restart the device. For the burning method, please refer to [this guide](../../zh/01_software/board/K230_SDK_使用说明.md).

Note: If the network port is unstable and cannot be found, please restart the device and try again.

### 3.4 GCC Verification

Main commands:

```bash
dhcpcd 
date -s "20240507 15:06"
apt-get update
apt-get install gcc
apt-get install ssh
apt-get install parted; parted /dev/mmcblk1 print; parted /dev/mmcblk1 resizepart 3 16G; resize2fs /dev/mmcblk1p3
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

## 4. Adding Qt and LXQt Support

### 4.1 Installing Qt, LXQt

Refer to [Creating the Debian Root Filesystem](#22 Creating the Debian Root Filesystem) or [Creating the K230 Ubuntu Root Filesystem](#32 Creating the K230 Ubuntu Root Filesystem) steps.

```sh
chroot /path/to/rootfs
apt-get install openssh-server
apt-get install libdrm-dev
apt-get install qtbase5-dev qtbase5-examples
apt-get install lxqt
systemctl disable sddm
```

### 4.2 Running Qt Example

Create a new QPA output configuration file and copy the following content to `kms_config.json`:

```json
{
  "device": "/dev/dri/card0",
  "outputs": [
    { "name": "DSI1", "format": "argb8888" }
  ]
}
```

Create a new QPA environment variable file and copy the following content to `env.sh`:

```sh
export QT_QPA_PLATFORM=linuxfb
export QT_QPA_FB_DRM=1
export QT_QPA_EGLFS_KMS_CONFIG="/root/kms_config.json"
```

Run the Qt example with the following command:

```sh
source env.sh
/usr/lib/riscv64-linux-gnu/qt5/examples/gui/analogclock/analogclock
```

4.3 Running LXQt

Currently, LXQt can only be displayed on a PC or other platforms via X11 Forwarding. Connect to the board using `ssh -X`, and then execute `startlxqt`.

## 5. References

<https://wiki.debian.org/RISC-V>
<https://github.com/carlosedp/riscv-bringup/blob/master/Ubuntu-Rootfs-Guide.md>
