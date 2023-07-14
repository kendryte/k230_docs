# K230 中间件API参考

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

本文档为使用中间件进行开发的程序员编写，目的是供开发过程中查阅中间件参考信息，包括API、头文件等。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称 | 说明 |
|------|------|
|      |      |
|      |      |

### 修订记录

| 文档版本号 | 修改者 | 日期 | 修改说明 |
|---|---|---|---|
| V0.1       | 软件部 | 2023.07.20 | 初版  |

## 1. 概述

### 1.1 概述

中间件在系统中的位置为`k230_sdk/src/common/cdk/user/middleware`

本文档描述相关的中间件部分，涉及可视对讲协议、混音、mp4格式封装与解封装、播放器等。

### 1.2 功能描述

#### 1.2.1 可视对讲rtsp协议

参照ONVIF rtsp扩展，实现单线视频的可视对讲协议；

rtsp-server支持发送audio、video以及接收backchannel audio mediaSubSesisons.

rtsp-client支持接收audio、video以及发送backchannel audio mediaSubSessions.

相关描述见可视对讲协议章节

#### 1.2.2 播放器

实现mp4文件播放。视频支持h264、h265，音频支持g711a/u。

#### 1.2.3 混音

实现两路g711a/u混音。

#### 1.2.4 MP4格式封装解封装

实现音视频与mp4格式间的封装与解封装。

## 2. API参考

### 2.1 可视对讲rtsp-server

KdRtspServer提供以下API：

