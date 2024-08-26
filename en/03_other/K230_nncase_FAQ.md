# K230 nncase FAQ

![cover](../../zh/03_other/images/canaan-cover.png)

Copyright ©2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the company") and its affiliates. All or part of the products, services, or features described in this document may not be within your scope of purchase or use. Unless otherwise agreed in the contract, the company makes no express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](images/logo.png)、 "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.
Without the company's written permission, no unit or individual may excerpt, copy any part or all of the contents of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[toc]

## 1. Error Installing whl Package

### 1.1 `xxx.whl is not a supported wheel on this platform.`

- A：Upgrade pip `pip install --upgrade pip`

---

## 2.Error Compiling Model

### 2.1 `System.NotSupportedException: Not Supported *** op: XXX`

- A: This exception indicates that the `XXX` operator is not yet supported. You can submit a feature request in the [nncase Github Issue](https://github.com/kendryte/nncase/issues). For a list of supported operators, please refer to the `***_ops.md` document in the [nncase repository](https://github.com/kendryte/nncase/tree/release/2.0/docs). If `XXX` belongs to FAKE_QUANT, `DEQUANTIZE`, `QUANTIZE`, etc., it indicates that the current model is a quantized model, which `nncase` currently does not support. Please use a floating-point model to compile the `kmodel`.

### 2.2 `System.IO.IOException: The configured user limit (128) on the number of inotify instances has been reached, or the per-process limit on the number of open file descriptors has been reached`

- A: Modify the value of 128 to a larger value using `sudo gedit /proc/sys/fs/inotify/max_user_instances`.

### 2.3 `RuntimeError: Failed to initialize hostfxr.` or `RuntimeError: Failed to get hostfxr path.`

- A: You need to install dotnet-sdk-7.0. Do not install it in the `anaconda` virtual environment.
  - Linux:

    ```shell
    sudo apt-get update
    sudo apt-get install dotnet-sdk-7.0
    ```

    If the error persists after installation, configure the `dotnet` environment variable.

    ```shell
    export DOTNET_ROOT=/usr/share/dotnet
    ```

  - Windows: Please refer to the official Microsoft documentation.

### 2.4 `The given key 'K230' was not present in the dictionary`

- A：You need to install nncase-kpu

  - Linux：`pip install nncase-kpu`
  - Windows：Download the corresponding version of the whl package from the [nncase GitHub tags page](https://github.com/kendryte/nncase/tags) and then install it using pip.

    > Before installing nncase-kpu, check the nncase version, and then install the nncase-kpu that matches the nncase version.

    ```shell
    > pip show nncase | grep "Version:"
     Version: 2.8.0
    (Linux)  > pip install nncase-kpu==2.8.0
    (Windows)> pip install nncase_kpu-2.8.0-py2.py3-none-win_amd64.whl
    ```

---

## 3. Errors During Inference

### 3.1 `nncase.simulator.k230.sc: not found`

Or the following cases:

> - `"nncase.simulator.k230.sc: Permision denied."`
> - `"Input/output error."`

- A：Add the installation path of nncase to the PATH environment variable and check if the nncase and nncase-kpu versions are consistent. If they are inconsistent, install the same version of the Python package using `pip install nncase==x.x.x.x nncase-kpu==x.x.x.x.`

  ```shell
  root@a52f1cacf581:/mnt# pip list | grep nncase
  nncase                       2.1.1.20230721
  nncase-kpu                   2.1.1.20230721
  ```

---

## 4. Errors During Inference on K230 Development Board

### 4.1 `data.size_bytes() == size = false (bool)`

- A: The input data is incorrect during inference and does not match the shape and type of the model input nodes. When configuring preprocessing parameters during model compilation, the shape and type information of the model input nodes will be updated accordingly. Please generate the input data according to the `input_shape` and `input_type` configured during model compilation.

### 4.2 `std::bad_alloc`

- A: This is usually due to memory allocation failure. The following checks can be made:
- Check if the generated kmodel exceeds the available memory of the current system.
- Check if the App has memory leaks.

### 4.3 `terminate:Invalid kmodel`

When loading the `kmodel` with the following code, this custom exception is thrown.

```CPP
interp.load_model(ifs).expect("Invalid kmodel");
```

- A: In the absence of other issues, this is due to the mismatch between the nncase version used to compile the `kmodel` and the current SDK version. Please refer to the [SDK and nncase version correspondence](./K230_SDK_nncase_version_correspondence.md) and follow the guide to [update the nncase runtime library](./K230_SDK_Updating_nncase_Runtime_Library_Guide.md) to resolve the issue.
