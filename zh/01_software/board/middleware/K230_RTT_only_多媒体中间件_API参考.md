# K230 RTT_only多媒体中间件API参考

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

本文档是K230 RTT_only多媒体中间件API参考的一部分，旨在为开发人员提供多媒体中间件的参考信息，包括API和头文件等。该中间件包含了各种功能，如rtsp server、rtsp client、rtsp pusher、播放器、MP4格式封装解封装等。开发人员可以通过本文档了解中间件的各个模块的API接口以及使用场景。请注意，本文档的内容可能会不定期更新或修改，因此请确保使用最新版本的文档进行开发。

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
| V0.1       | 软件部 | 2024.06.21 | 初版  |

## 1. 概述

### 1.1 概述

中间件代码在系统中的位置为`k230_sdk/src/big/mpp/middleware`，其中`k230_sdk/src/big/mpp/middleware/src`目录下为多媒体封装的api接口，`k230_sdk/src/big/mpp/middleware/sample`目录下为使用多媒体api接口对应的demo。

本文档提供了中间件中每个模块的API接口的详细描述，以及演示示例，帮助用户更好地理解不同模块API的使用场景。

### 1.2 功能描述

#### 1.2.1 rtsp server

rtsp-server支持将板子上的音频和视频数据以rtsp server协议发送给rtsp client客户端。

常用的使用场景有：

- 实时音视频传输：通过rtsp server将板子上的音频和视频数据实时传输给rtsp client客户端。
- 多媒体流媒体服务：搭建一个rtsp server，提供音视频流媒体服务，供客户端进行播放和访问。
- 远程监控：将板子上的音视频数据以rtsp server协议发送给远程客户端，实现远程监控功能。

#### 1.2.2 rtsp client

rtsp-client支持板子使用rtsp客户端协议从rtsp服务器获取音频和视频数据。

常用的使用场景有：

- 实时监控系统：通过rtsp-client从rtsp服务器获取实时的音频和视频数据，用于监控和录制。
- 多媒体播放器：使用rtsp-client从rtsp服务器获取音频和视频数据，用于播放多媒体内容。
- 视频会议系统：通过rtsp-client从rtsp服务器获取音频和视频数据，用于实现视频会议功能。

#### 1.2.3 rtsp推流

实现将板子上的视频数据以RTSP协议推送到第三方流媒体服务器，客户端可以通过第三方流媒体服务器获取板子推送的视频数据。

常用的使用场景有：

- 视频监控系统：将板子上的视频数据推送到流媒体服务器，供监控客户端实时查看。
- 视频直播：将板子上的视频数据推送到流媒体服务器，供观众通过流媒体服务器观看直播。
- 视频录制：将板子上的视频数据推送到流媒体服务器，实现视频录制功能。
- 视频分发：将板子上的视频数据推送到流媒体服务器，供多个客户端同时获取视频数据。

#### 1.2.4 播放器

实现mp4文件播放。视频支持h264、h265，音频支持g711a/u。

#### 1.2.5 MP4格式封装解封装

实现音视频与mp4格式间的封装与解封装。

#### 1.2.6 其他

本文件包含了K230中间件的API参考，其中包括了live555和ffmpeg开源多媒体库。
用户可以根据自己的需求使用这些库提供的功能。

## 2. API参考

### 2.1 rtsp-server

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

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
- 库文件：librtsp_server.a

【举例】

无。

### 2.2 rtsp-client

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
- 库文件：librtsp_client.a

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
- 库文件：librtsp_client.a

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
- 库文件: librtsp_client.a

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
- 库文件: librtsp_client.a

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
- 库文件：librtsp_client.a

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

### 2.4 MP4格式封装解封装

MP4格式封装解封装提供如下API：

