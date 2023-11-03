# K230 Memory Optimization Guide

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Memory analysis

Please refer to the document [K230_Memory Usage Analysis Guide.md](K230_Memory_Analysis_Guide.md)

## Memory optimization

## Small-core memory optimization

### Linux module removal

Depending on the description ksize.py in the Memory Usage Analysis Guide, you can remove unwanted modules or configuration information, for example

- Remove CONFIG_IKCONFIG/CONFIG_IKCONFIG_PROC, in-kernel .config support, also known as IKCONFIG, allows system administrators to build a copy of the configuration used when building the kernel into the kernel itself. This allows the kernel's configuration to be checked while the kernel is running without worrying about whether the kernel source directory has been changed or cleaned up after compilation.
- Delete CONFIG_KPROBES
- Remove CONFIG_ACORN_*, Acorn is an application packaging and deployment framework that simplifies the process of running applications on Kubernetes.
- Delete CONFIG_SGI_PARTITION
- Delete CONFIG_ULTRIX_PARTITION
- Delete CONFIG_IPV6
- Remove CONFIG_IP_PNP, this option enables the automatic configuration of the device's IP address and routing table at kernel startup based on information provided by the kernel command line or according to protocols such as BOOTP/DHCP/RARP.
- Remove CONFIG_NET_9P, CONFIG_NET_9P is one of the Linux kernel configuration options to enable network file system support for the 9P protocol.
- Remove CONFIG_VIRITO_NET to remove virtual network support
- Remove unwanted file system drivers, for example, when using Flash UBFIS, you can remove file system support such as ext2, ext4, NFS, JFSS, 9PFS, etc
- UDELETE CONFIG_FTRACE REMOVES THE FTRACE DEBUGGING OPTION
- CONFIG_SCTION_ALIGN_4KB=y, change the segment alignment size of the kernel to 4KB, which effectively prevents the static size of the kernel from occupying too much memory due to segment alignment
- Removed SWIOTLB, this option is used to handle the DMA controller's ability to access address intervals, which is not required for the K230. It needs to be removed at arch/riscv/kconfig`select SWIOTLB if MMU`

In the current Linux code, you can refer to the following clipped defconfig file, the path where the file is located:`k230_sdk/src/little/linux/arch/riscv/configs`

```shell
k230_evb_fastboot_defconfig
k230_evb_doorlock_defconfig
```

### LVGL shows memory optimization

This item mainly introduces how LVGL reduces the program's use of display memory, taking door lock POC as an example, code reference`src/little/buildroot-ext/package/door_lock/src/ui/`

Use ARGB4444 or RGB565 to refer to the`lvgl_port/k230/lv_port_disp.cpp` following code in the door lock POC

  ```C
  static int disp_init(void)
  {
    if (drm_dev_setup(&drm_dev, DRM_DEV_NAME_DEFAULT))
        return -1;

    drm_get_resolution(&drm_dev, &screen_width, &screen_height);
    input_map_set(0);

    for (int i = DRM_UI_BUF_SRART_IDX; i < DRM_UI_BUF_END_IDX; i++) {
        drm_bufs[i].width = ALIGNED_UP_POWER_OF_TWO(display_width, 3);
        drm_bufs[i].height = ALIGNED_DOWN_POWER_OF_TWO(display_height, 0);
        drm_bufs[i].offset_x = (screen_width - display_width) / 2;
        drm_bufs[i].offset_y = (screen_height - display_height);
        drm_bufs[i].fourcc = DRM_FORMAT_ARGB4444;
        drm_bufs[i].bpp = 16;
        buf_mgt_reader_put(&ui_buf_mgt, (void *)i);
    }
  }
  ```

Reduce the buffer of DRM to 2, modify the`lvgl_port/k230/lv_port_disp.cpp` following code in the door lock POC

```C
#define DRM_UI_BUF_COUNT 2
```

## Big core memory optimization

### Memory multiplexing

At present, based on the SDK of K230 heterogeneous system, multimedia services are generally placed on the big core, before the big core application is fully started, the big core ELF application can be loaded into the address range of MMZ through ROMfs, the disadvantage of this method is that the program can only run once, and currently only supports the spinor flash startup mode

In the k230_sdk directory, use  the command to configure the `make menuconfig` memory distribution range of the SDK, enter the command and select`Memory configuration--->spi nor cfg part configuration` to configure.

You can refer to the configuration file of the door lock POC`k230_sdk/configs/k230_evb_doorlock_defconfig`

``` shell
CONFIG_MEM_MMZ_BASE=0x5c00000
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000
CONFIG_MEM_RTAPP_SIZE=0x2000000
```

### Multimedia memory optimization

Under the condition of meeting the needs of the program itself, minimize the number of VBs, and the optimization method is to enter cat /proc/umap/vb on the msh command line after the program is started and running. The upper limit of the number of vb that can be optimized can be judged by the MinFree attribute of each pool pool

