# K230核间通讯API参考

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

本文档主要介绍媒体子系统中系统控制模块的功能和用法，其它模块的功能和用法将各有专门的文档加以论述。

### 读者对象

本文档（本指南）主要适用于以下人员：

- 技术支持工程师
- 软件开发工程师

### 缩略词定义

| 简称   | 说明                                     |
|--------|------------------------------------------|
| ipcm   | internal processor communication module  |
| IPCMSG | internal processor communication message |

### 修订记录

| 文档版本号 | 修改说明 | 修改者 | 日期     |
|------------|----------|--------|----------|
| v1.0       | 初版     | 郝海波 | 2023/3/8 |

## 1. 概述

### 1.1 概述

该文档描述了K230异构核间通讯的相关内容。

#### 1.1.1 核间通讯实现原理

![日程表 低可信度描述已自动生成](images/91c0f5a20c9460bd6c865a704f7b9404.png)

- 共享内存用于大小核发送通信消息的具体内容
- 共享内存管理用于标识通信消息的属性例如地址，大小，端口号等
- Mailbox通过中断方式实现大小核发送消息后的通知机制

#### 1.1.2 内存空间使用

目前大小核使用的数据共享内存区域设计共1M空间，对于参与通讯的一方来说发送和接收各占512KB的空间大小。用于维护各个核状态的共享内存区域为4KB。

### 1.2 功能描述

#### 1.2.1 IPCMSG

IPCMSG是K230大小核在用户态进行通讯的组件，主要用于发送控制类消息。该模块包括服务添加删除，消息创建删除，断开连接，发送消息等功能。支持三种消息发送方式，发送异步消息，发送同步消息，以及发送不需要对方回复的消息。其中同步消息支持超时机制，用户调用API时可自定义设置超时时间。需要得到回复的消息，在发出60秒之后才收到回复消息的话，该回复消息会被丢弃。

#### 1.2.2 DATAFIFO

DATAFIFO是K230大小核在用户态进行大量数据交互(例如编码数据)时，使用的核间通讯组件。内部主要使用共享内存来完成数据的交互，数据传递的是指针，不会拷贝数据的内容，数据的收发通知依靠线程轮训来实现。

DATAFIFO 主要包含通路的打开、关闭、数据的写入和读出，以及其他控制命令

## 2. API 参考

### 2.1 IPCMSG

该功能模块提供以下API：

