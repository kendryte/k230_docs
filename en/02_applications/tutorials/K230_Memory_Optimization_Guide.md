# K230 Memory Optimization Guide

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company makes no express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is provided only as a guide for reference.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
No unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form without the written permission of the Company.

<div style="page-break-after:always"></div>

## Memory Analysis

Please refer to the document [K230_Memory_Usage_Analysis_Guide.md](K230_Memory_Usage_Analysis_Guide.md)

## Memory Optimization

## Small-core Memory Optimization

### Linux Module Deletion

Based on the introduction of ksize.py in the memory usage analysis guide, unnecessary modules or configuration information can be deleted, for example:

- Remove CONFIG_IKCONFIG/CONFIG_IKCONFIG_PROC: The .config support within the kernel, also known as IKCONFIG, allows system administrators to build a copy of the configuration used during kernel build into the kernel itself. This allows checking the kernel's configuration while the kernel is running without worrying about changes or cleaning the kernel source directory after compilation.
- Remove CONFIG_KPROBES
- Remove CONFIG_ACORN_*, Acorn is an application packaging and deployment framework that simplifies running applications on Kubernetes.
- Remove CONFIG_SGI_PARTITION
- Remove CONFIG_ULTRIX_PARTITION
- Remove CONFIG_IPV6
- Remove CONFIG_IP_PNP, this option enables the automatic configuration of the device's IP address and routing table based on information provided on the kernel command line or protocols like BOOTP/DHCP/RARP during kernel startup.
- Remove CONFIG_NET_9P, CONFIG_NET_9P is a Linux kernel configuration option for enabling 9P protocol network file system support.
- Remove CONFIG_VIRITO_NET, remove virtual network support
- Remove unnecessary filesystem drivers, such as removing support for ext2, ext4, nfs, jffs, 9pfs, etc., if using flash ubifs.
- Remove CONFIG_FTRACE, remove FTRACE debugging options
- Set CONFIG_SECTION_ALIGN_4KB=y to change the segment alignment size of the kernel to 4KB, effectively avoiding excessive memory usage due to segment alignment.
- Remove SWIOTLB, this option handles the capability of the DMA controller to access address ranges, which is not needed for K230. It needs to be deleted in arch/riscv/Kconfig with `select SWIOTLB if MMU`.

In the current Linux code, you can refer to the following trimmed defconfig files located at `k230_sdk/src/little/linux/arch/riscv/configs`:

```shell
k230_evb_fastboot_defconfig # Regular fastboot configuration file
k230_evb_doorlock_defconfig # Configuration file for door locks, optimized for memory by default
```

### LVGL Display Memory Optimization

This section mainly introduces how to reduce the display memory usage for LVGL, taking the door lock POC as an example. Refer to the code at `src/little/buildroot-ext/package/door_lock/src/ui/`.

Use ARGB4444 or RGB565 as referenced in the door lock POC `lvgl_port/k230/lv_port_disp.cpp` with the following code:

```C
static int disp_init(void)
{
    if (drm_dev_setup(&drm_dev, DRM_DEV_NAME_DEFAULT))
        return -1;

    drm_get_resolution(&drm_dev, &screen_width, &screen_height);
    input_map_set(0);

    for (int i = DRM_UI_BUF_START_IDX; i < DRM_UI_BUF_END_IDX; i++) {
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

Reduce the DRM buffer to 2 by modifying the door lock POC `lvgl_port/k230/lv_port_disp.cpp` with the following code:

```C
#define DRM_UI_BUF_COUNT 2
```

## Large-core Memory Optimization

### Memory Reuse

In the current K230 heterogeneous system SDK, multimedia tasks are generally placed on the large core. Before the application on the large core is fully started, the ELF application of the large core can be loaded into the MMZ address range via ROMFS. The downside of this method is that the program can only run once, and currently only supports spinor flash boot method.

Use the `make menuconfig` command in the k230_sdk directory to configure the SDK's memory distribution range. After entering the command, choose `Memory configuration--->spi nor cfg part configuration` to configure.

Refer to the door lock POC configuration file `k230_sdk/configs/k230_evb_doorlock_defconfig`.

```shell
CONFIG_MEM_MMZ_BASE=0x5c00000
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000 # Reuse MMZ address space
CONFIG_MEM_RTAPP_SIZE=0x2000000
```

### Multimedia Memory Optimization

To meet the program's needs, minimize the number of VBs. After the program starts, use the msh command to input `cat /proc/umap/vb` to check the VB usage information. The maximum optimization limit of the VB quantity can be judged by the MinFree attribute of each pool.

```shell
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

