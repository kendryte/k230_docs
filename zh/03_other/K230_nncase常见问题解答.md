# K230 nncase 常见问题解答

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

## 目录

[toc]

## 1. 安装 `whl`包出错

### 1.1 `xxx.whl is not a supported wheel on this platform.`

- A：升级 pip `pip install --upgrade pip`

---

## 2.编译模型时报错

### 2.1 `System.NotSupportedException: Not Supported *** op: XXX`

- A：该异常表明 `XXX`算子尚未支持，可以在[nncase Github Issue](https://github.com/kendryte/nncase/issues)中提需求。当前目录下 `***_ops.md`文档，可以查看各个推理框架中已经支持的算子。如果 `XXX`属于 `FAKE_QUANT`、`DEQUANTIZE`、`QUANTIZE`等量化相关的算子，表明当前模型属于量化模型，`nncase`目前不支持这类模型，请使用浮点模型来编译 `kmodel`。

### 2.2 `System.IO.IOException: The configured user limit (128) on the number of inotify instances has been reached, or the per-process limit on the number of open file descriptors has been reached`

- A：使用 `sudo gedit /proc/sys/fs/inotify/max_user_instances`修改128为更大的值即可。

### 2.3 `RuntimeError: Failed to initialize hostfxr.` or `RuntimeError: Failed to get hostfxr path.`

- A：需要安装dotnet-sdk-7.0，不要在`anaconda`的虚拟环境中安装。
  - Linux:

    ```shell
    sudo apt-get update
    sudo apt-get install dotnet-sdk-7.0
    ```

    如果安装完毕后仍然报错，配置`dotnet`环境变量。

    ```shell
    export DOTNET_ROOT=/usr/share/dotnet
    ```

  - Windows: 请自行查阅微软官方文档。

### 2.4 `The given key 'K230' was not present in the dictionary`

- A：需要安装nncase-kpu

  - Linux：`pip install nncase-kpu`
  - Windows：在[nncase github tags界面](https://github.com/kendryte/nncase/tags)下载对应版本的whl包，然后使用pip安装。

    > 安装nncase-kpu之前，请先检查nncase版本，然后安装与nncase版本一致的nncase-kpu。

    ```shell
    > pip show nncase | grep "Version:"
     Version: 2.8.0
    (Linux)  > pip install nncase-kpu==2.8.0
    (Windows)> pip install nncase_kpu-2.8.0-py2.py3-none-win_amd64.whl
    ```

---

## 3. 推理时报错

### 3.1 `nncase.simulator.k230.sc: not found`

或者以下情况：

> - `"nncase.simulator.k230.sc: Permision denied."`
> - `"Input/output error."`

- A：将nncase的安装路径加入到 `PATH`环境变量中，并检查一下nncase和nncase-kpu版本是否一致，如果不一致，请安装相同版本的Python包 `pip install nncase==x.x.x.x nncase-kpu==x.x.x.x`。

  ```shell
  root@a52f1cacf581:/mnt# pip list | grep nncase
  nncase                       2.1.1.20230721
  nncase-kpu                   2.1.1.20230721
  ```

---

## 4. k230开发板推理时报错

### 4.1 `data.size_bytes() == size = false (bool)`

- A：推理时输入数据有错误，与模型输入节点shape、type不匹配。当编译模型时配置了前处理相关参数，模型输入节点shape和type信息会有相应的更新。请以模型编译时配置的 `input_shape`、`input_type`为准来生成输入数据。

### 4.2 `std::bad_alloc`

- A：通常是因为内存分配失败导致的，可做如下排查。
  - 检查生成的kmodel是否超过当前系统可用内存
  - 检查App是否存在内存泄露

### 4.3 `terminate:Invalid kmodel`

加载`kmodel`代码如下时，抛出该自定义异常内容。

```CPP
interp.load_model(ifs).expect("Invalid kmodel");
```

- A：在不存在其他问题的情况下，是由于编译`kmodel`时的nncase版本与当前SDK版本不匹配导致，请按照[SDK、nncase版本对应关系](./K230_SDK_nncase版本对应关系.md)查询，并按照[更新nncase运行时库教程](./K230_SDK更新nncase运行时库指南.md)解决。
