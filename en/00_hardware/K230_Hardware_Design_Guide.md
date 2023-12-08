# K230 Hardware Design Guide

![cover](../../zh/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## directory

[toc]

## preface

### overview

This document mainly introduces the key points and precautions of K230 processor hardware design, aiming to help customers shorten the design cycle of products, improve product design stability and reduce failure rate. Customers are requested to refer to the requirements of this guide for hardware design, and try to use the relevant core templates released by K230. If it needs to be changed for special reasons, please strictly follow the high-speed digital circuit design requirements.

### Reader object

This document (this guide) is intended primarily for:

- Hardware Development Engineer
- Technical Support Engineer
- Test Engineer

### Glossary

| abbreviation  | illustrate                                     |
| ----- | ---------------------------------------- |
| DDR   | Double Data Rate                         |
| SDRAM | Synchronous Dynamic Random Access Memory |
| LPDDR | low power double data rate               |
| MIPI  | Mobile Industry Processor Interface      |
| OTG   | On the Go                                |
| APB   | Advanced Peripheral Bus                  |
| SPI   | Serial Peripheral Interface              |
| DMA   | Direct Memory Access                     |
| AHB   | Advanced High Performance Bus            |
| PCM   | Pulse Code Modulation                    |
| PDM   | Pulse Density Modulation                 |
| PCLK  | Peripheral High-speed Clock              |
| CLK   | Clock                                    |
| DQS   | Bi-directional Data Strobe               |
| GPIO  | General-purpose Input/Output             |
| eMMC  | Embedded Multi-media Card                |
| SIP   | System In a Package                      |
| PMU   | Power Management Unit                    |

### Revision history

| Document version number | Modify the description | Modified by | date       |
| ---------- | -------- | ------ | ---------- |
| V1.0       | first edition     | Zhao Ruixin | 2023-06-14 |

## 1. Chip overview

### 1.1 Chip block diagram

![Figure 1-1 K230 block diagram]（../../zh/00_hardware/images/HDG/image002.jpg)
Figure 1-1 K230 block diagram

### 1.2 Application Block Diagram

Figure 1-2 is the K230 door lock application block diagram
![Figure 1-2 K230 door lock scheme application block diagram]（../../zh/00_hardware/images/HDG/image003.jpg)
Figure 1-2 K230 door lock scheme application block diagram
Figure 1-3 is a block diagram of the dictionary pen scheme
![Figure 1-3 K230 dictionary pen scheme application block diagram]（../../zh/00_hardware/images/HDG/image004.jpg)
Figure 1-3 K230 dictionary pen scheme application block diagram

## 2. Package and pinout

### 2.1 Encapsulation

#### 2.1.1 Information

The package information of the K230 is shown in Table 2-1 below:

| Devices  | encapsulation     | size        | Pitch |
| ----- | -------- | ----------- | ----- |
| K230  | VFBGA390 | 13mm x 13mm | 0.65  |
| K230D | LFBGA256 | 11mm x 11mm | 0.65  |

#### 2.1.2 Package size

##### K230 size

![Figure 2-1]（../../zh/00_hardware/images/HDG/image005.png)
Figure 2-1
![Figure 2-2]（../../zh/00_hardware/images/HDG/image006.png)
Figure 2-2
![Figure 2-3]（../../zh/00_hardware/images/HDG/image007.png)
Figure 2-3

Spherical solder mask opening: 0.270mm

The main benchmark C and the bottom surface are solder balls

Size b is the measured maximum solder ball diameter, parallel to the main reference C

##### K230D size

![Figure 2-4]（../../zh/00_hardware/images/HDG/image008.png)
Figure 2-4
![Figure 2-5]（../../zh/00_hardware/images/HDG/image009.png)
Figure 2-5

Spherical solder mask opening: 0.270mm

The main benchmark C and the bottom surface are solder balls

Size b is the measured maximum solder ball diameter, parallel to the main reference C

#### 2.1.3 Pin definition diagram

The K230 pinout diagram is as follows:
![Figure 2-6 Pin distribution of K230 package]（../../zh/00_hardware/images/HDG/image010.png)
Figure 2-6 Pin distribution of K230 package
![Figure 2-7 Pin distribution of K230D package]（../../zh/00_hardware/images/HDG/image011.png)
Figure 2-7 Pin distribution of K230D package
Pin details are shown in Table[K230_PINOUT_V1.0_20230524.xlsx](../../zh/00_hardware/K230_PINOUT_V1.0_20230524.xlsx)

## 3. Schematic design suggestions

### 3.1. Minimal System Design

#### 3.1.1 Clock Requirements

The K230's main system requires a 24MHz high-speed clock, and the PMU subsystem's RTC requires a low-speed clock of 32.768kHz.

Table 3-1 shows the allowed clock source parameters for K230.

| Frequency      | precision  | Level |
| --------- | ----- | ---- |
| 32.768KHz | 20ppm | 1.8V |
| 24MHz     | 20ppm | 1.8V |

It is recommended to use a clock source of 20ppm or higher accuracy to provide the clock.

##### High-speed clock

The recommended passive crystal connection method is shown in Figure 3-1.
![Figure 3-1 K230 crystal circuit]（../../zh/00_hardware/images/HDG/image012.png)
Figure 3-1 K230 crystal circuit
Note:

- The capacitor selected needs to match the load capacitance of the crystal oscillator, and the material is recommended to use NPO.
- It is recommended to use a 4Pin oscillator, and the two GND pins are fully connected to the ground to enhance the system clock's anti-ESD interference capability.
- If you need to increase the starting speed, add a 1MΩ resistor between the IN pin and the OUT pin.

The recommended connection method of oscillator is shown in Figure 3-2.
![Figure 3-2 K230 oscillator circuit]（../../zh/00_hardware/images/HDG/image013.png)
Figure 3-2 K230 oscillator circuit
When working, the oscillator output is connected to the CLK24M_XIN pin of the K230, and the CLK24M_XOUT foot is suspended in the air.

##### Low-speed clock

