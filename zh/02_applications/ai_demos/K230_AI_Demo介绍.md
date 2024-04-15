# K230 AI Demo介绍

![cover](../tutorials/images/canaan-cover.png)

版权所有©2023北京嘉楠捷思信息技术有限公司

<div style="page-break-after:always"></div>

## 免责声明

您购买的产品、服务或特性等应受北京嘉楠捷思信息技术有限公司（“本公司”，下同）及其关联公司的商业合同和条款的约束，本文档中描述的全部或部分产品、服务或特性可能不在您的购买或使用范围之内。除非合同另有约定，本公司不对本文档的任何陈述、信息、内容的正确性、可靠性、完整性、适销性、符合特定目的和不侵权提供任何明示或默示的声明或保证。除非另有约定，本文档仅作为使用指导参考。

由于产品版本升级或其他原因，本文档内容将可能在未经任何通知的情况下，不定期进行更新或修改。

## 商标声明

![logo](../tutorials/images/logo.png)“嘉楠”和其他嘉楠商标均为北京嘉楠捷思信息技术有限公司及其关联公司的商标。本文档可能提及的其他所有商标或注册商标，由各自的所有人拥有。

**版权所有 © 2023北京嘉楠捷思信息技术有限公司。保留一切权利。**
非经本公司书面许可，任何单位和个人不得擅自摘抄、复制本文档内容的部分或全部，并不得以任何形式传播。

<div style="page-break-after:always"></div>

## K230 AI Demo

### 概述

K230 AI Demo集成了人脸、人体、手部、车牌、单词续写、语音、dms等模块，包含了分类、检测、分割、识别、跟踪、单目测距等多种功能，给客户提供如何使用K230开发AI相关应用的参考。

### 硬件环境

- `CanMV-K230-V1.x / CanMV-K230-V2.x / K230-UNSIP-LPx-EVB-V1.x`

### 源码位置

源码路径位于`k230_sdk/src/reference/ai_poc`，目录结构如下：

```shell
# AI Demo子目录（eg：bytetrack、face_detection等）中有详细的Demo说明文档
.
├── anomaly_det
├── build_app.sh
├── bytetrack
├── cmake
├── CMakeLists.txt
├── crosswalk_detect
├── dec_ai_enc
├── demo_mix
├── distraction_reminder
├── dms_system
├── dynamic_gesture
├── eye_gaze
├── face_alignment
├── face_detection
├── face_emotion
├── face_gender
├── face_glasses
├── face_landmark
├── face_mask
├── face_mesh
├── face_parse
├── face_pose
├── face_verification
├── falldown_detect
├── finger_guessing
├── fitness
├── head_detection
├── helmet_detect
├── kws
├── licence_det
├── licence_det_rec
├── llamac
├── nanotracker
├── object_detect_yolov8n
├── ocr
├── person_attr
├── person_detect
├── person_distance
├── pose_detect
├── pose_det_rtsp_plug
├── pphumanseg
├── puzzle_game
├── segment_yolov8n
├── self_learning
├── shell
├── smoke_detect
├── space_resize
├── sq_hand_det
├── sq_handkp_class
├── sq_handkp_det
├── sq_handkp_flower
├── sq_handkp_ocr
├── sq_handreco
├── traffic_light_detect
├── translate_en_ch
├── tts_zh
├── vehicle_attr
├── virtual_keyboard
└── yolop_lane_seg
```

kmodel、image及相关依赖路径位于`k230_sdk/src/big/kmodel/ai_poc`，目录结构如下：