- [Init](#211-kdrtspserverinit)：初始化。
- [DeInit](#212-kdrtspserverdeinit)：反初始化。
- [CreateSession](#213-kdrtspservercreatesession)：创建rtsp session。
- [DestroySession](#214-kdrtspserverdestroysession)：销毁rtsp session。
- [Start](#215-kdrtspserverstart)：开启rtsp-server服务。
- [Stop](#216-kdrtspserverstop)：停止rtsp-server服务。
- [SendVideoData](#217-kdrtspserversendvideodata)：写入视频码流数据。
- [SendAudioData](#218-kdrtspserversendaudiodata)：写入音频码流数据。

#### 2.1.1 KdRtspServer::Init

【描述】

rtsp-server初始化。

【语法】

int Init(Port port = 8554, IOnBackChannel *back_channel = nullptr);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| port  | rtsp服务端口。 | 输入      |
| back_channel     | 对端来的音频数据回调指针。   | 输入      |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败。                        |

【需求】

- 头文件：rtsp_server.h
- 库文件：

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.1.2 KdRtspServer::DeInit

【描述】

反初始化。

【语法】

void DeInit();

【参数】

无。

【返回值】

无。

【需求】

- 头文件：rtsp_server.h
- 库文件：

【举例】

无。

#### 2.1.3 KdRtspServer::CreateSession

【描述】

创建RtspSession。

【语法】

int CreateSession(const std::string &session_name, const SessionAttr &session_attr);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| session_name | stream url。 | 输入 |
| session_attr | session 配置参数。 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_server.h
- 库文件：

【注意】

【举例】

无。

#### 2.1.4 KdRtspServer::DestroySession

【描述】

销毁rtsp session。

【语法】

int DestroySession(const std::string &session_name);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| session_name | stream url。| 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_server.h
- 库文件：

【注意】

【举例】

无。

【相关主题】

#### 2.1.5 KdRtspServer::Start

【描述】

开启rtsp server服务。

【语法】

void Start();

【参数】

无。

【返回值】

无。

【需求】

- 头文件：rtsp-server.h
- 库文件：

【注意】
无

【举例】

无。

【相关主题】

#### 2.1.6 KdRtspServer::Stop

【描述】

停止rtsp-server服务。

【语法】

void Stop();

【参数】

无

【返回值】

无

【需求】

- 头文件：rtsp_server.h
- 库文件：

【注意】

【举例】

无。

#### 2.1.7 KdRtspServer::SendVideoData

【描述】

写入视频码流数据。

【语法】

int SendVideoData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| session_name  | stream url | 输入 |
| data   | 视频码流地址。 | 输入 |
| size   | 视频码流大小。 | 输入 |
| timestamp   | 码流时间戳（毫秒） | 输入 |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_server.h
- 库文件：

【举例】

无。

#### 2.1.8 KdRtspServer::SendAudioData

【描述】

写入音频码流数据。

【语法】

int SendAudioData(const std::string &session_name, const uint8_t *data, size_t size, uint64_t timestamp);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| session_name  | stream url | 输入 |
| data   | 音频码流地址。 | 输入 |
| size   | 音频码流大小。 | 输入 |
| timestamp   | 码流时间戳（毫秒） | 输入 |

【返回值】

| 返回值 | 描述 |
|---|---|
| 0      | 成功。                        |
| 非0    | 失败。  |

【需求】

- 头文件：rtsp_server.h
- 库文件：

【举例】

无。

### 2.2 可视对讲rtsp-client

KdRtspClient模块提供以下API：

- [Init](#221-kdrtspclientinit)：初始化。
- [DeInit](#222-kdrtspclientdeinit)：反初始化。
- [Open](#223-kdrtspclientopen)：打开并运行rtspclient连接。
- [Close](#224-kdrtspclientclose)：关闭rtspclient连接。
- [SendAudioData](#225-kdrtspclientsendaudiodata)：写入backchannel音频码流数据。

#### 2.2.1 KdRtspClient::Init

【描述】

初始化

【语法】

int Init(const RtspClientInitParam &param);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| param  | rtspclient初始化参数 | 输入 |

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
        IOnVideoData *on_video_data{nullptr}; // 从server侧收到的视频码流帧回调
        IOnAudioData *on_audio_data{nullptr}; // 从server侧收到的音频码流帧回调
        IRtspClientEvent *on_event{nullptr};  // rtspclient event回调
        bool enableBackchanel{false};         // 是否enable audio backchannel
    };
```

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_client.h
- 库文件：

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.2.2 KdRtspClient::Deinit

【描述】

反初始化。

【语法】

void DeInit();

【参数】

无。

【返回值】

无。

【需求】

- 头文件：rtsp_client.h
- 库文件：

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.2.3 KdRtspClient::Open

【描述】

打开并运行rtspclient连接

【语法】

int Open(const char *url);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| url  | rtsp url。 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_client.h
- 库文件:

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.2.4 KdRtspClient::Close

【描述】

关闭rtsp client。

【语法】

void Close();

【参数】

【返回值】

【需求】

- 头文件：rtsp_client.h
- 库文件:

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.2.5 KdRtspClient::SendAudioData

【描述】

写入音频back channnel码流数据。

【语法】

int SendAudioData(const uint8_t *data, size_t size, uint64_t timestamp);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| data  | 音频码流数据地址 | 输入 |
| size  | 音频码流数据大小 | 输出 |
| timestamp | 音频码流数据时间戳（毫秒） | 输出 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_client.h
- 库文件：

【注意】

无。

【举例】

无。

【相关主题】

无。

### 2.3 播放器封装

KdPlayer模块提供以下API：

- [kd_player_init](#231-kd_player_init)：初始化。
- [kd_player_deinit](#232-kd_player_deinit)：反初始化。
- [kd_player_setdatasource](#233-kd_player_setdatasource)：设置媒体播放文件。
- [kd_player_regcallback](#234-kd_player_regcallback)：注册事件回调。
- [kd_player_start](#235-kd_player_start)：开始播放。
- [kd_player_stop](#236-kd_player_stop)：停止播放。

#### 2.3.1 kd_player_init

【描述】

播放器初始化。

【语法】

k_s32 kd_player_init();

【参数】

无

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.3.2 kd_player_deinit

【描述】

反初始化。

【语法】

k_s32 kd_player_deinit();

【参数】

无

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.3.3 kd_player_setdatasource

【描述】

反初始化。

【语法】

k_s32 kd_player_setdatasource(const k_char* filePath);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| filePath  | 媒体文件路径 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.3.4 kd_player_regcallback

【描述】

注册播放器事件回调。

【语法】

k_s32 kd_player_regcallback( K_PLAYER_EVENT_FN pfnCallback,void* pData);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| pfnCallback  | 回调函数指针 | 输入 |
| pData  | 回调数据指针 | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.3.5 kd_player_start

【描述】

开始播放。

【语法】

k_s32 kd_player_start();

【参数】

无

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.3.6 kd_player_stop

【描述】

停止播放。

【语法】

k_s32 kd_player_stop();

【参数】

无

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：kplayer.h
- 库文件：libkplayer.a

【注意】

无。

【举例】

无。

【相关主题】

无。

### 2.4 音频混音

混音模块提供以下API：

- [kd_mix_g711a_audio](#241-kd_mix_g711a_audio)：g711a混音。
- [kd_mix_g711u_audio](#242-kd_mix_g711u_audio)：g711u混音。

#### 2.4.1 kd_mix_g711a_audio

【描述】

g711a混音

【语法】

k_s32 kd_mix_g711a_audio(k_char \*src_data1, k_char \*src_data2, k_u32 data_len, k_char \*dst_mix_data);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| src_data1  | 混音源数据1 | 输入 |
| src_data2  | 混音源数据2 | 输入 |
| data_len  | 混音数据长度 | 输入 |
| dst_mix_data  | 混音结果数据 | 输出 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：g711_mix_audio.h
- 库文件：libaudio_mix.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.4.2 kd_mix_g711u_audio

【描述】

g711u混音

【语法】

k_s32 kd_mix_g711u_audio(k_char \*src_data1, k_char \*src_data2, k_u32 data_len, k_char \*dst_mix_data);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| src_data1  | 混音源数据1 | 输入 |
| src_data2  | 混音源数据2 | 输入 |
| data_len  | 混音数据长度 | 输入 |
| dst_mix_data  | 混音结果数据 | 输出 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：g711_mix_audio.h
- 库文件：libaudio_mix.a

【注意】

无。

【举例】

无。

【相关主题】

无。

### 2.5 MP4格式封装解封装

MP4格式封装解封装提供如下API：

- [kd_mp4_create](#251-kd_mp4_create)：MP4实例创建
- [kd_mp4_destroy](#252-kd_mp4_destroy)：MP4实例销毁
- [kd_mp4_create_track](#253-kd_mp4_create_track)：为MP4创建track
- [kd_mp4_destroy_tracks](#254-kd_mp4_destroy_tracks)：为MP4销毁所有track
- [kd_mp4_write_frame](#255-kd_mp4_write_frame)：MP4中写入帧数据。
- [kd_mp4_get_file_info](#256-kd_mp4_get_file_info)：获取MP4文件信息。
- [kd_mp4_get_track_by_index](#257-kd_mp4_get_track_by_index)：根据下标获取track信息。
- [kd_mp4_get_frame](#258-kd_mp4_get_frame)：获取track码流信息。

#### 2.5.1 kd_mp4_create

【描述】

MP4实例创建

【语法】

int kd_mp4_create(KD_HANDLE *mp4_handle, k_mp4_config_s \*mp4_cfg);

【参数】

|     参数   |     描述    |   输入/输出   |
|------------|------------|--------------|
| mp4_handle | MP4实例句柄 |     输出     |
| mp4_cfg    | 参数配置信息 |     输入     |

【返回值】

|  返回值  |   描述  |
|----------|--------|
|    0     |  成功  |
|   非0    |  失败  |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

通过mp4_cfg配置信息可以指定当前创建的MP4实例时muxer实例或者demuxer实例

【举例】

参考 samples下 mp4_muxer和mp4_demuxer

【相关主题】

无

#### 2.5.2 kd_mp4_destroy

【描述】

MP4实例销毁

【语法】

int kd_mp4_destroy(KD_HANDLE mp4_handle);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle | MP4实例句柄 |     输入       |

【返回值】

|    返回值    |    描述    |
|--------------|-----------|
|      0       |    成功    |
|     非0      |    失败     |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

无

【举例】

参考 samples下 mp4_muxer和mp4_demuxer

【相关主题】

无

#### 2.5.3 kd_mp4_create_track

【描述】

为MP4创建track

【语法】

int kd_mp4_create_track(KD_HANDLE mp4_handle, KD_HANDLE \*track_handle, k_mp4_track_info_s \*mp4_track_info);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle | MP4实例句柄 |    输入        |
|track_handle| track句柄   |    输出        |
|mp4_track_info| track配置 |    输入        |

【返回值】

|    返回值   |    描述    |
|-------------|------------|
|     0       |    成功     |
|    非0      |    失败     |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为muxer API，当创建的MP4实例为muxer实例时使用
- 目前每个MP4支持创建最多3个track

【举例】

参考 samples下 mp4_muxer

【相关主题】

无

#### 2.5.4 kd_mp4_destroy_tracks

【描述】

为MP4销毁所有track

【语法】

int kd_mp4_destroy_tracks(KD_HANDLE mp4_handle);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle |  MP4实例   |   输入          |

【返回值】

|    返回值    |    描述    |
|--------------|-----------|
|     0        |   成功     |
|    非0       |   失败     |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为muxer API，当创建的MP4实例为muxer实例时使用
- 请在创建MP4实例和track之后调用该接口

【举例】

参考 samples下 mp4_muxer

【相关主题】

无

#### 2.5.5 kd_mp4_write_frame

【描述】

MP4中写入帧数据

【语法】

int kd_mp4_write_frame(KD_HANDLE mp4_handle, KD_HANDLE track_handle, k_mp4_frame_data_s *frame_data);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
|  mp4_handle| MP4实例句柄 |  输入          |
| track_handle| track句柄  |  输入          |
| frame_data  |  帧数据信息 |  输入         |

【返回值】

|    返回值    |    描述    |
|--------------|-----------|
|      0       |    成功    |
|     非0      |    失败    |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为muxer API，当创建的MP4实例为muxer实例时使用
- 请在创建MP4实例和track之后调用该接口

【举例】

参考 samples下 mp4_muxer

【相关主题】

无

#### 2.5.6 kd_mp4_get_file_info

【描述】

获取MP4文件信息

【语法】

int kd_mp4_get_file_info(KD_HANDLE mp4_handle, k_mp4_file_info_s *file_info);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle | MP4实例句柄 |   输入         |
| file_info  | MP4文件信息 |   输出         |

【返回值】

|    返回值    |    描述    |
|--------------|-----------|
|      0       |    成功    |
|     非0      |    失败    |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为demuxer API，当创建的MP4实例为demuxer实例时使用

【举例】

参考 samples下 mp4_demuxer

【相关主题】

无

#### 2.5.7 kd_mp4_get_track_by_index

【描述】

根据下标获取track信息

【语法】

int kd_mp4_get_track_by_index(KD_HANDLE mp4_handle, uint32_t index, k_mp4_track_info_s *mp4_track_info);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle | MP4实例句柄|   输入          |
|   index    |   下标     |   输入          |
| mp4_track_info | track信息 | 输出         |

【返回值】

|    返回值    |    描述    |
|--------------|------------|
|      0       |    成功     |
|     非0      |    失败     |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为demuxer API，当创建的MP4实例为demuxer实例时使用

【举例】

参考 samples下 mp4_demuxer

【相关主题】

无

#### 2.5.8 kd_mp4_get_frame

【描述】

获取track码流信息

【语法】

int kd_mp4_get_frame(KD_HANDLE mp4_handle, k_mp4_frame_data_s *frame_data);

【参数】

|    参数    |    描述    |    输入/输出    |
|------------|------------|----------------|
| mp4_handle |  MP4实例句柄|    输入        |
| frame_data |  码流信息   |    输出        |

【返回值】

|    返回值    |    描述    |
|--------------|-----------|
|      0       |   成功     |
|     非0      |   失败     |

【需求】

- 头文件：mp4_format.h
- 库文件：libmp4.a

【注意】

- 该API为demuxer API，当创建的MP4实例为demuxer实例时使用

【举例】

参考 samples下 mp4_demuxer

【相关主题】

无
