# K230 ISP初始化配置指南

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

## 前言

### 概述

本文档主要是指导用户对K230 ISP进行初始化配置。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 图像调试工程师
- 技术支持工程师
- 软件开发工程师

### 修订记录

| 文档版本号  | 修改说明                           | 修改者 | 日期       |
|------------|-----------------------------------|--------|------------|
| V1.0       | 初版                              | 荣 坚 | 2024-01-24 |
| V1.1       | 更新部分参数描述                   | 荣 坚 | 2024-04-28 |

## 1. K230 ISP初始化配置概述

在图像调优后，所形成的ISP配置参数，需要写入相应sensor的初始化配置文件中。开机时，ISP会自动调用这些配置文件中的设置完成初始化。当模块自适应功能使能时，ISP将按该模块自适应功能的设置进行运行。
ISP初始化配置有三个文件：xml、manaual.json和auto.json，若sensor可选不同分辨率，则不同分辨率下都需有这三个配置文件。这些配置文件都存放于\k230_sdk\src\big\mpp\userapps\src\sensor\config目录下。

## 2. xml文件

### 2.1 概述

可使用K230 ISP Calibration Tool(K230ISPCalibrationTool.exe)生成xml文件，工具中所有模块的校准都需要完成，以得到完整的校准数据。

xml文件中包含的数据有两个来源：

- 使用Calibration Tool得到的校准结果
- 工具发布包中提供的专业数据文件

校准数据及校准参数文件存放的位置，如下表所示：

| 校准数据                       | 生成方法或参数文件 | 校准参数文件位置 |
| ------                        | ----------------- | -------------------------------------------------------- |
| Auto White Balance            | Calibration Tool | sensor/lens/sample/AWB/ |
| Black Level Calibration       | Calibration Tool | sensor/lens/sample/BlackLevel/ |
| Chromatic Aberration          | Calibration Tool | sensor/lens/sample/Calibration Tool/ChromaticAberration/ |
| Color Calibration             | Calibration Tool | sensor/lens/sample/Calibration Tool/ColorReproduction/ |
| Defect Pixel Color Correction | dpcc_para.txt    | sensor/lens/sample/Calibration Tool/DefectPixel/ |
| Auto Exposure Calibration     | aec_para.m; k_para.txt | sensor/lens/sample/Calibration Tool/ExposureCalibration/ |
| HDR                           | hdr_para.txt     | sensor/lens/sample/Calibration Tool/HDR/ |
| Lens Shading Correction       | Calibration Tool | sensor/lens/sample/Calibration Tool/LensShading/ |
| Noise Calibration             | Calibration Tool | sensor/lens/sample/Calibration Tool/Noise/ |
| Photo Response Linearity      | degamma_para.txt | sensor/lens/sample/Calibration Tool/PhotoResponseLinearity/ |

### 2.2 为校准参数创建校准文件文件夹

请按照以下步骤为每个分辨率创建文件夹：

1. 使用sensor名称创建文件夹 (如：/OV9732)
1. 使用镜头名称创建文件夹 (如：/2MP)
1. 使用样本名称创建文件夹 (如：/01_30)
1. 为每个校准功能创建子文件夹 (如下图所示)<br/>
![创建文件夹](images/xml_04.png)<br/>
1. 将校准参数文件复制到相应的参数文件夹中

对于每个分辨率，示例如下:

- sensor
  - lens
    - sample
      - AWB
        - AWB parameters.txt
        - AWB parameters.mat
      - BlackLevel
        - BLS parameters.txt
      - ...

### 2.3 使用K230 ISP Calibration Tool生成xml文件

将所有校准参数文件复制到相应文件夹后, 打开K230 ISP Calibration Tool，用其生成xml文件。

如下图所示，点击主界面“7. XML Generator”按钮：

![主界面](images/xml_01.png)

弹出如图所示“XML Generator”对话框：

![选取生成XML文件](images/xml_02.png)

在“Data Location”栏中选择正确的标定目录地址，在“Sensor”选择创建的sensor文件夹，“Lens”选择栏中选择创建的镜头文件夹，“Data”栏中选择创建的样本文件夹。

在“Resolution”栏中输入图片正确的Width和Height，“Format”栏中选择“XML”, “Creator”栏中输入创建者名称，然后点击“Manually Generate”，即可在所选的镜头文件夹下生成“XML”子目录，该目录中将生成.xml文件。

