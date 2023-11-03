# K230 xx User Guide

![cover](../images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## Preface

### Overview

This document mainly introduces xxx.

### Reader object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of acronyms

| abbreviation | illustrate |
| ---- | ---- |
| XXX  | xx   |
| XXX  | xx   |

### Revision history

| Document version number |  Author| Modify the description  | date       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | first edition     | System Software Department | 2023-03-10 |
| V1.1       |          |            |            |
| V1.2       |          |            |            |

## 1. Overview

This document describes xxx and more.

## Introduction to the 2.xx module

### 2.1 xx module

#### 2.1.1 Introduction to xx modules

xxx

#### 2.1.2 Feature description

xx contains:

#### 2.1.3 Dependent Resources

A screen is required

## 3. Markdown syntax reference (removed when completing the document)

### Insert a picture

grammar

```markdown
![image description](image path)
```

Example：
![logo](../images/logo.png)

### Insert a table

| Column1  |Column2  | Column3  |
|  -       |-         |-         |
|  Cell1   |  Cell2   |  Cell3   |
|  Cell4   |  Cell5   |  Cell6   |
|  Cell7   |  Cell8   |  Cell9   |

### Italic & bold

*Italics* **Bold**

### Insert a web link

```markdown
[link text](https://www.zhihu.com/question/20409634/answer/90728572)
```

### Image link

```markdown
![text description](Link address of the image )
```

### Quote text

>Here is the quote

### Insert code

Grammar:

```language
 Code
 Code
```

Example：

```Python
 #!/usr/bin/env python3
 print("Hello, World!")
```

### Dividing line

---

### Ordered list

1. Article 1
    (1) Article 1
    (2) Article 2
    (3) Article 3
1. Entry 2
1. Entry 3

### Unordered list

- Entry 1
- Entry 2

### Displays the symbol itself

\+
\-
\*
\!
\!

### Attention/Tips

**Notes/Tips:**
>Pay attention to the content

### API description

#### kd_xxx_func

【Description】

Sample API

【Syntax】

```c
k_s32 kd_xxx_func(k_s32 a)
```

【Parameters】

| Parameter name        | description                          | Input/output |
|-----------------|-------------------------------|-----------|
| a  | Example parameters            | input      |

【Return value】

| Return value  | description                            |
|---------|---------------------------------|
| 0       | Succeed.                          |
| Non-0    | Failed with value \[error code\] |

【Difference】

none

【Requirement】

- Header file: k_xxx.h
- Library file: libxxx.a

【Note】

none

【Example】

none

【See Also】

none

## Data structure description

### k_xxx_type

【Description】

Sample data junction structure

【Syntax】

```c
typedef struct
{
  int a;
} k_xxx_type
```

【Member】

|Meber  | Description                            |
|---------|---------------------------------|
| a       | xxx.                          |

【Note】

none

【See Also】

none

## Debugging and printing information

``` shell
root@develop:/proc$ cat /proc/version
Linux version 5.4.0-139-generic (buildd@lcy02-amd64-112) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #156-Ubuntu SMP Fri Jan 20 17:27:18 UTC 2023
```
