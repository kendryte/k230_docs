# K230 Multimedia Middleware API Reference

![cover](../../../../zh/01_software/board/middleware/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. ("the Company", hereinafter the same) and its affiliates. All or part of the products, services, or features described in this document may not fall within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for guidance and reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/board/middleware/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document is written for programmers developing with middleware, providing reference information for multimedia middleware, including APIs, header files, etc.

### Target Audience

This document (this guide) is primarily intended for the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
|--------------|-------------|
|              |             |
|              |             |

### Revision History

| Document Version | Author | Date       | Description |
|------------------|--------|------------|-------------|
| V0.1             | Software Department | 2023.07.20 | Initial version |

## Overview

### Overview

The middleware's position in the system is `k230_sdk/src/common/cdk/user/middleware`.

This document describes the relevant parts of the middleware, involving intercom protocol, mixing, MP4 format encapsulation and decapsulation, player, etc.

### Function Description

#### Visual Intercom RTSP Protocol

Referencing the ONVIF RTSP extension, it implements a single-line video visual intercom protocol;

The RTSP server supports sending audio, video, and receiving backchannel audio mediaSubSessions.

The RTSP client supports receiving audio, video, and sending backchannel audio mediaSubSessions.

For related descriptions, see the visual intercom protocol chapter.

#### Player

Implements MP4 file playback. Video supports H264, H265, and audio supports G711a/u.

#### Mixing

Implements two-way G711a/u mixing.

#### MP4 Format Encapsulation and Decapsulation

Implements encapsulation and decapsulation between audio-video and MP4 formats.

## API Reference

### Visual Intercom RTSP Server

KdRtspServer provides the following APIs:

- [Init](#kdrtspserverinit): Initialization.
- [DeInit](#kdrtspserverdeinit): Deinitialization.
- [CreateSession](#kdrtspservercreatesession): Create RTSP session.
- [DestroySession](#kdrtspserverdestroysession): Destroy RTSP session.
- [Start](#kdrtspserverstart): Start RTSP server service.
- [Stop](#kdrtspserverstop): Stop RTSP server service.
- [SendVideoData](#kdrtspserversendvideodata): Write video stream data.
- [SendAudioData](#kdrtspserversendaudiodata): Write audio stream data.

#### KdRtspServer::Init

**Description**:

RTSP server initialization.

**Syntax**:

```cpp
int Init(Port port = 8554, IOnBackChannel *back_channel = nullptr);
```

**Parameters**:

| Parameter Name | Description                  | Input/Output |
|----------------|------------------------------|--------------|
| port           | RTSP service port.           | Input        |
| back_channel   | Callback pointer for audio data from the other end. | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspServer::DeInit

**Description**:

Deinitialization.

**Syntax**:

```cpp
void DeInit();
```

**Parameters**:

None.

**Return Value**:

None.

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Example**:

None.

#### KdRtspServer::CreateSession

**Description**:

Create RTSP session.

**Syntax**:

```cpp
int CreateSession(const std::string &session_name, const SessionAttr &session_attr);
```

**Parameters**:

| Parameter Name | Description     | Input/Output |
|----------------|-----------------|--------------|
| session_name   | Stream URL.     | Input        |
| session_attr   | Session configuration parameters. | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Notes**:

None.

**Example**:

None.

#### KdRtspServer::DestroySession

**Description**:

Destroy RTSP session.

**Syntax**:

```cpp
int DestroySession(const std::string &session_name);
```

**Parameters**:

| Parameter Name | Description     | Input/Output |
|----------------|-----------------|--------------|
| session_name   | Stream URL.     | Input        |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspServer::Start

**Description**:

Start RTSP server service.

**Syntax**:

```cpp
void Start();
```

**Parameters**:

None.

**Return Value**:

None.

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspServer::Stop

**Description**:

Stop RTSP server service.

**Syntax**:

```cpp
void Stop();
```

**Parameters**:

None.

**Return Value**:

None.

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Notes**:

None.

**Example**:

None.

#### KdRtspServer::SendVideoData

**Description**:

Write video stream data.

**Syntax**:

```cpp
int SendVideoData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);
```

**Parameters**:

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| session_name   | Stream URL        | Input        |
| data           | Video stream address. | Input    |
| size           | Video stream size. | Input     |
| timestamp      | Stream timestamp (milliseconds). | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Example**:

None.

#### KdRtspServer::SendAudioData

**Description**:

Write audio stream data.

**Syntax**:

```cpp
int SendAudioData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);
```

**Parameters**:

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| session_name   | Stream URL        | Input        |
| data           | Audio stream address. | Input    |
| size           | Audio stream size. | Input     |
| timestamp      | Stream timestamp (milliseconds). | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_server.h
- Library file:

**Example**:

None.

### Visual Intercom RTSP Client

KdRtspClient module provides the following APIs:

- [Init](#kdrtspclientinit): Initialization.
- [DeInit](#kdrtspclientdeinit): Deinitialization.
- [Open](#kdrtspclientopen): Open and run RTSP client connection.
- [Close](#kdrtspclientclose): Close RTSP client connection.
- [SendAudioData](#kdrtspclientsendaudiodata): Write backchannel audio stream data.

#### KdRtspClient::Init

**Description**:

Initialization.

**Syntax**:

```cpp
int Init(const RtspClientInitParam &param);
```

**Parameters**:

| Parameter Name | Description                  | Input/Output |
|----------------|------------------------------|--------------|
| param          | RTSP client initialization parameters | Input |

```cpp
class IOnAudioData {
public:
    virtual ~IOnAudioData() {}
    virtual void OnAudioData(const uint8_t *data, size_t size, uint64_t timestamp) = 0;
};

class IOnVideoData {
public:
    enum VideoType {VideoTypeInvalid, VideoTypeH264, VideoTypeH265};
    virtual ~IOnVideoData() {}
    virtual void OnVideoType(VideoType type, uint8_t *extra_data, size_t extra_data_size) = 0;
    virtual void OnVideoData(const uint8_t *data, size_t size, uint64_t timestamp, bool keyframe) = 0;
};

class IRtspClientEvent {
public:
    virtual ~IRtspClientEvent() {}
    virtual void OnRtspClientEvent(int event) = 0; // event 0: shutdown
};

struct RtspClientInitParam {
    IOnVideoData *on_video_data{nullptr}; // Callback for video stream frames received from the server
    IOnAudioData *on_audio_data{nullptr}; // Callback for audio stream frames received from the server
    IRtspClientEvent *on_event{nullptr};  // RTSP client event callback
    bool enableBackchannel{false};        // Whether to enable audio backchannel
};
```

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_client.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspClient::Deinit

**Description**:

Deinitialization.

**Syntax**:

```cpp
void DeInit();
```

**Parameters**:

None.

**Return Value**:

None.

**Requirements**:

- Header file: rtsp_client.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspClient::Open

**Description**:

Open and run RTSP client connection.

**Syntax**:

```cpp
int Open(const char *url);
```

**Parameters**:

| Parameter Name | Description  | Input/Output |
|----------------|--------------|--------------|
| url            | RTSP URL.    | Input        |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_client.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspClient::Close

**Description**:

Close RTSP client.

**Syntax**:

```cpp
void Close();
```

**Parameters**:

None.

**Return Value**:

None.

**Requirements**:

- Header file: rtsp_client.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### KdRtspClient::SendAudioData

**Description**:

Write backchannel audio stream data.

**Syntax**:

```cpp
int SendAudioData(const uint8_t *data, size_t size, uint64_t timestamp);
```

**Parameters**:

| Parameter Name | Description            | Input/Output |
|----------------|------------------------|--------------|
| data           | Address of audio stream data | Input   |
| size           | Size of audio stream data | Input    |
| timestamp      | Timestamp of audio stream data (milliseconds) | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: rtsp_client.h
- Library file:

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

### Player Encapsulation

KdPlayer module provides the following APIs:

- [kd_player_init](#kd_player_init): Initialization.
- [kd_player_deinit](#kd_player_deinit): Deinitialization.
- [kd_player_setdatasource](#kd_player_setdatasource): Set media playback file.
- [kd_player_regcallback](#kd_player_regcallback): Register event callback.
- [kd_player_start](#kd_player_start): Start playback.
- [kd_player_stop](#kd_player_stop): Stop playback.

#### kd_player_init

**Description**:

Player initialization.

**Syntax**:

```cpp
k_s32 kd_player_init();
```

**Parameters**:

None.

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_player_deinit

**Description**:

Deinitialization.

**Syntax**:

```cpp
k_s32 kd_player_deinit();
```

**Parameters**:

None.

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_player_setdatasource

**Description**:

Set media playback file.

**Syntax**:

```cpp
k_s32 kd_player_setdatasource(const k_char* filePath);
```

**Parameters**:

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| filePath       | Media file path   | Input        |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_player_regcallback

**Description**:

Register player event callback.

**Syntax**:

```cpp
k_s32 kd_player_regcallback(K_PLAYER_EVENT_FN pfnCallback, void* pData);
```

**Parameters**:

| Parameter Name | Description         | Input/Output |
|----------------|---------------------|--------------|
| pfnCallback    | Callback function pointer | Input |
| pData          | Callback data pointer    | Input |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_player_start

**Description**:

Start playback.

**Syntax**:

```cpp
k_s32 kd_player_start();
```

**Parameters**:

None.

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_player_stop

**Description**:

Stop playback.

**Syntax**:

```cpp
k_s32 kd_player_stop();
```

**Parameters**:

None.

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: kplayer.h
- Library file: libkplayer.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

### Audio Mixing

The mixing module provides the following APIs:

- [kd_mix_g711a_audio](#kd_mix_g711a_audio): g711a mixing.
- [kd_mix_g711u_audio](#kd_mix_g711u_audio): g711u mixing.

#### kd_mix_g711a_audio

**Description**:

g711a mixing.

**Syntax**:

```cpp
k_s32 kd_mix_g711a_audio(k_char *src_data1, k_char *src_data2, k_u32 data_len, k_char *dst_mix_data);
```

**Parameters**:

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| src_data1      | Source data 1     | Input        |
| src_data2      | Source data 2     | Input        |
| data_len       | Length of data    | Input        |
| dst_mix_data   | Mixed result data | Output       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: g711_mix_audio.h
- Library file: libaudio_mix.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

#### kd_mix_g711u_audio

**Description**:

g711u mixing.

**Syntax**:

```cpp
k_s32 kd_mix_g711u_audio(k_char *src_data1, k_char *src_data2, k_u32 data_len, k_char *dst_mix_data);
```

**Parameters**:

| Parameter Name | Description       | Input/Output |
|----------------|-------------------|--------------|
| src_data1      | Source data 1     | Input        |
| src_data2      | Source data 2     | Input        |
| data_len       | Length of data    | Input        |
| dst_mix_data   | Mixed result data | Output       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: g711_mix_audio.h
- Library file: libaudio_mix.a

**Notes**:

None.

**Example**:

None.

**Related Topics**:

None.

### MP4 Format Encapsulation and Decapsulation

The MP4 format encapsulation and decapsulation provide the following APIs:

- [kd_mp4_create](#kd_mp4_create): Create MP4 instance.
- [kd_mp4_destroy](#kd_mp4_destroy): Destroy MP4 instance.
- [kd_mp4_create_track](#kd_mp4_create_track): Create track for MP4.
- [kd_mp4_destroy_tracks](#kd_mp4_destroy_tracks): Destroy all tracks for MP4.
- [kd_mp4_write_frame](#kd_mp4_write_frame): Write frame data to MP4.
- [kd_mp4_get_file_info](#kd_mp4_get_file_info): Get MP4 file information.
- [kd_mp4_get_track_by_index](#kd_mp4_get_track_by_index): Get track information by index.
- [kd_mp4_get_frame](#kd_mp4_get_frame): Get track stream information.

#### kd_mp4_create

**Description**:

Create MP4 instance.

**Syntax**:

```cpp
int kd_mp4_create(KD_HANDLE *mp4_handle, k_mp4_config_s *mp4_cfg);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Output      |
| mp4_cfg        | Configuration parameters | Input  |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

The configuration information in mp4_cfg can specify whether the created MP4 instance is a muxer or demuxer instance.

**Example**:

Refer to samples under mp4_muxer and mp4_demuxer.

**Related Topics**:

None.

#### kd_mp4_destroy

**Description**:

Destroy MP4 instance.

**Syntax**:

```cpp
int kd_mp4_destroy(KD_HANDLE mp4_handle);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

None.

**Example**:

Refer to samples under mp4_muxer and mp4_demuxer.

**Related Topics**:

None.

#### kd_mp4_create_track

**Description**:

Create track for MP4.

**Syntax**:

```cpp
int kd_mp4_create_track(KD_HANDLE mp4_handle, KD_HANDLE *track_handle, k_mp4_track_info_s *mp4_track_info);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |
| track_handle   | Track handle       | Output       |
| mp4_track_info | Track configuration | Input       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for muxer. Use when the created MP4 instance is a muxer instance.
- Currently, each MP4 supports creating up to 3 tracks.

**Example**:

Refer to samples under mp4_muxer.

**Related Topics**:

None.

#### kd_mp4_destroy_tracks

**Description**:

Destroy all tracks for MP4.

**Syntax**:

```cpp
int kd_mp4_destroy_tracks(KD_HANDLE mp4_handle);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for muxer. Use when the created MP4 instance is a muxer instance.
- Call this interface after creating the MP4 instance and tracks.

**Example**:

Refer to samples under mp4_muxer.

**Related Topics**:

None.

#### kd_mp4_write_frame

**Description**:

Write frame data to MP4.

**Syntax**:

```cpp
int kd_mp4_write_frame(KD_HANDLE mp4_handle, KD_HANDLE track_handle, k_mp4_frame_data_s *frame_data);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |
| track_handle   | Track handle       | Input       |
| frame_data     | Frame data information | Input   |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for muxer. Use when the created MP4 instance is a muxer instance.
- Call this interface after creating the MP4 instance and tracks.

**Example**:

Refer to samples under mp4_muxer.

**Related Topics**:

None.

#### kd_mp4_get_file_info

**Description**:

Get MP4 file information.

**Syntax**:

```cpp
int kd_mp4_get_file_info(KD_HANDLE mp4_handle, k_mp4_file_info_s *file_info);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |
| file_info      | MP4 file information | Output     |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for demuxer. Use when the created MP4 instance is a demuxer instance.

**Example**:

Refer to samples under mp4_demuxer.

**Related Topics**:

None.

#### kd_mp4_get_track_by_index

**Description**:

Get track information by index.

**Syntax**:

```cpp
int kd_mp4_get_track_by_index(KD_HANDLE mp4_handle, uint32_t index, k_mp4_track_info_s *mp4_track_info);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |
| index          | Index              | Input        |
| mp4_track_info | Track information  | Output       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for demuxer. Use when the created MP4 instance is a demuxer instance.

**Example**:

Refer to samples under mp4_demuxer.

**Related Topics**:

None.

#### kd_mp4_get_frame

**Description**:

Get track stream information.

**Syntax**:

```cpp
int kd_mp4_get_frame(KD_HANDLE mp4_handle, k_mp4_frame_data_s *frame_data);
```

**Parameters**:

| Parameter Name | Description        | Input/Output |
|----------------|--------------------|--------------|
| mp4_handle     | MP4 instance handle | Input       |
| frame_data     | Stream information | Output       |

**Return Value**:

| Return Value | Description |
|--------------|-------------|
| 0            | Success.    |
| Non-0        | Failure.    |

**Requirements**:

- Header file: mp4_format.h
- Library file: libmp4.a

**Notes**:

- This API is for demuxer. Use when the created MP4 instance is a demuxer instance.

**Example**:

Refer to samples under mp4_demuxer.

**Related Topics**:

None.
