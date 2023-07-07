# K230 SDK IoT WiFi AiW4211LV10驱动开发指南

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

本文档主要描述IoT WiFi AiW4211LV10驱动在K230 EVB平台上的开发方法，其中包括硬件环境搭建，模块编译配置方法，驱动加载及网络配置工具使用等信息，并对WiFi控制接口进行介绍。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
|------|------|
|      |      |

### 修订记录

| 文档版本号 | 修改说明                                                                                               | 修改者 | 日期       |
|------------|--------------------------------------------------------------------------------------------------------|--------|------------|
| V1.0       | 初版                                                                                                   | 徐百坤 | 2023/04/08 |
| V1.1       | 修改2.2章节，WiFi子板硬件更新到V1.1，分线链接变化 修改3.2、3.3章节，修改sdio扫描接口调用方式为间接调用 | 徐百坤 | 2023/04/13 |

## 1. 功能介绍

AiW4211LV10是一款低功耗IoT WiFi芯片，我司采用该芯片平台设计了一款AiW4211LV10开发板，该开发板可插入K230 EVB板的TF卡插槽实现接入。K230 EVB加载AiW4211LV10驱动之后，可以生成wlan0无线网卡，实现网络数据通信。

## 2. 模块依赖

硬件上依赖AiW4211LV10开发板，依赖K230 EVB开发板，K230 EVB为WiFi提供电源及中断检测连线。

软件上依赖于K230 SDIO主控驱动，依赖GPIO驱动的完备，需要emmc引导启动实现。

### 2.1 操作系统

当前驱动支持linux 4.9、linux 4.17和linux 5.10.4

### 2.2 硬件环境

K230 EVB开发板设置emmc启动，空出TF卡插槽用于AiW4211LV10开发板接入。

K230 EVB开发板飞线到AiW4211LV10开发板排针。连接关系如下：

表 2-1 飞线关系

|          | Link1         | Link2                  | Link3        | Link4        | Link5         |
|----------|---------------|------------------------|--------------|--------------|---------------|
| K230排针 | J5 PIN16 (5V) | J8 PIN9 (GPIO34)       |              |              |               |
| WiFi排针 | J6 PIN1 (5V)  | J2 PIN3 (SDIO_INT_OUT) | J2 PIN4 (TX) | J2 PIN5 (RX) | J2 PIN6 (GND) |
| TTL-USB  |               |                        | RX           | TX           | GND           |

备注：TTL-USB与WiFi的连线主要是为了观察WiFi的固件输出，可以不连接

## 3. 模块配置

### 3.1 设备树修改

#### 3.1.1 配置引脚function

修改uboot设备树arch/riscv/dts/k230_evb.dts，配置K230 EVB IO52引脚功能为GPIO，方向为input：

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

#### 3.1.2 配置GPIO控制器

修改linux设备树arch/riscv/boot/dts/kendryte/gpio_provider.dtsi，配置K230 EVB GPIO52控制器：

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

#### 3.1.3 配置SDHCI1参数

修改linux设备树arch/riscv/boot/dts/kendryte/k230_evb.dtsi，配置对应sdio主控参数：

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

### 3.2 内核配置项

通过内核配置将AiW4211LV10驱动编译为内核模块，并将必要的协议及驱动编入内核。

使能kprobes：

