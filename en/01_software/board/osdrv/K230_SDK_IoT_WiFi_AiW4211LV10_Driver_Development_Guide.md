# K230 SDK IoT WiFi AiW4211LV10 Driver Development Guide

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

## Preface

### Overview

This document mainly describes the development method of IoT WiFi AiW4211LV10 driver on the K230 EVB platform, including hardware environment construction, module compilation and configuration methods, driver loading and network configuration tool use, and introduces the WiFi control interface.

### Reader Object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of Acronyms

| abbreviation | illustrate |
|------|------|
|      |      |

### Revision History

| Document version number | Modify the description                                                                                               | Author | date       |
|------------|--------------------------------------------------------------------------------------------------------|--------|------------|
| V1.0       | Initial edition                                                                                                   | Xu Baikun | 2023/04/08 |
| V1.1       | Modify section 2.2, update WiFi daughter board hardware to V1.1, and change the breakout link Modify sections 3.2 and 3.3 to change the SDK scan interface call mode to indirect | Xu Baikun | 2023/04/13 |

## 1. Function Introduction

AiW4211LV10 is a low-power IoT WiFi chip, our company uses this chip platform to design an AiW4211LV10 development board, which can be inserted into the TF card slot of the K230 EVB board to achieve access. After the K230 EVB is loaded with the AiW4211LV10 driver, a wlan0 wireless card can be generated to realize network data communication.

## 2. Module Dependencies

The hardware relies on the AiW4211LV10 development board and the K230 EVB development board, which provides power and interrupt detection connection for WiFi.

The software relies on the K230 SDIO main control driver, relies on the complete GPIO driver, and requires emmc boot implementation.

### 2.1 Operating System

The current driver supports Linux 4.9, Linux 4.17, and Linux 5.10.4

### 2.2 Hardware Environment

The K230 EVB development board is set to emmc startup, and the TF card slot is vacated for AiW4211LV10 development board access.

K230 EVB development board flying wire to AiW4211LV10 development board pin header. The connection relationship is as follows:

Table 2-1 Flyline relationships

|          | Link1         | Link2                  | Link3        | Link4        | Link5         |
|----------|---------------|------------------------|--------------|--------------|---------------|
| K230 pin header | J5 PIN16 (5V) | J8 PIN9 (GPIO34)       |              |              |               |
| WiFi pin header | J6 PIN1 (5V)  | J2 PIN3 (SDIO_INT_OUT) | J2 PIN4 (TX) | J2 PIN5 (RX) | J2 PIN6 (GND) |
| TTL-USB  |               |                        | RX           | TX           | GND           |

Note: TTL-USB is connected to WiFi mainly to observe the firmware output of WiFi, and can not be connected

## 3. Module Configuration

### 3.1 Device Tree Modification

#### 3.1.1 Configure Pin Function

Modify the uboot device tree arch/riscv/dts/k230_evb.dts, and configure the K230 EVB IO52 pin function as GPIO and the direction as input:

```c
&iomux {
pinctrl-names = "default";
pinctrl-0 = <&pins>;
pins: iomux_pins {
pinctrl-single,pins = <

......

(IO52) ( 0 <<SEL | 0<<SL | BANK_VOLTAGE_IO50_IO61<<MSC | 1<<IE | 0<<OE | 0<<PU | 1<<PD | 7<<DS | 0<<ST )
}
}
```

#### 3.1.2 Configure the GPIO Controller

Modify the Linux device tree arch/riscv/boot/dts/kendryte/gpio_provider.dtsi to configure the K230 EVB GPIO52 controller:

```c
/ {

......

gpio52: gpio52@9140c000 {
#address-cells = <1>;
#size-cells = <0>;
compatible = "canaan,k230-apb-gpio";
reg = <0x0 0x9140c000 0x0 0x1000>;
interrupt-controller;
interrupt-parent = <&intc>;
#interrupt-cells = <2>;
interrupts = <84 IRQ_TYPE_EDGE_RISING>;

port52: gpio-controller@0 {
gpio-controller;
#gpio-cells = <2>;
nr-gpios = <1>;
reg-bank = <0>;
id = <52>;
};
};
};
```

#### 3.1.3 Configure SDHCI1 Parameters

Modify the Linux device tree arch/riscv/boot/dts/kendryte/k230_evb.dtsi, and configure the corresponding sdio master parameters:

```c
sdcard: sdhci1@91581000 {
compatible = "snps,dwcmshc-sdhci";
reg = <0x0 0x91581000 0x0 0x1000>;
interrupt-parent = <&intc>;
interrupts = <144>;
interrupt-names = "sdhci1irq";
clocks = <&dummy_sd>,<&dummy_sd>;
clock-names = "core", "bus";
max-frequency = <50000000>;
bus-width = <4>;
//cd-gpios = <>;
no-1-8-v;
cap-sd-highspeed;
sdhci,auto-cmd12;
status = "okay";
};
```

### 3.2 Kernel Configuration Items

Compile the AiW4211LV10 driver into a kernel module through kernel configuration, and program the necessary protocols and drivers into the kernel.

Enable kprobes:

```c
> General architecture-dependent options

|| [*] Kprobes

Integrate cfg80211 into the kernel. Note that cfg80211 wireless extensions compatibility needs to be selected：

> Networking support > Wireless

│ --- Wireless │ │

│ │ <*> cfg80211 - wireless configuration API │ │

│ │ [ ] nl80211 testmode command │ │

│ │ [ ] enable developer warnings │ │

│ │ [ ] cfg80211 certification onus │ │

│ │ [*] enable powersave by default │ │

│ │ [ ] cfg80211 DebugFS entries │ │

│ │ [*] support CRDA │ │

│ │ [*] cfg80211 wireless extensions compatibility │ │

│ │ [ ] lib80211 debugging messages │ │

│ │ < > Generic IEEE 802.11 Networking Stack (mac80211)
```

To compile the AiW4211LV10 driver into a kernel module, note that IEEE 802.11 for Host AP (Prism2/2.5/3 and WEP/TKIP/CCMP) needs to be selected:

```c
> Device Drivers > Network device support > Wireless LAN

│ --- Wireless LAN │ │

│ │ [ ] mac80211-based legacy WDS support │ │

│ │ [ ] ADMtek devices │ │

│ │ [*] Aich devices │ │

│ │ <M> Aich AiW4211LV10 (SDIO) support │

│ │ [ ] Atheros/Qualcomm devices │ │

│ │ [ ] Atmel devices │ │

│ │ [ ] Broadcom devices │ │

│ │ [ ] Cisco devices │ │

│ │ [ ] Intel devices │ │

│ │ [*] Intersil devices │ │

│ │ <*> IEEE 802.11 for Host AP (Prism2/2.5/3 and WEP/TKIP/CCMP)

│ │ [ ] Support downloading firmware images with Host AP driver │ │

│ │ [ ] Marvell devices │ │

│ │ [ ] MediaTek devices │ │

│ │ [ ] Microchip devices
```

### 3.3 SDIO Master Adds Scanning Interface

The AiW4211LV10 driver needs to initiate SDIO scanning according to the slot to which the WiFi is connected, so it specially encapsulates plat_sdio_rescan interface functions. Modify the drivers/mmc/host/sdhci-of-dwcmshc.c file as follows:

```c
static unsigned int slot_index = 0;
static struct mmc_host \*__mmc__host[3] = {NULL};
int plat_sdio_rescan(int slot)
{
struct mmc_host \*mmc = \__mmc__host[slot];
if (mmc == NULL) {
pr_err("invalid mmc, please check the argument\\n");
return -EINVAL;
}

mmc_detect_change(mmc, 0);
return 0;
}

static int dwcmshc_probe(struct platform_device \*pdev)
{

......

priv->bus_clk = devm_clk_get(&pdev-\>dev, "bus");
if (!IS_ERR(priv->bus_clk))
clk_prepare_enable(priv->bus_clk);
__mmc__host[slot_index++] = host->mmc;
err = mmc_of_parse(host->mmc);
if (err)
goto err_clk;

......

}
```

## 4. Module Compilation

Execute make linux at the top level of the SDK, compile with the kernel, and temporarily store the kot in the output/k230_evb_defconfig/little/linux/drivers/net/wireless/aich/aiw4211lv10/ directory.

## 5. Module Starts

### 5.1 WiFi Firmware

In the K230 SDK, WiFi firmware AiW4211L_demo_allinone.bin provided as binary files, please contact us for source code.

Firmware storage path: k230_sdk/src/little/utils/firmware/AiW4211L_demo_allinone.bin

### 5.2 Driver Loading

After the hardware environment configuration is completed, power on and start, execute the following instructions to achieve driver loading:

modprobe AIW4211LV10 or modprobe AIW4211LV10 MMC=1 GPIO=52