![XML文件夹](images/xml_03.png)

将生成的xml文件，按K230 SDK代码中输入的xml名称改名后(如ov9732-1280x720.xml)，放入config目录下,即可被K230 SDK正确调用。

### 2.4 AWB参数K_Factor

在xml文件中awb子段中有一个K_Factor参数需要另行标定和手动填入。该参数反馈了摄像模组的感光灵敏度。

在AWB算法中，环境为outdoor的判别为: Exp*K_Factor <=0.12（Exp为曝光量）。

比如以2000 lux为outdoor与transition的环境照度分割点，获取对应该照度的曝光值(ET \* gain)， 则可计算：K_Factor = 0.12 / (ET\*gain)。

## 3. manual.json文件

manual.json文件需手动创建。请参考imx335-2592x1944_manual.json文件创建所需sensor分辨率的manual.json文件。

### 3.1 CHdrv2

#### 3.1.1 功能描述

该模块为未包含在其它ISP模块下的HDR mode参数的设置。

#### 3.1.2 主要参数

| 参数        | 类型及取值范围      | 描述                       |
| ----------- | ------------------- | -------------------------- |
| base_frame  | int 0~1        | 0: S帧为参考帧; <br/>1: L帧为参考帧。<br/>推荐设置为0. |
| bls_out     | int[4]         | Black level out <br/>默认配置为[0,0,0,0], 设置值基于ISP 12bits       |
| bypass      | bool           |  false: 经过HDR模块 <br/>true: 不经过HDR模块      |
| bypass_select | int 0~2      | 0: HDR模块输出L帧; <br/>1: HDR模块输出S帧; <br/>2: HDR模块输出VS帧 |
| color_weight  | int[3] 0~255 | color_weight <br/> stitch_color_weight0+stitch_color_weight1*2+stitch_color_weight2=256 <br/> 建议设置为[255, 0, 1] |
| enable        | bool         | false: HDR不使能 <br/>true: HDR使能      |
| extend_bit    | int[2] -1~8  | 扩展bit位 <br/>  [L/S帧融合, LS/VS帧融合] <br/> 建议设置为[-1,-1], 自动计算；0 ~ 8为手动设置值。 |
| ratio         | float[3] 1.0~256.0 |  曝光量比值 <br/> [long/short, short/very short, very short/exposure 3]  |
| sensor_type   | int 0~6      | 0,1,2: L_12+S_12+VS_12 <br/>3: LS_16+VS_12 <br/>4,6: L_12+S_12 <br/> 5: L_12+VS_12       |
| stitching_mode| int 0~1      |  0: 线性合成模式; <br/> 1: 非线性合成模式      |
| trans_range   | float\[6][2] 0.0~1.0 |  合成区间的起始值与终止值<br/> 参考帧像素低于起始值，合成帧像素为较长帧；<br/> 参考帧像素高于终止值，合成帧像素为较短帧；<br/> 参考真像素位于两者之间，合成帧为较长帧与较短帧的融合。<br/> [[L+S_ref(L)_start, L+S_ref(L)_end], <br/> [LS+VS_ref(LS)_start, LS+VS_ref(LS)_end], <br/> [L+S_ref(S)_start, L+S+ref(S)_end], <br/> [LS+VS_ref(VS)_start, LS+VS_ref(VS)_end], <br/> [LSVS+E3_ref(LSVS)_start, LSVS+E3_ref(LSVS)_end], <br/> [LSVS+E3_ref(E3)_start, LSVS+E3_ref(E3)_end]]      |

上表中：

| 帧号        |  描述                       |
| -----------|------------------ |
| L帧 | (曝光时长)长帧 |
| S帧 | (曝光时长)短帧 |
| VS帧 | (曝光时长)非常短帧 |
| LS帧 | L帧与S帧融合后的帧 |
| LSVS帧 | LS帧与VS帧融合后的帧 |

请注意，K230 HDR模式下，K230 CSI（Camera serial interface）模块不支持Hsync在Vsync之前的sensor数据模式，且各帧（L/S/VS）Vsync拉高(有效数据输出)时不能有交叠。

### 3.2 CGreenEqu

请参考《K230 ISP图像调优指南》第3.7章节。