``` shell
.
├── images
│   ├── 000.png
│   ├── 1000.jpg
│   ├── 1024x1111.jpg
│   ├── 1024x1331.jpg
│   ├── 1024x624.jpg
│   ├── 1024x768.jpg
│   ├── 333.jpg
│   ├── 640x340.jpg
│   ├── bus.jpg
│   ├── bytetrack_data
│   ├── car.jpg
│   ├── cw.jpg
│   ├── falldown_elder.jpg
│   ├── helmet.jpg
│   ├── hrnet_demo.jpg
│   ├── identification_card.png
│   ├── input_flower.jpg
│   ├── input_hd.jpg
│   ├── input_ocr.jpg
│   ├── input_pd.jpg
│   ├── licence.jpg
│   ├── person.png
│   ├── road.jpg
│   ├── smoke1.jpg
│   └── traffic.jpg
├── kmodel
│   ├── anomaly_det.kmodel
│   ├── bytetrack_yolov5n.kmodel
│   ├── cropped_test127.kmodel
│   ├── crosswalk.kmodel
│   ├── eye_gaze.kmodel
│   ├── face_alignment.kmodel
│   ├── face_alignment_post.kmodel
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection_hwc.kmodel
│   ├── face_emotion.kmodel
│   ├── face_gender.kmodel
│   ├── face_glasses.kmodel
│   ├── face_landmark.kmodel
│   ├── face_mask.kmodel
│   ├── face_parse.kmodel
│   ├── face_pose.kmodel
│   ├── face_recognition.kmodel
│   ├── flower_rec.kmodel
│   ├── gesture.kmodel
│   ├── hand_det.kmodel
│   ├── handkp_det.kmodel
│   ├── hand_reco.kmodel
│   ├── head_detection.kmodel
│   ├── helmet.kmodel
│   ├── hifigan.kmodel
│   ├── human_seg_2023mar.kmodel
│   ├── kws.kmodel
│   ├── licence_reco.kmodel
│   ├── LPD_640.kmodel
│   ├── nanotrack_backbone_sim.kmodel
│   ├── nanotracker_head_calib_k230.kmodel
│   ├── ocr_det_int16.kmodel
│   ├── ocr_det.kmodel
│   ├── ocr_rec_int16.kmodel
│   ├── ocr_rec.kmodel
│   ├── person_attr_yolov5n.kmodel
│   ├── person_detect_yolov5n.kmodel
│   ├── person_pulc.kmodel
│   ├── recognition.kmodel
│   ├── traffic.kmodel
│   ├── translate_decoder.kmodel
│   ├── translate_encoder.kmodel
│   ├── vehicle_attr_yolov5n.kmodel
│   ├── vehicle.kmodel
│   ├── yolop.kmodel
│   ├── yolov5n-falldown.kmodel
│   ├── yolov5s_smoke_best.kmodel
│   ├── yolov8n_320.kmodel
│   ├── yolov8n_640.kmodel
│   ├── yolov8n-pose.kmodel
│   ├── yolov8n_seg_320.kmodel
│   ├── yolov8n_seg_640.kmodel
│   ├── zh_fastspeech_1_f32.kmodel
│   ├── zh_fastspeech_1.kmodel
│   └── zh_fastspeech_2.kmodel
└── utils
    ├── Asci0816.zf
    ├── bfm_tri.bin
    ├── bu.bin
    ├── dict_6625.txt
    ├── dict_ocr_16.txt
    ├── dict_ocr.txt
    ├── file
    ├── HZKf2424.hz
    ├── jiandao.bin
    ├── libsentencepiece.a
    ├── llama.bin
    ├── memory.bin
    ├── ncc_code.bin
    ├── pintu.bin
    ├── reply_wav
    ├── shang.bin
    ├── shitou.bin
    ├── tokenizer.bin
    ├── trans_src.model
    ├── trans_tag.model
    ├── wav_play.elf
    ├── xia.bin
    ├── you.bin
    └── zuo.bin
```

### 编译及运行程序

#### a.自编译上板镜像

