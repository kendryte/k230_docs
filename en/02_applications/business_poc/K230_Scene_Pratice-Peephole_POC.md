# K230 Practical Scenario - Maoyan POC

![cover](../../../zh/02_applications/business_poc/images/canaan-cover.png)

Copyright © 2023 Beijing Canaan Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Information Technology Co., Ltd. ("the Company", hereinafter) and its affiliates. All or part of the products, services, or features described in this document may not fall within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not make any express or implied statements or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, and non-infringement of any representations, information, or content in this document. Unless otherwise agreed, this document is for reference only.

Due to product version upgrades or other reasons, the content of this document may be updated or modified from time to time without any notice.

## Trademark Statement

![logo](../../../zh/02_applications/business_poc/images/logo.png) "Canaan" and other Canaan trademarks are trademarks of Beijing Canaan Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## K230 Maoyan

A product-grade program developed on the K230 platform that integrates UI, video intercom, and human detection functions. The Maoyan product supports both remote and local peephole functionalities, where the remote peephole allows interaction between the peephole device and a remote mobile device.

### Hardware Environment

- K230-USIP-LP3-EVB-V1.0/K230-USIP-LP3-EVB-V1.1 * 2 units
- Matching LCD modules * 2 units
- K230-USIP-IMX335-SENSOR-V1.1 modules * 2 units
- Type-C to Ethernet adapters * 2 units
- One external audio sub-board
- One Ethernet cable

Apart from the external audio sub-board and Ethernet cable, two sets of devices are needed for the remote peephole: one set as the peephole device and one set to simulate the mobile device. The audio sub-board is used on the peephole device end.

![peephole boards](../../../zh/02_applications/business_poc/images/peephole_boards.jpg)

In the above image, the EVB board on the left runs the peephole device end, while the EVB board on the right runs the simulated mobile end. The button functions on the UI interface are as follows:

- Intercom button: Controls the start/cancel of the intercom.
- Voice change button: Controls the enable/cancel of the voice change.
- Playback button: Enters the playback interface to replay recorded videos or captured images.
- Shutdown button: Controls the shutdown of the peephole device end.

## Overview

The Maoyan program, as a POC project, provides a reference for customers on how to use lvgl, big-small core communication, network communication, multimedia pipelines, and AI functions.

Main functions of the program:

1. Simulates two wake-up modes: PIR wake-up and doorbell wake-up.
   - PIR wake-up:
     - The peephole device end performs human detection and captures snapshots for storage.
   - Doorbell wake-up:
     - Supports remote video intercom, local voice intercom, storage, and playback.
1. RTSP network service and RPC service.
1. Big-small core event and data communication.
1. Image capture, video recording, and playback.
1. GUI display.

The program consists of two main parts:

- Peephole device side program: includes both big core and small core programs.
  1. Big core program
     - Mainly handles AI human detection, video input, video/image encoding, audio input and encoding, audio decoding, and output functions.
  1. Small core program
     - Mainly handles UI interface control, audio and video streaming, storage, playback, interaction with mobile devices for video intercom, and local voice intercom functions.

- Mobile device side program: includes only the small core program.
  - The small core program mainly handles the start, end, and voice change functions of video intercom through the UI interface and interaction with the peephole device for video intercom.

## Functional Demonstration

### Doorbell Mode

Peephole Device
Start by long-pressing the button to launch the UI interface. The button functions are as follows:

- Intercom button: Enables/cancels the intercom, used only for local doorbell intercom. The first press after the program runs starts the intercom.
- Voice change button: Controls the enable/cancel of voice change, used only for local doorbell intercom, default is no voice change.
- Playback button: Used for playback, to play locally stored videos and images. (Note: During local intercom, cancel the intercom first before playback)
- Shutdown button: Controls the device shutdown.

The local IP address is displayed above the intercom button.

When the doorbell wakes up the peephole device, the screen displays the video captured by the local camera. Video intercom can be conducted in two ways: local doorbell voice intercom and remote doorbell video intercom.

#### Local Doorbell Voice Intercom

Click the intercom button on the peephole device to start the intercom between inside and outside the door. Connect the headset to the EVB board's onboard headset interface and the sub-board headset interface to hear the sound from the other end.

#### Remote Doorbell Video Intercom

For remote intercom, an additional development board is needed to run the mobile end program. When connected to the device end, the mobile end will pop up a "Connected" message, then disappear, and continue to display the main interface. The three buttons at the bottom have the following functions:

- Intercom button: Controls the enable/cancel of the intercom. After the program runs, a wake-up mode pop-up will appear. Subsequently, this button triggers the intercom, and the first press starts the intercom.
- Voice change button: Controls the enable/cancel of voice change, default is no voice change.
- Shutdown button: Remotely controls the shutdown of the peephole device end.

## Limitations and Notes

1. Currently, only direct network connection tests are supported, with both the mobile end and device end configured with static IPs.
1. After a remote video intercom is disconnected, re-connection is not supported.
1. After playback ends, remote video intercom is not supported.
1. After the doorbell mode starts, storage begins, and the storage format is mp4. Restarting in doorbell mode will overwrite the previous storage.
1. Images captured after human detection in PIR mode can be viewed by waking up the device in doorbell mode and clicking the playback button.
1. The currently configured storage space is 256MB.

## Source Code Location

- The source code for the big core program of the peephole device is located at `k230_sdk/src/reference/business_poc/peephole/big`
- The source code for the small core program of the peephole device is located at `k230_sdk/src/reference/business_poc/peephole/peephole_device`
- The source code for the simulated mobile device program is located at `k230_sdk/src/reference/business_poc/peephole/peephole_phone`

## Compiling the Program

### Peephole Device

The peephole device end needs to be compiled using the peephole device configuration script. The compile command is `make CONF=k230_evb_peephole_device_defconfig`.
**Note that after configuring CONF, subsequent compile commands will use the last CONF even if CONF is not specified. The compile output is located in the `k230_sdk/output/${CONF}` directory.**
The default CONF is `k230_evb_defconfig`.
The generated image is located at `output/k230_evb_peephole_device_defconfig/images/sysimage-spinor32m.img`. Flash this image to automatically run the peephole device end after startup.

### Simulated Mobile Device

You can compile the mobile end image using `make CONF=k230_evb_peephole_phone_defconfig`. The generated image is located at `output/k230_evb_peephole_phone_defconfig/images/sysimage-sdcard.img.gz`. Flash this image to automatically run the simulated mobile end program after startup.

## Running the Program

### Running the Peephole Device End Program

The peephole device end can be started in two ways as shown below.

- Method 1: Toggle the dip switch to `ON` to simulate PIR wake-up.
  - The device will perform the first frame capture, human detection, and capture 10 seconds after detecting a human. Human detection here refers to the whole human body.
  - After starting this mode, you can enter doorbell mode by briefly pressing the doorbell button.
- Method 2: Long press the button to simulate doorbell wake-up.
  - The mic and headset on the EVB board simulate the outside door scene; the mic and headset on the audio sub-board simulate the inside door scene.

![peephole_device](./images/peephole_device.png)

The peephole image is in self-start mode. After flashing the peephole image, short the 1, 2 pins, 13, 14 pins, and 9, 15 pins of J1 as shown below.

![pmu connection](../../../zh/02_applications/business_poc/images/pmu_connection.jpg)

### Running the Simulated Mobile End

After flashing the simulated mobile end image, the mobile end program will automatically run after startup. Once the pop-up message indicates a successful connection, you can control the interaction with the peephole device end through the buttons.
