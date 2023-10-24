# CanMV K230 教程

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

## 快速上手

## Linux+RT-smart双系统开发

## nncase开发

`nncase`是面向 AI 加速器的神经网络编译器，用于为 `Kendryte`系列芯片生成推理所需要的模型文件 `.kmodel`，并提供模型推理所需要的 `runtime lib`。

本教程主要包括以下内容：

1. 使用 `nncase`完成模型编译，生成 `kmodel`。
1. 在PC和开发板上执行 `kmodel`推理。

> Tips：
>
> 1. 本教程旨在让用户熟悉nncase的使用流程,文中模型输入数据均为随机数。实际应用场景的具体流程请参阅后续章节《AI开发》。
> 1. 官方CanMV镜像中的nncase版本可能已过时，如果需使用最新nncase，需自行更新运行时库并重新编译CanMV镜像。

### 模型编译和模拟器推理

#### 安装nncase工具链

nncase工具链包括 `nncase`和 `nncase-kpu`插件包，两者均需正确安装才可以编译出CanMV-K230所支持的模型文件。`nncase`和 `nncase-kpu`插件包均在[nncase github release](https://github.com/kendryte/nncase/releases)发布，并且依赖dotnet-7.0。

* `Linux`平台可以直接使用pip进行 `nncase`和 `nncase-kpu`插件包在线安装，Ubuntu环境下可使用 `apt`安装 `dotnet`。

    ```Python
    pip install --upgrade pip
    pip install nncase==2.3.0
    pip install nncase-kpu==2.3.0
    # nncase-2.x need dotnet-7
    sudo apt-get update
    sudo apt-get install -y dotnet-sdk-7.0
    ```

    >Tips：如果使用官方提供的CanMV镜像，必须使用2.3.0版本进行模型编译

* **`Windows`平台仅支持`nncase`在线安装，`nncase-kpu`需要在[nncase github release](https://github.com/kendryte/nncase/releases)手动下载安装。**
* 用户若没有Ubuntu环境, 可使用 `nncase docker`(Ubuntu 20.04 + Python 3.8 + dotnet-7.0)

    ```Python
    cd /path/to/nncase_sdk
    docker pull ghcr.io/kendryte/k230_sdk
    docker run -it --rm -v `pwd`:/mnt -w /mnt ghcr.io/kendryte/k230_sdk /bin/bash -c "/  bin/bash"  
    ```

    > Tips：目前仅支持py3.6-3.10，如果pip安装失败请检查pip对应的Python版本。

#### 环境配置

使用pip安装软件包后,需将安装路径添加到PATH环境变量中。

```Python
export PATH=$PATH:/path/to/python/site-packages/
```

#### 原始模型说明

`nncase`目前支持 `tflite`、`onnx`格式的模型，更多格式的支持还在进行中。

> Tips：
>
> 1. 对于TensorFlow的`pb`模型,请参考官方文档将其转换为`tflite`格式。注意不要设置量化选项,直接输出浮点模型即可。如果模型中存在quantize和dequantize算子,则属于量化模型，目前不支持。
> 1. 对于PyTorch的`pth`等格式模型,需使用`torch.export.onnx`接口导出`onnx`格式。

#### 编译参数说明

进行模型编译前,您需要了解以下关键信息:

1. `KPU`推理使用定点运算。因此在编译模型时,必须配置量化相关参数,用于将模型从浮点转换为定点。详见 `nncase`文档中的[PTQTensorOptions](https://github.com/kendryte/nncase/blob/master/docs/USAGE_v2.md#ptqtensoroptions)说明。
1. `nncase`支持将前处理层集成到模型中，这可以减少推理时的前处理开销。相关参数和示意图见 `nncase`文档的[CompileOptions](https://github.com/kendryte/nncase/blob/master/docs/USAGE_v2.md#compileoptions)部分。

#### 编译脚本说明

本[Jupyter notebook](https://github.com/kendryte/nncase/blob/master/examples/user_guide/k230_simulate-ZH.ipynb)分步骤详细描述了使用nncase编译、推理kmodel的流程，notebook内容涵盖:

* 参数配置:介绍如何正确配置编译参数,以满足实际部署需求；
* 获取模型信息:说明从原始模型中获取网络结构、层信息等关键数据的方法；
* 设置校正集数据:阐述如何准备好校正集样本数据，包括单输入和多输入模型两种情况，以用于量化校准过程；
* 设置推理数据格式:讲解推理部署时如何配置输入数据，支持不同需求场景；
* 配置多输入模型:介绍处理多输入模型时,如何正确设置每个输入的形状、数据格式等信息；
* PC模拟器推理:说明如何在PC上利用模拟器进行编译后的kmodel推理,是验证编译效果的关键步骤；
* 比较推理结果:通过与不同框架(TensorFlow、PyTorch等)的推理结果比较,验证kmodel的正确性；

  以上步骤系统地介绍了模型编译的全流程,既适合初学者从零开始学习,也可作为经验丰富用户的参考指南。

#### 示例代码

当您阅读了Jupyter笔记本中的完整教程后，可以基于以下示例代码进行修改。

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
    # 你需要修改下面这段代码中的参数来适配你的模型。
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
  
    # 可自行修改kmodel_path,在推理时需要传入正确的kmodel_path
    kmodel_path = os.path.join(dump_path, "test.kmodel")
    with open(kmodel_path, 'wb') as f:
        f.write(kmodel)
    print("----------------end-----------------")
    return kmodel_path

if __name__ == "__main__":
    # compile kmodel single input
    model_path = "./test.tflite"
    dump_path = "./tmp_tflite"

    # 校正集的数量为2
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

#### 注意事项

当编译模型时遇到问题，可以在[FAQ](https://github.com/kendryte/nncase/blob/master/docs/FAQ_ZH.md)中查找出错log寻找解决办法，也可以在github中按照模板提[issue](https://github.com/kendryte/nncase/issues)，或者在 `nncase QQ交流群 :790699378`中直接提问。

同时，也欢迎您将您遇到的问题以及解决方案，提 `PR`到 `nncase`中，为开源工作贡献力量。

### 基于开发板进行模型推理

目前 `CanMV`支持两套开发API，`C++`和 `MicroPython`，您可以根据您的需求进行选择。

* `MicroPython`具有较低的开发门槛，用户可以直接编写类似于 `Python`的代码进行应用开发；
* `C++`具有较高的门槛，但是更具灵活性，有着更好的性能（芯片的推理性能不受语言的影响）。

在开发板上推理时，我们提供两个模块用于加速模型推理

* 基于硬件的前处理模块：`AI2D`，详细功能说明见[AI2D运行时APIs](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/ai/K230_nncase_%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.md#5-ai2d-%E8%BF%90%E8%A1%8C%E6%97%B6apisc)；
* 基于硬件的模型推理模块：`KPU`，详细功能说明见[KPU运行时APIs](https://github.com/kendryte/k230_docs/blob/main/zh/01_software/board/ai/K230_nncase_%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.md#4-kpu%E8%BF%90%E8%A1%8C%E6%97%B6apisc)；

接下来，我们将在C++代码示例中说明这两个模块如何使用，有哪些需要注意的地方。

这里以人脸检测为例，下面将对编译的目录结构，代码重要功能进行说明，完整的代码示例见 `k230_sdk/src/big/nncase/examples/image_face_detect`。

#### 目录结构

在example目录下，与模型推理相关的文件结构如下：

```C++
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

* build_app.sh：编译生成可执行文件 `image_face_detect.elf`的脚本，输出到out目录。
* CMakeLists.txt：设置编译时需要链接的库：`opencv`、`mmz`、`nncase`，在工程中仅需要修改 `add_subdirectory()`即可。
* image_face_detect：完整的人脸检测demo，其中包含了 `AI2D`、`KPU`、模型后处理等功能。

#### AI2D 配置

在 `mobile_retinaface.cc`中使用了AI2D功能中的 `Pad`和 `Resize`功能，接下来将对类 `MobileRetinaface`的构造函数进行代码块解释，这里完成了 `AI2D`的参数配置：

1. 设置 `AI2D`的输出tensor

```C++
    ai2d_out_tensor_ = input_tensor(0);
```

`input_tensor(0)`是在获取 `KPU`的输入tensor。这一步就是在将 `KPU`的输入tensor同时设置为`AI2D`的输出tensor，将这两部分硬件连接起来使用。

1. 设置 `AI2D`的参数

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

首先需要设置`AI2D`的基础参数，包括输入格式、输出格式、输入类型和输出类型，具体参见文档。
然后设置`AI2D`功能参数，在人脸检测中仅使用了 `Pad`和 `Resize`功能，但是仍需要显式设置其他功能(`crop`，`shift`，`affine`)的参数，只将第一个参数设置为 `false`，其余参数符合语法即可。

1. 生成 `AI2D`相关指令

```C++
    ai2d_builder_.reset(new ai2d_builder(in_shape, out_shape, ai2d_dtype, crop_param, shift_param, pad_param, resize_param, affine_param));
    ai2d_builder_->build_schedule();
```

首先需要创建`ai2d_builder`对象，如果已经存在该对象，那么需要使用reset函数来更新其中的参数，之后调用 `build_schedule()`功能即可完成指令生成。

到此，`AI2D`的配置就已经结束了，接下来我们来看一下 `KPU`相关的配置。

#### KPU 配置

在 `model.cc`中进行了 `KPU`相关的配置，主要是提前分配输入tensor的内存分配及设置。我们来看类 `Model`的构造函数：

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

1. 读取模型

```C++
std::ifstream ifs(kmodel_file, std::ios::binary);
interp_.load_model(ifs).expect("load_model failed");
```

首先将文件路径转换为流，然后通过 `load_model()` 进行流式加载。

1. 输入tensor内存分配

```C++
auto desc = interp_.input_desc(i);
auto shape = interp_.input_shape(i);
auto tensor = host_runtime_tensor::create(desc.datatype, shape, hrt::pool_shared).expect("cannot create input tensor");
```

这里根据从模型中获取到的shape信息以及类型信息，创建一个空的tensor。

> Q：为什么是空的tensor，而不是直接填充数据进去呢？
>
> A：可以先看一下 `AI2D`设置输出tensor时我们做了什么，没错，空的tensor是为了接收AI2D的输出数据，因此没有必要直接设置数据。但是，如果不使用 `AI2D`模块，那么这里是需要设置输入数据的，例如：
>
> auto tensor = host_runtime_tensor::create(
> desc.datatype, shape, { (gsl::bytes*)vector.data(), (size_t)vector.size()  },
> true,  hrt::pool_shared).expect("cannot create input tensor");

到此，`KPU`相关的配置也完成了，接下来我们看如何执行这两部分模块。

#### 启动推理

在 `main.cc`的 `ai_proc`函数中进行了推理，启动推理的代码为：

```Python
model.run(reinterpret_cast<uintptr_t>(vaddr), reinterpret_cast<uintptr_t>(paddr));
auto result = model.get_result();
```

`result`即为模型的输出结果，而在 `run()`中调用了 `AI2D`和 `KPU`。

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

其中 `preprocess`函数启动了 `AI2D`的推理 `invoke`，`kpu_run`函数中启动了 `kpu`的推理，当然在开始推理之前，需要设置 `AI2D`的输入，这里直接通过设定物理地址的方式，将其输入数据绑定在输入设备上。

> Tips：postprocess() 函数调用了模型的后处理部分，由于不同模型后处理各不相同，并且相同模型还有不同版本后处理的区别，在进行完整的推理之前，
>
> 请先确保您的后处理C++代码的结果和您的Python模型后处理结果是一致的！！！
>
> 请先确保您的后处理C++代码的结果和您的Python模型后处理结果是一致的！！！
>
> 请先确保您的后处理C++代码的结果和您的Python模型后处理结果是一致的！！！
>

## AI开发