### 3.3 CRgbIR

#### 3.3.1 功能描述

该模块为针对RGBIR sensor的输入处理设置.

#### 3.3.2 主要参数

| 参数        | 类型及取值范围      | 描述                       |
| --------- | -------------- | --------------- |
|  bit      | int       | 12, 固定值 |
| ccmatrix  | float[12] | 3x4色彩转换矩阵，将RGBIR值转换为RGB值 |
| dpcc_mid_th | int     | DPCC通道中阈值值 |
| dpcc_th   | int       | DPCC通道阈值 |
| enable    | bool      | false: RGBIR子模块不使能 <br/>true: RGBIR子模块使能 |
| gain      | int[3]    | R/G/B通道增益 <br/> 默认设置为[1,1,1] |
| ir_threshold | int    |  IR高值阈值 <br/> 如果IR值高于该值，IR色彩影响因子为0. |
| irbayer_pattern | int | RGBIR排列类型 <br/> 0: BGGIR <br/> 2: RGGIR <br/> K230 仅支持RGGIR和BGGIR两种排列类型, 请将RGBIR sensor的数据输出设置为该两种类型其中的一种。|
| l_threshold | int     | IR低值阈值 <br/> 如果IR值低于该值，IR色彩影响因子为1. |
| out_rgb_pattern | int | 输出RGB数据排列类型 <br/> 3: BGGR <br/> 无需更改。|

### 3.4 CManualWb

请参考《K230 ISP图像调优指南》第3.12章节。

### 3.5 CCcm

请参考《K230 ISP图像调优指南》第3.13章节。

### 3.6 CDgain

请参考《K230 ISP图像调优指南》第3.3章节。

### 3.7 CCpdv1

请参考《K230 ISP图像调优指南》第3.19章节。

### 3.8 Bls

#### 3.8.1 功能描述

该模块为设置black level。默认bls功能为打开。

#### 3.8.2 主要参数

| 参数        | 类型及取值范围      | 描述    |
| --------- | -------------- | --------------- |
| bls        | int[4] | Black level <br/>[bls_r,bls_gr,bls_gb,bls_b]。<br/>目前驱动仅支持各通道配置相同的黑电平，设置值基于ISP 12bits |

### 3.9 CGamma64

请参考《K230 ISP图像调优指南》第3.14章节。

### 3.10 CDpcc

请参考《K230 ISP图像调优指南》第3.8章节。

### 3.11 CDpf

请参考《K230 ISP图像调优指南》第3.9章节。

### 3.12 CLscv2

请参考《K230 ISP图像调优指南》第3.2章节。

### 3.13 CWdrv4

请参考《K230 ISP图像调优指南》第3.6章节。

### 3.14 C3dnrv3_1

请参考《K230 ISP图像调优指南》第3.10章节。

### 3.15 CCproc

请参考《K230 ISP图像调优指南》第3.18章节。

### 3.16 CEEv1

#### 3.16.1 功能描述

该模块包含了CA、DCI和EE三个子块。

#### 3.16.2 主要参数

请参考《K230 ISP图像调优指南》第3.15（EE）、3.16（CA）和3.17（DCI）章节。

### 3.17 CDmscv2

#### 3.17.1 功能描述

该模块包含了CAC和DMSC两个子块。

#### 3.17.2 主要参数

CAC参数设置请参考《K230 ISP图像调优指南》第3.20章节。
DMSC参数设置请参考《K230 ISP图像调优指南》第3.11章节。

## 4. auto.json文件

auto.json文件需手动创建。请参考imx335-2592x1944_auto.json文件创建所需sensor分辨率的auto.json文件。

### 4.1 AdaptiveAe

#### 4.1.1 功能描述

该模块为AE控制和AE自适应功能的参数设置。

#### 4.1.2 主要参数

