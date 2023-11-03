# K230 SHA256 API Reference

![cover](../../../../zh/01_software/board/mpp/images/canaan-cover.png)

Copyright 2023 Canaan Inc. ©

<div style="page-break-after:always"></div>

## Disclaimer

The products, services or features you purchase should be subject to Canaan Inc. ("Company", hereinafter referred to as "Company") and its affiliates are bound by the commercial contracts and terms and conditions of all or part of the products, services or features described in this document may not be covered by your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied representations or warranties as to the correctness, reliability, completeness, merchantability, fitness for a particular purpose and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is intended as a guide for use only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Notice

![The logo](../../../../zh/01_software/board/mpp/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Canaan Inc. and its affiliates. All other trademarks or registered trademarks that may be mentioned in this document are owned by their respective owners.

**Copyright 2023 Canaan Inc.. © All Rights Reserved.**
Without the written permission of the company, no unit or individual may extract or copy part or all of the content of this document without authorization, and shall not disseminate it in any form.

<div style="page-break-after:always"></div>

## Directory

[TOC]

## Preface

### Overview

This document mainly introduces the use of K230 SHA256 software, including the use of SHA256 API and test procedures.

### Reader Object

This document (this guide) is intended primarily for:

- Technical Support Engineer
- Software Development Engineer

### Definition of Acronyms

| abbreviation    | illustrate |
| ----    | ---- |
| SHA256  | Secure Hash Algorithm   |

### Revision History

| Document version number | Modify the description | Author     | date       |
| ---------- | -------- | ---------- | ---------- |
| V1.0       | Initial edition     | Yang Fan          | 2023-05-30 |

## 1. Function Introduction

SHA256 is mainly used to calculate the hash value of data, and the SHA256 algorithm is implemented in the big core rt-smart to calculate the hash value of data, and the code logic is shown in the following figure:

![sha256](../../../../zh/01_software/board/mpp/images/sha256.png)

## 2. API Reference

The SHA256 module mainly provides the following APIs:

- [kd_mpi_cipher_sha256](#21-kd_mpi_cipher_sha256)

### 2.1 kd_mpi_cipher_sha256

【Description】

Calculates the hash value of the message based on the incoming message.

【Syntax】

kd_mpi_cipher_sha256(const void \*data, k_u32 len, k_u8 \*hash);

【Parameters】

| Parameter name        | description                          | Input/output |
|-----------------|-------------------------------|-----------|
| data            | Incoming messages                      | input      |
| only            | The length of the incoming message                    | input      |
| hash            | The calculated hash value               | output      |

【Return value】

| Return value  | description                            |
|---------|---------------------------------|
| 0       | Succeed.                          |
| Non-0    | Failed, refer to Error Code Definition |

【Differences】

None

【Requirement】

- Header file: mpi_cipher_api.h
- Library file: libcipher.a

【Note】

None

【Example】

None

【See Also】

None

## 3. Debugging and Printing Information

Write a user-mode application *sample_cipher.c* to test SHA256 functionality.

The test code has been written, located in the *mpp/userapps/sample/sample_cipher* directory, the specific debugging method is as follows:

1. After the big core starts, go to the *bin* directory;
1. Run the *sample_cipher.elf* program;
1. Print the information.

The specific printing information is as follows:

```shell
msh />cd bin/
msh /bin>./sample_cipher.elf
input = ''
digest: e3b0c442 98fc1c14 9afbf4c8 996fb924 27ae41e4 649b934c a495991b 7852b855
result: PASS

input = 'abc'
digest: ba7816bf 8f01cfea 414140de 5dae2223 b00361a3 96177a9c b410ff61 f20015ad
result: PASS

input = 'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq'
digest: 248d6a61 d20638b8 e5c02693 0c3e6039 a33ce459 64ff2167 f6ecedd4 19db06c1
result: PASS

input = 'The quick brown fox jumps over the lazy dog'
digest: d7a8fbb3 07d78094 69ca9abc b0082e4f 8d5651e4 6d3cdb76 2d02d0bf 37c9e592
result: PASS

input = 'The quick brown fox jumps over the lazy cog'
digest: e4c4d8f3 bf76b692 de791a17 3e053211 50f7a345 b46484fe 427f6acc 7ecc81be
result: PASS

input = 'bhn5bjmoniertqea40wro2upyflkydsibsk8ylkmgbvwi420t44cq034eou1szc1k0mk46oeb7ktzmlxqkbte2sy'
digest: 9085df2f 02e0cc45 5928d0f5 1b27b4bf 1d9cd260 a66ed1fd a11b0a3f f5756d99
result: PASS
```
