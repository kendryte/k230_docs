# K230 Power Management Usage Guide

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

This document describes the K230 platform power management framework and how to use power control.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate |
| ---- | ---- |
|      |      |
|      |      |

### Revision history

| Document version number | Modify the description | Author | date |
| --- | --- | --- | --- |
| V1.0 | Initial edition | Zhang Tao | 2023/07/17 |

## 1. Overview

The K230 platform power management framework is divided into big-core power management and little-core power management, and the two cores are independently controlled.
The big core (rt-smart) mainly controls CPU1, AI module, display module, multimedia module, etc., and the little core (linux) mainly controls CPU0.
All power domains and clocks are enabled by default after the chip is powered on, and in order to reduce power consumption, the following power domains and clocks are turned off during the uboot-SPL phase:

1. KPU Power、KPU clk、KPU aclk
1. VPU Power、VPU clk、VPU aclk、VPU cfgclk
1. DPU Power、DPU clk、DPU aclk、DPU pclk
1. DISP Power
1. mclk

At the same time, each device driver is responsible for the corresponding clock and power domain management, when the user turns on the device, the driver should open the power domain and clock, when the user turns off the device, the driver should turn off the clock and power domain. For devices that do not support power domain management, only the clock needs to be controlled.

## 2. Big core power consumption control

### 2.1 Introduction to the control framework

#### 2.1.1 Power Management Domains

The power control of big cores mainly revolves around several power management domains:

1. CPU1
1. KPU
1. DPU
1. VPU
1. DISP

Each power management domain can set the frequency separately, where CPU1 and KPU also support DVFS, and other power management domains only support setting frequency. The power management domain supports frequency as built-in drivers, and users can change it according to their actual scenarios.

#### 2.1.2 Control Policies

Each power management domain can set the power control policy separately, which is divided into four policies:

1. Manual mode, where the user can manually configure the frequency by invoking the interface in the program
1. Performance mode, which locks the highest frequency
1. Power saving mode to lock the lowest frequency
1. Auto mode, automatically switch frequency according to load (only CPU1 supported)

#### 2.1.3 Thermal Protection

Power control supports two levels of thermal protection, the first stage is to limit the frequency of the module after the specified temperature is exceeded, and the second stage is to force the module to shut down the power domain after the specified temperature is exceeded, both levels support user configuration.

#### 2.1.4 Power Supply and Clock

Power control supports manual power-up and down and clock control for each power management domain, users generally do not need to call manually, the device driver will turn on the power and clock when using the device, and the device driver will turn off the power and clock when the device is turned off.

#### 2.1.5 CPU1

The CPU supports 4 strategies: `MANUAL_MODE`, `PERFORMANCE_MODE`, `ENERGYSAVING_MODE`, `AUTO_MODE`

For the current CPU 1 power consumption optimization of door lock and dictionary pen POC, it mainly adopts manual mode, and the user sets the high frequency before the program segment with a large amount of calculation, and sets it to low frequency after running. For multi-process or multithreaded apps, each app can lock the minimum run frequency.
You can tune your application to achieve optimal power consumption by looking at CPU statistics.

#### 2.1.6 KPU

KPU supports 3 strategies: `MANUAL_MODE`, `PERFORMANCE_MODE`, `ENERGYSAVING_MODE`

KPU power consumption control is mainly by adjusting the KPU frequency and switching power supply clock, through the nncase call interface to inform the current KPU operation stage, users can control each `kd_mpi_pm_runtime_runstage`module clock and power supply through each stage, such as when AI uses KPU, you can turn on the KPU clock, immediately after the use of the clock (AI2D clock control by default by hardware automatic control). Users can also manually set the KPU frequency according to the actual scenario, set the maximum frequency if the model is required to have a high frame rate, and set a lower frequency to reduce power consumption if the frame rate is not required or can meet the requirements.

#### 2.1.7 DPU

Refer to KPU

