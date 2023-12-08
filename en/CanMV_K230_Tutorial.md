# CanMV K230 Tutorial

![cover](../zh/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[toc]

## preface

Based on the CanMV-K230 development board, this article introduces the development process of the K230 SDK, nncase, and AI.

## Get started quickly

### Overview of the development board

The CanMV-K230 development board uses the latest generation of SoC chip K230 in the Canaan Kendryte® series AIoT chips. The chip adopts a new multi-heterogeneous unit accelerated computing architecture, integrates 2 RISC-V energy-efficient computing cores, built-in a new generation of KPU (Knowledge Process Unit) intelligent computing unit, has multi-precision AI computing power, widely supports common AI computing frameworks, and the utilization rate of some typical networks exceeds 70%.

The chip also has a variety of peripheral interfaces, as well as 2D, 2.5D and other scalar, vector, graphics and other special hardware acceleration units, which can accelerate the whole process of computing and acceleration of a variety of diverse computing tasks such as image, video, audio, and AI, and has many characteristics such as low latency, high performance, low power consumption, fast startup, and high security.

![K230_block_diagram](../zh/images/K230_block_diagram.png)

CanMV-K230 adopts a single board design and rich expansion interfaces, which greatly exerts the advantages of K230's high performance, and can be directly used in the development of various intelligent products to accelerate product landing.

### CanMV-K230 default kit

The CanMV-K230 board default kit contains the following items:

1 CanMV-K230 motherboard x 1

2 OV5647 camera x 1

3 Type-C data cable x 1

In addition, the user needs to prepare the following accessories:

1 TF card, used to flash firmware, boot system (required)

2 Display with HDMI interface and HDMI cable, the display must support 1080P30, otherwise it cannot be displayed

3 100M/1000M Ethernet cable, and wired router

### Debugging instructions

#### Serial port connection

Use the Type-C cable to connect the CanMV-K230 to the position shown below, and connect the other end of the cable to the computer.

#### Serial port debugging

##### Windows

Install the driver

CanMV-K230 comes with USB to serial port chip CH342, driver download address<https://www.wch.cn/downloads/CH343SER_EXE.html>.

Check the serial port number

Two serial ports are shown here, COM80 is the debugging serial port of small-core Linux, and COM81 is the debugging serial port of large-core rt-smart.

Configure serial port information

Open the tool Xshell (you can also use other serial port tools).

1 Port number: Select the port number displayed by Device Manager

2 Baud rate 115200

3 Data bit 8

4 Stop bit 1

5 Not Parity test

6 Not Flow control

##### linux

The Linux serial port is displayed as follows:

- `/dev/ttyACM0`Debug the serial port for small-core Linux
- `/dev/ttyACM1`Debug the serial port for the large-core RT-SMART

You can use Linux minicom or other serial port tools for connection debugging, and the serial port configuration information is consistent with Windows.

### Firmware acquisition and flashing

#### Firmware acquisition

CanMV-K230 firmware download address: <https://kendryte-download.canaan-creative.com/developer/k230>

Please download the gz archive starting with "k230_canmv" and extract the sysimage-sdcard.img file, which is the firmware of CanMV-K230.

#### Firmware flashing

Flash the firmware to the TF card through the computer.

##### Burning under Linux

Before inserting the TF card into the host, enter:

`ls -l /dev/sd\*`

View the current storage device.

After inserting the TF card into the host, enter again:

`ls -l /dev/sd\*`

Looking at the storage device at this time, the new addition is the TF card device node.

Assume that /dev/sdc is the TF card device node, run the following command to flash the TF card:

`sudo dd if=sysimage-sdcard.img of=/dev/sdc bs=1M oflag=sync`

##### Flashing under Windows

TF card can be burned through the balena Etcher tool under Windows (balena Etcher tool download address<https://www.balena.io/etcher/>).

1) Insert the TF card into the PC, then launch the balena Etcher tool, click the "Flash from file" button on the tool interface, and select the firmware to be programmed.

![balena-Etcher-flash-from-file](../zh/images/balena-Etcher-flash-from-file.jpg)

1) Click the "Select target" button on the tool interface to select the target sdcard card.

![balena-Etcher-select-target](../zh/images/balena-Etcher-select-target.jpg)

1) Click the "Flash" button to start flashing, the flashing process has a progress bar display, and Flash Finish will be prompted after flashing.

![balena-Etcher-flash](../zh/images/balena-Etcher-flash.jpg)
![balena-Etcher-finish](../zh/images/balena-Etcher-finish.jpg)
>Note 1: When burning the image, other programs are forbidden to read and write sd card, please turn off the computer's auto play function (Settings - auto play).

### Start the system

Insert the TF card with burned firmware into the CanMV-K230 TF card slot, connect the Type-C cable to the POWER port at the computer and the board end, the board will be powered on, and the system will start to start.
![CanMV-K230-poweron](../zh/images/CanMV-K230-poweron.png)

If the red light in the red frame is on, it means that the board is powered up normally. View the serial port information at this time.

![CanMV-K230-run](../zh/images/CanMV-K230-run.png)

After the system starts, the face detection program is run by default, the camera is pointed at the face, and the face will be framed on the monitor.

![CanMV-K230-aidemo](../zh/images/CanMV-K230-aidemo.png)

## Linux + RT-smart dual system development

This section describes how to use the K230 SDK for Linux and RT-smart system development. The K230 SDK includes the source code, toolchain and other related resources needed for development of heterogeneous systems based on Linux and RT-smart dual-core.

### Development environment setup

#### Compile the environment

| Host environment                    | description                                                 |
|-----------------------------|------------------------------------------------------|
| Docker compilation environment              | The SDK provides a docker file, which can generate docker images for compiling the SDK |
| Ubuntu 20.04.4 LTS (x86_64) | The SDK can be compiled in the ubuntu 20.04 environment                      |

The K230 SDK needs to be compiled in the Linux environment, the SDK supports docker environment compilation, and the docker file() is released in the SDK development package,`tools/docker/Dockerfile` which can generate docker images. The specific dockerfile usage and compilation steps will be described in detail in the compilation section below.

The Docker image used by the SDK is based on ubuntu 20.04, if you do not use the docker compilation environment, you can refer to the content of dockerfile in the ubuntu 20.04 host environment, install the relevant HOST package and toolchain, and compile the SDK.

The K230 SDK has not been verified in the host environment of other Linux versions, and there is no guarantee that the SDK can be compiled in other environments.

#### SDK development kit acquisition

The SDK is currently released simultaneously on GitHub and GitHub

<https://github.com/kendryte/k230_sdk>

<https://gitee.com/kendryte/k230_sdk>

