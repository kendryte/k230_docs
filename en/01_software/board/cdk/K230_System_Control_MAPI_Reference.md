# K230 System Control MAPI Reference

![cover](../../../../zh/01_software/board/cdk/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/cdk/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the functions and usage of the system control module in MAPI, and the functions and usage of other modules will be discussed in their own special documents.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate                                |
|------|-------------------------------------|
| cdk  | Media Process Platform  |
| .vb   | Video buffer              |

### Revision history

| Document version number | Modify the description | Author | date     |
|------------|----------|--------|----------|
| V1.0       | Initial edition     | Haibo Hao | 2023/5/4 |

## 1. Overview

### 1.1 Overview

According to the characteristics of the k230 chip, the system control completes the reset and basic initialization of each component of the hardware, and is responsible for completing the inter-core communication establishment of the cdk (Media Process Platform media processing platform) system, the initialization and deinitialization of multimedia memory management and other modules.

### 1.2 Function Description

The feature of MAPI is cross-OS calling, and the same API can be called on both large and little cores of the K230 to achieve the required functions. The overall system architecture is shown in the figure below

For details on binding and memory management in MAPI, please refer to the document "K230 System Control API Reference V1.0"

## 2. API Reference

This function module provides the following APIs:

- [K230 System Control MAPI Reference](#k230-system-control-mapi-reference)
  - [disclaimer](#disclaimer)
  - [Trademark Notice](#trademark-notice)
  - [directory](#directory)
  - [preface](#preface)
    - [overview](#overview)
    - [Reader object](#reader-object)
    - [Definition of acronyms](#definition-of-acronyms)
    - [Revision history](#revision-history)
  - [1. Overview](#1-overview)
    - [1.1 Overview](#11-overview)
    - [1.2 Function Description](#12-function-description)
  - [2. API Reference](#2-api-reference)
    - [2.1 kd\_mapi\_sys\_init](#21-kd_mapi_sys_init)
    - [2.2 kd\_mapi\_sys\_deinit](#22-kd_mapi_sys_deinit)
    - [2.3 kd\_mapi\_media\_init](#23-kd_mapi_media_init)
    - [2.4 kd\_mapi\_media\_deinit](#24-kd_mapi_media_deinit)
    - [2.5 kd\_mapi\_alloc\_buffer](#25-kd_mapi_alloc_buffer)
    - [2.6 kd\_mapi\_free\_buffer](#26-kd_mapi_free_buffer)
    - [2.7 kd\_mapi\_sys\_get\_vb\_block](#27-kd_mapi_sys_get_vb_block)
    - [2.8 kd\_mapi\_sys\_release\_vb\_block](#28-kd_mapi_sys_release_vb_block)
  - [3. Data Type](#3-data-type)
    - [3.1 k\_mapi\_mod\_id\_e](#31-k_mapi_mod_id_e)
    - [3.2 k\_mapi\_media\_config\_t](#32-k_mapi_media_config_t)
    - [3.3 k\_mapi\_media\_attr\_t](#33-k_mapi_media_attr_t)
  - [4. Error codes](#4-error-codes)

### 2.1 kd_mapi_sys_init

【Description】

Initialize system resources and establish a message communication pipeline between the two cores. In order to establish a dual-core connection, services running on each operating system need to call this interface during initialization to establish a connection before intercore communication can take place.

【Syntax】

```c
k_s32 kd_mapi_sys_init(void );
```

【Parameters】

none

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

This function needs to be called before calling the kd_mapi_media_init

【Example】

none

【See Also】

none

### 2.2 kd_mapi_sys_deinit

【Description】

To initialize system resources, disconnect the message communication pipeline between the two cores.

【Syntax】

```c
k_s32 kd_mapi_sys_deinit(void );
```

【Parameters】

none

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

When the kd_mapi_sys_init is not called, the call to this MAPI returns success.

【Example】

none

【See Also】

none

### 2.3 kd_mapi_media_init

【Description】

Initialize multimedia related resources. Configure the number and size of VBs

【Syntax】

```c
k_s32 kd_mapi_media_init(const [k_mapi_media_attr_t](#33-k_mapi_media_attr_t) *media_attr);
```

【Parameters】

| **Parameter name**   | **Description**         | **Input/output** |
|------------|--------------|-----------|
| media_attr | Media property pointer | input      |

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

none

【Example】

none

【See Also】

none

### 2.4 kd_mapi_media_deinit

【Description】

Go and initialize multimedia related resources.

【Syntax】

```c
k_s32 kd_mapi_media_deinit(void);
```

【Parameters】

none

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

none

【Example】

none

【See Also】

none

### 2.5 kd_mapi_alloc_buffer

【Description】

Allocate memory for MMZ in user mode (with cache)

【Syntax】

```c
k_s32 kd_mapi_alloc_buffer(k_u64 *phys_addr, void **virt_addr, k_u32 len, const k_char *name);
```

【Parameters】

| **Parameter name**  | **Description**             | **Input/output** |
|-----------|------------------|-----------|
| phys_addr | The physical address of the buffer | output      |
| virt_addr | The virtual address of buffer | output      |
| only       | The length of the buffer     | input      |
| name      | The name of buffer     | input      |

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

- The virtual and physical addresses of the buffer are mapped
- After allocating memory, use cat/proc/umap/media-mem under the large kernel msh to see if the buffer is allocated successfully.

【Example】

none

【See Also】

none

### 2.6 kd_mapi_free_buffer

【Description】

Frees the memory of the MMZ in user mode.

【Syntax】

```c
k_s32 kd_mapi_free_buffer(k_u64 phys_addr, void *virt_addr, k_u32 len);
```

【Parameters】

| **Parameter name**  | **Description**             | **Input/output** |
|-----------|------------------|-----------|
| phys_addr | The physical address of the buffer | input      |
| virt_addr | The virtual address of buffer | input      |
| only       | The length of the buffer     | input      |

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

After freeing the memory, check whether the buffer is successfully freed under the large kernel side msh through cat /proc/umap/media-mem.

【Example】

none

【See Also】

none

### 2.7 kd_mapi_sys_get_vb_block

【Description】

Gets a vb block in user mode.

【Syntax】

```c
k_s32 kd_mapi_sys_get_vb_block(k_u32 \*pool_id, k_u64 \*phys_addr, k_u64 blk_size, const char\* mmz_name);
```

【Parameters】

| **Parameter name**  | **Description**                   | **Input/output** |
|-----------|------------------------|-----------|
| pool_id   | The ID number of the vb pool where the vb block resides | output      |
| phys_addr | The physical address of the vb block       | output      |
| blk_size  | The size of the vb block           | input      |
| mmz_name  | The name of the DDR where the vb pool resides  | input      |

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

- If the user needs to fetch a block of the specified size from any of the public vb pools, set parameter 2 blk_size to the desired vb block size and specify the public vb pool on which DDR to obtain the vb block from. If there is no public vb pool on the specified DDR, the vb block will not be fetched. If mmz_name equals NULL, it means that the public vb pool on an unnamed DDR fetches vb blocks
- When media initializes, if VB creates a vb pool in an unnamed DDR, it obtains a block of the specified size from any public vb pool, mmz_name set to NULL

【Example】

none

【See Also】

none

### 2.8 kd_mapi_sys_release_vb_block

【Description】

A vb block is released in user mode.

【Syntax】

```c
k_s32 kd_mapi_sys_release_vb_block(k_u64 phys_addr, k_u64 blk_size);
```

【Parameters】

| **Parameter name**  | **Description**             | **Input/output** |
|-----------|------------------|-----------|
| phys_addr | The physical address of the vb block | output      |
| blk_size  | The size of the vb block     | input      |

【Return value】

| **Return value** | **Description**                            |
|--------|---------------------------------|
| 0      | succeed                            |
| Non-0    | Failed, the value of which is described in [error code](#4-error-codes) |

【Differences】

none.

【Requirement】

- Header file: mapi_sys_api.h
- Library file: libmapi.a

【Note】

After the obtained vb block is exhausted, this interface should be called to free the vb block.

【Example】

none

【See Also】

none

## 3. Data Type

### 3.1 k_mapi_mod_id_e

【Description】

Define the MAPI module ID

【Definition】

```C

typedef enum

{

K_MAPI_MOD_SYS = 0,

K_MAPI_MOD_VI,

K_MAPI_MOD_VPROC,

K_MAPI_MOD_VENC,

K_MAPI_MOD_VDEC,

K_MAPI_MOD_VREC,

K_MAPI_MOD_VO,

K_MAPI_MOD_AI,

K_MAPI_MOD_AENC,

K_MAPI_MOD_ADEC,

K_MAPI_MOD_AREC,

K_MAPI_MOD_AO,

K_MAPI_MOD_VVI,

K_MAPI_MOD_VVO,

K_MAPI_MOD_DPU,

K_MAPI_MOD_VICAP,

K_MAPI_MOD_SENSOR,

K_MAPI_MOD_ISP,

K_MAPI_MOD_BUTT,

} k_mapi_mod_id_e;
```

【Members】

none

【Note】

none

【See Also】

none

### 3.2 k_mapi_media_config_t

【Description】

Define the media configuration attribute structure

【Definition】

```C

typedef struct {

k_vb_supplement_config vb_supp;

k_vb_config vb_config;

} k_mapi_media_config_t;
```

【Members】

| **Member Name** | **Description**                                            |
|--------------|-----------------------------------------------------|
| vb_supp      | VB Additional Information Structure, see K230 System Control API Reference    |
| vb_config    | For the video buffer pool attribute structure, see K230 System Control API Reference |

【Note】

none

【See Also】

none

### 3.3 k_mapi_media_attr_t

【Description】

Defines the media initialization attribute structure

【Definition】

```C

typedef struct {

k_mapi_media_config_t media_config;

} k_mapi_media_attr_t;
```

【Members】

| **Member Name** | **Description**           |
|--------------|--------------------|
| media_config | Media configuration attribute struct |

【Note】

none

【See Also】

none

## 4. Error codes

Table 41

| Error code   | Macro definitions                       | **Description**                         |
|------------|------------------------------|------------------------------|
| 0xb0008003 | K_MAPI_ERR_SYS_ILLEGAL_PARAM | Parameter error                     |
| 0xb0008006 | K_MAPI_ERR_SYS_NULL_PTR      | Null pointer error                   |
| 0xb0008009 | K_MAPI_ERR_SYS_NOT_PERM      | Operation is not allowed                   |
| 0xb0008010 | K_MAPI_ERR_SYS_NOTREADY      | The device is not ready                   |
| 0xb0008012 | K_MAPI_ERR_SYS_BUSY          | The system is busy                       |
| 0xb000800c | K_MAPI_ERR_SYS_NOMEM         | Failed to allocate memory, such as low system memory |
