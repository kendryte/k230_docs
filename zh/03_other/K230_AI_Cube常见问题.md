# AI Cube常见问题解答

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

[TOC]

## 1 AI Cube使用问题

问题1：AI Cube打开后遇到license提示。

![license_error](images/license_error.jpg)

答：AI Cube内部采用license校验机制，进入AI Cube需要当月的授权license。用户可以向<Developersupport@canaan-creative.com>发送邮件申请当月授权license，我们的专业团队会为您提供license支持。

问题： 运行AI Cube时发生闪退，无响应。

答：遇到闪退问题时首先要按照[AI Cube用户指南](https://kendryte-download.canaan-creative.com/developer/common/AI_Cube_V1.2%E7%94%A8%E6%88%B7%E6%8C%87%E5%8D%97.pdf)排查是否正确安装Nvidia显卡驱动及dotnet。

其次可能引起原因如下：

* AI Cube首次启动需要等待，用户可进入AI Cube目录手动执行AI Cube.exe来加速打开。

* 系统system32文件夹中缺少libomp.dll。请参考[github issue](https://github.com/kendryte/nncase/issues/451)解决该问题

* dotnet环境变量配置错误。用户可以在系统环境变量部分添加环境变量，例如"C:\Program Files\dotnet\sdk\7.0.406"

![dotnet环境变量](images/dotnet_env_var.png)