The K230 chip has a built-in PMU module, and you should provide a clock circuit for the PMU module. The recommended circuit is shown in Figure 3-3.
![Figure 3-3 K230 RTC clock crystal circuit]（../../zh/00_hardware/images/HDG/image014.png)
Figure 3-3 K230 RTC clock crystal circuit
The recommended connection method of active crystal oscillator is shown in Figure 3-4.
![Figure 3-4 K230 RTC clock oscillator circuit]（../../zh/00_hardware/images/HDG/image015.png)
Figure 3-4 K230 RTC clock oscillator circuit

When working, the oscillator output is connected to the CLK32K768_XIN feet of the K230, and the CLK32K768_XOUT feet are suspended in the air.
Note:

- When using oscillators, the NC needs to be connected with 0Ω resistors in the above oscillator circuit diagrams.

#### 3.1.2 Reset circuit

The hardware reset of the K230 is implemented by the function of RSTN, which is active low.
If you use the button reset, it is recommended to add 100nF capacitor to the reset signal pin to eliminate the jitter of the reset signal, enhance the anti-interference ability, and prevent abnormal system reset caused by false triggering.
A schematic diagram of the reset circuit is shown in Figure 3-5.
![Figure 3-5 K230 reset circuit]（../../zh/00_hardware/images/HDG/image016.png)
Figure 3-5 K230 reset circuit

#### 3.1.3 System boot sequence

The K230 chip provides four boot methods, which can be configured through the BOOT0 and BOOT1 pins.
Table 3-2 shows the startup mode of K230 under different configurations.

| BOOT0 | BOOT1 | K230       | K230D      |
| ----- | ----- | ---------- | ---------- |
| 0     | 0     | NOR FLASH  | NOR FLASH  |
| 1     | 0     | NAND FLASH | NAND FLASH |
| 0     | 1     | MMC0       | MMC1       |
| 1     | 1     | MMC1       | MMC0       |

Table 3-2 Description of the start-up method

Note:

- When all four boot methods fail, it will jump to USB/UART boot.

Figure 3-6 shows the recommended BOOT circuit
![Figure 3-6 K230 BOOT circuit]（../../zh/00_hardware/images/HDG/image017.png)
Figure 3-6 K230 BOOT circuit

#### 3.1.4 JTAG Debug circuit

The recommended JTAG interface circuit for the K230 chip is shown in Figure 3-7.
![Figure 3-7 K230 JTAG download circuit]（../../zh/00_hardware/images/HDG/image018.png)
[Figure 3-7 K230 JTAG download circuit.]
Among them, JTAG_TCK, JTAG_TDI, JTAG_TMS and JTAG_RST are recommended to use 10kΩ pull-up JTAG_TDO dangling.
The K230 must use the CKLink series debugger provided by Pingtouge Semiconductor Co., Ltd., otherwise the chip cannot be debugged.

#### 3.1.5 DDR controller

The K230 chip is available in K230 and K230D versions, and the K230 version requires a separate DDR circuit. The K230D version packages a DDR Die without the need for external DDR circuitry.
The K230 DDR controller has the following features:

- Support LPDDR3/LPDDR4
- Support 2 rank
- Supports 16-bit and 32-bit DDR data bus widths
- Verified model: | type | Part number | Manufacturer | Capacity |
  | ------ | ---------------- | -------- | ---- |
  | LPDDR3 | NT6CL128M32DM-H0 | Nanya | 4Gb  |
  | LPDDR4 | W66AP6NBUAF/G/HI | Winbond | 4Gb  |

The schematics of the K230 DDR PHY and individual DRAM must match the reference schematic, including the power supply decoupling capacitors.

##### LPDDR3

The circuit design of LPDDR3 is based on Figures 3-8, 3-9, 3-10, and 3-11.
![Figure 3-8 K230 LPDDR3 circuit]（../../zh/00_hardware/images/HDG/image019.png)
Figure 3-8 K230 LPDDR3 circuit
![Figure 3-9 K230 LPDDR3 power supply circuit]（../../zh/00_hardware/images/HDG/image020.png)
Figure 3-9 K230 LPDDR3 power supply circuit
![Figure 3-10 LPDDR3 particle power supply circuit]（../../zh/00_hardware/images/HDG/image021.png)
Figure 3-10 LPDDR3 particle power supply circuit
![Figure 3-11 LPDDR3 particle circuit]（../../zh/00_hardware/images/HDG/image022.png)
Figure 3-11 LPDDR3 particle circuit

When using LPDDR3:

- The DDR PHY and each DRAM schematic need to be consistent with the reference design diagram, including the power supply decoupling capacitors
- DDR_ZN pin needs to be connected to ground with a calibration resistor of 240Ω (1%)
- DDR_RESET pin should be floating
- The chip has built-in the VREF circuit of the DDR controller, so the DDR_VREF pin needs to be floating
- The LP3 particles have a LP3_VREFDQ voltage of 0.8V, and it is recommended to divide the voltage using resistors of 100Ω and 200Ω (1%)
- LP3_VREFCA voltage is 0.6V, it is recommended to use a 1kΩ (1%) resistor generated
- The CA, CS, CKE, CLK, and ODT pins of LP3 all require 100Ω resistors to be pulled up and down to DDR_VDDQ_1V2 and ground

##### LPDDR4

The circuit design of LPDDR4 refers to Figure 3-12, Figure 3-13, Figure 3-14, Figure 3-15, and Figure 3-16.
![Figure 3-12 K230 LPDDR4 circuit]（../../zh/00_hardware/images/HDG/image023.png)
Figure 3-12 K230 LPDDR4 circuit
![Figure 3-13 K230 LPDDR4 power supply circuit]（../../zh/00_hardware/images/HDG/image024.png)
K230 LPDDR4 power circuit
![Figure 3-14 K230 LPDDR4 reference voltage circuit]（../../zh/00_hardware/images/HDG/image025.png)
Figure 3-14 K230 LPDDR4 reference voltage circuit LPDDR4 particle circuit] （../../zh/00_hardware/images/HDG/image026.png)
![Figure 3-16 LPDDR4 particle power supply circuit]（../../zh/00_hardware/images/HDG/image027.png)
Figure 3-16 LPDDR4 particle power supply circuit

When using LPDDR4, note:

