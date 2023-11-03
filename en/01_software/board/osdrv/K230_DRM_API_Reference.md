# K230_DRM_API_Reference

![cover](../../../../zh/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

This document mainly introduces the DRM driver and its user-mode interface libdrm library

### Reader object

This document is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate |
| --- | --- |
| DRM | Direct Rendering Manager |
| KMS | Kernel Mode Setting
| GEM | Graphics Execution Manager

### Revision history

| Document version number | Modify the description | Author | date |
| --- | --- | --- | --- |
| V1.0 | Initial edition | Author | 2023/06/29 |

## 1. Introduction to DRM

DRM is the management architecture responsible for interacting with the graphics card in the Linux kernel, and user programs can easily use the API provided by DRM to achieve display control, 3D rendering, video encoding and decoding, GPU computing and other work

### 1.1 DRM architecture features

DRM is the mainstream graphics display framework in the current Linux kernel, compared with the traditional FB architecture, it has the following characteristics:

1. DRM architecture natively supports multi-layer synthesis, FB schema natively does not support multi-layer synthesis
1. The DRM architecture natively supports VSYNC, DMA_BUF, and Fence mechanisms
1. The DRM architecture manages rendering and display drivers in a unified manner, making software development and maintenance simpler

### 1.2 DRM architecture composition

From the overall architecture, DRM is mainly divided into three parts:

- libdrm

    libdrm encapsulates the underlying interface and provides a common API interface to user patterns

    libdrm also provides a modetest program internally for querying the details of DRM devices, as well as basic display testing
- KMS

    KMS stands for Kernel Mode Settings, which mainly sets display resolution, color space, refresh rate, and display buffer switching and multilayer compositing
- GEM

    Memory management, responsible for memory allocation and release

## 2. ModeTest instructions

modetest is a test program provided by libdrm that can query the details of DRM devices while also performing basic display tests

### 2.1 Query K230 DRM details

The specific instructions are as follows:

```sh
[root@canaan ~ ]#modetest -M canaan-drm
Encoders:
id      crtc    type    possible crtcs  possible clones
37      36      DSI     0x00000001      0x00000001

Connectors:
id      encoder status          name            size (mm)       modes   encoders
38      37      connected       DSI-1           68x120          1       37
  modes:
        index name refresh (Hz) hdisp hss hse htot vdisp vss vse vtot
  #0 1080x1920 30.00 1080 1310 1330 1350 1920 1925 1931 1939 78529 flags: ; type: preferred, driver
  props:
        1 EDID:
                flags: immutable blob
                blobs:

                value:
        2 DPMS:
                flags: enum
                enums: On=0 Standby=1 Suspend=2 Off=3
                value: 0
        5 link-status:
                flags: enum
                enums: Good=0 Bad=1
                value: 0
        6 non-desktop:
                flags: immutable range
                values: 0 1
                value: 0
        4 TILE:
                flags: immutable blob
                blobs:

                value:

CRTCs:
id      fb      pos     size
36      0       (0,0)   (1080x1920)
  #0 1080x1920 30.00 1080 1310 1330 1350 1920 1925 1931 1939 78529 flags: ; type: preferred, driver
  props:
        24 VRR_ENABLED:
                flags: range
                values: 0 1
                value: 0
        28 GAMMA_LUT:
                flags: blob
                blobs:

                value:
        29 GAMMA_LUT_SIZE:
                flags: immutable range
                values: 0 4294967295
                value: 256

Planes:
id      crtc    fb      CRTC x,y        x,y     gamma size      possible crtcs
31      0       0       0,0             0,0     0               0x00000001
  formats: NV12 NV21 NV16 NV61
  props:
        8 type:
                flags: immutable enum
                enums: Overlay=0 Primary=1 Cursor=2
                value: 0
32      0       0       0,0             0,0     0               0x00000001
  formats: AR24 AR12 AR15 RG24 RG16
  props:
        8 type:
                flags: immutable enum
                enums: Overlay=0 Primary=1 Cursor=2
                value: 1
33      0       0       0,0             0,0     0               0x00000001
  formats: AR24 AR12 AR15 RG24 RG16
  props:
        8 type:
                flags: immutable enum
                enums: Overlay=0 Primary=1 Cursor=2
                value: 2
34      0       0       0,0             0,0     0               0x00000001
  formats: AR24 AR12 AR15 RG24 RG16
  props:
        8 type:
                flags: immutable enum
                enums: Overlay=0 Primary=1 Cursor=2
                value: 0
35      0       0       0,0             0,0     0               0x00000001
  formats: AR24 AR12 AR15 RG24 RG16
  props:
        8 type:
                flags: immutable enum
                enums: Overlay=0 Primary=1 Cursor=2
                value: 0

Frame buffers:
id      size    pitch

[root@canaan ~ ]#

```

The above information is the K230 DRM details, here is a brief description:

| Module ID | Module name | Module description |
| --- | --- | --- |
| 37 | Encoder | none |
| 38 | Connector | none |
| 36 | CRTC | Resolution support: 1080x1920 |
| 31 | Video layer |  Color space support: NV12, NV21, NV16, NV61 |
| 32 | OSD layer |  Color space support: AR24, AR12, AR15, RG24, RG16 |
| 33 | OSD layer |  Color space support: AR24, AR12, AR15, RG24, RG16 |
| 34 | OSD layer |  Color space support: AR24, AR12, AR15, RG24, RG16 |
| 35 | OSD layer |  Color space support: AR24, AR12, AR15, RG24, RG16 |

AR24 Display ARGB8888

AR12 Display ARGB4444

AR15 Display ARGB1555

RG24 means RGB888

RG16 stands for RGB565

### The 2.2 video layer outputs smpte color bars with NV12 color space

The specific instructions are as follows:

```sh
modetest -M canaan-drm -D 0 -a -s 38@36:1080x1920-30 -P 31@36:1080x1920@NV12 -v -F smpte
```

The following figure shows the LCD display:

![Display content](../../../../zh/01_software/board/osdrv/images/modetest_video_nv12_smpte.png)

### 2.3 The OSD layer outputs tiles color bars, and the color space is AR24(ARGB8888)

The specific instructions are as follows

```sh
modetest -M canaan-drm -D 0 -a -s 38@36:1080x1920-30 -P 32@36:1080x1920@AR24 -v -F tiles
```

The following figure shows the LCD display:

![Display content](../../../../zh/01_software/board/osdrv/images/modetest_osd_ar24_tiles.png)

### 2.4 OSD layer outputs tiles color bars with a color space of RG16(RGB565)

The specific instructions are as follows:

```sh
modetest -M canaan-drm -D 0 -a -s 38@36:1080x1920-30 -P 32@36:1080x1920@RG16 -v -F tiles
```

The following figure shows the LCD display:

![Display content](../../../../zh/01_software/board/osdrv/images/modetest_osd_rg16_tiles.png)

## 3. Introduction to DRM API

### 3.1 Turn on the DRM device

```c
    fd = open("/dev/dri/card0", O_RDWR | O_CLOEXEC);
    if (fd < 0) {
        fprintf(stderr, "open card0 error \n");
        return -1;
    }

```

### 3.2 Retrieving DRM resources

```c
drmModeResPtr drmModeGetResources(int fd);

typedef struct _drmModeRes {

        int count_fbs;
        uint32_t *fbs;

        int count_crtcs;
        uint32_t *crtcs;

        int count_connectors;
        uint32_t *connectors;

        int count_encoders;
        uint32_t *encoders;

        uint32_t min_width, max_width;
        uint32_t min_height, max_height;
} drmModeRes, *drmModeResPtr;

```

An example of a code call is as follows:

```c
    res = drmModeGetResources(fd);
    if (res == NULL) {
        fprintf(stderr, "drmModeGetResources error \n");
        return -1;
    }
    conn_id = res->connectors[0];
    crtc_id = res->crtcs[0];

```

### 3.3 Enable or disable DRM-related features

```c
int drmSetClientCap(int fd, uint64_t capability, uint64_t value);
```

An example of a code call is as follows:

```c
    ret = drmSetClientCap(fd, DRM_CLIENT_CAP_UNIVERSAL_PLANES, 1);
    if (ret) {
        fprintf(stderr, "drmSetClientCap DRM_CLIENT_CAP_UNIVERSAL_PLANES error \n");
        return -1;
    }

    ret = drmSetClientCap(fd, DRM_CLIENT_CAP_ATOMIC, 1);
    if (ret) {
        fprintf(stderr, "drmSetClientCap DRM_CLIENT_CAP_ATOMIC error \n");
        return -1;
    }
```

### 3.4 Retrieving layer resources

```c
drmModePlaneResPtr drmModeGetPlaneResources(int fd);

typedef struct _drmModePlaneRes {
        uint32_t count_planes;
        uint32_t *planes;
} drmModePlaneRes, *drmModePlaneResPtr;

```

An example of a code call is as follows:

```c
    plane_res = drmModeGetPlaneResources(fd);
    if (plane_res == NULL) {
        fprintf(stderr, "drmModeGetPlaneResources error \n");
        return -1;
    }
    plane_id = plane_res->planes[1];

```

In K230 DRM, the layer correspondence is as follows:

plane_res->plans[0] stand for Video layer

plane_res->plans[1] to plane_res->plans[4] stand for OSD layer

### 3.5 Obtaining Connectors

```c
drmModeConnectorPtr drmModeGetConnector(int fd, uint32_t connector_id);

typedef struct _drmModeConnector {
        uint32_t connector_id;
        uint32_t encoder_id; /**< Encoder currently connected to */
        uint32_t connector_type;
        uint32_t connector_type_id;
        drmModeConnection connection;
        uint32_t mmWidth, mmHeight; /**< HxW in millimeters */
        drmModeSubPixel subpixel;

        int count_modes;
        drmModeModeInfoPtr modes;

        int count_props;
        uint32_t *props; /**< List of property ids */
        uint64_t *prop_values; /**< List of property values */

        int count_encoders;
        uint32_t *encoders; /**< List of encoder ids */
} drmModeConnector, *drmModeConnectorPtr;

```

An example of a code call is as follows:

```c
    conn = drmModeGetConnector(fd, conn_id);
    if (conn == NULL) {
        fprintf(stderr, "drmModeGetConnector error \n");
        return -1;
    }

```

### 3.6 Apply for DRM DUMB buffer

An example of a code call is as follows:

```c
    creq.width = 1080;
    creq.height = 1920;
    creq.bpp = 32;
    creq.fourcc = DRM_FORMAT_ARGB8888;
    ret = drmIoctl(fd, DRM_IOCTL_MODE_CREATE_DUMB, &creq);
    if (ret < 0) {
        fprintf(stderr, "cannot create dumb buffer (%d): %m\n",
            errno);
        return -errno;
    }

```

### 3.7 Submit DRM Requests

An example of a code call is as follows:

```c
int drmModeAtomicCommit(int fd,
                   drmModeAtomicReqPtr req,
                   uint32_t flags,
                   void *user_data);

```

## 4. Precautions

1. K230 DRM development and testing rely on LCD screens

1. K230 DRM internal module ID is not static, we should according to the actual ID of each module