| 参数            | 类型及取值范围 | 描述                                                   |
| --------------- | -------------- | ------------------------------------------------------ |
| enable          | bool           | 自动曝光使能开关。<br/>false: 关闭自动曝光 <br/>true : 使能自动曝光    |
| semMode  | int 0~2  | 场景模式 <br/>0: 场景评估关闭模式 <br/>1: 场景评估固定模式 <br/>2: 场景评估动态模式    |
| antiFlickerMode | Int 0~3        | 抗工频干扰工作模式 <br/>0: Off<br/>1: 50Hz<br/>2: 60Hz<br/>3: User defined |
| setPoint  | float 0~255.0  | 设置AE的亮度目标值 |
| tolerance  | float 0~100.0  | 设置AE的亮度目标值百分比锁定范围  |
| dampOver        | float 0~1.0    | 阻尼因子，用于平滑过曝时的AE收敛 |
| dampOverGain    | float 0~128.0  | AE过曝时clip范围外的收敛加速增益因子，值越大，收敛越快 |
| dampOverRatio   | float 1.0~4.0  | AE过曝时clip范围外比例因子，值越小，收敛越快 |
| dampUnder       | float 0~1.0    | 阻尼因子，用于平滑欠曝时的AE收敛 |
| dampUnderGain   | float 0~16.0   | AE欠曝时clip范围外的收敛加速增益因子，值越大，收敛越快 |
| dampUnderRatio  | float 0~1.0    | AE欠曝时clip范围比例因子，值越大，收敛越快 |
| motionFilter  | float 0~1.0  | 运动变化平滑参数，用于计算AE场景评估自适应模式下的运动因子 |
| motionThreshold  | float 0~1.0 | 运动判别阈值     |
| targetFilter  | float 0~1.0 | AE的亮度目标值变化平滑系数，值越大变化越快 |
| lowLightLinearRepress  | float[20] 0~1.0   | 线性模式下，当前增益阶数对应的目标亮度压制比例  |
| lowLightLinearGain  | float[20] 0~255.0   | 线性模式下，当前增益阶数对应的增益值 |
| lowLightLinearLevel  | int 0~19   | 线性模式下总的增益阶数 |
| lowLightHdrRepress  | float[20] 0~1.0   | 宽动态模式下，当前增益阶数对应的目标亮度压制比例    |
| lowLightHdrGain  | float[20] 0~255.0   | 宽动态模式下，当前增益阶数对应的增益值 |
| lowLightHdrLevel  | int 0~16  | 宽动态模式下总的增益阶数 |
| wdrContrastMax | float 0~255.0   | AE场景评估自适应模式下计算AE setpoint的最大对比度值  |
| wdrContrastMin  | float 0~255.0   | AE场景评估自适应模式下计算AE setpoint的最小对比度值    |
| frameCalEnable          | bool           | 曝光设置帧间隔使能开关。<br/>true : 使能曝光设置帧间隔功能 <br/>false: 关闭曝光设置帧间隔功能   |
| autoHdrEnable | bool        | true: HDR mode下，自动计算当前帧HDR ratio<br/>false: HDR mode下，使用固定的HDR ratio |
| roiNumber  | int   |  当前ROI窗口序号   |
| roiWindow  | float (fx,fy,fw,fh,weight) | 当前ROI窗口的起始点坐标(x,y)、宽高和亮度计算权重 |
| expV2WindowWeight | float[32x32] 0~255  | 各子块曝光权重 |

### 4.2 Awbv2

### 4.2.1 功能描述

该模块为awb自适应功能的参数设置。

### 4.2.2 主要参数

| 参数        | 类型及取值范围      | 描述                       |
| --------- | -------------- | --------------- |
| enable      | bool  | true : 使能AWB <br/> false: 关闭AWB |
| mode   | int 0,1  |  0: AWB <br/> 1: AWB METEDATA |
| useCcMatrix | bool  | true : 使能CCM 自适应 <br/>false: 关闭CCM自适应 |
| useCcOffset | bool  | true : 使能CCM offset自适应 <br/> false: 关闭CCM offset自适应  |
| useDamping  | bool  | true : 使能AWB阻尼变化 <br/> false: 关闭AWB阻尼变化 |
| roiNumber   | int   |  当前ROI窗口序号   |
| roiWindow   | float (fx,fy,fw,fh,weight) | 当前ROI窗口的起始点坐标(x,y)、宽高和AWB计算权重 |

### 4.3 Af

#### 4.3.1 功能描述

该模块为AF功能的参数设置。该模块暂未生效。

#### 4.3.2 主要参数