```c
> General architecture-dependent options

|| [*] Kprobes

将cfg80211编入内核，注意需要选中 cfg80211 wireless extensions compatibility：

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

将AiW4211LV10驱动编译成内核模块，注意需要选中 IEEE 802.11 for Host AP (Prism2/2.5/3 and WEP/TKIP/CCMP)：

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

### 3.3 SDIO主控增加扫描接口

AiW4211LV10驱动需要依据WiFi所接入的槽位发起SDIO扫描，因此特封装plat_sdio_rescan接口函数。修改drivers/mmc/host/sdhci-of-dwcmshc.c文件如下：

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

## 4. 模块编译

在SDK顶层执行make linux，随内核一同编译，ko临时存储在output/k230_evb_defconfig/little/linux/drivers/net/wireless/aich/aiw4211lv10/目录。

## 5. 模块启动

### 5.1 WiFi固件

在K230 SDK当中WiFi固件AiW4211L_demo_allinone.bin以二进制文件形式提供，如需源码请联系我们。

固件存储路径：k230_sdk/src/little/utils/firmware/AiW4211L_demo_allinone.bin

### 5.2 驱动加载

在硬件环境配置完成后上电启动，执行以下指令即可实现驱动加载：

modprobe aiw4211lv10 或者 modprobe aiw4211lv10 mmc=1 gpio=52

当前驱动支持传入mmc主控编号及用于中断检测的gpio编号，可以实现较为灵活的硬件配置，如果不传参则分别使用代码中规定的默认值1和52。

驱动加载完成后，使用ifconfig -a指令可以看到已经生成了无线网卡wlan0。

### 5.3 网络配置

启动配置工具server端并置于后台运行：iotwifi_link &

该工具的功能角色类似于wpa_supplicant。iotwifi_link首先会将wlan0 up起来，然后从WiFi设备侧同步mac地址及ip地址到host端。

运行配置工具client端，控制WiFi接入AP及设置其他参数：iotwifi_cli --config /etc/wifi.conf

运行配置工具client端，控制WiFi进入深睡模式：iotwifi_cli --dirsleep

/etc/wifi.conf是WiFi工作参数配置文件，以json格式编写，基本上是对wifi_config_t结构体的映射，具体可参考6.1.2章节。

## 6. API参考

AiW4211LV10驱动加载后生成的无线网卡与一般WiFi网卡无异，因此网络通信功能无特殊API需要说明。

除基本的网络通信外，K230与WiFi还存在两个消息通信接口，需要重点说明。

### 6.1 config接口

#### 6.1.1 API

int kd_wifi_config([wifi_config_t](#6121-wifi_config_t) \*config)

配置WiFi工作参数：

- 配置目标AP的名称、密码、认证及加密方式
- 配置WiFi休眠等级，苏醒周期以及可唤醒的gpio
- 配置tcp keepalive时间参数等

#### 6.1.2 数据结构

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

表 6-1 wifi_config_t结构体成员

| 成员                            |  说明   |
|---------------------------------|---------|
| config_mask                    | 配置目标项掩码，使能或屏蔽目标项，例如全部配置则：config_mask = CFG_MASK_SLEEP\|CFG_MASK_CONNECT\|CFG_MASK_KEEPALIVE;  CFG_MASK_SLEEP：配置休眠参数，CFG_MASK_CONNECT：配置AP连接参数，CFG_MASK_KEEPALIVE：配置tcp keepalive参数 |
| [sleep](#6122-wifi_sleep_t)         | 休眠参数  |
| [conn](#6123-wifi_connect_t)        | AP连接参数|
| [keepalive](#6124-wifi_keepalive_t) | tcp keepalive参数|

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

表 6-2 wifi_sleep_t结构体成员

| 成员         | 说明 |
|-------------|-------|
| level      | 休眠等级 WIFI_SLEEP_LIGHT：浅睡 WIFI_SLEEP_DEEP：深睡，主要休眠模式 WIFI_SLEEP_ULTRA：超深睡，只有3/5/7/14号gpio可唤醒，目前不使用 |
| period     | 苏醒周期，有效数值33\~\~4000ms。WiFi周期性从休眠态醒来，检测AP是否有发给自己的数据缓存                                             |
| wake_gpios | enable或disable可唤醒WiFi的gpio（WiFi侧gpio）|

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

表 6-3 wifi\_**connect**\_t结构体成元

| ssid     | AP名称 |
|----------|--------|
| auth     | 认证类型 EXT_WIFI_SECURITY_OPEN EXT_WIFI_SECURITY_WEP EXT_WIFI_SECURITY_WPA2PSK EXT_WIFI_SECURITY_WPAPSK_WPA2PSK_MIX EXT_WIFI_SECURITY_WPAPSK EXT_WIFI_SECURITY_WPA EXT_WIFI_SECURITY_WPA2 EXT_WIFI_SECURITY_SAE EXT_WIFI_SECURITY_WPA3_WPA2_PSK_MIX EXT_WIFI_SECURITY_UNKNOWN |
| Key      | AP密码                                                                                                                                                                                                                                                                         |
| bssid    | AP bssid，一般为AP mac地址                                                                                                                                                                                                                                                     |
| pairwise | 加密类型 EXT_WIFI_PARIWISE_UNKNOWN EXT_WIFI_PAIRWISE_AES EXT_WIFI_PAIRWISE_TKIP EXT_WIFI_PAIRWISE_TKIP_AES_MIX                                                                                                                                                                 |

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

表 6-4 wifi_keepalive_t结构体成员

| svrip                | server端ip地址                                                          |
|----------------------|-------------------------------------------------------------------------|
| svrport              | server端端口号                                                          |
| tcp_keepalive_time   | TCP层keepalive心跳包常规发送周期，秒                                    |
| tcp_keepalive_intvl  | TCP层keepalive心跳包无回应之后新的发送周期，秒                          |
| tcp_keepalive_probes | TCP层keepalive心跳包无回应计数超过该阈值之后，判断TCP连接异常，断开重连 |
| heartbeat_intvl      | 应用层心跳包发送周期，秒                                                |
| heartbeat_probes     | 应用层心跳包无回应计数超过该阈值之后，判断socket连接异常，断开重连      |

### 6.2 sleep接口

int kd_wifi_sleep(void)

控制WiFi进入休眠，休眠相关参数在config API当中设置。

## 7. 基本性能测试

### 7.1 吞吐量测试

在办公室环境使用iperf进行网络吞吐量测试，PC通过网线接入AP，K230 EVB通过AiW4211LV10接入同一AP，分别在两端启动iperf工具，交叉测试上行及下行吞吐量。

client：iperf -c xxx.xxx.xxx.xxx -i 2 -t 300

server：iperf -s -i 2

dual：iperf -c xxx.xxx.xxx.xxx -i 2 -t 300 -d

表 7-1 TCP吞吐量粗测数据

| WiFi ROLE | Bandwidth(Mbits/sec) |
|-----------|----------------------|
| client    | 12.2                 |
| server    | 20.3                 |

client：iperf -c xxx.xxx.xxx.xxx -i 2 -t 300 -u -b 25M

server：iperf -s -i 2 -u

表 7-2 UDP吞吐量粗测数据

| WiFi ROLE | Bandwidth(Mbits/sec) | Jitter(ms) | Lost/Total Datagrams |
|-----------|----------------------|------------|----------------------|
| client    | 17.8                 | 1.341      | 1571/455457 (0.34%)  |
| server    | 21.0                 | 1.064      | 1/534990 (0.00019%)  |

## 7.2 文件传输测试

分别在PC与K230 EVB端架设nginx服务器，并分别使用wget拉取544MB大文件，并校验拉取文件的MD5值，测试150次无异常。
