# CanMV-K230快速入门指南

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

## 1. 开发板概况

CanMV-K230开发板采用的是嘉楠科技Kendryte®系列AIoT芯片中的最新一代SoC芯片K230。该芯片采用全新的多异构单元加速计算架构，集成了2个RISC-V高能效计算核心，内置新一代KPU（Knowledge Process Unit）智能计算单元，具备多精度AI算力，广泛支持通用的AI计算框架，部分典型网络的利用率超过了70%。

该芯片同时具备丰富多样的外设接口，以及2D、2.5D等多个标量、向量、图形等专用硬件加速单元，可以对多种图像、视频、音频、AI等多样化计算任务进行全流程计算加速，具备低延迟、高性能、低功耗、快速启动、高安全性等多项特性。

![K230_block_diagram](images/K230_block_diagram.png)

CanMV-K230采用单板设计，扩展接口丰富，极大程度的发挥K230高性能的优势，可直接用于各种智能产品的开发，加速产品落地。

![board-front](images/CanMV-K230_front.png)
![board-behind](images/CanMV-K230_behind.png)

## 2. CanMV-K230默认套件

CanMV-K230开发板默认套件包含以下物品：

1、CanMV-K230主板 x 1

2、OV5647摄像头 x 1

3、Type-C数据线 x 1

另外，需要用户准备以下配件：

1、TF卡， 用于烧写固件，启动系统（必须）

2、带HDMI接口的显示器及HDMI连接线，显示器要求支持1080P30，否则无法显示

3、100M/1000M 以太网线缆，及有线路由器

## 3 调试说明

### 3.1 串口连接

使用Type-C线连接CanMV-K230如下图的位置，线另一端连接至电脑。

![debug](images/CanMV-K230_debug.png)

### 3.2 串口调试

#### 3.2.1 Windows

安装驱动

CanMV-K230自带usb转串口芯片 CH342，驱动下载地址<https://www.wch.cn/downloads/CH343SER_EXE.html>。

查看串口号

![windows-serial](images/windows-serial.png)

这里显示两个串口，COM80为小核Linux的调试串口，COM81为大核rt-smart的调试串口。

配置串口信息

打开工具Xshell（也可以使用其它串口工具）。

1、端口号选择设备管理器显示的端口号

2、波特率 115200

3、数据位 8

4、停止位 1

5、奇偶检验 无

6、流控制 无

![serial_setting.png](images/serial_setting.png)

#### 3.2.2 linux

Linux串口显示如下：

- `/dev/ttyACM0`为小核linux调试串口
- `/dev/ttyACM1`为大核rt-smart调试串口

可以使用linux的minicom或其它串口工具进行连接调试，串口配置信息与windows一致。

## 4 固件获取及烧录

### 4.1 固件获取

CanMV-K230 固件下载地址： <https://kendryte-download.canaan-creative.com/developer/k230>

请下载“k230_canmv”开头的gz压缩包，解压得到sysimage-sdcard.img文件，即为CanMV-K230的固件。

### 4.2 固件烧录

将固件通过电脑烧写至TF卡中。

#### 4.2.1 Linux下烧录

在TF卡插到宿主机之前，输入：

`ls -l /dev/sd\*`

查看当前的存储设备。

将TF卡插入宿主机后，再次输入：

`ls -l /dev/sd\*`

查看此时的存储设备，新增加的就是TF卡设备节点。

假设/dev/sdc就是TF卡设备节点，执行如下命令烧录TF卡：

`sudo dd if=sysimage-sdcard.img of=/dev/sdc bs=1M oflag=sync`

#### 4.2.2 Windows下烧录

Windows下可通过balena Etcher工具对TF卡进行烧录（balena Etcher工具下载地址<https://www.balena.io/etcher/>）。

1）将TF卡插入PC，然后启动balena Etcher工具，点击工具界面的"Flash from file”按钮，选择待烧写的固件。

![balena-Etcher-flash-from-file](images/balena-Etcher-flash-from-file.jpg)

2）点击工具界面的“Select target”按钮，选择目标sdcard卡。

![balena-Etcher-select-target](images/balena-Etcher-select-target.jpg)

3）点击“Flash”按钮开始烧写，烧写过程有进度条展示，烧写结束后会提示Flash Finish。

![balena-Etcher-flash](images/balena-Etcher-flash.jpg)
![balena-Etcher-finish](images/balena-Etcher-finish.jpg)

## 5 启动系统

将烧好固件的TF卡插入CanMV-K230 TF卡插槽，Type-C线连接电脑和板端的POWER口，板子即上电，系统开始启动。
![CanMV-K230-poweron](images/CanMV-K230-poweron.png)

红框的中红灯亮，则说明开发板正常上电。此时查看串口信息。

![CanMV-K230-run](images/CanMV-K230-run.png)

系统启动后默认运行人脸检测程序，将摄像头对准人脸，在显示器上会将人脸框出。

![CanMV-K230-aidemo](images/CanMV-K230-aidemo.png)
