# K230 Scene Practice-Smart Door Lock POC

![cover](../../images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## K230 smart door lock

A set of programs developed on the K230 platform that integrate UI, face detection, ir detection, depth detection, face recognition, and face registration functions. Use 8-wire nor flash fast, from power on to image within 400ms, to unlock within 700ms, the use flash size is 32M, DDR size is 128M.

### Hardware environment

- K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1
- Matching LCD module
- K230-USIP-OV9286-SENSOR-V1.1模组

### Overview

As a POC project, the smart door lock program provides customers with a reference on how to use LVGL, big and little core communication, multimedia pipeline and AI functions, the program is mainly divided into two parts, the big core terminal program mainly completes video input and output, AI processing and other related functions, the little core end completes the function of UI and face feature value management, the big and little cores communicate through IPCMSG, and the development board is started by norflash.

### remark

1. In order to ensure the recognition effect, the configuration file and reference frame file used by the DPU must be matched with the sensor used, if they do not match, please`src/reference/business_poc/doorlock_ov9286/big/bin/` replace the matching sum under the path`H1280W720_conf.bin``H1280W720_ref.bin`, replace and recompile the image.

1. Before powering down and reset, the little core serial port should be input now`halt` to protect the file system from being damaged.

1. In the door lock POC scenario, personal private information such as face feature values must be stored in ciphertext to avoid private information being stolen by attackers and leaving potential security risks. In the K230 smart door lock POC scenario, the face feature value is encrypted and stored in norflash, and the uboot stage will move the ciphertext data from flash to DDR and complete data decryption. This project uses AES-GCM encryption and decryption algorithm to complete the feature value encryption and decryption, and the key used for encryption and decryption is hardcoded into the app in clear text, so that customers can experience the door lock POC function more conveniently. However, encoding the key into the app in plaintext itself is an insecure behavior, if there is a demand, we will provide a complete set of face feature value encryption and decryption storage scheme, the specific process is as follows:

3.1 After the customer gets the k230 development board kit, he needs to burn the key to the OTP key area;

3.2 In the door lock POC scenario, when the customer needs to store the face feature value, the key will be read from the OTP, and then the key will be used to implement AES-GCM encryption;

3.3 In the uboot stage, read the key burned by the user in the OTP key area for decryption.

### Source code location

The source code path of the big kernel program is located in the`src/reference/business_poc/doorlock_ov9286/big` directory structure as follows:

```sh
.
├── anchors_320.cc
├── bin
│   ├── H1280W720_conf.bin
│   └── H1280W720_ref.bin
├── build
├── CMakeLists.txt
├── main.cc
├── mobile_face.cc
├── mobile_face.h
├── mobilenetv2_depth.cc
├── mobilenetv2_depth.h
├── mobilenetv2_ir.cc
├── mobilenetv2_ir.h
├── mobile_retinaface.cc
├── mobile_retinaface.h
├── model.cc
├── model.h
├── util.cc
├── util.h
└── vi_vo.h


```

The source code path of the little core program is located in the`src/little/buildroot-ext/package/door_lock` directory structure as follows:

```sh
.
├── Config.in
├── src
│   ├── CMakeLists.txt
│   └── ui
│       ├── CMakeLists.txt
│       ├── data
│       │   └── img
│       │       ├── delete.png
│       │       ├── import.png
│       │       └── signup.png
│       ├── demo
│       │   └── main.c
│       ├── lvgl_port
│       │   ├── CMakeLists.txt
│       │   ├── k230
│       │   │   ├── buf_mgt.cpp
│       │   │   ├── buf_mgt.hpp
│       │   │   ├── CMakeLists.txt
│       │   │   ├── lv_port_disp.cpp
│       │   │   └── lv_port_indev.c
│       │   ├── lv_conf_demo.h
│       │   ├── lv_conf.h
│       │   └── lv_port.h
│       └── src
│           ├── db_proc.c
│           ├── db_proc.h
│           ├── main.c
│           ├── msg_proc.cpp
│           ├── msg_proc.h
│           ├── scr_main.c
│           ├── scr_signup.c
│           └── ui_common.h
└── src.mk

```

#### Compile the program

K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1 Development Board Compiler:
Execute under the`k230_sdk` directory, generate big core programs`make CONF=k230_evb_doorlock_ov9286_defconfig` under the directory, and`k230_sdk/src/reference/business_poc/doorlock_ov9286/big/out` generate little core program`door_lock.elf` directories under the directory`k230_sdk/output/k230_evb_doorlock_ov9286_defconfig/little/buildroot-ext/target``app`.

#### Run the program

The smart door lock is in the NOR flash image, the big and little core programs are self-starting, K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1 development board will generate`output/k230_evb_doorlock_ov9286_defconfig/images/` an image in the directory after compilation, burn the NOR flash `sysimage-spinor32m.img`image, and the development board DIP switch is set to NOR flash startup

#### Feature demo

1. After the big and little core programs are started, the interface is displayed as follows:![ ov9286_door_lock_menu](../../../zh/02_applications/business_poc/images/ov9286_door_lock_menu.png)

1. SD face picture import function, must be put in the picture under /sharefs/pic, in order to ensure the recognition effect, the format of the imported picture is required to be jpg, the resolution is 720*1280, the ratio is 9:16, the user puts the face picture that needs to be imported down `/sharefs/pic`, press the picture import key, the program will automatically complete the function of extracting feature values, and the file name of the picture is lable after successful recognition, the operation effect is as follows:![ov9286_door_lock_import](../../../zh/02_applications/business_poc/images/ov9286_door_lock_import.png)

1. Face real-time registration function, click the face registration button, enter lable through the keyboard displayed by the UI, in order to ensure the recognition effect, the face should be located in the center of the image when registering, and the operation effect is as follows:![ ov9286_door_lock_singup](../../../zh/02_applications/business_poc/images/ov9286_door_lock_singup.png)
Recognition effect:![ ov9286_door_lock_singup_show](../../../zh/02_applications/business_poc/images/ov9286_door_lock_singup_show.png)

1. The face library deletion function deletes all faces registered in real time through SD cards and faces, and the operation effect is as follows:![ ov9286_door_lock_delete](../../../zh/02_applications/business_poc/images/ov9286_door_lock_delete.png)
