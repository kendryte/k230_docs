# K230 Inter Processer Communication Sharefs Usage

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## overview

ShareFs provides large cores with access to the small kernel file system through access to the respective /sharefs directories of large and small cores. In actual use, the executable programs of the big core are usually stored in the /sharefs directory, and the big core executes these programs through the sharefs function to facilitate the development and debugging of applications on the big core.

## Environment preparation

### Hardware environment

- K230-USIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1

### Software environment

k230_SDK

## use

### Sharefs runs

The underlying layer of sharefs depends on the driver components of inter-core communication and the upper layer of IPCMSG library, and the sharefs function will be enabled by default after the SDK image is flashed, and the last partition of the sd card will be mounted to the /sharefs directory

``` shell
/dev/mmcblk1p4 on /sharefs type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,errors=remount-ro)
```

If there is not enough space, you can unmount it first, then delete the last partition of the SD card, redivide it into a larger partition, and finally restart the development board, and the SDK will automatically perform the mount.

### File creation, write, view

Under the msh command line of RT-Smart, you can create a file in /sharefs via echo.

``` shell
msh /sharefs>echo "hello wrold" hello.txt
```

In the shell terminal of small-core Linux, the contents of this file can be viewed in /sharefs

``` shell
[root@canaan ~ ]#cd /sharefs/
[root@canaan /sharefs ]#cat hello.txt
hello wrold[root@canaan /sharefs ]#
```

### Folder creation

Under the msh command line of the big core rt-smart, create a directory through mkdir

``` shell
msh /sharefs>mkdir test
```

In the Linux shell of the little core, use ls to view the newly added directories

``` shell
[root@canaan /sharefs ]#ls
System Volume Information  hello.txt    test
```

### File read

In the shell of small-core Linux, create a file via echo

``` shell
[root@canaan /sharefs ]#echo "hello world this is linux" >> linux.txt
```

Under the msh command line of the large-core RT-SMART, use CAT to view the file contents

``` shell
msh /sharefs>cat linux.txt
hello world this is linux
```

### File loading

Copy the compiled rt-smart user-mode executable elf file to the /sharefs directory of the little core, and then execute it through the msh command line of the large kernel rt-smart

``` shell
msh /sharefs>./hello.elf
Hello world
```

### File deletion

Under the msh command line of the big core rt-smart, use rm to delete the file

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

In the shell of the small kernel Linux, use ls to see the removal results

``` shell
[root@canaan /sharefs ]#ls
System Volume Information
```

### other

ShareFS supports most POSIX file interface operations on RT-Smart, including:

- open
- close
- ioctl
- read
- write
- flush
- lseek
- state
- statfs
- OpenDir
- rewinddir
- mkdir
- rmdir
- rename

Interested readers can write their own file IO read and write related test code experience

### Notes

- ShareFS is not suitable for scenarios where high-frequency real-time reads and writes, such as encoding and saving
- Files created by large cores under sharefs, read and write executable permissions on linux are present
- sharefs is not suitable for multi-process use, that is, avoid starting multiple processes on the big core to read and write files in the /sharefs directory at the same time