- The DDR PHY and each DRAM schematic need to be consistent with the reference design diagram, including the power supply decoupling capacitors
- DDR_ZN pin needs to be connected to ground with a calibration resistor of 240Ω (1%)
- RESRT_N pin is connected directly to the corresponding pin of the Dram
- When the K230 uses LPDDR4 particles, the VREF voltage is 0.6V, and it is recommended to use a 1kΩ (1%) resistor generated

##### K230D DDR module

The K230D already has a built-in DDR die, so just connect the reference voltage and calibration resistor.
The reference circuits are shown in Figure 3-17 and Figure 3-18

![Figure 3-17 K230D DDR peripheral circuit]（../../zh/00_hardware/images/HDG/image028.png)
Figure 3-17 K230D DDR peripheral circuit
![Figure 3-18 K230D DDR reference voltage]（../../zh/00_hardware/images/HDG/image029.png)
Figure 3-18 K230D DDR reference voltage

When using the K230D's DDR module, note:

- The VREF voltage is 0.55V, and a 100Ω (1%) resistor divider is recommended
- 240Ω (1%) for calibration resistor

#### 3.1.6 FLASH

The K230 has an OSPI/QSPI controller that can be used to connect FLASH memory chips, which has the following features:

- OSPI supports NOR FLASH in 4/8-BIT MODE
- OSPI supports up to DDR200, SDR166 NOR FLASH
- QSPI SUPPORTS NAND&NOR FLASH IN 1/2/4 BIT MODE
- QSPI SUPPORTS NOR-FLASH UP TO SDR100

##### OSPI

The OSPI reference schematics are shown in Figure 3-19 and Figure 3-20
![Figure 3-19 K230 OSPI circuit]（../../zh/00_hardware/images/HDG/image030.png)
Figure 3-19 K230 OSPI circuit
![FIG. 3-20 OSPI FLASH CIRCUIT]（../../zh/00_hardware/images/HDG/image031.png)
FIG. 3-20 OSPI FLASH CIRCUIT

Please place the pull-up resistor according to the requirements of the FLASH chip.

##### QSPI NOR

In the QSPI signal, the pins of the CS, CLK, D0, D1, D2 and D3 signals are multiplexed with the pins of the corresponding signals of OSPI, as shown in Table 3-3

| QSPI pins | OSPI pins |
| -------- | -------- |
| QSPI_CS  | OSPI_CS  |
| QSPI_CLK | OSPI_CLK |
| QSPI_D0  | OSPI_D0  |
| QSPI_D1  | OSPI_D1  |
| QSPI_D2  | OSPI_D2  |
| QSPI_D3  | OSPI_D3  |

Table 3-3 QSPI and OSPI correspond to the pins

The reference circuit is shown in Figure 3-21
![FIG. 3-21 QSPI NOR FLASH CHIP CIRCUIT]（../../zh/00_hardware/images/HDG/image032.png)
FIG. 3-21 QSPI NOR FLASH CHIP CIRCUIT
Please place the pull-up resistor according to the requirements of the FLASH chip.

##### QSPI NAND

The reference circuit for QSPI NAND is shown in Figure 3-22.
![FIG. 3-22 QSPI NAND FLASH CHIP CIRCUIT]（../../zh/00_hardware/images/HDG/image033.png)
FIG. 3-22 QSPI NAND FLASH CHIP CIRCUIT
Please place the pull-up resistor according to the requirements of the FLASH chip.

### 3.2. MMC circuit

The K230 eMMC control circuit has two controllers, MMC0 and MMC1.

#### MMC0

The MMC0 controller has the following features:

- Support SDIO 3.0, operate in 4/1-bits mode, and support up to SDR104
- Support eMMC5.0 works in 8/4/1-bits mode, supports HS200
- Supports conversion of 3.3V and 1.8V voltages required by SD cards

MMC0 has more functions and is generally used to control eMMC circuits.
The recommended reference circuits for eMMC are shown in Figure 3-23 and Figure 3-24.

![Figure 3-23 K230 eMMC circuit]（../../zh/00_hardware/images/HDG/image034.png)
Figure 3-23 K230 eMMC circuit
![Figure 3-24 eMMC particle circuit]（../../zh/00_hardware/images/HDG/image035.png)
Figure 3-24 eMMC particle circuit

Please connect the corresponding pins according to the vender's requirements. If there are no special requirements, directly connect the corresponding pin.

#### MMC1

The MMC1 controller has the following features:

- Support SDIO 3.0, operate in 4/1-bits mode, and support up to SDR104
- Supports conversion of 3.3V and 1.8V voltages required by SD cards

the performance and function of MMC1 interface cannot meet the requirements of controlling eMMC circuits, and can only be used to control SD/TF card circuits.
The reference schematics are shown in Figure 3-25, Figure 3-26 and Figure 3-27.

![Figure 3-25 K230 SD card interface circuit]（../../zh/00_hardware/images/HDG/image036.png)
Figure 3-25 K230 SD card interface circuit
![Figure 3-26 SD card pull-up circuit]（../../zh/00_hardware/images/HDG/image037.png)
Figure 3-26 SD card pull-up circuit
![Figure 3-27 SD card holder circuit]（../../zh/00_hardware/images/HDG/image038.png)
Figure 3-27 SD card holder circuit

SD card circuit design should pay attention to:

- The voltage decoupling capacitor of the SD card pin must not be removed and should be placed close to the card holder
- Each signal needs to be placed with an ESD device near the SD card holder
- Each signal requires a pull-up resistor
- It is recommended to design according to the reference circuit

### 3.3. USB circuits

The K230 chip has two built-in USB2.0 OTG controllers, which have the following features:

- Supports USB 2.0 protocol and backward compatibility with USB 1.1 protocol
- Support Host mode or Device mode, optional support dynamic switching
- Host mode supports 480Mbps, 12Mbps, 1.5Mbps transmission rates
- Device mode supports 480Mbps, 12Mbps transmission mode

The USB circuit reference schematic is shown in Figure 3-28 and Figure 3-29.

![Figure 3-28 K230 USB circuit]（../../zh/00_hardware/images/HDG/image039.png)
Figure 3-28 K230 USB circuit
![Figure 3-29 USB interface circuit]（../../zh/00_hardware/images/HDG/image040.png)
Figure 3-29 USB interface circuit

