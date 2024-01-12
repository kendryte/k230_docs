# K230小核Linux驱动API参考

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

本文档主要介绍K230小核Linux的驱动api，主要包括uart、i2c、gpio、watchdog、hardlock、OTP、Tsensor、TRNG等。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称      | 说明                                         |
|-----------|---------------------------------------------|
| UART      | Universal Asynchronous Receiver/Transmitter |
| I2C       | Inter-Integrated Circuit                    |
| GPIO      | General-purpose input/output                |
| Hard-lock | 硬件互斥锁                                   |
| WDT       | watchdog                                    |
| OTP       | One-Time Programmable                       |
| TS        | Temperature Sensor                          |
| TRNG      | True Random Number Generator                |
| ADC       | analog-to_digital converter                 |
| PWM       | Pulse Width Modulation                      |
| FBTFT     | small TFT LCD display                       |

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期         |
|------------|----------|--------|---------|
| V1.0       | 初版     | 范俊涛 | 2023/5/26 |
| V1.1       | 增加ADC, PWM部分内容 | 范俊涛 | 2023/8/4 |
| V1.2       | 增加ST7735S配置章节  | 范俊涛 | 2023/9/5 |

## 1 概述

### 1.1 概述

UART：
通用异步收发器，该总线双向通信，可以实现全双工传输和接收。在嵌入式设计中，UART用来与PC进行通信，包括与监控调试器和其它器件，如EEPROM通信。

I2C：
由Philips公司（2006年迁移到NXP）在1980年代初开发的一种简单、双线双向的同步串行总线，它利用一根时钟线和一根数据线在连接总线的两个器件之间进行信息的传递，为设备之间数据交换提供了一种简单高效的方法。每个连接到总线上的器件都有唯一的地址，任何器件既可以作为主机也可以作为从机，但同一时刻只允许有一个主机。

GPIO：
（general porpose intput output）通用输入输出端口的简称。可以通过软件控制其输出和输入，通俗来说就是常用引脚，可以控制引脚的高低电平，对其进行读取或者写入。

Hard-lock：
嘉楠自研模块，用于同核不通进程间或异核之间对共享资源的互斥而实现的硬件互斥锁，可用于对共享资源的互斥使用。

WDT：
WDT是watchdog的简称，本质上是一个硬件定时器，软件程序需要每隔一段时间喂一次狗，如果WDT超时则可以产生一个中断信号或复位信号到CPU，由此通过软硬件结合的方式防止程序运行异常而不能恢复。

OTP：
OTP 主要用于存储安全敏感的机密信息，例如 bootrom 的固件信息、加解密密钥、签名信息以及用户自己定义的安全信息等。

TS：
K230 TS（Temperature Sensor），自研温度传感器，采用 TSMC 12nm 工艺，TS 的应用场景是降频。

TRNG：
TRNG 主要用于产生真随机数，从而为加解密运算提供一个随机熵源。

ADC：
ADC 指模数转换器，是指将连续变化的模拟信号转换为离散的数字信号的器件。

PWM：
PWM 脉冲宽度调制，是一种对模拟信号电平进行数字编码的方法，通过调制正脉冲周期所占的比例来对一个具体模拟信号的电平进行编码。

FBTFT：
FBTFT 小屏幕驱动，支持framebuffer，内核现已很少维护，驱动代码在 `driver/staging/fbtft` 下。

### 1.2 功能描述

#### 1.2.1 uart模块

K230共有5路uart，且uart模块支持红外模式，支持RS485模式，支持DMA，部分端口支持流控，数据位支持5/6/7/8比特，停止位1/2比特，波特率可以支持到1.5MHz。

#### 1.2.2 i2c模块

K230共有5路i2c，i2c模块支持主模式，支持DMA，支持7/10比特寻址，支持中断，i2c模块传输速率支持100k/400k/1M/3.4M.

#### 1.2.3 gpio模块

