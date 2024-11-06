# K230 4G Module Linux Porting Reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not fall within your purchase or usage scope. Unless otherwise agreed in the contract, the Company makes no express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representation, information, or content in this document. Unless otherwise agreed, this document is intended solely as a usage guide reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the Company's written permission, no unit or individual is allowed to excerpt, copy any part or all of the content of this document, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly describes how the K230 SDK adapts to the EC200A 4G module. Other 4G modules are similar.

### Target Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Revision History

| Document Version | Description of Changes | Author | Date |
| --- | --- | --- | --- |
| V1.0 | Initial version | Wang Jianxin | 2024/05/08 |

## 1. Introduction to the EC200A 4G Module

The EC200A series is an LTE Cat 4 wireless communication module designed by Quectel for the M2M and IoT fields, supporting USB-to-serial PPP, RNDIS, and ECM networking modes. The EC200A has 5 USB interfaces; interfaces 2-4 need to adapt to the USB serial driver and use PPP dial-up internet through the ttyUSB2 node; interfaces 0-1 need to adapt to the ECM/RNDIS driver.

### 1.1 Hardware Information Seen in `dmesg`

The `dmesg` output shows information like the following (if not seen, please check the hardware), indicating idVendor=2c7c, idProduct=6005,

```bash
[    3.164090] usb 1-1: config 1 has an invalid interface number: 6 but max is 5
[    3.171285] usb 1-1: config 1 has no interface number 5
[    3.176872] usb 1-1: New USB device found, idVendor=2c7c, idProduct=6005, bcdDevice= 3.18
[    3.185112] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[    3.192272] usb 1-1: Product: Android
[    3.195947] usb 1-1: Manufacturer: Android
[    3.200055] usb 1-1: SerialNumber: 0000
[    3.206045] cdc_ether 1-1:1.0 usb0: register 'cdc_ether' at usb-91500000.usb-otg-1, CDC Ethernet Device, 02:0c:29:a3:9b:6d
[    3.217948] option 1-1:1.2: GSM modem (1-port) converter detected
[    3.224776] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB0
[    3.232473] option 1-1:1.3: GSM modem (1-port) converter detected
[    3.239214] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB1
[    3.246848] option 1-1:1.4: GSM modem (1-port) converter detected
[    3.253653] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB2
[    3.261388] option 1-1:1.6: GSM modem (1-port) converter detected
```

### 1.2 `lsusb`

The `lsusb` command output shows information like the following:

```bash
[root@canaan ~ ]#lsusb
Bus 002 Device 002: ID 0bda:8152
Bus 001 Device 001: ID 1d6b:0002
Bus 001 Device 002: ID 2c7c:6005
Bus 002 Device 001: ID 1d6b:0002
[root@canaan ~ ]#
```

### 1.3 Viewing EC200A Information in `/usb/devices`

```bash
[root@canaan ~ ]#mount -t debugfs none /sys/kernel/debug/
[root@canaan ~ ]#cat /sys/kernel/debug/usb/devices

T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  2 Spd=480  MxCh= 0
D:  Ver= 2.00 Cls=ef(misc ) Sub=02 Prot=01 MxPS=64 #Cfgs=  1
P:  Vendor=2c7c ProdID=6005 Rev= 3.18
S:  Manufacturer=Android
S:  Product=Android
S:  SerialNumber=0000
C:* #Ifs= 6 Cfg#= 1 Atr=e0 MxPwr=500mA
A:  FirstIf#= 0 IfCount= 2 Cls=02(comm.) Sub=06 Prot=00
I:* If#= 0 Alt= 0 #EPs= 1 Cls=02(comm.) Sub=06 Prot=00 Driver=cdc_ether
E:  Ad=87(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:  If#= 1 Alt= 0 #EPs= 0 Cls=0a(data ) Sub=00 Prot=00 Driver=cdc_ether
I:* If#= 1 Alt= 1 #EPs= 2 Cls=0a(data ) Sub=00 Prot=00 Driver=cdc_ether
E:  Ad=83(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0c(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
I:* If#= 2 Alt= 0 #EPs= 2 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=82(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0b(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
I:* If#= 3 Alt= 0 #EPs= 3 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=86(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0f(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=89(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:* If#= 4 Alt= 0 #EPs= 3 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=81(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0a(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=88(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:* If#= 6 Alt= 0 #EPs= 2 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=85(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0e(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
```

