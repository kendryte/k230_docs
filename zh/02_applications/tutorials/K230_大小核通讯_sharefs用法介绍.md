# K230大小核通讯Sharefs使用简介

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

ShareFs通过对大小核各自/sharefs目录的访问，提供了大核访问小核文件系统的功能。在实际使用中，通常会将大核的可执行程序存放在/sharefs目录下，大核通过sharefs功能执行这些程序，方便大核上应用程序的开发和调试。

## 环境准备

### 硬件环境

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### 软件环境

k230_SDK

## 使用

### sharefs运行

sharefs底层依赖核间通讯的驱动组件以及上层的IPCMSG库，SDK镜像烧录后会默认开启sharefs功能，并将sd卡的最后一个分区挂载到/sharefs目录下

``` shell
/dev/mmcblk1p4 on /sharefs type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,errors=remount-ro)
```

如果空间不够的话，可以先解除挂载，然后删除掉sd卡的最后一个分区，重新分一个更大的分区，最后重启开发板，SDK会自动执行挂载。

### 文件创建写入查看

在大核rt-smart的msh命令行下，可通过echo的方式在/sharefs里创建一个文件。

``` shell
msh /sharefs>echo "hello wrold" hello.txt
```

在小核linux的shell终端下可以在/sharefs中查看这个文件内容

``` shell
[root@canaan ~ ]#cd /sharefs/
[root@canaan /sharefs ]#cat hello.txt
hello wrold[root@canaan /sharefs ]#
```

### 文件夹创建

在大核rt-smart的msh命令行下，通过mkdir创建一个目录

``` shell
msh /sharefs>mkdir test
```

在小核的linux的shell中，使用ls查看新增的目录

``` shell
[root@canaan /sharefs ]#ls
System Volume Information  hello.txt    test
```

### 文件读取

在小核linux的shell中，通过echo创建一个文件

``` shell
[root@canaan /sharefs ]#echo "hello world this is linux" >> linux.txt
```

在大核rt-smart的msh命令行下，使用cat查看文件内容

``` shell
msh /sharefs>cat linux.txt
hello world this is linux
```

### 文件加载

将编译好的rt-smart用户态可执行的elf文件，拷贝到小核的/sharefs目录，然后通过大核rt-smart的msh命令行来执行

``` shell
msh /sharefs>./hello.elf
Hello world
```

### 文件删除

在大核rt-smart的msh命令行下，使用rm删除文件

``` shell

msh /sharefs>ls
Directory /sharefs:
.                   <DIR>
..                  <DIR>
System Volume Information<DIR>
hello.txt           11
linux.txt           26
msh /sharefs>rm hello.txt
msh /sharefs>rm linux.txt
msh /sharefs>ls
Directory /sharefs:
.                   <DIR>
..                  <DIR>
System Volume Information<DIR>
msh /sharefs>
```

在小核的linux的shell中，使用ls查看删除结果

``` shell
[root@canaan /sharefs ]#ls
System Volume Information
```

### 其他

sharefs在rt-smart上支持大多数的posix文件接口操作，包括

- open
- close
- ioctl
- read
- write
- flush
- lseek
- stat
- statfs
- opendir
- rewinddir
- mkdir
- rmdir
- rename

等，感兴趣的读者可自行编写文件IO读写相关的测试代码体验

### 注意事项

- sharefs不适合高频次实时读写的场景，例如编码存盘
- 大核在sharefs下创建的文件，在linux上的读写可执行权限都存在
- sharefs不适合多进程使用，即避免在大核上启动多个进程同时读写/sharefs目录下的文件
