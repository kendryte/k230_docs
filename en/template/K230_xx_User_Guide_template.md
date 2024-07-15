# K230 xx User Guide

![cover](../../zh/template/images/canaan-cover.png)

Copyright © 2023 Canaan Creative Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Canaan Creative Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any explicit or implied statements or warranties regarding the correctness, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../zh/template/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Canaan Creative Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Canaan Creative Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may extract, copy, or distribute part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly introduces xxx.

### Intended Audience

This document (this guide) is mainly applicable to the following personnel:

- Technical Support Engineers
- Software Development Engineers

### Abbreviation Definitions

| Abbreviation | Description |
| ------------ | ----------- |
| XXX          | xx          |
| XXX          | xx          |

### Revision History

| Document Version | Modification Description | Modifier       | Date       |
| ---------------- | ------------------------ | -------------- | ---------- |
| V1.0             | Initial version          | System Software Dept. | 2023-03-10 |
| V1.1             |                          |                |            |
| V1.2             |                          |                |            |

## 1. Overview

This document introduces xxx, etc.

## 2. xx Module Introduction

### 2.1 xx Module

#### 2.1.1 Introduction to xx Module

xxx

#### 2.1.2 Feature Description

xx includes.

#### 2.1.3 Dependent Resources

Requires a screen

## 3. Markdown Syntax Reference (Delete when completing the document)

### Inserting Images

Syntax

```markdown
![Image Description](Relative Path to Image)
```

Example:
![logo](../../zh/images/logo.png)

### Inserting Tables

| Column1 | Column2 | Column3 |
| ------- | ------- | ------- |
| Cell1   | Cell2   | Cell3   |
| Cell4   | Cell5   | Cell6   |
| Cell7   | Cell8   | Cell9   |

### Italics & Bold

*Italics*   **Bold**

### Inserting Web Links

```markdown
[Link Text](https://www.zhihu.com/question/20409634/answer/90728572)
```

### Image Links

```markdown
![Text Description](Image Link Address)
```

### Quoting Text

> Here is the quoted text

### Inserting Code

Syntax:

```language
 Code
 Code
```

Example:

```Python
 #!/usr/bin/env python3
 print("Hello, World!")
```

### Divider

---

### Ordered List

1. Item 1
    (1) Item 1
    (2) Item 2
    (3) Item 3
1. Item 2
1. Item 3

### Unordered List

- Item 1
- Item 2

### Displaying Symbols Themselves

\+
\-
\*
\!
\!

### Note/Tip

**Note/Tip:**
> Note content

### API Description

#### kd_xxx_func

[Description]

Example API

[Syntax]

```c
k_s32 kd_xxx_func(k_s32 a)
```

[Parameters]

| Parameter Name | Description | Input/Output |
| -------------- | ----------- | ------------ |
| a              | Example parameter | Input      |

[Return Values]

| Return Value | Description |
| ------------ | ----------- |
| 0            | Success.    |
| Non-zero     | Failure, the value is \[error code\] |

[Chip Differences]

None

[Requirements]

- Header file: k_xxx.h
- Library file: libxxx.a

[Note]
None

[Example]

None

[Related Topics]

None

## Data Structure Description

### k_xxx_type

[Description]

Example data structure

[Definition]

```c
typedef struct
{
  int a;
} k_xxx_type
```

[Notes]

None

[Related Data Types and Interfaces]

None

## Debugging and Print Information

```shell
haohaibo@develop:/proc$ cat /proc/version
Linux version 5.4.0-139-generic (buildd@lcy02-amd64-112) (gcc version 9.4.0 (Ubuntu 9.4.0-1ubuntu1~20.04.1)) #156-Ubuntu SMP Fri Jan 20 17:27:18 UTC 2023
```
