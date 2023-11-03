# K230 little core Linux driver API reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the driver APIs of K230 small-core Linux, mainly including uart, i2c, gpio, watchdog, hardlock, OTP, Tsensor, TRNG, etc.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| Abbreviation      |            Illustrate               |
|-----------|---------------------------------------------|
| UART      | Universal Asynchronous Receiver/Transmitter |
| I2C       | Inter-Integrated Circuit                    |
| GPIO      | General-purpose input/output                |
| Hard-lock | Hardware mutexes                            |
| WDT       | watchdog                                    |
| OTP       | One-Time Programmable                       |
| TS        | Temperature Sensor                          |
| TRNG      | True Random Number Generator                |
| ADC       | analog-to_digital converter                 |
| PWM       | Pulse Width Modulation                      |
| FBTFT     | small TFT LCD display                       |

### Revision history

| Document version | Modify the description | Author | Date |
|------------------|------------------------|--------|------|
| V1.0 |        Initial         | Juntao Fan | 2023/5/26 |
| V1.1 |   Add ADC, PWM parts   | Juntao Fan | 2023/8/4 |
| V1.2 | Added ST7735S configuration section | Juntao Fan | 2023/9/5 |

## 1 Overview

### 1.1 Overview

UART：
A universal asynchronous transceiver that communicates bidirectionally and enables full-duplex transmission and reception. In embedded designs, UART is used to communicate with PCs, including supervisory debuggers and other devices such as EEPROMs.

I2C：
Developed by Philips (migrated to NXP in 2006), a simple, two-wire, bidirectional synchronous serial bus in the early 1980s, it uses a clock line and a data line to transfer information between two devices connected to the bus, providing a simple and efficient method for data exchange between devices. Each device connected to the bus has a unique address, and any device can act as both a master and a slave, but only one master is allowed at a time.

GPIO：
(General Porpose Intput Output) Short for General Purpose Input and Output Port. Its output and input can be controlled through software, which is commonly used pins, and the high and low levels of the pin can be controlled to read or write it.

Hard-lock：
Canaan self-developed module, it is used for the mutual exclusion of shared resources between processes with the same core or between different cores, and can be used for the mutual exclusion of shared resources.

WDT：
WDT is the abbreviation of watchdog, which is essentially a hardware timer, the software program needs to feed the dog every once in a while, if the WDT timeout, it can generate an interrupt signal or reset signal to the CPU, thereby preventing the program from running abnormally and cannot be recovered through the combination of software and hardware.

OTP：
OTP is mainly used to store security-sensitive confidential information, such as bootrom firmware information, encryption and decryption keys, signature information, and user-defined security information.

TS：
K230 TS (Temperature Sensor), self-developed temperature sensor, using TSMC 12nm process, TS application scenario is frequency down.

TRNG：
TRNG is mainly used to generate true random numbers, thereby providing a random source of entropy for encryption and decryption operations.

ADC：
ADC, or analog-to-digital converter, refers to a device that converts a continuously changing analog signal into a discrete digital signal.

PWM：
PWM pulse-width modulation is a method of digitally encoding the level of an analog signal by modulating the proportion of positive pulse periods to encode the level of a specific analog signal.

FBTFT：
FBTFT small screen driver, support framebuffer, kernel is now rarely maintained, driver code under `driver/staging/fbtft` .

### 1.2 Function Description

#### 1.2.1 UART module

K230 has a total of 5 UARTs, and the UART module supports infrared mode, supports RS485 mode, supports DMA, some ports support flow control, data bits support 5/6/7/8 bits, stop bit 1/2 bit, baud rate can support up to 1.5MHz.

#### 1.2.2 I2C module

K230 has a total of 5 channels I2C, I2C module supports main mode, supports DMA, supports 7/10 bit addressing, supports interrupt, I2C module transmission rate supports 100K/400K/1M/3.4M.

#### 1.2.3 GPIO module

K230 has a total of 2 GPIOs, each GPIO contains 32 GPIO ports, a total of 64 GPIO ports, each GPIO port supports input and output functions, support rising edge interrupt, falling edge interrupt, high and low level interrupt, and bilateral edge interrupt. The interrupts of each GPIO port of the K230 are independent of each other.

