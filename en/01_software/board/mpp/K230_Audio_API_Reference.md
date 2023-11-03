# K230 Audio API reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## preface

### Overview

The AUDIO module includes four sub-modules of audio input, audio output, audio encoding, audio decoding, and control of the built-in audio codec.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate         |
|------|--------------|
| ai   | Audio input module |
| ao   | Audio output module |
| aenc | Audio coding module |
| adec | Audio decoding module |

### Revision history

| Document version number | Modify the description                                                     | Author      | date      |
| ---------- | ------------------------------------------------------------ | ----------- | --------- |
| V1.0       | Initial edition                                                         | Sun Xiaopeng      | 2023/3/7  |
| V1.1       | 1) Add support for I2S built-in codec 2) Add PDM single/dual channel support 3) Add AI and AO different sampling accuracy support (16/24/32) 4) The API interface remains unchanged, and parameter properties are added, and the documentation is improved. | Sun Xiaopeng      | 2023/3/27 |
| V1.1.1     | Add audio codec API interface Add sound quality enhancement API[interface kd_mpi_ai_set_vqe_attr](#219-kd_mpi_ai_set_vqe_attr)/[kd_mpi_ai_get_vqe_attr](#2110-kd_mpi_ai_get_vqe_attr), and description. | Sun Xiaopeng/Cui Yan | 2023/4/12 |
| V1.2       | Modify the sound quality enhancement API[kd_mpi_ai_set_vqe_attr](#219-kd_mpi_ai_set_vqe_attr)kd_mpi_ai_set_vqe_attr/[kd_mpi_ai_get_vqe_attr](#2110-kd_mpi_ai_get_vqe_attr) Add audio codec mapi interface function | Sun Xiaopeng/Cui Yan | 2023/4/27 |
| V1.3       | 1) Add built-in Audio Codec API interface                                | Sun Xiaopeng      | 2023/5/10 |
| v1.4       | 1)Support single and dual channel input and output, modify[k_audio_i2s_attr](#3110-k_audio_i2s_attr)attributes, and add snd_Mode attribute. 2)Add built-in Audio Codec API interface: including volume acquisition and reset related interfaces:[k_acodec_get_gain_micl/](#257-k_acodec_get_gain_hpoutl)k_acodec_get_gain_micr[/k_acodec_get_adcl_volume](#2516-k_acodec_get_gain_micr)/k_acodec_get_adcr_volume[/k_acodec_get_alc_gain_micl](#2518-k_acodec_get_adcl_volume)/k_acodec_get_alc_gain_micr[/k_acodec_get_gain_hpoutl](#2519-k_acodec_get_adcr_volume)/k_acodec_get_gain_hpoutr[/k_acodec_get_dacl_volume](#255-k_acodec_get_alc_gain_micl)[](#256-k_acodec_get_alc_gain_micr)[](#257-k_acodec_get_gain_hpoutl)[](#258-k_acodec_get_gain_hpoutr)[/](#259-k_acodec_get_dacl_volume)[k_acodec_get_dacr_volume](#2510-k_acodec_get_dacr_volume)/[k_acodec_reset](#2510-k_acodec_reset) | Sun Xiaopeng      | 2023/6/15 |

## 1. Overview

### 1.1 Overview

The audio module includes four sub-modules of audio input AI, audio output AO, audio coding AENC, audio decoding ADCE, and support for built-in analog audio codec. The audio input module includes i2s and pdm two audio interfaces, with PDMA for memory copying, support digital microphone (PDM/I2S) and analog audio codec (i2S) sound source input, built-in analog audio codec, support sound quality enhancement (VQE) processing of audio data: 3A (AEC echo cancellation, ANR noise reduction, AGC automatic gain). The audio output module supports I2S audio interface, with PDMA to do memory copy, and can be connected to an external data speaker or analog audio codec as sound output. The audio encoding and decoding module temporarily supports audio codec functions for the G711 format and supports the registration of external codecs.

The audio module is divided into multiple sub-modules, and the data flow is transmitted to each other in a low-coupling manner, which is sufficient to meet the existing multimedia services under MAIX3. The following figure only analyzes the use of the audio module in the voice intercom service scenario. The collected audio data is encoded by the audio input module and sent to the remote end through the network, and the audio coding data obtained from the remote end is decoded by the audio decoding module and the remote sound can be played through the audio output module.

### 1.2 Function Description

#### 1.2.1 Audio input

The audio input module (AI) mainly implements functions such as configuring and enabling audio input devices and obtaining audio frame data.

The audio input module supports I2s and PDM protocol interfaces. i2S supports simultaneous capture of up to 2 channels of two-channel audio, and PDM supports simultaneous capture of up to 8 channels of mono audio. The detailed I2S and PDM characteristics are as follows:

- I2S audio interface

  1. The data sampling rate supports 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz, and the sampling accuracy supports 16/24/32bit.

  1. Support 2 sets of configurable IOs for input/output I2S audio data, support full-duplex mode.

- PDM audio interface

  1. Support PDM audio input, 1bit wide, sample clock frequency of 0.256MHz/0.384MHz/0.512MHz/0.768MHz/1.024MHz/1.4112MHz/1.536MHz/2.048MHz/2.8224MHz/3.072MHz/4.096MHz/5.6448MHz/6.144MHz/12.288MHz/ 24.576MHz, the input PCM audio sampling rate is 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz. The sampling accuracy supports 16/24/32bit.

  1. Support oversampling rate 128, 64, 32 times oversampling.

  1. Supports 1-4 IOs for input PDM audio data.

  1. The input supports 1-8 PDM channels, supports PDM left and right mono mode and two-channel mode, each IO channel mode is unified, and PDM two-channel mode uses up to 4 IOs

  1. The sequence number of the enabled channels is small to large and continuous, and each channel is not supported to be enabled randomly

#### 1.2.2 Audio output

Audio output (AO) mainly implements the functions of enabling audio output devices and sending audio frames to output channels.

The audio output module supports an I2s protocol interface. i2S supports simultaneous output of up to 2 channels of two-channel audio.

- I2S audio interface

  1. The data sampling rate supports 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz, and the sampling accuracy is 16/24/32bit.

  1. Support 2 sets of configurable IOs for input/output I2S audio data, support full-duplex mode.

#### 1.2.3 Audio Link

- The audio codec receives the signal from the analog microphone, converted into the PCM data in the I2S format, and input into the I2S in audio; the PCM data output by I2S, after the audio codec, becomes an analog signal emitted, the mode does not use digital IO, fixed use of I2S sdi0 and sdo0 interface.

- I2S interfaces directly with off-chip digital microphones and PAs. There are two sets of interfaces to choose from: SDI0, SDO0, and SDI1, SDO1.

- Off-chip PDM microphone with up to 8 PDM data inputs to Audio's 4 input data interfaces.

Links to choose from include:

- 3 groups pdm_in + 1 group i2s_in + 2 groups i2s out, where 1 group i2s_in can use the built-in audio codec or off-chip

- 4 groups pdm_in + 2 groups I2S out

- 2 groups i2s_in + 2 groups pdm_in + 2 groups I2s out

You can use the built-in codec or an external device (audio daughter board) to test audio-related functions. Use the built-in codec to test one set of I2S audio input and output and audio codec related functions, and use the audio daughter board to test 2 sets of I2S audio input and output and 4 groups of PDM audio input functions.

#### 1.2.4 Sound Quality Enhancement

The audio module supports sound quality enhancement processing of audio data to realize audio 3A function. Currently, the supported sampling accuracy is 16bit, and the supported sampling rate is 16K.

## 2. API Reference

### 2.1 Audio input

This function module provides the following APIs:

- [kd_mpi_ai_set_pub_attr](#211-kd_mpi_ai_set_pub_attr)
- [kd_mpi_ai_get_pub_attr](#212-kd_mpi_ai_get_pub_attr)
- [kd_mpi_ai_enable](#213-kd_mpi_ai_enable)
- [kd_mpi_ai_disable](#214-kd_mpi_ai_disable)
- [kd_mpi_ai_enable_chn](#215-kd_mpi_ai_enable_chn)
- [kd_mpi_ai_disable_chn](#215-kd_mpi_ai_enable_chn)
- [kd_mpi_ai_get_frame](#217-kd_mpi_ai_get_frame)
- [kd_mpi_ai_release_frame](#218-kd_mpi_ai_release_frame)
- [kd_mpi_ai_set_vqe_attr](#219-kd_mpi_ai_set_vqe_attr)
- [kd_mpi_ai_get_vqe_attr](#2110-kd_mpi_ai_get_vqe_attr)

#### 2.1.1 kd_mpi_ai_set_pub_attr

【Description】

Set AI device properties.

【Syntax】

k_s32 kd_mpi_ai_set_pub_attr([k_audio_dev](#312-k_audio_dev) ai_dev, const [k_aio_dev_attr](#3112-k_aio_dev_attr) \*attr);

【Parameters】

| Parameter name | description              | Input/output |
|----------|-------------------|-----------|
| ai_dev   | Audio device number.      | input      |
| attr     | AI device property pointer.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

【Note】

none

【Example】

```c
k_aio_dev_attr aio_dev_attr;
aio_dev_attr.audio_type = KD_AUDIO_INPUT_TYPE_I2S;
aio_dev_attr.kd_audio_attr.i2s_attr.sample_rate = 44100;
aio_dev_attr.kd_audio_attr.i2s_attr.bit_width = KD_AUDIO_BIT_WIDTH_16
aio_dev_attr.kd_audio_attr.i2s_attr.chn_cnt = 2;
aio_dev_attr.kd_audio_attr.i2s_attr.i2s_mode = K_STANDARD_MODE;
aio_dev_attr.kd_audio_attr.i2s_attr.frame_num = 25;
aio_dev_attr.kd_audio_attr.i2s_attr.point_num_per_frame = 44100/25;
aio_dev_attr.kd_audio_attr.i2s_attr.i2s_type = K_AIO_I2STYPE_INNERCODEC;
if (K_SUCCESS != kd_mpi_ai_set_pub_attr(0, &aio_dev_attr))
{
printf("kd_mpi_ai_set_pub_attr failed\n");
return K_FAILED;
}
if (K_SUCCESS != kd_mpi_ai_enable(0))
{
printf("kd_mpi_ai_set_pub_attr failed\n");
return K_FAILED;
}
if (K_SUCCESS != kd_mpi_ai_enable_chn(0, 0))
{
printf("kd_mpi_ai_set_pub_attr failed\n");
return K_FAILED;
}
```

#### 2.1.2 kd_mpi_ai_get_pub_attr

【Description】

Get AI device properties.

【Syntax】

k_s32 kd_mpi_ai_get_pub_attr([k_audio_dev](#312-k_audio_dev) ai_dev, [k_aio_dev_attr](#3112-k_aio_dev_attr) \*attr);

【Parameters】

| Parameter name | description             | Input/output |
|----------|------------------|-----------|
| ai_dev   | Audio device number.     | input      |
| attr     | AI device property pointer. | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.3 kd_mpi_ai_enable

【Description】

Enable AI devices.

【Syntax】

k_s32 kd_mpi_ai_enable([k_audio_dev](#312-k_audio_dev) ai_dev);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ai_dev   | Audio device number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.4 kd_mpi_ai_disable

【Description】

Disable the AI device.

【Syntax】

k_s32 kd_mpi_ai_disable([k_audio_dev](#312-k_audio_dev) ai_dev);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ai_dev   | Audio device number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.5 kd_mpi_ai_enable_chn

【Description】

Enable the AI channel.

【Syntax】

k_s32 kd_mpi_ai_enable_chn([k_audio_dev](#312-k_audio_dev) ai_dev.k_ai_chn[](#313-k_ai_chn) ai_chn);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ai_dev   | Audio device number.  | input      |
| ai_chn   | Audio channel number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.6 kd_mpi_ai_disable_chn

【Description】

Disable the AI channel.

【Syntax】

k_s32 kd_mpi_ai_disable_chn([k_audio_dev](#312-k_audio_dev) ai_dev.k_ai_chn[](#313-k_ai_chn) ai_chn);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ai_dev   | Audio device number.  | input      |
| ai_chn   | Audio channel number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.7 kd_mpi_ai_get_frame

【Description】

Gets the audio frame.

【Syntax】

k_s32 kd_mpi_ai_get_frame([k_audio_dev](#312-k_audio_dev) ai_dev.k_ai_chn[](#313-k_ai_chn) ai_chn.k_audio_frame[](#3114-k_audio_frame)\*frame, k_u32 milli_sec);

【Parameters】

| Parameter name  | description                                                                                                                                        | Input/output |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| ai_dev    | Audio device number.                                                                                                                                | input      |
| ai_chn    | Audio channel number.                                                                                                                                | input      |
| frame     | Audio frame data.                                                                                                                                | output      |
| milli_sec | The timeout period for getting data. -1 indicates blocking mode, waiting until there is no data; 0 indicates non-blocking mode, and returns an error when there is no data; >0 indicates blocking milli_sec milliseconds, and an error is returned if the timeout is returned.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

【Note】

- The value of the milli_sec must be greater than or equal to -1, the blocking mode is used to obtain data when it is equal to -1, and the data is obtained in blocking mode when it is equal to 0

When the blocking mode obtains data, if it is greater than 0, after blocking for milli_sec milliseconds, no data returns a timeout and an error is reported.

- Before obtaining audio frame data, the corresponding AI channel must be enabled.

【Example】

```c
k_audio_frame audio_frame;
while(true)
{
//get frame
if (K_SUCCESS != kd_mpi_ai_get_frame(dev_num, channel, &audio_frame, 1000))
{
printf("=========kd_mpi_ai_get_frame timeout\n");
continue ;
}
//process frame
process_frame(&audio_frame);
//release frame
kd_mpi_ai_release_frame(dev_num, channel, &audio_frame);
}
```

#### 2.1.8 kd_mpi_ai_release_frame

【Description】

Release audio frames.

【Syntax】

k_s32 kd_mpi_ai_release_frame([k_audio_dev](#312-k_audio_dev) ai_dev,k_ai_chn[](#313-k_ai_chn) ai_chn,const [k_audio_frame](#3114-k_audio_frame) *frame);【参数】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ai_dev   | Audio device number.  | input      |
| ai_chn   | Audio channel number.  | input      |
| frame    | Audio frame data.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

#### 2.1.9 kd_mpi_ai_set_vqe_attr

【Description】

Set properties related to the AI's sound quality enhancements.

【Syntax】

k_s32 kd_mpi_ai_set_vqe_attr([k_audio_dev](#312-k_audio_dev) ai_dev[k_ai_chn](#313-k_ai_chn) k_ai_chn ai_chn, const k_bool \*vqe_enable);

【Parameters】

| Parameter name   | description                                                      | Input/output |
|------------|-----------------------------------------------------------|-----------|
| ai_dev     | Audio device number.                                              | input      |
| ai_chn     | Audio channel number.                                              | input      |
| vqe_enable | Sound quality enhancement enable flag bit. K_TRUE: Enable. K_FALSE: Not enabled. | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h

Library file: libai.a

【Note】

Currently, the supported sampling accuracy is 16bit, and the supported sampling rates are 8K and 16K.

#### 2.1.10 kd_mpi_ai_get_vqe_attr

【Description】

Get AI's sound quality enhancement related attributes.

【Syntax】

k_s32 kd_mpi_ai_get_vqe_attr([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn, k_bool \*vqe_enable);

【Parameters】

| Parameter name   | description                                                          | Input/output |
|------------|---------------------------------------------------------------|-----------|
| ai_dev     | Audio device number.                                                  | input      |
| ai_chn     | Audio channel number.                                                  | input      |
| vqe_enable | Sound quality enhancement enable flag bit pointer. K_TRUE: Enable. K_FALSE: Not enabled. | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.2 Audio output

This function module provides the following APIs:

- [kd_mpi_ao_set_pub_attr](#221-kd_mpi_ao_set_pub_attr)
- [kd_mpi_ao_get_pub_attr](#212-kd_mpi_ai_get_pub_attr)
- [kd_mpi_ao_enable](#223-kd_mpi_ao_enable)
- [kd_mpi_ao_disable](#224-kd_mpi_ao_disable)
- [kd_mpi_ao_enable_chn](#225-kd_mpi_ao_enable_chn)
- [kd_mpi_ao_disable_chn](#226-kd_mpi_ao_disable_chn)
- [kd_mpi_ao_send_frame](#227-kd_mpi_ao_send_frame)

#### 2.2.1 kd_mpi_ao_set_pub_attr

【Description】

Set the AO device properties.

【Syntax】

k_s32 kd_mpi_ao_set_pub_attr([k_audio_dev](#312-k_audio_dev) ao_dev, const [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);

【Parameters】

| Parameter name | description              | Input/output |
|----------|-------------------|-----------|
| ao_dev   | Audio device number.      | input      |
| attr     | AO device property pointer.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

【Note】

none

【Example】

```c
k_aio_dev_attr ao_dev_attr;
ao_dev_attr.audio_type = KD_AUDIO_OUTPUT_TYPE_I2S;
ao_dev_attr.kd_audio_attr.i2s_attr.sample_rate = 48000;
ao_dev_attr.kd_audio_attr.i2s_attr.bit_width = KD_AUDIO_BIT_WIDTH_24;
ao_dev_attr.kd_audio_attr.i2s_attr.chn_cnt = 2;
ao_dev_attr.kd_audio_attr.i2s_attr.i2s_mode = K_RIGHT_JUSTIFYING_MODE;
ao_dev_attr.kd_audio_attr.i2s_attr.frame_num = 15;
ao_dev_attr.kd_audio_attr.i2s_attr.point_num_per_frame = 48000/25;
ao_dev_attr.kd_audio_attr.i2s_attr.i2s_type = K_AIO_I2STYPE_EXTERN;
if (K_SUCCESS != kd_mpi_ao_set_pub_attr(0, &ao_dev_attr))
{
printf("kd_mpi_ao_set_pub_attr failed\n");
return K_FAILED;
}

if (K_SUCCESS != kd_mpi_ai_enable(0))
{
printf("kd_mpi_ai_enable failed\n");
return K_FAILED;
}

if (K_SUCCESS != kd_mpi_ai_enable_chn(0,1))
{
printf("kd_mpi_ai_enable_chn failed\n");
return K_FAILED;
}
```

#### 2.2.2 kd_mpi_ao_get_pub_attr

【Description】

Gets the AO device properties.

【Syntax】

k_s32 kd_mpi_ao_get_pub_attr([k_audio_dev](#312-k_audio_dev) ao_dev, [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);

【Parameters】

| Parameter name | description             | Input/output |
|----------|------------------|-----------|
| ao_dev   | Audio device number.     | input      |
| attr     | AO device property pointer. | output      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.3 kd_mpi_ao_enable

【Description】

Enable the AO device.

【Syntax】

k_s32 kd_mpi_ao_enable([k_audio_dev](#312-k_audio_dev) ao_dev);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ao_dev   | Audio device number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.4 kd_mpi_ao_disable

【Description】

Disable the AO device.

【Syntax】

k_s32 kd_mpi_ao_disable([k_audio_dev](#312-k_audio_dev) ao_dev);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ao_dev   | Audio device number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.5 kd_mpi_ao_enable_chn

【Description】

Enable the AO channel.

【Syntax】

k_s32 kd_mpi_ao_enable_chn([k_audio_dev](#312-k_audio_dev) ao_dev.k_ao_chn[](#314-k_ao_chn) ao_chn);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ao_dev   | Audio device number.  | input      |
| ao_chn   | Audio channel number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.6 kd_mpi_ao_disable_chn

【Description】

Disable the AO channel.

【Syntax】

k_s32 kd_mpi_ao_disable_chn([k_audio_dev](#312-k_audio_dev) ao_dev.k_ao_chn[](#314-k_ao_chn) ao_chn);

【Parameters】

| Parameter name | description          | Input/output |
|----------|---------------|-----------|
| ao_dev   | Audio device number.  | input      |
| ao_chn   | Audio channel number.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.7 kd_mpi_ao_send_frame

【Description】

Send AO frame data.

【Syntax】

k_s32 kd_mpi_ao_send_frame

([k_audio_dev](#312-k_audio_dev) ao_dev,k_ao_chn[](#314-k_ao_chn) ao_chn,const [k_audio_frame](#3114-k_audio_frame)*frame,k_s32 milli_sec);

【Parameters】

| Parameter name  | description                                                                                                                                        | Input/output |
|-----------|---------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| ao_dev    | Audio device number.                                                                                                                                | input      |
| ao_chn    | Audio channel number.                                                                                                                                | input      |
| frame     | Audio frame data pointer.                                                                                                                            | input      |
| milli_sec | The timeout period for sending data. -1 indicates blocking mode, waiting until there is no data; 0 indicates non-blocking mode, and returns an error when there is no data; >0 indicates blocking milli_sec milliseconds, and an error is returned if the timeout is returned.  | input      |

【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_ai_api.h
- Library file: libai.a

【Note】

- The value of the milli_sec must be greater than or equal to -1, the blocking mode is used to obtain data when it is equal to -1, and the data is obtained in blocking mode when it is equal to 0

When the blocking mode obtains data, if it is greater than 0, after blocking for milli_sec milliseconds, no data returns a timeout and an error is reported.

- Before sending audio frame data, the corresponding AO channel must be enabled.

【Example】

```c
k_audio_frame audio_frame;
k_s32 ret = 0;
while (true)
{
//get ai frame
ret = kd_mpi_ai_get_frame(0, 0, &audio_frame, 1000);
if (K_SUCCESS != ret)
{
printf("=========kd_mpi_ai_get_frame timeout\n");
continue ;
}
//send ai frame to ao
ret = kd_mpi_ao_send_frame(0, 1, &audio_frame, 0);
if (K_SUCCESS != ret)
{
printf("=======kd_mpi_ao_send_frame failed\n");
}
//release ai frame
kd_mpi_ai_release_frame(0, 0, &audio_frame);
}
```

### 2.3 Audio Coding

Audio coding mainly implements the functions of creating encoding channels, sending audio frame encoding, and obtaining encoding code streams. For the audio coding part, G711A/U encoding is provided, and only supports 16-bit sampling accuracy.

This function module provides the following APIs:

- [kd_mpi_aenc_register_encoder](#231-kd_mpi_aenc_register_encoder):Register the encoder.
- [kd_mpi_aenc_unregister_encoder](#232-kd_mpi_aenc_unregister_encoder):Unregister the encoder.
- [kd_mpi_aenc_create_chn](#233-kd_mpi_aenc_create_chn): Create an encoding channel
- [kd_mpi_aenc_destroy_chn](#234-kd_mpi_aenc_destroy_chn):Destroy the audio encoding channel.
- [kd_mpi_aenc_send_frame](#235-kd_mpi_aenc_send_frame): Send audio encoded audio frames
- [kd_mpi_aenc_get_stream](#236-kd_mpi_aenc_get_stream): Obtain the audio encoding stream
- [kd_mpi_aenc_release_stream](#237-kd_mpi_aenc_release_stream): Release the audio encoding bitstream

#### 2.3.1 kd_mpi_aenc_register_encoder

- 【Description】

Register the encoder.

- 【Syntax】

k_s32 kd_mpi_aenc_register_encoder(k_s32 \*handle, const [k_aenc_encoder](#322-k_aenc_encoder) \*encoder);

- 【Parameters】

| **Parameter name** | **Description**           | **Input/output** |
|--------------|--------------------|---------------|
| handle       | Register the handle.         | output          |
| encoder      | Encoder property structure. | input          |

- 【Description】

The user registers an encoder with the AENC module by passing in the encoder attribute struct and returns a registration sentence

handle, the user can finally register the encoder by registering the handle.

The AENC module can register up to 20 encoders and has itself registered G711.a, G711.u

Two encoders.

The same encoding protocol does not allow duplicate encoder registrations, for example, if the G711 encoder is already registered, another encoder is not allowed

Register another G711 encoder

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.2 kd_mpi_aenc_unregister_encoder

- 【Description】

Unregister the encoder.

- 【Syntax】

k_s32 kd_mpi_aenc_unregister_encoder(k_s32 handle);

- 【Parameters】

| **Parameter name** | **Description**    | **Input/output** |
|--------------|-------------|---------------|
| handle       | Logoff handle.  | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.3 kd_mpi_aenc_create_chn

- 【Description】

Create an audio encoding channel.

- 【Syntax】

k_s32 kd_mpi_aenc_create_chn([k_aenc_chn](#326-k_aenc_chn) aenc_chn, const [k_aenc_chn_attr](#323-k_aenc_chn_attr) \*attr);

| **Parameter name** | **Description**                                                           | **Input/output** |
|--------------|--------------------------------------------------------------------|---------------|
| aenc_chn     | Tōdō-go. value range: [0, [AENC_MAX_CHN_NUM](#324-aenc_max_chn_nums))。  | input          |
| attr         | Audio encoding channel property pointer.                                             | input          |

- 【Description】

The buffer size is measured in frames, the value range is [2,[K_MAX_AUDIO_FRAME_NUM]](#315-k_max_audio_frame_num)the recommended configuration is 10 or above, too small buffer configuration may cause abnormalities such as frame drops. Each encoding channel configures the queue size based on the buffer size to cache the encoded frame data.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.4 kd_mpi_aenc_destroy_chn

- 【Description】

Destroy the audio encoding channel.

- 【Syntax】

k_s32 kd_mpi_aenc_destroy_chn([k_aenc_chn](#326-k_aenc_chn) aenc_chn);

| **Parameter name** | **Description**                                                           | **Input/output** |
|--------------|--------------------------------------------------------------------|---------------|
| aenc_chn     | Tōdō-go. Value range: [0, [AENC_MAX_CHN_NUM](#324-aenc_max_chn_nums))。  | input          |

- 【Description】

none

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.5 kd_mpi_aenc_send_frame

- 【Description】

Send audio encoded frames.

- 【Syntax】

k_s32 kd_mpi_aenc_send_frame([k_aenc_chn](#326-k_aenc_chn) aenc_chn,const [k_audio_frame](#3114-k_audio_frame) \*frame);

- 【Parameters】

| **Parameter name** | **Description**                                          | **Input/output** |
|--------------|---------------------------------------------------|---------------|
| aenc_chn     | Channel number.  Value range: [0, AENC_MAX_CHN_NUM].  input | input          |
| frame        | Audio frame structure pointer.                                | input          |

- 【Description】

The audio encoding sending stream is a non-blocking interface, and if the audio stream cache is full, it will directly return the failure. This interface is used for users to actively send audio frames for encoding, and if the AENC channel is already bound to AI through the system binding interface, this interface is not required or recommended. When you call this operation to send audio encoded audio frames, you must first create a corresponding encoding channel.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.6 kd_mpi_aenc_get_stream

- 【Description】

Gets the audio encoding stream.

- 【Syntax】

k_s32 kd_mpi_aenc_get_stream([k_aenc_chn](#326-k_aenc_chn) aenc_chn, [k_audio_stream](#327-k_audio_stream) \*stream, k_s32 milli_sec);

- 【Parameters】

| **Parameter name** | **Description**                                                                                                                                          | **Input/output** |
|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| aenc_chn     | Channel number.  Value range: [0, AENC_MAX_CHN_NUM].                                                                                                       | input          |
| stream       | The obtained audio stream.                                                                                                                                  | output          |
| milli_sec    | The timeout period for obtaining data -1 indicates blocking mode, waiting until there is no data; 0 indicates non-blocking mode, and an error is returned when there is no data; \>0 indicates blocking s32MilliSec milliseconds, and an error is returned if the timeout is returned.  | input          |

- 【Description】

The channel must be created before it is possible to obtain the bitstream, otherwise it will fail directly if it is pinned in the process of obtaining the bitstream

Destroying the channel will immediately return failure.

The value of s32MilliSec must be greater than or equal to -1, and data must be obtained in blocking mode when equal to -1, and 0 when it is equal

Data is obtained in non-blocking mode, and when greater than 0, no data is returned after blocking s32MilliSec milliseconds

and report an error.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.7 kd_mpi_aenc_release_stream

- 【Description】

Release the audio encoding stream.

- 【Syntax】

k_s32 kd_mpi_aenc_release_stream([k_aenc_chn](#326-k_aenc_chn) aenc_chn, const [k_audio_stream](#327-k_audio_stream) \*stream);

- 【Parameters】

| **Parameter name** | **Description**                                     | **Input/output** |
|--------------|----------------------------------------------|---------------|
| aenc_chn     | Channel number.  Value range: [0, AENC_MAX_CHN_NUM].  | input          |
| stream       | The obtained audio stream.                             | output          |

- 【Description】

none

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

### 2.4 Audio Decoding

Audio decoding mainly realizes the functions of decoding channels, sending audio code stream decoding, and obtaining decoded audio frames.

The audio codec part provides G711A/U decoding, which temporarily supports 16-bit sampling accuracy.

This function module provides the following APIs:

- [kd_mpi_adec_register_decoder](#241-kd_mpi_adec_register_decoder):Register the decoder.
- [kd_mpi_adec_unregister_decoder](#242-kd_mpi_adec_unregister_decoder):Log out of the decoder.
- [kd_mpi_adec_create_chn](#243-kd_mpi_adec_create_chn): Create an audio decoding channel
- [kd_mpi_adec_destroy_chn](#244-kd_mpi_adec_destroy_chn):Destroy the audio decoding channel.
- [kd_mpi_adec_send_stream](#245-kd_mpi_adec_send_stream): Send the audio stream to the audio decoding channel
- [kd_mpi_adec_clr_chn_buf](#246-kd_mpi_adec_clr_chn_buf): Clears the current audio data cache in the ADEC channel.
- [kd_mpi_adec_get_frame](#247-kd_mpi_adec_get_frame): Get audio decoded frame data
- [kd_mpi_adec_release_frame](#248-kd_mpi_adec_release_frame): Release audio decoded frame data

#### 2.4.1 kd_mpi_adec_register_decoder

- 【Description】

Register the decoder.

- 【Syntax】

k_s32 kd_mpi_adec_register_decoder(k_s32 \*handle, const [k_adec_decoder](#329-k_adec_decoder) \*decoder);

- 【Parameters】

| **Parameter name** | **Description**           | **Input/output** |
|--------------|--------------------|---------------|
| handle       | Register the handle.         | output          |
| decoder      | The decoder property structure. | input          |

- 【Description】

The user registers a decoder with the ADEC module by passing in the decoder attribute structure and returns a registration handle, which the user can finally unregister by registering the handle. The ADEC module can register up to 20 decoders, and it has registered two decoders, G711a and G711u. The same decoding protocol does not allow duplicate registration of decoders, for example, if a G711 decoder is already registered, another G711 decoder is not allowed.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

#### 2.4.2 kd_mpi_adec_unregister_decoder

- 【Description】

Log out of the decoder.

- 【Syntax】

k_s32 kd_mpi_adec_unregister_decoder(k_s32 handle);

- 【Parameters】

| **Parameter name** | **Description**    | **Input/output** |
|--------------|-------------|---------------|
| handle       | Logoff handle.  | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】
- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.3 kd_mpi_adec_create_chn

- 【Description】

Create an audio decoding channel.

- 【Syntax】

k_s32 kd_mpi_adec_create_chn([k_adec_chn](#3212-k_adec_chn) adec_chn, const [k_adec_chn_attr](#328-k_adec_chn_attr) \*attr);

- 【Parameters】

| **Parameter name** | **Description**                                                            | **Input/output** |
|--------------|---------------------------------------------------------------------|---------------|
| adec_chn     | Tōdō-go.  value range:[0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).  | input          |
| attr         | Channel property pointer.                                                      | input          |

- 【Description】

The protocol type specifies the decoding protocol for that channel and currently supports G711. Some properties of audio decoding need to match the output device properties, such as sample rate, frame length (number of samples per frame), and so on. The buffer size is measured in frames, the value range is [2, K_MAX_AUDIO_FRAME_NUM](#315-k_max_audio_frame_num)it is recommended to configure it to be above 10, too small buffer configuration may cause exceptions such as frame drops. This interface can only be used before (or after the channel has been created) and returned if the channel has already been created.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

#### 2.4.4 kd_mpi_adec_destroy_chn

- 【Description】

Destroy the audio decoding channel.

- 【Syntax】

k_s32 kd_mpi_adec_destroy_chn([k_adec_chn](#3212-k_adec_chn) adec_chn);

- 【Parameters】

| **Parameter name** | **Description**                                                           | **Input/output** |
|--------------|--------------------------------------------------------------------|---------------|
| adec_chn     | Tōdō-go. value range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums))。  | input          |

- 【Description】

none

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】
- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.5 kd_mpi_adec_send_stream

- 【Description】

Send an audio stream to the audio decoding channel.

- 【Syntax】

k_s32 kd_mpi_adec_send_stream(k_adec_chn adec_chn,const k_audio_stream \*stream,k_bool block);

- 【Parameters】

| **Parameter name** | **Description**                                         | **Input/output** |
|--------------|--------------------------------------------------|---------------|
| adec_chn     | Tōdō-go.  value range:[0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).      | input          |
| stream       | Audio bitstream.                                       | input          |
| block        | Blocking identification.  HI_TRUE: Blocking.  HI_FALSE: Non-blocking.  | input          |

- 【Description】

When sending data, you must ensure that the channel has been created, otherwise the direct return fails, and if the channel is destroyed during the data delivery process, the failure will be returned immediately. Supports blocking or non-blocking stream sending. When sending a stream in blocking mode, if the buffer used to cache the decoded audio frame is full, this interface call will be blocked until the decoded audio frame data is removed or the ADEC channel is destroyed.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

#### 2.4.6 kd_mpi_adec_clr_chn_buf

- 【Description】

Clears the current audio data cache in the ADEC channel.

- 【Syntax】

k_s32 kd_mpi_adec_clr_chn_buf([k_adec_chn](#3212-k_adec_chn) adec_chn);

- 【Parameters】

| **Parameter name** | **Description**                                                           | **Input/output** |
|--------------|--------------------------------------------------------------------|---------------|
| adec_chn     | Tōdō-go. value range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums))。  | input          |

- 【Description】

It is required that the decoding channel has already been created, and if the channel has not been created, the error code of the channel is returned.

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

#### 2.4.7 kd_mpi_adec_get_frame

- 【Description】

Gets the audio decoded frame data.

- 【Syntax】

k_s32 kd_mpi_adec_get_frame([k_adec_chn](#3212-k_adec_chn) adec_chn, [k_audio_frame](#3114-k_audio_frame) \*frame, k_s32 milli_sec);

- 【Parameters】

| **Parameter name** | **Description**                 | **Input/output** |
|--------------|--------------------------|---------------|
| adec_chn     | Audio decoding channel.           | input          |
| frame_info   | Audio frame data structure output   | output          |
| block        | Whether to get in blocking mode       | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

#### 2.4.8 kd_mpi_adec_release_frame

- 【Description】

Release the obtained audio decoded frame data.

- 【Syntax】

k_s32 kd_mpi_adec_release_frame([k_adec_chn](#326-k_aenc_chn) adec_chn, const [k_audio_frame](#3114-k_audio_frame) \*frame);

- 【Parameters】

| **Parameter name** | **Description**                 | **Input/output** |
|--------------|--------------------------|---------------|
| adec_chn     | Audio decoding channel.           | input          |
| frame_info   | Audio frame data structure output   | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: mpi_adec_api.h

Library file: libadec.a

### 2.5 built-in Audio Codec

The built-in Audio Codec mainly provides operation of hardware devices through ioctl. Among the CMDs of the IOCTL offered, there are some

cmd users do not need to call it, and can directly use the default value when the module is loaded. The ioctl call implements the reading and writing of the built-in Audio Codec registers.

The control operation of the current version of the audio codec mainly includes: ADC digital and analog volume, DAC digital/analog volume, ADC/DAC mute control. Among them, the sampling rate, sampling accuracy, and I2S alignment mode are automatically completed by the user by calling the API interface kernel of AI and AO (the kernel code automatically implements the operation on the codec hardware device), and no longer provides an IOCTL interface to control.

Built-in Audio Codec standard function cmd:

- [k_acodec_set_gain_micl](#251-k_acodec_set_gain_micl): Left channel input analog gain control
- [k_acodec_set_gain_micr](#252-k_acodec_set_gain_micr): Right channel input analog gain control
- [k_acodec_set_adcl_volume](#253-k_acodec_set_adcl_volume): Left channel input digital volume control
- [k_acodec_set_adcr_volume](#254-k_acodec_set_adcr_volume): Digital volume control with right channel input
- [k_acodec_set_alc_gain_micl](#255-k_acodec_set_alc_gain_micl): Analog gain control for the ALC left channel input
- [k_acodec_set_alc_gain_micr](#256-k_acodec_set_alc_gain_micr): Analog gain control for the ALC right channel input
- [k_acodec_set_gain_hpoutl](#257-k_acodec_set_gain_hpoutl): Left channel output analog volume control
- [k_acodec_set_gain_hpoutr](#258-k_acodec_set_gain_hpoutr): Right channel output analog volume control
- [k_acodec_set_dacl_volume](#259-k_acodec_set_dacl_volume): Left channel output digital volume control
- [k_acodec_set_dacr_volume](#2510-k_acodec_set_dacr_volume): Right channel output digital volume control
- [k_acodec_set_micl_mute](#2511-k_acodec_set_micl_mute): Left channel input mute control
- [k_acodec_set_micr_mute](#2512-k_acodec_set_micr_mute): Right channel input mute control
- [k_acodec_set_dacl_mute](#2513-k_acodec_set_dacl_mute): Left channel output mute control
- [k_acodec_set_dacr_mute](#2514-k_acodec_set_dacr_mute): Right channel output mute control
- [k_acodec_get_gain_micl](#2515-k_acodec_get_gain_micl): Obtain the analog gain value of the left channel input
- [k_acodec_get_gain_micr](#2516-k_acodec_get_gain_micr): Get the analog gain value of the right channel input
- [k_acodec_get_adcl_volume](#2518-k_acodec_get_adcl_volume): Gets the left channel input digital volume value
- [k_acodec_get_adcr_volume](#2519-k_acodec_get_adcr_volume): Gets the right channel input digital volume value
- [k_acodec_get_alc_gain_micl](#255-k_acodec_get_alc_gain_micl): Obtain the analog gain value of the ALC left channel input
- [k_acodec_get_alc_gain_micr](#256-k_acodec_get_alc_gain_micr): Get the analog gain value of the right channel input of the ALC
- [k_acodec_get_gain_hpoutl](#257-k_acodec_get_gain_hpoutl): Get the analog volume value of the left channel output
- [k_acodec_get_gain_hpoutr](#258-k_acodec_get_gain_hpoutr): Get the analog volume value of the right channel output
- [k_acodec_get_dacl_volume](#259-k_acodec_get_dacl_volume): Get the left channel output digital volume value
- [k_acodec_get_dacr_volume](#2510-k_acodec_get_dacr_volume): Get the digital volume value of the right channel output
- [k_acodec_reset](#2510-k_acodec_reset):Reset Volume

#### 2.5.1 k_acodec_set_gain_micl

- 【Description】

Left channel input analog gain control

- 【Syntax】

int ioctl (int fd, k_acodec_set_gain_micl, k_u32 \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_gain_micl | IOCTL number                   | input          |
| Arg                    | Unsigned integer pointer            | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

The analog gain ranges are 0db, 6db, 20db, 30db.

#### 2.5.2 k_acodec_set_gain_micr

- 【Description】

Right channel input analog gain control

- 【Syntax】

int ioctl (int fd, k_acodec_set_gain_micr, k_u32 \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_gain_micr | IOCTL number                   | input          |
| Arg                    | Unsigned integer pointer            | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

The analog gain ranges are 0db, 6db, 20db, 30db.

#### 2.5.3 k_acodec_set_adcl_volume

- 【Description】

Left channel input digital gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_adcl_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_adcl_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-97,30]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.4 k_acodec_set_adcr_volume

- 【Description】

Right channel input digital gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_adcr_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_adcr_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-97,30]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.5 k_acodec_set_alc_gain_micl

- 【Description】

Left channel ALC input analog gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_alc_gain_micl, float \*arg);

- 【Parameters】

| **Parameter name**               | **Description**                  | **Input/output** |
| -------------------------- | ------------------------- | ------------- |
| fd                         | Audio Codec device file descriptor | input          |
| k_acodec_set_alc_gain_micl | IOCTL number                   | input          |
| Arg                        | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-18,28.5]`louder the volume, in 1.5dB increments.

#### 2.5.6 k_acodec_set_alc_gain_micr

- 【Description】

Right-channel ALC input analog gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_alc_gain_micr, float \*arg);

- 【Parameters】

| **Parameter name**               | **Description**                  | **Input/output** |
| -------------------------- | ------------------------- | ------------- |
| fd                         | Audio Codec device file descriptor | input          |
| k_acodec_set_alc_gain_micr | IOCTL number                   | input          |
| Arg                        | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-18,28.5]`louder the volume, in 1.5dB increments.

#### 2.5.7 k_acodec_set_gain_hpoutl

- 【Description】

Left channel output analog gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_gain_hpoutl, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_gain_hpoutl | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-39,6]`louder the volume, in 1.5dB increments.

#### 2.5.8 k_acodec_set_gain_hpoutr

- 【Description】

The right channel outputs analog gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_gain_hpoutr, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_gain_hpoutr | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-39,6]`louder the volume, in 1.5dB increments.

#### 2.5.9 k_acodec_set_dacl_volume

- 【Description】

Left channel output digital gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_dacl_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_dacl_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-120,7]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.10 k_acodec_set_dacr_volume

- 【Description】

The right channel outputs digital gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_dacr_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_set_dacr_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-120,7]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.11 k_acodec_set_micl_mute

- 【Description】

Left channel input mute control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_micl_mute, k_bool \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_micl_mute | IOCTL number                   | input          |
| Arg                    | Bool-type pointers                | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Value range: K_TRUE mute, K_FALSE unmute.

#### 2.5.12 k_acodec_set_micr_mute

- 【Description】

Right channel input mute control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_micr_mute, k_bool \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_micr_mute | IOCTL number                   | input          |
| Arg                    | Bool-type pointers                | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Value range: K_TRUE mute, K_FALSE unmute.

#### 2.5.13 k_acodec_set_dacl_mute

- 【Description】

Left channel output mute control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_dacl_mute, k_bool \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_dacl_mute | IOCTL number                   | input          |
| Arg                    | Bool-type pointers                | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Value range: K_TRUE mute, K_FALSE unmute.

#### 2.5.14 k_acodec_set_dacr_mute

- 【Description】

Right channel output mute control.

- 【Syntax】

int ioctl (int fd, k_acodec_set_dacr_mute, k_bool \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_set_dacr_mute | IOCTL number                   | input          |
| Arg                    | Bool-type pointers                | input          |

- 【Return value】

| Return value | description                 |
|--------|----------------------|
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Value range: K_TRUE mute, K_FALSE unmute.

#### 2.5.15 k_acodec_get_gain_micl

- 【Description】

Gets the analog gain value for the left channel input.

- 【Syntax】

int ioctl (int fd, k_acodec_get_gain_micl, k_u32 \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_get_gain_micl | IOCTL number                   | input          |
| Arg                    | Unsigned integer pointer            | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

The obtained analog gain ranges are 0dB, 6dB, 20dB, 30dB.

#### 2.5.16 k_acodec_get_gain_micr

- 【Description】

Gets the right channel input analog gain value.

- 【Syntax】

int ioctl (int fd, k_acodec_get_gain_micr, k_u32 \*arg);

- 【Parameters】

| **Parameter name**           | **Description**                  | **Input/output** |
| ---------------------- | ------------------------- | ------------- |
| fd                     | Audio Codec device file descriptor | input          |
| k_acodec_get_gain_micr | IOCTL number                   | input          |
| Arg                    | Unsigned integer pointer            | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

The obtained analog gain ranges are 0dB, 6dB, 20dB, 30dB.

#### 2.5.18 k_acodec_get_adcl_volume

- 【Description】

Gets the left channel input digital volume value

- 【Syntax】

int ioctl (int fd, k_acodec_get_adcl_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_adcl_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-97,30]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.19 k_acodec_get_adcr_volume

- 【Description】

Gets the right channel input digital gain control value.

- 【Syntax】

int ioctl (int fd, k_acodec_get_adcr_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_adcr_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-97,30]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.5 k_acodec_get_alc_gain_micl

- 【Description】

Obtain the analog gain value for the left channel ALC input.

- 【Syntax】

int ioctl (int fd, k_acodec_set_alc_gain_micl, float \*arg);

- 【Parameters】

| **Parameter name**               | **Description**                  | **Input/output** |
| -------------------------- | ------------------------- | ------------- |
| fd                         | Audio Codec device file descriptor | input          |
| k_acodec_get_alc_gain_micl | IOCTL number                   | input          |
| Arg                        | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-18,28.5]`louder the volume, in 1.5dB increments.

#### 2.5.6 k_acodec_get_alc_gain_micr

- 【Description】

Obtain the analog gain value of the right channel ALC input.

- 【Syntax】

int ioctl (int fd, k_acodec_get_alc_gain_micr, float \*arg);

- 【Parameters】

| **Parameter name**               | **Description**                  | **Input/output** |
| -------------------------- | ------------------------- | ------------- |
| fd                         | Audio Codec device file descriptor | input          |
| k_acodec_get_alc_gain_micr | IOCTL number                   | input          |
| Arg                        | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-18,28.5]`louder the volume, in 1.5dB increments.

#### 2.5.7 k_acodec_get_gain_hpoutl

- 【Description】

Gets the analog gain value of the left channel output.

- 【Syntax】

int ioctl (int fd, k_acodec_get_gain_hpoutl, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_gain_hpoutl | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-39,6]`louder the volume, in 1.5dB increments.

#### 2.5.8 k_acodec_get_gain_hpoutr

- 【Description】

Get right channel output analog gain control.

- 【Syntax】

int ioctl (int fd, k_acodec_get_gain_hpoutr, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_gain_hpoutr | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the larger the assignment, the `[-39,6]`louder the volume, in 1.5dB increments.

#### 2.5.9 k_acodec_get_dacl_volume

- 【Description】

Gets the digital gain value of the left channel output.

- 【Syntax】

int ioctl (int fd, k_acodec_get_dacl_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_dacl_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-120,7]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.10 k_acodec_get_dacr_volume

- 【Description】

Gets the digital gain value of the right channel output.

- 【Syntax】

int ioctl (int fd, k_acodec_get_dacr_volume, float \*arg);

- 【Parameters】

| **Parameter name**             | **Description**                  | **Input/output** |
| ------------------------ | ------------------------- | ------------- |
| fd                       | Audio Codec device file descriptor | input          |
| k_acodec_get_dacr_volume | IOCTL number                   | input          |
| Arg                      | Signed floating-point pointer          | output          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

Analog gain range, the `[-120,7]`larger the assignment, the louder the volume, in 0.5dB increments.

#### 2.5.10 k_acodec_reset

- 【Description】

Volume reset: Includes ADC, DAC, ALC digital and analog gain.

- 【Syntax】

int ioctl (int fd, k_acodec_reset, ...);

- 【Parameters】

| **Parameter name**   | **Description**                  | **Input/output** |
| -------------- | ------------------------- | ------------- |
| fd             | Audio Codec device file descriptor | input          |
| k_acodec_reset | IOCTL number                   | input          |

- 【Return value】

| Return value | description                 |
| ------ | -------------------- |
| 0      | succeed                 |
| Non-0    | Failed, see Error Code for value |

- 【Requirement】

Header file: k_acodec_comm.h

Library file: libacodec.a

- 【Note】

none

### 2.6 Audio coding MAPI

The Audio Coding feature module provides the following MAPIs:

- [kd_mapi_aenc_init](#261-kd_mapi_aenc_init): Initialize the encoding channel
- [kd_mapi_aenc_deinit](#262-kd_mapi_aenc_deinit): Deinitialize the encoding channel.
- [kd_mapi_aenc_start](#263-kd_mapi_aenc_start): Start the encoding channel.
- [kd_mapi_aenc_stop](#264-kd_mapi_aenc_stop):Stop encoding the channel.
- [kd_mapi_aenc_registercallback](#265-kd_mapi_aenc_registercallback): Register the encoding callback function.
- [kd_mapi_aenc_unregistercallback](#266-kd_mapi_aenc_unregistercallback): Deregister the encoding callback function.
- [kd_mapi_aenc_bind_ai](#267-kd_mapi_aenc_bind_ai):Bind AI.
- [kd_mapi_aenc_unbind_ai](#268-kd_mapi_aenc_unbind_ai):Unbind AI.
- [kd_mapi_register_ext_audio_encoder](#269-kd_mapi_register_ext_audio_encoder): Register an external audio encoder.
- [kd_mapi_unregister_ext_audio_encoder](#2610-kd_mapi_unregister_ext_audio_encoder): Unregister the external audio encoder.
- [kd_mapi_aenc_send_frame](#2611-kd_mapi_aenc_send_frame): Send audio encoded audio frames.

#### 2.6.1 kd_mapi_aenc_init

- 【Description】

Initialize the encoding channel.

- 【Syntax】

kd_mapi_aenc_init([k_handle](#331-k_handle) aenc_hdl,const [k_aenc_chn_attr](#323-k_aenc_chn_attr) \*attr);

#### 2.6.2 kd_mapi_aenc_deinit

- 【Description】

Go to initialize the encoding channel.

- 【Syntax】

kd_mapi_aenc_deinit([k_handle](#331-k_handle) aenc_hdl);

#### 2.6.3 kd_mapi_aenc_start

- 【Description】

Start the encoding channel.

- 【Syntax】

kd_mapi_aenc_start([k_handle](#331-k_handle) aenc_hdl);

#### 2.6.4 kd_mapi_aenc_stop

- 【Description】

Stop encoding the channel.

- 【Syntax】

kd_mapi_aenc_stop([k_handle](#331-k_handle) aenc_hdl);

#### 2.6.5 kd_mapi_aenc_registercallback

- 【Description】

Registers the encoding callback function.

- 【Syntax】

k_s32 kd_mapi_aenc_registercallback([k_handle](#331-k_handle) aenc_hdl.k_aenc_callback_s \*aenc_cb);

#### 2.6.6 kd_mapi_aenc_unregistercallback

- 【Description】

Registers the encoding callback function.

- 【Syntax】

k_s32 kd_mapi_aenc_unregistercallback([k_handle](#331-k_handle) aenc_hdl);

#### 2.6.7 kd_mapi_aenc_bind_ai

- 【Description】

Bind AI.

- 【Syntax】

k_s32 kd_mapi_aenc_bind_ai([k_handle](#331-k_handle) ai_hdl.k_handle[](#331-k_handle) aenc_hdl);

#### 2.6.8 kd_mapi_aenc_unbind_ai

- 【Description】

Unbind AI.

- 【Syntax】

k_s32 kd_mapi_aenc_unbind_ai([k_handle](#331-k_handle) ai_hdl.k_handle[](#331-k_handle) aenc_hdl);

#### 2.6.9 kd_mapi_register_ext_audio_encoder

- 【Description】

Register an external encoder.

- 【Syntax】

k_s32 kd_mapi_register_ext_audio_encoder(const [k_aenc_encoder](#322-k_aenc_encoder) \*encoder,k_handle[](#331-k_handle) \* aencoder_hdl);

#### 2.6.10 kd_mapi_unregister_ext_audio_encoder

- 【Description】

Unregister the external audio encoder.

- 【Syntax】

k_s32 kd_mapi_unregister_ext_audio_encoder( [k_handle](#331-k_handle) aencoder_hdl);

#### 2.6.11 kd_mapi_aenc_send_frame

- 【Description】

Send audio encoded audio frames

- 【Syntax】

k_s32 kd_mapi_aenc_send_frame([k_handle](#331-k_handle) ai_hdl,const [k_audio_frame](#3114-k_audio_frame) \*frame);

### 2.7 Audio Decoding MAPI

The Audio Decoding feature module provides the following MAPIs:

- [kd_mapi_adec_init](#261-kd_mapi_aenc_init):Initialize the decoding channel.
- [kd_mapi_adec_deinit](#271-kd_mapi_adec_init):Deinitialize the decoding channel.
- [kd_mapi_adec_start](#273-kd_mapi_adec_start): Start the decoding channel.
- [kd_mapi_adec_stop](#274-kd_mapi_adec_stop):Stop the decoding channel.
- [kd_mapi_adec_registercallback](#275-kd_mapi_adec_registercallback): Register the decode callback function.
- [kd_mapi_adec_unregistercallback](#276-kd_mapi_adec_unregistercallback): Deregister the decoding callback function.
- [kd_mapi_adec_bind_ao](#277-kd_mapi_adec_bind_ao):Bind ao.
- [kd_mapi_adec_unbind_ao](#278-kd_mapi_adec_unbind_ao):Unbind ao.
- [kd_mapi_register_ext_audio_decoder](#279-kd_mapi_register_ext_audio_decoder): Register an external audio decoder.
- [kd_mapi_unregister_ext_audio_decoder](#2710-kd_mapi_unregister_ext_audio_decoder): Deregister the external audio decoder.
- [kd_mapi_adec_send_stream](#2711-kd_mapi_adec_send_stream): Send audio to decode audio frames.

#### 2.7.1 kd_mapi_adec_init

- 【Description】

Initialize the decoding channel.

- 【Syntax】

kd_mapi_adec_init([k_handle](#331-k_handle) adec_hdl,const [k_adec_chn_attr](#323-k_aenc_chn_attr) \*attr);

#### 2.7.2 kd_mapi_adec_deinit

- 【Description】

Deinitialize the decoding channel.

- 【Syntax】

kd_mapi_adec_deinit([k_handle](#331-k_handle) adec_hdl);

#### 2.7.3 kd_mapi_adec_start

- 【Description】

Start the decoding channel.

- 【Syntax】

kd_mapi_adec_start([k_handle](#331-k_handle) adec_hdl);

#### 2.7.4 kd_mapi_adec_stop

- 【Description】

Stop the decoding channel.

- 【Syntax】

kd_mapi_adec_stop([k_handle](#331-k_handle) adec_hdl);

#### 2.7.5 kd_mapi_adec_registercallback

- 【Description】

Register the decode callback function.

- 【Syntax】

k_s32 kd_mapi_adec_registercallback([k_handle](#331-k_handle) adec_hdl.k_adec_callback_s \*adec_cb);

#### 2.7.6 kd_mapi_adec_unregistercallback

- 【Description】

Register the decode callback function.

- 【Syntax】

k_s32 kd_mapi_adec_unregistercallback([k_handle](#331-k_handle) adec_hdl);

#### 2.7.7 kd_mapi_adec_bind_ao

- 【Description】

Bind ao.

- 【Syntax】

k_s32 kd_mapi_adec_bind_ao([k_handle](#331-k_handle) ao_hdl.k_handle[](#331-k_handle) adec_hdl);

#### 2.7.8 kd_mapi_adec_unbind_ao

- 【Description】

Unbind ao.

- 【Syntax】

k_s32 kd_mapi_adec_unbind_ao([k_handle](#331-k_handle) ao_hdl.k_handle[](#331-k_handle) adec_hdl);

#### 2.7.9 kd_mapi_register_ext_audio_decoder

- 【Description】

Register the external decoder.

- 【Syntax】

k_s32 kd_mapi_register_ext_audio_decoder(const [k_adec_decoder](#329-k_adec_decoder) \*decoder,k_handle[](#331-k_handle) \* adecoder_hdl);

#### 2.7.10 kd_mapi_unregister_ext_audio_decoder

- 【Description】

Unregister the external audio decoder.

- 【Syntax】

k_s32 kd_mapi_unregister_ext_audio_decoder( [k_handle](#331-k_handle) adecoder_hdl);

#### 2.7.11 kd_mapi_adec_send_stream

- 【Description】

Send audio to decode audio frames.

- 【Syntax】

k_s32 kd_mapi_adec_send_stream([k_handle](#331-k_handle) ai_hdl,const [k_audio_stream](#327-k_audio_stream) \*stream);

## 3. Data Type

### 3.1 Audio input and output

The data types and data structures related to audio input and output are defined as follows:

- [k_audio_type](#311-k_audio_type): Define the audio input and output type.
- [k_audio_dev](#312-k_audio_dev): Define the audio device.
- [k_ai_chn](#313-k_ai_chn): Define AI audio channels.
- [k_ao_chn](#314-k_ao_chn): Define the AO audio channel.
- [K_MAX_AUDIO_FRAME_NUM](#315-k_max_audio_frame_num): Define the maximum number of audio decoding cache frames.
- [k_audio_bit_width](#316-k_audio_bit_width): Define the audio sampling accuracy.
- [k_audio_snd_mode](#317-k_audio_snd_mode): Define the audio channel mode.
- [k_audio_pdm_oversample](#318-k_audio_pdm_oversample): Define PDM oversampling.
- [k_aio_dev_attr](#3112-k_aio_dev_attr): Define the audio input and output device property structure.
- [k_audio_pdm_attr](#319-k_audio_pdm_attr): Define PDM audio input properties.
- [k_i2s_work_mode](#3111-k_i2s_work_mode): Define the I2S working mode.
- [k_audio_i2s_attr](#3110-k_audio_i2s_attr): Define I2S audio input properties.
- [k_aio_i2s_type](#3113-k_aio_i2s_type): Define the type of I2S docking device.
- [k_audio_frame](#3114-k_audio_frame): Define the audio frame structure.
- [k_audio_anr_cfg](#3115-k_audio_anr_cfg): Define the configuration information structure of the audio speech noise reduction function.
- [k_audio_agc_cfg](#3116-k_audio_agc_cfg): Define the audio auto gain function configuration information structure.
- [k_ai_vqe_cfg](#3117-k_ai_vqe_cfg): Define the audio input sound quality enhancement configuration information structure.

#### 3.1.1 k_audio_type

【Description】

Define audio input and output types.

【Definition】

```c
typedef enum {
KD_AUDIO_INPUT_TYPE_I2S = 0,//i2s in
KD_AUDIO_INPUT_TYPE_PDM = 1,//pdm in
KD_AUDIO_OUTPUT_TYPE_I2S = 2,//i2s out
} k_audio_type;
```

【Note】

The audio input includes I2S and PDM, and the audio output is only I2S.

【See Also】

none

#### 3.1.2 k_audio_dev

【Description】

Define an audio device.

【Definition】

**typedef k_u32 k_audio_dev;**

【Note】

AI module, k_audio_dev values are 0 and 1, where 0 is the I2S audio input and 1 is the PDM audio input.

AO module, the k_audio_dev value is fixed to 0, that is, the I2S audio output.

#### 3.1.3 k_ai_chn

【Description】

Define AI audio channels.

【Definition】

**typedef k_u32 k_ai_chn;**

【Note】

I2S audio input, there are 2 groups, the value range is .`[0,1]`

PDM audio input, there are 4 groups, the value range is .`[0,3]`

#### 3.1.4 k_ao_chn

【Description】

Define the AO audio channel.

【Definition】

**typedef k_u32 k_ao_chn;**

【Note】

I2S audio output, there are 2 groups, the value range is .`[0,1]`

#### 3.1.5 K_MAX_AUDIO_FRAME_NUM

【Description】

Defines the maximum number of audio decoding cache frames.

【Definition】

\#define K_MAX_AUDIO_FRAME_NUM 50

#### 3.1.6 k_audio_bit_width

【Description】

- Define the audio sampling accuracy.

【Definition】

```c
typedef enum {
KD_AUDIO_BIT_WIDTH_16 = 0, /* 16bit width */
KD_AUDIO_BIT_WIDTH_24 = 1, /* 24bit width */
KD_AUDIO_BIT_WIDTH_32 = 2, /* 32bit width */
} k_audio_bit_width;
```

【Note】

none

【See Also】

none

#### 3.1.7 k_audio_snd_mode

【Description】

- Define the channel mode.

【Definition】

```c
typedef enum {
KD_AUDIO_SOUND_MODE_MONO = 0, /* mono */
KD_AUDIO_SOUND_MODE_STEREO = 1, /* stereo */
} k_audio_snd_mode;
```

#### 3.1.8 k_audio_pdm_oversample

【Description】

Define PDM oversampling.

【Definition】

```c
typedef enum
{
KD_AUDIO_PDM_INPUT_OVERSAMPLE_32 = 0,
KD_AUDIO_PDM_INPUT_OVERSAMPLE_64 ,
KD_AUDIO_PDM_INPUT_OVERSAMPLE_128 ,
} k_audio_pdm_oversample;
```

#### 3.1.9 k_audio_pdm_attr

【Description】

Define PDM audio input properties.

【Definition】

```c
typedef struct {
k_u32 chn_cnt; /* channle number on FS,i2s valid value:1/2,pdm valid value:1/2/3/4*/
k_audio_sample_rate rate;
k_audio_bit_width width;
k_audio_snd_mode mode;
k_audio_pdm_oversample oversample;
k_u32 frame_num; /* frame num in buf[2,K_MAX_AUDIO_FRAME_NUM] */
k_u32 point_num_per_frame;
} k_audio_pdm_attr;
```

【Members】

| Member name            | description                                                |
|---------------------|-----------------------------------------------------|
| chn_cnt             | The number of channels supported.  Supports 1-4 channels, and channel enablement needs to be continuous. |
| sample_rate         | Sample rate: support 8K\~192K                                 |
| bit_width           | Sampling accuracy: support 16/24/32                              |
| snd_mode            | Audio channel mode. Supports mono and dual channels.                  |
| pdm_oversample      | Oversampling: Supports 32, 64, and 128 times oversampling.                   |
| frame_num           | The number of cached frames`[2,K_MAX_AUDIO_FRAME_NUM]`.               |
| point_num_per_frame | The number of sample points per frame.                                  |

【Note】

none

【See Also】

none

#### 3.1.10 k_audio_i2s_attr

【Description】

Define I2S audio input properties.

【Definition】

```c
typedef struct
{
k_u32 chn_cnt; /* channle number on FS,i2s valid value:1/2,pdm valid value:1/2/3/4 */
k_u32 sample_rate; /* sample rate 8k ~192k */
k_audio_bit_width bit_width;
k_audio_snd_mode snd_mode; /* momo or stereo */
k_i2s_work_mode   i2s_mode;  /*i2s work mode*/
k_u32 frame_num; /* frame num in buf[2,K_MAX_AUDIO_FRAME_NUM] */
k_u32 point_num_per_frame;
k_aio_i2s_type type;
} k_audio_i2s_attr;
```

【Members】

| Member name            | description                                                 |
| ------------------- | ---------------------------------------------------- |
| chn_cnt             | The number of channels supported.  Support 1-2 channels.                    |
| sample_rate         | Sample rate: support 8K~192K                                   |
| bit_width           | Sampling accuracy: support 16/24/32                               |
| snd_mode            | Audio channel mode. Supports mono and dual channels.                   |
| I2s_mode            | I2S working mode: support Philips mode, left alignment mode, right alignment mode. |
| frame_num           | The number of cached frames`[2,K_MAX_AUDIO_FRAME_NUM]`.              |
| point_num_per_frame | The number of sample points per frame`[sample_rate/100,sample_rate]`.    |
| i2s_type            | I2S docking device type: built-in codec or external device.                |

【Note】

The number of sample points per frame point_num_per_frame and the value of the sample rate sample_rate determine the hardware generation

The frequency of interruptions, too high a frequency will affect the performance of the system, and other services will also affect each other, it is recommended that these two parameters be involved

The value of the number satisfies the formula: (point_num_per_frame * 1000) / sample_rate > = 10 (interrupt 100 times), such as sampling

When the rate is 16000Hz, it is recommended that the number of sampling points be greater than or equal to 160.

【See Also】

none

#### 3.1.11 k_i2s_work_mode

【Description】

Define the I2S operating mode.

【Definition】

```c
typedef enum
{
K_STANDARD_MODE = 1,
K_RIGHT_JUSTIFYING_MODE = 2,
K_LEFT_JUSTIFYING_MODE = 4
} k_i2s_work_mode;
```

【Note】

none

【See Also】

none

#### 3.1.12 k_aio_dev_attr

【Description】

Defines the audio input/output device property structure.

【Definition】

```c
typedef struct {
k_audio_type type;
union
{
k_audio_pdm_attr pdm_attr;
k_audio_i2s_attr i2s_attr;
} kd_audio_attr;
} k_aio_dev_attr;
```

【Members】

| Member name      | description         |
|---------------|--------------|
| audio_type    | Audio type.   |
| kd_audio_attr | Audio property settings |

【Note】

none

【See Also】

none

#### 3.1.13 k_aio_i2s_type

【Description】

Define the I2S docking device type.

【Definition】

```c
typedef enum
{
K_AIO_I2STYPE_INNERCODEC = 0, /* AIO I2S connect inner audio CODEC */
K_AIO_I2STYPE_EXTERN,/* AIO I2S connect extern hardware */
} k_aio_i2s_type;
```

【Note】

The built-in audio codec uses the group 0 I2S path, and the group 1 I2S path still uses an external codec.

【See Also】

none

#### 3.1.14 k_audio_frame

【Description】

Defines the audio frame structure.

【Definition】

```c
typedef struct {
k_audio_bit_width bit_width;
k_audio_snd_mode snd_mode;
void* virt_addr;
k_u64 phys_addr;
k_u64 time_stamp; /* audio frame time stamp */
k_u32 seq; /* audio frame seq */
k_u32 len; /* data lenth per channel in frame */
k_u32 pool_id;
} k_audio_frame;
```

【Members】

| Member name   | description                       |
|------------|----------------------------|
| bit_width  | Sampling accuracy.                 |
| snd_mode   | Audio channel mode.             |
| virt_addr  | Audio frame data virtual address.       |
| phys_addr  | The physical address of the audio frame data.       |
| time_stamp | Audio frame timestamp, in μs. |
| seq        | Audio frame sequence number.               |
| only        | Audio frame length, in bytes. |
| pool_id    | Audio framebuffer pool ID.           |

【Note】

none

【See Also】

none

#### 3.1.15 k_audio_anr_cfg

【Description】

Define the audio voice noise reduction feature configuration information structure.

【Definition】

```c
typedef struct

{
k_bool anr_switch;
} k_audio_anr_cfg;
```

【Members】

| Member name   | description                   |
|------------|------------------------|
| anr_switch | Audio voice noise reduction function enabled. |

【Note】

none

【See Also】

none

#### 3.1.16 k_audio_agc_cfg

【Description】

Define the audio auto-gain function configuration information structure.

【Definition】

```c
typedef struct
{
k_bool agc_switch;
} k_audio_agc_cfg;
```

【Members】

| Member name   | description                   |
|------------|------------------------|
| agc_switch | Audio auto-gain is enabled. |

【Note】

none

【See Also】

none

#### 3.1.17 k_ai_vqe_cfg

【Description】

Define the audio input sound quality enhancement configuration information structure.

【Definition】

typedef struct
{
k_audio_anr_cfg anr_cfg;
k_audio_agc_cfg agc_cfg;
} k_ai_vqe_cfg;

【Members】

| Member name | description                       |
|----------|----------------------------|
| anr_cfg  | Audio voice noise reduction function configuration parameters. |
| agc_cfg  | Audio automatic gain control configuration parameters. |

【Note】

none

【See Also】

none

### 3.2 Audio codec

The relevant data types and data structures of audio codecs are defined as follows:

[k_payload_type](#321-k_payload_type)

[k_aenc_encoder](#322-k_aenc_encoder)

[k_aenc_chn_attr](#323-k_aenc_chn_attr)

[AENC_MAX_CHN_NUMS](#324-aenc_max_chn_nums)

[K_MAX_ENCODER_NAME_LEN](#325-k_max_encoder_name_len)

[k_aenc_chn](#326-k_aenc_chn)

[k_audio_stream](#327-k_audio_stream)

[k_adec_chn_attr](#328-k_adec_chn_attr)

[k_adec_decoder](#329-k_adec_decoder)

[K_MAX_DECODER_NAME_LEN](#3210-k_max_decoder_name_len)

[ADEC_MAX_CHN_NUMS](#3211-adec_max_chn_nums)

#### 3.2.1 k_payload_type

【Description】

Define an audio and video payload type enumeration.

【Definition】

```c
typedef enum {
K_PT_PCMU = 0,
K_PT_1016 = 1,
K_PT_G721 = 2,
K_PT_GSM = 3,
K_PT_G723 = 4,
K_PT_DVI4_8K = 5,
K_PT_DVI4_16K = 6,
K_PT_LPC = 7,
K_PT_PCMA = 8,
K_PT_G722 = 9,
K_PT_S16BE_STEREO = 10,
K_PT_S16BE_MONO = 11,
K_PT_QCELP = 12,
K_PT_CN = 13,
K_PT_MPEGAUDIO = 14,
K_PT_G728 = 15,
K_PT_DVI4_3 = 16,
K_PT_DVI4_4 = 17,
K_PT_G729 = 18,
K_PT_G711A = 19,
K_PT_G711U = 20,
K_PT_G726 = 21,
K_PT_G729A = 22,
K_PT_LPCM = 23,
K_PT_CelB = 25,
K_PT_JPEG = 26,
K_PT_CUSM = 27,
K_PT_NV = 28,
K_PT_PICW = 29,
K_PT_CPV = 30,
K_PT_H261 = 31,
K_PT_MPEGVIDEO = 32,
K_PT_MPEG2TS = 33,
K_PT_H263 = 34,
K_PT_SPEG = 35,
K_PT_MPEG2VIDEO = 36,
K_PT_AAC = 37,
K_PT_WMA9STD = 38,
K_PT_HEAAC = 39,
K_PT_PCM_VOICE = 40,
K_PT_PCM_AUDIO = 41,
K_PT_MP3 = 43,
K_PT_ADPCMA = 49,
K_PT_AEC = 50,
K_PT_X_LD = 95,
K_PT_H264 = 96,
K_PT_D_GSM_HR = 200,
K_PT_D_GSM_EFR = 201,
K_PT_D_L8 = 202,
K_PT_D_RED = 203,
K_PT_D_VDVI = 204,
K_PT_D_BT656 = 220,
K_PT_D_H263_1998 = 221,
K_PT_D_MP1S = 222,
K_PT_D_MP2P = 223,
K_PT_D_BMPEG = 224,
K_PT_MP4VIDEO = 230,
K_PT_MP4AUDIO = 237,
K_PT_VC1 = 238,
K_PT_JVC_ASF = 255,
K_PT_D_AVI = 256,
K_PT_DIVX3 = 257,
K_PT_AVS = 258,
K_PT_REAL8 = 259,
K_PT_REAL9 = 260,
K_PT_VP6 = 261,
K_PT_VP6F = 262,
K_PT_VP6A = 263,
K_PT_SORENSON = 264,
K_PT_H265 = 265,
K_PT_VP8 = 266,
K_PT_MVC = 267,
K_PT_PNG = 268,
K_PT_AMR = 1001,
K_PT_MJPEG = 1002,
K_PT_AMRWB = 1003,
K_PT_PRORES = 1006,
K_PT_OPUS = 1007,
K_PT_BUTT
} k_payload_type;
```

【Note】

none

【See Also】

none

#### 3.2.2 k_aenc_encoder

【Description】

Define the encoder property structure.

【Definition】

```c
typedef struct {
k_payload_type k_u32 max_frame_len;
k_char name[K_MAX_ENCODER_NAME_LEN];
k_s32 (func_open_encoder)(void encoder_attr,void *encoder);
k_s32 (func_enc_frame)(void *encoder,const k_audio_frame *data,k_u8 *outbuf, k_u32 *out_len);
k_s32 (*func_close_encoder)(void *encoder);
} k_aenc_encoder;

```

【Members】

| Member name           | description                    |
|--------------------|-------------------------|
| type               | Encoded protocol type.          |
| max_frame_len      | Maximum bitstream length.          |
| name               | Encoder name.            |
| func_open_encoder  | Open the function pointer for the encoder.  |
| func_enc_frame     | The function pointer to be encoded.    |
| func_close_encoder | Turn off the encoder's function pointer.  |

【Note】

none

【See Also】

none

#### 3.2.3 k_aenc_chn_attr

【Description】

Defines the encoder channel property structure.

【Definition】

```c
typedef struct {
k_payload_type type;
k_u32 point_num_per_frame;
k_u32 buf_size; // buf size[2,K_MAX_AUDIO_FRAME_NUM]
} k_aenc_chn_attr;
```

【Members】

| Member name            | description                                                                                                    |
|---------------------|---------------------------------------------------------------------------------------------------------|
| type                | Audio encoding protocol type.                                                                                      |
| point_num_per_frame | The corresponding frame length of the audio coding protocol (the audio frame length received when encoding is less than or equal to that frame length can be encoded).                          |
| buf_size            | Audio encoding cache size.  Value range:`[2, K_MAX_AUDIO_FRAME_NUM]` in frames. |

【Note】

none

【See Also】

none

#### 3.2.4 AENC_MAX_CHN_NUMS

【Description】

Defines the maximum number of encoded channels.

【Definition】

\#define AENC_MAX_CHN_NUMS 4

【Note】

none

【See Also】

none

#### 3.2.5 K_MAX_ENCODER_NAME_LEN

【Description】

Defines the audio encoder name maximum length.

【Definition】

\#define K_MAX_ENCODER_NAME_LEN 25

【Note】

none

【See Also】

none

#### 3.2.6 k_aenc_chn

【Description】

Defines the encoding channel type.

【Definition】

typedef k_u32 k_aenc_chn;

【Note】

none

【See Also】

none

#### 3.2.7 k_audio_stream

【Description】

Define the bitstream structure.

【Definition】

```c
typedef struct {
void *stream; /* the virtual address of stream */
k_u64 phys_addr; /* the physics address of stream */
k_u32 len; /* stream lenth, by bytes */
k_u64 time_stamp; /* frame time stamp */
k_u32 seq; /* frame seq, if stream is not a valid frame,seq is 0 */
} k_audio_stream;
```

【Members】

| Member name   | description                         |
|------------|------------------------------|
| stream     | Audio stream data pointer             |
| phys_addr  | The physical address of the audio stream.         |
| only        | Audio stream length. Units in byte. |
| time_stamp | Audio stream timestamp.             |
| seq        | Audio stream sequence number.               |

【Note】

none

【See Also】

none

#### 3.2.8 k_adec_chn_attr

【Description】

Defines the decoder channel property structure.

【Definition】

```c
typedef struct {
k_payload_type payload_type;
k_u32 point_num_per_frame;
k_u32 buf_size; /* buf size[2~K_MAX_AUDIO_FRAME_NUM] */
} k_adec_chn_attr;
```

【Members】

| Member name            | description                                                                                                    |
|---------------------|---------------------------------------------------------------------------------------------------------|
| type                | Audio decoding protocol type.                                                                                      |
| point_num_per_frame | The frame length corresponding to the audio decoding protocol                                                                                  |
| buf_size            | Audio encoding cache size.  Value range:`[2, K_MAX_AUDIO_FRAME_NUM]` in frames. |

【Note】

Some properties of audio decoding need to match output device properties, such as sample rate, frame length (samples per frame

Number of points), etc.

【See Also】

none

#### 3.2.9 k_adec_decoder

【Description】

Defines the decoder property structure.

【Definition】

```c
typedef struct {
k_payload_type payload_type;
k_char name[K_MAX_DECODER_NAME_LEN];
k_s32 (func_open_decoder)(void *decoder_attr, void **decoder);
k_s32 (*func_dec_frame)(void *decoder, k_u8 **inbuf, k_s32 *left_byte, k_u16*outbuf, k_u32 *out_len, k_u32 *chns);
k_s32 (*func_get_frame_info)(void *decoder, void *info);
k_s32 (*func_close_decoder)(void *decoder);
k_s32 (*func_reset_decoder)(void *decoder);
} k_adec_decoder;
```

【Members】

| Member name            | description                                    |
|---------------------|-----------------------------------------|
| type                | Decodes the protocol type.                          |
| name                | Decoder name.                            |
| func_open_decoder   | Open the function pointer for the decoder.                  |
| func_get_frame_info | A function pointer that gets audio frame information.              |
| func_close_decoder  | Turns off the function pointer for the decoder.                  |
| func_reset_decoder  | Empty the buffer buffer, reset the decoder's function pointer.  |

【Note】

none

【See Also】

none

#### 3.2.10 K_MAX_DECODER_NAME_LEN

【Description】

Defines the maximum length of the audio decoder name.

【Definition】

\#define K_MAX_DECODER_NAME_LEN 25

【Note】

none

【See Also】

none

#### 3.2.11 ADEC_MAX_CHN_NUMS

【Description】

Defines the maximum number of decoding channels.

【Definition】

\#define ADEC_MAX_CHN_NUMS 4

【Note】

none

【See Also】

none

#### 3.2.12 k_adec_chn

【Description】

Defines the decoding channel type.

【Definition】

typedef k_u32 k_adec_chn;

【Note】

none

【See Also】

none

### 3.3 MAPI

The data types and data structures related to audio MAPI are defined as follows

[k_handle](#331-k_handle)

#### 3.3.1 k_handle

【Description】

Define the operation handle.

【Definition】

typedef k_u32 k_handle;

【See Also】

none

## 4. Error codes

### 4.1 Audio Input API Error Code

| Error code | Macro definitions                 | description                        |
|----------|------------------------|-----------------------------|
|0xA0158001| K_ERR_AI_INVALID_DEVID | The audio input device number is invalid          |
|0xA0158002| K_ERR_AI_INVALID_CHNID | The audio input channel number is invalid          |
|0xA0158003| K_ERR_AI_ILLEGAL_PARAM | The audio input parameter setting is invalid        |
|0xA0158004| K_ERR_AI_NOT_ENABLED   | The audio input device or channel is not enabled |
|0xA0158005| K_ERR_AI_NULL_PTR      | The input parameter null pointer is incorrect          |
|0xA0158006| K_ERR_AI_NOT_CFG       | Audio input device properties are not set      |
|0xA0158007| K_ERR_AI_NOT_SUPPORT   | Operation is not supported                  |
|0xA0158008| K_ERR_AI_NOT_PERM      | Operation is not allowed                  |
|0xA0158009| K_ERR_AI_NO_MEM        | Failed to allocate memory                |
|0xA015800A| K_ERR_AI_NO_BUF        | Insufficient audio input cache            |
|0xA015800B| K_ERR_AI_BUF_EMPTY     | The audio input cache is empty            |
|0xA015800C| K_ERR_AI_BUF_FULL      | The audio input cache is full            |
|0xA015800D| K_ERR_AI_NOT_READY     | The audio input system is not initialized        |
|0xA015800E| K_ERR_AI_BUSY          | The audio input system is busy              |

### 4.2 Audio Output API error codes

| Error code | Macro definitions                  | description                      |
|----------|-------------------------|---------------------------|
|0xA0159001| K_ERR_AO_INVALID_DEV_ID | The audio output device number is invalid        |
|0xA0159002| K_ERR_AO_INVALID_CHN_ID | The audio output channel number is invalid        |
|0xA0159003| K_ERR_AO_ILLEGAL_PARAM  | The audio output parameter setting is invalid      |
|0xA0159004| K_ERR_AO_NOT_ENABLED    | The audio output device or channel is not enabled  |
|0xA0159005| K_ERR_AO_NULL_PTR       | Output null pointer error            |
|0xA0159006| K_ERR_AO_NOT_CFG        | The audio output device property is not set    |
|0xA0159007| K_ERR_AO_NOT_SUPPORT    | The operation is not supported              |
|0xA0159008| K_ERR_AO_NOT_PERM       | Operation is not allowed                |
|0xA0159009| K_ERR_AO_NO_MEM         | The system is low on memory              |
|0xA015900A| K_ERR_AO_NO_BUF         | Insufficient audio output cache          |
|0xA015900B| K_ERR_AO_BUF_EMPTY      | The audio output cache is empty          |
|0xA015900C| K_ERR_AO_BUF_FULL       | The audio output cache is full          |
|0xA015900D| K_ERR_AO_NOT_READY      | The audio output system is not initialized      |
|0xA015900E| K_ERR_AO_BUSY           | The audio output system is busy            |
