# K230 Audio API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliated companies. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for use as a reference guide only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual is allowed to excerpt, copy, or disseminate part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

The AUDIO module includes four sub-modules: audio input, audio output, audio encoding, and audio decoding, as well as control of the built-in audio codec.

### Intended Audience

This document (this guide) is mainly intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description         |
|--------------|---------------------|
| ai           | Audio Input Module  |
| ao           | Audio Output Module |
| aenc         | Audio Encoding Module |
| adec         | Audio Decoding Module |

### Revision History

| Document Version | Description                                                     | Author       | Date       |
|------------------|-----------------------------------------------------------------|--------------|------------|
| V1.0             | Initial version                                                 | Sun Xiaopeng | 2023/3/7   |
| V1.1             | 1) Added support for i2s built-in codec 2) Added support for pdm single/dual channel 3) Added support for different sampling precision (16/24/32) for ai and ao 4) API interface unchanged, added parameter attributes, improved documentation. | Sun Xiaopeng | 2023/3/27  |
| V1.1.1           | Added audio encoding and decoding API interfaces, added sound quality enhancement API interfaces [kd_mpi_ai_set_vqe_attr](#219-kd_mpi_ai_set_vqe_attr)/[kd_mpi_ai_get_vqe_attr](#2110-kd_mpi_ai_get_vqe_attr), and explanations. | Sun Xiaopeng/Cui Yan | 2023/4/12 |
| V1.2             | Modified sound quality enhancement API interfaces [kd_mpi_ai_set_vqe_attr](#219-kd_mpi_ai_set_vqe_attr)/[kd_mpi_ai_get_vqe_attr](#2110-kd_mpi_ai_get_vqe_attr), added audio encoding and decoding mapi interface functions | Sun Xiaopeng/Cui Yan | 2023/4/27 |
| V1.3             | 1) Added built-in Audio Codec API interfaces                     | Sun Xiaopeng | 2023/5/10  |
| v1.4             | 1) i2s supports single and dual channel input and output, modified [k_audio_i2s_attr](#3110-k_audio_i2s_attr) attributes, added snd_mode attribute. 2) Added built-in Audio Codec API interfaces: including volume acquisition and reset related interfaces: [k_acodec_get_gain_micl](#257-k_acodec_get_gain_hpoutl)/[k_acodec_get_gain_micr](#2516-k_acodec_get_gain_micr)/[k_acodec_get_adcl_volume](#2518-k_acodec_get_adcl_volume)/[k_acodec_get_adcr_volume](#2519-k_acodec_get_adcr_volume)/[k_acodec_get_alc_gain_micl](#255-k_acodec_get_alc_gain_micl)/[k_acodec_get_alc_gain_micr](#256-k_acodec_get_alc_gain_micr)/[k_acodec_get_gain_hpoutl](#257-k_acodec_get_gain_hpoutl)/[k_acodec_get_gain_hpoutr](#258-k_acodec_get_gain_hpoutr)/[k_acodec_get_dacl_volume](#259-k_acodec_get_dacl_volume)/[k_acodec_get_dacr_volume](#2510-k_acodec_get_dacr_volume)/[k_acodec_reset](#2510-k_acodec_reset) | Sun Xiaopeng | 2023/6/15 |
| V1.5             | 1) Added control for selecting single channel for audio input and output | Sun Xiaopeng | 2024/6/5   |

## 1. Overview

### 1.1 Overview

The audio module includes four sub-modules: audio input (ai), audio output (ao), audio encoding (aenc), and audio decoding (adec), as well as support for the built-in analog audio codec. The audio input module includes two types of audio interfaces, i2s and pdm, working with pdma for memory copying. It supports digital microphones (pdm/i2s) and analog audio codec (i2s) sound source input, with an internal analog audio codec that supports sound quality enhancement (VQE) processing: 3A (AEC echo cancellation, ANR noise reduction, AGC automatic gain control). The audio output module supports the i2s audio interface, working with pdma for memory copying, and can connect external data speakers or analog audio codecs for sound output. The audio encoding and decoding modules currently support G711 format audio encoding and decoding functions and support external codec registration.

The audio module is split into multiple sub-modules, with low-coupling data flow transmission between modules. This design meets the existing multimedia business requirements under MAIX3. The following diagram analyzes the usage scenario of the audio module in a voice intercom business. The audio data collected by the audio input module is encoded by the audio encoding module and then sent to the remote end through the network. The audio encoded data obtained from the remote end is decoded by the audio decoding module and then played through the audio output module.

![img](../../../../zh/01_software/board/mpp/images/b96e2ea6fe9536e76af33afe46b2069e.png)

### 1.2 Function Description

#### 1.2.1 Audio Input

The audio input module (AI) mainly implements the configuration and activation of audio input devices and the acquisition of audio frame data.

The audio input module supports i2s and pdm protocol interfaces. i2s supports simultaneous collection of up to 2 dual-channel audio streams, and pdm supports simultaneous collection of up to 8 single-channel audio streams. Detailed i2s and pdm features are as follows:

- i2s audio interface

  1. Data sampling rates support 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz, with sampling precision supporting 16/24/32bit.

  1. Supports 2 configurable IO groups for input/output of I2S audio data, supporting full-duplex mode.

- pdm audio interface

  1. Supports PDM audio input, 1-bit width, sampling clock frequencies of 0.256MHz/0.384MHz/0.512MHz/0.768MHz/1.024MHz/1.4112MHz/1.536MHz/2.048MHz/2.8224MHz/3.072MHz/4.096MHz/5.6448MHz/6.144MHz/12.288MHz/24.576MHz, with the input PCM audio sampling rates of 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz. Sampling precision supports 16/24/32bit.

  1. Supports oversampling rates of 128, 64, and 32 times.

  1. Supports 1-4 IOs for inputting PDM audio data.

  1. Input supports configurable 1-8 PDM channels, supporting PDM left and right single-channel mode and dual-channel mode. Each IO channel mode is unified, and PDM dual-channel mode uses up to 4 IOs.

  1. Enabled channel numbers are continuous from small to large and do not support random enabling of channels.

#### 1.2.2 Audio Output

The audio output (AO) mainly implements the activation of audio output devices and the sending of audio frames to the output channel.

The audio output module supports the i2s protocol interface. i2s supports simultaneous output of up to 2 dual-channel audio streams.

- i2s audio interface

  1. Data sampling rates support 8kHz/12kHz/16kHz/24kHz/32kHz/44.1kHz/48kHz/96kHz/192kHz, with sampling precision of 16/24/32bit.

  1. Supports 2 configurable IO groups for input/output of I2S audio data, supporting full-duplex mode.

#### 1.2.3 Audio Link

- The signal received from the analog microphone by the audio codec is converted to I2S format PCM data and input into the audio's I2S. The PCM data output by I2S, after passing through the audio codec, is converted to an analog signal and emitted. This mode does not use digital IO, and the fixed I2S sdi0 and sdo0 interfaces are used.

- I2S directly connects with external digital microphones and PAs. There are two sets of interfaces to choose from: sdi0, sdo0, and sdi1, sdo1.

- External PDM microphones input up to 8 PDM data streams to the audio's 4 input data interfaces.

Selectable links include:

- 3 sets of pdm_in + 1 set of i2s_in + 2 sets of i2s out, where 1 set of i2s_in can use the built-in audio codec or external

- 4 sets of pdm_in + 2 sets of i2s out

- 2 sets of i2s_in + 2 sets of pdm_in + 2 sets of i2s out

You can use the built-in codec or external devices (audio sub-boards) to test audio-related functions. Using the built-in codec, you can test one set of I2S audio input and output and related audio codec functions. Using the audio sub-board, you can test 2 sets of i2s audio input and output and 4 sets of pdm audio input functions.

![img](../../../../zh/01_software/board/mpp/images/b76dc39c5256a09c53be0e7572c2f587.png)

#### 1.2.4 Sound Quality Enhancement

The audio module supports sound quality enhancement processing for audio data, realizing audio 3A functions. Currently supported sampling precision is 16bit, with a supported sampling rate of 16k.

## 2. API Reference

### 2.1 Audio Input

This functional module provides the following APIs:

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

**Description**:

Set AI device attributes.

**Syntax**:

```c
k_s32 kd_mpi_ai_set_pub_attr([k_audio_dev](#312-k_audio_dev) ai_dev, const [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);
```

**Parameters**:

| Parameter | Description              | Input/Output |
|-----------|--------------------------|--------------|
| ai_dev    | Audio device number.     | Input        |
| attr      | AI device attribute pointer. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

**Notes**:

None

**Example**:

```c
k_aio_dev_attr aio_dev_attr;
memset(&aio_dev_attr, 0, sizeof(aio_dev_attr));
aio_dev_attr.audio_type = KD_AUDIO_INPUT_TYPE_I2S;
aio_dev_attr.kd_audio_attr.i2s_attr.sample_rate = 44100;
aio_dev_attr.kd_audio_attr.i2s_attr.bit_width = KD_AUDIO_BIT_WIDTH_16;
aio_dev_attr.kd_audio_attr.i2s_attr.chn_cnt = 2;
aio_dev_attr.kd_audio_attr.i2s_attr.i2s_mode = K_STANDARD_MODE;
aio_dev_attr.kd_audio_attr.i2s_attr.frame_num = 25;
aio_dev_attr.kd_audio_attr.i2s_attr.point_num_per_frame = 44100 / 25;
aio_dev_attr.kd_audio_attr.i2s_attr.i2s_type = K_AIO_I2STYPE_INNERCODEC;
if (K_SUCCESS != kd_mpi_ai_set_pub_attr(0, &aio_dev_attr)) {
    printf("kd_mpi_ai_set_pub_attr failed\n");
    return K_FAILED;
}
if (K_SUCCESS != kd_mpi_ai_enable(0)) {
    printf("kd_mpi_ai_set_pub_attr failed\n");
    return K_FAILED;
}
if (K_SUCCESS != kd_mpi_ai_enable_chn(0, 0)) {
    printf("kd_mpi_ai_set_pub_attr failed\n");
    return K_FAILED;
}
```