The current driver supports passing in the MMC master number and GPIO number for interrupt detection, which can achieve a more flexible hardware configuration, and if the parameter is not passed, the default values of 1 and 52 specified in the code are used respectively.

After the driver is loaded, use the ifconfig -a command to see that the wireless card wlan0 has been generated.

### 5.3 Network Configuration

Start the configuration tool server side and run it in the background: iotwifi_link &

The functional role of the tool is similar to wpa_supplicant. iotwifi_link first up, and then synchronize the MAC address and IP address from the WiFi device side to the host side.

Run the configuration tool client, control WiFi access AP and set other parameters: iotwifi_cli --config /etc/wifi.conf

Run the configuration tool client and control WiFi into deep sleep mode: iotwifi_cli --dirsleep

/etc/wifi.conf is a WiFi working parameter configuration file, written in JSON format, which is basically a mapping of wifi_config_t structures, please refer to Section 6.1.2 for details.

## 6. API Reference

The wireless network card generated after the AiW4211LV10 driver is loaded is no different from that of general WiFi network cards, so there is no special API for network communication functions.

In addition to basic network communication, K230 and WiFi also have two message communication interfaces, which need to be highlighted.

### 6.1 Config Interface

#### 6.1.1 API

int kd_wifi_config([wifi_config_t](#6121-wifi_config_t) \*config)

Configure WiFi working parameters:

- Configure the name, password, authentication, and encryption method of the target AP
- Configure WiFi sleep level, wake-up period, and wake-up GPIOs
- Configure TCP keepalive time parameters, etc

#### 6.1.2 Data Structures

##### 6.1.2.1 wifi_config_t

```c
typedef struct {
unsigned int config_mask;
#define CFG_MASK_SLEEP (1 << 0)
#define CFG_MASK_CONNECT (1 << 1)
#define CFG_MASK_KEEPALIVE (1 << 2)
wifi_sleep_t sleep;
wifi_connect_t conn;
wifi_keepalive_t keepalive;
} wifi_config_t;
```

Table 6-1 wifi_config_t struct members

| member                            |  illustrate   |
|---------------------------------|---------|
| config_mask                    | Configure the target item mask to enable or mask the target item, for example, configure all: config_mask = CFG_MASK_SLEEP\|CFG_MASK_CONNECT\|CFG_MASK_KEEPALIVE;  CFG_MASK_SLEEP: Configure sleep parameters, CFG_MASK_CONNECT: Configure AP connection parameters, CFG_MASK_KEEPALIVE: Configure tcp keepalive parameters |
| [sleep](#6122-wifi_sleep_t)         | Sleep parameters  |
| [Conn](#6123-wifi_connect_t)        | AP connection parameters|
| [keepalive](#6124-wifi_keepalive_t) | TCP keepalive parameter|

#### 6.1.2.2 wifi_sleep_t

```c
typedef struct
{
unsigned int level;
#define WIFI_SLEEP_LIGHT 1
#define WIFI_SLEEP_DEEP 2
#define WIFI_SLEEP_ULTRA 3
unsigned int period;
union
{
/*
* gpioX_wake: 0---disable, 1---enable
*/
struct {
unsigned int gpio0_wake:1;
unsigned int gpio1_wake:1;
unsigned int gpio2_wake:1;
unsigned int gpio3_wake:1;
unsigned int gpio4_wake:1;
unsigned int gpio5_wake:1;
unsigned int gpio6_wake:1;
unsigned int gpio7_wake:1;
unsigned int gpio8_wake:1;
unsigned int gpio9_wake:1;
unsigned int gpio10_wake:1;
unsigned int gpio11_wake:1;
unsigned int gpio12_wake:1;
unsigned int gpio13_wake:1;
unsigned int gpio14_wake:1;
};
unsigned int wake_gpios;
};
} wifi_sleep_t;
```

Table 6-2 wifi_sleep_t struct members

| member         | illustrate |
|-------------|-------|
| level      | Sleep level WIFI_SLEEP_LIGHT: light sleep WIFI_SLEEP_DEEP: deep sleep, main sleep mode WIFI_SLEEP_ULTRA: super deep sleep, only 3/5/7/14 GPIO can wake up, currently not used |
| period     | Wake up period, effective value 33\~\~4000ms. WiFi periodically wakes up from sleep to detect whether the AP has sent a cache of data to itself                                             |
| wake_gpios | Enable or disable to wake up WiFi gpio (WiFi side gpio)|

#### 6.1.2.3 wifi_connect_t

```c
typedef struct
{
char ssid[EXT_WIFI_MAX_SSID_LEN + 1];
ext_wifi_auth_mode auth;
char key[EXT_WIFI_MAX_KEY_LEN + 1];
unsigned char bssid[EXT_WIFI_MAC_LEN];
ext_wifi_pairwise pairwise;
} wifi_connect_t;
```

Table 6-3 wifi\_**connect**\_t structure elements

| ssid     | AP name |
|----------|--------|
| Auth     | Authentication Type EXT_WIFI_SECURITY_OPEN EXT_WIFI_SECURITY_WEP EXT_WIFI_SECURITY_WPA2PSK EXT_WIFI_SECURITY_WPAPSK_WPA2PSK_MIX EXT_WIFI_SECURITY_WPAPSK EXT_WIFI_SECURITY_WPA EXT_WIFI_ SECURITY_WPA2 EXT_WIFI_SECURITY_SAE EXT_WIFI_SECURITY_WPA3_WPA2_PSK_MIX EXT_WIFI_SECURITY_UNKNOWN |
| Key      | AP password                                                                                                                                                                                                                                                                         |
| BSSID    | AP bssid, generally the AP mac address                                                                                                                                                                                                                                                     |
| pairwise | Encryption type EXT_WIFI_PARIWISE_UNKNOWN EXT_WIFI_PAIRWISE_AES EXT_WIFI_PAIRWISE_TKIP EXT_WIFI_PAIRWISE_TKIP_AES_MIX                                                                                                                                                                 |

#### 6.1.2.4 wifi_keepalive_t

```c
typedef struct
{
unsigned char svrip[16];
unsigned short svrport;
unsigned short tcp_keepalive_time;
unsigned short tcp_keepalive_intvl;
unsigned short tcp_keepalive_probes;
unsigned short heartbeat_intvl;
unsigned short heartbeat_probes;
} wifi_keepalive_t;
```

Table 6-4 wifi_keepalive_t struct members

| svrip                | IP address of the server                                                          |
|----------------------|-------------------------------------------------------------------------|
| svrport              | The port number on the server side                                                          |
| tcp_keepalive_time   | TCP layer keepalive heartbeat packet regular send cycle, seconds                                    |
| tcp_keepalive_intvl  | TCP layer keepalive heartbeat packet does not respond after a new send cycle, seconds                          |
| tcp_keepalive_probes | After the TCP keepalive heartbeat packet no response count exceeds this threshold, the TCP connection is judged to be abnormal and disconnected and reconnected |
| heartbeat_intvl      | Application layer heartbeat packet sending cycle, seconds                                                |
| heartbeat_probes     | After the application-layer heartbeat packet no response count exceeds this threshold, the socket connection is determined to be abnormal and the socket is disconnected and reconnected      |

### 6.2 Sleep Interface

int kd_wifi_sleep(void)

To control WiFi sleep, sleep related parameters are set in the config API.

## 7. Basic Performance Test

### 7.1 Throughput Testing

In the office environment, iperf is used for network throughput testing, the PC is connected to the AP through the network cable, and the K230 EVB is connected to the same AP through the AiW4211LV10, and the iperf tool is launched at both ends to cross-test the upstream and downstream throughput.

client:iperf -c xxx.xxx.xxx.xxx -i 2 -t 300

server:iperf -s -i 2

dual:iperf -c xxx.xxx.xxx.xxx -i 2 -t 300 -d

Table 7-1 TCP throughput coarse measurement data

| WiFi ROLE | Bandwidth(Mbits/sec) |
|-----------|----------------------|
| client    | 12.2                 |
| server    | 20.3                 |

client:iperf -c xxx.xxx.xxx.xxx -i 2 -t 300 -u -b 25M

server:iperf -s -i 2 -u

Table 7-2 UDP throughput rough measurement data

| WiFi ROLE | Bandwidth(Mbits/sec) | Jitter(ms) | Lost/Total Datagrams |
|-----------|----------------------|------------|----------------------|
| client    | 17.8                 | 1.341      | 1571/455457 (0.34%)  |
| server    | 21.0                 | 1.064      | 1/534990 (0.00019%)  |

## 7.2 File Transfer Testing

Set up nginx servers on the PC and K230 EVB side, use wget to pull 544MB large files, verify the MD5 value of the pulled files, and test 150 times without abnormalities.