#### 2.1.8 VPU

Refer to KPU

#### 2.1.9 DISPLAY

Display the relevant part, built-in several frequency combinations, such as 60fps, 30fps, etc., set according to different scenarios at startup, do not support frequency adjustment at runtime, only support turning off the clock and turning off the power domain.

### 2.2 Usage

The power management framework is enabled by default, all domains are initialized `MANUAL_MODE` and the frequency is the default initial value of the system, which does not affect the original system function.

#### 2.2.1 Use manual mode

Users can refer to the following process to use `MANUAL_MODE`:

1. Obtain the `kd_mpi_pm_get_profiles`frequency points supported by the power management domain through the interface
1. Set the management `kd_mpi_pm_set_governor`policy of the power management domain through the interface to manual mode
1. Set the profile sequence number of the power management domain`kd_mpi_pm_set_profile` through`kd_mpi_pm_set_profile_lock` the OR interface

#### 2.2.2 Use other modes

Users can refer to the following process to use `PERFORMANCE_MODE`, `ENERGYSAVING_MODE`, `AUTO_MODE`

1. Set the management `kd_mpi_pm_set_governor`policy of the power management domain through the interface to the appropriate mode

#### 2.2.3 Use thermal protection

1. Through the `kd_mpi_pm_set_thermal_protect`interface, set the thermal protection temperature and downclocking serial number, and reduce the frequency to the specified profile when the temperature exceeds the specified value
1. The `kd_mpi_pm_set_thermal_shutdown`thermal shutdown temperature is set through the interface, and each power management domain will force down power when the temperature exceeds the specified value

#### 2.2.4 Use custom frequencies

For example, if you need to modify the frequency supported by the CPU, you can modify`k230_sdk/src/big/mpp/kernel/pm/src/pm_domain_cpu.c` the array in the file`profiles`:

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

After modifying the array, you also need to modify the function under the same file to generate the corresponding frequency, if the `set_clock`domain supports DVFS, the user also needs to specify the voltage corresponding to each frequency, if not, it is unified to the default voltage.

The modifications of KPU, DPU, VPU are similar.

*Note:* If you need to use the CPU `AUTO_MODE` policy, modify the frequency and modify the load conversion table `load_table`.

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

Write registers for expansion or debugging

【Syntax】

```c
int kd_mpi_pm_set_reg(uint32_t reg, uint32_t val);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| reg | Register address | input |
| valley | Register data | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

Only CMU and PWR address blocks are supported

【Example】

None

#### 2.3.2 kd_mpi_pm_get_reg

【Description】

Read registers for expansion or debugging

【Syntax】

```c
int kd_mpi_pm_get_reg(uint32_t reg, uint32_t *pval);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| reg | Register address | input |
| pval | Register data | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

Only CMU and PWR address blocks are supported

【Example】

None

#### 2.3.3 kd_mpi_pm_get_profiles

【Description】

Gets the profile property of the power management domain

【Syntax】

```c
int kd_mpi_pm_get_profiles(k_pm_domain domain, uint32_t *pcount, k_pm_profile *pprofile);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| pcount | The number of attributes | Input/output |
| pprofile | attribute | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. The maximum value of \*pcount is 128
1. If \*pcount is 0, the number of profiles in the power management domain is returned, and pprofile is not used
1. When \*pcount is greater than 0 and less than a certain value, the profile property of the specified number is returned, and pprofile cannot be empty and must be greater than \*pcount
1. When \*pcount is greater than a certain value, the maximum number of profiles and the maximum number of profile properties are returned, and pprofile cannot be empty and must be greater than the maximum value of \*pcount
1. Profile is in descending order, sequence number 0 is the highest frequency, the larger the sequence number, the lower the frequency

【Example】

None

#### 2.3.4 kd_mpi_pm_get_stat

【Description】

Gets statistics for the power management domain

【Syntax】

```c
int kd_mpi_pm_get_stat(k_pm_domain domain);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Currently, only CPU power management domains are supported