- 确保已根据[k230 sdk官方说明](https://github.com/kendryte/k230_sdk)构建docker容器，并构建镜像

- 进入k230_sdk/src/reference/ai_poc

- 执行build_app.sh脚本，会将kmodel、images、utils、shell、elf统一拷贝生成到k230_bin文件夹

- 将k230_bin整个文件夹拷贝到板子，在大核上执行sh脚本即可运行相应AI demo

（1）确保已根据[k230 sdk官方说明](https://github.com/kendryte/k230_sdk)构建docker容器并构建镜像

（2）进入k230_sdk/src/reference/ai_poc

```bash
cd k230_sdk/src/reference/ai_poc
```

（3）编译单个AI Demo（以人脸检测为例）

```shell
./build_app.sh face_detection
```

**注**：执行build_app.sh前，确保已经准备好依赖，即`k230_sdk/src/big/kmodel/ai_poc`下已经有相应kmodel、images、utils

```bash
#若是没有上述依赖，执行一下命令下载
cd k230_sdk
make prepare_sourcecode
```

生成以下文件：

```bash
k230_bin/
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
```

将k230_bin/整个文件夹拷贝到板子，在大核上执行sh脚本即可运行相应AI demo

```shell
#进入开发板小核sharefs目录
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

#进入开发板大核sharefs目录
cd /sharefs/k230_bin/face_detection
#执行相应脚本即可运行人脸检测
#详细人脸检测说明可以参考k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

（4）编译所有AI Demo（若只需编译某个demo，无需执行该步骤）

```shell
./build_app.sh
```

生成以下文件：

```bash
k230_bin/
......
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
......
└── llamac
    ├── llama.bin
    ├── llama_build.sh
    ├── llama_run
    └── tokenizer.bin
......
```

将k230_bin/整个文件夹拷贝到板子，在大核上执行sh脚本即可运行相应AI demo

```shell
#进入小核sharefs目录
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

#进入大核sharefs目录
cd /sharefs/k230_bin/face_detection
#执行相应脚本即可运行人脸检测
#详细人脸检测说明可以参考k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

#### b.直接下载官网上板镜像

（1）确保已根据[k230 sdk官方说明](https://github.com/kendryte/k230_sdk)构建docker容器

（2）从[官网资源库](https://developer.canaan-creative.com/resource)下载镜像

（3）环境准备

```bash
cd k230_sdk
make prepare_sourcecode #（若之前已执行，请忽略）
make mpp
make cdk-user
#根据使用的开发板型号，分别执行不同的命令
#若是型号是CanMV-K230-V1.x，执行以下命令
make CONF=k230_canmv_defconfig prepare_memory
#若是型号是CanMV-K230-V2.x，执行以下命令
make CONF=k230_canmv_v2_defconfig prepare_memory
#若是型号是K230-xxx-xxx-EVB-V1.x，执行以下命令
make CONF=k230_evb_defconfig prepare_memory
cd k230_sdk/src/reference/ai_poc
```

（4）编译单个AI Demo（以人脸检测为例）

```shell
./build_app.sh face_detection
```

**注**：执行build_app.sh前，确保已经准备好依赖，即`k230_sdk/src/big/kmodel/ai_poc`下已经有相应kmodel、images、utils

```bash
#若是没有上述依赖，执行一下命令下载
cd k230_sdk
make prepare_sourcecode
```

生成以下文件：

```bash
k230_bin/
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
```

将k230_bin整个文件夹拷贝到板子，在大核上执行sh脚本即可运行相应AI demo

```shell
#进入开发板小核sharefs目录
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

#进入开发板大核sharefs目录
cd /sharefs/k230_bin/face_detection
#执行相应脚本即可运行人脸检测
#详细人脸检测说明可以参考k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

（5）编译所有AI Demo（若只需编译某个demo，无需执行该步骤）

```shell
./build_app.sh
```

生成以下文件：

```bash
k230_bin/
......
├── face_detection
│   ├── 1024x624.jpg
│   ├── face_detect_image.sh
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_detection.elf
│   └── face_detect_isp.sh
......
└── llamac
    ├── llama.bin
    ├── llama_build.sh
    ├── llama_run
    └── tokenizer.bin
......
```

将k230_bin整个文件夹拷贝到板子，在大核上执行sh脚本即可运行相应AI demo

```shell
#进入小核sharefs目录
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

#进入大核sharefs目录
cd /sharefs/k230_bin/face_detection
#执行相应脚本即可运行人脸检测
#详细人脸检测说明可以参考k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```