#### 1.2.4 Hard-lock module

The k230 has 128 hardware mutexes, which act like Linux spinlocks and can be used to mutually exclusive the same resource.

#### 1.2.5 WDT module

WDT, watchdog module, K230 has two WDT, the size of the core uses one way, WDT supports interrupt and reset two modes, default use reset mode, that is, when the WDT timeout overflows, directly reset the SOC.

#### 1.2.6 OTP module

The OTP is integrated into the security module PUF, providing secure storage capabilities for the entire SoC, protecting critical data such as the root key and boot code from being compromised by attackers. The small-core side OTP driver mainly provides the read function, and the readable area is 24Kbits including production information. The Linux OTP driver is mounted on the nvmem framework, and the specific framework structure is shown in the following figure:

![OTP](../../../../zh/01_software/board/osdrv/images/otp_linux.png)

#### 1.2.7 TS module

The big core-side TS driver mainly provides the read function, and before reading the TS, it is necessary to configure the TS register enable signal, output mode, and then read the junction temperature of the chip. In addition, the TS register reads the die junction temperature every 2.6s. The structure of the TS driver on the RT-smart side is shown in the following figure:

![ts](../../../../zh/01_software/board/osdrv/images/ts_linux.png)

#### 1.2.8 TRNG module

Integrated in the security module PUF, TRNG provides true random number functionality to the entire SoC, protecting critical data such as root key and boot code from attackers. The little core side TRNG driver mainly provides read function, and the TRNG driver is mounted on the HW random framework, and the specific framework structure is shown in the following figure:

![trng](../../../../zh/01_software/board/osdrv/images/trng_linux.png)

#### 1.2.9 ADC Module

The K230 integrates an ADC converter with a total of 6 channels with a resolution of 12 bits, and a maximum of 1M consecutive analog-to-digital conversions per second.

#### 1.2.10 PWM module

K230 integrates 2 PWMs, each channel has 3 channels, that is, channel 0~2 belongs to PWM0, channel 3~5 belongs to PWM1 (software manifested as channel 0~5), each channel can output independent waveform.

#### 1.2.11 FBTFT module