Users can download the archive directly, download it at [GitHub](https://github.com/kendryte/k230_sdk/releases) [Gitee](https://gitee.com/kendryte/k230_sdk/releases) or

`git clone https://github.com/kendryte/k230_sdk`

`git clone https://gitee.com/kendryte/k230_sdk.git`

Users can choose to use GitHub or GitHub according to their network conditions.

### SDK compilation

#### Compile the introduction

The K230 SDK supports one-click compilation of large and little core operating systems and common components, and generates image files that can be programmed for deployment to the development board and start running. The username of the Linux system on the device is root without password;

Setp 1: Refer to the above to get the SDK development package

Step 2: Enter the SDK root directory

`cd k230_sdk`

Step 3: Download toolchain

`source tools/get_download_url.sh && make prepare_sourcecode`

>`make prepare_sourcecode` will download both Linux and RT-Smart toolchain, buildroot package and AI package from Microsoft Azure cloud server with CDN, the download cost time may based on your network connection speed.

Step 4: Generate a docker image (required for the first compilation, skip this step after you have generated a docker image)

`docker build -f tools/docker/Dockerfile -t k230_docker tools/docker`

Step 5: Enter the docker environment,

`docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) k230_docker /bin/bash`

Step 6: Run the following command in the Docker environment to compile the SDK

make CONF=k230_canmv_defconfig #编译CanMV-K230 board image

The SDK does not support multi-process compilation, do not add multi-process compilation parameters like -j32.

#### Compile the output artifacts

After the compilation is complete, you `output/k230_canmv_defconfig/images`can see the compilation output in the directory

`images`The image files in the directory are described as follows:

`sysimage-sdcard.img` ------------- is the boot image of the TF card;

`sysimage-sdcard.img.gz` --------- is the boot image compressed package of the TF card (gzip archive of sysimage-sdcard.img file), which needs to be decompressed first when burning.

At this point, the entire SDK is compiled, and the adult image sysimage-sdcard.img can be flashed to the TF card to boot the system.

#### example

For basic hello world, please refer to [K230_Practical_Basics_hello_world](02_applications/tutorials/K230_Practical_Basics_hello_world.md)

In the case of Vicap_demo, the code is located at k230_sdk/src/big/mpp/userapps/sample/sample_vicap

VICAP Demo implements the camera data acquisition preview function by calling the MPI interface. The CanMV development board uses the OV5647 camera module by default, which supports up to three data streams for a single camera.

##### compile

Execute make rt-smart-clean && rt-smart && make build-image in the k230_sdk directory, compile the changes of the big core into the sd card image, and generate the image file sysimage-sdcard.img in the k230_sdk/output/k230_evb_defconfig/images/ directory

The corresponding program is located at k230_sdk/src/big/mpp/userapps/sample/elf/sample_vicap.elf

##### execute

The big kernel end enters /sharefs/app and executes commands in this directory`./sample_vicap` to obtain command help information
When you enter`sample_vicap` the : command, print the following prompt:

```shell
usage: ./sample_vicap -mode 0 -dev 0 -sensor 0 -chn 0 -chn 1 -ow 640 -oh 480 -preview 1 -rotation 1
Options:
 -mode:         vicap work mode[0: online mode, 1: offline mode. only offline mode support multiple sensor input]     default 0
 -dev:          vicap device id[0,1,2]        default 0
 -dw:           enable dewarp[0,1]    default 0
 -sensor:       sensor type[0: ov9732@1280x720, 1: ov9286_ir@1280x720], 2: ov9286_speckle@1280x720]
 -ae:           ae status[0: disable AE, 1: enable AE]        default enable
 -awb:          awb status[0: disable AWB, 1: enable AWb]     default enable
 -chn:          vicap output channel id[0,1,2]        default 0
 -ow:           the output image width, default same with input width
 -oh:           the output image height, default same with input height
 -ox:           the output image start position of x
 -oy:           the output image start position of y
 -crop:         crop enable[0: disable, 1: enable]
 -ofmt:         the output pixel format[0: yuv, 1: rgb888, 2: rgb888p, 3: raw], only channel 0 support raw data, default yuv
 -preview:      the output preview enable[0: disable, 1: enable], only support 2 output channel preview
 -rotation:     display rotaion[0: degree 0, 1: degree 90, 2: degree 270, 3: degree 180, 4: unsupport rotaion]
 -help:         print this help
```

The parameters are described as follows:

| **Parameter name** | **Optional parameter value** | **Parameter description** |
|---|---|---|
| -Dev         | 0: vicap device 0 1: vicap device 1 2: vicap device 2.                             | Specify the currently used vicap device, and the system supports up to three vicap devices. By specifying the device number, the binding relationship between the sensor and different vicap devices is realized. For example: -dev 1 -sensor 0 binds the ov9732 1280x720 RGB image output to vicap device 1.                   |
| -mode | 0: Online mode; 1: Offline mode | Specify the vicap device working mode, current before online mode and offline mode. For multiple sensor inputs, it must be specified as offline mode. |
| -sensor      | 23: OV5647 (CanMV development board only supports this sensor) | Specifies the type of sensor currently in use                                                         |
| -Chn         | 0: vicap device output channel 0 1: vicap device output channel 1 2: vicap device output channel 2.     | Specify the output channel of the currently used vicap device, one vicap device supports up to three outputs, and only channel 0 supports RAW image format output  |
| -ow          |                                                                         | Specifies the output image width, which defaults to the input image width. The width needs to be 16 bytes aligned. If the default width exceeds the maximum width of the display output, the display output width is used as the final output width of the image If the output width is smaller than the input image width and the ox or oy parameters are not specified, the default is the scaled output |
| -oh          |                                                                         | Specifies the output image height, which defaults to the input image height. If the default height exceeds the maximum height of the display output, the display output height is used as the final output height of the image If the output height is less than the input image height and the ox or oy parameter is not specified, the default is the scaled output  |
| -ox          |                                                                         | Specifies the horizontal start position of the image output, this parameter greater than 0 will perform the output cropping operation  |
| -Limited liability company          |                                                                         | Specifies the vertical start position of the image output, this parameter greater than 0 will perform the output cropping operation |
| -crop        | 0: Disable the cropping function 1: Enable the cropping function                                         | When the output image size is smaller than the input image size, the output is not scaled by default, or clipped if the flag is specified  |
| -ofmt        | 0:YUV format output 1:RGB format output 2:RAW format output                            | Specify the output image format, the default is YUV output.  |
| -preview     | 0: Disable preview display 1: Enable preview display                                         | Specifies the output image preview display function. The default is enabled. Currently, up to 2 output images can be previewed at the same time. |
| -rotation    | 0: Rotate 0 degrees 1: Rotate 90 degrees 2: Rotate 180 degrees 3: Rotate 270 degrees 4: Rotation is not supported          | Specifies the rotation angle of the preview display window. By default, only the first output image window supports the rotation function. |

Example 1:

`./sample_vicap -dev 0 -sensor 23 -chn 0 -chn 1 -ow 640 -oh 480`

Note: Bind the ov5647@1920x1080 RGB output to vicap device 0 and enable vicap device output channel 0 and channel 1, where channel 0 output size defaults to the input image size (1920x1080) and channel 1 output image size is 640x480

For the API used in this example, refer to

[K230_VICAP_API Reference.md](01_software/board/mpp/K230_VICAP_API_Reference.md)

[K230_Video Output _API Reference.md](01_software/board/mpp/K230_video_output_API_reference.md)

For other demos supported by the CanMV-K230 development board, please refer to [the K230_SDK_CanMV_Board_Demo User Guide](01_software/board/examples/K230_SDK_CanMV_Board_Demo_User_Guide.md)

For other SDK-related documents, please visit [the K230 SDK documentation](https://github.com/kendryte/k230_docs)

## Developed by nncase

`nncase` is a neural network compiler for AI accelerators, which is used to generate model files, `.kmodel`, required for inference for `Kendryte` series chips and provide `runtime lib`.

This tutorial mainly includes the following:

1. Use `nncase` to compile the model and generate `kmodel`.
1. Inference `kmodel` on PCs and development boards.

> Tips：
>
> 1. This tutorial aims to familiarize users with the process of using nncase, and the input data of the model in this doc are random numbers. For details about the actual application scenario, see the subsequent chapter "AI Development".
> 1. The version of nncase in the official CanMV image may be outdated, if you need to use the latest nncase, you need to update the runtime library and recompile the CanMV image.

### Model compilation and simulator inference

#### Install the nncase toolchain

The nncase toolchain includes both `nncase` and `nncase-kpu` plugin packages, both of which need to be installed correctly to compile the model files supported by CanMV-K230. Both `nncase` and `nncase-kpu` plugin packages are released on [NNcase GitHub Release](https://github.com/kendryte/nncase/releases) and depend on `dotnet-7.0`.

- In `Linux` platform, `nncase` and `nncase-kpu` can be installed directly online by `pip`, and use `apt` to install `dotnet` in the Ubuntu environment.

    ```Shell
    pip install --upgrade pip
    pip install nncase
    pip install nncase-kpu
    
    # nncase-2.x need dotnet-7
    sudo apt-get update
    sudo apt-get install -y dotnet-sdk-7.0
    ```

    >Tips: If you use the official CanMV image, you need to check the version of SDK and nncase.

- **The `Windows` platform only supports `nncase` online installation, and  you need to manually download `nncase-kpu` on [NNcase GitHub Release](https://github.com/kendryte/nncase/releases) and install it.**
- If you do not have an Ubuntu environment, you can use `nncase docker` (Ubuntu 20.04 + Python 3.8 + dotnet-7.0).

    ```Shell
    cd /path/to/nncase_sdk
    docker pull ghcr.io/kendryte/k230_sdk
    docker run -it --rm -v `pwd`:/mnt -w /mnt ghcr.io/kendryte/k230_sdk /bin/bash -c "/  bin/bash"
    ```

    > Tips: Currently only support py3.6-3.10, if pip installation fails, please check the pip version corresponding to Python.

#### Environment configuration

After using pip to install the packages, you need to add the installation path to the PATH environment variable.

```Shell
export PATH=$PATH:/path/to/python/site-packages/
```

#### Original model description

Currently `nncase` supporte `tflite`, `onnx` format models, more formats support is ongoing.

> Tips：
>
> 1. For TensorFlow models, `pb` format, please refer to the official documentation to convert them to the `tflite` model. Be careful not to set quantization options, just export the floating-point model. If `quantize` and `dequantize` operators exist in the model, they belong to quantization models and are currently not supported.
> 1. For PyTorch models, `pth` format, you need to use `torch.export.onnx` to export the `onnx` model.

#### Description of compilation parameters

Before compiling a model, you need to know the following key information:

1. `KPU` uses fixed-point operations when making inferences. Therefore, when compiling the `kmodel`, you must configure quantization-related parameters that are used to convert the `kmodel` from floating point to fixed point. Details in `nncase` documentation [PTQTensorOptions](https://github.com/kendryte/nncase/blob/master/docs/USAGE_v2.md#ptqtensoroptions).
1. `nncase` support for adding preprocessing operations in `kmodel`, which can reduce the preprocessing overhead when inference. The relevant parameters and schematics are found in `nncase` documentation [CompileOptions](https://github.com/kendryte/nncase/blob/master/docs/USAGE_v2.md#compileoptions).

#### Description of compilation script

This [Jupyter notebook](https://github.com/kendryte/nncase/blob/master/examples/user_guide/k230_simulate-EN.ipynb) describes in detail the process of compiling and infering kmodels using nncase. It contains the following information。

- Parameter configuration: describes how to correctly configure compilation parameters in order to satisfy the demands of actual deployment.
- Obtain model information: explain the method of obtaining key data such as network structure and layer information from the original model.
- Set calibration dataset: explains how to prepare calibration dataset sample data, including single-input and multiple-input models, for quantifying the calibration process.
- Set the inference data format: explains how to configure input data during inference to support different demand scenarios.
- Configure multi-input model: describes how to correctly set the shape, data format and other information of each input when processing multi-input model.
- PC simulator inference: explain how to use the simulator to infer on PC the `kmodel`, which is a key step to verify the compilation effect;
- Compare inference results: verify the correctness of kmodels by comparing inference results with different frameworks (TensorFlow, PyTorch, etc.);

  The above steps systematically introduce the whole process of model compilation and inference, which is suitable for beginners to learn from scratch and can also be used as a reference guide for experienced users.

#### Sample code

When you have read the full tutorial in the Jupyter notebook, you can modify the options based on the following sample code.

```Python
import nncase
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import onnx
import onnxsim

def get_cosine(vec1, vec2):
    """
    result compare
    """
    return cosine_similarity(vec1.reshape(1, -1), vec2.reshape(1, -1))


def read_model_file(model_file):
    """
    read model
    """
    with open(model_file, 'rb') as f:
        model_content = f.read()
    return model_content


def parse_model_input_output(model_file):
    """
    parse onnx model
    """
    onnx_model = onnx.load(model_file)
    input_all = [node.name for node in onnx_model.graph.input]
    input_initializer = [node.name for node in onnx_model.graph.initializer]
    input_names = list(set(input_all) - set(input_initializer))
    input_tensors = [
        node for node in onnx_model.graph.input if node.name in input_names]

    # input
    inputs = []
    for _, e in enumerate(input_tensors):
        onnx_type = e.type.tensor_type
        input_dict = {}
        input_dict['name'] = e.name
        input_dict['dtype'] = onnx.mapping.TENSOR_TYPE_TO_NP_TYPE[onnx_type.elem_type]
        input_dict['shape'] = [i.dim_value for i in onnx_type.shape.dim]
        inputs.append(input_dict)

    return onnx_model, inputs

def model_simplify(model_file):
    """
    simplify model
    """
    if model_file.split('.')[-1] == "onnx":
        onnx_model, inputs = parse_model_input_output(model_file)
        onnx_model = onnx.shape_inference.infer_shapes(onnx_model)
        input_shapes = {}
        for input in inputs:
            input_shapes[input['name']] = input['shape']

        onnx_model, check = onnxsim.simplify(onnx_model, input_shapes=input_shapes)
        assert check, "Simplified ONNX model could not be validated"

        model_file = os.path.join(os.path.dirname(model_file), 'simplified.onnx')
        onnx.save_model(onnx_model, model_file)
        print("[ onnx done ]")
    elif model_file.split('.')[-1] == "tflite":
        print("[ tflite skip ]")
    else:
        raise Exception(f"Unsupport type {model_file.split('.')[-1]}")

    return model_file

def run_kmodel(kmodel_path, input_data):
    print("\n---------start run kmodel---------")
    print("Load kmodel...")
    model_sim = nncase.Simulator()
    with open(kmodel_path, 'rb') as f:
        model_sim.load_model(f.read())

    print("Set input data...")
    for i, p_d in enumerate(input_data):
        model_sim.set_input_tensor(i, nncase.RuntimeTensor.from_numpy(p_d))

    print("Run...")
    model_sim.run()

    print("Get output result...")
    all_result = []
    for i in range(model_sim.outputs_size):
        result = model_sim.get_output_tensor(i).to_numpy()
        all_result.append(result)
    print("----------------end-----------------")
    return all_result


def compile_kmodel(model_path, dump_path, calib_data):
    """
    Set compile options and ptq options.
    Compile kmodel.
    Dump the compile-time result to 'compile_options.dump_dir'
    """
    print("\n----------   compile    ----------")
    print("Simplify...")
    model_file = model_simplify(model_path)

    print("Set options...")
    # import_options
    import_options = nncase.ImportOptions()

    ############################################
    # The code below, you need to modify to fit your model.
    ############################################
    # compile_options
    compile_options = nncase.CompileOptions()
    compile_options.target = "k230" #"cpu"
    compile_options.dump_ir = True  # if False, will not dump the compile-time result.
    compile_options.dump_asm = True
    compile_options.dump_dir = dump_path
    compile_options.input_file = ""

    # preprocess args
    compile_options.preprocess = False
    if compile_options.preprocess:
        compile_options.input_type = "uint8" # "uint8" "float32"
        compile_options.input_shape = [1,224,320,3]
        compile_options.input_range = [0,1]
        compile_options.input_layout = "NHWC" # "NHWC"
        compile_options.swapRB = False
        compile_options.mean = [0,0,0]
        compile_options.std = [1,1,1]
        compile_options.letterbox_value = 0
        compile_options.output_layout = "NHWC" # "NHWC"

    # quantize options
    ptq_options = nncase.PTQTensorOptions()
    ptq_options.quant_type = "uint8" # datatype : "float32", "int8", "int16"
    ptq_options.w_quant_type = "uint8"  # datatype : "float32", "int8", "int16"
    ptq_options.calibrate_method = "NoClip" # "Kld"
    ptq_options.finetune_weights_method = "NoFineTuneWeights"
    ptq_options.dump_quant_error = False
    ptq_options.dump_quant_error_symmetric_for_signed = False

    # mix quantize options
    # more details in docs/MixQuant.md
    ptq_options.quant_scheme = ""
    ptq_options.export_quant_scheme = False
    ptq_options.export_weight_range_by_channel = False
    ############################################

    ptq_options.samples_count = len(calib_data[0])
    ptq_options.set_tensor_data(calib_data)

    print("Compiling...")
    compiler = nncase.Compiler(compile_options)
    # import
    model_content = read_model_file(model_file)
    if model_path.split(".")[-1] == "onnx":
        compiler.import_onnx(model_content, import_options)
    elif model_path.split(".")[-1] == "tflite":
        compiler.import_tflite(model_content, import_options)

    compiler.use_ptq(ptq_options)

    # compile
    compiler.compile()
    kmodel = compiler.gencode_tobytes()

    kmodel_path = os.path.join(dump_path, "test.kmodel")
    with open(kmodel_path, 'wb') as f:
        f.write(kmodel)
    print("----------------end-----------------")
    return kmodel_path

if __name__ == "__main__":
    # compile kmodel single input
    model_path = "./test.tflite"
    dump_path = "./tmp_tflite"

    # sample_count is 2
    calib_data = [[np.random.rand(1, 240, 320, 3).astype(np.float32), np.random.rand(1, 240, 320, 3).astype(np.float32)]]
    kmodel_path = compile_kmodel(model_path, dump_path, calib_data)

    # run kmodel(simulate)
    kmodel_path = "./tmp_tflite/test.kmodel"
    input_data = [np.random.rand(1, 240, 320, 3).astype(np.float32)]
    input_data[0].tofile(os.path.join(dump_path,"input_0.bin"))

    result = run_kmodel(kmodel_path, input_data)

    for idx, i in enumerate(result):
        print(i.shape)
        i.tofile(os.path.join(dump_path,"nncase_result_{}.bin".format(idx)))
```

#### Notes

When you encounter problems when compiling the model, you can find the error log in the [FAQ](https://github.com/kendryte/nncase/blob/master/docs/FAQ_ZH.md) to find a solution, you can also raise an issue according to the template in [github](https://github.com/kendryte/nncase/issues) or ask questions directly in `nncase QQ communication group: 790699378`.

At the same time, you are also welcome to propose your problems and solutions `PR`  to `nncase`, contribute to the open source work.

### Model inference based on the development board

Currently `CanMV`supports two sets of development APIs,`C++` and  , `MicroPython`you can choose according to your needs.

- `MicroPython` with a low development threshold, users can directly write code similar to `Python` for application development;
- `C++` has a higher threshold, but it is more flexible and has better performance (the inference performance of the chip is not affected by language).

When inference on the board, we provide two modules to accelerate model inference

- Hardware-based pre-processing module: `AI2D`. More details in [AI2D runtime APIs](01_software/board/ai/K230_nncase_Development_Guide.md);
- Hardware-based model inference module:`KPU`. More details in [KPU runtime APIs](01_software/board/ai/K230_nncase_Development_Guide.md);

Next, we will explain how these two modules are used in the C++ code example and what needs to be noticed.

Taking face detection as an example, the directory structure and important functions of the code will be explained below, and the complete code example is shown in `k230_sdk/src/big/nncase/examples/image_face_detect` .

#### Directory structure

In the example directory, the file structure related to model inference is as follows:

```Shell
k230_sdk/src/big/nncase/examples/
├── build_app.sh
├── CMakeLists.txt
├── image_face_detect
│   ├── anchors_320.cc
│   ├── CMakeLists.txt
│   ├── main.cc
│   ├── mobile_retinaface.cc
│   ├── mobile_retinaface.h
│   ├── model.cc
│   ├── model.h
│   ├── util.cc
│   └── util.h
└── README.md
```

- build_app.sh: The script of compile that generates the executable `image_face_detect.elf` and output it to the `out` directory.
- CMakeLists.txt: Set the libraries that need to be linked during compilation:`opencv`, `mmz`, `nncase`. Only need to modify `add_subdirectory()` in your project.
- image_face_detect: Complete face detection demo, which includes `AI2D`, `KPU` and post-processing, etc.

#### AI2D configuration

In `mobile_retinaface.cc`, the `pad` and `resize` of AI2D function were used. The code block of class `MobileRetinaface` constructor will be explained below, it contains the configuration of `AI2D` parameters.

1. Set the `AI2D`output tensor

```C++
    ai2d_out_tensor_ = input_tensor(0);
```

`input_tensor(0)` is to get the input tensor of `KPU`. This step is to set the input tensor of `KPU` to the output tensor of `AI2D`. Connect the two parts of the hardware without any other hardware control.

1. Set `AI2D`the parameters

```C++
    dims_t in_shape { 1, ai2d_input_c_, ai2d_input_h_, ai2d_input_w_ };
    auto out_shape = input_shape(0);

    ai2d_datatype_t ai2d_dtype { ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, typecode_t::dt_uint8, typecode_t::dt_uint8 };
    ai2d_crop_param_t crop_param { false, 0, 0, 0, 0 };
    ai2d_shift_param_t shift_param { false, 0 };

    float h_ratio = static_cast<float>(height) / out_shape[2];
    float w_ratio = static_cast<float>(width) / out_shape[3];
    float ratio = h_ratio > w_ratio ? h_ratio : w_ratio;

    int h_pad = out_shape[2] - height / ratio;
    int h_pad_before = h_pad / 2;
    int h_pad_after = h_pad - h_pad_before;

    int w_pad = out_shape[3] - width / ratio;
    int w_pad_before = w_pad / 2;
    int w_pad_after = w_pad - w_pad_before;

#if ENABLE_DEBUG
    std::cout << "h_ratio = " << h_ratio << ", w_ratio = " << w_ratio << ", ratio = " << ratio << std::endl;
    std::cout << "h_pad = " << h_pad << ", h_pad_before = " << h_pad_before << ", h_pad_after = " << h_pad_after << std::endl;
    std::cout << "w_pad = " << w_pad << ", w_pad_before = " << w_pad_before << ", w_pad_after = " << w_pad_after << std::endl;
#endif

    ai2d_pad_param_t pad_param{true, {{ 0, 0 }, { 0, 0 }, { h_pad_before, h_pad_after }, { w_pad_before, w_pad_after }}, ai2d_pad_mode::constant, { 0, 0, 0 }};
    ai2d_resize_param_t resize_param { true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel };
    ai2d_affine_param_t affine_param { false };
```

First, you need to set the basic parameters of `AI2D`, including input format, output format, input type, and output type.Then set the `AI2D` function parameters, only `Pad` and `Resize` function were used in face detection demo, but you still need to explicitly set the parameters of other functions, such as `crop`,`shift` and `affine`, only set the first parameter to `false` and the rest of the parameters conform to the syntax.

1. Generate instructions of `AI2D`

```C++
    ai2d_builder_.reset(new ai2d_builder(in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param));
    ai2d_builder_->build_schedule();
```

First you need to create the `ai2d_builder` object. If it already exists, you need to use the `reset` function to update the parameters in it, and then call the function `build_schedule()` to complete the instruction generation.

At this point, the configuration of `AI2D` is over, let's take a look at the related configuration of `KPU`.

#### KPU configuration

The `KPU` related configuration is carried out in 'model.cc', mainly allocating the memory and settings of the input tensor in advance. Let's look at the constructor of the class 'Model':

```C++
Model::Model(const char *model_name, const char *kmodel_file): model_name_(model_name)
{
    // load kmodel
    kmodel_ = read_binary_file<unsigned char>(kmodel_file);
    interp_.load_model({ (const gsl::byte *)kmodel_.data(), kmodel_.size() }).expect("cannot load kmodel.");

    // create kpu input tensors
    for (size_t i = 0; i < interp_.inputs_size(); i++)
    {
        auto desc = interp_.input_desc(i);
        auto shape = interp_.input_shape(i);
        auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create input tensor");
        interp_.input_tensor(i, tensor).expect("cannot set input tensor");
    }

}
```

1. Read the model

```C++
std::ifstream ifs(kmodel_file, std::ios::binary);
interp_.load_model(ifs).expect("load_model failed");
```

First convert the file path to a stream, and then stream loading via `load_model()`.

1. Input tensor memory allocation

```C++
auto desc = interp_.input_desc(i);
auto shape = interp_.input_shape(i);
auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create input tensor");
```

Here, an empty tensor is created based on the shape information and type information obtained from the model.

> Q: Why is it empty tensor, instead of directly filling the data into it?
>
> A: You can first take a look at `AI2D` what we did when setting the output tensor. Yeah, the empty tensor is to receive the output data of `AI2D`, so there is no need to set the data directly. However, if you do not use `AI2D` module, then here you need to set the input data, for example:
>
> auto tensor = host_runtime_tensor::create(
> desc.datatype, shape, { (gsl::bytes*)vector.data(), (size_t)vector.size()  },
> true,  hrt::pool_shared).expect("cannot create input tensor");

At this point, the relevant configuration of `KPU` is also completed, and then we will see how to execute these two parts of the module.

#### Start inference

Inference is performed in the `ai_proc` function of `main.cc`, and the code that initiates inference is:

```C++
model.run(reinterpret_cast<uintptr_t>(vaddr), reinterpret_cast<uintptr_t>(paddr));
auto result = model.get_result();
```

`result` is the output of the model, `AI2D` and `KPU` were called in `run()`.

```C++
void Model::run(uintptr_t vaddr, uintptr_t paddr)
{
    preprocess(vaddr, paddr);
    kpu_run();
    postprocess();
}

void MobileRetinaface::preprocess(uintptr_t vaddr, uintptr_t paddr)
{
    // ai2d input tensor
    dims_t in_shape { 1, ai2d_input_c_, ai2d_input_h_, ai2d_input_w_ };
    auto ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, in_shape, { (gsl::byte *)vaddr, compute_size(in_shape) },
        false, hrt::pool_shared, paddr).expect("cannot create input tensor");
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("sync write_back failed");

    // run ai2d
    ai2d_builder_->invoke(ai2d_in_tensor, ai2d_out_tensor_).expect("error occurred in ai2d running");
}

void Model::kpu_run()
{
    interp_.run().expect("error occurred in running model");
}
```

The `preprocess()` function starts the inference of `AI2D` and the `kpu_run()` function starts the inference of `KPU`. Of course, before starting the inference, you need to set the physical address of input for `AI2D`. The input tensor of `AI2D` can get the data through input device directly.

> Tips: The `postprocess()` function calls the post-processing part of the model, which varies from model to model and from version to version of the same model, before the full inference is done.
>
> Make sure that the results of your post-processing `C++` code are consistent with the results of your `Python` model post-processing!!
>
> Make sure that the results of your post-processing `C++` code are consistent with the results of your `Python` model post-processing!!
>
> Make sure that the results of your post-processing `C++` code are consistent with the results of your `Python` model post-processing!!
>

## AI development

AI development requires environment construction, data preparation, model training and testing, CANMV k230 image compilation and programming, C++ code compilation, network configuration and file transfer, and k230 device deployment. Take the vegetable classification scenario as an example. For the code, see: <https://github.com/kendryte/K230_training_scripts/tree/main/end2end_cls_doc>.

### Environment setup

(1) Linux system;

(2) Install the graphics card driver;

(3) Install Anaconda to create a model training environment;

(4) Install Docker to create an SDK image compilation environment;

(5) Install dotnet SDK;

### Data preparation

The custom data set for the image classification task is organized in the following format:

![dataset_frame](../zh/images/dataset_frame.png)

Note: Image categories must be organized strictly according to the above format.

### Model training and testing

This section is implemented in the training environment.

#### Create a virtual environment

Open the command terminal:

```Shell
conda create -n myenv python=3.9
conda activate myenv
```

#### Install the Python library

Install the Python library used for training according to the requriements .txt in the project, and wait for installation:

```Shell
pip install -r requriements.txt
```

In the requriments .txt, the model transformation packages nncase and nncase-kpu, a neural network compiler designed for AI accelerators, are installed.

#### Configure training parameters

The configuration file yaml/config.yaml in the given training script is set as follows:

```YAML
dataset:
  root_folder: ../data/veg_cls # Classification dataset path
  split: true # Whether to re-execute the split, the first execution must be true
  train_ratio: 0.7 # Training set proportion
  val_ratio: 0.15 # Validation set proportion
  test_ratio: 0.15 # Test set proportion

train:
  device: cuda
  txt_path: ../gen # The training set, verification set, test set txt files, label name files, and calibration set files generated by the splitting process
  image_size: [ 224,224 ] 
  mean: [ 0.485, 0.456, 0.406 ]
  std: [ 0.229, 0.224, 0.225 ]
  epochs: 10
  batchsize: 8
  learningrate: 0.001
  save_path: ../checkpoints # Model save path

inference:
  mode: image # Inference mode is divided into image and video; in image mode, a single picture and all pictures in the directory can be inferred, and video calls the camera to achieve inference.
  inference_model: best # best or last, call best.pth and last.pth under checkpoints respectively for reasoning.
  images_path: ../data/veg_cls/bocai # If the path is a image path, inference will be performed on a single picture; if the path is a directory, inference will be performed on all pictures in the directory.

deploy:
  chip: k230 # k230 or cpu
  ptq_option: 0 # Quantization type, 0 is uint8, 1, 2, 3, 4 are different forms of uint16
```

#### Model training

Go to the project's scripts directory and execute the training code:

```Shell
python3 main.py
```

If the training is successful, you can find the trained last.pth, best.pth, best.onnx, and best.kmodel in the model_save_dir directory of the configuration file.

#### Model testing

Set the Inference section in the configuration file, set the test configuration, execute the test code:

```shell
python3 inference.py
```

#### Prepare the file

The files required for later deployment steps include:

（1）checkpoints/best.kmodel;

（2）gen/labels.txt;

   (3)  test .jpg of the picture to be tested;

### CANMV K230 image compilation and burning

#### Docker environment setup

```Shell
# Download docker compiled image
docker pull ghcr.io/kendryte/k230_sdk
# You can use the following command to confirm whether the docker image is successfully pulled
docker images | grep ghcr.io/kendryte/k230_sdk
# download sdk
git clone -b v1.0.1 --single-branch https://github.com/kendryte/k230_sdk.git
cd k230_sdk
# Download toolchain Linux and RT-Smart toolchain, buildroot package, AI package, etc.
make prepare_sourcecode
# Create a docker container, $(pwd):$(pwd) means that the current directory of the system is mapped to the same directory inside the docker container, and the toolchain directory under the system is mapped to the /opt/toolchain directory inside the docker container.
docker run -u root -it -v $(pwd):$(pwd) -v $(pwd)/toolchain:/opt/toolchain -w $(pwd) ghcr.io/kendryte/k230_sdk /bin/bash
```

#### Image compilation

```Shell
# Compiling the image in the docker container takes a long time, please wait patiently for completion.
make CONF=k230_canmv_defconfig
```

#### Image burning

After the compilation is completed, you can find the compiled image file in the output/k230_canmv_defconfig/images directory:

```shell
k230_evb_defconfig/images
 ├── big-core
 ├── little-core
 ├── sysimage-sdcard.img    # SDcard image
 └── sysimage-sdcard.img.gz 
```

The CANMV K230 supports SDCard boot mode. To facilitate development, it is recommended that you prepare a TF card (Micro SD card).

**Linux:** If you use Linux to flash a TF card, you need to confirm the name of the SD card in the system /dev/sdx, and replace /dev/sdx in the following command

sudo dd if=sysimage-sdcard.img of=/dev/sdx bs=1M oflag=sync

**Windows:** If you are using Windows burning, it is recommended to use[the balena Etcher](https://etcher.balena.io/)tool. Download the generated sysimage-sdcard.img locally and burn it using the burning tool The balena Etcher.

![balena-Etcher-flash](../zh/images/balena-Etcher-flash.jpg)

After the burning is successful, a notification message will pop up. It is best to format the SD card before flashing.

### Power on the development board

Install MobaXterm to achieve serial communication, MobaXterm download address:<https://mobaxterm.mobatek.net> .

![CanMV-K230_debug](../zh/images/CanMV-K230_debug.png)

Insert the flashed SD card into the open board card slot, HDMI output to display, 100 Gigabit network port to Ethernet, POWER to serial port and power supply.

After the system is powered on, there will be**two serial devices by default**, which can be used to access small-core Linux and large-core RTSmart

The default user name of little core Linux is root, and the password is empty. The RTSmart system automatically launches an application and can exit`q` to the Command Prompt terminal by pressing the key.

### C++ code compilation

After completing the preparations for the above development board, we can use C++ to write our own code. Taking the image classification task as an example, the following example code for related image classification tasks is given and analyzed. Sample code reference: <https://github.com/kendryte/K230_training_scripts/tree/main/end2end_cls_doc/k230_code>.

#### Code structure

```shell
k230_code
├── cmake
│    ├── link.lds 
│    ├── Riscv64.cmake
├── k230_deploy
│    ├── ai_base.cc # Model deployment base class 
│    ├── ai_base.h # The model deployment base class encapsulates nncase loading, input settings, model inference, and output acquisition operations. For subsequent specific task development, you only need to focus on the pre-processing and post-processing of the model.
│    ├── classification.cc # classification code
│    ├── classification.h # Image classification task class definition, inherits AIBase, and is used to encapsulate the pre- and post-processing of model inference.
│    ├── main.cc # Main function, parameter analysis, initialization of Classification class examples, and implementation of the board function
│    ├── scoped_timing.hpp # tool of getting  running time
│    ├── utils.cc # tool class
│    ├── utils.h # The tool class encapsulates common functions for image preprocessing and image classification, including reading binary files, saving pictures, image processing, result drawing, etc. Users can enrich the file according to their own needs.
│    ├── vi_vo.h # Video input and output header files
│    ├── CMakeLists.txt # CMake script is used to build an executable file using C/C++ source files and linking to various libraries
├── build_app.sh # Compile the script and use the cross-compilation tool chain to compile the k230_deploy project
└── CMakeLists.txt # CMake script is used to build the nncase_sdk project project
```

#### Core code

After you get the kmodel model, the specific AI board code includes: sensor&display initialization, kmodel loading, model input and output settings, image acquisition, input data loading, input data preprocessing, model inference, model output acquisition, output post-processing, OSD display Wait for steps. as the picture shows:

![pipeline](../zh/images/pipeline.jpg)

The yellow box part in the figure provides sample code in Example 2 of the SDK compilation chapter. The following describes how to implement AI development for the red box part.

In the above process, kmodel loading, model input setting, model inference, and model output acquisition are common steps for all tasks. We have encapsulated this, and ai_base.h and ai_base.cc can be copied and used directly.

ai_base.h defines the AIBase base class and interfaces for common operations:

```c++
#ifndef AI_BASE_H
#define AI_BASE_H
#include <vector>
#include <string>
#include <fstream>
#include <nncase/runtime/interpreter.h>
#include "scoped_timing.hpp"

using std::string;
using std::vector;
using namespace nncase::runtime;

/**
 * @brief AI base class, encapsulating nncase related operations
 * It mainly encapsulates the loading, setting input, running, and obtaining output operations of nncase. Subsequent development of the demo only needs to focus on the pre-processing and post-processing of the model.
 */
class AIBase
{
public:
    /**
     * @brief AI base class constructor, loads kmodel, and initializes kmodel input and output
     * @param kmodel_file kmodel file path
     * @param debug_mode  0（no debug）、 1（print time）、2（print all）None
     * @return None
     */
    AIBase(const char *kmodel_file,const string model_name, const int debug_mode = 1);
    /**
     * @brief AI base class destructor
     * @return None
    */
    ~AIBase();

    /**
     * @brief set kmodel input
     * @param buf input data pointer
     * @param size Input data size
     * @return None
     */
    void set_input(const unsigned char *buf, size_t size);

    /**
     * @brief Get kmodel input tensor according to index
     * @param idx 
     * @return None
     */
    runtime_tensor get_input_tensor(size_t idx);

    /**
     * @brief Set the input tensor of the model
     * @param idx 
     * @param tensor
     */
    void set_input_tensor(size_t idx, runtime_tensor &tensor);

    /**
     * @brief Initialize kmodel output
     * @return None
     */
    void set_output();

    /**
     * @brief inference kmodel
     * @return None
     */
    void run();

    /**
     * @brief Get kmodel output and save the result in the corresponding class attribute
     * @return None
     */
    void get_output();



protected:
    string model_name_;                    // model name
    int debug_mode_;                       
    vector<float *> p_outputs_;            // kmodel outputs the corresponding pointer list
    vector<vector<int>> input_shapes_;     //{{N,C,H,W},{N,C,H,W}...}
    vector<vector<int>> output_shapes_;    //{{N,C,H,W},{N,C,H,W}...}} or {{N,C},{N,C}...}}
    vector<int> each_input_size_by_byte_;  //{0,layer1_length,layer1_length+layer2_length,...}
    vector<int> each_output_size_by_byte_; //{0,layer1_length,layer1_length+layer2_length,...}
    
private:
    /**
     * @brief Initialize the kmodel input for the first time and obtain the input shape
     * @return None
     */
    void set_input_init();

    /**
     * @brief Initialize kmodel output for the first time and obtain the output shape
     * @return None
     */
    void set_output_init();

    vector<unsigned char> kmodel_vec_; // The entire kmodel data is obtained by reading the kmodel file, which is used to pass it to the kmodel interpreter to load kmodel.
    interpreter kmodel_interp_; // The kmodel interpreter is built from the kmodel file and is responsible for the loading, input and output of the model.
};
#endif
```

ai_base.cc is the specific implementation of all interfaces defined in ai_base.h.

```c++
/*
The specific implementation of the interface defined by the AIBase class in ai_base.h
*/
#include "ai_base.h"
#include <iostream>
#include <cassert>
#include "utils.h"

using std::cout;
using std::endl;
using namespace nncase;
using namespace nncase::runtime::detail;

/*AIBase constructor*/
AIBase::AIBase(const char *kmodel_file,const string model_name, const int debug_mode) : debug_mode_(debug_mode),model_name_(model_name)
{
    if (debug_mode > 1)
        cout << "kmodel_file:" << kmodel_file << endl;
    std::ifstream ifs(kmodel_file, std::ios::binary);//read kmodel
    kmodel_interp_.load_model(ifs).expect("Invalid kmodel");//load kmodel
    set_input_init();
    set_output_init();
}

/*destructor*/
AIBase::~AIBase()
{
}

/*
Initialize kmodel input for the first time
*/
void AIBase::set_input_init()
{
    ScopedTiming st(model_name_ + " set_input init", debug_mode_);//get time
    int input_total_size = 0;
    each_input_size_by_byte_.push_back(0); // Fill in 0 
    for (int i = 0; i < kmodel_interp_.inputs_size(); ++i)
    {
        auto desc = kmodel_interp_.input_desc(i);//Input description with index i
        auto shape = kmodel_interp_.input_shape(i);//Input shape with index i
        auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create input tensor");//create a tensor
        kmodel_interp_.input_tensor(i, tensor).expect("cannot set input tensor");//Bind tensor to model input
        vector<int> in_shape = {shape[0], shape[1], shape[2], shape[3]};
        input_shapes_.push_back(in_shape);//Store input shape
        int dsize = shape[0] * shape[1] * shape[2] * shape[3];//Enter the total number of bytes
        if (debug_mode_ > 1)
            cout << "input shape:" << shape[0] << " " << shape[1] << " " << shape[2] << " " << shape[3] << endl;
        if (desc.datatype == 0x06)//The input data is of uint8 type
        {
            input_total_size += dsize;
            each_input_size_by_byte_.push_back(input_total_size);
        }
        else if (desc.datatype == 0x0B)//The input data is of float32 type
        {
            input_total_size += (dsize * 4);
            each_input_size_by_byte_.push_back(input_total_size);
        }
        else
            assert(("kmodel input data type supports only uint8, float32", 0));
    }
    each_input_size_by_byte_.push_back(input_total_size); 
}

/*
Set the input data of the model and load the specific data input by the model. The difference between set_input_init and set_input_init is whether there is a data copy process.
*/
void AIBase::set_input(const unsigned char *buf, size_t size)
{
    //Check whether the input data size matches the model required size
    if (*each_input_size_by_byte_.rbegin() != size)
        cout << "set_input:the actual input size{" + std::to_string(size) + "} is different from the model's required input size{" + std::to_string(*each_input_size_by_byte_.rbegin()) + "}" << endl;
    assert((*each_input_size_by_byte_.rbegin() == size));
    //get time
    ScopedTiming st(model_name_ + " set_input", debug_mode_);
   
    for (size_t i = 0; i < kmodel_interp_.inputs_size(); ++i)
    {
        //Get the input description and shape of the model
        auto desc = kmodel_interp_.input_desc(i);
        auto shape = kmodel_interp_.input_shape(i);
        //create tensor
        auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create input tensor");
        //Map input tensor to writable area
        auto mapped_buf = std::move(hrt::map(tensor, map_access_::map_write).unwrap()); 
        //Copy data to tensor buffer
        memcpy(reinterpret_cast<void *>(mapped_buf.buffer().data()), buf, each_input_size_by_byte_[i + 1] - each_input_size_by_byte_[i]);
        //Unmap
        auto ret = mapped_buf.unmap();
        ret = hrt::sync(tensor, sync_op_t::sync_write_back, true);
        if (!ret.is_ok())
        {
            std::cerr << "hrt::sync failed" << std::endl;
            std::abort();
        }
        //Bind the tensor to the input of the model
        kmodel_interp_.input_tensor(i, tensor).expect("cannot set input tensor");
    }
}

/*
Get the input tensor of the model according to the index
*/
runtime_tensor AIBase::get_input_tensor(size_t idx)
{
    return kmodel_interp_.input_tensor(idx).expect("cannot get input tensor");
}

/*
Set the input tensor of the model according to the index
*/
void AIBase::set_input_tensor(size_t idx, runtime_tensor &tensor)
{
    ScopedTiming st(model_name_ + " set_input_tensor", debug_mode_);
    kmodel_interp_.input_tensor(idx, tensor).expect("cannot set input tensor");
}

/*
Initialize kmodel output for the first time
*/
void AIBase::set_output_init()
{
    //get time
    ScopedTiming st(model_name_ + " set_output_init", debug_mode_);
    each_output_size_by_byte_.clear();
    int output_total_size = 0;
    each_output_size_by_byte_.push_back(0);
   
    for (size_t i = 0; i < kmodel_interp_.outputs_size(); i++)
    {
        //Get output description and shape
        auto desc = kmodel_interp_.output_desc(i);
        auto shape = kmodel_interp_.output_shape(i);
        vector<int> out_shape;
        int dsize = 1;
        for (int j = 0; j < shape.size(); ++j)
        {
            out_shape.push_back(shape[j]);
            dsize *= shape[j];
            if (debug_mode_ > 1)
                cout << shape[j] << ",";
        }
        if (debug_mode_ > 1)
            cout << endl;
        output_shapes_.push_back(out_shape);
        //Get the total size of data
        if (desc.datatype == 0x0B)
        {
            output_total_size += (dsize * 4);
            each_output_size_by_byte_.push_back(output_total_size);
        }
        else
            assert(("kmodel output data type supports only float32", 0));
        //create tensor
        auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create output tensor");
        //Bind the tensor to the output of the model
        kmodel_interp_.output_tensor(i, tensor).expect("cannot set output tensor");
    }
}

/*
Set the output of the kmodel 
*/
void AIBase::set_output()
{
    ScopedTiming st(model_name_ + " set_output", debug_mode_);
    //The loop binds the output tensor to the output of the kmodel
    for (size_t i = 0; i < kmodel_interp_.outputs_size(); i++)
    {
        auto desc = kmodel_interp_.output_desc(i);
        auto shape = kmodel_interp_.output_shape(i);
        auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create output tensor");
        kmodel_interp_.output_tensor(i, tensor).expect("cannot set output tensor");
    }
}

/*
Call kmodel_interp_.run() to implement model inference
*/
void AIBase::run()
{
    ScopedTiming st(model_name_ + " run", debug_mode_);
    kmodel_interp_.run().expect("error occurred in running model");
}

/*
Obtain the output of the kmodel and prepare for subsequent post-processing
*/
void AIBase::get_output()
{
    ScopedTiming st(model_name_ + " get_output", debug_mode_);
    //p_outputs_ pointer to store the output of the kmodel, there can be multiple outputs
    p_outputs_.clear();
    for (int i = 0; i < kmodel_interp_.outputs_size(); i++)
    {
        //get output tensor
        auto out = kmodel_interp_.output_tensor(i).expect("cannot get output tensor");
        //Map the output tensor into host memory
        auto buf = out.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_read).unwrap().buffer();
        //Convert mapped data to float pointer
        float *p_out = reinterpret_cast<float *>(buf.data());
        p_outputs_.push_back(p_out);
    }
}
```

The pre-processing and post-processing of different task scenarios are different. For example, softmax is used to calculate the category probability for classification, and nms is required for target detection. Therefore, you can define your task scenario class to inherit the AIBase class and perform pre-processing and post-processing for the task. Code is encapsulated. Take image classification as an example:

The Classification class in classification.h inherits from the AIBase class, implements the class definition of the image classification task, and mainly defines the pre-processing, inference, and post-processing interfaces of the image classification model. Initialize the ai2d builder to implement image preprocessing. Some variables for image classification tasks are also defined, such as classification thresholds, category names, number of categories, etc.

```c++
#ifndef _CLASSIFICATION_H
#define _CLASSIFICATION_H
#include "utils.h"
#include "ai_base.h" 

/**
 * @brief classification task
 * It mainly encapsulates the process from preprocessing, running to post-processing to give results for each frame of picture.
 */
class Classification : public AIBase
{
    public:
    /**
    * @brief Classification constructor, loads kmodel, and initializes kmodel input and output classification thresholds
    * @param kmodel_path kmodel path
    * @param image_path image path
    * @param labels the list of labels
    * @param cls_thresh classification threshold
    * @param debug_mode  0（no debug）、 1（print time）、2（print all）
    * @return None
    */
    Classification(string &kmodel_path, string &image_path,std::vector<std::string> labels, float cls_thresh,const int debug_mode);

    /**
    * @brief Classification constructor, loads kmodel, and initializes kmodel input and output classification thresholds
    * @param kmodel_path kmodel path
    * @param image_path  image path 
    * @param labels      the list of labels
    * @param cls_thresh  classification threshold
    * @param isp_shape   isp shape（chw）
    * @param vaddr       isp virtual address
    * @param paddr       isp physical address
    * @param debug_mode   0（no debug）、 1（print time）、2（print all）
    * @return None
    */
    Classification(string &kmodel_path, string &image_path,std::vector<std::string> labels,float cls_thresh, FrameCHWSize isp_shape, uintptr_t vaddr, uintptr_t paddr,const int debug_mode);
    
    /**
    * @brief Classification destructor
    * @return None
    */
    ~Classification();

    /**
    * @brief image preprocessing
    * @param ori_img image
    * @return None
    */
    void pre_process(cv::Mat ori_img);

    /**
    * @brief video preprocessing（ai2d for isp）
    * @return None
    */
    void pre_process();

    /**
    * @brief kmodel inference
    * @return None
    */
    void inference();

    /**
    * @brief postprocessing
    * @param results the result of classification
    * @return None
    */
    void post_process(vector<cls_res> &results);
    
    private:

    /**
    * @brief exp
    */
    float fast_exp(float x);

    /**
    * @brief sigmoid
    */
    float sigmoid(float x);

    std::unique_ptr<ai2d_builder> ai2d_builder_; // ai2d builder
    runtime_tensor ai2d_in_tensor_;              // ai2d input tensor
    runtime_tensor ai2d_out_tensor_;             // ai2d output tensor
    uintptr_t vaddr_;                            // isp virtual address
    FrameCHWSize isp_shape_;                     // isp shape

    float cls_thresh;      //classification threshold
    vector<string> labels; //Names of categories
    int num_class;         //Number of categories

    float* output;         
};
#endif
```

Implement the above interface in classification.cc:

```c++
#include "classification.h"

/*
Constructor for image
*/
Classification::Classification(std::string &kmodel_path, std::string &image_path,std::vector<std::string> labels_,float cls_thresh_,const int debug_mode)
:AIBase(kmodel_path.c_str(),"Classification", debug_mode)
{   
    cls_thresh=cls_thresh_;
    labels=labels_;
    num_class = labels.size();
    ai2d_out_tensor_ = this -> get_input_tensor(0);
}

/*
Constructor for video
*/
Classification::Classification(std::string &kmodel_path, std::string &image_path,std::vector<std::string> labels_,float cls_thresh_, FrameCHWSize isp_shape, uintptr_t vaddr, uintptr_t paddr,const int debug_mode)
:AIBase(kmodel_path.c_str(),"Classification", debug_mode)
{
    cls_thresh=cls_thresh_;
    labels=labels_;
    num_class = labels.size();
    vaddr_ = vaddr;
    isp_shape_ = isp_shape;
    dims_t in_shape{1, isp_shape.channel, isp_shape.height, isp_shape.width};
    ai2d_in_tensor_ = hrt::create(typecode_t::dt_uint8, in_shape, hrt::pool_shared).expect("create ai2d input tensor failed");
    ai2d_out_tensor_ = this -> get_input_tensor(0);
    Utils::resize(ai2d_builder_, ai2d_in_tensor_, ai2d_out_tensor_);
}

/*
destructor
*/
Classification::~Classification()
{
}

/*
preprocessing for image inference
*/
void Classification::pre_process(cv::Mat ori_img)
{
    //get time
    ScopedTiming st(model_name_ + " pre_process image", debug_mode_);
    std::vector<uint8_t> chw_vec;
    //bgr to rgb,hwc to chw
    Utils::bgr2rgb_and_hwc2chw(ori_img, chw_vec);
    //resize
    Utils::resize({ori_img.channels(), ori_img.rows, ori_img.cols}, chw_vec, ai2d_out_tensor_);
}

/*
preprocessing for video inference
*/
void Classification::pre_process()
{
    ScopedTiming st(model_name_ + " pre_process video", debug_mode_);
    size_t isp_size = isp_shape_.channel * isp_shape_.height * isp_shape_.width;
    auto buf = ai2d_in_tensor_.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(buf.data()), (void *)vaddr_, isp_size);
    hrt::sync(ai2d_in_tensor_, sync_op_t::sync_write_back, true).expect("sync write_back failed");
    ai2d_builder_->invoke(ai2d_in_tensor_, ai2d_out_tensor_).expect("error occurred in ai2d running");
}

/*
inference function
*/
void Classification::inference()
{
    this->run();
    this->get_output();
}

/*
exp
*/
float Classification::fast_exp(float x)
{
    union {
        uint32_t i;
        float f;
    } v{};
    v.i = (1 << 23) * (1.4426950409 * x + 126.93490512f);
    return v.f;
}

/*
sigmoid
*/
float Classification::sigmoid(float x)
{
    return 1.0f / (1.0f + fast_exp(-x));
}

/*
postprocessing function
*/
void Classification::post_process(vector<cls_res> &results)
{
    ScopedTiming st(model_name_ + " post_process", debug_mode_);
    //p_outputs_ stores a float type pointer, pointing to the output
    output = p_outputs_[0];
    cls_res b;
    //If it is multiple categories
    if(num_class > 2){
        float sum = 0.0;
        for (int i = 0; i < num_class; i++){
            sum += exp(output[i]);
        }
        b.score = cls_thresh;
        int max_index;
        //softmax
        for (int i = 0; i < num_class; i++)
        {
            output[i] = exp(output[i]) / sum;
        }
        max_index = max_element(output,output+num_class) - output; 
        if (output[max_index] >= b.score)
        {
            b.label = labels[max_index];
            b.score = output[max_index];
            results.push_back(b);
        }
    }
    else// Two categories
    {
        float pre = sigmoid(output[0]);
        if (pre > cls_thresh)
        {
            b.label = labels[0];
            b.score = pre;
        }
        else{
            b.label = labels[1];
            b.score = 1 - pre;
        }
        results.push_back(b);
    }
}
```

In the preprocessing part of the above code, some utility functions are used, which we encapsulate in utils.h:

```c++
#ifndef UTILS_H
#define UTILS_H
#include <algorithm>
#include <vector>
#include <iostream>
#include <fstream>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <nncase/functional/ai2d/ai2d_builder.h>
#include <string>
#include <string.h>
#include <cmath>
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <stdint.h>
#include <random>


using namespace nncase;
using namespace nncase::runtime;
using namespace nncase::runtime::k230;
using namespace nncase::F::k230;


using namespace std;
using namespace cv;
using cv::Mat;
using std::cout;
using std::endl;
using std::ifstream;
using std::vector;

#define STAGE_NUM 3
#define STRIDE_NUM 3
#define LABELS_NUM 1

/**
 * @brief Classification result structure
 */
typedef struct cls_res
{
    float score;//score
    string label;//result
}cls_res;

/**
 * @brief Frame shape structure
 */
typedef struct FrameSize
{
    size_t width;  // width
    size_t height; // height
} FrameSize;

/**
 * @brief Frame shape structure
 */
typedef struct FrameCHWSize
{
    size_t channel; 
    size_t height;  
    size_t width;  
} FrameCHWSize;

/**
 * @brief AI tools
 * Encapsulates commonly used functions in AI, including binary file reading, file saving, image preprocessing and other operations
 */
class Utils
{
public:
    /**
     * @brief resize image
     * @param ori_img         image
     * @param frame_size      width and height
     * @return                image of processing
     */
    static cv::Mat resize(const cv::Mat ori_img, const FrameSize &frame_size);


    /**
     * @brief bgr to rgb,hwc to chw
     * @param ori_img          image
     * @param chw_vec          data
     * @return None
     */
    static void bgr2rgb_and_hwc2chw(cv::Mat &ori_img, std::vector<uint8_t> &chw_vec);

    /*************************for ai2d ori_img process********************/
    // resize
    /**
     * @brief resize
     * @param ori_shape        image (chw)
     * @param chw_vec          data
     * @param ai2d_out_tensor  ai2d output
     * @return None
     */
    static void resize(FrameCHWSize ori_shape, std::vector<uint8_t> &chw_vec, runtime_tensor &ai2d_out_tensor);

    /**
     * @brief resize
     * @param builder          ai2d builder
     * @param ai2d_in_tensor   ai2d input
     * @param ai2d_out_tensor  ai2d output
     * @return None
     */
    static void resize(std::unique_ptr<ai2d_builder> &builder, runtime_tensor &ai2d_in_tensor, runtime_tensor &ai2d_out_tensor);

    /**
     * @brief Plot the results of a classification task onto an image
     * @param frame         
     * @param results       
     * @return None
     */
    static void draw_cls_res(cv::Mat& frame, vector<cls_res>& results);

    /**
     * @brief Draw the results of the classification task into the OSD of the screen
     * @param frame                 
     * @param results               
     * @param osd_frame_size        width and height of osd
     * @param sensor_frame_size     width and height of sensor
     * @return None
     */
    static void draw_cls_res(cv::Mat& frame, vector<cls_res>& results, FrameSize osd_frame_size, FrameSize sensor_frame_size);
};
#endif
```

You can add other tool functions if needed. The following is the utils.cc file to complete the implementation of the tool class interface:

```c++
#include <iostream>
#include "utils.h"

using std::ofstream;
using std::vector;

auto cache = cv::Mat::zeros(1, 1, CV_32FC1);

cv::Mat Utils::resize(const cv::Mat img, const FrameSize &frame_size)
{
    cv::Mat cropped_img;
    cv::resize(img, cropped_img, cv::Size(frame_size.width, frame_size.height), cv::INTER_LINEAR);
    return cropped_img;
}

void Utils::bgr2rgb_and_hwc2chw(cv::Mat &ori_img, std::vector<uint8_t> &chw_vec)
{
    // for bgr format
    std::vector<cv::Mat> bgrChannels(3);
    cv::split(ori_img, bgrChannels);
    for (auto i = 2; i > -1; i--)
    {
        std::vector<uint8_t> data = std::vector<uint8_t>(bgrChannels[i].reshape(1, 1));
        chw_vec.insert(chw_vec.end(), data.begin(), data.end());
    }
}

void Utils::resize(FrameCHWSize ori_shape, std::vector<uint8_t> &chw_vec, runtime_tensor &ai2d_out_tensor)
{
    // build ai2d_in_tensor
    dims_t in_shape{1, ori_shape.channel, ori_shape.height, ori_shape.width};
    runtime_tensor ai2d_in_tensor = host_runtime_tensor::create(typecode_t::dt_uint8, in_shape, hrt::pool_shared).expect("cannot create input tensor");

    auto input_buf = ai2d_in_tensor.impl()->to_host().unwrap()->buffer().as_host().unwrap().map(map_access_::map_write).unwrap().buffer();
    memcpy(reinterpret_cast<char *>(input_buf.data()), chw_vec.data(), chw_vec.size());
    hrt::sync(ai2d_in_tensor, sync_op_t::sync_write_back, true).expect("write back input failed");

    // run ai2d
    // ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, typecode_t::dt_uint8, typecode_t::dt_uint8};
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param { false, 30, 20, 400, 600 };
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {114, 114, 114}};
    ai2d_resize_param_t resize_param{true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    dims_t out_shape = ai2d_out_tensor.shape();
    ai2d_builder builder { in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param };
    builder.build_schedule();
    builder.invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");
}

void Utils::resize(std::unique_ptr<ai2d_builder> &builder, runtime_tensor &ai2d_in_tensor, runtime_tensor &ai2d_out_tensor)
{
    // run ai2d
    ai2d_datatype_t ai2d_dtype{ai2d_format::NCHW_FMT, ai2d_format::NCHW_FMT, ai2d_in_tensor.datatype(), ai2d_out_tensor.datatype()};
    ai2d_crop_param_t crop_param { false, 30, 20, 400, 600 };
    ai2d_shift_param_t shift_param{false, 0};
    ai2d_pad_param_t pad_param{false, {{0, 0}, {0, 0}, {0, 0}, {0, 0}}, ai2d_pad_mode::constant, {114, 114, 114}};
    ai2d_resize_param_t resize_param{true, ai2d_interp_method::tf_bilinear, ai2d_interp_mode::half_pixel};
    ai2d_affine_param_t affine_param{false, ai2d_interp_method::cv2_bilinear, 0, 0, 127, 1, {0.5, 0.1, 0.0, 0.1, 0.5, 0.0}};

    dims_t in_shape = ai2d_in_tensor.shape();
    dims_t out_shape = ai2d_out_tensor.shape();
    builder.reset(new ai2d_builder(in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param));
    builder->build_schedule();
    builder->invoke(ai2d_in_tensor,ai2d_out_tensor).expect("error occurred in ai2d running");
}


void Utils::draw_cls_res(cv::Mat& frame, vector<cls_res>& results)
{
    double fontsize = (frame.cols * frame.rows * 1.0) / (300 * 250);
    if (fontsize > 2)
    {
        fontsize = 2;
    }

    for(int i = 0; i < results.size(); i++)
    {   
        std::string text = "class: " + results[i].label + ", score: " + std::to_string(round(results[i].score * 100) / 100.0).substr(0, 4);

        cv::putText(frame, text, cv::Point(1, 40), cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(255, 255, 0), 2);
        std::cout << text << std::endl;
    }
}

void Utils::draw_cls_res(cv::Mat& frame, vector<cls_res>& results, FrameSize osd_frame_size, FrameSize sensor_frame_size)
{
    double fontsize = (frame.cols * frame.rows * 1.0) / (1100 * 1200);
    for(int i = 0; i < results.size(); i++)
    {   
        std::string text = "class: " + results[i].label + ", score: " + std::to_string(round(results[i].score * 100) / 100.0).substr(0, 4);
        cv::putText(frame, text, cv::Point(1, 40), cv::FONT_HERSHEY_SIMPLEX, 0.8, cv::Scalar(255, 255, 255, 0), 2);
        std::cout << text << std::endl;
    }
}
```

In order to facilitate debugging, we have encapsulated the timing class ScopedTiming in scoped_timing.hpp to count the time consumption during the life cycle of this class instance.

```c++
#include <chrono>
#include <string>
#include <iostream>

/**
 * @brief Timing class
 * Statistics of the time spent during the life cycle of this type of instance
 */
class ScopedTiming
{
public:
    /**
     * @brief ScopedTiming Constructor, initializes the timing object name and starts timing
     * @param info Timing object name
     * @param enable_profile Whether to start timing
     * @return None
     */
    ScopedTiming(std::string info = "ScopedTiming", int enable_profile = 1)
    : m_info(info), enable_profile(enable_profile)
    {
        if (enable_profile)
        {
            m_start = std::chrono::steady_clock::now();
        }
    }

    /**
     * @brief ScopedTiming destructs, ends timing, and prints the time taken
     * @return None
     */ 
     ~ScopedTiming()
    {
        if (enable_profile)
        {
            m_stop = std::chrono::steady_clock::now();
            double elapsed_ms = std::chrono::duration<double, std::milli>(m_stop - m_start).count();
            std::cout << m_info << " took " << elapsed_ms << " ms" << std::endl;
        }
    }

private:
    int enable_profile;                            // Whether to count time
    std::string m_info;                            // Timing object name
    std::chrono::steady_clock::time_point m_start; // Timing start time
    std::chrono::steady_clock::time_point m_stop;  // Timing end time
};
```

main.cc is the main code that implements board-end reasoning. It mainly implements parsing incoming parameters, printing instructions, and realizing reasoning in two different branches. If the second parameter entered is the inference image path, the image_proc function is called for image inference; if None is passed in, the video_proc function is called for video stream inference.

- Static graph inference code

```C++
void image_proc_cls(string &kmodel_path, string &image_path,vector<string> labels,float cls_thresh ,int debug_mode)
{
    cv::Mat ori_img = cv::imread(image_path);
    int ori_w = ori_img.cols;
    int ori_h = ori_img.rows;
    //Create task class instance
    Classification cls(kmodel_path,image_path,labels,cls_thresh,debug_mode);
    //preprocessing
    cls.pre_process(ori_img);
    //inference
    cls.inference();
    vector<cls_res> results;
    //postprocessing
    cls.post_process(results);
    Utils::draw_cls_res(ori_img,results);
    cv::imwrite("result_cls.jpg", ori_img);
    
}
```

The above code is the static image inference code part in main.cc. It first initializes the cv::Mat object ori_img from the image path, then initializes the Classification instance cls, calls the cls preprocessing function pre_process, the reasoning function reference, the post-processing function post_process, and finally calls draw_cls_res in utils.h draws the result on the picture and saves it as result_cls.jpg. If you need to modify the pre- and post-processing parts, you can modify them in Classification.cc. If you want to add other tool methods, you can define them in utils and implement them in utils.cc.

- For the video stream inference code, please refer to the example 2 part of the **SDK compilation chapter**. The core code for AI development is:

```c++
Classification cls(kmodel_path,labels,cls_thresh, {3, ISP_CHN1_HEIGHT, ISP_CHN1_WIDTH}, reinterpret_cast<uintptr_t>(vbvaddr), reinterpret_cast<uintptr_t>(dump_info.v_frame.phys_addr[0]), debug_mode);
vector<cls_res> results;
results.clear();
cls.pre_process();
cls.inference();
cls.post_process(results);
```

For ease of use, we have encapsulated the video stream processing part. You can refer to the sample code: <https://github.com/kendryte/K230_training_scripts/tree/main/end2end_cls_doc>.The vi_vo.h file in k230_code in tree/main/end2end_cls_doc)> and the specific implementation in main.cc.

- k230_code/k230_deploy/CMakeLists.txt description

This is the CMakeLists script in the k230_code/k230_deploy directory .txt set the compiled C++ file and the generated elf executable name, as follows:

```Shell
set(src main.cc utils.cc ai_base.cc classification.cc) 
set(bin main.elf)

include_directories(${PROJECT_SOURCE_DIR})：#Add the project's root directory to the header file search path.
include_directories(${nncase_sdk_root}/riscv64/rvvlib/include)：#Add the header file directory of the nncase RISC-V vector library.
include_directories(${k230_sdk}/src/big/mpp/userapps/api/)：#Add the user application API header file directory in the k230 SDK.
include_directories(${k230_sdk}/src/big/mpp/include)：#Add the general header file directory of k230 SDK.
include_directories(${k230_sdk}/src/big/mpp/include/comm)：#Add a directory of communication-related header files.
include_directories(${k230_sdk}/src/big/mpp/userapps/sample/sample_vo)：#Added sample VO (video output) application header files directory.

link_directories(${nncase_sdk_root}/riscv64/rvvlib/): #Add linker search path pointing to the directory of the nncase RISC-V vector library.
add_executable(${bin} ${src}): #Create an executable file taking as input the list of source files set previously.
target_link_libraries(${bin} ...)：#Set the libraries that the executable needs to link to. Various libraries are listed in the list, including nncase-related libraries, k230 SDK libraries, and some other libraries.
target_link_libraries(${bin} opencv_imgproc opencv_imgcodecs opencv_core zlib libjpeg-turbo libopenjp2 libpng libtiff libwebp csi_cv): #Link some OpenCV related libraries and some other libraries into the executable.
install(TARGETS ${bin} DESTINATION bin): #Install the generated executable file into the specified target path (bin directory).
```

- k230_code/CMakeLists.txt description

```Shell
cmake_minimum_required(VERSION 3.2)
project(nncase_sdk C CXX)

set(nncase_sdk_root "${PROJECT_SOURCE_DIR}/../../nncase/")
set(k230_sdk ${nncase_sdk_root}/../../../)
set(CMAKE_EXE_LINKER_FLAGS "-T ${PROJECT_SOURCE_DIR}/cmake/link.lds --static")

# set opencv
set(k230_opencv ${k230_sdk}/src/big/utils/lib/opencv)
include_directories(${k230_opencv}/include/opencv4/)
link_directories(${k230_opencv}/lib ${k230_opencv}/lib/opencv4/3rdparty)

# set mmz
link_directories(${k230_sdk}/src/big/mpp/userapps/lib)

# set nncase
include_directories(${nncase_sdk_root}/riscv64)
include_directories(${nncase_sdk_root}/riscv64/nncase/include)
include_directories(${nncase_sdk_root}/riscv64/nncase/include/nncase/runtime)
link_directories(${nncase_sdk_root}/riscv64/nncase/lib/)

add_subdirectory(k230_deploy)
```

This is the CMakeLists .txt script in the k230_code directory. The script focuses on the following parts:

```Shell
set(nncase_sdk_root "${PROJECT_SOURCE_DIR}/../../nncase/"):#Set nncase directory
set(k230_sdk ${nncase_sdk_root}/../../../):#The directory where k230_sdk is located is currently obtained from the third-level parent directory of the nncase directory.
set(CMAKE_EXE_LINKER_FLAGS "-T ${PROJECT_SOURCE_DIR}/cmake/link.lds --static"):#Set the link script path and place the link script under k230_code/cmake
...
add_subdirectory(k230_deploy): #Add the subdirectory of the project to be compiled. If you want to compile your own project, you can replace this line
```

- k230_code/build_app.sh description

```Shell
#!/bin/bash
set -x

# set cross build toolchain
export PATH=$PATH:/opt/toolchain/riscv64-linux-musleabi_for_x86_64-pc-linux-gnu/bin/

clear
rm -rf out
mkdir out
pushd out
cmake -DCMAKE_BUILD_TYPE=Release                 \
      -DCMAKE_INSTALL_PREFIX=`pwd`               \
      -DCMAKE_TOOLCHAIN_FILE=cmake/Riscv64.cmake \
      ..

make -j && make install
popd

# The generated main.elf can be found in the k230_bin folder under the k230_code directory.
k230_bin=`pwd`/k230_bin
rm -rf ${k230_bin}
mkdir -p ${k230_bin}

if [ -f out/bin/main.elf ]; then
      cp out/bin/main.elf ${k230_bin}
fi
```

#### Code compilation

Copy the k230_code folder in the project to src/big/nncase in the k230_sdk directory, execute the compilation script, and compile the C++ code into the main.elf executable.

```Shell
# Execute in the k230_SDK root directory
make CONF=k230_canmv_defconfig prepare_memory
# Return to the current project directory and grant permissions
chmod +x build_app.sh
./build_app.sh
```

#### Prepare the ELF file

The files required for later deployment steps include:

1. k230_code/k230_bin/main.elf;

### Network configuration and file transfer

There are two ways to copy the files to be used to the board. One is the TFTP transfer method and the other is the SCP transfer method.

#### TFTP file transfer

- Windows system PC network configuration

Control Panel - > Network and Sharing Center - > Change Adapter Settings - > Ethernet Network Card - > Right-click Properties - > Selected (TCP/IPv4) - > Properties

Configure the IP address, mask, gateway, and DNS server address:

![net_config_0](../zh/images/net_config_0.png)

- Development board network configuration

Go to the little core command line and execute:

```Shell
# Check if there is eth0
ifconfig
# Configure the development board IP and be in the same network segment as the PC
ifconfig eth0 192.168.1.22
ifconfig
```

- Tool: TFTPD64

Install the TFTP communication tool, download address:<https://bitbucket.org/phjounin/tftpd64/downloads/>

Start TFTPD64 and configure the directory and service NIC for files to be transferred

![net_config_1](../zh/images/net_config_1.png)

- ShareFs instructions

```Shell
# Enter the root directory of the small core
cd /
ls
# The sharefs directory is a directory shared by both large and small cores, so files copied from the small core to the sharefs directory are also visible to the large core.
```

- File transfer

```Shell
# The following code is executed on the small core serial port
# Transfer the files in the directory where the tftpd64 configuration file is stored on the PC to the current directory of the development board
tftp -g -r your_file 192.168.1.2
# Transfer the files in the current directory of the development board to the directory where the tftpd64 configuration file is stored.
tftp -p -r board_file 192.168.1.2
```

#### SCP file transfer

In the Linux system, the PC is normally connected to the network, and the development board can be connected to other network ports under the gateway where the PC is located through the network cable, and file transfer can be realized through the scp command.

Power on the development board, enter the COM interface of large and small cores, and execute the scp transmission command on the little core:

```Shell
# Copy files from PC to development board
scp username@IP:file_path_PC file_path_board
#copy folder from PC to development board
scp -r username@IP:folder_path_PC folder_path_board
# Copy files from development board to PC
scp file_path_board username@IP:file_path_PC 
# Copy folder from development board to PC
scp -r folder_path_board username@IP:folder_path_PC 
```

### K230 side deployment

#### Board-side deployment process

Follow the file transfer process configured in the previous section, enter /sharefs on the little core interface on MobaXterm, and create a test folder:

```Shell
cd /sharefs
mkdir test_cls
cd test_cls
```

Copy the prepared files in the model training and testing section and the elf files prepared in the C++ code compilation section to the development board.

```shell
test_cls
 ├──best.kmodel
 ├──labels.txt
 ├──main.elf
 ├──test.jpg
```

Enter the /sharefs/test_cls directory at the big core COM port,

To perform static graph inference, execute the following code (note: the code needs to be executed under the big core, and the file copy needs to be completed under the little core):

```Shell
# "Instructions for passing parameters during model inference："
# "<kmodel_path> <image_path> <labels_txt> <debug_mode>"
# "Options:"
# "  kmodel_path     Kmodel path\n"
# "  image_path      image path/None\n"
# "  labels_txt      Category label file path\n"
# "  debug_mode      0(no debug)、1(print time)、2(print all information)\n"
main.elf best.kmodel test.jpg labels.txt 2 
```

To perform camera video stream inference, execute the following code:

```Shell
main.elf best.kmodel None labels.txt 2 
```

#### Effect of deployment on the board

Static graph reasoning diagram:

![image_inference](../zh/images/image_inference.jpg)

Video streaming inference diagram:

![video_inference](../zh/images/video_inference.jpg)

## Frequently Asked Questions (FAQs)

### TF boot failed with exit code 13

Problem: TF card boot fails with exit code 13 error

Answer: The reasons are as follows: 1. The file error in the boot media. 2. The startup pin is set incorrectly.

### Bootrom boot error code

Question: What does the bootrom boot error code mean?

When bootROM fails to boot, it will print an error similar to the following boot failed with exit code 19, the last number is the cause of the error, and the common error meaning is as follows

| value   | meaning                                                |
| ---- | --------------------------------------------------- |
| 13   | The boot media contains a file error                                |
| 19   | Boot media initialization failed, such as not inserting an SD card                |
| 17   | The OTP requirement must be a secure image, but the files on the media are non-secure images |

### perf use

Question: How is perf compiled and what hardware events are supported?

A: The reference image with PERF function is linked below<https://kvftsfijpo.feishu.cn/file/LJjpbwxnzowI9RxvL0NcEK73nkf?from=from_copylink>

When perf, you can use the RAW event, such as perf stat -e r12, and the perf tool compile command as follows

```bash
cd src/little/linux/tools
make CROSS_COMPILE=riscv64-unknown-linux-gnu- ARCH=riscv perf V=1 WERROR=0
#copy perf/perf file to board
```

Special note: Versions prior to 1.1 have the following modifications

```bash
#src/little/linux/arch/riscv/boot/dts/kendryte/k230_evb.dtsi add
pmu_thead: pmu_thead {
    interrupt-parent = <&cpu0_intc>;
    interrupts = <17>;
    compatible = "thead,c900_pmu";
};
#src/little/linux/arch/riscv/configs/k230_evb_defconfig  add
CONFIG_KALLSYMS=y
CONFIG_KALLSYMS_ALL=y
CONFIG_PERF_EVENTS=y
CONFIG_DEBUG_PERF_USE_VMALLOC=y
CONFIG_KUSER_HELPERS=y
CONFIG_DEBUG_INFO=y
CONFIG_FRAME_POINTER=y
```

```bash
[root@canaan ~ ]#perf list hw cache  > a ;cat a
  branch-instructions OR branches                    [Hardware event]
  branch-misses                                      [Hardware event]
  bus-cycles                                         [Hardware event]
  cache-misses                                       [Hardware event]
  cache-references                                   [Hardware event]
  cpu-cycles OR cycles                               [Hardware event]
  instructions                                       [Hardware event]
  ref-cycles                                         [Hardware event]
  stalled-cycles-backend OR idle-cycles-backend      [Hardware event]
  stalled-cycles-frontend OR idle-cycles-frontend    [Hardware event]
  L1-dcache-load-misses                              [Hardware cache event]
  L1-dcache-loads                                    [Hardware cache event]
  L1-dcache-store-misses                             [Hardware cache event]
  L1-dcache-stores                                   [Hardware cache event]
  L1-icache-load-misses                              [Hardware cache event]
  L1-icache-loads                                    [Hardware cache event]
  LLC-load-misses                                    [Hardware cache event]
  LLC-loads                                          [Hardware cache event]
  LLC-store-misses                                   [Hardware cache event]
  LLC-stores                                         [Hardware cache event]
  dTLB-load-misses                                   [Hardware cache event]
  dTLB-loads                                         [Hardware cache event]
  dTLB-store-misses                                  [Hardware cache event]
  dTLB-stores                                        [Hardware cache event]
  iTLB-load-misses                                   [Hardware cache event]
  iTLB-loads                                         [Hardware cache event]
[root@canaan ~ ]#

```

### Big Core runs Vector Linux

Question: How does Big Core run Linux with Vector?

Answer: make CONF=k230_evb_only_linux_defconfig ; The compiled image, the big core runs Linux with vector by default.

### Big core serial port ID

Question: How to modify the serial port ID of the big core?

Answer: The configuration file below configs CONFIG_RTT_CONSOLE_ID stands for the big core serial port ID, modify it to the correct value.

### uboot command line

How to compile the version that can enter the uboot command line

Answer: The configuration file below configs CONFIG_QUICK_BOOT stands for fast, modify it to CONFIG_QUICK_BOOT=n to generate a command-line version that can be entered into uboot.

### How to start slowly and start faster

Answer: Enter the uboot command line and execute the following command:

```bash
setenv quick_boot true;saveenv;reset;
```

### How Linux modifies the last partition size

Answer: You can use the parted tool to dynamically modify the size of the last partition, refer to the following command:

```bash
umount /sharefs/
parted   -l /dev/mmcblk1
parted  -a minimal  /dev/mmcblk1  resizepart 4  31.3GB
mkfs.ext2 /dev/mmcblk1p4
mount /dev/mmcblk1p4 /sharefs
#reference log
[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   487MB   268MB   fat16        fat32appfs


[root@canaan ~ ]#umount /sharefs/
[root@canaan ~ ]#parted  -a minimal  /dev/mmcblk1  resizepart 4  31.3GB
Information: You may need to update /etc/fstab.

[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   31.3GB  31.1GB  fat16        fat32appfs


[root@canaan ~ ]#mkfs.ext2 /dev/mmcblk1p4
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
1896832 inodes, 7586811 blocks
379340 blocks (5%) reserved for the super user
First data block=0
Maximum filesystem blocks=8388608
232 block groups
32768 blocks per group, 32768 fragments per group
8176 inodes per group
Superblock backups stored on blocks:
32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208, 4096000
[root@canaan ~ ]#parted   -l /dev/mmcblk1
Model: SD SD32G (sd/mmc)
Disk /dev/mmcblk1: 31.3GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags:

Number  Start   End     Size    File system  Name        Flags
 1      10.5MB  31.5MB  21.0MB               rtt
 2      31.5MB  83.9MB  52.4MB               linux
 3      134MB   218MB   83.9MB  ext4         rootfs
 4      218MB   31.3GB  31.1GB  ext2         fat32appfs


[root@canaan ~ ]#mount /dev/mmcblk1p4 /sharefs/
[  332.688642] EXT4-fs (mmcblk1p4): mounted filesystem without journal. Opts: (null)
[root@canaan ~ ]#df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                73.5M     60.9M     10.2M  86% /
devtmpfs                 41.7M         0     41.7M   0% /dev
tmpfs                    51.8M         0     51.8M   0% /dev/shm
tmpfs                    51.8M     56.0K     51.7M   0% /tmp
tmpfs                    51.8M     36.0K     51.7M   0% /run
/dev/mmcblk1p4           28.5G     20.0K     27.0G   0% /sharefs
[root@canaan ~ ]#

```

### How to modify bootargs

Answer: Method 1: Modify bootargs using env file. For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi；
```

Method 2: Enter the uboot command line and modify bootargs with reference to the following command.

```bash
setenv bootargs  "root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 earlycon=sbi" ;saveenv;reset;
```

### How to view bootargs

Answer: Method 1: Under linux, enter cat /proc/cmdline to view

```bash
[root@canaan ~ ]#cat /proc/cmdline
root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan ~ ]#

```

Method 2: Linux command line input dmesg | grep command view

```bash
[root@canaan ~ ]#dmesg | grep  command
[    0.000000] Kernel command line: root=/dev/mmcblk0p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS0,115200 crashkernel=256M-:128M earlycon=sbi
[root@canaan
```

### The little core is modified by default serial port

Answer: At present, the little core serial port in the SDK defaults to 0, if you need to modify it to other serial ports (such as serial port 2), please refer to the following to modify:

Modification 1: Refer to the following to modify the uboot device tree (e.g. arch/riscv/dts/k230_evb.dts):

```bash
aliases {
        uart2 = &serial2;
    };

    chosen {
        stdout-path = "uart2:115200n8";
    };

    serial2: serial@91402000 {
    compatible = "snps,dw-apb-uart";
    reg = <0x0 0x91402000 0x0 0x400>;
    clock-frequency = <50000000>;
    clock-names = "baudclk";
    reg-shift = <2>;
    reg-io-width = <4>;
    u-boot,dm-pre-reloc;
};
```

Modification 2: Refer to the following to modify the Linux device tree (e.g. arch/riscv/boot/dts/kendryte/k230_evb.dts)

```bash
aliases {
        serial2 = &uart2;
    };
chosen {
        stdout-path = "serial2";
    };

&uart2 {
    status = "okay";
};
```

Modification 3: Modify bootargs using env files (see 2.10).

 For example, you can add the following content to the board/common/env/default.env file:

```bash
bootargs=root=/dev/mmcblk1p3 loglevel=8 rw rootdelay=4 rootfstype=ext4 console=ttyS2,115200 earlycon=sbi；
```

### How to completely recompile the SDK

Answer: After updating and modifying the SDK source code, or after modifying the SDK source code, it is recommended to enter the following command to completely recompile the SDK.

```bash
make clean; make;
```

Special note: The SDK does not support multi-process compilation, do not add multi-process compilation options like -j32.