## 2

## Kernel Mode Driver Modification

### 2.1 USB Serial Driver Modification (Mandatory)

After loading the USB-to-serial option driver for the module, device files such as ttyUSB0, ttyUSB1, and ttyUSB2 are created in the /dev directory. This section describes the modifications needed for the USB-to-serial option driver.

#### 2.1.1 Add the following configurations to the Linux kernel. For modification methods, please refer to [this link](../../../03_other/K230_SDK_FAQ_C.md#19-how-to-quickly-modify-linux-configuration)

```bash
CONFIG_USB_SERIAL
CONFIG_USB_SERIAL_OPTION
CONFIG_PPP=y
CONFIG_PPP_BSDCOMP=y
CONFIG_PPP_DEFLATE=y
CONFIG_PPP_FILTER=y
CONFIG_PPP_MPPE=y
CONFIG_PPP_MULTILINK=y
CONFIG_PPPOE=y
CONFIG_PPP_ASYNC=y
CONFIG_PPP_SYNC_TTY=y
```

#### 2.1.2 Add VID and PID to the option driver

```c
// Add the following option to the option_ids[] array in src/little/linux/drivers/usb/serial/option.c (approximately line 583)
{ USB_DEVICE_AND_INTERFACE_INFO(0x2c7c, 0x6005, 0xff, 0, 0) },
```

### 2.2 RNDIS/ECM Driver Modification