【Example】

None

#### 2.3.5 kd_mpi_pm_set_governor

【Description】

Set the management policy for the power management domain

【Syntax】

```c
int kd_mpi_pm_set_governor(k_pm_domain domain, k_pm_governor governor);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| governor | Manage policies | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.6 kd_mpi_pm_get_governor

【Description】

Gets the management policy for the power management domain

【Syntax】

```c
int kd_mpi_pm_get_governor(k_pm_domain domain, k_pm_governor *pgovernor);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| pgovernor | Manage policies | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.7 kd_mpi_pm_set_profile

【Description】

Sets the current profile sequence number for the power management domain

【Syntax】

```c
int kd_mpi_pm_set_profile(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| index | profile index | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Only manual mode settings are supported
1. Negative numbers are supported, such as -1 for the penultimate profile and -2 for the penultimate profile
1. Negative numbers that are out of range are limited to the first profile
1. Positive numbers that are out of range are limited to the last profile

【Example】

None

#### 2.3.8 kd_mpi_pm_get_profile

【Description】

Gets the current profile sequence number of the power management domain

【Syntax】

```c
int kd_mpi_pm_get_profile(k_pm_domain domain, int32_t *pindex);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| pindex | profile index | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.9 kd_mpi_pm_set_profile_lock

【Description】

Sets the lowest profile sequence number for the power management domain

【Syntax】

```c
int kd_mpi_pm_set_profile_lock(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| index | profile index | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. After the setting is completed, the current profile may be larger than the set value, such as other processes setting the minimum profile to 1, the current process setting the minimum profile to 2, and the actual profile is 1
1. Other references[kd_mpi_pm_get_profile](#237-kd_mpi_pm_set_profile)

【Example】

None

#### 2.3.10 kd_mpi_pm_set_profile_unlock

【Description】

Clear the lowest profile sequence number in the power management domain

【Syntax】

```c
int kd_mpi_pm_set_profile_unlock(k_pm_domain domain, int32_t index);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| index | profile index | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.11 kd_mpi_pm_set_thermal_protect

【Description】

Set up power management domain thermal protection throttling

【Syntax】

```c
int kd_mpi_pm_set_thermal_protect(k_pm_domain domain, int32_t temp, int32_t index);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| temp | Temperature in 0.01°C | input |
| index | profile index | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Thermal protection settings are only supported in CPU and KPU power management domains

【Example】

None

#### 2.3.12 kd_mpi_pm_get_thermal_protect

【Description】

Obtain a power management domain thermally protected throttling configuration

【Syntax】

```c
int kd_mpi_pm_get_thermal_protect(k_pm_domain domain, int32_t *ptemp, int32_t *pindex);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| ptemp | Temperature in 0.01°C | output |
| pindex | profile index | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. Thermal protection settings are only supported in CPU and KPU power management domains

【Example】

None

#### 2.3.13 kd_mpi_pm_set_thermal_shutdown

【Description】

Set the thermal shutdown temperature

【Syntax】

```c
int kd_mpi_pm_set_thermal_shutdown(int32_t temp);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| temp | Temperature in 0.01°C | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.14 kd_mpi_pm_get_thermal_shutdown

【Description】

Gets the thermal shutdown temperature

【Syntax】

```c
int kd_mpi_pm_get_thermal_shutdown(int32_t *ptemp);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| ptemp | Temperature in 0.01°C | output |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.15 kd_mpi_pm_set_clock

【Description】

Set the power management domain clock

【Syntax】

```c
int kd_mpi_pm_set_clock(k_pm_domain domain, bool enable);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| enable | switch | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.16 kd_mpi_pm_set_power

【Description】

Set the power management domain power

【Syntax】

```c
int kd_mpi_pm_set_power(k_pm_domain domain, bool enable);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| domain | Power management domain | input |
| enable | switch | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

None

