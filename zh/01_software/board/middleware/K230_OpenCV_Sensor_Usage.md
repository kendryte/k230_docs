# K230 OpenCV开发指南

## 环境搭建

在 k230_sdk/src/big/mpp/userapps/src 下

```shell
git clone https://github.com/opencv/opencv.git
```

也可以把opencv先下载下来。放到

`k230_sdk/src/big/mpp/userapps/src/opencv`

补丁放在 k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0

```shell
cp k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0 k230_sdk/src/big/mpp/userapps/src/opencv/patch -r
```

v4.6.0复制为patch文件夹

在 opencv 根目录执行以下命令，应用补丁

```shell
git am ./patch/*.patch
```

不用理会警告。

## 编译opencv

首先在 build.sh 路径确认工具链路径，打完patch build.sh即是正确的。

随后创建文件夹 build，在 build 目录中执行以下命令即可：

```shell
source ../build.sh
make -j
make install
```

在编译过程中，若终端未出现告警信息，则说明编译成功，编译完成的产物在 build/install 中，此文件即为 rt-smart 平台的 opencv 库文件。

## 编译例程

修改 k230_sdk/src/big/mpp/userapps/sample/Makefile

将

```shell
#@cd opencv_camera_test; make || exit 1
```

修改为

```shell
@cd opencv_camera_test; make || exit 1
```

在k230_sdk下

```shell
make mpp-apps
```

在 k230_sdk\src\big\mpp\userapps\sample\elf 下面会生成 opencv_camera_test.elf文件。

将opencv_camera_test.elf 通过scp或nfs或直接copy至TF卡的方式，移至板端。

在大核执行

```shell
./opencv_camera_test.elf -D 101 -m 0 -d 0 -s 24 -c 0 -f 0 -W 1920 -H 1080
```

会在HDMI显示上显示ov5647采集的画面。
