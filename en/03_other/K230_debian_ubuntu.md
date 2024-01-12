# K230 debian ubuntu Notes

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../zh/03_other/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the K230 canmv board debian and ubuntu image download and generation  methods.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| Abbreviation               | Illustrate                                                   |
|--------------------|--------------------------------------------------------|
| gcc | GNU Compiler Collection |
| dhcp           | Dynamic Host Configuration Protocol |

### Revision history

| Document version number | Modify the description | Author     | date     |
|------------|----------|------------|----------|
| V1.0      | Initial     | System Software Department | 2023-11-8 |

## 1.  download note

debian and ubuntu related files can be found on the [canaan developer community website](https://developer.canaan-creative.com/resource) under k230/images

1.1). similar canmv_debian_sdcard_sdk_x.x.img.gz is k230 debian compressed image;

​        debian version is  trixie/sid (debian13)，You can see "Welcome to Debian GNU/Linux trixie/sid!" print at startup  .

1.2) similar canmv_ubuntu_sdcard_x.x.img.gz is k230 ubuntu compressed mirror image;

​​        debian version is Ubuntu 23.10(mantic)，You can see "Welcome to Ubuntu 23.10! "print at startup.

1.3) [debian13.ext4.tar.gz](https://kvftsfijpo.feishu.cn/file/NiOGbdnxkoYaRRxLyfJcjxYhnif) is k230 debian rootfs;

1.4). [ubuntu23_rootfs.ext4.gz](https://kvftsfijpo.feishu.cn/file/Ig3Gb4hTLogZPdxz3w6cJasZnxh)  is k230 ubuntu rootfs.

>note1:mirror image only applies to the canmv board.
>note2:image need uncompress.
>note3: The network port is unstable. If the network port cannot be found, reset the board.

## 2.k230 debian Rootfs build and verification

### 2.1environment

I  build the debian rootfs  file system in ubuntu21.04 (other systems should be able to do it too), and it need root permission.

```bash
wangjianxin@v:~/t$ lsb_release  -a
 No LSB modules are available.
 Distributor ID: Ubuntu
 Description:    Ubuntu 21.04
 Release:        21.04
 Codename:       hirsute
```

### 2.2debian rootfs  build

please  referring to the following command to build the debian rootfs.

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

### 2.3image build

1).download and compile k230 sdk

>Compile related issues please [reference](../../en/01_software/board/K230_SDK_Instructions.md#4-sdk-compilation)

```Bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
#target file is "output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img"
```

2). Decompress  [debian13.ext4.tar.gz](https://kvftsfijpo.feishu.cn/file/NiOGbdnxkoYaRRxLyfJcjxYhnif)  to output/k230_canmv_only_linux_defconfig/images/

```Bash
tar -xvf debian13.ext4.tar.gz  -C output/k230_canmv_only_linux_defconfig/images/
```

3).k230_sdk code modify：

```Bash
#board/common/gen_image_cfg/genimage-sdcard.cfg add：
 partition debian { 
        image = "debian13.ext4" 
 }
#board/common/env/default.env bootcmd modify to 
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

4).build sdk image

```Bash
make build-image
```

5).burn image and boot system

burn "output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img" file to tf card，Insert the tf card into the device and restart the device。

> note1：Burning method can [reference](<../../en/01_software/board/K230_SDK_Instructions.md#5-sdk-image-flashing>).
>
> note2: The network port is unstable. If the network port cannot be found, reset the board.

### 1.3gcc test

```bash
dhclient
date -s 20231027
apt-get update
apt-get install gcc
apt-get install ssh
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

> note: The network port is unstable. If the network port cannot be found, reset the board.

## 3. k230 ubuntu23 rootfs build

### 3.1 environment

build k230 ubuntu23 need ubuntu23 systerm, i use follow command  to build ubuntu23 systerm:

3.1.1)save follow content to Dockerfile23:

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

3.1.1)build ubuntu23 systerm

```bash
docker build -t ubuntu23:v1 . -f  Dockerfile23
```

### 3.2 k230 ubuntu rootfs build

please  referring to the following command to build the k230 ubuntu23 rootfs

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

### 3.3 image build

1).下载k230 sdk并进行编译：

> Compile related issues please [reference](../../en/01_software/board/K230_SDK_Instructions.md#4-sdk-compilation)

```Bash
git clone git@github.com:kendryte/k230_sdk.git
cd k230_sdk
source tools/get_download_url.sh && make prepare_sourcecode
docker build -f tools/docker/Dockerfile -t k230_docker tools/docker
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash
make CONF=k230_canmv_only_linux_defconfig
#target file is "output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img"
```

2). Decompress [ubuntu23_rootfs.ext4.gz](https://kvftsfijpo.feishu.cn/file/Ig3Gb4hTLogZPdxz3w6cJasZnxh)  to output/k230_canmv_only_linux_defconfig/images/

```Bash
tar -xvf ubuntu23_rootfs.ext4.gz  -C output/k230_canmv_only_linux_defconfig/images/
```

3).k230_sdk code modify：

```Bash
#board/common/gen_image_cfg/genimage-sdcard.cfg add：
 partition debian { 
        image = "ubuntu23_rootfs.ext4" 
 }
#board/common/env/default.env bootcmd modify to:
bootcmd=setenv bootargs "root=/dev/mmcblk1p5 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi";k230_boot auto auto_boot;
```

4).build sdk image

```Bash
make build-image
```

5).burn image and boot system

burn "output/k230_canmv_only_linux_defconfig/images/sysimage-sdcard.img" file to tf card，Insert the tf card into the device and restart the device。

> note1：Burning method can [reference](<../../en/01_software/board/K230_SDK_Instructions.md#5-sdk-image-flashing>).
>
> note2: The network port is unstable. If the network port cannot be found, reset the board.

### 2.4 gcc test

```bash
dhcpcd 
apt-get update
apt-get install gcc
apt-get install ssh
scp wangjianxin@10.10.1.94:~/t/a.c .
gcc a.c
./a.out 
```

> note: The network port is unstable. If the network port cannot be found, reset the board.

## 4. reference material

<https://wiki.debian.org/RISC-V>
<https://github.com/carlosedp/riscv-bringup/blob/master/Ubuntu-Rootfs-Guide.md>
