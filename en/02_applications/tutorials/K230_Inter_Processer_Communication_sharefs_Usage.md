# Introduction to K230 Big-Little Core Communication with Sharefs

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Canaan Creative (Beijing) Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Canaan Creative (Beijing) Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative (Beijing) Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Overview

ShareFs provides the functionality for the big core to access the file system of the little core by accessing the respective /sharefs directories of the big and little cores. In practical use, executable programs for the big core are usually stored in the /sharefs directory, and the big core executes these programs using the sharefs functionality, facilitating the development and debugging of applications on the big core.

## Environment Preparation

### Hardware Environment

- K230-USIP-LP3-EVB-V1.0 / K230-UNSIP-LP3-EVB-V1.1

### Software Environment

k230_SDK

## Usage

### Running sharefs

Sharefs relies on the inter-core communication driver component and the upper-layer IPCMSG library. After burning the SDK image, the sharefs functionality will be enabled by default, and the last partition of the SD card will be mounted to the /sharefs directory.

```shell
/dev/mmcblk1p4 on /sharefs type vfat (rw,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=iso8859-1,shortname=mixed,utf8,errors=remount-ro)
```

If there is not enough space, you can unmount it first, then delete the last partition of the SD card, repartition it to a larger size, and finally restart the development board. The SDK will automatically execute the mounting.

### Creating, Writing, and Viewing Files

In the rt-smart command line of the big core, you can create a file in /sharefs using the echo command.

```shell
msh /sharefs>echo "hello world" hello.txt
```

In the shell terminal of the little core running Linux, you can view the content of this file in /sharefs.

```shell
[root@canaan ~]#cd /sharefs/
[root@canaan /sharefs]#cat hello.txt
hello world[root@canaan /sharefs]#
```

### Creating Folders

In the rt-smart command line of the big core, create a directory using mkdir.

```shell
msh /sharefs>mkdir test
```

In the shell of the little core running Linux, use ls to view the newly created directory.

```shell
[root@canaan /sharefs]#ls
System Volume Information  hello.txt  test
```

### Reading Files

In the shell of the little core running Linux, create a file using echo.

```shell
[root@canaan /sharefs]#echo "hello world this is linux" >> linux.txt
```

In the rt-smart command line of the big core, use cat to view the file content.

```shell
msh /sharefs>cat linux.txt
hello world this is linux
```

### Loading Files

Copy the compiled rt-smart user-mode executable ELF file to the /sharefs directory of the little core, and then execute it through the rt-smart command line of the big core.

```shell
msh /sharefs>./hello.elf
Hello world
```

### Deleting Files

In the rt-smart command line of the big core, delete files using rm.

```shell
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

In the shell of the little core running Linux, use ls to check the deletion result.

```shell
[root@canaan /sharefs]#ls
System Volume Information
```

### Others

Sharefs supports most POSIX file interface operations on rt-smart, including:

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

Interested readers can write their own file I/O related test code to experience.

### Notes

- Sharefs is not suitable for high-frequency real-time read-write scenarios, such as encoding and saving.
- Files created by the big core in sharefs have read-write and executable permissions in Linux.
- Sharefs is not suitable for multi-process use, i.e., avoid starting multiple processes on the big core to read and write files in the /sharefs directory simultaneously.