Note:

- Each signal needs to be placed with an ESD device near the USB base
- The USB_VBUS power supply of the K230 must be connected in series with a 30kΩ (1%) resistor to a 5V power supply, and cannot be directly connected to the power supply
- To ensure signal quality, the K230's USB_TXRTUNE pin must be connected to ground with a 200Ω (1%) resistor
- USB_ID can be used for the identification of OTG devices, K230 is used as the HOST end when it is grounded, and K230 is used as the SLAVE end when it floats or pulls high

### 3.4. Audio Circuits

#### 3.4.1 I2S

The K230 chip has an I2S controller, which has the following features:

- Has two inputs and outputs
- Supports the PHILIP I2S standard
- Supports left and right and PCM formats
- Synchronous working mode
- Master or slave mode is optional
- Adjustable interface voltage
- Sample rates 8k to 384kHz

The I2S interface has 3 pins: I2S_CLK, I2S_WS and I2S_SD.
I2S_CK is a serial clock signal, I2S_WS is a data frame control signal, and I2S_SD is a serial data signal.
I2S interfaces are typically used to connect audio peripherals such as decoders.
Figure 3-30 and Figure 3-31 show the K230 I2S interface circuit and some peripheral circuits.
![Figure 3-30 K230 I2S interface circuit]（../../zh/00_hardware/images/HDG/image041.png)
Figure 3-30 K230 I2S interface circuit
![Figure 3-31 K230 I2S reference peripheral]（../../zh/00_hardware/images/HDG/image042.png)
Figure 3-31 K230 I2S reference peripheral

#### 3.4.2 PDM

The K230 supports 4 PDM signal inputs. Sample rates from 8k to 384kHz.
PDM interfaces are typically used to access audio devices with PDM interfaces such as digital microphones.
Figure 3-32 shows the PDM peripheral circuit of the K230.
![Figure 3-32 K230 PDM peripheral circuit]（../../zh/00_hardware/images/HDG/image043.png)
Figure 3-32 K230 PDM peripheral circuit

#### 3.4.3 Analog Audio Interface

The analog audio part of the K230 chip has the following features:

- Supports 2 DACs and 2 ADCs
- The DAC supports differential and single-ended outputs, and the ADC supports differential and single-ended inputs
- Supports low-noise analog microphone bias outputs

The reference circuits for analog audio are shown in Figure 3-33 and Figure 3-34
![Figure 3-33 K230 analog audio interface circuit]（../../zh/00_hardware/images/HDG/image044.png)
Figure 3-33 K230 analog audio interface circuit
![Figure 3-34 Audio interface circuit]（../../zh/00_hardware/images/HDG/image045.png)
Figure 3-34 Audio interface circuit

Note that for better sound quality, it is recommended to consider the following measures:

- The power supply pins use both large and small capacity low ESR ceramic capacitors
- The MICBIAS pin requires a large capacity low ESR capacitor
- The DC-blocking capacitor of the audio input is placed close to the K230 chip
- The output pin requires filter circuitry or DC-blocking capacitors

### 3.5. Video Circuits

#### 3.5.1 MIPI DSI

The K230's MIPI DSI controller has the following features:

- Support 1 signal output
- Supports 1/2/4 lane mode
- The maximum speed can reach 1.5Gbps

Each MIPI DSI signal is directly connected.
The reference hardware design is shown in Figure 3-35 and Figure 3-36

![Figure 3-35 K230 MIPI DSI interface circuit]（../../zh/00_hardware/images/HDG/image046.png)
![Figure 3-35 K230 MIPI DSI interface circuit]（../../zh/00_hardware/images/HDG/image047.png)
Figure 3-35 K230 MIPI DSI interface circuit
![Figure 3-36 Screen interface circuit]（../../zh/00_hardware/images/HDG/image048.png)
Figure 3-36 Screen interface circuit
Note:

- MIPI_ATB pin must be floating
- The MIPI_REXT pin must be connected to a 200Ω (1%) resistor to ground
- Each pin of this connector circuit is only suitable for the screen of Jinchaohui, please design the circuit according to your own screen module

### 3.6. Camera circuitry

#### 3.6.1 MIPI CSI

The K230's MIPI CSI controller has the following features:

- Support up to 3 channels MIPI input, support 1/2/4lane mode
- It can be configured as up to 3 channel 2lane or 1 channel 4lane and 1 channel 2lane signal input
- The maximum speed can reach 1.5Gbps

The MIPI CSI signal is recommended for direct connection.
The reference hardware design is shown in Figure 3-37 and Figure 3-38
![Figure 3-37 K230 MIPI CSI interface circuit]（../../zh/00_hardware/images/HDG/image049.png)
Figure 3-37 K230 MIPI CSI interface circuit
![Figure 3-38 Camera connector circuit]（../../zh/00_hardware/images/HDG/image050.png)
Figure 3-38 Camera connector circuit
Note:

- This connector circuit is for internal testing only, please design the circuit according to your needs

### 3.7. Low-speed subsystem circuits

#### 3.7.1 I2C circuit

The K230 chip supports 5 I2C interfaces with the following functions:

- Support I2C bus master mode
- Supports 7/10 bit addresses
- Supports I2C rates up to 3.4Mbit/s

When using I2C peripherals, it is necessary to pay attention to the corresponding power domain power supply, which must be consistent.
The SCL and SDA of I2C signals require external pull-up resistors, and resistors with different values are selected according to the bus load and bus rate.

- In a system of no more than 400kb/s, the recommended resistance is 4.7kΩ;
- In systems greater than 400 kb/s and less than 3.4 Mb/s, a pull-up resistor of 2.2 kΩ is recommended.

#### 3.7.2 UART circuits

The K230 supports 5 UART signals, which have the following features:

- Supports 2-wire UART and 4-wire UART
- Support RS485 interface
- Supports baud rates up to 3.125M
- Support software and hardware flow control, in line with 16750 standard
- Supports IrDA 1.0 SIR reception

When using UART peripherals, it is necessary to pay attention to the corresponding power domain, which must be consistent.