k230共有2路gpio，每路gpio包含32个gpio端口，共64个gpio端口，每个gpio端口均支持输入输出功能，支持上升沿中断，下降沿中断，高低电平中断，和双边沿中断。k230的每个gpio端口的中断相互独立互不影响。

#### 1.2.4 hard-lock模块

k230有128个硬件互斥锁，其作用类似Linux的自旋锁，可以用于对同一资源的互斥。

#### 1.2.5 wdt模块

wdt，watchdog模块，k230有两路wdt，大小核分别使用一路，wdt支持中断和复位两种模式，默认使用复位模式，即当wdt的超时时间溢出时，直接使soc复位。

#### 1.2.6 OTP模块

OTP 集成在安全模块 PUF 中，为整个 SoC 提供安全存储功能，保护根密钥和启动代码等关键数据不被攻击者破坏。小核侧 OTP 驱动主要提供读功能，可读写区域空间为768bytes。Linux 侧 OTP 驱动挂载在 nvmem 框架上，具体的框架结构如下图所示：

![otp](images/otp_linux.png)

#### 1.2.7 TS模块

大核侧 TS 驱动主要提供读功能，在读 TS 之前，首先需要配置 TS 寄存器使能信号、输出模式，然后才能读出芯片的结温。另外，TS 寄存器每 2.6s 读取一次芯片结温。Rt-smart 侧 TS 驱动的结构如下图所示：

![ts](images/ts_linux.png)

#### 1.2.8 TRNG模块

TRNG 集成在安全模块 PUF 中，为整个 SoC 提供真随机数功能，保护根密钥和启动代码等关键数据不被攻击者破坏。小核侧 TRNG 驱动主要提供读功能，TRNG 驱动挂载在 HW random 框架上，具体的框架结构如下图所示：

![trng](images/trng_linux.png)

#### 1.2.9 ADC模块

K230集成一路ADC转换器，共6各通道，分辨率12bit，最高每秒1M次的单通道连续模数转换。

#### 1.2.10 PWM模块

K230集成了2路PWM，每一路有3各通道，即通道 0~2 属于PWM0，通道 3~5 属于PWM1（软件上表现为通道 0~5 ），每一路都可输出独立波形。

#### 1.2.11 FBTFT模块