### 2.1.2 kd_mpi_ai_get_pub_attr

**Description**:

Get AI device attributes.

**Syntax**:

```c
k_s32 kd_mpi_ai_get_pub_attr([k_audio_dev](#312-k_audio_dev) ai_dev, [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |
| attr      | AI device attribute pointer. | Output       |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.3 kd_mpi_ai_enable

**Description**:

Enable AI device.

**Syntax**:

```c
k_s32 kd_mpi_ai_enable([k_audio_dev](#312-k_audio_dev) ai_dev);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.4 kd_mpi_ai_disable

**Description**:

Disable AI device.

**Syntax**:

```c
k_s32 kd_mpi_ai_disable([k_audio_dev](#312-k_audio_dev) ai_dev);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.5 kd_mpi_ai_enable_chn

**Description**:

Enable AI channel.

**Syntax**:

```c
k_s32 kd_mpi_ai_enable_chn([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |
| ai_chn    | Audio channel number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.6 kd_mpi_ai_disable_chn

**Description**:

Disable AI channel.

**Syntax**:

```c
k_s32 kd_mpi_ai_disable_chn([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |
| ai_chn    | Audio channel number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.7 kd_mpi_ai_get_frame

**Description**:

Get audio frame.

**Syntax**:

```c
k_s32 kd_mpi_ai_get_frame([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn, [k_audio_frame](#3114-k_audio_frame) *frame, k_u32 milli_sec);
```

**Parameters**:

| Parameter  | Description                                                                                      | Input/Output |
|------------|--------------------------------------------------------------------------------------------------|--------------|
| ai_dev     | Audio device number.                                                                             | Input        |
| ai_chn     | Audio channel number.                                                                            | Input        |
| frame      | Audio frame data.                                                                                | Output       |
| milli_sec  | Timeout for getting data. -1 means blocking mode, waiting indefinitely if no data; 0 means non-blocking mode, returning an error if no data; >0 means blocking for milli_sec milliseconds, returning an error if timeout. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

**Notes**:

- The value of milli_sec must be greater than or equal to -1. When it is -1, data is retrieved in blocking mode. When it is 0, data is retrieved in non-blocking mode. When it is greater than 0, it blocks for milli_sec milliseconds, and if there is no data, it returns a timeout error.
- The corresponding AI channel must be enabled before retrieving audio frame data.

**Example**:

```c
k_audio_frame audio_frame;
while(true) {
    // get frame
    if (K_SUCCESS != kd_mpi_ai_get_frame(dev_num, channel, &audio_frame, 1000)) {
        printf("=========kd_mpi_ai_get_frame timeout\n");
        continue;
    }
    // process frame
    process_frame(&audio_frame);
    // release frame
    kd_mpi_ai_release_frame(dev_num, channel, &audio_frame);
}
```

### 2.1.8 kd_mpi_ai_release_frame

**Description**:

Release audio frame.

**Syntax**:

```c
k_s32 kd_mpi_ai_release_frame([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn, const [k_audio_frame](#3114-k_audio_frame) *frame);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ai_dev    | Audio device number. | Input        |
| ai_chn    | Audio channel number. | Input        |
| frame     | Audio frame data.    | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.1.9 kd_mpi_ai_set_vqe_attr

**Description**:

Set AI sound quality enhancement attributes.

**Syntax**:

```c
k_s32 kd_mpi_ai_set_vqe_attr([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn, const k_bool *vqe_enable);
```

**Parameters**:

| Parameter  | Description                              | Input/Output |
|------------|------------------------------------------|--------------|
| ai_dev     | Audio device number.                     | Input        |
| ai_chn     | Audio channel number.                    | Input        |
| vqe_enable | Sound quality enhancement enable flag. K_TRUE: enable. K_FALSE: disable. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

**Notes**:

Currently supported sampling precision is 16bit, and supported sampling rates are 8k and 16k.

### 2.1.10 kd_mpi_ai_get_vqe_attr

**Description**:

Get AI sound quality enhancement attributes.

**Syntax**:

```c
k_s32 kd_mpi_ai_get_vqe_attr([k_audio_dev](#312-k_audio_dev) ai_dev, [k_ai_chn](#313-k_ai_chn) ai_chn, k_bool *vqe_enable);
```

**Parameters**:

| Parameter  | Description                              | Input/Output |
|------------|------------------------------------------|--------------|
| ai_dev     | Audio device number.                     | Input        |
| ai_chn     | Audio channel number.                    | Input        |
| vqe_enable | Pointer to sound quality enhancement enable flag. K_TRUE: enable. K_FALSE: disable. | Output       |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

### 2.2 Audio Output

This functional module provides the following APIs:

- [kd_mpi_ao_set_pub_attr](#221-kd_mpi_ao_set_pub_attr)
- [kd_mpi_ao_get_pub_attr](#222-kd_mpi_ao_get_pub_attr)
- [kd_mpi_ao_enable](#223-kd_mpi_ao_enable)
- [kd_mpi_ao_disable](#224-kd_mpi_ao_disable)
- [kd_mpi_ao_enable_chn](#225-kd_mpi_ao_enable_chn)
- [kd_mpi_ao_disable_chn](#226-kd_mpi_ao_disable_chn)
- [kd_mpi_ao_send_frame](#227-kd_mpi_ao_send_frame)

### 2.2.1 kd_mpi_ao_set_pub_attr

**Description**:

Set AO device attributes.

**Syntax**:

```c
k_s32 kd_mpi_ao_set_pub_attr([k_audio_dev](#312-k_audio_dev) ao_dev, const [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |
| attr      | AO device attribute pointer. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

**Notes**:

None

**Example**:

```c
k_aio_dev_attr ao_dev_attr;
memset(&ao_dev_attr, 0, sizeof(ao_dev_attr));
ao_dev_attr.audio_type = KD_AUDIO_OUTPUT_TYPE_I2S;
ao_dev_attr.kd_audio_attr.i2s_attr.sample_rate = 48000;
ao_dev_attr.kd_audio_attr.i2s_attr.bit_width = KD_AUDIO_BIT_WIDTH_24;
ao_dev_attr.kd_audio_attr.i2s_attr.chn_cnt = 2;
ao_dev_attr.kd_audio_attr.i2s_attr.i2s_mode = K_RIGHT_JUSTIFYING_MODE;
ao_dev_attr.kd_audio_attr.i2s_attr.frame_num = 15;
ao_dev_attr.kd_audio_attr.i2s_attr.point_num_per_frame = 48000 / 25;
ao_dev_attr.kd_audio_attr.i2s_attr.i2s_type = K_AIO_I2STYPE_EXTERN;
if (K_SUCCESS != kd_mpi_ao_set_pub_attr(0, &ao_dev_attr)) {
    printf("kd_mpi_ao_set_pub_attr failed\n");
    return K_FAILED;
}

if (K_SUCCESS != kd_mpi_ao_enable(0)) {
    printf("kd_mpi_ao_enable failed\n");
    return K_FAILED;
}

if (K_SUCCESS != kd_mpi_ao_enable_chn(0, 1)) {
    printf("kd_mpi_ao_enable_chn failed\n");
    return K_FAILED;
}
```

### 2.2.2 kd_mpi_ao_get_pub_attr

**Description**:

Get AO device attributes.

**Syntax**:

```c
k_s32 kd_mpi_ao_get_pub_attr([k_audio_dev](#312-k_audio_dev) ao_dev, [k_aio_dev_attr](#3112-k_aio_dev_attr) *attr);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |
| attr      | AO device attribute pointer. | Output       |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

### 2.2.3 kd_mpi_ao_enable

**Description**:

Enable AO device.

**Syntax**:

```c
k_s32 kd_mpi_ao_enable([k_audio_dev](#312-k_audio_dev) ao_dev);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

### 2.2.4 kd_mpi_ao_disable

**Description**:

Disable AO device.

**Syntax**:

```c
k_s32 kd_mpi_ao_disable([k_audio_dev](#312-k_audio_dev) ao_dev);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

### 2.2.5 kd_mpi_ao_enable_chn

**Description**:

Enable AO channel.

**Syntax**:

```c
k_s32 kd_mpi_ao_enable_chn([k_audio_dev](#312-k_audio_dev) ao_dev, [k_ao_chn](#314-k_ao_chn) ao_chn);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |
| ao_chn    | Audio channel number. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a
| Input      |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.6 kd_mpi_ao_disable_chn

**Description**:

Disable AO channel.

**Syntax**:

```c
k_s32 kd_mpi_ao_disable_chn([k_audio_dev](#312-k_audio_dev) ao_dev, [k_ao_chn](#314-k_ao_chn) ao_chn);
```

**Parameters**:

| Parameter | Description          | Input/Output |
|-----------|----------------------|--------------|
| ao_dev    | Audio device number. | Input        |
| ao_chn    | Audio channel number.| Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ao_api.h
- Library file: libao.a

#### 2.2.7 kd_mpi_ao_send_frame

**Description**:

Send AO frame data.

**Syntax**:

```c
k_s32 kd_mpi_ao_send_frame([k_audio_dev](#312-k_audio_dev) ao_dev, [k_ao_chn](#314-k_ao_chn) ao_chn, const [k_audio_frame](#3114-k_audio_frame) *frame, k_s32 milli_sec);
```

**Parameters**:

| Parameter  | Description                                                                                      | Input/Output |
|------------|--------------------------------------------------------------------------------------------------|--------------|
| ao_dev     | Audio device number.                                                                             | Input        |
| ao_chn     | Audio channel number.                                                                            | Input        |
| frame      | Pointer to audio frame data.                                                                     | Input        |
| milli_sec  | Timeout for sending data. -1 means blocking mode, waiting indefinitely if no data; 0 means non-blocking mode, returning an error if no data; >0 means blocking for milli_sec milliseconds, returning an error if timeout. | Input        |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_ai_api.h
- Library file: libai.a

**Notes**:

- The value of milli_sec must be greater than or equal to -1. When it is -1, data is sent in blocking mode. When it is 0, data is sent in non-blocking mode. When it is greater than 0, it blocks for milli_sec milliseconds, and if there is no data, it returns a timeout error.
- The corresponding AO channel must be enabled before sending audio frame data.

**Example**:

```c
k_audio_frame audio_frame;
k_s32 ret = 0;
while (true) {
    // get ai frame
    ret = kd_mpi_ai_get_frame(0, 0, &audio_frame, 1000);
    if (K_SUCCESS != ret) {
        printf("=========kd_mpi_ai_get_frame timeout\n");
        continue;
    }
    // send ai frame to ao
    ret = kd_mpi_ao_send_frame(0, 1, &audio_frame, 0);
    if (K_SUCCESS != ret) {
        printf("=======kd_mpi_ao_send_frame failed\n");
    }
    // release ai frame
    kd_mpi_ai_release_frame(0, 0, &audio_frame);
}
```

### 2.3 Audio Encoding

Audio encoding primarily implements creating encoding channels, sending audio frames for encoding, and retrieving encoded streams.

The audio encoding section provides G711a/u encoding, currently only supporting 16-bit sampling precision.

This functional module provides the following APIs:

- [kd_mpi_aenc_register_encoder](#231-kd_mpi_aenc_register_encoder): Register encoder.
- [kd_mpi_aenc_unregister_encoder](#232-kd_mpi_aenc_unregister_encoder): Unregister encoder.
- [kd_mpi_aenc_create_chn](#233-kd_mpi_aenc_create_chn): Create encoding channel.
- [kd_mpi_aenc_destroy_chn](#234-kd_mpi_aenc_destroy_chn): Destroy encoding channel.
- [kd_mpi_aenc_send_frame](#235-kd_mpi_aenc_send_frame): Send audio frame for encoding.
- [kd_mpi_aenc_get_stream](#236-kd_mpi_aenc_get_stream): Get encoded audio stream.
- [kd_mpi_aenc_release_stream](#237-kd_mpi_aenc_release_stream): Release encoded audio stream.

#### 2.3.1 kd_mpi_aenc_register_encoder

**Description**:

Register encoder.

**Syntax**:

```c
k_s32 kd_mpi_aenc_register_encoder(k_s32 *handle, const [k_aenc_encoder](#322-k_aenc_encoder) *encoder);
```

**Parameters**:

| Parameter | Description            | Input/Output |
|-----------|------------------------|--------------|
| handle    | Registration handle.   | Output       |
| encoder   | Encoder attribute structure. | Input  |

**Notes**:

Users register an encoder by passing in the encoder attribute structure to the AENC module and receive a registration handle, which can be used later to unregister the encoder.

The AENC module can register up to 20 encoders, and it already registers G711.a and G711.u encoders.

The same encoding protocol cannot register multiple encoders. For example, if a G711 encoder is already registered, another G711 encoder cannot be registered.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.2 kd_mpi_aenc_unregister_encoder

**Description**:

Unregister encoder.

**Syntax**:

```c
k_s32 kd_mpi_aenc_unregister_encoder(k_s32 handle);
```

**Parameters**:

| Parameter | Description      | Input/Output |
|-----------|------------------|--------------|
| handle    | Unregistration handle. | Input |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.3 kd_mpi_aenc_create_chn

**Description**:

Create audio encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_aenc_create_chn([k_aenc_chn](#326-k_aenc_chn) aenc_chn, const [k_aenc_chn_attr](#323-k_aenc_chn_attr) *attr);
```

**Parameters**:

| Parameter | Description                                                                  | Input/Output |
|-----------|------------------------------------------------------------------------------|--------------|
| aenc_chn  | Channel number. Range: [0, [AENC_MAX_CHN_NUM](#324-aenc_max_chn_nums)).      | Input        |
| attr      | Pointer to audio encoding channel attributes.                                | Input        |

**Notes**:

Buffer size is in frames, ranging from [2, [K_MAX_AUDIO_FRAME_NUM](#315-k_max_audio_frame_num)], recommended to be configured above 10. Small buffer configurations may result in frame loss and other anomalies. Each encoding channel configures queue size based on buffer size to cache encoded frame data.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.4 kd_mpi_aenc_destroy_chn

**Description**:

Destroy audio encoding channel.

**Syntax**:

```c
k_s32 kd_mpi_aenc_destroy_chn([k_aenc_chn](#326-k_aenc_chn) aenc_chn);
```

**Parameters**:

| Parameter | Description                                                                  | Input/Output |
|-----------|------------------------------------------------------------------------------|--------------|
| aenc_chn  | Channel number. Range: [0, [AENC_MAX_CHN_NUM](#324-aenc_max_chn_nums)).      | Input        |

**Notes**:

None

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.5 kd_mpi_aenc_send_frame

**Description**:

Send audio frame for encoding.

**Syntax**:

```c
k_s32 kd_mpi_aenc_send_frame([k_aenc_chn](#326-k_aenc_chn) aenc_chn, const [k_audio_frame](#3114-k_audio_frame) *frame);
```

**Parameters**:

| Parameter | Description                                          | Input/Output |
|-----------|------------------------------------------------------|--------------|
| aenc_chn  | Channel number. Range: [0, AENC_MAX_CHN_NUM).        | Input        |
| frame     | Pointer to audio frame structure.                    | Input        |

**Notes**:

Sending encoded audio frames is a non-blocking interface. If the audio stream buffer is full, it returns failure. This interface is used for users to actively send audio frames for encoding. If the AENC channel is already bound to AI through the system binding interface, it is not necessary and not recommended to call this interface. When calling this interface to send audio frames, the corresponding encoding channel must be created first.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.6 kd_mpi_aenc_get_stream

**Description**:

Get encoded audio stream.

**Syntax**:

```c
k_s32 kd_mpi_aenc_get_stream([k_aenc_chn](#326-k_aenc_chn) aenc_chn, [k_audio_stream](#327-k_audio_stream) *stream, k_s32 milli_sec);
```

**Parameters**:

| Parameter  | Description                                                                                      | Input/Output |
|------------|--------------------------------------------------------------------------------------------------|--------------|
| aenc_chn   | Channel number. Range: [0, AENC_MAX_CHN_NUM).                                                    | Input        |
| stream     | Pointer to the retrieved audio stream.                                                           | Output       |
| milli_sec  | Timeout for getting data. -1 means blocking mode, waiting indefinitely if no data; 0 means non-blocking mode, returning an error if no data; >0 means blocking for milli_sec milliseconds, returning an error if timeout. | Input        |

**Notes**:

The channel must be created before retrieving streams, otherwise it directly returns failure. If the channel is destroyed during the process of retrieving streams, it immediately returns failure.

The value of milli_sec must be greater than or equal to -1. When it is -1, data is retrieved in blocking mode. When it is 0, data is retrieved in non-blocking mode. When it is greater than 0, it blocks for milli_sec milliseconds, and if there is no data, it returns a timeout error.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

#### 2.3.7 kd_mpi_aenc_release_stream

**Description**:

Release encoded audio stream.

**Syntax**:

```c
k_s32 kd_mpi_aenc_release_stream([k_aenc_chn](#326-k_aenc_chn) aenc_chn, const [k_audio_stream](#327-k_audio_stream) *stream);
```

**Parameters**:

| Parameter | Description                                                                  | Input/Output |
|-----------|------------------------------------------------------------------------------|--------------|
| aenc_chn  | Channel number. Range: [0, AENC_MAX_CHN_NUM).                                | Input        |
| stream    | Pointer to the retrieved audio stream.                                       | Output       |

**Notes**:

None

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_aenc_api.h
- Library file: libaenc.a

### 2.4 Audio Decoding

Audio decoding primarily implements creating decoding channels, sending audio streams for decoding, and retrieving decoded audio frames.

The audio encoding and decoding section provides G711a/u decoding, currently supporting 16-bit sampling precision.

This functional module provides the following APIs:

- [kd_mpi_adec_register_decoder](#241-kd_mpi_adec_register_decoder): Register decoder.
- [kd_mpi_adec_unregister_decoder](#242-kd_mpi_adec_unregister_decoder): Unregister decoder.
- [kd_mpi_adec_create_chn](#243-kd_mpi_adec_create_chn): Create audio decoding channel.
- [kd_mpi_adec_destroy_chn](#244-kd_mpi_adec_destroy_chn): Destroy audio decoding channel.
- [kd_mpi_adec_send_stream](#245-kd_mpi_adec_send_stream): Send audio stream to audio decoding channel.
- [kd_mpi_adec_clr_chn_buf](#246-kd_mpi_adec_clr_chn_buf): Clear current audio data buffer in ADEC channel.
- [kd_mpi_adec_get_frame](#247-kd_mpi_adec_get_frame): Retrieve decoded audio frame.
- [kd_mpi_adec_release_frame](#248-kd_mpi_adec_release_frame): Release decoded audio frame.

#### 2.4.1 kd_mpi_adec_register_decoder

**Description**:

Register decoder.

**Syntax**:

```c
k_s32 kd_mpi_adec_register_decoder(k_s32 *handle, const [k_adec_decoder](#329-k_adec_decoder) *decoder);
```

**Parameters**:

| **Parameter** | **Description**           | **Input/Output** |
|---------------|---------------------------|------------------|
| handle        | Registration handle.      | Output           |
| decoder       | Decoder attribute struct. | Input            |

**Notes**:

Users register a decoder to the ADEC module by passing in the decoder attribute structure and receive a registration handle, which can be used later to unregister the decoder. The ADEC module can register up to 20 decoders, and it already registers G711a and G711u decoders. The same decoding protocol cannot register multiple decoders. For example, if a G711 decoder is already registered, another G711 decoder cannot be registered.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.2 kd_mpi_adec_unregister_decoder

**Description**:

Unregister decoder.

**Syntax**:

```c
k_s32 kd_mpi_adec_unregister_decoder(k_s32 handle);
```

**Parameters**:

| **Parameter** | **Description**      | **Input/Output** |
|---------------|----------------------|------------------|
| handle        | Unregistration handle.| Input            |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.3 kd_mpi_adec_create_chn

**Description**:

Create audio decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_adec_create_chn([k_adec_chn](#3212-k_adec_chn) adec_chn, const [k_adec_chn_attr](#328-k_adec_chn_attr) *attr);
```

**Parameters**:

| **Parameter** | **Description**                                                            | **Input/Output** |
|---------------|---------------------------------------------------------------------------|------------------|
| adec_chn      | Channel number. Range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).   | Input            |
| attr          | Pointer to channel attributes.                                            | Input            |

**Notes**:

The protocol type specifies the decoding protocol for the channel, currently supporting G711. Some attributes of audio decoding need to match the output device attributes, such as sampling rate, frame length (number of samples per frame), etc. Buffer size is in frames, ranging from [2, [K_MAX_AUDIO_FRAME_NUM](#315-k_max_audio_frame_num)], recommended to be configured above 10. Small buffer configurations may result in frame loss and other anomalies. This interface can only be used before the channel is created (or after it is destroyed). If the channel has already been created, it returns that the channel is already created.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.4 kd_mpi_adec_destroy_chn

**Description**:

Destroy audio decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_adec_destroy_chn([k_adec_chn](#3212-k_adec_chn) adec_chn);
```

**Parameters**:

| **Parameter** | **Description**                                                            | **Input/Output** |
|---------------|---------------------------------------------------------------------------|------------------|
| adec_chn      | Channel number. Range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).   | Input            |

**Notes**:

None

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.5 kd_mpi_adec_send_stream

**Description**:

Send audio stream to audio decoding channel.

**Syntax**:

```c
k_s32 kd_mpi_adec_send_stream(k_adec_chn adec_chn, const k_audio_stream *stream, k_bool block);
```

**Parameters**:

| **Parameter** | **Description**:                                                            | **Input/Output** |
|---------------|---------------------------------------------------------------------------|------------------|
| adec_chn      | Channel number. Range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).   | Input            |
| stream        | Audio stream.                                                             | Input            |
| block         | Blocking flag. HI_TRUE: Blocking. HI_FALSE: Non-blocking.                 | Input            |

**Notes**:

When sending data, the channel must already be created; otherwise, it directly returns failure. If the channel is destroyed during the data sending process, it immediately returns failure. Supports sending streams in blocking or non-blocking mode. When sending streams in blocking mode, if the buffer used to cache the decoded audio frames is full, this interface call will be blocked until the decoded audio frame data is taken away or the ADEC channel is destroyed.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.6 kd_mpi_adec_clr_chn_buf

**Description**:

Clear current audio data buffer in ADEC channel.

**Syntax**:

```c
k_s32 kd_mpi_adec_clr_chn_buf([k_adec_chn](#3212-k_adec_chn) adec_chn);
```

**Parameters**:

| **Parameter** | **Description**                                                            | **Input/Output** |
|---------------|---------------------------------------------------------------------------|------------------|
| adec_chn      | Channel number. Range: [0, [ADEC_MAX_CHN_NUM](#3211-adec_max_chn_nums)).   | Input            |

**Notes**:

The decoding channel must be created; otherwise, it returns a channel does not exist error code.

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.7 kd_mpi_adec_get_frame

**Description**:

Retrieve decoded audio frame.

**Syntax**:

```c
k_s32 kd_mpi_adec_get_frame([k_adec_chn](#3212-k_adec_chn) adec_chn, [k_audio_frame](#3114-k_audio_frame) *frame, k_s32 milli_sec);
```

**Parameters**:

| **Parameter** | **Description**                 | **Input/Output** |
|---------------|---------------------------------|------------------|
| adec_chn      | Audio decoding channel.         | Input            |
| frame_info    | Audio frame data structure.     | Output           |
| block         | Blocking flag for retrieval.    | Input            |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

#### 2.4.8 kd_mpi_adec_release_frame

**Description**:

Release the retrieved audio decoding frame data.

**Syntax**:

```c
k_s32 kd_mpi_adec_release_frame([k_adec_chn](#326-k_aenc_chn) adec_chn, const [k_audio_frame](#3114-k_audio_frame) *frame);
```

**Parameters**:

| **Parameter** | **Description**                 | **Input/Output** |
|---------------|---------------------------------|------------------|
| adec_chn      | Audio decoding channel.         | Input            |
| frame_info    | Audio frame data structure.     | Input            |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: mpi_adec_api.h
- Library file: libadec.a

### 2.5 Built-in Audio Codec

The built-in Audio Codec primarily provides operations on hardware devices through ioctl. Among the provided ioctl commands, some commands can be used with the default values set during module loading. The ioctl call implements reading and writing to the built-in Audio Codec registers.

The current version of audio codec control operations mainly includes: ADC digital and analog volume, DAC digital/analog volume, ADC/DAC mute control. Sampling rate, sampling precision, and I2S alignment mode control operations are automatically completed by the kernel through the AI and AO API interfaces (the kernel code automatically implements the operation of the codec hardware device), and ioctl interfaces are no longer provided for control.

Standard function commands for the built-in Audio Codec:

- [k_acodec_set_gain_micl](#251-k_acodec_set_gain_micl): Left channel input analog gain control
- [k_acodec_set_gain_micr](#252-k_acodec_set_gain_micr): Right channel input analog gain control
- [k_acodec_set_adcl_volume](#253-k_acodec_set_adcl_volume): Left channel input digital volume control
- [k_acodec_set_adcr_volume](#254-k_acodec_set_adcr_volume): Right channel input digital volume control
- [k_acodec_set_alc_gain_micl](#255-k_acodec_set_alc_gain_micl): ALC left channel input analog gain control
- [k_acodec_set_alc_gain_micr](#256-k_acodec_set_alc_gain_micr): ALC right channel input analog gain control
- [k_acodec_set_gain_hpoutl](#257-k_acodec_set_gain_hpoutl): Left channel output analog volume control
- [k_acodec_set_gain_hpoutr](#258-k_acodec_set_gain_hpoutr): Right channel output analog volume control
- [k_acodec_set_dacl_volume](#259-k_acodec_set_dacl_volume): Left channel output digital volume control
- [k_acodec_set_dacr_volume](#2510-k_acodec_set_dacr_volume): Right channel output digital volume control
- [k_acodec_set_micl_mute](#2511-k_acodec_set_micl_mute): Left channel input mute control
- [k_acodec_set_micr_mute](#2512-k_acodec_set_micr_mute): Right channel input mute control
- [k_acodec_set_dacl_mute](#2513-k_acodec_set_dacl_mute): Left channel output mute control
- [k_acodec_set_dacr_mute](#2514-k_acodec_set_dacr_mute): Right channel output mute control
- [k_acodec_get_gain_micl](#2515-k_acodec_get_gain_micl): Get left channel input analog gain value
- [k_acodec_get_gain_micr](#2516-k_acodec_get_gain_micr): Get right channel input analog gain value
- [k_acodec_get_adcl_volume](#2518-k_acodec_get_adcl_volume): Get left channel input digital volume value
- [k_acodec_get_adcr_volume](#2519-k_acodec_get_adcr_volume): Get right channel input digital volume value
- [k_acodec_get_alc_gain_micl](#255-k_acodec_get_alc_gain_micl): Get ALC left channel input analog gain value
- [k_acodec_get_alc_gain_micr](#256-k_acodec_get_alc_gain_micr): Get ALC right channel input analog gain value
- [k_acodec_get_gain_hpoutl](#257-k_acodec_get_gain_hpoutl): Get left channel output analog volume value
- [k_acodec_get_gain_hpoutr](#258-k_acodec_get_gain_hpoutr): Get right channel output analog volume value
- [k_acodec_get_dacl_volume](#259-k_acodec_get_dacl_volume): Get left channel output digital volume value
- [k_acodec_get_dacr_volume](#2510-k_acodec_get_dacr_volume): Get right channel output digital volume value
- [k_acodec_reset](#2510-k_acodec_reset): Volume reset

#### 2.5.1 k_acodec_set_gain_micl

**Description**:

Left channel input analog gain control

**Syntax**:

```c
int ioctl (int fd, k_acodec_set_gain_micl, k_u32 *arg);
```

**Parameters**:

| **Parameter**           | **Description**                  | **Input/Output** |
|-------------------------|----------------------------------|------------------|
| fd                      | Audio Codec device file descriptor | Input          |
| k_acodec_set_gain_micl  | ioctl number                     | Input            |
| arg                     | Unsigned integer pointer         | Input            |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

- Header file: k_acodec_comm.h
- Library file: libacodec.a

**Notes**:

The analog gain range is 0db, 6db, 20db, 30db.

#### 2.5.2 k_acodec_set_gain_micr

- **Description**:

Right channel input analog gain control

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_gain_micr, k_u32 *arg);
```

- **Parameters**:

| **Parameter Name**      | **Description**                  | **Input/Output** |
|-------------------------|----------------------------------|------------------|
| fd                      | Audio Codec device file descriptor | Input          |
| k_acodec_set_gain_micr  | ioctl number                     | Input            |
| arg                     | Unsigned integer pointer         | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range is 0db, 6db, 20db, 30db.

#### 2.5.3 k_acodec_set_adcl_volume

- **Description**:

Left channel input digital gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_adcl_volume, float *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_adcl_volume     | ioctl number                     | Input            |
| arg                          | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The digital gain range is `[-97, 30]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.4 k_acodec_set_adcr_volume

- **Description**:

Right channel input digital gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_adcr_volume, float *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_adcr_volume     | ioctl number                     | Input            |
| arg                          | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The digital gain range is `[-97, 30]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.5 k_acodec_set_alc_gain_micl

- **Description**:

Left channel ALC input analog gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_alc_gain_micl, float *arg);
```

- **Parameters**:

| **Parameter Name**               | **Description**                  | **Input/Output** |
|----------------------------------|----------------------------------|------------------|
| fd                               | Audio Codec device file descriptor | Input          |
| k_acodec_set_alc_gain_micl       | ioctl number                     | Input            |
| arg                              | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range is `[-18, 28.5]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.6 k_acodec_set_alc_gain_micr

- **Description**:

Right channel ALC input analog gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_alc_gain_micr, float *arg);
```

- **Parameters**:

| **Parameter Name**               | **Description**                  | **Input/Output** |
|----------------------------------|----------------------------------|------------------|
| fd                               | Audio Codec device file descriptor | Input          |
| k_acodec_set_alc_gain_micr       | ioctl number                     | Input            |
| arg                              | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range is `[-18, 28.5]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.7 k_acodec_set_gain_hpoutl

- **Description**:

Left channel output analog gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_gain_hpoutl, float *arg);
```

- **Parameters**:

| **Parameter Name**             | **Description**                  | **Input/Output** |
|--------------------------------|----------------------------------|------------------|
| fd                             | Audio Codec device file descriptor | Input          |
| k_acodec_set_gain_hpoutl       | ioctl number                     | Input            |
| arg                            | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range is `[-39, 6]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.8 k_acodec_set_gain_hpoutr

- **Description**:

Right channel output analog gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_gain_hpoutr, float *arg);
```

- **Parameters**:

| **Parameter Name**             | **Description**                  | **Input/Output** |
|--------------------------------|----------------------------------|------------------|
| fd                             | Audio Codec device file descriptor | Input          |
| k_acodec_set_gain_hpoutr       | ioctl number                     | Input            |
| arg                            | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range is `[-39, 6]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.9 k_acodec_set_dacl_volume

- **Description**:

Left channel output digital gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_dacl_volume, float *arg);
```

- **Parameters**:

| **Parameter Name**             | **Description**                  | **Input/Output** |
|--------------------------------|----------------------------------|------------------|
| fd                             | Audio Codec device file descriptor | Input          |
| k_acodec_set_dacl_volume       | ioctl number                     | Input            |
| arg                            | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The digital gain range is `[-120, 7]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.10 k_acodec_set_dacr_volume

- **Description**:

Right channel output digital gain control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_dacr_volume, float *arg);
```

- **Parameters**:

| **Parameter Name**             | **Description**                  | **Input/Output** |
|--------------------------------|----------------------------------|------------------|
| fd                             | Audio Codec device file descriptor | Input          |
| k_acodec_set_dacr_volume       | ioctl number                     | Input            |
| arg                            | Signed float pointer             | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The digital gain range is `[-120, 7]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.11 k_acodec_set_micl_mute

- **Description**:

Left channel input mute control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_micl_mute, k_bool *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_micl_mute       | ioctl number                     | Input            |
| arg                          | Bool pointer                     | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

Value range: K_TRUE for mute, K_FALSE to unmute.

#### 2.5.12 k_acodec_set_micr_mute

- **Description**:

Right channel input mute control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_micr_mute, k_bool *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_micr_mute       | ioctl number                     | Input            |
| arg                          | Bool pointer                     | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

Value range: K_TRUE for mute, K_FALSE to unmute.

#### 2.5.13 k_acodec_set_dacl_mute

- **Description**:

Left channel output mute control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_dacl_mute, k_bool *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_dacl_mute       | ioctl number                     | Input            |
| arg                          | Bool pointer                     | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

Value range: K_TRUE for mute, K_FALSE to unmute.

#### 2.5.14 k_acodec_set_dacr_mute

- **Description**:

Right channel output mute control.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_set_dacr_mute, k_bool *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_set_dacr_mute       | ioctl number                     | Input            |
| arg                          | Bool pointer                     | Input            |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

Value range: K_TRUE for mute, K_FALSE to unmute.

#### 2.5.15 k_acodec_get_gain_micl

- **Description**:

Get left channel input analog gain value.

- **Syntax**:

```c
int ioctl (int fd, k_acodec_get_gain_micl, k_u32 *arg);
```

- **Parameters**:

| **Parameter Name**           | **Description**                  | **Input/Output** |
|------------------------------|----------------------------------|------------------|
| fd                           | Audio Codec device file descriptor | Input          |
| k_acodec_get_gain_micl       | ioctl number                     | Input            |
| arg                          | Unsigned integer pointer         | Output           |

- **Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

- **Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

- **Notes**:

The analog gain range obtained is 0db, 6db, 20db, 30db.

#### 2.5.16 k_acodec_get_gain_micr

- **Description**:

Get right channel input analog gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_gain_micr, k_u32 *arg);
```

**Parameters**:

| **Parameter Name**      | **Description**                      | **Input/Output** |
|-------------------------|--------------------------------------|------------------|
| fd                      | Audio Codec device file descriptor   | Input            |
| k_acodec_get_gain_micr  | ioctl number                         | Input            |
| arg                     | Unsigned integer pointer             | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The analog gain range obtained is 0db, 6db, 20db, 30db.

#### 2.5.18 k_acodec_get_adcl_volume

**Description**:

Get left channel input digital volume value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_adcl_volume, float *arg);
```

**Parameters**:

| **Parameter Name**           | **Description**                      | **Input/Output** |
|------------------------------|--------------------------------------|------------------|
| fd                           | Audio Codec device file descriptor   | Input            |
| k_acodec_get_adcl_volume     | ioctl number                         | Input            |
| arg                          | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The digital gain range is `[-97, 30]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.19 k_acodec_get_adcr_volume

**Description**:

Get right channel input digital gain control value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_adcr_volume, float *arg);
```

**Parameters**:

| **Parameter Name**           | **Description**                      | **Input/Output** |
|------------------------------|--------------------------------------|------------------|
| fd                           | Audio Codec device file descriptor   | Input            |
| k_acodec_get_adcr_volume     | ioctl number                         | Input            |
| arg                          | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The digital gain range is `[-97, 30]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.5 k_acodec_get_alc_gain_micl

**Description**:

Get left channel ALC input analog gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_alc_gain_micl, float *arg);
```

**Parameters**:

| **Parameter Name**               | **Description**                      | **Input/Output** |
|----------------------------------|--------------------------------------|------------------|
| fd                               | Audio Codec device file descriptor   | Input            |
| k_acodec_get_alc_gain_micl       | ioctl number                         | Input            |
| arg                              | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The analog gain range is `[-18, 28.5]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.6 k_acodec_get_alc_gain_micr

**Description**:

Get right channel ALC input analog gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_alc_gain_micr, float *arg);
```

**Parameters**:

| **Parameter Name**               | **Description**                      | **Input/Output** |
|----------------------------------|--------------------------------------|------------------|
| fd                               | Audio Codec device file descriptor   | Input            |
| k_acodec_get_alc_gain_micr       | ioctl number                         | Input            |
| arg                              | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The analog gain range is `[-18, 28.5]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.7 k_acodec_get_gain_hpoutl

**Description**:

Get left channel output analog gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_gain_hpoutl, float *arg);
```

**Parameters**:

| **Parameter Name**             | **Description**                      | **Input/Output** |
|--------------------------------|--------------------------------------|------------------|
| fd                             | Audio Codec device file descriptor   | Input            |
| k_acodec_get_gain_hpoutl       | ioctl number                         | Input            |
| arg                            | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The analog gain range is `[-39, 6]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.8 k_acodec_get_gain_hpoutr

**Description**:

Get right channel output analog gain control.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_gain_hpoutr, float *arg);
```

**Parameters**:

| **Parameter Name**             | **Description**                      | **Input/Output** |
|--------------------------------|--------------------------------------|------------------|
| fd                             | Audio Codec device file descriptor   | Input            |
| k_acodec_get_gain_hpoutr       | ioctl number                         | Input            |
| arg                            | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The analog gain range is `[-39, 6]`, the larger the value, the higher the volume, incremented by 1.5db.

#### 2.5.9 k_acodec_get_dacl_volume

**Description**:

Get left channel output digital gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_dacl_volume, float *arg);
```

**Parameters**:

| **Parameter Name**             | **Description**                      | **Input/Output** |
|--------------------------------|--------------------------------------|------------------|
| fd                             | Audio Codec device file descriptor   | Input            |
| k_acodec_get_dacl_volume       | ioctl number                         | Input            |
| arg                            | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The digital gain range is `[-120, 7]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.10 k_acodec_get_dacr_volume

**Description**:

Get right channel output digital gain value.

**Syntax**:

```c
int ioctl (int fd, k_acodec_get_dacr_volume, float *arg);
```

**Parameters**:

| **Parameter Name**             | **Description**                      | **Input/Output** |
|--------------------------------|--------------------------------------|------------------|
| fd                             | Audio Codec device file descriptor   | Input            |
| k_acodec_get_dacr_volume       | ioctl number                         | Input            |
| arg                            | Signed float pointer                 | Output           |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

The digital gain range is `[-120, 7]`, the larger the value, the higher the volume, incremented by 0.5db.

#### 2.5.10 k_acodec_reset

**Description**:

Volume reset: including ADC, DAC, ALC digital and analog gain.

**Syntax**:

```c
int ioctl (int fd, k_acodec_reset, ...);
```

**Parameters**:

| **Parameter Name**   | **Description**                      | **Input/Output** |
|----------------------|--------------------------------------|------------------|
| fd                   | Audio Codec device file descriptor   | Input            |
| k_acodec_reset       | ioctl number                         | Input            |

**Return Value**:

| Return Value | Description                 |
|--------------|-----------------------------|
| 0            | Success                     |
| Non-zero     | Failure, see error code     |

**Requirements**:

Header file: k_acodec_comm.h

Library file: libacodec.a

**Notes**:

None

### 2.6 Audio Encoding MAPI

The audio encoding function module provides the following MAPI:

- [kd_mapi_aenc_init](#261-kd_mapi_aenc_init): Initialize encoding channel
- [kd_mapi_aenc_deinit](#262-kd_mapi_aenc_deinit): Deinitialize encoding channel
- [kd_mapi_aenc_start](#263-kd_mapi_aenc_start): Start encoding channel
- [kd_mapi_aenc_stop](#264-kd_mapi_aenc_stop): Stop encoding channel
- [kd_mapi_aenc_registercallback](#265-kd_mapi_aenc_registercallback): Register encoding callback function
- [kd_mapi_aenc_unregistercallback](#266-kd_mapi_aenc_unregistercallback): Unregister encoding callback function
- [kd_mapi_aenc_bind_ai](#267-kd_mapi_aenc_bind_ai): Bind AI
- [kd_mapi_aenc_unbind_ai](#268-kd_mapi_aenc_unbind_ai): Unbind AI
- [kd_mapi_register_ext_audio_encoder](#269-kd_mapi_register_ext_audio_encoder): Register external audio encoder
- [kd_mapi_unregister_ext_audio_encoder](#2610-kd_mapi_unregister_ext_audio_encoder): Unregister external audio encoder
- [kd_mapi_aenc_send_frame](#2611-kd_mapi_aenc_send_frame): Send audio encoding frame

#### 2.6.1 kd_mapi_aenc_init

**Description**:

Initialize encoding channel.

**Syntax**:

```c
kd_mapi_aenc_init([k_handle](#331-k_handle) aenc_hdl, const [k_aenc_chn_attr](#323-k_aenc_chn_attr) *attr);
```

#### 2.6.2 kd_mapi_aenc_deinit

**Description**:

Deinitialize encoding channel.

**Parameters**:

```c
kd_mapi_aenc_deinit([k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.3 kd_mapi_aenc_start

**Description**:

Start encoding channel.

**Syntax**:

```c
kd_mapi_aenc_start([k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.4 kd_mapi_aenc_stop

**Description**:

Stop encoding channel.

**Syntax**:

```c
kd_mapi_aenc_stop([k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.5 kd_mapi_aenc_registercallback

**Description**:

Register encoding callback function.

**Syntax**:

```c
k_s32 kd_mapi_aenc_registercallback([k_handle](#331-k_handle) aenc_hdl, k_aenc_callback_s *aenc_cb);
```

#### 2.6.6 kd_mapi_aenc_unregistercallback

**Description**:

Unregister encoding callback function.

**Syntax**:

```c
k_s32 kd_mapi_aenc_unregistercallback([k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.7 kd_mapi_aenc_bind_ai

**Description**:

Bind AI.

**Syntax**:

```c
k_s32 kd_mapi_aenc_bind_ai([k_handle](#331-k_handle) ai_hdl, [k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.8 kd_mapi_aenc_unbind_ai

**Description**:

Unbind AI.

**Syntax**:

```c
k_s32 kd_mapi_aenc_unbind_ai([k_handle](#331-k_handle) ai_hdl, [k_handle](#331-k_handle) aenc_hdl);
```

#### 2.6.9 kd_mapi_register_ext_audio_encoder

**Description**:

Register external audio encoder.

**Syntax**:

```c
k_s32 kd_mapi_register_ext_audio_encoder(const [k_aenc_encoder](#322-k_aenc_encoder) *encoder, [k_handle](#331-k_handle) * aencoder_hdl);
```

#### 2.6.10 kd_mapi_unregister_ext_audio_encoder

**Description**:

Unregister external audio encoder.

**Syntax**:

```c
k_s32 kd_mapi_unregister_ext_audio_encoder([k_handle](#331-k_handle) aencoder_hdl);
```

#### 2.6.11 kd_mapi_aenc_send_frame

**Description**:

Send audio encoding frame.

**Syntax**:

```c
k_s32 kd_mapi_aenc_send_frame([k_handle](#331-k_handle) ai_hdl, const [k_audio_frame](#3114-k_audio_frame) *frame);
```

### 2.7 Audio Decoding MAPI

The audio decoding function module provides the following MAPI:

- [kd_mapi_adec_init](#261-kd_mapi_aenc_init): Initialize decoding channel
- [kd_mapi_adec_deinit](#271-kd_mapi_adec_init): Deinitialize decoding channel
- [kd_mapi_adec_start](#273-kd_mapi_adec_start): Start decoding channel.
- [kd_mapi_adec_stop](#274-kd_mapi_adec_stop): Stop decoding channel.
- [kd_mapi_adec_registercallback](#275-kd_mapi_adec_registercallback): Register decoding callback function.
- [kd_mapi_adec_unregistercallback](#276-kd_mapi_adec_unregistercallback): Unregister decoding callback function.
- [kd_mapi_adec_bind_ao](#277-kd_mapi_adec_bind_ao): Bind AO.
- [kd_mapi_adec_unbind_ao](#278-kd_mapi_adec_unbind_ao): Unbind AO.
- [kd_mapi_register_ext_audio_decoder](#279-kd_mapi_register_ext_audio_decoder): Register external audio decoder.
- [kd_mapi_unregister_ext_audio_decoder](#2710-kd_mapi_unregister_ext_audio_decoder): Unregister external audio decoder.
- [kd_mapi_adec_send_stream](#2711-kd_mapi_adec_send_stream): Send audio decoding frame.

#### 2.7.1 kd_mapi_adec_init

- **Description**:

Initialize decoding channel.

- **Syntax**:

```c
kd_mapi_adec_init([k_handle](#331-k_handle) adec_hdl, const [k_adec_chn_attr](#323-k_adec_chn_attr) *attr);
```

#### 2.7.2 kd_mapi_adec_deinit

- **Description**:

Deinitialize decoding channel.

- **Syntax**:

```c
kd_mapi_adec_deinit([k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.3 kd_mapi_adec_start

- **Description**:

Start decoding channel.

- **Syntax**:

```c
kd_mapi_adec_start([k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.4 kd_mapi_adec_stop

- **Description**:

Stop decoding channel.

- **Syntax**:

```c
kd_mapi_adec_stop([k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.5 kd_mapi_adec_registercallback

- **Description**:

Register decoding callback function.

- **Syntax**:

```c
k_s32 kd_mapi_adec_registercallback([k_handle](#331-k_handle) adec_hdl, k_adec_callback_s *adec_cb);
```

#### 2.7.6 kd_mapi_adec_unregistercallback

- **Description**:

Unregister decoding callback function.

- **Syntax**:

```c
k_s32 kd_mapi_adec_unregistercallback([k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.7 kd_mapi_adec_bind_ao

- **Description**:

Bind AO.

- **Syntax**:

```c
k_s32 kd_mapi_adec_bind_ao([k_handle](#331-k_handle) ao_hdl, [k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.8 kd_mapi_adec_unbind_ao

- **Description**:

Unbind AO.

- **Syntax**:

```c
k_s32 kd_mapi_adec_unbind_ao([k_handle](#331-k_handle) ao_hdl, [k_handle](#331-k_handle) adec_hdl);
```

#### 2.7.9 kd_mapi_register_ext_audio_decoder

- **Description**:

Register external audio decoder.

- **Syntax**:

```c
k_s32 kd_mapi_register_ext_audio_decoder(const [k_adec_decoder](#329-k_adec_decoder) *decoder, [k_handle](#331-k_handle) *adecoder_hdl);
```

#### 2.7.10 kd_mapi_unregister_ext_audio_decoder

- **Description**:

Unregister external audio decoder.

- **Syntax**:

```c
k_s32 kd_mapi_unregister_ext_audio_decoder([k_handle](#331-k_handle) adecoder_hdl);
```

#### 2.7.11 kd_mapi_adec_send_stream

- **Description**:

Send audio decoding frame.

- **Syntax**:

```c
k_s32 kd_mapi_adec_send_stream([k_handle](#331-k_handle) ai_hdl, const [k_audio_stream](#327-k_audio_stream) *stream);
```

## 3. Data Types

### 3.1 Audio Input/Output

The data types and structures related to audio input/output are defined as follows:

- [k_audio_type](#311-k_audio_type): Defines audio input/output types.
- [k_audio_dev](#312-k_audio_dev): Defines audio devices.
- [k_ai_chn](#313-k_ai_chn): Defines AI channels.
- [k_ao_chn](#314-k_ao_chn): Defines AO channels.
- [K_MAX_AUDIO_FRAME_NUM](#315-k_max_audio_frame_num): Defines the maximum number of audio decoding buffer frames.
- [k_audio_bit_width](#316-k_audio_bit_width): Defines audio sampling precision.
- [k_audio_snd_mode](#317-k_audio_snd_mode): Defines audio channel modes.
- [k_audio_pdm_oversample](#318-k_audio_pdm_oversample): Defines PDM oversampling.
- [k_aio_dev_attr](#3112-k_aio_dev_attr): Defines the attribute structure of audio input/output devices.
- [k_audio_pdm_attr](#319-k_audio_pdm_attr): Defines PDM audio input attributes.
- [k_i2s_work_mode](#3111-k_i2s_work_mode): Defines I2S working modes.
- [k_audio_i2s_attr](#3110-k_audio_i2s_attr): Defines I2S audio input attributes.
- [k_aio_i2s_type](#3113-k_aio_i2s_type): Defines I2S interfacing device types.
- [k_audio_frame](#3114-k_audio_frame): Defines audio frame structures.
- [k_audio_anr_cfg](#3115-k_audio_anr_cfg): Defines the configuration structure for audio noise reduction.
- [k_audio_agc_cfg](#3116-k_audio_agc_cfg): Defines the configuration structure for audio automatic gain control.
- [k_ai_vqe_cfg](#3117-k_ai_vqe_cfg): Defines the configuration structure for audio input voice quality enhancement.

#### 3.1.1 k_audio_type

- **Description**:

Defines audio input/output types.

- **Definition**:

```c
typedef enum {
    KD_AUDIO_INPUT_TYPE_I2S = 0, // I2S input
    KD_AUDIO_INPUT_TYPE_PDM = 1, // PDM input
    KD_AUDIO_OUTPUT_TYPE_I2S = 2, // I2S output
} k_audio_type;
```

- **Notes**:

Audio input includes I2S and PDM, while audio output only includes I2S.

- **Related Data Types and Interfaces**:

None

#### 3.1.2 k_audio_dev

- **Description**:

Defines audio devices.

- **Definition**:

```c
typedef k_u32 k_audio_dev;
```

- **Notes**:

For the AI module, `k_audio_dev` can be 0 or 1, where 0 is for I2S audio input and 1 is for PDM audio input.

For the AO module, `k_audio_dev` is fixed at 0, which means I2S audio output.

#### 3.1.3 k_ai_chn

- **Description**:

Defines AI audio channels.

- **Definition**:

```c
typedef k_u32 k_ai_chn;
```

- **Notes**:

I2S audio input has 2 channels, with values ranging from `[0, 1]`.

PDM audio input has 4 channels, with values ranging from `[0, 3]`.

#### 3.1.4 k_ao_chn

- **Description**:

Defines AO audio channels.

- **Definition**:

```c
typedef k_u32 k_ao_chn;
```

- **Notes**:

I2S audio output has 2 channels, with values ranging from `[0, 1]`.

#### 3.1.5 K_MAX_AUDIO_FRAME_NUM

- **Description**:

Defines the maximum number of audio decoding buffer frames.

- **Definition**:

```c
#define K_MAX_AUDIO_FRAME_NUM 50
```

#### 3.1.6 k_audio_bit_width

- **Description**:

Defines audio sampling precision.

- **Definition**:

```c
typedef enum {
    KD_AUDIO_BIT_WIDTH_16 = 0, /* 16-bit width */
    KD_AUDIO_BIT_WIDTH_24 = 1, /* 24-bit width */
    KD_AUDIO_BIT_WIDTH_32 = 2, /* 32-bit width */
} k_audio_bit_width;
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.7 k_audio_snd_mode

- **Description**:

Defines audio channel modes.

- **Definition**:

```c
typedef enum {
    KD_AUDIO_SOUND_MODE_MONO = 0, /* Mono */
    KD_AUDIO_SOUND_MODE_STEREO = 1, /* Stereo */
} k_audio_snd_mode;
```

#### 3.1.8 k_audio_pdm_oversample

- **Description**:

Defines PDM oversampling.

- **Definition**:

```c
typedef enum {
    KD_AUDIO_PDM_INPUT_OVERSAMPLE_32 = 0,
    KD_AUDIO_PDM_INPUT_OVERSAMPLE_64,
    KD_AUDIO_PDM_INPUT_OVERSAMPLE_128,
} k_audio_pdm_oversample;
```

#### 3.1.9 k_audio_pdm_attr

- **Description**:

Defines PDM audio input attributes.

- **Definition**:

```c
typedef struct {
    k_u32 chn_cnt; /* Channel number on FS, I2S valid value: 1/2, PDM valid value: 1/2/3/4 */
    k_audio_sample_rate rate;
    k_audio_bit_width width;
    k_audio_snd_mode mode;
    k_audio_pdm_oversample oversample;
    k_u32 frame_num; /* Frame number in buffer [2, K_MAX_AUDIO_FRAME_NUM] */
    k_u32 point_num_per_frame;
} k_audio_pdm_attr;
```

- **Members**:

| Member Name          | Description                                                |
|----------------------|------------------------------------------------------------|
| chn_cnt              | Supported channel count. Supports 1-4 channels, channels must be consecutive. |
| sample_rate          | Sampling rate: supports 8k~192k                             |
| bit_width            | Sampling precision: supports 16/24/32                       |
| snd_mode             | Audio channel mode. Supports mono and stereo.               |
| pdm_oversample       | Oversampling: supports 32, 64, 128 times oversampling.      |
| frame_num            | Buffer frame number `[2, K_MAX_AUDIO_FRAME_NUM]`.           |
| point_num_per_frame  | Number of sampling points per frame.                        |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.10 k_audio_i2s_attr

- **Description**:

Defines I2S audio input attributes.

- **Definition**:

```c
typedef struct {
    k_u32 chn_cnt; /* Channel number on FS, I2S valid value: 1/2, PDM valid value: 1/2/3/4 */
    k_u32 sample_rate; /* Sample rate 8k ~192k */
    k_audio_bit_width bit_width;
    k_audio_snd_mode snd_mode; /* Mono or stereo */
    k_i2s_in_mono_channel mono_channel; /* Use mic input or headphone input */
    k_i2s_work_mode i2s_mode;  /* I2S work mode */
    k_u32 frame_num; /* Frame number in buffer [2, K_MAX_AUDIO_FRAME_NUM] */
    k_u32 point_num_per_frame;
    k_aio_i2s_type type;
} k_audio_i2s_attr;
```

- **Members**:

| Member Name          | Description                                                  |
|----------------------|--------------------------------------------------------------|
| chn_cnt              | Supported channel count. Supports 1-2 channels.              |
| sample_rate          | Sampling rate: supports 8k~192k                              |
| bit_width            | Sampling precision: supports 16/24/32                        |
| snd_mode             | Audio channel mode. Supports mono and stereo.                |
| mono_channel         | Mono channel source selection. 0: mic input, 1: headphone input |
| i2s_mode             | I2S working mode: supports Philips mode, left-justified mode, right-justified mode. |
| frame_num            | Buffer frame number `[2, K_MAX_AUDIO_FRAME_NUM]`.            |
| point_num_per_frame  | Number of sampling points per frame `[sample_rate/100, sample_rate]`. |
| i2s_type             | I2S interfacing device type: internal codec or external device. |

- **Notes**:

The value of `point_num_per_frame` and `sample_rate` determines the interrupt frequency generated by the hardware. A high frequency can affect system performance and other tasks. It is recommended that these parameters satisfy the equation: `(point_num_per_frame * 1000) / sample_rate >= 10` (100 interrupts). For example, at a sampling rate of 16000Hz, it is recommended to set the number of sampling points to be greater than or equal to 160.

- **Related Data Types and Interfaces**:

None

#### 3.1.11 k_i2s_work_mode

- **Description**:

Defines I2S working modes.

- **Definition**:

```c
typedef enum {
    K_STANDARD_MODE = 1,
    K_RIGHT_JUSTIFYING_MODE = 2,
    K_LEFT_JUSTIFYING_MODE = 4,
} k_i2s_work_mode;
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.12 k_aio_dev_attr

- **Description**:

Defines the attribute structure of audio input/output devices.

- **Definition**:

```c
typedef struct {
    k_audio_type type;
    union {
        k_audio_pdm_attr pdm_attr;
        k_audio_i2s_attr i2s_attr;
    } kd_audio_attr;
} k_aio_dev_attr;
```

- **Members**:

| Member Name      | Description         |
|------------------|---------------------|
| audio_type       | Audio type.         |
| kd_audio_attr    | Audio attribute settings. |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.13 k_aio_i2s_type

- **Description**:

Defines I2S interfacing device types.

- **Definition**:

```c
typedef enum {
    K_AIO_I2STYPE_INNERCODEC = 0, /* AIO I2S connect inner audio CODEC */
    K_AIO_I2STYPE_EXTERN, /* AIO I2S connect external hardware */
} k_aio_i2s_type;
```

- **Notes**:

The built-in audio codec uses I2S channel 0, while I2S channel 1 is used for external codecs.

- **Related Data Types and Interfaces**:

None

#### 3.1.14 k_audio_frame

- **Description**:

Defines audio frame structures.

- **Definition**:

```c
typedef struct {
    // Definition of audio frame structure
} k_audio_frame;
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

### 3.1.14 k_audio_frame

- **Description**:

Defines audio frame structures.

- **Definition**:

```c
typedef struct {
    k_audio_bit_width bit_width;
    k_audio_snd_mode snd_mode;
    void* virt_addr;
    k_u64 phys_addr;
    k_u64 time_stamp; /* audio frame time stamp */
    k_u32 seq; /* audio frame seq */
    k_u32 len; /* data length per channel in frame */
    k_u32 pool_id;
} k_audio_frame;
```

- **Members**:

| Member Name | Description                             |
|-------------|-----------------------------------------|
| bit_width   | Sampling precision.                     |
| snd_mode    | Audio channel mode.                     |
| virt_addr   | Virtual address of the audio frame data.|
| phys_addr   | Physical address of the audio frame data.|
| time_stamp  | Audio frame timestamp, in μs.           |
| seq         | Audio frame sequence number.            |
| len         | Audio frame length, in bytes.           |
| pool_id     | Audio frame buffer pool ID.             |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.15 k_audio_anr_cfg

- **Description**:

Defines the configuration structure for audio noise reduction function.

- **Definition**:

```c
typedef struct {
    k_bool anr_switch;
} k_audio_anr_cfg;
```

- **Members**:

| Member Name | Description                  |
|-------------|------------------------------|
| anr_switch  | Audio noise reduction enable.|

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.16 k_audio_agc_cfg

- **Description**:

Defines the configuration structure for audio automatic gain control function.

- **Definition**:

```c
typedef struct {
    k_bool agc_switch;
} k_audio_agc_cfg;
```

- **Members**:

| Member Name | Description                  |
|-------------|------------------------------|
| agc_switch  | Audio automatic gain control enable.|

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.17 k_ai_vqe_cfg

- **Description**:

Defines the configuration structure for audio input voice quality enhancement.

- **Definition**:

```c
typedef struct {
    k_audio_anr_cfg anr_cfg;
    k_audio_agc_cfg agc_cfg;
} k_ai_vqe_cfg;
```

- **Members**:

| Member Name | Description                      |
|-------------|----------------------------------|
| anr_cfg     | Audio noise reduction configuration parameters.|
| agc_cfg     | Audio automatic gain control configuration parameters.|

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.1.18 k_i2s_in_mono_channel

- **Description**:

Defines mono channel source.

- **Definition**:

```c
typedef enum {
    KD_I2S_IN_MONO_RIGHT_CHANNEL = 0,  // mic input
    KD_I2S_IN_MONO_LEFT_CHANNEL = 1,   // hp input
} k_i2s_in_mono_channel;
```

### 3.2 Audio Encoding/Decoding

The data types and structures related to audio encoding/decoding are defined as follows:

- [k_payload_type](#321-k_payload_type)
- [k_aenc_encoder](#322-k_aenc_encoder)
- [k_aenc_chn_attr](#323-k_aenc_chn_attr)
- [AENC_MAX_CHN_NUMS](#324-aenc_max_chn_nums)
- [K_MAX_ENCODER_NAME_LEN](#325-k_max_encoder_name_len)
- [k_aenc_chn](#326-k_aenc_chn)
- [k_audio_stream](#327-k_audio_stream)
- [k_adec_chn_attr](#328-k_adec_chn_attr)
- [k_adec_decoder](#329-k_adec_decoder)
- [K_MAX_DECODER_NAME_LEN](#3210-k_max_decoder_name_len)
- [ADEC_MAX_CHN_NUMS](#3211-adec_max_chn_nums)

#### 3.2.1 k_payload_type

- **Description**:

Defines the enumeration of audio and video payload types.

- **Definition**:

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

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.2 k_aenc_encoder

- **Description**:

Defines the encoder attribute structure.

- **Definition**:

```c
typedef struct {
    k_payload_type type;
    k_u32 max_frame_len;
    k_char name[K_MAX_ENCODER_NAME_LEN];
    k_s32 (*func_open_encoder)(void *encoder_attr, void **encoder);
    k_s32 (*func_enc_frame)(void *encoder, const k_audio_frame *data, k_u8 *outbuf, k_u32 *out_len);
    k_s32 (*func_close_encoder)(void *encoder);
} k_aenc_encoder;
```

- **Members**:

| Member Name          | Description                       |
|----------------------|-----------------------------------|
| type                 | Encoding protocol type.           |
| max_frame_len        | Maximum stream length.            |
| name                 | Encoder name.                     |
| func_open_encoder    | Function pointer to open encoder. |
| func_enc_frame       | Function pointer to encode frame. |
| func_close_encoder   | Function pointer to close encoder.|

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.3 k_aenc_chn_attr

- **Description**:

Defines the encoder channel attribute structure.

- **Definition**:

```c
typedef struct {
    k_payload_type type;
    k_u32 point_num_per_frame;
    k_u32 buf_size; // buffer size [2, K_MAX_AUDIO_FRAME_NUM]
} k_aenc_chn_attr;
```

- **Members**:

| Member Name          | Description                                                                                                    |
|----------------------|---------------------------------------------------------------------------------------------------------------|
| type                 | Audio encoding protocol type.                                                                                  |
| point_num_per_frame  | Frame length corresponding to the audio encoding protocol (encoding can be performed if the received audio frame length is less than or equal to this frame length). |
| buf_size             | Audio encoding buffer size. Range: `[2, K_MAX_AUDIO_FRAME_NUM]`, in frames.                                    |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.4 AENC_MAX_CHN_NUMS

- **Description**:

Defines the maximum number of encoding channels.

- **Definition**:

```c
#define AENC_MAX_CHN_NUMS 4
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.5 K_MAX_ENCODER_NAME_LEN

- **Description**:

Defines the maximum length of the audio encoder name.

- **Definition**:

```c
#define K_MAX_ENCODER_NAME_LEN 25
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.6 k_aenc_chn

- **Description**:

Defines the encoding channel type.

- **Definition**:

```c
typedef k_u32 k_aenc_chn;
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.7 k_audio_stream

- **Description**:

Defines the stream structure.

- **Definition**:

```c
typedef struct {
    void *stream; /* the virtual address of stream */
    k_u64 phys_addr; /* the physical address of stream */
    k_u32 len; /* stream length, in bytes */
    k_u64 time_stamp; /* frame timestamp */
    k_u32 seq; /* frame sequence number, if stream is not a valid frame, seq is 0 */
} k_audio_stream;
```

- **Members**:

| Member Name | Description                            |
|-------------|----------------------------------------|
| stream      | Pointer to the audio stream data.      |
| phys_addr   | Physical address of the audio stream.  |
| len         | Length of the audio stream, in bytes.  |
| time_stamp  | Timestamp of the audio stream.         |
| seq         | Sequence number of the audio stream.   |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.8 k_adec_chn_attr

- **Description**:

Defines the decoder channel attribute structure.

- **Definition**:

```c
typedef struct {
    k_payload_type payload_type;
    k_u32 point_num_per_frame;
    k_u32 buf_size; /* buffer size [2~K_MAX_AUDIO_FRAME_NUM] */
} k_adec_chn_attr;
```

- **Members**:

| Member Name          | Description                                                                                                    |
|----------------------|---------------------------------------------------------------------------------------------------------------|
| payload_type         | Audio decoding protocol type.                                                                                  |
| point_num_per_frame  | Frame length corresponding to the audio decoding protocol.                                                     |
| buf_size             | Audio decoding buffer size. Range: `[2, K_MAX_AUDIO_FRAME_NUM]`, in frames.                                    |

- **Notes**:

Some attributes of audio decoding need to match the attributes of the output device, such as sampling rate, frame length (number of sampling points per frame), etc.

- **Related Data Types and Interfaces**:

None

#### 3.2.9 k_adec_decoder

- **Description**:

Defines the decoder attribute structure.

- **Definition**:

```c
typedef struct {
    k_payload_type payload_type;
    k_char name[K_MAX_DECODER_NAME_LEN];
    k_s32 (*func_open_decoder)(void *decoder_attr, void **decoder);
    k_s32 (*func_dec_frame)(void *decoder, k_u8 **inbuf, k_s32 *left_byte, k_u16 *outbuf, k_u32 *out_len, k_u32 *chns);
    k_s32 (*func_get_frame_info)(void *decoder, void *info);
    k_s32 (*func_close_decoder)(void *decoder);
    k_s32 (*func_reset_decoder)(void *decoder);
} k_adec_decoder;
```

- **Members**:

| Member Name          | Description                                    |
|----------------------|------------------------------------------------|
| payload_type         | Decoding protocol type.                        |
| name                 | Decoder name.                                  |
| func_open_decoder    | Function pointer to open decoder.              |
| func_dec_frame       | Function pointer to decode frame.              |
| func_get_frame_info  | Function pointer to get audio frame information.|
| func_close_decoder   | Function pointer to close decoder.             |
| func_reset_decoder   | Function pointer to reset decoder.             |

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.10 K_MAX_DECODER_NAME_LEN

- **Description**:

Defines the maximum length of the audio decoder name.

- **Definition**:

```c
#define K_MAX_DECODER_NAME_LEN 25
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.11 ADEC_MAX_CHN_NUMS

- **Description**:

Defines the maximum number of decoding channels.

- **Definition**:

```c
#define ADEC_MAX_CHN_NUMS 4
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

#### 3.2.12 k_adec_chn

- **Description**:

Defines the decoding channel type.

- **Definition**:

```c
typedef k_u32 k_adec_chn;
```

- **Notes**:

None

- **Related Data Types and Interfaces**:

None

### 3.3 MAPI

The data types and structures related to audio MAPI are defined as follows:

- [k_handle](#331-k_handle)

#### 3.3.1 k_handle

- **Description**:

Defines the operation handle.

- **Definition**:

```c
typedef k_u32 k_handle;
```

- **Related Data Types and Interfaces**:

None

### 4.1 Audio Input API Error Codes

| Error Code | Macro Definition         | Description                        |
|------------|--------------------------|------------------------------------|
| 0xA0158001 | K_ERR_AI_INVALID_DEVID   | Invalid audio input device number  |
| 0xA0158002 | K_ERR_AI_INVALID_CHNID   | Invalid audio input channel number |
| 0xA0158003 | K_ERR_AI_ILLEGAL_PARAM   | Invalid audio input parameter setting |
| 0xA0158004 | K_ERR_AI_NOT_ENABLED     | Audio input device or channel not enabled |
| 0xA0158005 | K_ERR_AI_NULL_PTR        | Null pointer error in input parameters |
| 0xA0158006 | K_ERR_AI_NOT_CFG         | Audio input device attributes not set |
| 0xA0158007 | K_ERR_AI_NOT_SUPPORT     | Operation not supported            |
| 0xA0158008 | K_ERR_AI_NOT_PERM        | Operation not permitted            |
| 0xA0158009 | K_ERR_AI_NO_MEM          | Failed to allocate memory          |
| 0xA015800A | K_ERR_AI_NO_BUF          | Insufficient audio input buffer    |
| 0xA015800B | K_ERR_AI_BUF_EMPTY       | Audio input buffer is empty        |
| 0xA015800C | K_ERR_AI_BUF_FULL        | Audio input buffer is full         |
| 0xA015800D | K_ERR_AI_NOT_READY       | Audio input system not initialized |
| 0xA015800E | K_ERR_AI_BUSY            | Audio input system is busy         |

### 4.2 Audio Output API Error Codes

| Error Code | Macro Definition          | Description                        |
|------------|---------------------------|------------------------------------|
| 0xA0159001 | K_ERR_AO_INVALID_DEV_ID   | Invalid audio output device number |
| 0xA0159002 | K_ERR_AO_INVALID_CHN_ID   | Invalid audio output channel number |
| 0xA0159003 | K_ERR_AO_ILLEGAL_PARAM    | Invalid audio output parameter setting |
| 0xA0159004 | K_ERR_AO_NOT_ENABLED      | Audio output device or channel not enabled |
| 0xA0159005 | K_ERR_AO_NULL_PTR         | Null pointer error in output       |
| 0xA0159006 | K_ERR_AO_NOT_CFG          | Audio output device attributes not set |
| 0xA0159007 | K_ERR_AO_NOT_SUPPORT      | Operation not supported            |
| 0xA0159008 | K_ERR_AO_NOT_PERM         | Operation not permitted            |
| 0xA0159009 | K_ERR_AO_NO_MEM           | Insufficient system memory         |
| 0xA015900A | K_ERR_AO_NO_BUF           | Insufficient audio output buffer   |
| 0xA015900B | K_ERR_AO_BUF_EMPTY        | Audio output buffer is empty       |
| 0xA015900C | K_ERR_AO_BUF_FULL         | Audio output buffer is full        |
| 0xA015900D | K_ERR_AO_NOT_READY        | Audio output system not initialized |
| 0xA015900E | K_ERR_AO_BUSY             | Audio output system is busy        |
