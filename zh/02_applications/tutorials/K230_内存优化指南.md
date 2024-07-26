# K230 内存优化指南

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

## 内存分析

请参考文档 [K230_内存占用分析指南.md](K230_内存占用分析指南.md)

## 内存优化

## 小核内存优化

>
> 此内容适用Linux+RT-smart双系统，RT-smart单系统请参考后面大核内存分析

### Linux模块删除

根据内存占用分析指南中ksize.py的介绍可以删除不需要的模块或配置信息例如

- 删除CONFIG_IKCONFIG/CONFIG_IKCONFIG_PROC，内核内 .config 支持，也称为IKCONFIG，允许系统管理员将内核构建时使用的配置的副本构建到内核本身中。这允许在内核运行时检查内核的配置，而不必担心编译后是否更改或清理了内核源目录。
- 删除CONFIG_KPROBES
- 删除CONFIG_ACORN_*，Acorn 是一个应用程序打包和部署框架，可简化在 Kubernetes 上运行应用程序的过程。
- 删除CONFIG_SGI_PARTITION
- 删除CONFIG_ULTRIX_PARTITION
- 删除CONFIG_IPV6
- 删除CONFIG_IP_PNP，该选项使能在内核启动时，根据内核命令行提供的信息或根据BOOTP/DHCP/RARP等协议，来自动配置设备的IP地址和路由表。
- 删除CONFIG_NET_9P，CONFIG_NET_9P是Linux内核配置选项之一，用于启用9P协议的网络文件系统支持。
- 删除CONFIG_VIRITO_NET，删除虚拟网络支持
- 删除不需要的文件系统驱动，例如使用flash ubfis时可以删除ext2、ext4、nfs、jfss、9pfs等文件系统的支持
- 删除CONFIG_FTRACE 删除FTRACE调试选项
- CONFIG_SCTION_ALIGN_4KB=y，将内核的段对齐大小改为4KB该选项可有效避免内核静态大小因段对齐占用过多的内存
- 删除SWIOTLB，该选项用来处理DMA控制器访问地址区间不足的能力，K230不需要该选项。需要在arch/riscv/Kconfig中删除`select SWIOTLB if MMU`

在当前linux代码中，可参考如下已裁剪的defconfig文件，文件所在路径：`k230_sdk/src/little/linux/arch/riscv/configs`

```shell
k230_evb_fastboot_defconfig #常规快启配置文件
k230_evb_doorlock_defconfig #适用于门锁的配置文件，门锁默认是经过了内存优化的配置
```

### lvgl显示内存优化

该项主要介绍针对lvgl如何减少程序对于显示内存的使用，以门锁poc为例，代码参考
`src/little/buildroot-ext/package/door_lock/src/ui/`

使用ARGB4444或RGB565参考门锁POC`lvgl_port/k230/lv_port_disp.cpp`中的如下代码

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

减少DRM的buffer为2，修改门锁POC`lvgl_port/k230/lv_port_disp.cpp`中的如下代码

```C
#define DRM_UI_BUF_COUNT 2
```

## 大核内存优化

>
>此内容适用Linux+RT-smart双系统及RT-smart单系统

### 内存复用

当前基于k230异构系统的sdk，多媒体业务一般被放在大核上，在大核应用程序完全启动之前，可以让大核的elf应用程序通过romfs的方式被加载到mmz的地址区间内，此方法的缺点为程序只能运行一次，当前只支持spinor flash的启动方式

在k230_sdk目录下使用 `make menuconfig` 命令配置sdk的内存分布区间，输入命令后选择`Memory configuration--->spi nor cfg part configuration`来配置。

可以参考门锁POC的配置文件`k230_sdk/configs/k230_evb_doorlock_defconfig`

``` shell
CONFIG_MEM_MMZ_BASE=0x5c00000
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000 #复用mmz的地址空间
CONFIG_MEM_RTAPP_SIZE=0x2000000
```

### 多媒体内存优化

在满足程序本身的需求下，尽量减少vb的个数，优化方式为程序启动运行后，在msh命令行输入cat /proc/umap/vb查看vb的使用信息。可通过每个pool池的MinFree属性来判断vb数量的可优化上限

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

### ISP内存占用优化

启用MCM的内存动态分配功能，在使用 kd_mpi_vicap_set_dev_attr配置vicap时，需要将dev_attr.pipe_ctrl.bits.dnr3_enable设置为0。

### rt-smart系统内存优化

#### 堆内存优化

在msh命令行使用free命令和list_page命令可以获取整个系统堆内存和page内存的最大占用情况，可根据得到的最大值调整堆内存和page内存的大小。在`tools/menuconfig_to_code.sh`中，当编译门锁POC的CONFIG选项时，会将rt-smart的堆内存大小配置为4M。

``` shell
  if [ "${CONFIG_BOARD_NAME}" = "k230_evb_doorlock" ]; then RT_HW_HEAP_END_SIZE="0x400000"; fi;
```

#### page内存优化

根据优化后的堆内存的大小，rt-smart镜像本身的静态占用大小以及list_page命令得到的最大值即可获得rt-smart系统整体需要的内存大小。这个大小可通过在k230_sdk下输入`make menuconfig`来配置

## 内存优化效果

经过以上的配置优化，k230门锁POC程序只需要使用128M物理内存即可运行。门锁POC各模块占用内存的情况可参考文件`k230_sdk/configs/k230_evb_doorlock_defconfig`

``` shell
CONFIG_MEM_TOTAL_SIZE=0x8000000 #总内存使用128M
CONFIG_MEM_QUICK_BOOT_CFG_BASE=0x00000000 #uboot快启参数内存区间
CONFIG_MEM_QUICK_BOOT_CFG_SIZE=0x00040000
CONFIG_MEM_SENSOR_CFG_BASE=0x00040000 #sensor配置参数内存区间
CONFIG_MEM_SENSOR_CFG_SIZE=0x000c0000
CONFIG_MEM_IPCM_BASE=0x00100000 #核间通讯内存区间
CONFIG_MEM_IPCM_SIZE=0x00100000
CONFIG_MEM_RTT_SYS_BASE=0x0200000 #大核rt-smart使用的内存区间
CONFIG_MEM_RTT_SYS_SIZE=0x02000000
CONFIG_MEM_LINUX_SYS_BASE=0x2200000 #小核linux使用的内存区间
CONFIG_MEM_LINUX_SYS_SIZE=0x3a00000
CONFIG_MEM_AI_MODEL_BASE=0x7d00000 #AI模型使用的内存区间
CONFIG_MEM_AI_MODEL_SIZE=0x0200000
CONFIG_MEM_FACE_DATA_BASE=0x7c00000 #人脸数据使用的内存区间
CONFIG_MEM_FACE_DATA_SIZE=0x040000
CONFIG_MEM_SPECKLE_BASE=0x7c40000 #散斑数据使用的内存区间，仅OV9286使用
CONFIG_MEM_SPECKLE_SIZE=0x10000
CONFIG_MEM_MMZ_BASE=0x5c00000 #多媒体内存区间
CONFIG_MEM_MMZ_SIZE=0x2000000
CONFIG_MEM_RTAPP_BASE=0x5c00000 #rt-smart应用程序在romfs中占用的内存区间
CONFIG_MEM_RTAPP_SIZE=0x2000000
```