### ISP Memory Usage Optimization

Enable the dynamic memory allocation function of MCM. When configuring VICAP with kd_mpi_vicap_set_dev_attr, set dev_attr.pipe_ctrl.bits.dnr3_enable to 0.

### RT-Smart System Memory Optimization

#### Heap Memory Optimization

Use the `free` and `list_page` commands in the msh command line to get the maximum usage of the entire system heap memory and page memory. Adjust the heap memory and page memory size based on the maximum value obtained. In `tools/menuconfig_to_code.sh`, when compiling the CONFIG options of the door lock POC, the heap memory size of RT-Smart is configured to 4M.

```shell
  if [ "${CONFIG_BOARD_NAME}" = "k230_evb_doorlock" ]; then RT_HW_HEAP_END_SIZE="0x400000"; fi;
```

#### Page Memory Optimization

Based on the optimized heap memory size, the static size of the RT-Smart image itself, and the maximum value obtained from the `list_page` command, you can determine the overall memory size required by the RT-Smart system. This size can be configured by entering `make menuconfig` in the k230_sdk directory.

## Memory Optimization Results

After the above configuration optimizations, the K230 door lock POC program only needs 128M of physical memory to run. The memory usage of each module in the door lock POC can be referenced in the configuration file `k230_sdk/configs/k230_evb_doorlock_defconfig`.

```shell
CONFIG_MEM_TOTAL_SIZE=0x8000000 # Total memory usage is 128M
CONFIG_MEM_QUICK_BOOT_CFG_BASE=0x00000000 # Uboot fastboot parameter memory range
CONFIG_MEM_QUICK_BOOT_CFG_SIZE=0x00040000
CONFIG_MEM_SENSOR_CFG_BASE=0x00040000 # Sensor configuration parameter memory range
CONFIG_MEM_SENSOR_CFG_SIZE=0x000c0000
CONFIG_MEM_IPCM_BASE=0x00100000 # Inter-core communication memory range
CONFIG_MEM_IPCM_SIZE=0x00100000
CONFIG_MEM_RTT_SYS_BASE=0x0200000 # Memory range used by the large core RT-Smart
CONFIG_MEM_RTT_SYS_SIZE=0x02000000
CONFIG_MEM_LINUX_SYS_BASE=0x2200000 # Memory range used by the small core Linux
CONFIG_MEM_LINUX_SYS_SIZE=0x3a00000
CONFIG_MEM_AI_MODEL_BASE=0x7d00000 # Memory range used by AI models
CONFIG_MEM_AI_MODEL_SIZE=0x0200000
CONFIG_MEM_FACE_DATA_BASE=0x7c00000 # Memory range used by facial data
CONFIG_MEM_FACE_DATA_SIZE=0x040000
CONFIG_MEM_SPECKLE_BASE=0x7c40000 # Memory range used by speckle data, only for OV9286
CONFIG_MEM_SPECKLE_SIZE=0x10000
CONFIG_MEM_MMZ_BASE=0x5c00000 # Multimedia memory range
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000 # Memory range occupied by RT-Smart applications in ROMFS
CONFIG_MEM_RTAPP_SIZE=0x2000000
```