K230适配了ST7735S驱动芯片的屏幕，默认处于关闭状态，如果需要可按照 [FBTFT 配置参考](#211-fbtft 配置参考) 章节使能该配置。

## 2 使用方法参考

### 2.1 UART 使用参考

Linux封装了termios API用来给用户使用，termios API描述了一个通用的终端接口，提供了控制异步通讯端口的配置和读写。

```text
termios API举例：
int tcgetattr(int fd,struct termios *termios_p);
int tcsetattr(int fd,int potional_actions,struct termios *termios_p);
int tcsendbreak(int fd,int duration);
int tcdrain(int fd);
int tcflush(int fd, int queue_selector);
int tcflow(int fd, int action);
void cfmakeraw(struct termios *termios_p);
speed_t cfgetispeed(const struct termios *termios_p);
speed_t cfgetospeed(const struct termios *termios_p);
int cfsetispeed(struct termios *termios_p, speed_t speed);
int cfsetospeed(struct termios *termios_p, speed_t speed);
int cfsetspeed(struct termios *termios_p, speed_t speed);
```

详细请参考`Documentation/driver-api/serial/tty.rst`。

### 2.2 I2C 使用参考

linux为用户称封装了系统调用来使用i2c。

`open`，`read`，`write`等。可参考`buildroot`中`i2c-tools`相关源码。

### 2.3 GPIO 使用参考

#### 2.3.1 sysfs操作gpio

GPIO驱动加载后会在 `/sys/class/gpio/` 下创建gpio端口的设备节点，每个节点代表一个gpio端口，通过sysfs操作这个gpio端口即可达到操作gpio输入输出和中断的作用。

方法1：

```text
echo N > /sys/class/gpio/export        //将编号为 N 的gpio端口导出到sysfs

echo in > /sys/class/gpio/gpioN/direction    //将该gpio端口设置成输入模式

cat /sys/class/gpio/gpioN/value      //读取该gpio端口电平状态

echo out > /sys/class/gpio/gpioN/direction    //将该gpio端口设置成输出模式

echo 1 > /sys/class/gpio/gpioN/value     //将该端口输出高电平，注意active_low极性

echo 0 > /sys/class/gpio/gpioN/value     //将该端口输出低电平，注意active_low极性

设置中断属性：
echo rising > /sys/class/gpio/gpioN/edge    上升沿中断，中断只能在direction为in时才可以设置

echo falling > /sys/class/gpio/gpioN/edge   下降沿中断

echo both > /sys/class/gpio/gpioN/edge      双边沿中断
```

方法2：

```text
设置好中断模式后通过poll函数监听中断:

struct pollfd fds[1];
fd = open("/sys/class/gpio/gpioN/value", O_RDONLY)

fds[0].fd = gpio_fd;
fds[0].events = POLLPRI;

while(1)
{
    poll(fds, 1, -1);

    if (fds[0].revents & POLLPRI)
    {
        /* 接收中断 */
    }
}

```

#### 2.3.2 ioctl操作gpio

用户程序直接操作 `/dev/gpiochipN`：

```text
struct gpiohandle_request req;
struct gpiohandle_data data;
struct gpioevent_request event_req;
struct gpioevent_data event_data;
struct pollfd poll_fd;
fd = open("/dev/gpiochipN", O_RDONLY);

.....

req.lineoffsets[0] = 0;
req.flags = GPIOHANDLE_REQUEST_OUTPUT;
req.lines = 1;

event_req.lineoffset = 0;
event_req.handleflags = GPIOHANDLE_REQUEST_INPUT;
event_req.eventflags = GPIOEVENT_REQUEST_RISING_EDGE;

ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, &req);
ioctl(fd, GPIO_GET_LINEEVENT_IOCTL, &event_req);

close(fd);

poll_fd.fd = event_req.fd;
poll_fd.events = POLLIN;

while(1)
{
    data.values[0] = !data.values[0];
    .....
    ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);
    .....

     ret = poll(&poll_fd, 1, 3000);
     if(ret == 0)
     ....
     else {
        read(event_req.fd, &event_data, sizeof(event_data));
     }
}

close(req.fd);

```

### 2.4 Hardlock 使用参考

Hardlock未提供用户api接口，其使用方法仅限内核态驱动之间使用。

### 2.5 Watchdog 使用参考

#### 2.5.1 通过ioctl使用watchdog

```text
示例：
fd = open("/dev/watchdog", O_WRONLY)

.....

ioctl(fd, WDIOC_SETTIMEOUT, &flags); /* 设置超时 */

ioctl(fd, WDIOC_GETTIMEOUT, &flags); /* 获取超时设置 */

ioctl(fd, WDIOC_SETPRETIMEOUT, &flags); /* 设置预超时 */

ioctl(fd, WDIOC_GETPRETIMEOUT, &flags); /* 获取预超时 */

ioctl(fd, WDIOC_GETTIMELEFT, &flags); /* 获取剩余超时时间 */

ioctl(fd, WDIOC_KEEPALIVE, &dummy); /* 喂狗 */

.....
```

#### 2.5.2 通过文件系统使用watchdog

```text
echo V > /dev/watchdog     watchdog开始计时，内核自动喂狗线程启动

echo A > /dev/watchdog     内核喂狗线程停止喂狗，但计时仍然继续，在默认超时时间后系统复位
```

> 注意：在命令行向watchdog节点写字符时，watchdog被使能并使用默认超时时间计数，且内核自动喂狗线程被唤醒

### 2.6 OTP 使用参考

用户可通过 `sysfs` 来访问 OTP 硬件，还可以通过运行用户态程序读取 OTP 空间。

SDK V1.3版本之前的otp空间与V1.3版本以及之后版本，otp空间有调整。

由于otp是一次性可编程的，且与芯片bootrom启动有关联，所以未提供写操作。如果产品量产需要向otp写入数据，或读写保护功能等等，请联系我们，我们会提供相关的接口驱动程序。

#### 2.6.1 sysfs 文件系统

Linux 内核使用 `sysfs` 文件系统，它的作用是将设备和驱动程序的信息导出到用户空间，方便了用户读取设备信息，同时支持修改和调整。`Sysfs` 虚拟文件系统一般被挂载在 `/sys` 目录下。OTP 一旦被注册到 Linux 中的 `NVMEM` 框架中之后，通过 `sysfs` 虚拟文件系统，可以很容易查看到 OTP 的信息。

OTP sysfs位于 `/sys/bus/nvmem/devices/kendryte_otp0/` 目录下，文件结构如下：

```shell
.
|-- nvmem
|-- of_node -> ../../../../../../firmware/devicetree/base/soc/security/otp@91213500
|-- subsystem -> ../../../../../../bus/nvmem
|-- type
|-- uevent

```

启动 Linux 之后，运行下列命令：

```shell
[root@canaan ~ ]#hexdump -C -v /sys/bus/nvmem/devices/kendryte_otp0/nvmem
00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
00000020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
......

```

#### 2.6.2 用户态访问 OTP

编写一个用户态应用程序，用户态应用程序通过标准的系统调用open()、close()、read()等函数陷入到内核态，最终会调用 OTP 驱动中注册的接口中，以测试 OTP 功能。

目前用户态应用程序已经编写完成，生成的可执行文件在 `/usr/bin/otp_test_demo` 目录下。

运行步骤如下：

1. 进入应用程序 demo 目录；
1. 在 demo 目录下运行 otp demo，读取长度作为参数；
1. 执行 otp demo。
1. 改变读取长度（长度范围：1~768），重新执行 otp demo。

启动小核Linux之后，运行下列命令：

```shell
[root@canaan / ]#otp_test_demo  192

Addr            Value
00000000        0x00000000
00000004        0x00000000
......
000002f8        0x00000000
000002fc        0x00000000
......

```

#### 2.6.3 获取芯片唯一标识

K230的PUF模块提供了芯片唯一标识，32bytes。linux用户态获取方式：

```shell
devmem 0x91213300 32
devmem 0x91213304 32
devmem 0x91213308 32
devmem 0x9121330c 32
devmem 0x91213310 32
devmem 0x91213314 32
devmem 0x91213318 32
devmem 0x9121331c 32
```

### 2.7 TS 使用参考

用户可通过 `sysfs` 来访问 TS 硬件，还可以通过运行用户态程序读取芯片结温。

#### 2.7.1 sysfs 文件系统

Linux 内核使用 `sysfs` 文件系统，它的作用是将设备和驱动程序的信息导出到用户空间，方便了用户读取设备信息，同时支持修改和调整。`sysfs` 虚拟文件系统一般被挂载在 `/sys` 目录下。TS 一旦被注册到 Linux 中的 Thermal 框架中之后，通过 `sysfs` 虚拟文件系统，可以很容易查看到 TS 的信息。

TS sysfs位于 `/sys/class/thermal/thermal_zone0/` 目录下，文件结构如下：

```shell
.
|-- available_policies
|-- integral_cutoff
|-- k_d
|-- k_i
|-- k_po
|-- k_pu
|-- mode
|-- offset
|-- passive
|-- policy
|-- slope
|-- subsystem -> ../../../../class/thermal
|-- sustainable_power
|-- temp
|-- type
|-- uevent

```

启动 Linux 之后，运行下列命令：

```shell
[root@canaan ~ ]#cat /sys/class/thermal/thermal_zone0/temp
7182
......

```

`7182` 这个值表示的含义为：读取 tsensor 寄存器的值，并没有做任何数学运算。相应的数学表达式如下:

```text

code = ts_val & 0xfff;
temp = (1e-10 * pow(code, 4) * 1.01472 - 1e-6 * pow(code, 3) * 1.10063 + 4.36150 * 1e-3 * pow(code, 2) - 7.10128 * code + 3565.87);

```

- ts_val：实际读取 TS 寄存器的值；
- code：TS 寄存器的值保留低12位得到的结果；
- temp：计算得到的温度值。

#### 2.7.2 用户态访问 TS

编写一个用户态应用程序，用户态应用程序通过标准的系统调用open()、close()、read()等函数陷入到内核态，最终会调用 TS 驱动中注册的接口中，以测试 TS 功能。

目前用户态应用程序已经编写完成，生成的可执行文件在 `/usr/bin/ts_test_demo` 目录下。

运行步骤如下：

1. 进入应用程序 demo 目录；
1. 在 demo 目录下运行 ts demo，循环次数作为参数；
1. 执行 ts demo。
1. 改变循环次数，重新执行 ts demo。

启动小核Linux之后，运行下列命令：

```shell
[root@canaan ~ ]#cd /usr/bin/
[root@canaan /usr/bin ]#./ts_test_demo 5
ts_val: 0x1c08, TS = 42.176993 C
ts_val: 0x1c07, TS = 41.875168 C
ts_val: 0x1c06, TS = 41.573277 C
ts_val: 0x1c07, TS = 41.875168 C
ts_val: 0x1c0a, TS = 42.780447 C
[root@canaan ~ ]#

```

### 2.8 TRNG 使用参考

用户可通过 `sysfs` 来访问 TRNG 硬件，还可以通过运行用户态程序读取真随机数。

#### 2.8.1 sysfs 文件系统

Linux 内核使用 `sysfs` 文件系统，它的作用是将设备和驱动程序的信息导出到用户空间，方便了用户读取设备信息，同时支持修改和调整。`sysfs` 虚拟文件系统一般被挂载在 `/sys` 目录下。TRNG 一旦被注册到 Linux 中的 HW random 框架中之后，通过 `sysfs` 虚拟文件系统，可以很容易查看到 TRNG 的信息。

TRNG sysfs位于 `/sys/class/misc/hw_random/` 目录下，文件结构如下：

```shell
.
|-- dev
|-- rng_available
|-- rng_current
|-- rng_selected
|-- subsystem -> ../../../../class/misc
|-- uevent

```

启动 Linux 之后，运行下列命令：

```shell
[root@canaan ~ ]# cat /sys/class/misc/hw_random/rng_current
91213000.trng
[root@canaan ~ ]# cat /sys/class/misc/hw_random/rng_available
91213000.trng

```

#### 2.8.2 用户态访问 TRNG

编写一个用户态应用程序，用户态应用程序通过标准的系统调用open()、close()、read()等函数陷入到内核态，最终会调用 TRNG 驱动中注册的接口中，查看每次读取得到的数据是否不一致，从而测试 TRNG 的功能。

目前用户态应用程序已经编写完成，生成的可执行文件在 */usr/bin/trng_test_demo* 目录下。

运行步骤如下：

1. 进入应用程序 demo 目录；
1. 在 demo 目录下运行 trng demo；
1. 执行 trng demo。
1. 重复执行 trng demo，查看每次读取的随机数是否一致。

启动小核Linux之后，运行下列命令：

```text
[root@canaan ~ ]#cd /usr/bin/
[root@canaan /usr/bin ]#./trng_test_demo
2C 10 B3 29 C3 98 10 41 3C 2A 90 75 EB C4 61 A5
[root@canaan /usr/bin ]#./trng_test_demo
6E AB 46 DD C1 7D FC 97 65 02 0C 58 1E A1 80 B9
[root@canaan ~ ]#

```

默认每次打印16个字节的随机数，每次打印的随机数不同。

### 2.9 ADC 使用参考

用户可通过 `sysfs` 来访问 ADC 各通道，还可以通过运行用户态程序读取各通道电压转换数据。

#### 2.9.1 sysfs访问 ADC

Linux下ADC是挂载在IIO子系统下的，通过`sysfs`访问可以参考如下示例；

```shell
1、cd /sys/devices/platform/soc/9140d000.adc/iio:device0
2、cat in_voltage0_raw   读取通道0
3、cat in_voltage1_raw   读取通道1
4、cat in_voltage2_raw   读取通道2
5、cat in_voltage3_raw   读取通道3
6、cat in_voltage4_raw   读取通道4
7、cat in_voltage5_raw   读取通道5
```

注意：在嘉楠 K230_EVB 开发板上，ADC通道5另一端已经接在音频输出接口上，所以不建议将此通道用作他用。

#### 2.9.2 用户态访问 ADC

略。

### 2.10 PWM 使用参考

用户可通过 `sysfs` 来访问 PWM 各通道，还可以通过运行用户态程序控制各通道输出波形周期及占空比。

#### 2.10.1 sysfs访问 PWM

```shell
1、cd /sys/devices/platform/soc/9140a000.pwm/pwm/pwmchip0
2、echo 4 > export          导出通道4 即PWM4；
3、cd pwm4/                 出现pwm4的目录，进入；
4、echo 100000 > period     设置周期 100us，
5、echo 50000 > duty_cycle  设置正占空比周期 50us，
6、echo 1 >enable           当前通道使能；

```

#### 2.10.2 用户态访问 PWM

略。

### 2.11 FBTFT 配置参考

K230 SDK支持小屏驱动，并适配了ST7735S驱动芯片(spi)，默认状态下该项配置处于关闭状态，如需打开请参考以下操作：

在SDK下执行：

```text
make linux-menuconfig

使能ST7735S驱动：
Device Drivers  --->
        [*] Staging drivers  --->
                [*] Support for small TFT LCD display modules  --->
                        <*>   FB driver for the ST7735S LCD Controller

使能ST7735S设备树节点：
spi-lcd@0 {
        ..................
        status = "okay";
        ..................
};

使能SPI驱动：
Device Drivers  --->
        [*] SPI support  --->
                <*>   DesignWare SPI controller core support
                <*>     Memory-mapped io interface driver for K230 DW SPI core

使能SPI设备节点：
spi1: spi@91582000 {
        compatible = "snps,dwc-ssi-1.01a-k230";(仅st7735s需要修改compatible)
        ..................
};

```

如需fb测试程序，请执行以下命令：

```text
make buildroot-menuconfig

Target packages  --->
        Graphic libraries and applications (graphic/text)  --->
                [*] fb-test-app
```

修改 uboot 下 `src/little/uboot/arch/riscv/dts/k230_evb.dts` 中关于spi的管脚配置即可使用。

fb测试程序使用：
编译完成后fb测试程序在 `usr/bin` 目录，分别是 `fb-test fb-string fb-test-perf fb-test-rect` 等。
使用举例：

```c
./fb-test -f 0 -p 5      显示一张图，详细使用请 ./fb-test -help
./fb-string x y hello 0xffffff 0x0      其中 x y 为字符显示坐标(左上角)，hello 为要显示的字符串，0xffffff 为字体颜色，0x0 为背景色。
```

注意：`st7735s` 设备默认在`spi1`设备节点下，驱动加载成功后将在`/dev`目录下出现`fb1`节点，如果将`src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi` 的 `dsi` 节点关闭，则 `/dev/fb0` 为`st7735s`设备。`fb-test-app`默认操作`fb0`。

`fb-test-app`的编译脚本需要修改：`src/little/buildroot-ext/buildroot-9d1d4818c39d97ad7a1cdf6e075b9acae6dfff71/package/fb-test-app/fb-test-app.mk`中增加:

```shell
define FB_TEST_APP_INSTALL_TARGET_CMDS

$(INSTALL) -D -m 0755 $(@D)/fb-string $(TARGET_DIR)/usr/bin/fb-string

endef

```
