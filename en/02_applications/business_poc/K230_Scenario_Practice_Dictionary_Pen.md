# K230 Scenario Practice - Dictionary Pen POC

![cover](../../../zh/images/canaan-cover.png)

© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase should be governed by the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.
Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**© 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy part or all of the content of this document, or disseminate it in any form.

<div style="page-break-after:always"></div>

## K230 Dictionary Pen

A program developed on the K230 platform that integrates UI, text recognition, and text translation functions.

### Hardware Environment

- K230-USIP-LP4-EVB-V1.0
- Supporting LCD module
- K230-USIP-SC035-SENSOR-V1.1 module

### Overview

The dictionary pen program, as a POC project, provides customers with a reference on how to use vicap to collect data, perform AI processing, and finally push the display function. The program mainly runs on the big core, completing image capture, image-to-text conversion, and text translation functions. It starts on the development board via an SD card, requiring a DDR size of 2G.

### Notes

1. Before powering off and resetting, you should input `halt` in the small core serial port to protect the file system from being damaged.

### Source Code Location

The source code path of the program is located at `src/reference/business_poc/dictionary_pen_poc`, with the directory structure as follows:

```sh
. ├── audio
│   ├── audio_buf_play.cc
│   ├── audio_buf_play.h
│   └── sample_audio.c
├── build.sh
├── CMakeLists.txt
├── main.cpp
├── README.md
├── include
│   ├── API
│   ├── det_ocr
│   └── stitch
│   └── tts
└── vo
    ├── vo.cc
    └── vo.h
```

The code in the include directory is provided by algorithm colleagues, and each kmodel and code needs to be used in matching.

#### Compiling the Program

To compile the program for the K230-USIP-LP4-EVB-V1.0 development board:
Execute `make prepare_sourcecode CONF=k230_evb_usiplpddr4_dictionary_pen_defconfig` in the `k230_sdk` directory to download the dictionary pen source code and kmodel. Then execute `make CONF=k230_evb_usiplpddr4_dictionary_pen_defconfig` in the `k230_sdk` directory. The program directory `dictionary_pen` will be generated in `k230_sdk/output/k230_evb_usiplpddr4_dictionary_pen_defconfig/images/big-core/app/`, with the executable program being `dictionary_pen.elf`.

Notes:
When executing `make prepare_sourcecode`, you must add `CONF=k230_evb_usiplpddr4_dictionary_pen_defconfig`; otherwise, the kmodel required for the dictionary pen to run will not be downloaded.

#### Running the Program

The dictionary pen demo is in the SD card image and is not started by default; it needs to be run manually. After the K230-USIP-LP4-EVB-V1.0 development board is compiled, the `sysimage-sdcard.img` image will be generated in the `output/k230_evb_usiplpddr4_dictionary_pen_defconfig/images/` directory. Run the development board, enter the big core `sharefs\app\dictionary_pen` directory, and run `dictionary_pen.elf`. Then you can scan text for translation using the dictionary pen's tip.

Notes:

1. When the dictionary pen's tip is pressed down, it starts scanning text; when the tip is released, it starts translating. The dictionary pen display will show the original text and the translated text.
1. Currently, the dictionary pen demo only supports translation between Chinese and English.

#### Function Demonstration

The result of the program running, translating Chinese to English, is as follows:
![door_lock_menu](../../../zh/02_applications/business_poc/images/dictionary_pen_zh_translate_en.jpg)

The result of the program running, translating English to Chinese, is as follows:
![door_lock_menu](../../../zh/02_applications/business_poc/images/dictionary_pen_en_translate_zh.jpg)