``` shell
-----VB PUB CONFIG--------------------------------------------------------------
MaxPoolCnt
        10
-----VB SUPPLEMENT ATTR---------------------------------------------------------
Config  Size    VbCnt
1       204     21
-----COMMON POOL CONFIG---------------------------------------------------------
PoolConfId        BlkSize           Count   RemapMode
0                 8294400           5       CACHED
1                 8192              3       NONE
2                 4096              5       NOCACHE
-----MODULE COMMON MOD POOL CONFIG of [2]---------------------------------------
PoolConfId        BlkSize           Count   RemapMode
0                 4096              5       CACHED
1                 8192              3       NONE

-------------------------------------------------------------------------------------
PoolId  PhysAddr            VirtAddr            IsComm  Owner  BlkSz     BlkCnt  Free    MinFree
0       0x18001000          0xc00d1000          1       -1     8294400   5       2       2
BLK   VI    VENC  VDEC  VO    USER  AI    AREC  AENC  ADEC  AO    V_VI  V_VO  DMA   DPU
0     0     0     0     0     1     0     0     0     0     0     0     0     0     0
1     0     0     0     0     1     0     0     0     0     0     0     0     0     0
2     0     0     0     0     1     0     0     0     0     0     0     0     0     0
Sum   0     0     0     0     3     0     0     0     0     0     0     0     0     0

-------------------------------------------------------------------------------------
PoolId  PhysAddr            VirtAddr            IsComm  Owner  BlkSz     BlkCnt  Free    MinFree
1       0x1a78f000          0x0                 1       -1     8192      3       3       3

-------------------------------------------------------------------------------------
PoolId  PhysAddr            VirtAddr            IsComm  Owner  BlkSz     BlkCnt  Free    MinFree
2       0x1a796000          0xc2860000          1       -1     4096      5       5       5

-------------------------------------------------------------------------------------
PoolId  PhysAddr            VirtAddr            IsComm  Owner  BlkSz     BlkCnt  Free    MinFree
3       0x1a79c000          0xc2866000          1       2      4096      5       5       5

-------------------------------------------------------------------------------------
PoolId  PhysAddr            VirtAddr            IsComm  Owner  BlkSz     BlkCnt  Free    MinFree
4       0x1a7a2000          0x0                 1       2      8192      3       3       3

```

### ISP memory usage optimization

To enable the memory dynamic allocation feature of MCM, when using kd_mpi_vicap_set_dev_attr to configure vicap, you need to set dev_attr.pipe_ctrl.bits.dnr3_enable to 0.

### RT-Smart system memory optimization

#### Heap memory optimization

Use the free command and list_page command in the msh command line to obtain the maximum occupation of the entire system heap memory and page memory, and adjust the size of heap memory and page memory according to the maximum value obtained. In`tools/menuconfig_to_code.sh` , when compiling the CONFIG option for the door lock POC, the heap memory size of rt-smart is configured to 4M.

``` shell
  if [ "${CONFIG_BOARD_NAME}" = "k230_evb_doorlock" ]; then RT_HW_HEAP_END_SIZE="0x400000"; fi;
```

#### Page memory optimization

According to the size of the optimized heap memory, the static occupation size of the rt-smart image itself, and the maximum value obtained by list_page command, the memory size required by the rt-smart system as a whole can be obtained. This size can be configured by entering it under k230_sdk`make menuconfig`

## Memory optimization effects

After the above configuration optimization, the k230 door lock POC program only needs to use 128M physical memory to run. Please refer to the file for the memory occupied by each module of the door lock POC`k230_sdk/configs/k230_evb_doorlock_defconfig`

``` shell
CONFIG_MEM_TOTAL_SIZE=0x8000000
CONFIG_MEM_QUICK_BOOT_CFG_BASE=0x00000000
CONFIG_MEM_QUICK_BOOT_CFG_SIZE=0x00040000
CONFIG_MEM_SENSOR_CFG_BASE=0x00040000
CONFIG_MEM_SENSOR_CFG_SIZE=0x000c0000
CONFIG_MEM_IPCM_BASE=0x00100000
CONFIG_MEM_IPCM_SIZE=0x00100000
CONFIG_MEM_RTT_SYS_BASE=0x0200000
CONFIG_MEM_RTT_SYS_SIZE=0x02000000
CONFIG_MEM_LINUX_SYS_BASE=0x2200000
CONFIG_MEM_LINUX_SYS_SIZE=0x3a00000
CONFIG_MEM_AI_MODEL_BASE=0x7d00000
CONFIG_MEM_AI_MODEL_SIZE=0x0200000
CONFIG_MEM_FACE_DATA_BASE=0x7c00000
CONFIG_MEM_FACE_DATA_SIZE=0x040000
CONFIG_MEM_SPECKLE_BASE=0x7c40000
CONFIG_MEM_SPECKLE_SIZE=0x10000
CONFIG_MEM_MMZ_BASE=0x5c00000
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000
CONFIG_MEM_RTAPP_SIZE=0x2000000
```
