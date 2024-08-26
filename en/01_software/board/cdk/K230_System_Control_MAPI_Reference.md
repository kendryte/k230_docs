# K230 System Control MAPI Reference

![cover](../../../../zh/01_software/board/cdk/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliates. All or part of the products, services, or features described in this document may not be within your purchase or usage scope. Unless otherwise stipulated in the contract, the Company does not make any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference purposes only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/cdk/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No part of this document may be excerpted, copied, or disseminated in any form without the written permission of the Company.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces the functions and usage of the system control module in MAPI. The functions and usage of other modules will be discussed in their respective dedicated documents.

### Intended Audience

This document (this guide) is primarily intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviations

| Abbreviation | Description                         |
|--------------|-------------------------------------|
| mpp          | Media Process Platform              |
| vb           | video buffer                        |

### Revision History

| Document Version | Description | Author  | Date       |
|------------------|-------------|---------|------------|
| V1.0             | Initial Version | Haibo Hao | 2023/5/4  |

## 1. Overview

### 1.1 Overview

System control, based on the characteristics of the K230 chip, completes the reset and basic initialization of various hardware components. It is also responsible for establishing inter-core communication for the MPP (Media Process Platform) system and initializing and deinitializing modules such as multimedia memory management.

### 1.2 Function Description

MAPI features cross-OS calls, enabling the same API to be called on both the big and small cores of the K230 to achieve the required functionality.

For specific details on binding and memory management in MAPI, please refer to the document "K230 System Control API Reference V1.0".

## 2. API Reference

This functional module provides the following APIs:

- [2. API Reference](#2-api-reference)
  - [2.1 kd\_mapi\_sys\_init](#21-kd_mapi_sys_init)
  - [2.2 kd\_mapi\_sys\_deinit](#22-kd_mapi_sys_deinit)
  - [2.3 kd\_mapi\_media\_init](#23-kd_mapi_media_init)
  - [2.4 kd\_mapi\_media\_deinit](#24-kd_mapi_media_deinit)
  - [2.5 kd\_mapi\_alloc\_buffer](#25-kd_mapi_alloc_buffer)
  - [2.6 kd\_mapi\_free\_buffer](#26-kd_mapi_free_buffer)
  - [2.7 kd\_mapi\_sys\_get\_vb\_block](#27-kd_mapi_sys_get_vb_block)
  - [2.8 kd\_mapi\_sys\_release\_vb\_block](#28-kd_mapi_sys_release_vb_block)
- [3. Data Types](#3-data-types)
  - [3.1 k\_mapi\_mod\_id\_e](#31-k_mapi_mod_id_e)
  - [3.2 k\_mapi\_media\_config\_t](#32-k_mapi_media_config_t)
  - [3.3 k\_mapi\_media\_attr\_t](#33-k_mapi_media_attr_t)
- [4. Error Codes](#4-error-codes)

### 2.1 kd_mapi_sys_init

**Description**:

Initialize system resources and establish message communication channels between the two cores. To establish a dual-core connection, services running on each operating system need to call this interface during initialization to establish the connection, after which inter-core communication can be performed.

**Syntax**:

```c
k_s32 kd_mapi_sys_init(void);
```

**Parameters**:

None

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

This function needs to be called before calling kd_mapi_media_init.

**Example**:

None

**Related Topics**:

None

### 2.2 kd_mapi_sys_deinit

**Description**:

Deinitialize system resources and disconnect the message communication channels between the two cores.

**Syntax**:

```c
k_s32 kd_mapi_sys_deinit(void);
```

**Parameters**:

None

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

If kd_mapi_sys_init has not been called, calling this API will return success.

**Example**:

None

**Related Topics**:

None

### 2.3 kd_mapi_media_init

**Description**:

Initialize multimedia-related resources, mainly configuring the number and size of the video buffers (vb).

**Syntax**:

```c
k_s32 kd_mapi_media_init(const k_mapi_media_attr_t *media_attr);
```

**Parameters**:

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| media_attr         | Pointer to media attributes | Input           |

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

None

**Example**:

None

**Related Topics**:

None

### 2.4 kd_mapi_media_deinit

**Description**:

Deinitialize multimedia-related resources.

**Syntax**:

```c
k_s32 kd_mapi_media_deinit(void);
```

**Parameters**:

None

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

None

**Example**:

None

**Related Topics**:

None

### 2.5 kd_mapi_alloc_buffer

**Description**:

Allocate MMZ memory in user space (with cache).

**Syntax**:

```c
k_s32 kd_mapi_alloc_buffer(k_u64 *phys_addr, void **virt_addr, k_u32 len, const k_char *name);
```

**Parameters**:

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| phys_addr          | Physical address of the buffer | Output           |
| virt_addr          | Virtual address of the buffer  | Output           |
| len                | Length of the buffer           | Input            |
| name               | Name of the buffer             | Input            |

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

- The virtual address and physical address of the buffer are already mapped.
- After allocating memory, check whether the buffer is successfully allocated on the big core side via `cat /proc/umap/media-mem`.

**Example**:

None

**Related Topics**:

None

### 2.6 kd_mapi_free_buffer

**Description**:

Free MMZ memory in user space.

**Syntax**:

```c
k_s32 kd_mapi_free_buffer(k_u64 phys_addr, void *virt_addr, k_u32 len);
```

**Parameters**:

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| phys_addr          | Physical address of the buffer | Input            |
| virt_addr          | Virtual address of the buffer  | Input            |
| len                | Length of the buffer           | Input            |

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

After freeing memory, check whether the buffer is successfully released on the big core side via `cat /proc/umap/media-mem`.

**Example**:

None

**Related Topics**:

None

### 2.7 kd_mapi_sys_get_vb_block

**Description**:

Get a buffer block in user space.

**Syntax**:

```c
k_s32 kd_mapi_sys_get_vb_block(k_u32 *pool_id, k_u64 *phys_addr, k_u64 blk_size, const char* mmz_name);
```

**Parameters**:

| **Parameter Name** | **Description**                   | **Input/Output** |
|--------------------|-----------------------------------|------------------|
| pool_id            | ID of the buffer pool containing the block | Output           |
| phys_addr          | Physical address of the buffer block | Output           |
| blk_size           | Size of the buffer block          | Input            |
| mmz_name           | Name of the DDR containing the buffer pool | Input            |

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

- If the user needs to get a buffer block of a specified size from any public buffer pool, set the second parameter blk_size to the required buffer block size and specify from which DDR to get the buffer block. If there is no public buffer pool on the specified DDR, the buffer block cannot be obtained. If mmz_name is NULL, it means getting the buffer block from the public buffer pool on an unnamed DDR.
- During media initialization, if a buffer pool is created in an unnamed DDR, set mmz_name to NULL to get a buffer block of the specified size from any public buffer pool.

**Example**:

None

**Related Topics**:

None

### 2.8 kd_mapi_sys_release_vb_block

**Description**:

Release a buffer block in user space.

**Syntax**:

```c
k_s32 kd_mapi_sys_release_vb_block(k_u64 phys_addr, k_u64 blk_size);
```

**Parameters**:

| **Parameter Name** | **Description**       | **Input/Output** |
|--------------------|-----------------------|------------------|
| phys_addr          | Physical address of the buffer block | Output           |
| blk_size           | Size of the buffer block          | Input            |

**Return Values**:

| **Return Value** | **Description**                     |
|------------------|-------------------------------------|
| 0                | Success                             |
| Non-zero         | Failure, see [Error Codes](#4-error-codes) for values |

**Chip Differences**:

None

**Requirements**:

- Header file: mapi_sys_api.h
- Library file: libmapi.a

**Notes**:

After using the buffer block, this interface should be called to release the buffer block.

**Example**:

None

**Related Topics**:

None

## 3. Data Types

### 3.1 k_mapi_mod_id_e

**Description**:

Defines MAPI module IDs.

**Definition**:

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

**Members**:

None

**Notes**:

None

**Related Data Types and Interfaces**:

None

### 3.2 k_mapi_media_config_t

**Description**:

Defines the media configuration attribute structure.

**Definition**:

```C
typedef struct {
    k_vb_supplement_config vb_supp;
    k_vb_config vb_config;
} k_mapi_media_config_t;
```

**Members**:

| **Member Name** | **Description**                        |
|-----------------|----------------------------------------|
| vb_supp         | VB Supplement Information Structure, see "K230 System Control API Reference" |
| vb_config       | Video Buffer Pool Attribute Structure, see "K230 System Control API Reference" |

**Notes**:

None

**Related Data Types and Interfaces**:

None

### 3.3 k_mapi_media_attr_t

**Description**:

Defines the media initialization attribute structure.

**Definition**:

```C
typedef struct {
    k_mapi_media_config_t media_config;
} k_mapi_media_attr_t;
```

**Members**:

| **Member Name** | **Description**                  |
|-----------------|----------------------------------|
| media_config    | Media configuration attribute structure |

**Notes**:

None

**Related Data Types and Interfaces**:

None

## 4. Error Codes

Table 41

| Error Code  | Macro Definition               | **Description**                  |
|-------------|--------------------------------|----------------------------------|
| 0xb0008003  | K_MAPI_ERR_SYS_ILLEGAL_PARAM   | Parameter error                  |
| 0xb0008006  | K_MAPI_ERR_SYS_NULL_PTR        | Null pointer error               |
| 0xb0008009  | K_MAPI_ERR_SYS_NOT_PERM        | Operation not permitted          |
| 0xb0008010  | K_MAPI_ERR_SYS_NOTREADY        | Device not ready                 |
| 0xb0008012  | K_MAPI_ERR_SYS_BUSY            | System busy                      |
| 0xb000800c  | K_MAPI_ERR_SYS_NOMEM           | Memory allocation failure, such as insufficient system memory |
