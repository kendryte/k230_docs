# K230 AI Demo introduction

![cover](C:\Work\K230\k230_docs\en\images\canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](C:\Work\K230\k230_docs\en\images\logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

## K230 AI Demo

### Overview

K230 AI Demo integrates face, human body, hand, license plate, word continuation and other modules, including classification, detection, segmentation, recognition, tracking and other functions, to provide customers with a reference on how to use K230 to develop AI-related applications.

### Hardware environment

- K230-UNSIP-LP3-EVB-V1.0/K230-UNSIP-LP3-EVB-V1.1/CanMV-K230 (supported by default)

### Source code location

The source code path is located in`src/reference/ai_poc` and the directory structure is as follows:

```shell
# Detailed Demo documentation is available in the AI Demo subdirectories (eg: bytetrack, face _ detection, etc.)
.
├── build_app.sh
├── bytetrack
├── cmake
├── CMakeLists.txt
├── face_detection
├── face_emotion
├── face_gender
├── face_glasses
├── face_landmark
├── face_mask
├── face_parse
├── face_pose
├── falldown_detect
├── finger_guessing
├── fitness
├── head_detection
├── k230_bin
├── licence_det
├── licence_det_rec
├── llamac
├── nanotracker
├── object_detect_yolov8n
├── person_attr
├── person_detect
├── pose_detect
├── pphumanseg
├── segment_yolov8n
├── shell
├── smoke_detect
├── space_resize
├── sq_hand_det
├── sq_handkp_class
├── sq_handkp_det
├── sq_handkp_ocr
├── sq_handreco
├── traffic_light_detect
├── vehicle_attr
└── version
```

The kmodel, image, and related dependency paths are located in `src/big/kmodel/ai_poc`. The directory structure is as follows:

``` shell
.
├── images
│   ├── 1000.jpg
│   ├── 1024x1331.jpg
│   ├── 1024x624.jpg
│   ├── 1024x768.jpg
│   ├── 640x340.jpg
│   ├── bus.jpg
│   ├── bytetrack_data
│   ├── car.jpg
│   ├── falldown_elder.jpg
│   ├── hrnet_demo.jpg
│   ├── input_hd.jpg
│   ├── input_ocr.jpg
│   ├── licence.jpg
│   ├── smoke1.jpg
│   └── traffic.jpg
├── kmodel
│   ├── bytetrack_yolov5n.kmodel
│   ├── cropped_test127.kmodel
│   ├── face_detection_320.kmodel
│   ├── face_detection_640.kmodel
│   ├── face_emotion.kmodel
│   ├── face_gender.kmodel
│   ├── face_glasses.kmodel
│   ├── face_landmark.kmodel
│   ├── face_mask.kmodel
│   ├── face_parse.kmodel
│   ├── face_pose.kmodel
│   ├── hand_det.kmodel
│   ├── handkp_det.kmodel
│   ├── hand_reco.kmodel
│   ├── head_detection.kmodel
│   ├── human_seg_2023mar.kmodel
│   ├── licence_reco.kmodel
│   ├── LPD_640.kmodel
│   ├── nanotrack_backbone_sim.kmodel
│   ├── nanotracker_head_calib_k230.kmodel
│   ├── ocr_det.kmodel
│   ├── ocr_rec.kmodel
│   ├── person_attr_yolov5n.kmodel
│   ├── person_detect_yolov5n.kmodel
│   ├── person_pulc.kmodel
│   ├── traffic_detect_yolov5s_best.kmodel
│   ├── vehicle_attr_yolov5n.kmodel
│   ├── vehicle.kmodel
│   ├── yolov5n-falldown.kmodel
│   ├── yolov5s_smoke_best.kmodel
│   ├── yolov8n_320.kmodel
│   ├── yolov8n_640.kmodel
│   ├── yolov8n-pose.kmodel
│   ├── yolov8n_seg_320.kmodel
│   └── yolov8n_seg_640.kmodel
└── utils
    ├── Asci0816.zf
    ├── bu.bin
    ├── dict_6625.txt
    ├── HZKf2424.hz
    ├── jiandao.bin
    ├── llama.bin
    ├── shitou.bin
    └── tokenizer.bin
```

### Compile and run the program

- Enter the src/reference/ai_poc
- Execute the build_app.sh script (before executing the script, make sure that there are corresponding kmodels, images, and utils under the src/big/kmodel/ai_poc), this will generate a unified copy of kmodel, images, utils, shell, and elf to the k230_bin folder
- Copy the entire folder to the board, and execute the sh script on the big core to run the corresponding AI demo