Add the following configurations to the Linux kernel. For modification methods, please refer to [this link](../../../03_other/K230_SDK_FAQ_C.md#19-how-to-quickly-modify-linux-configuration):

```shell
CONFIG_USB_NET_DRIVERS
CONFIG_USB_USBNET
CONFIG_USB_NET_RNDIS_HOST
CONFIG_USB_NET_CDCETHER
CONFIG_USB_NET_CDC_NCM
```

## 3. User-mode pppd Program Compilation and Configuration

Note: This chapter is needed only for PPPoE dial-up internet (PPP mode).

### 3.1 Adding pppd Program

Add the following configurations to buildroot:

```sh
BR2_PACKAGE_PPPD
BR2_PACKAGE_PPPD_FILTER
BR2_PACKAGE_PPPD_RADIUS
```

To add configurations to buildroot:

Execute `make buildroot-menuconfig` in the SDK main directory;

Add the required configurations, save the configuration;

Execute `make buildroot-savedefconfig`.

### 3.2 Adding PPP Configuration Files

#### 3.2.1 Create directories in the SDK main directory

```sh
mkdir board/common/post_copy_rootfs/etc/ppp
mkdir board/common/post_copy_rootfs/etc/ppp/peers
```

#### 3.2.2 Create the following files

- `board/common/post_copy_rootfs/etc/ppp/ip-up`
- `board/common/post_copy_rootfs/etc/ppp/peers/quectel-pppd`
- `board/common/post_copy_rootfs/etc/ppp/peers/quectel-chat-disconnect`
- `board/common/post_copy_rootfs/etc/ppp/quectel-pppd.sh`
- `board/common/post_copy_rootfs/etc/ppp/quectel-ppp-kill`

Contents of the files:

```shell
#!/bin/sh
# board/common/post_copy_rootfs/etc/ppp/ip-up
if [ -f /etc/ppp/resolv.conf ]; then
    cp /etc/ppp/resolv.conf /etc/resolv.conf
elif [ -f /var/run/ppp/resolv.conf ]; then
    cp /var/run/ppp/resolv.conf /etc/resolv.conf
else
    echo nameserver $DNS1 > /etc/resolv.conf
    echo nameserver $DNS2 >> /etc/resolv.conf
fi
```

```sh
# /etc/ppp/peers/quectel-pppd
# Usage: root> pppd call quectel-pppd
# Modem path, like /dev/ttyUSB3, /dev/ttyACM0, depend on your module, default path is /dev/ttyUSB3
/dev/ttyUSB2 115200
# Insert the username and password for authentication, default user and password are test
user "test" password "test"
# The chat script, customize your APN in this file
connect 'chat -s -v -f /etc/ppp/peers/quectel-chat-connect'
# The close script
disconnect 'chat -s -v -f /etc/ppp/peers/quectel-chat-disconnect'
# Hide password in debug messages
hide-password
# The phone is not required to authenticate
noauth
# Debug info from pppd
debug
# If you want to use the HSDPA link as your gateway
defaultroute
# pppd must not propose any IP address to the peer
noipdefault
# No ppp compression
novj
novjccomp
noccp
ipcp-accept-local
ipcp-accept-remote
local
# For sanity, keep a lock on the serial line
lock
modem
dump
nodetach
# Hardware flow control
nocrtscts
remotename 3gppp
ipparam 3gppp
ipcp-max-failure 30
# Ask the peer for up to 2 DNS server addresses
usepeerdns
```

```sh
# /etc/ppp/peers/quectel-chat-disconnect
ABORT "ERROR"
ABORT "NO DIALTONE"
SAY "\nSending break to the modem\n"
""  +++
""  +++
""  +++
SAY "\nGoodbye\n"
```

```shell
#!/bin/sh
# /etc/ppp/quectel-pppd.sh

# quectel-pppd devname apn user password
echo "quectel-pppd options in effect:"
QL_DEVNAME=/dev/ttyUSB2
QL_APN=3gnet
QL_USER=user
QL_PASSWORD=passwd
if [ $# -ge 1 ]; then
    QL_DEVNAME=$1
    echo "devname   $QL_DEVNAME    # (from command line)"
else
    echo "devname   $QL_DEVNAME    # (default)"
fi
if [ $# -ge 2 ]; then
    QL_APN=$2
    echo "apn       $QL_APN    # (from command line)"
else
    echo "apn       $QL_APN    # (default)"
fi
if [ $# -ge 3 ]; then
    QL_USER=$3
    echo "user      $QL_USER   # (from command line)"
else
    echo "user      $QL_USER   # (default)"
fi
if [ $# -ge 4 ]; then
    QL_PASSWORD=$4
    echo "password  $QL_PASSWORD   # (from command line)"
else
    echo "password  $QL_PASSWORD   # (default)"
fi

CONNECT="'chat -s -v ABORT BUSY ABORT \"NO CARRIER\" ABORT \"NO DIALTONE\" ABORT ERROR ABORT \"NO ANSWER\" TIMEOUT 30 \
\"\" AT OK ATE0 OK ATI\;+CSUB\;+CSQ\;+CPIN?\;+COPS?\;+CGREG?\;\&D2 \
OK AT+CGDCONT=1,\\\"IP\\\",\\\"$QL_APN\\\",,0,0 OK ATD*99# CONNECT'"

pppd $QL_DEVNAME 115200 user "$QL_USER" password "$QL_PASSWORD" \
connect "'$CONNECT'" \
disconnect 'chat -s -v ABORT ERROR ABORT "NO DIALTONE" SAY "\nSending break to the modem\n" "" +++ "" +++ "" +++ SAY "\nGoodbye\n"' \
noauth debug defaultroute noipdefault novj novjccomp noccp ipcp-accept-local ipcp-accept-remote ipcp-max-configure 30 local lock modem dump nodetach nocrtscts usepeerdns &
```

```shell
#!/bin/sh
# /etc/ppp/quectel-ppp-kill
timeout=5
killall -15 pppd
sleep 1
killall -0 pppd
while [ $? -eq 0 ]
do
    timeout=`expr $timeout - 1`
    if [ $timeout -eq 0 ]
    then
        exit 1
    fi
    sleep 1
    killall -0 pppd
done

if [ $? -ne 0 ]
then
    killall -9 pppd
fi
```

Increase executable permissions:

```shell
chmod a+x board/common/post_copy_rootfs/etc/ppp/ip-up
chmod a+x board/common/post_copy_rootfs/etc/ppp/peers/quectel-pppd
chmod a+x board/common/post_copy_rootfs/etc/ppp/peers/quectel-chat-disconnect
chmod a+x board/common/post_copy_rootfs/etc/ppp/quectel-pppd.sh
chmod a+x board/common/post_copy_rootfs/etc/ppp/quectel-ppp-kill
```

## 3. Testing

### 3.1 Confirm Whether the Driver is Loaded Correctly

Execute `cat /sys/kernel/debug/usb/devices` and `dmesg` commands to check if the driver is loaded correctly. Correct output should be similar to the following:

```shell
[root@canaan ~ ]#mount -t debugfs none /sys/kernel/debug/
[root@canaan ~ ]#cat /sys/kernel/debug/usb/devices

T:  Bus=01 Lev=01 Prnt=01 Port=00 Cnt=01 Dev#=  2 Spd=480  MxCh= 0
D:  Ver= 2.00 Cls=ef(misc ) Sub=02 Prot=01 MxPS=64 #Cfgs=  1
P:  Vendor=2c7c ProdID=6005 Rev= 3.18
S:  Manufacturer=Android
S:  Product=Android
S:  SerialNumber=0000
C:* #Ifs= 6 Cfg#= 1 Atr=e0 MxPwr=500mA
A:  FirstIf#= 0 IfCount= 2 Cls=02(comm.) Sub=06 Prot=00
I:* If#= 0 Alt= 0 #EPs= 1 Cls=02(comm.) Sub=06 Prot=00 Driver=cdc_ether
E:  Ad=87(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:  If#= 1 Alt= 0 #EPs= 0 Cls=0a(data ) Sub=00 Prot=00 Driver=cdc_ether
I:* If#= 1 Alt= 1 #EPs= 2 Cls=0a(data ) Sub=00 Prot=00 Driver=cdc_ether
E:  Ad=83(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0c(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
I:* If#= 2 Alt= 0 #EPs= 2 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=82(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0b(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
I:* If#= 3 Alt= 0 #EPs= 3 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=86(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0f(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=89(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:* If#= 4 Alt= 0 #EPs= 3 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=81(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0a(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=88(I) Atr=03(Int.) MxPS=  64 Ivl=4096ms
I:* If#= 6 Alt= 0 #EPs= 2 Cls=ff(vend.) Sub=00 Prot=00 Driver=option
E:  Ad=85(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0e(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms
```

Sub=00 Prot=00 Driver=option
E:  Ad=85(I) Atr=02(Bulk) MxPS= 512 Ivl=0ms
E:  Ad=0e(O) Atr=02(Bulk) MxPS= 512 Ivl=0ms

Run `ls /sys/bus/usb/drivers` to see the drivers

```shell
[root@canaan ~ ]# ls /sys/bus/usb/drivers
asix          cdc_subset    net1080       rtl8150       zaurus
ax88179_178a  cdc_wdm       option        usb
catc          hub           pegasus       usb-storage
cdc_ether     kaweth        qmi_wwan      usbfs
cdc_ncm       lan78xx       r8152         usbhid rndis_host
[root@canaan ~ ]#
```

Using `dmesg`, you can see output similar to the following:

```shell
[    3.164039] usb 1-1: config 1 has an invalid interface number: 6 but max is 5
[    3.171246] usb 1-1: config 1 has no interface number 5
[    3.176938] usb 1-1: New USB device found, idVendor=2c7c, idProduct=6005, bcdDevice= 3.18
[    3.185189] usb 1-1: New USB device strings: Mfr=1, Product=2, SerialNumber=3
[    3.192350] usb 1-1: Product: Android
[    3.196026] usb 1-1: Manufacturer: Android
[    3.200151] usb 1-1: SerialNumber: 0000
[    3.206236] cdc_ether 1-1:1.0 usb0: register 'cdc_ether' at usb-91500000.usb-otg-1, CDC Ethernet Device, 02:0c:29:a3:9b:6d
[    3.218140] option 1-1:1.2: GSM modem (1-port) converter detected
[    3.224982] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB0
[    3.232586] option 1-1:1.3: GSM modem (1-port) converter detected
[    3.239337] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB1
[    3.247057] option 1-1:1.4: GSM modem (1-port) converter detected
[    3.253786] usb 1-1: GSM modem (1-port) converter now attached to ttyUSB2
```

### 3.2 Testing AT Functionality

You can use UART tools like "minicom" or "busybox microcom" to test AT functionality.

```shell
[root@canaan ~ ]# microcom -t 10000 -s 115200 /dev/ttyUSB2
at+cpin?;+csq;+cops? +CSQ: 31,99

+CME ERROR: 10

+COPS: 0
```

### 3.3 RNDIS/ECM Mode Network Testing

#### 3.3.1 Set Module Working Mode

```sh
If in ECM mode, execute the following command:
echo -e "AT+QCFG=\"usbnet\",1\n\n;AT+CFUN=1,1\n\n" > /dev/ttyUSB2 ;sleep 15;
If in RNDIS mode:
echo -e "AT+QCFG=\"usbnet\",3\n\n;AT+CFUN=1,1\n\n" > /dev/ttyUSB2 ;sleep 15;
```

> Note: After setting, you need to wait for the module to restart. The correct driver will be loaded after the restart. The meaning of the above AT commands is as follows:
>
> `AT+QCFG="usbnet",1;`  // Set mode
>
> `AT+CFUN=1,1` // Restart module
>
> `AT+QCFG=usbnet` // Query mode
>
> `AT+qnetdevctl=3,1,1`  // Dial-up;

#### 3.3.2 Dial-up

```sh
echo -e "AT+qnetdevctl=3,1,1\n\n" > /dev/ttyUSB2
```

#### 3.3.3 Obtain IP Address

```sh
[root@canaan ~ ]# ifconfig eth0 down; udhcpc -i usb0; ifconfig;
udhcpc: started, v1.33.0
udhcpc: sending discover
udhcpc: sending select for 10.232.182.16
udhcpc: lease of 10.232.182.16 obtained, lease time 86400
deleting routers
adding dns 183.230.126.225
adding dns 183.230.126.224
```

#### 3.3.4 Network Testing

```shell
[root@canaan ~ ]# ping -I usb0 www.163.com
PING www.163.com (111.13.104.117): 56 data bytes
64 bytes from 111.13.104.117: seq=0 ttl=55 time=45.732 ms
64 bytes from 111.13.104.117: seq=1 ttl=55 time=46.759 ms
^C
--- www.163.com ping statistics ---
2 packets transmitted, 2 packets received, 0% packet loss
round-trip min/avg/max = 45.732/46.245/46.759 ms
[root@canaan ~ ]#
```

### 3.4 PPP Mode Network Testing

#### 3.4.1 Dial-up

```shell
ifconfig eth0 down
/etc/ppp/quectel-ppp-kill
/etc/ppp/quectel-pppd.sh  /dev/ttyUSB2 CMNET
```

#### 3.4.2 Testing

```shell
ifconfig
ping www.163.com
```

## 4. References

- "Quectel_UMTS_LTE_5G_Linux_USB_Driver_User_Guide"
- "Quectel_LTE_Standard(A)_Series_AT_Commands_Manual_V1.1"
- <https://doc.embedfire.com/linux/rk356x/quick_start/zh/latest/quick_start/wireless/4g/4g.html#quectel-cm>
- <https://github.com/turmary/linux-ppp-scripts>
