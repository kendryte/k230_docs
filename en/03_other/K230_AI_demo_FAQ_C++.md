# K230 AI Demo Frequently Asked Questions (C++)

![cover](../../zh/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not provide any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../zh/images/logo.png), "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may extract, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## 1 TF Boot Failed with Exit Code 13

Problem: TF card boot reports a "boot failed with exit code 13" error.

Solution: The reasons are as follows: 1. There is an error in the files within the boot medium. 2. Incorrect boot pin settings.

Special note on TF card boot pin settings: The TF card will only boot when the levels of the two boot pins are high (they need to be set to positions 1 and 2 as per the silkscreen, which is the opposite direction of ON).
