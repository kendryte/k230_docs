# K230视频编解码API参考

## 概述

这个文档主要是介绍vicap中的配置文件转换成bin 的格式、为了节约vicap解析配置文件所消耗的时间

## 使用方式

下载最新的sdk、vicap 将配置文件转换成bin 的代码在如下路径：

```c
k230_sdk/src/big/mpp/userapps/sample/sample_vicap_transform_bin/
```

默认这个demo 是没有做编译的，需要自行增加demo 的配置到makefile 中

```c
@cd sample_vicap_transform_bin; make || exit 1
```

代码中主要就是调用一个api，api介绍如下：

```c
int kd_mpi_export_vicap_config_to_bin(char *path, char *config_name)
```

- path ：配置文件的路径（对应sensor 的xml、json文件的路径）。
- config_name ：配置文件的名称，可以参考 k_vicap_sensor_info 中database_name。

下边以imx335 1920x1080 的配置为例子：

```c
char *path = "/sharefs/sharefs/";
char *config_name = "imx335-1920x1080";
kd_mpi_export_vicap_config_to_bin(path, config_name);
```

运行结果如下：

```c
cfg_file is /sharefs/sharefs/imx335-1920x1080_manual.json
cfg_file is /sharefs/sharefs/imx335-1920x1080_auto.json
calib_file is /sharefs/sharefs/imx335-1920x1080_auto.json
illuminationNumber is 5 lscNumber 5 ccNumber 5 ecmNumber 3
bls num is 1 deGammaNumber is 1 cacNumber 1  dpfNumber is 1 dpccNumber is 1
ret = 409656
```

会打印要转换json 和xml 的路径，ret 的值是配置文件转换成bin文件的大小。运行结束后会在当前目录下生成一个bin 文件

```c
imx335-1920x1080_fastboot.bin           409656
```

将bin文件考到下边目录，从新编译镜像即可

```c
k230_sdk/src/big/mpp/userapps/src/sensor/config
```

烧录后，会在bin 下看见imx335-1920x1080_fastboot.bin 文件、然后在运行程序即可

```c
msh /sharefs/sharefs>ls /bin/
imx335-1920x1080_fastboot.bin
```