| 参数        | 类型及取值范围      | 描述                       |
| --------- | -------------- | --------------- |
| enable | bool | false: 关闭AF  <br/>true : 使能AF |
| mode| int | 0: 普通AF模式  <br/> (计划开发其它AF模式) |
| weightWindow  | float[3] 0~255.0 | 设置用于锐度计算的三个统计值窗口的权重值 |
| cMotionThreshold | float 0~1.0 | 暂未使用，将用于运动检测 |
| cPointsOfCurve | int 1~20| AF爬坡算法等分数量。该值越大，聚焦速度越慢；该值越小，聚焦速度越快，但移动步长过大会造成一定聚焦不准的情况。 |
| cStableTolerance | float 0~1.0 | AF从锁定状态进入失焦状态的阈值。该值越小，越容易失焦进入重新聚焦状态。 |
| focalFilter | float[5] 0~1023 | 暂未使用 |
| shapFilter | float[5] 0~1023 | 暂未使用 |
| focalStableThreshold | float 0~1.0 | 聚焦进入锁定状态的阈值。该值越小，越难进入锁定状态 |
| maxFocal | int 0~1023 | AF标定的最大马达位置 |
| minFocal | int 0~1023 | AF标定的最小马达位置 |
| cMseTolerance | float 0~1.0 | 暂未使用 |
| cPdConfThreshold  | float 0~1023.0  | 未使用 |
| PdFocal  | int -254~254 | 未使用 |
| PdDistance  | int 1~254 | 未使用 |
| PdShiftThrehold | float 0~1.0 | 未使用 |
| PdStablecountMax | uint8 1~10 | 未使用 |
| PdROIIndex | uint8 0~48 | 未使用 |

### 4.4 ALscv2

#### 4.4.1 功能描述

该模块为LSC自适应功能的参数设置。

#### 4.4.2 主要参数

| 参数        | 类型及取值范围      | 描述     |
| --------- | -------------- | --------------- |
| enable | bool | false: 关闭ALSC  <br/>true: 使能ALSC|
| damping | float | 阻尼因子，用于平滑ALSC时的LSC曲线变化|
| interMode | int 0~2 | 0: 根据增益值自适应调节 <br/> 1: 根据色温自适应调节 <br/> 2: 根据增益值和色温自适应调节|
| hdr | bool |false: 表示该组设置为线性模式下的设置 <br/> true: 表示该组设置为HDR模式下的设置。|
| gain | float[20] | 各阶对应的增益值 |
| strength | float[20] 0~1.0 | 各阶增益值对应的保留LSC的强度 |

### 4.5 其它

本章节对其它自适应功能模块进行统一介绍。

这些自适应功能模块的设置参数，通常用“tables”标记引导的中括号“[]”分为两部分，在该中括号外的都为bool类型的使能参数，在该中括号内的则为参与自适应功能调节的参数。

#### 4.5.1 tables外的参数说明

这些功能模块中，在tables外通常有以下三个参数：
| 参数        | 类型      | 描述                       |
| --------- | -------------- | --------------- |
| disable | bool | 可固定设置为false|
| enable | bool | false: 关闭; true: 使能 <br/>按所需adaptive模块功能进行设置|
| forcecreate | bool | 可固定设置为true|

在A3dnrv3模块中，在tables外还有两个参数：

| 参数        | 类型      | 描述                       |
| --------- | -------------- | --------------- |
| nlm_en | bool | 非局部均值降噪使能开关，建议设置为true|
| tnr_en | bool | 时域降噪使能开关，建议设置为true|

#### 4.5.2 tables内的参数说明

在功能模块中，都有以下两个参数：

| 参数        | 类型及取值范围      | 描述                       |
| --------- | -------------- | --------------- |
| hdr | bool |false: 表示该组设置为线性模式下的设置 <br/> true: 表示该组设置为HDR模式下的设置。|
| gain | float[20] | 各阶对应的增益值 |

其它自适应功能参数，请参考《K230 ISP图像调优指南》中的相应功能章节。

“gain”从最小值（通常为1倍）到最大值，最多可被分为20阶，每阶都需在gain这个参数数组中设置对应的增益值。

需要注意的是，各个自适应模块都可根据其自适应的需要自定义不同的阶数，最大不超过20阶即可。

同一自适应功能模块中的所有参与自适应的参数，都随gain的阶数来确定其数组大小，并且每阶都应根据对应的同阶增益值大小来设置合适的值。