#### 3.7.3 PWM circuit

K230 supports 6 PWM signals, which have the following features:

- Any duty cycle is supported
- Support programmable output waveform
- Supports the generation of periodic pulse signals and one-off pulse signals
- Can be used as a cycle-accurate interrupt generator
- Supports output glitch removal

#### 3.7.4 MCLK circuit

The K230 supports the output of 3 MCLK signals. This signal can be used as the camera's drive clock.
The supported output clock frequencies are shown in Table 3-4:

|        |        |      |      |      |      |      |      |
| :----: | :----: | :---: | :---: | :---: | :---: | :---: | :---: |
|  792  |  132  | 66.67 | 46.59 |  36  | 28.57 | 23.76 | 18.56 |
|  594  | 118.8 |  66  | 45.69 | 34.94 | 28.29 | 23.53 | 18.18 |
|  400  | 113.14 |  66  | 44.44 | 34.43 | 28.29 | 22.85 | 17.39 |
|  396  |  100  | 60.92 |  44  | 33.33 | 27.31 | 22.22 | 16.67 |
|  297  |   99   | 59.4 | 42.43 |  33  |  27  |  22  |  16  |
|  264  |   99   | 57.14 | 41.68 |  33  | 26.67 | 21.21 | 15.38 |
|  200  |   88   | 56.57 |  40  | 31.68 | 26.4 | 21.05 | 14.81 |
|  198  | 84.86 |  54  | 39.6 | 31.26 | 25.83 | 20.48 | 14.29 |
|  198  |   80   | 52.8 | 39.6 | 30.77 | 25.55 |  20  | 13.79 |
| 158.4 |  79.2  |  50  | 37.71 | 30.46 |  25  | 19.8 | 13.33 |
| 148.5 | 74.25 | 49.5 | 37.13 | 29.7 | 24.75 | 19.16 | 12.9 |
| 133.33 |   72   | 49.5 | 36.36 | 29.33 | 24.75 | 19.05 | 12.5 |

Table 3-4 MCLK output clock frequency (unit: MHz)

#### 3.7.5 ADC circuit

The K230 integrates a SARADC with a resolution of 11 bits (effective resolution) and a maximum sampling rate of not less than 1MHz.
It has the following characteristics:

- Signal input range: 0-1.8V
- Supports 6 channel inputs
- Supports single and continuous sampling
- Integrated signal conditioning circuitry with a cutoff frequency of 1/2 bandwidth. The ADC can sample the signal directly or design peripheral circuitry as needed

#### 3.7.6 PMU circuit

The K230's PMU module is used to control the internal and external power supplies of the management chip.
It has a built-in RTC circuit and supports 6 inputs. Its functions are as follows:

| Interruption source | Along trigger | Level triggering | Debounce | Edge quantity detection | Long and short press detection |
| :----: | :----: | :------: | :----: | :----------: | :--------: |
| INT_0 |  support  |   support   |  support  |      -      |    support    |
| INT_1 |  support  |   support   |  support  |     support     |     -     |
| INT_2 |  support  |   support   |   -   |      -      |     -     |
| INT_3 |  support  |   support   |   -   |      -      |     -     |
| INT_4 |   -   |   support   |   -   |      -      |     -     |
| INT_5 |   -   |   support   |   -   |      -      |     -     |

Two outputs, OUT0 and OUT1, can be used to enable the power supply.
In the cold crank state, the PMU only enables the long press interrupt of INT0 and the high input interrupt of INT4 as the trigger source for the PMU module startup. OUT0 and OUT1 default output low with an initial pull-down resistor of approximately 40Ω.
When one of the above two interrupts is received, OUT0 pulls high, and OUT1 pulls up after about 50ms.
OUT0 and OUT1 can be used to control the enable pins of external PMICs or for other purposes.

### 3.8. Power Supply Design

#### 3.8.1 K230 Power Requirements

| module          | Power pins        | description                                                    |
| ------------- | --------------- | ------------------------------------------------------- |
| CORE          | VDD0P8_CORE     | CPU0 and other unit power supplies                                      |
| CPU           | VDD0P8_CPU      | CPU1 power supply                                                |
| KPU           | VDD0P8_KPU      | KPU power supply                                                 |
| DDR controller     | VDD0P8_DDR_CORE | DDR's digital CORE power supply, which can be powered down                                |
|               | VDD1P1_DDR_IO   | IO power supply for DDR                                             |
|               | VAA_DDR         | DDR phase-locked loop power supply                                           |
| USB           | AVDD3P3_USB     | The 3.3V power supply used by the USB PHY does not power up when not in use                 |
|               | AVDD1P8_USB     | The 1.8V power supply used by the USB PHY does not power up when not in use                 |
| PLL           | AVDD0P8_PLL     | PLL power supply                                                 |
| MIPI          | AVDD0P8_MIPI    | MIPI 0.8V power supply, not powered up when not in use                         |
|               | AVDD1P8_MIPI    | MIPI 1.8V power supply, not powered up when not in use                         |
| VDD1P8        | VDD1P8          | 1.8V module power supply                                            |
| ADC           | AVDD1P8_ADC     | ADC power supply, which does not power up when not in use                               |
| CODEC         | AVDD1P8_CODEC   | CODEC power supply, can not be powered on when not in use                             |
| PMU           | AVDD1P8_RTC     | The PMU has a built-in RTC power supply and can not be powered on when not in use                        |
|               | AVDD1P8_LDO     | The PMU has a built-in LDO power supply and can not be powered on when not in use                        |
| MMC           | VDD3P3_SD       | 3.3V output buffer and pre-buffer I/O power supply, which can not be powered up when not in use    |
| IO            | VDDIO3P3_0      | IO_2-IO_13 power supply, the voltage can be selected from 1.8V or 3.3V, and it can not be powered on when not in use  |
|               | VDDIO3P3_1      | IO_14-IO_25 power supply, the voltage can be selected from 1.8V or 3.3V, and it can not be powered on when not in use |
|               | VDDIO3P3_2      | IO_26-IO_37 power supply, the voltage can be selected from 1.8V or 3.3V, and it can be unpowered when not in use |
|               | VDDIO3P3_3      | IO_38-IO_49 power supply, the voltage can be selected 1.8V or 3.3V, and it can not be powered on when not in use |
|               | VDDIO3P3_4      | IO_50-IO_61 power supply, the voltage can be selected from 1.8V or 3.3V, and it can not be powered on when not in use |
|               | VDDIO3P3_5      | IO_62-IO_63 power supply, the voltage can be selected from 1.8V or 3.3V, and it can be powered up when not in use |
| K230D DDR section | VDD1P8_DDR_VDD1 | In the K230D, the DDR particle power supply, the K230 does not have this pin                      |
|               | VDD1P1_DDR_VDD2 | In the K230D DDR particle power supply, the K230 does not have this pin, and it cannot be powered down            |
|               | VDD1P1_DDR_VDDQ | The DDR particle power supply in the K230D, the K230 does not have this pin, and it can be powered down              |

