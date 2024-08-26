# Introduction to K230 AI Demo

![cover](../../../zh/images/canaan-cover.png)

© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or usage. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## K230 AI Demo

### Overview

The K230 AI Demo integrates modules such as face, human body, hand, license plate, word continuation, voice, DMS, etc., and includes various functions such as classification, detection, segmentation, recognition, tracking, and monocular distance measurement, providing customers with a reference on how to use K230 to develop AI-related applications.

### Hardware Environment

- `CanMV-K230-V1.x / CanMV-K230-V2.x / K230-UNSIP-LPx-EVB-V1.x`

### Source Code Location

The source code path is located at `k230_sdk/src/reference/ai_poc`, with the directory structure as follows:

```shell
# Detailed demo instructions are available in the subdirectories of AI Demo (e.g., bytetrack, face_detection, etc.)
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

The paths for kmodel, images, and related dependencies are located at `k230_sdk/src/big/kmodel/ai_poc`, with the directory structure as follows:

```shell
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

### Compiling and Running the Program

#### a. Self-Compiling Board Image

- Ensure that you have constructed the Docker container and built the image according to the [official K230 SDK instructions](https://github.com/kendryte/k230_sdk).

- Navigate to k230_sdk/src/reference/ai_poc.

- Execute the build_app.sh script, which will copy the kmodel, images, utils, and shell to the k230_bin folder.

- Copy the entire k230_bin folder to the board and execute the sh script on the main core to run the corresponding AI demo.

(1) Ensure that you have constructed the Docker container and built the image according to the [official K230 SDK instructions](https://github.com/kendryte/k230_sdk).

(2) Navigate to k230_sdk/src/reference/ai_poc.

```bash
cd k230_sdk/src/reference/ai_poc
```

(3) Compile a single AI Demo (e.g., face detection)

```shell
./build_app.sh face_detection
```

**Note**: Before executing build_app.sh, ensure that the dependencies are ready, i.e., the relevant kmodel, images, and utils are already present under `k230_sdk/src/big/kmodel/ai_poc`.

```bash
# If the dependencies are not present, execute the following command to download them
cd k230_sdk
make prepare_sourcecode
```

The following files will be generated:

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

Copy the entire k230_bin/ folder to the board, and execute the sh script on the main core to run the corresponding AI demo.

```shell
# Navigate to the sharefs directory of the small core on the development board
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

# Navigate to the sharefs directory of the big core on the development board
cd /sharefs/k230_bin/face_detection
# Execute the corresponding script to run face detection
# Detailed face detection instructions can be found in k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

(4) Compile all AI Demos (if you only need to compile a specific demo, skip this step)

```shell
./build_app.sh
```

The following files will be generated:

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

(5) For the 01studio development board, which supports compiling AI demos for HDMI display and LCD display, the compilation commands are as follows:

```shell
./build_app.sh face_detection hdmi
./build_app.sh face_detection lcd
```

The above commands will generate compiled outputs for a single demo under different display modes. If you want to compile all AI demos, the compilation commands are as follows:

```shell
./build_app.sh all hdmi
./build_app.sh all lcd
```

The above commands will compile all AI demos according to the specified display mode. The compiled outputs for HDMI will be located in the k230_bin directory, while the compiled outputs for LCD display mode will be located in the k230_bin_lcd directory.

Copy the entire k230_bin/ folder to the board, and execute the sh script on the main core to run the corresponding AI demo.

```shell
# Navigate to the sharefs directory of the small core
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

# Navigate to the sharefs directory of the big core
cd /sharefs/k230_bin/face_detection
# Execute the corresponding script to run face detection
# Detailed face detection instructions can be found in k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

### b. Directly Download the Official Board Image

(1) Ensure that you have constructed the Docker container according to the [official K230 SDK instructions](https://github.com/kendryte/k230_sdk).

(2) Download the image from the [official resource library](https://developer.canaan-creative.com/resource).

(3) Environment Preparation

```bash
cd k230_sdk
make prepare_sourcecode # (ignore if already executed)
make mpp
make cdk-user
# Execute different commands based on the development board model
# If the model is CanMV-K230-V1.x, execute the following command
make CONF=k230_canmv_defconfig prepare_memory
# If the model is CanMV-K230-V2.x, execute the following command
make CONF=k230_canmv_v2_defconfig prepare_memory
# If the model is K230-xxx-xxx-EVB-V1.x, execute the following command
make CONF=k230_evb_defconfig prepare_memory
cd k230_sdk/src/reference/ai_poc
```

(4) Compile a Single AI Demo (e.g., face detection)

```shell
./build_app.sh face_detection
```

**Note**: Before executing build_app.sh, ensure that the dependencies are ready, i.e., the relevant kmodel, images, and utils are already present under `k230_sdk/src/big/kmodel/ai_poc`.

```bash
# If the dependencies are not present, execute the following command to download them
cd k230_sdk
make prepare_sourcecode
```

The following files will be generated:

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

Copy the entire k230_bin folder to the board, and execute the sh script on the big core to run the corresponding AI demo.

```shell
# Navigate to the sharefs directory of the small core on the development board
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

# Navigate to the sharefs directory of the big core on the development board
cd /sharefs/k230_bin/face_detection
# Execute the corresponding script to run face detection
# Detailed face detection instructions can be found in k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```

(5) Compile All AI Demos (if you only need to compile a specific demo, skip this step)

```shell
./build_app.sh
```

The following files will be generated:

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

Copy the entire k230_bin folder to the board, and execute the sh script on the big core to run the corresponding AI demo.

```shell
# Navigate to the sharefs directory of the small core
scp -r username@ip:/xxx/k230_sdk/src/big/kmodel/ai_poc/k230_bin .

# Navigate to the sharefs directory of the big core
cd /sharefs/k230_bin/face_detection
# Execute the corresponding script to run face detection
# Detailed face detection instructions can be found in k230_sdk/src/reference/ai_poc/face_detection/README.md
./face_detect_isp.sh
```