The K230 is adapted to the screen of the ST7735S driver chip, which is turned off by default, and can be enabled if needed according to the [FBTFT configuration reference]section (#211-fbtft configuration reference).

## 2 Usage reference

### 2.1 UART Usage Reference

Linux encapsulates the termios API for user use, and the termios API describes a common terminal interface that provides configuration and read/write to control asynchronous communication ports.

```text
termios API example：
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

Please refer to it for details`Documentation/driver-api/serial/tty.rst`.

### 2.2 I2C Usage Reference

Linux encapsulates system calls for users to use I2C.

`open`,`read`,`write`, etc. Please refer to`buildroot` the `i2c-tools`relevant source code in .

### 2.3 GPIO Usage Reference

#### 2.3.1 sysfs operates GPIO

After the GPIO driver is loaded, a GPIO port device node will be `/sys/class/gpio/` created under , each node represents a GPIO port, and the GPIO port can be operated through sysfs to achieve the role of operating GPIO input, output and interrupt.

Method 1:

```text
echo N > /sys/class/gpio/export        //Export the number N of gpio to sysfs

echo in > /sys/class/gpio/gpioN/direction    //Set the gpio port to output mode

cat /sys/class/gpio/gpioN/value      //Get the voltage status of gpio port (0 or 1)

echo out > /sys/class/gpio/gpioN/direction    //Set the gpio port to output mode

echo 1 > /sys/class/gpio/gpioN/value     //Port output high level

echo 0 > /sys/class/gpio/gpioN/value     //Port output low level

gpio interrupte:
echo rising > /sys/class/gpio/gpioN/edge    //Rising edge, interrupts can only be set if the direction is in

echo falling > /sys/class/gpio/gpioN/edge   //Falling edge

echo both > /sys/class/gpio/gpioN/edge      //Double edge
```

Method 2:

```text
After the interrupt mode is configured, use the poll function to listen for interrupt events;

struct pollfd fds[1];
fd = open("/sys/class/gpio/gpioN/value", O_RDONLY)

fds[0].fd = gpio_fd;
fds[0].events = POLLPRI;

while(1)
{
    poll(fds, 1, -1);

    if (fds[0].revents & POLLPRI)
    {
        /* Receive interrupt event */
    }
}

```

#### 2.3.2 Using gpio via ioctl

User program direct manipulation `/dev/gpiochipN`:

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

### 2.4 Hardlock usage reference

Hardlock does not provide a user API interface, and its use is limited to kernel-state drivers.

### 2.5 Watchdog usage reference

#### 2.5.1 Using Watchdog via IOCTL

```text
Examples:
fd = open("/dev/watchdog", O_WRONLY)

.....

ioctl(fd, WDIOC_SETTIMEOUT, &flags); /* Set timeout */

ioctl(fd, WDIOC_GETTIMEOUT, &flags); /* Get timeout */

ioctl(fd, WDIOC_SETPRETIMEOUT, &flags); /* Set the pre-timeout time */

ioctl(fd, WDIOC_GETPRETIMEOUT, &flags); /* Gets the pre-timeout time */

ioctl(fd, WDIOC_GETTIMELEFT, &flags); /* Gets the remaining timeout period */

ioctl(fd, WDIOC_KEEPALIVE, &dummy); /* Feed dog */

.....
```

#### 2.5.2 Using watchdog via file system

```text
echo V > /dev/watchdog     //Start watchdog timer,start the kernel automatic dog feed thread

echo A > /dev/watchdog     //Stop the kernel automatic dog feed thread，but the watchdog timer running,the system resets after the default timeout period
```

> Note: When writing characters to the watchdog node on the command line, watchdog is enabled and counts with the default timeout, and the kernel autofeed dog thread is woken up

### 2.6 OTP Usage Reference

Users can  access OTP hardware through and read `sysfs` OTP space by running user-mode programs.

#### 2.6.1 Sysfs file system

The Linux kernel uses `sysfs` a file system, which exports device and driver information to user space, making it easier for users to read device information, while supporting modification and adjustment. `Sysfs` Virtual file systems are typically mounted in `/sys` the  directory. Once the OTP is registered with `NVMEM` the  Linux framework,  the `sysfs` OTP information can be easily viewed through the virtual file system.

OTP sysfs is located in `/sys/bus/nvmem/devices/kendryte_otp0/` the directory and the file structure is as follows:

```shell
.
|-- nvmem
|-- of_node -> ../../../../../../firmware/devicetree/base/soc/security/otp@91214000
|-- subsystem -> ../../../../../../bus/nvmem
|-- type
|-- uevent

```

After starting Linux, run the following command:

```shell
[root@canaan ~ ]# hexdump -C -v /sys/bus/nvmem/devices/kendryte_otp0/nvmem
00000000  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000020  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000030  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000040  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000050  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000060  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000070  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000080  00 02 00 00 50 02 00 00  00 01 00 00 00 00 00 00  |....P...........|
00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
000000a0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
......

```

Alternatively, utilize `dd` the command:

```shell
[root@canaan ~ ]# dd if=/sys/bus/nvmem/devices/kendryte_otp0/nvmem of=/tmp/file
6+0 records in
6+0 records out
[root@canaan ~ ]# hexdump -C -v /tmp/file
00000000  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000010  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000020  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000030  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000040  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000050  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000060  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000070  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
00000080  00 02 00 00 50 02 00 00  00 01 00 00 00 00 00 00  |....P...........|
00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
......

```

#### 2.6.2 User-mode access to OTP

Write a user-mode application that falls into kernel mode by calling functions such as open(), close(), read(), etc. by standard system calls, and eventually calls the interface registered in the OTP driver to test OTP functionality.

The user-mode application has been written, and the generated executable is in `/usr/bin/otp_test_demo` the  directory.

The steps to run are as follows:

1. Go to the application demo directory;
1. Run the otp demo in the demo directory and read the length as a parameter;
1. Execute the OTP demo.
1. Change the read length (length range: 1~768) and re-execute the OTP demo.

After starting the little core Linux, run the following command:

```shell
[root@canaan ~ ]#cd /usr/bin/
[root@canaan /usr/bin ]# ./otp_test_demo 768
Addr                    Value
00000000                0xffffffff
00000004                0xffffffff
00000008                0xffffffff
0000000c                0xffffffff
00000010                0xffffffff
00000014                0xffffffff
00000018                0xffffffff
0000001c                0xffffffff
00000020                0xffffffff
00000024                0xffffffff
00000028                0xffffffff
0000002c                0xffffffff
00000030                0xffffffff
00000034                0xffffffff
00000038                0xffffffff
0000003c                0xffffffff
00000040                0xffffffff
......

```

#### 2.6.3 OTP space defaults

The OTP space default value information is shown below, please verify whether the OTP space is read correctly against the default value.

```text
00000000  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
*
00000080  00 02 00 00 50 02 00 00  00 01 00 00 00 00 00 00  |....P...........|
00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000100  8d 3d da 24 1c f6 fa f6  88 4b c3 91 fb 2d 7b 09  |.=.$.....K...-{.|
00000110  a6 64 03 7d ce 98 e0 d2  92 5a a0 cf 3c 58 50 d0  |.d.}.....Z..<XP.|
00000120  3b 77 37 e6 0d 36 eb 9a  21 42 a1 2a 53 d8 aa 87  |;w7..6..!B.*S...|
00000130  ab 53 5c e7 ab 3e 7a c6  f4 29 16 71 45 f1 30 0d  |.S\..>z..).qE.0.|
00000140  91 3f a6 3d 48 30 dd 6d  18 c2 1c 13 97 fe 1f 9b  |.?.=H0.m........|
00000150  fd 08 1c 16 1b a7 9a 20  1d 80 70 8a 20 08 61 a3  |....... ..p. .a.|
00000160  24 2b cf ec 97 9e 3f 25  89 b9 f2 a8 7a 63 5c c7  |$+....?%....zc\.|
00000170  44 86 70 30 45 e4 4f 35  4d 2e 3e 8c e5 3a 49 29  |D.p0E.O5M.>..:I)|
00000180  b6 06 6e 15 6b 62 d3 94  5f 8a ea e3 ea a3 a1 fc  |..n.kb.._.......|
00000190  0f 19 f5 50 05 4d 63 47  77 14 c1 c0 bf 06 3b 55  |...P.McGw.....;U|
000001a0  47 be 7c c6 93 e2 e1 31  05 27 f5 a2 77 16 1f 75  |G.|....1.'..w..u|
000001b0  5a 95 0a 15 24 16 a8 1a  fc d8 67 f4 dd 15 e4 8c  |Z...$.....g.....|
000001c0  25 44 b9 48 59 b1 17 bb  8e 05 15 db ff fa 77 47  |%D.HY.........wG|
000001d0  52 ce f7 86 bf 20 b5 46  ac 83 e9 ac 08 a7 e3 67  |R.... .F.......g|
000001e0  02 24 50 de 49 9d 24 57  9f 78 bb 74 21 8f 74 f0  |.$P.I.$W.x.t!.t.|
000001f0  47 25 9b cb 99 e7 6a 0f  51 52 be 4b ea 6a a3 ee  |G%....j.QR.K.j..|
00000200  7b 8d f8 ad c8 c6 5e c4  13 66 4b 50 3b 02 98 c8  |{.....^..fKP;...|
00000210  20 11 c5 ca 54 ee 32 ea  89 e4 38 58 cd 5a cb 34  | ...T.2...8X.Z.4|
00000220  2f d2 d9 b3 d9 97 50 a8  10 74 73 17 b0 76 19 ec  |/.....P..ts..v..|
00000230  8e 1e 07 58 ba f5 5b b9  a3 6e 0b f8 ae 8c ba 35  |...X..[..n.....5|
00000240  53 6b 5d 52 9d e9 76 46  ae f7 1f 8d 45 b4 93 b6  |Sk]R..vF....E...|
00000250  28 93 b4 07 6f 8e be 37  41 57 86 19 c1 d0 fb 9b  |(...o..7AW......|
00000260  8e 09 7a 77 a4 23 83 db  39 64 6c 5f 73 0d 82 2e  |..zw.#..9dl_s...|
00000270  ca 5b 2e c4 5f b0 6b 23  3d fd 96 88 e8 b9 e9 02  |.[.._.k#=.......|
00000280  a8 e1 22 b1 c4 af 61 4c  bc ab 93 a1 d1 80 aa 6f  |.."...aL.......o|
00000290  01 dc cd c1 a0 71 36 58  86 ed 7e d9 c1 15 95 50  |.....q6X..~....P|
000002a0  f2 4e 9a 0e c9 d8 58 d6  14 93 c9 de 86 0e 87 52  |.N....X........R|
000002b0  85 e6 ff d6 28 e8 dd 29  5a ab b4 b3 ce de 35 e9  |....(..)Z.....5.|
000002c0  48 f2 1f a8 22 8f e3 17  d7 86 d8 e8 de 24 4d 2a  |H..."........$M*|
000002d0  70 89 37 47 9c 53 9b 33  0b 74 95 30 d6 4e e0 36  |p.7G.S.3.t.0.N.6|
000002e0  bc 10 ff da ab bd 74 e7  df 04 08 11 e7 43 94 09  |......t......C..|
000002f0  4d 74 df 13 84 a0 86 54  4c d0 cb c2 63 fb 42 7d  |Mt.....TL...c.B}|
00000300  5b e6 9d 3b dc 86 59 d7  cb df 29 65 53 51 54 8b  |[..;..Y...)eSQT.|
00000310  b1 50 96 a2 85 e0 b6 b4  d2 ce 6d 63 48 09 b3 62  |.P........mcH..b|
00000320  9d f5 d4 16 4c 81 5f b4  e1 f7 91 7b 5f 7f c9 29  |....L._....{_..)|
00000330  43 22 56 e8 f5 ae 68 b3  a0 a8 f9 7d 7b d9 b1 2e  |C"V...h....}{...|
00000340  98 25 07 7b 38 33 9c 99  f6 85 c7 49 cb dc 6f 1d  |.%.{83.....I..o.|
00000350  1c 45 d1 ff 57 a4 b9 d7  2a 6c 3f 9e dd 9a ee 5b  |.E..W...*l?....[|
00000360  f3 0b 21 af 2e d8 e5 ce  4f b7 4d 07 ea ba 5a e9  |..!.....O.M...Z.|
00000370  df 85 d8 6d 88 78 84 9a  dd 1a 4a 4a 86 2e e4 62  |...m.x....JJ...b|
00000380  c2 94 4c e7 77 0b 2c 7a  38 03 2c 2a a1 f7 5b dd  |..L.w.,z8.,*..[.|
00000390  14 a7 d8 4a 66 38 d0 9f  e8 28 a8 7c 33 36 39 72  |...Jf8...(.|369r|
000003a0  1b 7b 84 68 a6 a8 dd 7e  a9 5b f0 8e 2b 50 6e 40  |.{.h...~.[..+Pn@|
000003b0  d2 a5 62 43 5e f1 f4 bf  90 11 0f e2 16 b5 80 4e  |..bC^..........N|
000003c0  10 68 a7 a2 aa 2d dd ba  c1 d7 d6 0c b7 17 a5 a3  |.h...-..........|
000003d0  c2 e2 77 e8 7c 9a ff 23  8c 30 ae b3 5a 79 1c fd  |..w.|..#.0..Zy..|
000003e0  77 4a f6 41 78 53 36 52  d4 45 a6 f9 c2 8e 8d fc  |wJ.AxS6R.E......|
000003f0  03 2e f4 00 58 e8 15 85  bf d9 3f b8 62 58 e2 97  |....X.....?.bX..|
00000400  d2 ea 7f b2 a2 ef 40 f2  fc 68 07 64 51 f7 c9 6e  |......@..h.dQ..n|
00000410  68 eb 68 ec 15 a8 a7 7e  1d 86 8b 12 f1 33 a0 18  |h.h....~.....3..|
00000420  21 06 f4 0a 58 4b ec 17  7d 87 2c ec ea ce 3e ce  |!...XK..}.,...>.|
00000430  02 2f 02 a5 76 61 57 dd  85 6e f5 14 d4 6b fb f9  |./..vaW..n...k..|
00000440  64 d3 60 2c 1f 45 00 9c  50 d4 2a aa 1d f0 96 82  |d.`,.E..P.*.....|
00000450  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
*
00000bf0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|

```

### 2.7 TS Usage Reference

The  user `sysfs` can access the TS hardware through and can also read the die junction temperature by running a user-mode program.

#### 2.7.1 sysfs file system

The Linux kernel uses `sysfs` a file system, which exports device and driver information to user space, making it easier for users to read device information, while supporting modification and adjustment. `sysfs` Virtual file systems are typically mounted in `/sys` the  directory. Once TS is registered with the Thermal Framework in Linux,  TS `sysfs` information can be easily viewed through the virtual file system.

TS sysfs is located in `/sys/class/thermal/thermal_zone0/` the directory, and the file structure is as follows:

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

After starting Linux, run the following command:

```shell
[root@canaan ~ ]#cat /sys/class/thermal/thermal_zone0/temp
7182
......

```

`7182` This value means that the value of the tsensor register is read without doing any mathematical operations. The corresponding mathematical expression is as follows:

```text

code = ts_val & 0xfff;
temp = (1e-10 * pow(code, 4) * 1.01472 - 1e-6 * pow(code, 3) * 1.10063 + 4.36150 * 1e-3 * pow(code, 2) - 7.10128 * code + 3565.87);

```

- ts_val: The value of the TS register is actually read;
- code: The value of the TS register is kept in the lower 12 bits;
- temp: The calculated temperature value.

#### 2.7.2 User-mode access TS

Write a user-mode application that falls into kernel mode through standard system calls to functions such as open(), close(), read(), etc., and eventually calls the interface registered in the TS driver to test TS functionality.

The user-mode application has been written, and the generated executable is in `/usr/bin/ts_test_demo` the  directory.

The steps to run are as follows:

1. Go to the application demo directory;
1. Run ts demo in the demo directory, and the number of loops is used as a parameter;
1. Execute the ts demo.
1. Change the number of loops and re-execute the ts demo.

After starting the little core Linux, run the following command:

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

### 2.8 TRNG Usage Reference

The  user `sysfs` can access the TRNG hardware through and can read true random numbers by running a user-mode program.

#### 2.8.1 sysfs file system

The Linux kernel uses `sysfs` a file system, which exports device and driver information to user space, making it easier for users to read device information, while supporting modification and adjustment. `sysfs` Virtual file systems are typically mounted in  the `/sys` directory. Once TRNG is registered with the HW random framework in Linux, TRNG `sysfs` information can be easily viewed through the virtual file system.

TRNG sysfs is located in  the `/sys/class/misc/hw_random/` directory, and the file structure is as follows:

```shell
.
|-- dev
|-- rng_available
|-- rng_current
|-- rng_selected
|-- subsystem -> ../../../../class/misc
|-- uevent

```

After starting Linux, run the following command:

```shell
[root@canaan ~ ]# cat /sys/class/misc/hw_random/rng_current
91213000.trng
[root@canaan ~ ]# cat /sys/class/misc/hw_random/rng_available
91213000.trng

```

#### 2.8.2 User access to TRNG

Write a user-mode application, the user-mode application through the standard system call open(), close(), read() and other functions into the kernel state, and eventually call the interface registered in the TRNG driver to see if the data obtained each time is inconsistent, so as to test the functionality of TRNG.

The user-mode application is now written, and the resulting executable is in *the /usr/bin/trng_test_demo* directory.

The steps to run are as follows:

1. Go to the application demo directory;
1. Run trng demo in the demo directory;
1. Execute the trng demo.
1. Run the trng demo repeatedly to see if the random numbers read are consistent each time.

After starting the little core Linux, run the following command:

```text
[root@canaan ~ ]#cd /usr/bin/
[root@canaan /usr/bin ]#./trng_test_demo
2C 10 B3 29 C3 98 10 41 3C 2A 90 75 EB C4 61 A5
[root@canaan /usr/bin ]#./trng_test_demo
6E AB 46 DD C1 7D FC 97 65 02 0C 58 1E A1 80 B9
[root@canaan ~ ]#

```

By default, 16 bytes of random numbers are printed each time, and the random numbers are different each time.

### 2.9 ADC Usage Reference

The user can access  each channel `sysfs` of the ADC through and read the voltage conversion data for each channel by running a user-mode program.

#### 2.9.1 sysfs access ADC

The ADC under Linux is mounted under the IIO subsystem, and`sysfs` the following example can be referred to through access

```shell
1、cd /sys/devices/platform/soc/9140d000.adc/iio:device0
2、cat in_voltage0_raw   //read from chanel-0
3、cat in_voltage1_raw   //read from chanel-1
4、cat in_voltage2_raw   //read from chanel-2
5、cat in_voltage3_raw   //read from chanel-3
6、cat in_voltage4_raw   //read from chanel-4
7、cat in_voltage5_raw   //read from chanel-5
```

Note: On the Canaan K230_EVB board, ADC channel 5 is already connected to the audio output interface at the other end, so it is not recommended to use this channel for other purposes.

#### 2.9.2 User-mode access ADC

Outline.

### 2.10 PWM usage reference

The  user `sysfs` can access each PWM channel through and can also control the output waveform period and duty cycle of each channel by running a user-mode program.

#### 2.10.1 sysfs access PWM

```shell
1、cd /sys/devices/platform/soc/9140a000.pwm/pwm/pwmchip0
2、echo 4 > export          //Export the channel-4 (PWM4);
3、cd pwm4/                 //The pwm4 directory appears. Go to it.
4、echo 100000 > period     //Set period 100us，
5、echo 50000 > duty_cycle  //Set the positive duty cycle 50us，
6、echo 1 >enable           //Enable current channel

```

#### 2.10.2 User-mode access PWM

Outline.

### 2.11 FBTFT Configuration Reference

K230 SDK supports small screen drivers and adapts to ST7735S driver chip (spi), this configuration is turned off by default, if you need to open it, please refer to the following operations:

Execute under the SDK:

```text
make linux-menuconfig

Enable ST7735S driver:
Device Drivers  --->
        [*] Staging drivers  --->
                [*] Support for small TFT LCD display modules  --->
                        <*>   FB driver for the ST7735S LCD Controller

Enable ST7735S device tree node:
spi-lcd@0 {
        ..................
        status = "okay";
        ..................
};

Enable SPI driver:
Device Drivers  --->
        [*] SPI support  --->
                <*>   DesignWare SPI controller core support
                <*>     Memory-mapped io interface driver for K230 DW SPI core

Enanle SPI device tree node:
spi1: spi@91582000 {
        compatible = "snps,dwc-ssi-1.01a-k230"; //(just st7735s device node need)
        ..................
};

```

To use the FB test program, execute the following command:

```text
make buildroot-menuconfig

Target packages  --->
        Graphic libraries and applications (graphic/text)  --->
                [*] fb-test-app
```

Modify  the `src/little/uboot/arch/riscv/dts/k230_evb.dts` SPI pin configuration under uboot to use.

The FB test program uses:
After the compilation is completed, the fb test program is in the `usr/bin` directory, which is `fb-test fb-string fb-test-perf fb-test-rect` ,  etc.
Usage examples:

```c
./fb-test -f 0 -p 5      //display a picture, using "./fb-test -help" for help
./fb-string x y hello 0xffffff 0x0      //x y is the string display coordinates , 'hello' is the string, 0xffffff is font color, 0x0 back color.
```

Note: The device is under the device `st7735s` node by default, and the node will `spi1`appear under the directory `/dev`after the driver is successfully loaded`fb1`, and if the node`src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi` of  is `dsi` shut down, it `/dev/fb0` is the `st7735s`device. `fb-test-app`Default action`fb0`.

`fb-test-app`The compilation script needs to be modified:`src/little/buildroot-ext/buildroot-9d1d4818c39d97ad7a1cdf6e075b9acae6dfff71/package/fb-test-app/fb-test-app.mk` added:

```shell
define FB_TEST_APP_INSTALL_TARGET_CMDS

$(INSTALL) -D -m 0755 $(@D)/fb-string $(TARGET_DIR)/usr/bin/fb-string

endef

```