【Example】

None

#### 2.3.17 kd_mpi_pm_runtime_runstage

【Description】

Set the nncase run stage, which is called by the nncase runtime

【Syntax】

```c
int kd_mpi_pm_runtime_runstage(k_runtimestage_id stage);
```

【Parameters】

| **Parameter name** | **Description** | Input/output |
| :-- | :-- | :-- |
| stage | Run stage ID | input |

【Return value】

| Return value | **Description** |
| :-- | :-- |
| 0 | succeed |
| Non-0 | Failed, the value of which is described in [error code](#25-error-codes) |

【Requirement】

- Header file: mpi_pm_api.h
- Library file: libpm.a

【Note】

1. The PM module has a built-in control strategy to `RUNTIMESTAGE_ID_KPU_START`turn on the KPU power and clock when it is turned on.
`RUNTIMESTAGE_ID_KPU_STOP`When the KPU power and clock are turned off, the user can override this function according to actual needs.

【Example】

None

### 2.4 Data Structures

#### 2.4.1 k_pm_domain

【Description】

Define the power management domain

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
| PM_DOMAIN_DISPLAY | Displays the power management domain |
| PM_DOMAIN_MEDIA | Video power management domain |
| PM_DOMAIN_NR | Total number of power management domains |

【Note】

None

#### 2.4.2 k_pm_governor

【Description】

Define power management policies

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
| PM_GOVERNOR_ENERGYSAVING | Energy saving mode |
| PM_GOVERNOR_AUTO | Automatic mode |

【Note】

None

#### 2.4.3 k_pm_profile

【Description】

Define frequency pairs, including frequency and voltage

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

【Note】

1. The frequency pairs are arranged in descending order, the sequence number 0 is the highest frequency, and the larger the serial number, the lower the frequency

#### 2.4.4 k_runtimestage_id

【Description】

Define the AI operation stage, which may use AI2D, KPU, and CPU during AI operation

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
| RUNTIMESTAGE_ID_AI2D_START | The AI2D run begins |
| RUNTIMESTAGE_ID_AI2D_STOP | The AI2D run ends |
| RUNTIMESTAGE_ID_KPU_START | KPU operation begins |
| RUNTIMESTAGE_ID_KPU_STOP | KPU operation ends |
| RUNTIMESTAGE_ID_CPU_START | CPU operation starts |
| RUNTIMESTAGE_ID_CPU_STOP | The CPU is running at the end of operation |

【Note】

None

### 2.5 Error Codes

| **Error code** | **Macro definition** | **Description** |
| :-- | :-- | :-- |
| 0xa0178003 | K_ERR_PM_ILLEGAL_PARAM | The parameter setting is invalid |
| 0xa0178004 | K_ERR_PM_EXIST | Device already exists |
| 0xa0178005 | K_ERR_PM_UNEXIST | The device does not exist |
| 0xa0178006 | K_ERR_PM_NULL_PTR | Parameter null pointer |
| 0xa0178007 | K_ERR_PM_NOT_CONFIG | The device is not configured |
| 0xa0178008 | K_ERR_PM_NOT_SUPPORT | Operation is not supported |
| 0xa0178009 | K_ERR_PM_NOT_PERM | Operation is not allowed |
| 0xa017800c | K_ERR_PM_NOMEM | Memory allocation failed |
| 0xa0178010 | K_ERR_PM_NOTREADY | The device is not ready |
| 0xa0178011 | K_ERR_PM_BADADDR | Error address |
| 0xa0178012 | K_ERR_PM_BUSY | The device is busy |

## 3. Little core power consumption control

### 3.1 Introduction to the control framework

The little core control is mainly for CPU0, and supports Linux cpu_freq, temperature protection, and cooling control.

### 3.1.1 cpu_freq

cpu_freq is a Linux standard, please refer to [the kernel documentation](https://www.kernel.org/doc/html/v5.10/cpu-freq/index.html)
