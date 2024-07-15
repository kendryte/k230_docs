# K230 Power Consumption Management Adaptation Guide

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties about the correctness, reliability, completeness, merchantability, suitability for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy any part or all of the content of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly describes the K230 platform power consumption management framework and how to use power control.

### Target Audience

This document (this guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
| ------------ | ----------- |
|              |             |
|              |             |

### Revision History

| Document Version | Modification Description | Modifier | Date       |
| ---------------- | ------------------------- | -------- | ---------- |
| V1.0             | Initial version           | Zhang Tao | 2023/07/17 |

## 1. Overview

The K230 platform power consumption management framework is divided into large core power management and small core power management, with both cores being independently controlled.
The large core (rt-smart) mainly controls CPU1, AI module, display module, multimedia module, etc., while the small core (linux) mainly controls CPU0, etc.
After the chip is powered on, all power domains and clocks are enabled by default. To reduce power consumption, the following power domains and clocks are turned off during the uboot-spl stage:

1. KPU power, KPU clk, KPU aclk
1. VPU power, VPU clk, VPU aclk, VPU cfgclk
1. DPU power, DPU clk, DPU aclk, DPU pclk
1. DISP power, disp clk
1. mclk

At the same time, each device driver is responsible for the corresponding clock and power domain management. When the user turns on the device, the driver should turn on the power domain and clock. When the user turns off the device, the driver should turn off the clock and power domain. For devices that do not support power domain management, only clock control is required.

## 2. Large Core Power Control

### 2.1 Control Framework Introduction

#### 2.1.1 Power Management Domains

Large core power control mainly revolves around several power management domains:

1. CPU1
1. KPU
1. DPU
1. VPU
1. DISP

Each power management domain can be set to different frequencies. Among them, CPU1 and KPU also support DVFS, while other power management domains only support frequency settings. The frequencies supported by power management domains are built into the driver, and users can modify them according to their actual scenarios.

#### 2.1.2 Control Strategies

Each power management domain can be set with different power control strategies, divided into four strategies:

1. Manual mode, where the user can manually configure the frequency by calling the interface in the program.
1. Performance mode, locking the highest frequency.
1. Power-saving mode, locking the lowest frequency.
1. Automatic mode, automatically switching frequencies based on load (only supported by CPU1).

#### 2.1.3 Thermal Protection

Power control supports two levels of thermal protection. The first level limits the frequency of the module when the specified temperature is exceeded, and the second level forcibly shuts down the power domain of the module when the specified temperature is exceeded. Both levels support user configuration.

#### 2.1.4 Power and Clock

Power control supports manual power on/off and clock control for each power management domain. Users generally do not need to manually call these; the device driver will turn on the power and clock when using the device and turn off the power and clock when turning off the device.

#### 2.1.5 CPU1

The CPU supports four strategies: `Manual Mode`, `Performance Mode`, `Power-saving Mode`, `Automatic Mode`.

For the current power consumption optimization of CPU1 in door lock and dictionary pen POC, the main approach is to use manual mode. Users set a high frequency before the program segment with heavy computation and set it to a low frequency after completion. For multi-process or multi-threaded applications, each application can lock the minimum operating frequency.
You can adjust the application to achieve the best power consumption by viewing the CPU statistics.

#### 2.1.6 KPU

The KPU supports three strategies: `Manual Mode`, `Performance Mode`, `Power-saving Mode`.

KPU power control mainly adjusts the KPU frequency and switches the power clock. Through nncase, the `kd_mpi_pm_runtime_runstage` interface is called to inform the current running stage of the KPU. Users can control the clocks and power of each module according to each stage. For example, when using KPU in AI, the KPU clock can be turned on, and the clock can be turned off immediately after use (the control of the AI2D clock is automatically controlled by hardware by default). Users can also manually set the KPU frequency according to actual scenarios, such as setting the maximum frequency for high frame rate requirements and setting a lower frequency to reduce power consumption if there are no frame rate requirements or if the requirements are met.

#### 2.1.7 DPU

Refer to KPU.

#### 2.1.8 VPU

Refer to KPU.

#### 2.1.9 DISPLAY

For the display-related part, several frequency combinations are built in, such as 60fps, 30fps, etc. Set them according to different scenarios at startup. Frequency adjustment during operation is not supported, only clock and power domain shutdown are supported.

### 2.2 Usage

The power management framework is enabled by default, with all domains initially set to `Manual Mode`, and the frequency is the system default initial value, which does not affect the original system functions.

#### 2.2.1 Using Manual Mode

Users can refer to the following process to use `Manual Mode`:

1. Use the `kd_mpi_pm_get_profiles` interface to get the supported frequency points of the power management domain.
1. Use the `kd_mpi_pm_set_governor` interface to set the management strategy of the power management domain to manual mode.
1. Use the `kd_mpi_pm_set_profile` or `kd_mpi_pm_set_profile_lock` interface to set the profile number of the power management domain.

#### 2.2.2 Using Other Modes

Users can refer to the following process to use `Performance Mode`, `Power-saving Mode`, `Automatic Mode`:

1. Use the `kd_mpi_pm_set_governor` interface to set the management strategy of the power management domain to the corresponding mode.

#### 2.2.3 Using Thermal Protection

1. Use the `kd_mpi_pm_set_thermal_protect` interface to set the thermal protection temperature and downclock profile number. When the temperature exceeds the specified value, it will downclock to the specified profile.
1. Use the `kd_mpi_pm_set_thermal_shutdown` interface to set the thermal shutdown temperature. When the temperature exceeds the specified value, each power management domain will be forcibly powered off.

#### 2.2.4 Using Custom Frequencies

For example, if you need to modify the frequencies supported by the CPU, you can modify the `profiles` array in the `k230_sdk/src/big/mpp/kernel/pm/src/pm_domain_cpu.c` file:

```c
static k_pm_profile profiles[] = {
    {1.6e9, 0.8e6},
    {1.188e9, 0.7e6},
    {0.8e9, 0.68e6},
    {0.594e9, 0.66e6},
    {0.4e9, 0.64e6},
    {0.2e9, 0.62e6},
};
```

After modifying the array, you also need to modify the `set_clock` function in the same file to generate the corresponding frequency. If the domain supports DVFS, you also need to specify the voltage corresponding to each frequency. If not supported, use the default voltage uniformly.

Modifications for KPU, DPU, and VPU are similar.

*Note:* If you need to use the CPU `Automatic Mode` strategy, after modifying the frequency, you also need to modify the load conversion table `load_table`.

### 2.3 API Reference

The framework provides the following APIs:

- [kd_mpi_pm_set_reg](#231-kd_mpi_pm_set_reg)
- [kd_mpi_pm_get_reg](#232-kd_mpi_pm_get_reg)
- [kd_mpi_pm_get_profiles](#233-kd_mpi_pm_get_profiles)
- [kd_mpi_pm_get_stat](#234-kd_mpi_pm_get_stat)
- [kd_mpi_pm_set_governor](#235-kd_mpi_pm_set_governor)
- [kd_mpi_pm_get_governor](#236-kd_mpi_pm_get_governor)
- [kd_mpi_pm_set_profile](#237-kd_mpi_pm_set_profile)
- [kd_mpi_pm_get_profile](#238-kd_mpi_pm_get_profile)
- [kd_mpi_pm_set_profile_lock](#239-kd_mpi_pm_set_profile_lock)
- [kd_mpi_pm_set_profile_unlock](#2310-kd_mpi_pm_set_profile_unlock)
- [kd_mpi_pm_set_thermal_protect](#2311-kd_mpi_pm_set_thermal_protect)
- [kd_mpi_pm_get_thermal_protect](#2312-kd_mpi_pm_get_thermal_protect)
- [kd_mpi_pm_set_thermal_shutdown](#2313-kd_mpi_pm_set_thermal_shutdown)
- [kd_mpi_pm_get_thermal_shutdown](#2314-kd_mpi_pm_get_thermal_shutdown)
- [kd_mpi_pm_set_clock](#2315-kd_mpi_pm_set_clock)
- [kd_mpi_pm_set_power](#2316-kd_mpi_pm_set_power)
- [kd_mpi_pm_runtime_runstage](#2317-kd_mpi_pm_runtime_runstage)

#### 2.3.1 kd_mpi_pm_set_reg

【Description】

Write to the register, used for extension or debugging.

【Syntax】

```c
int kd_mpi_pm_set_reg(uint32_t reg, uint32_t val);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| ------------------ | --------------- | ------------ |
| reg                | Register address | Input        |
| val                | Register data    | Input        |

【Return Value】

| Return Value | **Description** |
| ------------ | --------------- |
| 0            | Success         |
| Non-zero     | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

Only supports CMU, PWR address segments.

【Example】

None

#### 2.3.2 kd_mpi_pm_get_reg

【Description】

Read the register, used for extension or debugging.

【Syntax】

```c
int kd_mpi_pm_get_reg(uint32_t reg, uint32_t *pval);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| ------------------ | --------------- | ------------ |
| reg                | Register address | Input        |
| pval               | Register data    | Output       |

【Return Value】

| Return Value | **Description** |
| ------------ | --------------- |
| 0            | Success         |
| Non-zero     | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

Only supports CMU, PWR address segments.

【Example】

None

#### 2.3.3 kd_mpi_pm_get_profiles

【Description】

Get the profile attributes of the power management domain.

【Syntax】

```c
int kd_mpi_pm_get_profiles(k_pm_domain domain, uint32_t *pcount, k_pm_profile *pprofile);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| ------------------ | --------------- | ------------ |
| domain             | Power management domain | Input        |
| pcount             | Number of attributes    | Input/Output |
| pprofile           | Attributes              | Output       |

【Return Value】

| Return Value | **Description** |
| ------------ | --------------- |
| 0            | Success         |
| Non-zero     | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. \*pcount maximum value is 128.
1. When \*pcount is 0, it returns the number of profiles in the power management domain, pprofile is not used.
1. When \*pcount is greater than 0 and less than a certain value, it returns the specified number of profile attributes, pprofile cannot be null and must be larger than \*pcount.
1. When \*pcount is greater than a certain value, it returns the maximum number of profiles and the maximum number of profile attributes, pprofile cannot be null and must be larger than the maximum value of \*pcount.
1. Profiles are arranged in descending order, with index 0 being the highest frequency, and the larger the index, the lower the frequency.

【Example】

None

#### 2.3.4 kd_mpi_pm_get_stat

【Description】

Get the statistical information of the power management domain.

【Syntax】

```c
int kd_mpi_pm_get_stat(k_pm_domain domain);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| ------------------ | --------------- | ------------ |
| domain             | Power management domain | Input        |

【Return Value】

| Return Value | **Description** |
| ------------ | --------------- |
| 0            | Success         |
| Non-zero     | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Currently, only the CPU power management domain is supported.

【Example】

None

#### 2.3.5 kd_mpi_pm_set_governor

【Description】

Set the management strategy of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_governor(k_pm_domain domain, k_pm_governor governor);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| governor | Management strategy | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.6 kd_mpi_pm_get_governor

【Description】

Get the management strategy of the power management domain.

【Syntax】

```c
int kd_mpi_pm_get_governor(k_pm_domain domain, k_pm_governor *pgovernor);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| pgovernor | Management strategy | Output |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.7 kd_mpi_pm_set_profile

【Description】

Set the current profile index of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_profile(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| index | Profile index | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Only supports manual mode.
1. Supports negative numbers, e.g., -1 represents the last profile, -2 represents the second last profile.
1. Negative numbers out of range will be limited to the first profile.
1. Positive numbers out of range will be limited to the last profile.

【Example】

None

#### 2.3.8 kd_mpi_pm_get_profile

【Description】

Get the current profile index of the power management domain.

【Syntax】

```c
int kd_mpi_pm_get_profile(k_pm_domain domain, int32_t *pindex);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| pindex | Profile index | Output |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.9 kd_mpi_pm_set_profile_lock

【Description】

Set the minimum profile index of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_profile_lock(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| index | Profile index | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. After setting, the current profile may be greater than the set value. For example, if another process sets the minimum profile to 1, and the current process sets the minimum profile to 2, the actual profile will be 1.
1. Refer to [kd_mpi_pm_set_profile](#237-kd_mpi_pm_set_profile) for other details.

【Example】

None

#### 2.3.10 kd_mpi_pm_set_profile_unlock

【Description】

Clear the minimum profile index of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_profile_unlock(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| index | Profile index | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.11 kd_mpi_pm_set_thermal_protect

【Description】

Set the thermal protection downclocking for the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_thermal_protect(k_pm_domain domain, int32_t temp, int32_t index);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| temp | Temperature, unit: 0.01℃ | Input |
| index | Profile index | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Only CPU and KPU power management domains support thermal protection settings.

【Example】

None

#### 2.3.12 kd_mpi_pm_get_thermal_protect

【Description】

Get the thermal protection downclocking configuration of the power management domain.

【Syntax】

```c
int kd_mpi_pm_get_thermal_protect(k_pm_domain domain, int32_t *ptemp, int32_t *pindex);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| ptemp | Temperature, unit: 0.01℃ | Output |
| pindex | Profile index | Output |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Only CPU and KPU power management domains support thermal protection settings.

【Example】

None

#### 2.3.13 kd_mpi_pm_set_thermal_shutdown

【Description】

Set the thermal shutdown temperature.

【Syntax】

```c
int kd_mpi_pm_set_thermal_shutdown(int32_t temp);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| temp | Temperature, unit: 0.01℃ | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.14 kd_mpi_pm_get_thermal_shutdown

【Description】

Get the thermal shutdown temperature.

【Syntax】

```c
int kd_mpi_pm_get_thermal_shutdown(int32_t *ptemp);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| ptemp | Temperature, unit: 0.01℃ | Output |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.15 kd_mpi_pm_set_clock

【Description】

Set the clock of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_clock(k_pm_domain domain, bool enable);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| enable | Enable/Disable | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.16 kd_mpi_pm_set_power

【Description】

Set the power of the power management domain.

【Syntax】

```c
int kd_mpi_pm_set_power(k_pm_domain domain, bool enable);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| domain | Power management domain | Input |
| enable | Enable/Disable | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.17 kd_mpi_pm_runtime_runstage

【Description】

Set the runtime stage for nncase, called by nncase runtime.

【Syntax】

```c
int kd_mpi_pm_runtime_runstage(k_runtimestage_id stage);
```

【Parameters】

| **Parameter Name** | **Description** | Input/Output |
| :-- | :-- | :-- |
| stage | Runtime stage ID | Input |

【Return Value】

| Return Value | **Description** |
| :-- | :-- |
| 0 | Success |
| Non-zero | Failure, see [Error Codes](#25-error-codes) for its value |

【Requirements】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. The PM module has a built-in control strategy. It turns on the KPU power and clock at `RUNTIMESTAGE_ID_KPU_START`, and turns off the KPU power and clock at `RUNTIMESTAGE_ID_KPU_STOP`. Users can override this function according to their actual needs.

【Example】

None

### 2.4 Data Structures

#### 2.4.1 k_pm_domain

【Description】

Define power management domains.

【Definition】

```C
typedef enum {
    PM_DOMAIN_CPU,
    PM_DOMAIN_KPU,
    PM_DOMAIN_DPU,
    PM_DOMAIN_VPU,
    PM_DOMAIN_DISPLAY,
    PM_DOMAIN_MEDIA,
    PM_DOMAIN_NR,
} k_pm_domain;
```

【Members】

| **Member Name** | **Description** |
| :-: | :-: |
| PM_DOMAIN_CPU | CPU power management domain |
| PM_DOMAIN_KPU | KPU power management domain |
| PM_DOMAIN_DPU | DPU power management domain |
| PM_DOMAIN_VPU | VPU power management domain |
| PM_DOMAIN_DISPLAY | Display power management domain |
| PM_DOMAIN_MEDIA | Media power management domain |
| PM_DOMAIN_NR | Total number of power management domains |

【Notes】

None

#### 2.4.2 k_pm_governor

【Description】

Define power management strategies.

【Definition】

```C
typedef enum {
    PM_GOVERNOR_MANUAL,
    PM_GOVERNOR_PERFORMANCE,
    PM_GOVERNOR_ENERGYSAVING,
    PM_GOVERNOR_AUTO,
} k_pm_governor;
```

【Members】

| **Member Name** | **Description** |
| :-: | :-: |
| PM_GOVERNOR_MANUAL | Manual mode |
| PM_GOVERNOR_PERFORMANCE | Performance mode |
| PM_GOVERNOR_ENERGYSAVING | Energy-saving mode |
| PM_GOVERNOR_AUTO | Automatic mode |

【Notes】

None

#### 2.4.3 k_pm_profile

【Description】

Define frequency points, including frequency and voltage.

【Definition】

```C
typedef struct {
    int32_t freq;
    int32_t volt;
} k_pm_profile;
```

【Members】

| **Member Name** | **Description** |
| :-: | :-: |
| freq | Frequency, unit: Hz |
| volt | Voltage, unit: uV |

【Notes】

1. Frequency points are arranged in descending order, with index 0 being the highest frequency, and the larger the index, the lower the frequency.

#### 2.4.4 k_runtimestage_id

【Description】

Define AI runtime stages, which may involve AI2D, KPU, CPU during AI operation.

【Definition】

```C
typedef enum {
    RUNTIMESTAGE_ID_AI2D_START,
    RUNTIMESTAGE_ID_AI2D_STOP,
    RUNTIMESTAGE_ID_KPU_START,
    RUNTIMESTAGE_ID_KPU_STOP,
    RUNTIMESTAGE_ID_CPU_START,
    RUNTIMESTAGE_ID_CPU_STOP,
} k_runtimestage_id;
```

【Members】

| **Member Name** | **Description** |
| :-: | :-: |
| RUNTIMESTAGE_ID_AI2D_START | AI2D operation start |
| RUNTIMESTAGE_ID_AI2D_STOP | AI2D operation stop |
| RUNTIMESTAGE_ID_KPU_START | KPU operation start |
| RUNTIMESTAGE_ID_KPU_STOP | KPU operation stop |
| RUNTIMESTAGE_ID_CPU_START | CPU operation start |
| RUNTIMESTAGE_ID_CPU_STOP | CPU operation stop |

【Notes】

None

### 2.5 Error Codes

| **Error Code** | **Macro Definition** | **Description** |
| :-- | :-- | :-- |
| 0xa0178003 | K_ERR_PM_ILLEGAL_PARAM | Invalid parameter setting |
| 0xa0178004 | K_ERR_PM_EXIST | Device already exists |
| 0xa0178005 | K_ERR_PM_UNEXIST | Device does not exist |
| 0xa0178006 | K_ERR_PM_NULL_PTR | Null pointer parameter |
| 0xa0178007 | K_ERR_PM_NOT_CONFIG | Device not configured |
| 0xa0178008 | K_ERR_PM_NOT_SUPPORT | Operation not supported |
| 0xa0178009 | K_ERR_PM_NOT_PERM | Operation not permitted |
| 0xa017800c | K_ERR_PM_NOMEM | Memory allocation failed |
| 0xa0178010 | K_ERR_PM_NOTREADY | Device not ready |
| 0xa0178011 | K_ERR_PM_BADADDR | Bad address |
| 0xa0178012 | K_ERR_PM_BUSY | Device busy |

## 3. Low-Power Core Control

### 3.1 Control Framework Introduction

The low-power core control mainly targets CPU0, supporting Linux `cpu_freq`, temperature protection, and cooling control.

### 3.1.1 cpu_freq

`cpu_freq` is a Linux standard. Please refer to the [kernel documentation](https://www.kernel.org/doc/html/v5.10/cpu-freq/index.html).