- [kd_mp4_create](#241-kd_mp4_create)：MP4实例创建
- [kd_mp4_destroy](#242-kd_mp4_destroy)：MP4实例销毁
- [kd_mp4_create_track](#243-kd_mp4_create_track)：为MP4创建track
- [kd_mp4_destroy_tracks](#244-kd_mp4_destroy_tracks)：为MP4销毁所有track
- [kd_mp4_write_frame](#245-kd_mp4_write_frame)：MP4中写入帧数据。
- [kd_mp4_get_file_info](#246-kd_mp4_get_file_info)：获取MP4文件信息。
- [kd_mp4_get_track_by_index](#247-kd_mp4_get_track_by_index)：根据下标获取track信息。
- [kd_mp4_get_frame](#248-kd_mp4_get_frame)：获取track码流信息。

#### 2.4.1 kd_mp4_create

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

#### 2.4.2 kd_mp4_destroy

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

#### 2.4.3 kd_mp4_create_track

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

#### 2.4.4 kd_mp4_destroy_tracks

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

#### 2.4.5 kd_mp4_write_frame

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

#### 2.4.6 kd_mp4_get_file_info

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

#### 2.4.7 kd_mp4_get_track_by_index

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

#### 2.4.8 kd_mp4_get_frame

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

### 2.5 rtsp 推流

rtsp推流提供如下API：

- [Init](#251-kdrtsppusherinit)：初始化。
- [DeInit](#252-kdrtsppusherdeinit)：反初始化。
- [Open](#253-kdrtsppusheropen)：与流媒体服务器建立rtsp推流连接。
- [Close](#254-kdrtsppusherclose)：关闭流媒体服务器连接。
- [PushVideoData](#255-kdrtsppusherpushvideodata)：推送视频数据到流媒体。

#### 2.5.1 KdRtspPusher::Init

【描述】

初始化

【语法】

int Init(const RtspPusherInitParam &param);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| param  | rtsppusher初始化参数 | 输入 |

```c
class IRtspPusherEvent {
  public:
    virtual ~IRtspPusherEvent() {}
    virtual void OnRtspPushEvent(int event) = 0; // event 0: connect  ok; event 1:disconnet ;   event 2:reconnect ok
};

struct RtspPusherInitParam {
    int video_width;
    int video_height;
    char sRtspUrl[256];
    IRtspPusherEvent *on_event{nullptr};
};
```

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_pusher.h
- 库文件：librtsp_pusher.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.5.2 KdRtspPusher::Deinit

【描述】

反初始化。

【语法】

void DeInit();

【参数】

无。

【返回值】

无。

【需求】

- 头文件：rtsp_pusher.h
- 库文件：librtsp_pusher.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.5.3 KdRtspPusher::Open

【描述】

与流媒体服务器建立rtsp推流连接。

【语法】

int Open();

【参数】

无。

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_pusher.h
- 库文件：librtsp_pusher.a

【注意】

无。

【举例】

无。

【相关主题】

无。

#### 2.5.4 KdRtspPusher::Close

【描述】

关闭流媒体服务器连接。

【语法】

void Close();

【参数】

【返回值】

【需求】

- 头文件：rtsp_pusher.h
- 库文件：librtsp_pusher.a

【注意】

无。

【举例】

无。
【相关主题】

无。

#### 2.5.5 KdRtspPusher::PushVideoData

【描述】

推送视频数据到流媒体。

【语法】

int  PushVideoData(const uint8_t *data, size_t size, bool key_frame,uint64_t timestamp);

【参数】

| 参数名称 | 描述 | 输入/输出 |
|---|---|---|
| data  | 音频码流数据地址 | 输入 |
| size  | 音频码流数据大小 | 输入 |
| key_frame  | 是否是关键帧 | 输入 |
| timestamp | 音频码流数据时间戳（微妙） | 输入 |

【返回值】

| 返回值 | 描述                          |
|--------|-------------------------------|
| 0      | 成功。                        |
| 非0    | 失败。 |

【需求】

- 头文件：rtsp_pusher.h
- 库文件：librtsp_pusher.a

【注意】

当前版本只支持264编码推流。

【举例】

无。

【相关主题】

无。

## 3. demo

### 3.1 rtsp server

该示例介绍了如何使用RTSP协议实时将板子上的sensor画面和采集到的音频输出。通过拉取RTSP流，客户端可以获取到板子上的音视频数据。

#### 3.1.1 编译程序

在`k230_sdk`目录下执行`make mpp-middleware`，在`k230_sdk/src/big/mpp/userapps/sample/elf`目录下生成`sample_rtspserver.elf`可执行文件。
程序源码目录:
`k230_sdk/src/big/mpp/middleware/sample/sample_rtspserver`
板子上可执行文件位置:
`/sdcard/app/sample_rtspserver.elf`。

#### 3.1.2 参数说明

| 参数名 | 描述 |参数范围 | 默认值 |
|:--|:--|:--|:--|
| H | 打印命令行参数信息 | - | - |
| t | 编码类型 | h264、h265 | h265 |
| w | 视频编码宽度 | `[640, 1920]` | 1280 |
| h | 视频编码高度 | `[480, 1080]` |720 |
| b | 视频编码码率 | - | 2000 |
| s | sensor类型| 查看camera sensor文档（evb:-s 7,Canmv 1.0/1.1板:-s 24,Canmv 2.0板:-s 39） | 7 |

#### 3.1.3 运行程序

以Canmv 1.0板子为例，开机启动后，在大核串口按`q`键退出自启动程序。输入命令:`/sdcard/app/sample_rtspserver.elf -t h264 -w 1280 -h 720 -s 24`,如下所示，
串口输出会打印出形如：`rtsp://<server_ip>:8554/test` 的url地址.客户端使用vlc打开该url地址即可获取到板子上的音视频数据。

```text
/sdcard/app/sample_rtspserver.elf -t h264 -w 1280 -h 720 -s 24
./rtsp_server -H to show usage
Validate the input config, not implemented yet, TODO.
with_video
with_audio
g711liveSubSession

"BackChannelTest" stream
Play this stream using the URL "rtsp://10.100.228.92:8554/test"
vb_set_config ok
debug: _ai_i2s_set_pitch_shift : semitones = 0
kd_mpi_venc_init start 0
venc[0] 1280*720 size:462848 cnt:30 srcfps:30 dstfps:30 rate:4000 rc_mode:1 type:96 profile:3
kd_mpi_venc_init end
audio i2s set clk freq is 512000(512000),ret:1
audio init codec dac clk freq is 11289600
audio set codec dac clk freq is 2048000(2048000)
adec_bind_call_back dev_id:0 chn_id:0
audio i2s set clk freq is 512000(512000),ret:1
audio codec adc clk freq is 2048000(2048000)
mirror mirror is 0 , sensor tpye is 24
ov5647_power_rest OV5647_CAM_PIN is 0
kd_mpi_isp_set_output_chn_format, width(1280), height(720), pix_format(2)
ov5647_power_rest OV5647_CAM_PIN is 0
[dw] init, version Jun 20 2024 16:28:19

```

### 3.2 rtsp client

该示例介绍了如何使用RTSP协议作为客户端从RTSP服务器获取音频和视频流，并将视频数据显示在HDMI输出显示器上。

#### 3.2.1 编译程序

在`k230_sdk`目录下执行`make mpp-middleware`，在`k230_sdk/src/big/mpp/userapps/sample/elf`目录下生成`sample_rtspclient.elf`可执行文件。
程序源码目录:
`k230_sdk/src/big/mpp/middleware/sample/sample_rtspclient`
板子上可执行文件位置:
`/sdcard/app/sample_rtspclient.elf`。

#### 3.2.2 运行程序

以Canmv 1.0板子为例，开机启动后，在大核串口按`q`键退出自启动程序。输入命令:`/sdcard/app/sample_rtspclient.elf <rtsp_url> <out_type>`,如下所示，拉取服务器端的`rtsp://10.10.1.94:8554/canaan.264`流数据。注:evb板 out_type为0，Canmv 1.0/1.1板out_type为1。

```text
msh />/sdcard/app/sample_rtspclient.elf rtsp://10.10.1.94:8554/canaan.264 1
vb_set_config ok
debug: _ai_i2s_set_pitch_shift : semitones = 0
Created new TCP socket 9 for connection
Connecting to 10.10.1.94, port 8554 on socket 9...
...remote connection opened
Sending request: DESCRIBE rtsp://10.10.1.94:8554/canaan.264 RTSP/1.0
CSeq: 2
User-Agent: BackChannel RTSP Client (LIVE555 Streaming Media v2023.01.19)
Accept: application/sdp
Require: www.onvif.org/ver20/backchannel


Received 691 new bytes of response data.
Received a complete DESCRIBE response:
RTSP/1.0 200 OK
CSeq: 2
Date: Tue, Jun 25 2024 03:40:03 GMT
Content-Base: rtsp://10.10.1.94:8554/canaan.264/
Content-Type: application/sdp
Content-Length: 524

```

注：服务器rtsp server搭建方式有多种，如：使用live555 中的Meidaserver输出rtsp地址， 使用上例中的rtsp server输出rtsp地址。

### 3.3 rtsp pusher

该示例介绍了如何使用RTSP协议实时将板子上的sensor画面推流到三方流媒体服务器。通过从流媒体服务器拉取RTSP流，客户端可以获取到板子上的音视频数据。

#### 3.3.1 编译程序

在`k230_sdk`目录下执行`make mpp-middleware`，在`k230_sdk/src/big/mpp/userapps/sample/elf`目录下生成`sample_rtsppusher.elf`可执行文件。
程序源码目录:
`k230_sdk/src/big/mpp/middleware/sample/sample_rtsppusher`
板子上可执行文件位置:
`/sdcard/app/sample_rtsppusher.elf`。

#### 3.3.2 参数说明

| 参数名 | 描述 |参数范围 | 默认值 |
|:--|:--|:--|:--|
| H | 打印命令行参数信息 | - | - |
| w | 视频编码宽度 | `[640, 1920]` | 1280 |
| h | 视频编码高度 | `[480, 1080]` |720 |
| b | 视频编码码率 | - | 2000 |
| s | sensor类型| 查看camera sensor文档（evb:-s 7,Canmv 1.0/1.1板:-s 24,Canmv 2.0板:-s 39） | 7 |
| o | rtsp 推流地址 | - | - |

#### 3.3.3 运行程序

以Canmv 1.0板子为例，开机启动后，在大核串口按下`q`键退出自启动程序。然后输入以下命令：`/sdcard/app/sample_rtsppusher.elf -w 1280 -h 720 -s 24 -o <rtsp_url>`。如下所示，这将把板子上的视频推送到`rtsp://10.10.1.94:10554/live/test1`的流媒体地址。

```text
/sdcard/app/sample_rtsppusher.elf -w 1280 -h 720 -s 24 -o rtsp://10.10.1.94:10554/live/test1
./rtsp_server -H to show usage
Validate the input config, not implemented yet, TODO.
vb_set_config ok
debug: _ai_i2s_set_pitch_shift : semitones = 0
kd_mpi_venc_init start 0
venc[0] 1280*720 size:462848 cnt:30 srcfps:30 dstfps:30 rate:4000 rc_mode:1 type:96 profile:3
kd_mpi_venc_init end
rtsp_pusher url:rtsp://10.10.1.94:10554/live/test1
zlmedia url: rtsp://10.10.1.94:10554/live/test1, w: 1280, h: 720
audio i2s set clk freq is 512000(512000),ret:1
audio init codec dac clk freq is 11289600
audio set codec dac clk freq is 2048000(2048000)
adec_bind_call_back dev_id:0 chn_id:0
[libx264 @ 0x300015340] using cpu capabilities: none!
[libx264 @ 0x300015340] profile Constrained High, level 3.2, 4:2:0, 8-bit
[libx264 @ 0x300015340] 264 - core 157 - H.264/MPEG-4 AVC codec - Copyleft 2003-2019 - http://www.videolan.org/x264.html - options: cabac=1 ref=3 deblock=1:0:0 analyse=0x3:0x113 me=hex subme=7 psy=1 psy_rd=1.00:0.00 mixed_ref=1 me_range=16 chroma_me=1 trellis=1 8x8dct=1 cqm=0 deadzone=21,11 fast_pskip=1 chroma_qp_offset=-2 threads=1 lookahead_threads=1 sliced_threads=0 nr=0 decimate=1 interlaced=0 bluray_compat=0 constrained_intra=0 bframes=0 weightp=2 keyint=25 keyint_min=2 scenecut=40 intra_refresh=0 rc_lookahead=0 rc=cbr mbtree=0 bitrate=20000 ratetol=1.0 qcomp=0.60 qpmin=0 qpmax=69 qpstep=4 vbv_maxrate=20000 vbv_bufsize=20000 nal_hrd=none filler=0 ip_ratio=1.40 aq=1:1.00
url: rtsp://10.10.1.94:10554/live/test1 pusher extradata: 0x300011f78, size: 0
extradata: 0x3001719a0, size: 0
-----rtsp://10.10.1.94:10554/live/test1:
rtsp pusher init success, url: rtsp://10.10.1.94:10554/live/test1
audio i2s set clk freq is 512000(512000),ret:1
audio codec adc clk freq is 2048000(2048000)
mirror mirror is 0 , sensor tpye is 24
ov5647_power_rest OV5647_CAM_PIN is 0
kd_mpi_isp_set_output_chn_format, width(1280), height(720), pix_format(2)
ov5647_power_rest OV5647_CAM_PIN is 0
[dw] init, version Jun 20 2024 16:28:19
[100]rtsp://10.10.1.94:10554/live/test1 fLiveFrameQueue_ size:1,free framequeue size:24

```

注：流媒体服务器的搭建可以使用easydarwin 或 ZLMediaKit等。