- [kd_ipcmsg_add_service](#211-kd_ipcmsg_add_service)
- [kd_ipcmsg_del_service](#212-kd_ipcmsg_del_service)
- [kd_ipcmsg_try_connect](#213-kd_ipcmsg_try_connect)
- [kd_ipcmsg_connect](#214-kd_ipcmsg_connect)
- [kd_ipcmsg_disconnect](#215-kd_ipcmsg_disconnect)
- [kd_ipcmsg_is_connect](#216-kd_ipcmsg_is_connect)
- [kd_ipcmsg_send_only](#217-kd_ipcmsg_send_only)
- [kd_ipcmsg_send_async](#218-kd_ipcmsg_send_async)
- [kd_ipcmsg_send_sync](#219-kd_ipcmsg_send_sync)
- [kd_ipcmsg_run](#2110-kd_ipcmsg_run)
- [kd_ipcmsg_create_message](#2111-kd_ipcmsg_create_message)
- [kd_ipcmsg_create_resp_message](#2112-kd_ipcmsg_create_resp_message)
- [kd_ipcmsg_destory_message](#2113-kd_ipcmsg_destroy_message)

#### 2.1.1 kd_ipcmsg_add_service

【描述】

添加服务

【语法】

k_s32 kd_ipcmsg_add_service(const k_char\* pszServiceName, const [k_ipcmsg_connect_s](#314-k_ipcmsg_connect_s)* pstConnectAttr);

【参数】

| **参数名称**         | **描述**                          | **输入/输出** |
|-----------------|-------------------------------|-----------|
| pszServiceName  | 服务的名称指针。。            | 输入      |
| pstConnectAttr  | 连接对端服务器的属性结构体。  | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

Service 可以添加多个，但不同的 service 不能使用相同的端口号，client 跟 service 是通

过相同的端口号来通信的，因此一个 service能对应一个 client

【举例】

无

【相关主题】

[kd_ipcmsg_del_service](#212-kd_ipcmsg_del_service)

#### 2.1.2 kd_ipcmsg_del_service

【描述】

删除服务

【语法】

k_s32 kd_ipcmsg_del_service(const k_char* pszServiceName);

【参数】

| **参数名称**         | **描述**                                                              | **输入/输出** |
|-----------------|-------------------------------------------------------------------|-----------|
| pszServiceName  | 服务的名称指针。服务名称最大长度： K_IPCMSG_MAX_SERVICENAME_LEN。 | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_create_resp_message](#2112-kd_ipcmsg_create_resp_message)

#### 2.1.3 kd_ipcmsg_try_connect

【描述】

非阻塞方式建立连接

【语法】

k_s32 kd_ipcmsg_try_connect(k_s32\* ps32Id, const k_char\* pszServiceName, [k_ipcmsg_handle_fn_ptr](#316-k_ipcmsg_handle_fn_ptr) pfnMessageHandle);

【参数】

| **参数名称**           | **描述**                | **输入/输出** |
|-------------------|---------------------|-----------|
| ps32Id            | 消息通信 ID 指针。  | 输出      |
| pszServiceName    | 服务名称指针。      | 输入      |
| pfnMessageHandle  | 消息处理回调函数。  | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_connect](#214-kd_ipcmsg_connect)

[kd_ipcmsg_disconnect](#215-kd_ipcmsg_disconnect)

#### 2.1.4 kd_ipcmsg_connect

【描述】

阻塞方式建立连接

【语法】

k_s32 kd_ipcmsg_connect(k_s32\* ps32Id, const k_char\* pszServiceName, [k_ipcmsg_handle_fn_ptr](#316-k_ipcmsg_handle_fn_ptr) pfnMessageHandle);

【参数】

| **参数名称**           | **描述**                | **输入/输出** |
|-------------------|---------------------|-----------|
| ps32Id            | 消息通信 ID 指针。  | 输出      |
| pszServiceName    | 服务名称指针。      | 输入      |
| pfnMessageHandle  | 消息处理函数。      | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_try_connect](#213-kd_ipcmsg_try_connect)

[kd_ipcmsg_disconnect](#215-kd_ipcmsg_disconnect)

#### 2.1.5 kd_ipcmsg_disconnect

【描述】

断开连接

【语法】

k_s32 kd_ipcmsg_disconnect(k_s32 s32Id);

【参数】

| **参数名称**   | **描述**           | **输入/输出** |
|-----------|----------------|-----------|
| s32Id     | 消息通信 ID。  | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_try_connect](#213-kd_ipcmsg_try_connect)

[kd_ipcmsg_connect](#214-kd_ipcmsg_connect)

#### 2.1.6 kd_ipcmsg_is_connect

【描述】

消息通信是否连接状态。

【语法】

k_bool kd_ipcmsg_is_connect(k_s32 s32Id);

【参数】

| **参数名称**   | **描述**           | **输入/输出** |
|-----------|----------------|-----------|
| s32Id     | 消息通信 ID。  | 输入      |

【返回值】

| **返回值**    | **描述**         |
|----------|--------------|
| K_TRUE   | 连接状态。   |
| K_FALSE  | 非连接状态。 |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

#### 2.1.7 kd_ipcmsg_send_only

【描述】

仅发送消息给对端，不接收对端的返回值

【语法】

k_s32 kd_ipcmsg_send_only(k_s32 s32Id, [k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s) *pstRequest);

【参数】

| **参数名称**     | **描述**                | **输入/输出** |
|-------------|---------------------|-----------|
| s32Id       | 消息服务 ID。       | 输入      |
| pstRequest  | 消息结构体的指针。  | 输入      |

【返回值】

| **返回值**  | **描述**                        |
|-------------|---------------------------------|
| 0           | 成功。                          |
| 非 0        | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

#### 2.1.8 kd_ipcmsg_send_async

【描述】

发送异步消息。这个接口是非阻塞接口，发送消息到对端后就返回了，不会等待消息命令的处理过程。

如果调用此接口发送回复消息，则不需要对端回复，否则对端必须回复

【语法】

k_s32 kd_ipcmsg_send_async(k_s32 s32Id, [k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)* pstMsg, k_ipcmsg_resphandle_fn_ptr pfnRespHandle);

【参数】

| **参数名称**        | **描述**                                                                   | **输入/输出** |
|----------------|------------------------------------------------------------------------|-----------|
| s32Id          | 消息服务 ID。                                                          | 输入      |
| pstMsg         | 消息指针。                                                             | 输入      |
| pfnRespHandle  | 消息回复处理函数。在发送回复消息时可以为 NULL，其他情况不允许为 NULL。 | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

#### 2.1.9 kd_ipcmsg_send_sync

【描述】

发送同步消息。这个接口会阻塞等待对端消息命令处理完成后再返回。

【语法】

k_s32 kd_ipcmsg_send_sync(k_s32 s32Id, [k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)* pstMsg, [k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)** ppstMsg, k_s32 s32TimeoutMs);

【参数】

| **参数名称**       | **描述**                    | **输入/输出** |
|---------------|-------------------------|-----------|
| s32Id         | 消息服务 ID。           | 输入      |
| pstMsg        | 消息指针。              | 输入      |
| ppstMsg       | 回复消息的指针的指针。  | 输出      |
| s32TimeoutMs  | 超时时间。单位：ms。    | 输入      |

【返回值】

| **返回值**   | **描述**                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为[错误码](#41-ipcmsg) |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

本接口超时的情况下，内部会调用 [kd_ipcmsg_destory_message](#2113-kd_ipcmsg_destroy_message)将*ppstMsg（回复消

息）销毁一次，由于同一个消息不能重复销毁，所以本接口超时退出后不必再做销毁

回复消息的处理

【举例】

无

【相关主题】

#### 2.1.10 kd_ipcmsg_run

【描述】

消息处理函数

【语法】

k_void kd_ipcmsg_run(k_s32 s32Id);

【参数】

| **参数名称**   | **描述**           | **输入/输出** |
|-----------|----------------|-----------|
| s32Id     | 消息服务 ID。  | 输入      |

【返回值】

| **返回值**   | **描述** |
|---------|------|
| void    | 无   |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

#### 2.1.11 kd_ipcmsg_create_message

【描述】

创建消息

【语法】

[k_ipcmsg_message_s *](#315-k_ipcmsg_messsage_s)kd_ipcmsg_create_message(k_u32 u32Module, k_u32 u32CMD, k_void*
pBody, k_u32 u32BodyLen);

【参数】

| **参数名称**     | **描述**                                                       | **输入/输出** |
|-------------|------------------------------------------------------------|-----------|
| u32Module   | 模块 ID。由用户创建，用于区分不同模块的不同消息。          | 输入      |
| u32CMD      | u32CMD 命令 ID。由用户创建，用于区分同一模块下的不同命令。 | 输入      |
| pBody       | 消息体指针                                                 | 输入      |
| u32BodyLen  | 消息体大小                                                 | 输入      |

【返回值】

| **返回值**                 | **描述**             |
|-----------------------|------------------|
| k_ipcmsg_message_s*  | 消息结构体指针。 |
| null                  | 消息创建失败     |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_destory_message](#2113-kd_ipcmsg_destroy_message)

#### 2.1.12 kd_ipcmsg_create_resp_message

【描述】

创建回复消息

【语法】

[k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)\* kd_ipcmsg_create_resp_message([k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)\* pstRequest, k_s32 s32RetVal, k_void* pBody, k_u32 u32BodyLen);

【参数】

| **参数名称**     | **描述**                    | **输入/输出** |
|-------------|-------------------------|-----------|
| pstRequest  | 请求消息的指针。        | 输入      |
| s32RetVal   | 回复返回值。            | 输入      |
| pBody       | 回复消息的消息体指针。  | 输入      |
| u32BodyLen  | 回复消息的消息体大小。  | 输入      |

【返回值】

| **返回值**                 | **描述**             |
|-----------------------|------------------|
| k_ipcmsg_message_s*  | 消息结构体指针。 |
| null                  | 消息创建失败     |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

无

【举例】

无

【相关主题】

[kd_ipcmsg_destory_message](#2113-kd_ipcmsg_destroy_message)

#### 2.1.13 kd_ipcmsg_destroy_message

【描述】

销毁消息

【语法】

k_void kd_ipcmsg_destroy_message([k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)* pstMsg);

【参数】

| **参数名称**   | **描述**        | **输入/输出** |
|-----------|-------------|-----------|
| pstMsg    | 消息指针。  | 输入      |

【返回值】

| **返回值**   | **描述** |
|---------|------|
| k_void  | 无   |

【芯片差异】

无

【需求】

- 头文件：k_comm_ipcmsg.h k_ipcmsg.h
- 库文件：libipcmsg.a

【注意】

不支持同一个消息重复销毁，否则会导致系统异常。

【举例】

无

【相关主题】

[kd_ipcmsg_create_message](#2111-kd_ipcmsg_create_message)

[kd_ipcmsg_create_resp_message](#2112-kd_ipcmsg_create_resp_message)

### 2.2 DATAFIFO

该功能模块提供以下API：

- [kd_datafifo_open](#221-kd_datafifo_open)
- [kd_datafifo_open_by_addr](#222-kd_datafifo_open_by_addr)
- [kd_datafifo_close](#223-kd_datafifo_close)
- [kd_datafifo_read](#224-kd_datafifo_read)
- [kd_datafifo_write](#225-kd_datafifo_write)
- [kd_datafifo_cmd](#226-kd_datafifo_cmd)

#### 2.2.1 kd_datafifo_open

【描述】

打开数据通路。

【语法】

k_s32 kd_datafifo_open([k_datafifo_handle](#321-k_datafifo_handle)\* Handle, [k_datafifo_params_s](#325-k_datafifo_params_s)\* pstParams)

【参数】

| **参数名称**    | **描述**                | **输入/输出** |
|------------|---------------------|-----------|
| Handle     | 数据通路句柄。      | 输出      |
| pstParams  | 数据通路参数指针。  | 输入      |

【返回值】

| **返回值**   | **描述**                                |
|---------|-------------------------------------|
| 0       | 成功。                              |
| 非 0    | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】

无

【举例】

无

#### 2.2.2 kd_datafifo_open_by_addr

【描述】

通过物理地址打开数据通路。

【语法】

k_s32 kd_datafifo_open_by_addr([k_datafifo_handle](#321-k_datafifo_handle) \*Handle, [k_datafifo_params_s](#325-k_datafifo_params_s) *pstParams, k_u64 u64Phyaddr)

【参数】

| **参数名称**     | **描述**                  | **输入/输出** |
|-------------|-----------------------|-----------|
| Handle      | 数据通路句柄。        | 输出      |
| pstParams   | 数据通路参数指针。    | 输入      |
| u32PhyAddr  | 数据缓存的物理地址。  | 输入      |

【返回值】

| **返回值**   | **描述**                                |
|---------|-------------------------------------|
| 0       | 成功。                              |
| 非 0    | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】

无

【举例】

无

#### 2.2.3 kd_datafifo_close

【描述】

关闭数据通路。

【语法】

k_s32 kd_datafifo_close([k_datafifo_handle](#321-k_datafifo_handle) Handle)

【参数】

| **参数名称**   | **描述**            | **输入/输出** |
|-----------|-----------------|-----------|
| Handle    | 数据通路句柄。  | 输入      |

【返回值】

| **返回值**   | **描述**                                |
|---------|-------------------------------------|
| 0       | 成功。                              |
| 非 0    | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】

关闭 DataFifo 的时候为了保证读写两端数据正常的释放，用户需要保证读端要读完DataFifo 中存在的数据，写端写完数据后需要额外调用一次[kd_datafifo_write](#225-kd_datafifo_write) (Handle, NULL) 触发写端的数据释放和读指针更新

【举例】

无

#### 2.2.4 kd_datafifo_read

【描述】

读取数据。

【语法】

k_s32 kd_datafifo_read([k_datafifo_handle](#321-k_datafifo_handle) Handle, void** ppData)

【参数】

| **参数名称**   | **描述**                    | **输入/输出** |
|-----------|-------------------------|-----------|
| Handle    | 数据通路句柄。          | 输入      |
| ppData    | 读取的数据指针的指针。  | 输出      |

【返回值】

| **返回值**   | **描述**                                |
|---------|-------------------------------------|
| 0       | 成功。                              |
| 非 0    | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】

无

【举例】

无

#### 2.2.5 kd_datafifo_write

【描述】

写入数据。

【语法】

k_s32 kd_datafifo_write([k_datafifo_handle](#321-k_datafifo_handle) Handle, void* pData)

【参数】

| **参数名称**   | **描述**            | **输入/输出** |
|-----------|-----------------|-----------|
| Handle    | 数据通路句柄。  | 输入      |
| pData     | 写入的数据。    | 输入      |

【返回值】

| **返回值**   | **描述**                                |
|---------|-------------------------------------|
| 0       | 成功。                              |
| 非 0    | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】
当 pData 为 NULL 时，触发写端的数据释放回调函数，同时更新写端的读尾指针。

【举例】

无

#### 2.2.6 kd_datafifo_cmd

【描述】

其他操作。

【语法】

k_s32 kd_datafifo_cmd([k_datafifo_handle](#321-k_datafifo_handle) Handle, [k_datafifo_cmd_e](#326-k_datafifo_cmd_e) enCMD, void* pArg)

【参数】

| **参数名称**   | **描述**                  | **输入/输出** |
|-----------|-----------------------|-----------|
| Handle    | 数据通路句柄。        | 输入      |
| enCMD     | 操作命令。            | 输入      |
| pArg      | 参数，详见【注意】。  | **输入/输出** |

【返回值】

| **返回值**  | **描述**                            |
|-------------|-------------------------------------|
| 0           | 成功。                              |
| 非 0        | 失败，其值为[错误码](#42-datafifo)。 |

【芯片差异】

无

【需求】

- 头文件：k_datafifo.h
- 库文件：libdatafifo.a

【注意】
控制命令和对应参数：

| 命令                                     | 参数以及说明                                                                                                                                                                                               |
|------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DATAFIFO_CMD_GET_PHY_ADDR                | 返回 DATAFIFO 的物理地址，k_u64类型。                                                                                                                                                                      |
| DATAFIFO_CMD_READ_DONE                   | 读端使用完数据后，需要调用这个更新读端的头尾指针。。                                                                                                                                                       |
| DATAFIFO_CMD_WRITE_DONE                  | 写端写完数据后，需要调用这个更新写端的写尾指针。无返回值，参数可以为 NULL。                                                                                                                                |
| DATAFIFO_CMD_SET_DATA_RELEASE \_CALLBACK | 数据释放回调函数。                                                                                                                                                                                         |
| DATAFIFO_CMD_GET_AVAIL_WRITE\_ LEN       | 返回可写入的数据个数，k_u32 类型。 注意：由于需要保留一个数据项辅助buffer 管理，实际可用于缓存数据的长度比配置的 DATAFIFO 的长度u32EntriesNum* u32CacheLineSize）少一个数据项的长度（u32CacheLineSize）。 |
| DATAFIFO_CMD_GET_AVAIL_READ_L EN         | 返回可读取的数据个数，k_u32 类型                                                                                                                                                                           |

【举例】

无

## 3. 数据类型

### 3.1 IPCMSG

该模块有如下数据类型

- [K_IPCMSG_MAX_CONTENT_LEN](#311-k_ipcmsg_max_content_len)
- [K_IPCMSG_PRIVDATA_NUM](#312-k_ipcmsg_privdata_num)
- [K_IPCMSG_INVALID_MSGID](#313-k_ipcmsg_invalid_msgid)
- [k_ipcmsg_connect_s](#314-k_ipcmsg_connect_s)
- [k_ipcmsg_message_s](#315-k_ipcmsg_messsage_s)
- [k_ipcmsg_handle_fn_ptr](#316-k_ipcmsg_handle_fn_ptr)

#### 3.1.1 K_IPCMSG_MAX_CONTENT_LEN

【说明】

定义消息体最长度。

【定义】

```C
#define K_IPCMSG_MAX_CONTENT_LEN (1024)
```

【注意事项】

无

【相关数据类型及接口】

无

该模块有如下数据类型

#### 3.1.2 K_IPCMSG_PRIVDATA_NUM

【说明】

定义消息体中私有数据最大个数。

【定义】

```C
#define K_IPCMSG_MAX\_ PRIVDATA_NUM (8)
```

【注意事项】

无

【相关数据类型及接口】

无

#### 3.1.3 K_IPCMSG_INVALID_MSGID

【说明】

定义无效消息 ID。

【定义】

```C
#define K_IPCMSG_INVALID_MSGID (0xFFFFFFFFFFFFFFFF)
```

【注意事项】

无

【相关数据类型及接口】

无

#### 3.1.4 k_ipcmsg_connect_s

【说明】

定义模块 ID 枚举类型。

【定义】

```C

typedef struct IPCMSG_CONNECT_S

{

k_u32 u32RemoteId;

k_u32 u32Port;

k_u32 u32Priority;

} k_ipcmsg_connect_s;
```

【成员】

| **成员名称** | **描述**                                                             |
|--------------|----------------------------------------------------------------------|
| u32RemoteId  | 标示连接远端 CPU 的枚举值。 0：小核； 1：大核                        |
| u32Port      | 消息通信用的自定义 port 号 取值范围：\[0, 512\]                        |
| u32Priority  | 消息传递的优先级。 取值范围： 0：普通优先级； 1：高优先级。 默认为 0 |

【注意事项】

无

【相关数据类型及接口】

[kd_ipcmsg_add_service](#211-kd_ipcmsg_add_service)

#### 3.1.5 k_ipcmsg_messsage_s

【说明】

定义消息结构体。

【定义】

``` C

typedef struct IPCMSG_MESSAGE_S

{

k_bool bIsResp; /**<Identify the response messgae*/

k_u64 u64Id; /**<Message ID*/

k_u32 u32Module; /**<Module ID, user-defined*/

k_u32 u32CMD; /**<CMD ID, user-defined*/

k_s32 s32RetVal; /**<Retrun Value in response message*/

k_s32 as32PrivData[K_IPCMSG_PRIVDATA_NUM]; /**<Private data, can be modify directly after ::kd_ipcmsg_create_message or ::kd_ipcmsg_create_resp_message*/

void* pBody; /**<Message body*/

k_u32 u32BodyLen; /**<Length of pBody*/

} k_ipcmsg_message_t;
```

【成员】

| **成员名称**     | **描述**                                                      |
|---------------|-----------------------------------------------------------|
| bIsResp       | 标示该消息是否回复消息： K_TURE：回复； K_FALSE：不回复。 |
| u64Id         | 消息 ID。                                                 |
| u32Module     | 模块 ID。                                                 |
| u32CMD        | CMD ID。                                                  |
| s32RetVal     | 返回值。                                                  |
| as32PrivData  | 私有数据。                                                |
| pBody         | 消息体指针。                                              |
| u32BodyLen    | 消息体长度，单位字节                                      |

【注意事项】

无

【相关数据类型及接口】

- [kd_ipcmsg_send_only](#217-kd_ipcmsg_send_only)
- [kd_ipcmsg_send_async](#218-kd_ipcmsg_send_async)
- [kd_ipcmsg_send_sync](#219-kd_ipcmsg_send_sync)
- [kd_ipcmsg_create_message](#2111-kd_ipcmsg_create_message)
- [kd_ipcmsg_create_resp_message](#2112-kd_ipcmsg_create_resp_message)
- [kd_ipcmsg_destory_message](#2113-kd_ipcmsg_destroy_message)

#### 3.1.6 k_ipcmsg_handle_fn_ptr

【说明】

定义消息回复处理函数

【定义】

```C
typedef void (*k_ipcmsg_handle_fn_ptr)(k_s32 s32Id, k_ipcmsg_message_s* pstMsg);
```

【成员】

| **成员名称** | **描述**   |
|--------------|------------|
| s32Id        | 消息服务ID |
| pstMsg       | 消息体指针 |

【注意事项】

无

【相关数据类型及接口】

- [kd_ipcmsg_try_connect](#213-kd_ipcmsg_try_connect)
- [kd_ipcmsg_connect](#214-kd_ipcmsg_connect)

### 3.2 DATAFIFO

本模块有以下数据结构

- [k_datafifo_handle](#321-k_datafifo_handle)
- [K_DATAFIFO_INVALID_HANDLE](#322-k_datafifo_invalid_handle)
- [K_DATAFIFO_RELEASESTREAM_FN_PTR](#323-k_datafifo_releasestream_fn_ptr)
- [K_DATAFIFO_OPEN_MODE_E](#324-k_datafifo_open_mode_e)
- [k_datafifo_params_s](#325-k_datafifo_params_s)
- [k_datafifo_cmd_e](#326-k_datafifo_cmd_e)

#### 3.2.1 k_datafifo_handle

【说明】

定义DATAFIFO句柄

【定义】

```C
typedef K_U32 K_DATAFIFO_HANDLE;
```

【成员】

| **成员名称** | **描述**   |
|--------------|------------|
| s32Id        | 消息服务ID |
| pstMsg       | 消息体指针 |

【注意事项】

无

【相关数据类型及接口】

无

#### 3.2.2 K_DATAFIFO_INVALID_HANDLE

【说明】

定义数据通路无效句柄。

【定义】

```C
#define K_DATAFIFO_INVALID_HANDLE (-1)
```

【注意事项】

无

【相关数据类型及接口】

无

#### 3.2.3 K_DATAFIFO_RELEASESTREAM_FN_PTR

【说明】

定义数据通路码流释放函数。。

【定义】

```C
typedef void (*K_DATAFIFO_RELEASESTREAM_FN_PTR)(void* pStream);
```

【注意事项】

无

【相关数据类型及接口】

无

#### 3.2.4 K_DATAFIFO_OPEN_MODE_E

【说明】

定义数据通路打开模式。

【定义】

```C

typedef struct k_DATAFIFO_PARAMS_S

{

k_u32 u32EntriesNum; /**< The number of items in the ring buffer*/

k_u32 u32CacheLineSize; /**< Item size*/

k_bool bDataReleaseByWriter; /**<Whether the data buffer release by writer*/

K_DATAFIFO_OPEN_MODE_E enOpenMode; /**<READER or WRITER*/

} k_datafifo_params_s;
```

【成员】

| **成员名称**    | **描述**             |
|-----------------|----------------------|
| DATAFIFO_READER | 读出角色，只读取数据 |
| DATAFIFO_WRITER | 写入角色，只写入数据 |

【注意事项】

无

【相关数据类型及接口】

无

#### 3.2.5 k_datafifo_params_s

【说明】

定义数据通路配置参数

【定义】

```C
typedef struct k_DATAFIFO_PARAMS_S

{

k_u32 u32EntriesNum; /**< The number of items in the ring buffer*/

k_u32 u32CacheLineSize; /**< Item size*/

k_bool bDataReleaseByWriter; /**<Whether the data buffer release by writer*/

K_DATAFIFO_OPEN_MODE_E enOpenMode; /**<READER or WRITER*/

} k_datafifo_params_s;
```

【成员】

| **成员名称**          | **描述**                 |
|-----------------------|--------------------------|
| u32EntriesNum         | 循环 Buffer 的数据个数。 |
| u32CacheLineSize      | 每个数据项的大小。       |
| bDataReleaseByWriter  | 是否需要写入者释放数据。 |
| enOpenMode            | 打开通路的角色。         |

【注意事项】

u32EntriesNum 和 u32CacheLineSize 并没有做取值范围做限制，只要 MMZ 内存足够大，DATAFIFO 就可以创建成功。因此，需要用户保证这 2 个参数在合理的范围之内。

【相关数据类型及接口】

无

#### 3.2.6 k_datafifo_cmd_e

【说明】

定义数据通路的控制类型

【定义】

```C
typedef enum k_DATAFIFO_CMD_E

{

DATAFIFO_CMD_GET_PHY_ADDR, /**<Get the physic address of ring buffer*/

DATAFIFO_CMD_READ_DONE, /**<When the read buffer read over, the reader should call this function to notify the writer*/

DATAFIFO_CMD_WRITE_DONE, /**<When the writer buffer is write done, the writer should call this function*/

DATAFIFO_CMD_SET_DATA_RELEASE_CALLBACK, /**<When bDataReleaseByWriter is K_TRUE, the writer should call this to register release callback*/

DATAFIFO_CMD_GET_AVAIL_WRITE_LEN, /**<Get available write length*/

DATAFIFO_CMD_GET_AVAIL_READ_LEN /**<Get available read length*/

} k_datafifo_cmd_e;
```

【成员】

| **成员名称**                                | **描述**                                                                                                                                                                                                        |
|------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| DATAFIFO_CMD_GET_PHY_ADDR                | 返回 DATAFIFO 的物理地址，k_u64类型。                                                                                                                                                                       |
| DATAFIFO_CMD_READ_DONE                   | 读端使用完数据后，需要调用这个更新读端的头尾指针。。                                                                                                                                                        |
| DATAFIFO_CMD_WRITE_DONE                  | 写端写完数据后，需要调用这个更新写端的写尾指针。无返回值，参数可以为 NULL。                                                                                                                                 |
| DATAFIFO_CMD_SET_DATA_RELEASE \_CALLBACK | 数据释放回调函数。                                                                                                                                                                                          |
| DATAFIFO_CMD_GET_AVAIL_WRITE\_ LEN       | 返回可写入的数据个数，k_u32 类型。 注意：由于需要保留一个数据项辅助buffer 管理，实际可用于缓存数据的长度比配置的 DATAFIFO 的长度u32EntriesNum* u32CacheLineSize） 少一个数据项的长度（u32CacheLineSize）。 |
| DATAFIFO_CMD_GET_AVAIL_READ_L EN         | 返回可读取的数据个数，k_u32 类型                                                                                                                                                                            |

【注意事项】

无

【相关数据类型及接口】

无

## 4. 错误码

### 4.1 IPCMSG

表 41

| 错误代码    | 宏定义              | **描述**         |
|-------------|---------------------|--------------|
| 0x1901      | K_IPCMSG_EINVAL     | 配置参数无效 |
| 0x1902      | K_IPCMSG_ETIMEOUT   | 超时错误     |
| 0x1903      | K_IPCMSG_ENOOP      | 驱动打开失败 |
| 0x1904      | K_IPCMSG_EINTER     | 内部错误     |
| 0x1905      | K_IPCMSG_ENULL_PTR  | 空指针错误   |
| 0x00000000  | K_SUCCESS           | 成功         |
| 0xFFFFFFFF  | K_FAILURE           | 失败         |
| 0x1901      | K_IPCMSG_EINVAL     | 配置参数无效 |
| 0x1902      | K_IPCMSG_ETIMEOUT   | 超时错误     |

### 4.2 DATAFIFO

表 42

| 错误代码    | 宏定义                           | **描述**         |
|-------------|----------------------------------|--------------|
| 0x1A01      | K_DATAFIFO_ERR_EINVAL_PARAM ETER | 配置参数无效 |
| 0x1A02      | K_DATAFIFO_ERR_NULL_PTR          | 空指针错误   |
| 0x1A03      | K_DATAFIFO_ERR_NOMEM             | 分配内存失败 |
| 0x1A04      | K_DATAFIFO_ERR_DEV_OPT           | 设备操作失败 |
| 0x1A05      | K_DATAFIFO_ERR_NOT_PERM          | 操作不允许   |
| 0x1A06      | K_DATAFIFO_ERR_NO_DATA           | 无可读取数据 |
| 0x1A07      | K_DATAFIFO_ERR_NO_SPACE          | 无可写入空间 |
| 0x1A08      | K_DATAFIFO_ERR_READ              | 读错误       |
| 0x1A09      | K_DATAFIFO_ERR_WRITE             | 写错误       |
| 0x00000000  | K_SUCCESS                        | 成功         |
| 0xFFFFFFFF  | K_FAILURE                        | 失败         |

## 5. 调试信息

### 5.1 ipcm

【调试信息】

``` text
msh /bin\>cat /proc/ipcm

*---REMOTE NODE: ID=0, STATE: READY

\|-RECV BUFFER, PHYS\<0x0000000000180000, 0x00079000\>

\|-SEND BUFFER, PHYS\<0x0000000000100000, 0x00080000\>

\|-Port \| State \| Send Count \| Recv Count \| Max Send Len \| Max Recv Len

1 Connected 15 15 320 608

*---LOCAL NODE: ID=1, STATE: ALIVE
```

【调试信息分析】

记录当前ipcm模块的使用情况

【参数说明】

| **参数**         | **描述**          |                            |
|--------------|---------------|----------------------------|
| REMOTE NODE  | ID            | 远端处理器的ID号           |
|              | STATE         | 远端处理器的状态。         |
|              | RECV BUFFER   | 接收buffer的物理地址区间   |
|              | SEND BUFFER   | 发送buffer的物理地址区间。 |
|              | Port          | 端口号                     |
|              | State         | 端口连接状态               |
|              | Send Count    | 发送次数                   |
|              | Recv Count    | 接收次数                   |
|              | Max Send len  | 最大发送的数据长度         |
|              | Max Recv len  | 最大接收的数据长度         |
