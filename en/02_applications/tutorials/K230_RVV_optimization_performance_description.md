# K230 RVV Performance Optimization Description

![cover](../../../zh/02_applications/tutorials/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/tutorials/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no organization or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[toc]

<div style="page-break-after:always"></div>

## Preface

### Overview

This document mainly introduces the impact of RVV on model inference performance.

### Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Revision History

| Document Version | Modification Description | Modifier | Date       |
| ---------------- | ------------------------ | -------- | ---------- |
| V1.0             | Initial Version          | Yang Haoqi | 2023/08/04 |

## 1. Overview

In recent years, the rapid development of the AI field has led to the emergence of various neural network models and new operators. However, the iteration cycle of AI chips is much longer compared to AI models, and many of these new operators cannot directly use AI chips for inference acceleration. At the same time, some old operators are also not suitable for inference acceleration using AI chips. Therefore, the CPU becomes the execution carrier for these operators, which means that the performance of the CPU will become a factor affecting the final performance during model deployment. The RVV extension is an important means to improve the performance of RISC-V CPUs. The K230 uses the Xuantie C908 dual-core processor, where the large core has the RVV1.0 extension feature, which can significantly improve the performance during CPU operator inference.

To perform model inference on the K230, a model in the `.kmodel` format is required. The `.kmodel` format is a compiled model format by [nncase](https://github.com/kendryte/nncase) for `ONNX` and `TFLite` models, suitable for development boards produced by the Company and related cooperative enterprises. nncase supports common neural network operators, but some operators cannot be accelerated for inference by the K230 and must use the CPU for inference.

## 2. RVV Application Scenarios

Currently, the most widely researched and applied neural network is the `Transformer`, which has a model structure significantly different from `CNN`. Many AI chips designed based on `CNN` cannot fully accelerate the `Transformer`. Below is the execution of operators in the `Decoder` model of `Transformer` with and without RVV optimization enabled.

### 2.1 Without RVV Optimization

| stackvm tensor op | count | time consumption(ms) | percentage(%) |
| ----------------- | ----- | -------------------- | ------------- |
| softmax           | 5     | 1749.61              | 88.6574       |
| where             | 4     | 199.432              | 10.1058       |
| EXTCALL           | 65    | 16.099               | 0.815779      |
| layer_norm        | 7     | 5.81                 | 0.294408      |
| gather            | 2     | 0.393                | 0.0199144     |
| STLOCAL           | 212   | 0.391                | 0.019813      |
| LDC_I4            | 241   | 0.388                | 0.019661      |
| reduce_arg        | 1     | 0.336                | 0.017026      |
| reshape           | 26    | 0.281                | 0.014239      |
| LDLOCAL           | 149   | 0.26                 | 0.0131749     |
| LDNULL            | 106   | 0.166                | 0.00841166    |
| LDTENSOR          | 29    | 0.103                | 0.00521929    |
| LEA_GP            | 58    | 0.097                | 0.00491525    |
| LDDATATYPE        | 29    | 0.07                 | 0.00354709    |
| LDARG             | 5     | 0.008                | 0.000405381   |
| RET               | 1     | 0.004                | 0.000202691   |
| LDTUPLE           | 1     | 0.003                | 0.000152018   |
| total             | 941   | 1973.45              | 100           |

### 2.2 With RVV Optimization

| stackvm tensor op | count | time consumption(ms) | percentage(%) |
| ----------------- | ----- | -------------------- | ------------- |
| softmax           | 5     | 25.722               | 55.6175       |
| EXTCALL           | 65    | 16.179               | 34.9831       |
| layer_norm        | 7     | 0.967                | 2.0909        |
| where             | 4     | 0.912                | 1.97198       |
| gather            | 2     | 0.39                 | 0.84328       |
| LDC_I4            | 241   | 0.386                | 0.834631      |
| STLOCAL           | 212   | 0.379                | 0.819495      |
| reduce_arg        | 1     | 0.34                 | 0.735167      |
| LDLOCAL           | 149   | 0.259                | 0.560024      |
| reshape           | 26    | 0.243                | 0.525428      |
| LDNULL            | 106   | 0.17                 | 0.367583      |
| LEA_GP            | 58    | 0.103                | 0.222712      |
| LDTENSOR          | 29    | 0.103                | 0.222712      |
| LDDATATYPE        | 29    | 0.076                | 0.164331      |
| LDARG             | 5     | 0.011                | 0.0237848     |
| RET               | 1     | 0.005                | 0.0108113     |
| LDTUPLE           | 1     | 0.003                | 0.00648677    |
| total             | 941   | 46.248               | 100           |

### 2.3 Performance Analysis and Description

In the model inference above, the KPU unit of K230 does not support hardware inference acceleration for `softmax`, `layer_norm`, `where`, `gather`, `reduce_arg`, and `reshape`, so the C908 is used for inference. RVV optimization has been completed for `softmax`, `layer_norm`, and `where`, with significant performance improvement.

Below are the pie charts showing the proportion of each operator's time consumption in model inference before and after RVV optimization.

<div class="mermaid">
pie
    title Without RVV Optimization
    "softmax" : 88.6574
    "where" : 10.1058
    "EXTCALL" : 0.815779
    "layer_norm" : 0.294408
    "gather" : 0.0199144
    "STLOCAL" : 0.019813
    "LDC_I4" : 0.019661
    "reduce_arg" : 0.017026
    "reshape" : 0.014239
    "LDLOCAL" : 0.0131749
    "LDNULL" : 0.00841166
    "LDTENSOR" : 0.00521929
    "LEA_GP" : 0.00491525
    "LDDATATYPE" : 0.00354709
    "LDARG" : 0.000405381
    "RET" : 0.000202691
    "LDTUPLE" : 0.000152018
</div>

<div class="mermaid">
pie
    title With RVV Optimization
    "softmax" : 55.6175
    "EXTCALL" : 34.9831
    "layer_norm" : 2.0909
    "where" : 1.97198
    "gather" : 0.84328
    "LDC_I4" : 0.834631
    "STLOCAL" : 0.819495
    "reduce_arg" : 0.735167
    "LDLOCAL" : 0.560024
    "reshape" : 0.525428
    "LDNULL" : 0.367583
    "LEA_GP" : 0.222712
    "LDTENSOR" : 0.222712
    "LDDATATYPE" : 0.164331
    "LDARG" : 0.0237848
    "RET" : 0.0108113
    "LDTUPLE" : 0.00648677
</div>

Below is the performance comparison of related operators before and after RVV optimization.

![RVV](../../../zh/02_applications/tutorials/images/RVV_optimize_performance.jpg)

From the comparison results above, it can be seen that enabling RVV optimization can greatly improve the inference performance of CPU operators, significantly reducing the overall model inference time (1973 ms to 46 ms). After RVV optimization, the `softmax` operator time is reduced to 25 ms, the `layer_norm` operator time is reduced to 0.97 ms, and the `where` operator time is reduced to 0.91 ms. The overall model inference time is shortened by 97.6%, which has high application value in actual model deployment.

### 2.4 RVV Optimization Example

#### 2.4.1 RVV Code

For specific implementation, please refer to `layer_norm` in `nncase` [here](https://github.com/kendryte/nncase/blob/master/src/Native/src/kernels/stackvm/optimized/riscv64/layer_norm.cpp). It requires some knowledge of RV instructions and V extension instructions.

The calculation formula for `layer_norm` is as follows:

```plaintext
y= (x−E[x])/sqrt(Var[x]+ϵ)∗γ+β
```

The overall calculation process can be found in the `layernorm_impl` function. For better readability, the RVV optimized code in this process is split into three parts:

1. Calculate `E[x]`, refer to the `get_mean` function.
1. Calculate `Var[x]`, refer to the `get_var` function.
1. Perform layer_norm calculation according to the formula above, refer to the `layer_norm_update1` function.

Since multiplication is less time-consuming than division, the formula in step 3 is transformed to use `rsqrt` instead of `sqrt` and multiplication instead of division.

#### 2.4.2 Core Code Explanation

Below is an explanation of the core code in `get_mean`. This code segment implements the loop load and summation of the array at a1, stores the summation result in v0, and finally stores the average value in ret. It uses RVV's vector load and vector accumulate instructions to achieve summation, thereby improving computational performance.

```plaintext
"vle32.v v8, (a1);"   // Load 32-bit vector at a1 address into v8 register
"sub a0,a0, t0;"      // a0 -= t0, used for loop control count
"slli t1, t0, 2;"     // t1 = t0 << 2, as each float32 is 4 bytes, so address increases by 4*t0
"vfredsum.vs v0,v8,v0;"  // v0 += v8, vector accumulate sum into v0

"add a1, a1, t1;"      // a1 += t1, update load address
"bnez a0, XXXXXX%=;"   // If a0 != 0, jump to loop start address
"vfmv.f.s f0, v0;"     // Move vector accumulate result from v0 to f0
"fcvt.s.w f1, %[avl];"  // Convert avl to float and save to f1
"fdiv.s %[ret], f0, f1;" // ret = f0/f1, i.e., calculate average
```

#### 2.4.3 Adding RVV Operator Process

In the following process, paths are based on [nncase](https://github.com/kendryte/nncase) as the root directory

1. Function Declaration: src/Native/src/kernels/stackvm/optimized/opt_ops.h
1. Operator Implementation:
   - General Optimization: src/Native/src/kernels/stackvm/optimized
   - x86 Optimization: src/Native/src/kernels/stackvm/optimized/x86_64
   - RVV Optimization: src/Native/src/kernels/stackvm/optimized/riscv64
1. Logical Call: src/Native/src/kernels/stackvm/tensor_ops.cpp
1. Modify CMakeLists: src/Native/src/kernels/stackvm/optimized/CMakeLists.txt
   - General Optimization: Add source file name in line 15
   - Platform-specific Optimization: Add source file name in line 44

### 2.5 Tips

If you encounter operators that are not yet supported by RVV optimization and need support, feel free to raise issues and PRs on [nncase](https://github.com/kendryte/nncase/issues).