Table 3-6 K230 Power Requirements Table

#### 3.8.2 Power-up timing

VDD0P8_CORE power-on must be earlier than VDD1P8, the IO interface from VDDIO3P3_0 to VDDIO3P3_5 must be powered on, AVDD0P8_MIPI power-up must be earlier than AVDD1P8_MIPI, AVDD1P8_RTC no later than AVDD1P8_LDO, and the rest of the order is not required.

#### 3.8.3 Power Supply Design Recommendations

##### PMU

| Module name | Pins        | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes        |
| -------- | ----------- | ----------- | ------------ | ----------- | --------- | --------------- |
| PMU      | AVDD1P8_RTC | 1.674       | 1.8          | 1.98        | 10        | LDO power supply is recommended |
|          | AVDD1P8_LDO | 1.674       | 1.8          | 1.98        | 10        | LDO power supply is recommended |

##### Core modules

| Module name | Pins        | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                                      |
| -------- | ----------- | ----------- | ------------ | ----------- | --------- | --------------------------------------------- |
| CORE     | VDD0P8_CORE | 0.72        | 0.8          | 0.88        | 2250      | It is recommended to use DC/DC with a power supply capacity of not less than 3A and low ripple noise |
| CPU      | VDD0P8_CPU  | 0.72        | 0.8          | 0.88        | 1000      | It is recommended to use DC/DC with a power supply capacity of not less than 2A and low ripple noise |
| KPU      | VDD0P8_KPU  | 0.72        | 0.8          | 0.88        | 3000      | It is recommended to use DC/DC with a power supply capacity of not less than 4A and low ripple noise |

##### DDR

| Module name | Pins                  | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                                              |
| -------- | --------------------- | ----------- | ------------ | ----------- | --------- | ----------------------------------------------------- |
| DDR      | VDD0P8_DDR_CORE       | 0.744       | 0.8          | 0.88        | 400       | The power supply ripple is required to be within 4%, and low-noise LDOs that can output high currents are recommended |
|          | VDD1P1_DDR_IO(LPDDR4) | 1.06        | 1.1          | 1.17        | 800       | LP4 ripple requirements are within 5%, and low-noise LDOs that can output large currents are recommended    |
|          | VDD1P1_DDR_IO(LPDDR3) | 1.14        | 1.2          | 1.3         | 800       | LP3 ripple requirements are within 10%, and low-noise LDOs that can output large currents are recommended   |
|          | VAA_DDR               | 1.674       | 1.8          | 1.98        | 10        | The ripple is required to be within 5% of the typical voltage                              |

##### K230D DDR Die

| Module name      | Pins            | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                                                |
| ------------- | --------------- | ----------- | ------------ | ----------- | --------- | ------------------------------------------------------- |
| K230D DDR die | VDD1P8_DDR_VDD1 | 1.7         | 1.8          | 1.95        | 75        | The ripple requirement is within 5% of the typical voltage and is in the same power network as the DDR controller power supply |
|               | VDD1P1_DDR_VDD2 | 1.06        | 1.1          | 1.17        | 450       | In the same power network as the VDD1P1_DDR_IO                           |
|               | VDD1P1_DDR_VDDQ | 1.06        | 1.1          | 1.17        | 300       | Low-noise LDOs that can output high currents are recommended                         |

##### I/O

| Module name | Pins       | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                                                                                                                                                                                   |
| -------- | ---------- | ----------- | ------------ | ----------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| IO       | VDDIO3P3_0 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        | The IO unit has a total of 5 sets of voltages, all of which can be configured as 1.8V or 3.3V, each group of voltages controls the output voltage and input voltage of the I/O port of the group, and also controls the output voltage and input voltage of the I/O multiplexed function. The IO voltage should be consistent with the peripheral device to be connected, and if it is inconsistent, level shifting is required. |
|          | VDDIO3P3_1 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        |                                                                                                                                                                                            |
|          | VDDIO3P3_2 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        |                                                                                                                                                                                            |
|          | VDDIO3P3_3 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        |                                                                                                                                                                                            |
|          | VDDIO3P3_4 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        |                                                                                                                                                                                            |
|          | VDDIO3P3_5 | 1.62/2.97   | 1.8/3.3      | 1.98/3.63   | 50        |                                                                                                                                                                                            |

##### USB

| Module name | Pins        | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes            |
| -------- | ----------- | ----------- | ------------ | ----------- | --------- | ------------------- |
| USB      | AVDD3P3_USB | 3.07        | 3.3          | 3.63        | 50        | It is recommended to use an LDO for power supply |
|          | AVDD1P8_USB | 1.674       | 1.8          | 1.98        | 60        | It is recommended to use an LDO for power supply |

##### PLL

| Module name | Pins        | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                  |
| -------- | ----------- | ----------- | ------------ | ----------- | --------- | ------------------------- |
| PLL      | AVDD0P8_PLL | 0.72        | 0.8          | 0.88        | 120       | It is recommended to use a high-precision LDO for power supply |

##### MIPI

| Module name | Pins         | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes            |
| -------- | ------------ | ----------- | ------------ | ----------- | --------- | ------------------- |
| MIPI     | AVDD0P8_MIPI | 0.744       | 0.8          | 0.88        | 100       | It is recommended to use an LDO for power supply |
|          | AVDD1P8_MIPI | 1.674       | 1.8          | 1.98        | 30        | It is recommended to use an LDO for power supply |

