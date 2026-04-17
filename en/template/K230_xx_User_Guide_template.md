# K230 xx User Guide

## Overview

This document introduces xxx, etc.

## xx Module Introduction

### xx Module

#### Introduction to xx Module

xxx

#### Feature Description

xx includes.

#### Dependent Resources

Requires a screen

## Markdown Syntax Reference (Delete when completing the document)

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
