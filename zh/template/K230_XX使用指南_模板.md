# K230 xx使用指南

## 概述

此文档介绍xxx等。

## xx模块介绍

### xx模块

#### xx模块简介

xxx

#### Feature说明

xx 包含了。

#### 依赖资源

需要屏幕

## Markdown语法参考（完成文档时删除）

### 插入图片

语法

```markdown
![图片描述](图片相对路径)
```

Example：
![logo](./images/logo.png)

### 插入表格

| Column1  |Column2  | Column3  |
|  -       |-         |-         |
|  Cell1   |  Cell2   |  Cell3   |
|  Cell4   |  Cell5   |  Cell6   |
|  Cell7   |  Cell8   |  Cell9   |

### 斜体&加粗

*斜体*   **加粗**

### 插入网页链接

```markdown
[链接文字](https://www.zhihu.com/question/20409634/answer/90728572)
```

### 图片链接

```markdown
![文字描述](图片链接地址)
```

### 引用文字

>这里是引用文字

### 插入代码

语法：

```语言
 Code
 Code
```

Example：

```Python
 #!/usr/bin/env python3
 print("Hello, World!")
```

### 分割线

---

### 有序列表

1. 条目1
    (1) 条目1
    (2) 条目2
    (3) 条目3
1. 条目2
1. 条目3

### 无序列表

- 条目1
- 条目2

### 显示符号本身

\+
\-
\*
\!
\!

### 注意/提示

**注意/提示：**
>注意内容

### API描述

#### kd_xxx_func

【描述】

示例API

【语法】

```c
k_s32 kd_xxx_func(k_s32 a)
```

【参数】

| 参数名称        | 描述                          | 输入/输出 |
|-----------------|-------------------------------|-----------|
| a  | 示例参数            | 输入      |

【返回值】

| 返回值  | 描述                            |
|---------|---------------------------------|
| 0       | 成功。                          |
| 非 0    | 失败，其值为\[错误码\] |

【芯片差异】

无

【需求】

- 头文件：k_xxx.h
- 库文件：libxxx.a

【注意】
无

【举例】

无

【相关主题】

无

## 数据结构描述

### k_xxx_type

【说明】

示例数据结结构

【定义】

```c
typedef struct
{
  int a;
} k_xxx_type
```

【注意事项】

无

【相关数据类型及接口】

无

## 调试及打印信息

``` shell
haohaibo@develop:/proc$ cat /proc/version
Linux version 5.4.0-139-generic (buildd@lcy02-amd64-112) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #156-Ubuntu SMP Fri Jan 20 17:27:18 UTC 2023
```