##### ADC

| Module name | Pins        | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                  |
| -------- | ----------- | ----------- | ------------ | ----------- | --------- | ------------------------- |
| ADC      | AVDD1P8_ADC | 1.62        | 1.8          | 1.98        | 10        | It is recommended to use a high-precision LDO for power supply |

##### CODEC

| Module name | Pins          | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes                  |
| -------- | ------------- | ----------- | ------------ | ----------- | --------- | ------------------------- |
| CODEC    | AVDD1P8_CODEC | 1.62        | 1.8          | 1.98        | 100       | It is recommended to use a high-precision LDO for power supply |

##### other

| Module name | Pins      | Minimum voltage(V) | Typical voltage (V) | Maximum voltage(V) | Current (mA) | Notes |
| -------- | --------- | ----------- | ------------ | ----------- | --------- | -------- |
| other     | VDD3P3_SD | 2.7         | 3.3          | 3.63        | 50        |          |
|          | VDD1P8    | 1.62        | 1.8          | 1.98        | 500       |          |

Note:

- For the DDR particles required by the K230, the power supply needs to be in the same power network as the main chip power supply.
- When voltage accuracy requirements and current requirements are met, modules with the same voltage requirements can use the same voltage source. For applications where accuracy is not required, analog modules such as ADCs can also be isolated and connected to the power supply used by digital modules.
- The K230 integrates DDR_Vref power to the chip DDR controller, and for external particles, the VREF power supply reference design of LPDDR3 is shown in Figure 3-39

![Figure 3-39 LPDDR3 particle Vref circuit]（../../zh/00_hardware/images/HDG/image051.png)
Figure 3-39 LPDDR3 particle Vref circuit

Resistors with an accuracy of ±1% are recommended for voltage divider resistors.
The external particle VREF power supply reference design for LPDDR4 is shown in Figure 3-40.

![Figure 3-40 LPDDR4 particle Vref circuit]（../../zh/00_hardware/images/HDG/image052.png)
Figure 3-40 LPDDR4 particle Vref circuit

The reference design of the K230D's DDR module VREF power supply is shown in Figure 3-41

![Figure 3-41 K230D version DDR Vref circuit]（../../zh/00_hardware/images/HDG/image053.png)
Figure 3-41 K230D version DDR Vref circuit

#### 3.8.4 Dynamic voltage regulation

The K230's CPU and KPU power supplies support dynamic voltage regulation to ensure both high performance and low power consumption.
The adjustable voltage nodes of the CPU are shown in Table 3-7

| Voltage node    | Voltage(V) |
| ----------- | ------- |
| V_typical   | 0.8     |
| V_high      | 0.9     |
| V_ultrahigh | 1.0     |
| V_low       | 0.7     |
| V_retention | 0.48    |

Table 3-8 CPU adjustable voltage nodes

Among them, V_retention is the voltage node for the DDR retention function.
The adjustable voltage nodes of the KPU are shown in Table 3-8

| Voltage node    | Voltage(V) |
| ----------- | ------- |
| V_typical   | 0.8     |
| V_high      | 0.9     |
| V_ultrahigh | 1.0     |
| V_low       | 0.7     |

Table 3-9 KPU adjustable voltage nodes

## 4. PCB design recommendations

### 4.1 High-speed PCB design recommendations

#### 4.1.1 DDR design

Impedance control: DDR single wire 60Ω, differential (clock CLK, data DQS) 120Ω;
Crosstalk requirements: Follow the 3W principle
Constant length requirements: the number of vias of the same type of signal line is consistent;
The length of the DDR trace in the substrate is shown in Table 4-1, which must be considered when routing the PCB to ensure that the sum of the inner and outer traces meets the equal length requirements.
PCB design strongly recommends referring to the design of the K230 EVB, including the selection and placement of traces and capacitors.

