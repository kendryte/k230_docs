# K230 Middleware API Reference

![cover](../../../../zh/01_software/board/middleware/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/middleware/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## Preface

### Overview

This document provides reference information about the middleware, including application programming interfaces (APIs), header files for programmers who use the middleware to develop products.

This document also describes the method of calling each API, and related data structures and error codes.

### Intended Audience

This document is intended primarily for:

- Technical support engineers
- Software development engineers

### Definition of acronyms

| abbreviation | illustrate |
|------|------|
|      |      |
|      |      |

### Revision history

| Document version number | Author | date | Modify the description |
|---|---|---|---|
| V0.1       | Software Department | 2023.07.20 | Initial edition  |

## 1. Overview

### 1.1 Overview

The location of middleware is `k230_sdk/src/common/cdk/user/middleware`

This document describes the relevant middleware parts, including video intercom, audio-mixer, fMP4(mp4) muxer and demuxer, players, etc.

### 1.2 Module Description

#### 1.2.1 Video intercom

The video intercom supports bidirectional audio and one-way video, is implemented based on rtsp protocol with ONVIF rtsp extension;

The rtsp-server supports audio, video and backchannel audio mediaSubSesisons to send audio, video data to the client and receive audio data from the client.

The rtsp-client supports audio, video and backchannel audio mediaSubSessions to receive audio, video data from the server and send audio data to the server.

#### 1.2.2 Player

The player supports MP4 file (H264/H265, and G711A-Law/mu-Law).

#### 1.2.3 Audio Mixer

The audio mixer supports G711 A-Law/mu-Law.

#### 1.2.4 fMP4(Mp4) muxer and demuxer

This module provides functions of encapsulation, decapsulation for H264/H265 and G711 A-Law/mu-Law in MPEG-4 Part 14(MP4) format, and supports fragment MP4 as well.

## 2. API Reference

### 2.1 Video intercom Server

KdRtspServer provides the following APIs:

- [Init](#211-kdrtspserverinit):Initializes the rtsp-server.
- [DeInit](#212-kdrtspserverdeinit):Deinitializes the rtsp-server.
- [CreateSession](#213-kdrtspservercreatesession)：Creates rtsp session.
- [DestroySession](#214-kdrtspserverdestroysession)：Destroys rtsp session.
- [Start](#215-kdrtspserverstart):Starts the rtsp-server service.
- [Stop](#216-kdrtspserverstop):Stops the rtsp-server service.
- [SendVideoData](#217-kdrtspserversendvideodata):Writes video stream data.
- [SendAudioData](#218-kdrtspserversendaudiodata):Writes audio stream data.

#### 2.1.1 KdRtspServer::Init

【Description】

 Initializes the rtsp-server.

【Syntax】

int Init(Port port = 8554, IOnBackChannel *back_channel = nullptr);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| port  | RTSP service port. | input      |
| back_channel     | pointer to the audio data callback. | input      |

【Return value】

| Return value | description |
|---|---|
| 0      | Succeed.                        |
| Non-0    | Fail.                        |

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.1.2 KdRtspServer::DeInit

【Description】

Deinitializes the rtsp-server.

【Syntax】

void DeInit();

【Parameters】

None

【Return value】

None

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Example】

None

#### 2.1.3 KdRtspServer::CreateSession

【Description】

Creates an RtspSession.

【Syntax】

int CreateSession(const std::string &session_name, const SessionAttr &session_attr);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| session_name | stream url。 | input |
| session_attr | session configuration parameters. | input |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Note】

【Example】

None

#### 2.1.4 KdRtspServer::DestroySession

【Description】

Destroys the rtsp session。

【Syntax】

int DestroySession(const std::string &session_name);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| session_name | stream url。| input |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Note】

【Example】

None

【See Also】

None

#### 2.1.5 KdRtspServer::Start

【Description】

Starts the rtsp-server service.

【Syntax】

void Start();

【Parameters】

None

【Return value】

None

【Requirement】

- Header files: rtsp-server.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.1.6 KdRtspServer::Stop

【Description】

Stops the rtsp-server service.

【Syntax】

void Stop();

【Parameters】

None

【Return value】

None

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Example】

None

#### 2.1.7 KdRtspServer::SendVideoData

【Description】

Writes the video stream data.

【Syntax】

int SendVideoData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| session_name  | stream url | input |
| data   | The video data address | input |
| size   | The video data size | input |
| timestamp   | The video data timestamp (ms) | input |

【Return value】

| Return value | description |
|---|---|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Example】

None.

#### 2.1.8 KdRtspServer::SendAudioData

【Description】

Writes the audio stream data.

【Syntax】

int SendAudioData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| session_name  | stream url | input |
| data   | The audio stream data address. | input |
| size   | The audio stream data size. | input |
| timestamp   | The audio stream data timestamp (ms) | input |

【Return value】

| Return value | description |
|---|---|
| 0      | Succeed.                        |
| Non-0    | Fail.  |

【Requirement】

- Header files: rtsp_server.h
- Library files:

【Example】

None

### 2.2 Video intercom Client

The KdRtspClient module provides the following APIs:

- [Init](#221-kdrtspclientinit):Initializes the rtsp-client.
- [DeInit](#222-kdrtspclientdeinit):Deinitializes the rtsp-client.
- [Open](#223-kdrtspclientopen):Opens the rtspclient session.
- [Close](#224-kdrtspclientclose):Closes the rtspclient session.
- [SendAudioData](#225-kdrtspclientsendaudiodata):Writes the backchannel audio stream data.

#### 2.2.1 KdRtspClient::Init

【Description】

Initializes the rtsp-client

【Syntax】

int Init(const RtspClientInitParam &param);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| param  | rtspclient initialization parameters | input |

```c
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
        IOnVideoData *on_video_data{nullptr}; // callback for video data from server
        IOnAudioData *on_audio_data{nullptr}; // callback for audio data from server
        IRtspClientEvent *on_event{nullptr};  // callback for rtsp-client event
        bool enableBackchanel{false};         // whether enable audio backchannel or not
    };
```

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_client.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.2.2 KdRtspClient::Deinit

【Description】

Deinitializes the rtsp-client.

【Syntax】

void DeInit();

【Parameters】

None

【Return value】

None

【Requirement】

- Header files: rtsp_client.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.2.3 KdRtspClient::Open

【Description】

Opens the rtspclient session

【Syntax】

int Open(const char *url);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| url  | rtsp url | input |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_client.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.2.4 KdRtspClient::Close

【Description】

Closes the rtsp client。

【Syntax】

void Close();

【Parameters】

None

【Return value】

None

【Requirement】

- Header files: rtsp_client.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

#### 2.2.5 KdRtspClient::SendAudioData

【Description】

Writes the audio back channnel stream data.

【Syntax】

int SendAudioData(const uint8_t *data, size_t size, uint64_t timestamp);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| data  | The audio stream data address | input |
| size  | The audio stream data size | output |
| timestamp | The audio stream data timestamp (ms) | output |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: rtsp_client.h
- Library files:

【Note】

None

【Example】

None

【See Also】

None

### 2.3 Player

The KdPlayer module provides the following APIs:

- [kd_player_init](#231-kd_player_init):Initialzes the player.
- [kd_player_deinit](#232-kd_player_deinit):Deinitializes the player.
- [kd_player_setdatasource](#233-kd_player_setdatasource):Sets up media playback file.
- [kd_player_regcallback](#234-kd_player_regcallback):Registers event callbacks.
- [kd_player_start](#235-kd_player_start):Starts to play.
- [kd_player_stop](#236-kd_player_stop):Stops.

#### 2.3.1 kd_player_init

【Description】

Initializes the player.

【Syntax】

k_s32 kd_player_init();

【Parameters】

None

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.3.2 kd_player_deinit

【Description】

Deinitializes the player.

【Syntax】

k_s32 kd_player_deinit();

【Parameters】

None

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.3.3 kd_player_setdatasource

【Description】

Sets the source file to play.

【Syntax】

k_s32 kd_player_setdatasource(const k_char* filePath);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| filePath  | The path to the media file | input |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.3.4 kd_player_regcallback

【Description】

Registers the event callbacks.

【Syntax】

k_s32 kd_player_regcallback( K_PLAYER_EVENT_FN pfnCallback,void* pData);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| pfnCallback  | The callback function pointer | input |
| pData  | Callback data pointer | input |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.3.5 kd_player_start

【Description】

Starts playing.

【Syntax】

k_s32 kd_player_start();

【Parameters】

None

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.3.6 kd_player_stop

【Description】

Stops the playback.

【Syntax】

k_s32 kd_player_stop();

【Parameters】

None

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: kplayer.h
- Library files: libkplayer.a

【Note】

None

【Example】

None

【See Also】

None

### 2.4 Audio Mixer

The Mix module provides the following APIs:

- [kd_mix_g711a_audio](#241-kd_mix_g711a_audio):mixes g711a-law data
- [kd_mix_g711u_audio](#242-kd_mix_g711u_audio):mixer g711mu-law data

#### 2.4.1 kd_mix_g711a_audio

【Description】

Mixes the G711 a-law data

【Syntax】

k_s32 kd_mix_g711a_audio(k_char \*src_data1, k_char \*src_data2, k_u32 data_len, k_char \*dst_mix_data);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| src_data1  | Mix source data1 | input |
| src_data2  | Mix source data 2 | input |
| data_len  | Mix data length | input |
| dst_mix_data  | Mix result data | output |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: g711_mix_audio.h
- Library files: libaudio_mix.a

【Note】

None

【Example】

None

【See Also】

None

#### 2.4.2 kd_mix_g711u_audio

【Description】

Mixes the G711 mu-law data

【Syntax】

k_s32 kd_mix_g711u_audio(k_char \*src_data1, k_char \*src_data2, k_u32 data_len, k_char \*dst_mix_data);

【Parameters】

| Parameter name | description | Input/output |
|---|---|---|
| src_data1  | Mix source data1 | input |
| src_data2  | Mix source data 2 | input |
| data_len  | Mix data length | input |
| dst_mix_data  | Mix result data | output |

【Return value】

| Return value | description                          |
|--------|-------------------------------|
| 0      | Succeed.                        |
| Non-0    | Fail. |

【Requirement】

- Header files: g711_mix_audio.h
- Library files: libaudio_mix.a

【Note】

None

【Example】

None

【See Also】

None

### 2.5 MP4 Muxer and Demuxer

The MP4 module provides the following APIs:

- [kd_mp4_create](#251-kd_mp4_create): Creates a MP4 instance
- [kd_mp4_destroy](#252-kd_mp4_destroy): Destroys a MP4 instance
- [kd_mp4_create_track](#253-kd_mp4_create_track): Creates a track for MP4
- [kd_mp4_destroy_tracks](#254-kd_mp4_destroy_tracks): Destroys all tracks for MP4
- [kd_mp4_write_frame](#255-kd_mp4_write_frame): Writes frame data
- [kd_mp4_get_file_info](#256-kd_mp4_get_file_info): Gets information
- [kd_mp4_get_track_by_index](#257-kd_mp4_get_track_by_index):Gets track information
- [kd_mp4_get_frame](#258-kd_mp4_get_frame):Gets the audio/video frame data.

#### 2.5.1 kd_mp4_create

【Description】

Creates a MP4 instance

【Syntax】

int kd_mp4_create(KD_HANDLE *mp4_handle, k_mp4_config_s \*mp4_cfg);

【Parameters】

|     parameter   |     description    |   Input/output   |
|------------|------------|--------------|
| mp4_handle | MP4 instance handle |     output     |
| mp4_cfg    | Parameter configuration information |     input     |

【Return value】

|  Return value  |   description  |
|----------|--------|
|    0     |  succeed  |
|   Non-0    |  fail  |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

Uses mp4_cfg to specify whether to create a muxer instance or a demuxer instance.

【Example】

Refer to the mp4_muxer and mp4_demuxer under the directory "samples"

【See Also】

None

#### 2.5.2 kd_mp4_destroy

【Description】

Destroys the MP4 instance

【Syntax】

int kd_mp4_destroy(KD_HANDLE mp4_handle);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle | MP4 instance handle |     input       |

【Return value】

|    Return value    |    description    |
|--------------|-----------|
|      0       |    succeed    |
|     Non-0      |    fail     |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

None

【Example】

Refer to the mp4_muxer and mp4_demuxer under the directory "samples"

【See Also】

None

#### 2.5.3 kd_mp4_create_track

【Description】

Creates a track for MP4

【Syntax】

int kd_mp4_create_track(KD_HANDLE mp4_handle, KD_HANDLE \*track_handle, k_mp4_track_info_s \*mp4_track_info);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle | MP4 instance handle |    input        |
|track_handle| Track handle   |    output        |
|mp4_track_info| Track configuration |    input        |

【Return value】

|    Return value   |    description    |
|-------------|------------|
|     0       |    succeed     |
|    Non-0      |    fail     |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

- This API is a muxer API and is used when creating an MP4 instance that is a muxer instance
- Currently each MP4 instance supports creating up to 3 tracks

【Example】

Refer to the samples under mp4_muxer

【See Also】

None

#### 2.5.4 kd_mp4_destroy_tracks

【Description】

Destroys all tracks for MP4

【Syntax】

int kd_mp4_destroy_tracks(KD_HANDLE mp4_handle);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle |  MP4 instance   |   input          |

【Return value】

|    Return value    |    description    |
|--------------|-----------|
|     0        |   succeed     |
|    Non-0       |   fail     |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

None

【Example】

Refer to the samples under mp4_muxer

【See Also】

None

#### 2.5.5 kd_mp4_write_frame

【Description】

Writes frame data

【Syntax】

int kd_mp4_write_frame(KD_HANDLE mp4_handle, KD_HANDLE track_handle, k_mp4_frame_data_s *frame_data);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
|  mp4_handle| MP4 instance handle |  input          |
| track_handle| Track handle  |  input          |
| frame_data  |  Frame data information |  input         |

【Return value】

|    Return value    |    description    |
|--------------|-----------|
|      0       |    succeed    |
|     Non-0      |    fail    |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

None

【Example】

Refer to the samples under mp4_muxer

【See Also】

None

#### 2.5.6 kd_mp4_get_file_info

【Description】

Gets MP4 file information

【Syntax】

int kd_mp4_get_file_info(KD_HANDLE mp4_handle, k_mp4_file_info_s *file_info);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle | MP4 instance handle |   input         |
| file_info  | MP4 file information |   output         |

【Return value】

|    Return value    |    description    |
|--------------|-----------|
|      0       |    succeed    |
|     Non-0      |    fail    |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

None

【Example】

Refer to the mp4_demuxer under samples

【See Also】

None

#### 2.5.7 kd_mp4_get_track_by_index

【Description】

Gets track information based on subscripts

【Syntax】

int kd_mp4_get_track_by_index(KD_HANDLE mp4_handle, uint32_t index, k_mp4_track_info_s *mp4_track_info);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle | MP4 instance handle|   input          |
|   index    |   subscript     |   input          |
| mp4_track_info | Track information | output         |

【Return value】

|    Return value    |    description    |
|--------------|------------|
|      0       |    succeed     |
|     Non-0      |    fail     |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

- This API is a demuxer API and is used when creating an MP4 instance that is a demuxer instance

【Example】

Refer to the mp4_demuxer under samples

【See Also】

None

#### 2.5.8 kd_mp4_get_frame

【Description】

Gets the video/audio frame data

【Syntax】

int kd_mp4_get_frame(KD_HANDLE mp4_handle, k_mp4_frame_data_s *frame_data);

【Parameters】

|    parameter    |    description    |    Input/output    |
|------------|------------|----------------|
| mp4_handle |  MP4 instance handle|    input        |
| frame_data |  Stream information   |    output        |

【Return value】

|    Return value    |    description    |
|--------------|-----------|
|      0       |   succeed     |
|     Non-0      |   fail     |

【Requirement】

- Header files: mp4_format.h
- Library files: libmp4.a

【Note】

- This API is a demuxer API and is used when creating an MP4 instance that is a demuxer instance

【Example】

Refer to the mp4_demuxer under samples

【See Also】

None
