# K230 OpenCV Sensor Usage

## Environment Setup

In `k230_sdk/src/big/mpp/userapps/src`

```shell
git clone https://github.com/opencv/opencv.git
```

You can also download OpenCV first and place it in

`k230_sdk/src/big/mpp/userapps/src/opencv`

Put the patch in `k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0`

```shell
cp k230_sdk/src/big/rt-smart/userapps/opencv/v4.6.0 k230_sdk/src/big/mpp/userapps/src/opencv/patch -r
```

Copy v4.6.0 to the patch folder.

Execute the following command in the root directory of OpenCV to apply the patch:

```shell
git am ./patch/*.patch
```

Ignore the warnings.

## Compiling OpenCV

First, confirm the toolchain path in the `build.sh` path. After applying the patch, `build.sh` should be correct.

Then, create a folder named `build`, and execute the following commands in the `build` directory:

```shell
source ../build.sh
make -j
make install
```

During the compilation process, if no warning messages appear in the terminal, the compilation is successful. The compiled product will be in `build/install`, which is the OpenCV library file for the rt-smart platform.

## Compiling Examples

Modify `k230_sdk/src/big/mpp/userapps/sample/Makefile`

Change

```shell
#@cd opencv_camera_test; make || exit 1
```

to

```shell
@cd opencv_camera_test; make || exit 1
```

In the `k230_sdk` directory, execute:

```shell
make mpp-apps
```

In `k230_sdk/src/big/mpp/userapps/sample/elf`, the `opencv_camera_test.elf` file will be generated.

Transfer `opencv_camera_test.elf` to the board via SCP, NFS, or by directly copying it to a TF card.

On the big core, execute:

```shell
./opencv_camera_test.elf -D 101 -m 0 -d 0 -s 24 -c 0 -f 0 -W 1920 -H 1080
```

The captured images from the ov5647 will be displayed on the HDMI screen.