| Pin number | Pin name         | Length(μm) | Length (mil) |
| -------- | ---------------- | --------- | --------- |
| N17      | DDR_CKE0_CKEA0   | 3725.8    | 146.8     |
| P18      | DDR_CKE1_CKEA1   | 4338.56   | 170.94    |
| T20      | DDR_CS0_CSA0     | 5839.03   | 230.06    |
| T19      | DDR_CS1_CSA1     | 5528.07   | 217.81    |
| R19      | DDR_CKP_CKAP     | 6252.24   | 246.34    |
| R20      | DDR_CKN_CKAN     | 6050.13   | 238.38    |
| N18      | DDR_NC_NC        | 3937.42   | 155.13    |
| M17      | DDR_NC_NC        | 1925.8    | 75.88     |
| P19      | DDR_CA9_CAA5     | 5809.3    | 228.89    |
| M18      | DDR_CA8_CAA4     | 4033.87   | 158.93    |
| N20      | DDR_CA7_CAA3     | 4888.23   | 192.6     |
| N19      | DDR_CA6_CAA2     | 4415.08   | 173.95    |
| L16      | DDR_CA5_CAA1     | 2171.4    | 85.55     |
| M19      | DDR_CA4_CAA0     | 4599.65   | 181.23    |
| L17      | DDR_CA3_NC       | 2258.98   | 89        |
| M20      | DDR_CA2_NA       | 4190.42   | 165.1     |
| L20      | DDR_CA1_NC       | 5108.55   | 201.28    |
| K20      | DDR_CA0_NC       | 4832.33   | 190.39    |
| L18      | DDR_ODT_NC       | 3849.11   | 151.65    |
| J18      | DDR_NC_CKEB0     | 2599.43   | 102.42    |
| J17      | DDR_NC_CKEB1     | 2792.84   | 110.04    |
| J19      | DDR_NC_CSB1      | 4018.49   | 158.33    |
| J20      | DDR_NC_CSB0      | 4941.35   | 194.69    |
| G20      | DDR_NC_CKBP      | 5403.63   | 212.9     |
| F20      | DDR_NC_CKBN      | 5418.33   | 213.48    |
| H18      | DDR_NC_NC        | 4350.39   | 171.41    |
| H19      | DDR_NC_NC        | 4900.25   | 193.07    |
| E20      | DDR_NC_CAB0      | 5468.25   | 215.45    |
| G19      | DDR_NC_CAB1      | 4067.91   | 160.28    |
| G18      | DDR_NC_CAB2      | 3807.29   | 150.01    |
| H17      | DDR_NC_CAB3      | 3113.45   | 122.67    |
| F17      | DDR_NC_CAB4      | 2757.73   | 108.65    |
| F19      | DDR_NC_CAB5      | 4558.27   | 179.6     |
| D20      | DDR_NC_NC        | 6535.69   | 257.51    |
| G17      | DDR_NC_NC        | 3477.72   | 137.02    |
| D19      | DDR_NC_NC        | 5257.59   | 207.15    |
| F18      | DDR_NC_NC        | 4584.72   | 180.64    |
| C20      | DDR_NC_NC        | 6979.27   | 274.98    |
| U17      | DDR_DQ29_DQA7    | 4829.45   | 190.28    |
| Y18      | DDR_DQ28_DQA6    | 6467.43   | 254.82    |
| V18      | DDR_DQ25_DQA5    | 5047.5    | 198.87    |
| W18      | DDR_DQ24_DQA4    | 5267.44   | 207.54    |
| Y16      | DDR_DQ27_DQA3    | 5846.86   | 230.37    |
| V16      | DDR_DQ26_DQA2    | 4311.64   | 169.88    |
| T16      | DDR_DQ30_DQA1    | 3576.39   | 140.91    |
| U16      | DDR_DQ31_DQA0    | 3132.83   | 123.43    |
| V17      | DDR_DM3_DMIA0    | 4110.44   | 161.95    |
| W17      | DDR_DQS3P_DQSA0P | 6342.48   | 249.89    |
| Y17      | DDR_DQS3N_DQSA0N | 6135.17   | 241.73    |
| R17      | DDR_DQ10_DQA8    | 4018.24   | 158.32    |
| T18      | DDR_DQ12_DQA9    | 5760.1    | 226.95    |
| R18      | DDR_DQ8_DQA10    | 4540.62   | 178.9     |
| U20      | DDR_DQ13_DQA11   | 5625.11   | 221.63    |
| W19      | DDR_DQ11_DQA12   | 6897.92   | 271.78    |
| U18      | DDR_DQ14_DQA13   | 4908.14   | 193.38    |
| P16      | DDR_DQ9_DQA14    | 2036.92   | 80.25     |
| T17      | DDR_DQ15_DQA15   | 4492.07   | 176.99    |
| P17      | DDR_DM1_DMIA1    | 4129.14   | 162.69    |
| V20      | DDR_DQS1P_DQSA1P | 7005.11   | 276       |
| V19      | DDR_DQS1N_DQSA1N | 6768.98   | 266.7     |
| C17      | DDR_DQ0_DQB4     | 4038.16   | 159.1     |
| D16      | DDR_DQ1_DQB1     | 3663.33   | 144.34    |
| D17      | DDR_DQ2_DQB0     | 4242.29   | 167.15    |
| C18      | DDR_DQ3_DQB5     | 5598.19   | 220.57    |
| E18      | DDR_DQ4_DQB2     | 3830.51   | 150.92    |
| E17      | DDR_DQ5_DQB3     | 4273.06   | 168.36    |
| B19      | DDR_DQ6_DQB7     | 6879.01   | 271.03    |
| C19      | DDR_DQ7_DQB6     | 6640.84   | 261.65    |
| D18      | DDR_DM0_DMIB0    | 5275.38   | 207.85    |
| B18      | DDR_DQS0P_DQSB0P | 6516.79   | 256.76    |
| A18      | DDR_DQS0N_DQSB0N | 6628.66   | 261.17    |
| C14      | DDR_DQ16_DQB11   | 2966.98   | 116.9     |
| D14      | DDR_DQ20_DQB8    | 2708.03   | 106.7     |
| B14      | DDR_DQ17_DQB10   | 4486.79   | 176.78    |
| A14      | DDR_DQ21_DQB9    | 5608.52   | 220.98    |
| A17      | DDR_DQ19_DQB14   | 5037.71   | 198.49    |
| B16      | DDR_DQ23_DQB15   | 4419.48   | 174.13    |
| C16      | DDR_DQ18_DQB13   | 4381.95   | 172.65    |
| B17      | DDR_DQ22_DQB12   | 5515.88   | 217.33    |
| C15      | DDR_DM2_DMIB1    | 4509.87   | 177.69    |
| B15      | DDR_DQS2P_DQSB1P | 4623.9    | 182.18    |
| A15      | DDR_DQS2N_DQSB1N | 4942.59   | 194.74    |

Table 4-1 Chip internal DDR trace length

##### LPDDR3 part

- 数据线内部等长要求:(DQ to DQS domain)DQS_P/N and DQ [7:0] & DM for each byte lane, the length of DQ = DQS +/- 10ps
- Address line internal isometric requirements: (CS, ODT, CKE, CMD, ADD TO CK/CK#)
- When routing CK_P/N and CA signals for the memory interface, the length of the CA = CK +/- 10ps
- DQS与CK之间的等长要求：（DQS to CK domain）When routing DQS for each byte lane, the length of each DQS pair must be (CK – 85ps) <= DQS <= CK

##### LPDDR4 part

- 数据线内部等长要求:DQS_P/N and DQ [7:0] & DM for each byte lane, the length of DQ = DQS +/- 10ps
- 地址线内部等长要求：（CS, ODT, CKE, Cmd, Add to CK/CK#）When routing CK_P/N and CA signals for the memory interface, the length of the CA = CK +/- 10ps
- DQS与CK之间的等长要求：When routing DQS for each byte lane, the length of each DQS pair must be (CK – 60ps) <= DQS <= CK

#### 4.1.2 USB 2.0 design

- Impedance control: differential 90Ω.
- The differential pair does not exceed 4ps within the skew, and the maximum allowable number of vias does not exceed 6.

#### 4.1.3 MIPI design

- Impedance control: MIPI_DSI differential 100Ω, MIPI_CSI differential 100Ω
- The equal length within the line pair is controlled at 0.3mm.
