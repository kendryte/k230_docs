# K230 ISP Image Tuning Guide

![cover](../../../../zh/01_software/pc/ISP_tuning/images/canaan-cover.png)

Copyright©2023 Beijing Canaan Creative Information Technology Co., Ltd.

<div style="page-break-after:always"></div>

## Disclaimer

The products, services, or features you purchase are subject to the commercial contracts and terms of Beijing Canaan Creative Information Technology Co., Ltd. (hereinafter referred to as "the Company") and its affiliates. All or part of the products, services, or features described in this document may not be within the scope of your purchase or use. Unless otherwise agreed in the contract, the Company does not make any express or implied representations or warranties regarding the accuracy, reliability, completeness, merchantability, fitness for a particular purpose, or non-infringement of any statements, information, or content in this document. Unless otherwise agreed, this document is only for reference as a usage guide.

Due to product version upgrades or other reasons, the content of this document may be updated or modified periodically without any notice.

## Trademark Statement

![logo](../../../../zh/01_software/pc/ISP_tuning/images/logo.png), "Canaan," and other Canaan trademarks are trademarks of Beijing Canaan Creative Information Technology Co., Ltd. and its affiliates. All other trademarks or registered trademarks mentioned in this document are owned by their respective owners.

**Copyright © 2023 Beijing Canaan Creative Information Technology Co., Ltd. All rights reserved.**
Without the written permission of the Company, no unit or individual may excerpt, copy, or disseminate any part or all of the content of this document in any form.

<div style="page-break-after:always"></div>

## Table of Contents

[TOC]

## Preface

### Overview

This document mainly guides users in tuning the K230 ISP for image optimization.

### Target Audience

This document (this guide) is primarily intended for the following personnel:

- Image Debugging Engineers
- Technical Support Engineers
- Software Development Engineers

### Revision History

| Document Version | Modification Description | Editor   | Date       |
|------------------|--------------------------|----------|------------|
| V1.0             | Initial version          | Liu Jia'an| 2023-09-04 |
| V1.1             | Updated some parameter descriptions | Rong Jian | 2024-01-30 |
| V1.2             | Updated some parameter descriptions | Rong Jian | 2024-04-28 |

## 1. Overview of K230 ISP Image Tuning

When tuning images, brightness, color, contrast, and clarity are our main focus areas. Through calibration of the sensor and lens and joint tuning of ISP sub-modules, we aim to achieve reasonable overall brightness, accurate color reproduction, good image clarity without obvious noise, high image contrast, and an overall transparent look.

The overall image tuning process is shown in the following figure:

![flow](../../../../zh/01_software/pc/ISP_tuning/images/01.png)

The K230 ISP pipeline is shown in the following figure:
![flow](../../../../zh/01_software/pc/ISP_tuning/images/K230_isp-pipe-line.jpg)

Please note:

- In K230 HDR mode, the K230 CSI (Camera Serial Interface) module does not support sensor data modes where Hsync precedes Vsync, and there should be no overlap when each frame (L/S/VS) Vsync is high (valid data output).
- When enabling TNR in 3DNR, the ISP requires the sensor Hblank to be no less than 180 pixel clocks (it is recommended to set it to no less than 256 pixel clocks). Recommendation: Frame length – Active lines >= 92 lines.

K230 ISP pipeline as following figure:
![flow](../../../../zh/01_software/pc/ISP_tuning/images/K230_isp-pipe-line.jpg)

Please note:

- In K230 HDR mode, the K230 CSI (Camera serial interface) module does not support the sensor data mode of Hsync before Vsync. And when the Vsync of each frame (L/S/VS) is high (effective data output), there should be no overlap.
- When enabling TNR in 3DNR, the ISP requires that the sensor Hblank should not be less than 180 pixel clocks (it is recommended to set it to not less than 256 pixel clocks), and it is recommended： the Frame length - Active lines >= 92 lines.

## 2. Calibration

### 2.1 Overview

Use the calibration tool (K230ISPCalibrationTool.exe) to complete the parameter calibration for the six ISP modules: BLC, LSC, CC, AWB, Noise Profile, and CAC.

The calibration sequence of the modules is as follows:

![flow](../../../../zh/01_software/pc/ISP_tuning/images/02.png)

Before using the calibration tool (K230ISPCalibrationTool.exe), users need to pre-install MATLAB Runtime (R2023a). Download link: <https://ssd.mathworks.com/supportfiles/downloads/R2023a/Release/0/deployment_files/installer/complete/win64/MATLAB_Runtime_R2023a_win64.zip>

The main interface of the calibration tool is shown below.

![image-20230821114715137](../../../../zh/01_software/pc/ISP_tuning/images/03.png)

Click the corresponding module button to directly jump to the calibration interface of each module and start calibration.

### 2.2 Black Level Correction

#### 2.2.1 Principle and Significance of Black Level Calibration

When the analog signal is very weak, it may not be converted by the A/D, resulting in loss of image details when the light is very dim. Therefore, the sensor will give the analog signal a fixed offset before A/D conversion to ensure that the output digital signal retains more image details. The black level correction module determines the specific value of this offset through calibration. Subsequent ISP processing modules need to subtract this offset to ensure data linearity. If the sensor's black level parameters are not obtained in advance, or more accurate black level values are needed, black level calibration is performed.

#### 2.2.2 Collecting RAW Images for Black Level Calibration

The steps for collecting RAW images during black level calibration are as follows:

1. Ensure the module is in a completely dark environment (e.g., cover the lens with a black cloth) to ensure no light enters the sensor.
1. Set the sensor's exposure mode to manual mode.
1. Collect 12 RAW images with different combinations of Gain values (1x, 2x, 3x, 4x) and integration times (0.01ms, 0.02ms, 0.03ms).
1. Save them in a folder according to the naming rules. The naming format of the folder is: Gain_4_T_0.03 (Gain_4_T_0.03 indicates exposure gain = 4, exposure time = 0.03s), other exposure times and Gain naming formats follow suit.

#### 2.2.3 Starting Calibration Using the Calibration Tool

When the "Black level correction" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230821145452924](../../../../zh/01_software/pc/ISP_tuning/images/04.png)

Steps:

1. Click the "Select" button to choose the folder where the RAW images are saved.
1. Fill in the RAW image's Bayer pattern in the "Align Pos" text box.
1. Set the input and output Bit Width.
1. Set the resolution: the width and height of the image.
1. Click the "OK" button to start calibration.

Among them:

1. Combine Channel text box: If checked, it means the BLC obtained by the user is the combined measurement value of the R, Gr, Gb, and B channels.
1. Normal File Out / Extended File Out: If Normal File Out is checked, it means the output is blc_para.txt; if Extended File Out is checked, the BLC of the R, Gr, Gb, and B channels will be output separately according to different exposure times and Gains.

After calibration, the Black Level vs Integration Time chart is shown below.

![image-20230821152200148](../../../../zh/01_software/pc/ISP_tuning/images/05.png)

### 2.3 Lens Shading Correction

#### 2.3.1 Basic Principle and Significance of LSC Calibration

The purpose of LSC calibration is to eliminate vignetting caused by uneven optical refraction of the lens. In the phenomenon of lens shading, the brightness attenuation from the center target point to the corners follows the cosine fourth power law. The calibration results can effectively reflect the brightness attenuation trend, and the brightness of each region of the image is restored to the target point brightness using a 32x16 grid to store the calibration results. LSC calibration includes luma shading and color shading calibration. Since the color shading characteristic curves under different color temperatures are different, LSC calibration needs to be performed under different color temperatures to meet the correction requirements of color shading under different color temperatures.

#### 2.3.2 Collecting RAW Images for LSC Calibration

Notes before collecting RAW images:

- Adjust the AE target brightness setting so that the average brightness of the center of the image is about 80% of the maximum value (e.g., 255 for 8bit).
- The light source environment for LSC collection must have a flat and uniform brightness distribution, and the collection object must be smooth and texture-free. Therefore, a DNP lightbox can be chosen as the LSC calibration RAW image collection scene.

The steps for collecting RAW images during LSC calibration are as follows:

1. Aim the device's lens at the target area of the DNP lightbox and ensure the environment is not disturbed.
1. Turn on the DNP lightbox, switch the color temperature light source to D65, and adjust the lightbox illuminance.
1. Collect a RAW image.
1. Switch the light source of the DNP lightbox (D50, TL84, F12, A) and repeat steps 2-3.

#### 2.3.3 Starting Calibration Using the Calibration Tool

When the "Lens Shade correction" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230821163641202](../../../../zh/01_software/pc/ISP_tuning/images/06.png)

Specific steps:

1. In area 2, select the Bayer pattern sorting of the RAW image, fill in the image width and height, bit width, select the type of LSC correction needed (Color Shading or Luma & Color Shading), select the corresponding color temperature light source in the CCT drop-down menu, and fill in the Black Level Offset values of each channel in the offset Subtraction field.
1. Click the "load image" button in area 1 to import the RAW image to be calibrated.
1. Area 3 is for setting the LSC grid nodes. First, determine the number of grids. The K230 ISP LSC hardware statistics are 32x16 grids, so you can choose "33Full x 17Symm knots" for calibration. If you plan to use the ISP ALSC function, check "ALSC uniform...". If "Automatic initial knot positioning" is checked, ALSC function cannot be enabled in auto.json.
1. In area 4, you can select the maximum calibration ratio of the center/corner.
1. In area 5, you can set the compensation ratio of the corners (e.g., if set to 80%, it means the brightness of the corners after calibration needs to be 80% of the center brightness).
1. Other settings can be kept as default.
1. Click "Start" to start calibration and save the LSC data.
1. In area 6, you can choose to apply the calibrated LSC data to the image, preview the calibration effect, and click "save image to file" to save the Png images under each light source.

Note: When setting the compensation ratio in step 5, it should be determined based on the severity of the lens shading. When the lens shading is severe, the gain of the four corners after compensation is large, which can easily cause noise in the four corners. In this case, reduce the compensation ratio to optimize the noise in the four corners.

### 2.4 Color Correction

#### 2.4.1 Principle of CCM Calibration

The principle of CCM calibration is to compare the actual color information of the 24-color card color blocks collected by the sensor with their expected values and calculate the 3x3 CCM matrix. The 3x3 matrix of the CCM converts the sensor's color space to the sRGB standard color space.

#### 2.4.2 Collecting RAW Images for CC Calibration

The steps for collecting RAW images during CC calibration are as follows:

1. Place the 24-color card on the inner wall of the standard lightbox (lens directly facing the color card to collect RAW images) or place the 24-color card at the bottom of the lightbox (lens and 24-color card at a 45-degree angle to collect RAW images).
1. Turn on the standard lightbox, select the D65 light source, and adjust the lightbox illuminance.
1. Adjust the distance and position of the lens to the 24-color card, ensuring the 24-color card occupies about 2/3 of the image range.
1. Adjust the AE target brightness setting to ensure the average brightness of the RAW image is around 50.
1. Collect a RAW image.
1. Switch the light source (D50, TL84, F12, A) and repeat step 5.
1. Keep the lens position unchanged, remove the 24-color card, and collect the RAW images of the gray wall background inside the lightbox under the five light sources.

#### 2.4.3 Starting Calibration Using the Calibration Tool

When the "Color Correction" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230822111931692](../../../../zh/01_software/pc/ISP_tuning/images/07.png)

Specific steps are as follows:

1. In area 1, set the width, height, bit width, Black Level Offset, and Bayer pattern of the RAW image.
1. Click the "Load" menu to sequentially import the color reference file CC_Standard.cxf (Load sRGB References, this file is located in the Canaan.Calibration.Samples\Data\ directory of the calibration tool), 24-color card RAW image (Load Color Checker Image), and gray wall background RAW image (Load Background Image).
   <br/>To import the reference color card, besides importing CC_Standard.cxf through "Load sRGB References," you can also get the customer's custom reference color card Lab values through "Load Lab-Customer References" under the "Load" menu; or load the reference color card image through "Load References Image" under the "Load" menu, then select "Select Reference Color Check" under the "Function" menu, and control the crosshair by moving the mouse to position it at the center of the four color blocks at the upper left, upper right, lower left, and lower right corners of the given color card image, and click the mouse sequentially to complete the specification of the reference color card area.
1. Click the "LSC" button to import the calibrated LSC parameter file.
1. Configure calibration parameters:
    - Set gamma
    - Check CIELAB reference
    - Configure the weights of the 24 color blocks
    - Set the preferred light source
    - Set the output saturation, default is 1
1. In the drop-down menu in area 3, select the method to pick the 24 color blocks (there are three modes: automatic, semi-automatic, and manual).
   <br/>In semi-automatic mode, the crosshair can be controlled by moving the mouse to position it at the center of the four color blocks at the upper left, upper right, lower left, and lower right corners of the color card image, and click the mouse sequentially to complete the specification of the reference color card area.
1. Click "Calibrate" to start calibration.

### 2.5 Auto White Balance

### 2.5.1 Basic Principle and Significance of AWB Calibration

AWB calibration involves calculating the best Planckian fit curve and color temperature fit curve based on the white point characteristics (R/G, B/G) of the sensor under several standard light sources. The purpose of AWB calibration is to enable the camera to automatically recognize and adapt to various color temperature light source conditions, ensuring accurate reproduction of white and other colors in the image.

#### 2.5.2 Starting Calibration Using the Calibration Tool

When the "Auto White Balance" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230822142135073](../../../../zh/01_software/pc/ISP_tuning/images/08.png)

The specific steps are as follows:

1. Click the "file" button to import the sensor spectral sensitivity file, as shown below:

   ![image-20230822152530065](../../../../zh/01_software/pc/ISP_tuning/images/09.png)

   Note: If the user does not have their own sensor spectral sensitivity file, they can use the default OV2775_sensitivity.txt included in the toolkit (this file is located in the Canaan.Calibration.Samples\Data\ directory of the calibration tool). Although AWB calibration no longer relies on the sensor spectral sensitivity file, any sensor spectral sensitivity file can be imported to proceed with the following steps without issues.

1. Click the "illumination" button to import the light source file CIE_Illuminants.cxf (this file is located in the Canaan.Calibration.Samples\Data\ directory of the calibration tool) and select the light sources to be calibrated (at least three), as shown below. Click the "OK" button to display the spectral distribution of each light source on the left side as shown below and classify each light source as indoor or outdoor using the dropdown menu.

   ![image-20230822152740591](../../../../zh/01_software/pc/ISP_tuning/images/10.png)

   ![image-20230822154937933](../../../../zh/01_software/pc/ISP_tuning/images/11.png)

1. Click the "AWB V2+ Calibration" button (in older versions of the calibration tool, click the "Start Calibration" button), and select the parameter files of each light source generated from CC calibration as shown in the red box below:

   ![image-20230822155713505](../../../../zh/01_software/pc/ISP_tuning/images/12.png)

1. Check the "White Points Evaluate" box and select an image for white point estimation.

1. Click the "Gain Region Modifier" button, select the PNG images of each light source saved during LSC calibration, as shown below, and click "OK" to proceed to the next step:

   ![image-20230822162343131](../../../../zh/01_software/pc/ISP_tuning/images/13.png)

1. Define the starting range size of the gain polygon, as shown below, and click the "OK" button to proceed to the next step:

   ![image-20230822162723170](../../../../zh/01_software/pc/ISP_tuning/images/14.png)

1. Manually adjust the range of the orange box (near white area) and the black box (all points within the black box are recognized as white points) using the buttons in the red box area, adjust the black box range to include the white points of all selected light sources, as shown below. Save the data, and if the test fails, readjust the polygon range.

   ![image-20230822164058879](../../../../zh/01_software/pc/ISP_tuning/images/15.png)

#### 2.5.3 Calibration of AWB Parameter K_Factor

In the AWB algorithm, the determination of an outdoor environment is: Exp * K_Factor <= 0.12 (where Exp is the exposure).

For example, if 2000 lux is taken as the illumination threshold between outdoor and transition environments, obtain the exposure value (ET *gain) corresponding to this illumination, and calculate: K_Factor = 0.12 / (ET* gain).

### 2.6 Noise Calibration

#### 2.6.1 Principle and Significance of Noise Profile Calibration

Noise Profile calibration involves quantitatively measuring and describing the noise characteristics generated by the sensor under different conditions. This is crucial because sensors produce different types and magnitudes of noise when operating under varying light, temperature, or ISO settings. Understanding these noise characteristics is key to effective noise reduction or correction.

#### 2.6.2 Collecting RAW Images for Noise Profile Calibration

During CC calibration, the steps for collecting RAW images are as follows:

1. Place the black-and-white gradient test card on the inner wall of the standard lightbox and turn on the lightbox, selecting the D50 color temperature light source.
1. Turn off AE and switch to manual exposure mode, collecting two sets of RAW images, each set containing 30 images:
    - Bright set: Adjust the lightbox brightness, keep the exposure time and gain at 1x constant, and ensure the black area of the gradient card is at the middle gray level.
    - Dark set: Adjust the lightbox brightness, keep the exposure time and gain at 1x constant, and ensure the white area of the gradient card is at the middle gray level.

#### 2.6.3 Starting Calibration Using the Calibration Tool

When the "Noise Calibration" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230822170824745](../../../../zh/01_software/pc/ISP_tuning/images/16.png)

The specific steps are as follows:

1. Set the width, height, bit width, and Black Level Offset of the RAW image.
1. Click the "file" button to import the bright and dark series of RAW images.
1. Click the "ROI" button to set the ROI of the image.
1. Adjust the parameters. For the Lowlight histogram, select the histogram area from the Lower range to the Split point; for the Highlight histogram, select the histogram area from the Split point to the Higher range. The combined area should cover all values from 0 to 255 (8-bit width). The selection of Split point and high range values should ensure that the retained areas of highlight and lowlight follow a Poisson distribution. If a black level offset is set, then Lower range >= black level.
1. Gamma correction and Model Fitting do not need to be set.
1. Click "Evaluate Measures".
1. Click "Fit to Model" to complete the Noise calibration and save the results.

### 2.7 Chromatic Aberration Correction

#### 2.7.1 Principle and Significance of CAC Calibration

Chromatic aberration is a common optical defect that occurs when a lens cannot focus all colors of light at the same focal point. This usually results in red-green or blue-purple color shifts at the edges of the image. To correct this shift, we need to perform CAC calibration. By analyzing the captured image data, a mathematical model can be established to describe the chromatic aberration. Once the model is established, correction parameters can be determined and used to correct the chromatic aberration.

#### 2.7.2 Collecting RAW Images for CAC Calibration

During CAC calibration, the steps for collecting RAW images are as follows:

1. Place a checkerboard or dot pattern on the inner wall of the standard lightbox and turn on the lightbox, selecting the D50 color temperature light source.
1. Adjust the AE settings so that the minimum value of the black block points is greater than the BLC value, and the maximum value of the white area does not exceed 208.
1. Capture and save a RAW image.

#### 2.7.3 Starting Calibration Using the Calibration Tool

When the "Chromatic Aberration Correction" button is clicked on the main interface, the tool will pop up a dialog box as shown below.

![image-20230822192525126](../../../../zh/01_software/pc/ISP_tuning/images/17.png)

The specific steps are as follows:

1. Click the "Demosaic&Filter" button and set the Bayer pattern format.

1. Click the "load image" button to load the RAW image, and the image will be displayed in the preview window.

1. Set the parameters under the "Demosaic&Filter" interface.

   Since the CAC module operates after demosaicing, the tool implements a simple demosaicing function here.

   - ISP_demosaic_threshold: The default threshold value is set to 4. The higher the value, the fewer edges detected by the edge detection algorithm; lower values will result in more detected edges. A value of 255 means edge detection is completely disabled.
   - Simulate 2 additional Line Buffers: Allows users to extend the vertical offset. This enables setting the vertical vector clipping to +-3. In this case, chroma reduction filtering is not performed. Default is unchecked.
   - Filter stage1 select:
   - Sharpen Level:
   - Denoise Level:
   - Lum_weight Off: Allows disabling a special feature of the filter algorithm. This feature helps suppress stronger noise in dark areas compared to bright areas. Due to nonlinear gamma correction in the processing chain, contrast and noise are emphasized in dark areas and attenuated in bright areas. To compensate for this, the texture parameter is weighted by a function derived from the average brightness of a 5x5 kernel before comparing it with the threshold. Default is unchecked, resulting in less noise in the image preview.

1. Click the "Color Correction" button and set the parameters under this interface.

   - Check "ISP_bls_enable" and set the correct BLC.
   - Check "Auto White-Balance".
   - Set the CCM.
   - The global gain is set to 1.0 by default.

1. Click the "Gamma" button and set the gamma curve, with the default set to gamma 2.2.

1. Click the "LSC" button, then click "Load parameters" to load the LSC calibration parameters under the corresponding D50 light source, and check "Enable".

1. Click the "CA Estimate" button, check the "CA_Estimate" box, and click "Process" to run.

1. Click the "CAC" button to view the calibration results from this interface.

## 3. Module Introduction

### 3.1 BLS

#### 3.1.1 Function Description

Subtract the black level offset value to ensure data linearity.

#### 3.1.2 Main Parameters

| Parameter   | Type and Range       | Description                                     |
|-------------|----------------------|-------------------------------------------------|
| bls_enable  | bool                 | BLS enable switch                               |
| bls         | int bls[4] 0~4095    | Black level compensation values for four channels, based on ISP 12 bits |

#### 3.1.3 Debugging Strategy

Although separate black level compensation values for the four channels are supported, it is recommended to use the same value.

### 3.2 LSC

#### 3.2.1 Function Description

In K230, the LSC algorithm uses a 32x16 grid to calibrate the image. During RAW image data processing, the LSC algorithm divides the image into 32x16 sub-blocks and processes the four channels of the RAW image.

#### 3.2.2 Main Parameters

| Parameter | Type and Range      | Description                                       |
|-----------|---------------------|---------------------------------------------------|
| enable    | bool                | LSC enable switch                                 |
| matrix    | matrix[4] [1089]     | Lens shading calibration parameters for R, Gr, Gb, and B channels, obtained from the calibration file |
| x_size    | xSize[32]           | Distance between every two grid nodes on the x-axis, obtained from the calibration file |
| y_size    | ySize[16]           | Distance between every two grid nodes on the y-axis, obtained from the calibration file |

### 3.3 Dgain

#### 3.3.1 Function Description

The digital gain of the ISP is mainly used to enhance the brightness of the image.

#### 3.3.2 Main Parameters

| Parameter           | Type and Range   | Description                  |
|---------------------|------------------|------------------------------|
| enable              | bool             | ISP digital gain enable switch |
| digital_gain_r      | float 1.0~255.99 | Digital gain for the R channel |
| digital_gain_gr     | float 1.0~255.99 | Digital gain for the Gr channel |
| digital_gain_gb     | float 1.0~255.99 | Digital gain for the Gb channel |
| digital_gain_b      | float 1.0~255.99 | Digital gain for the B channel |

### 3.4 AE

#### 3.4.1 Function Description

AE (Auto Exposure) controls the brightness of the image. The main debugging involves adjusting the AE target brightness, AE convergence speed, and smoothness.

#### 3.4.2 Main Parameters

| Parameter          | Type and Range     | Description                                                                                 |
|--------------------|--------------------|---------------------------------------------------------------------------------------------|
| enable             | bool               | Auto exposure enable switch.<br/>false: Disable auto exposure<br/>true: Enable auto exposure |
| antiFlickerMode    | int 0~3            | Anti-flicker mode<br/>0: Off<br/>1: 50Hz<br/>2: 60Hz<br/>3: User defined                     |
| autoHdrEnable      | bool               | true: Automatically calculate the HDR ratio for the current frame in HDR mode<br/>false: Use a fixed HDR ratio in HDR mode |
| dampOver           | float 0~1.0        | Damping factor for smoothing AE convergence during overexposure                              |
| dampOverGain       | float 0~128.0      | AE convergence acceleration gain factor for overexposure outside the clip range; the larger the value, the faster the convergence |
| dampOverRatio      | float 1.0~4.0      | AE convergence ratio factor for overexposure outside the clip range; the smaller the value, the faster the convergence |
| dampUnder          | float 0~1.0        | Damping factor for smoothing AE convergence during underexposure                             |
| dampUnderGain      | float 0~16.0       | AE convergence acceleration gain factor for underexposure outside the clip range; the larger the value, the faster the convergence |
| dampUnderRatio     | float 0~1.0        | AE convergence ratio factor for underexposure outside the clip range; the larger the value, the faster the convergence |
| expV2WindowWeight  | float[32x32] 0~255 | Exposure weight for each sub-block                                                           |
| frameCalEnable     | bool               | Exposure setting frame interval enable switch. <br/>true: Enable the exposure setting frame interval function <br/>false: Disable the exposure setting frame interval function |
| lowLightHdrGain  | float[20] 0~255.0   | Gain value corresponding to the current gain level in wide dynamic range mode |
| lowLightHdrLevel  | int 0~16  | Total gain levels in wide dynamic range mode |
| lowLightHdrRepress  | float[20] 0~1.0   | Target brightness suppression ratio corresponding to the current gain level in wide dynamic range mode |
| lowLightLinearGain  | float[20] 0~255.0   | Gain value corresponding to the current gain level in linear mode |
| lowLightLinearLevel  | int 0~19   | Total gain levels in linear mode |
| lowLightLinearRepress  | float[20] 0~1.0   | Target brightness suppression ratio corresponding to the current gain level in linear mode |
| motionFilter  | float 0~1.0  | Motion smoothing parameter used to calculate the motion factor in AE scene evaluation adaptive mode |
| motionThreshold  | float 0~1.0 | Motion discrimination threshold |
| roiNumber  | int   | Current ROI window index |
| roiWeight  | float   | Brightness calculation weight of the current ROI window |
| roiWindow  | float (fx,fy,fw, fh) | Starting point coordinates (x,y) and width and height of the current ROI window |
| semMode  | int 0~2  | Scene mode <br/>0: Scene evaluation off mode <br/>1: Scene evaluation fixed mode <br/>2: Scene evaluation dynamic mode |
| setPoint  | float 0~255.0  | Set the target brightness value for AE |
| targetFilter  | float 0~1.0 | Smoothing coefficient for changes in AE target brightness value; the larger the value, the faster the change |
| tolerance  | float 0~100.0  | Set the percentage lock range for AE target brightness value |
| wdrContrast.max  | float 0~255.0   | Maximum contrast value for calculating AE setpoint in AE scene evaluation adaptive mode |
| wdrContrast.min  | float 0~255.0   | Minimum contrast value for calculating AE setpoint in AE scene evaluation adaptive mode |

### 3.5 AWB

#### 3.5.1 Function Description

Under different light source environments, the color of objects will vary. Human eyes have the characteristic of constancy, being able to recognize the true color of objects under different color temperatures, but sensors react differently under various light sources compared to human eyes, leading to color cast. AWB (Auto White Balance) can reduce the impact of external light sources on the true color of objects, making color-cast objects appear as if they are under ideal daylight without color cast.

#### 3.5.2 Main Parameters

| Parameter    | Type and Range | Description                       |
| ------- | -------------- | ------------------------------------ |
| enable      | bool  | true: Enable AWB <br/> false: Disable AWB |
| awbTempWeight   | float 0.0~1.0  | AWB color temperature light source weight  |
| mode   | int 0,1  |  0: AWB <br/> 1: AWB METADATA |
| roiNumber   | int   | Current ROI window index   |
| roiWeight  | float   | AWB calculation weight of the current ROI window |
| roiWindow   | float (fx,fy,fw,fh) | Starting point coordinates (x,y) and width and height of the current ROI window |
| useCcMatrix | bool  | true: Enable CCM adaptive <br/>false: Disable CCM adaptive |
| useCcOffset | bool  | true: Enable CCM offset adaptive <br/> false: Disable CCM offset adaptive  |
| useDamping  | bool  | true: Enable AWB damping change <br/> false: Disable AWB damping change |
| kFactor     | float | Sensitivity coefficient used to identify outdoor and transition areas |

#### 3.5.3 Explanation of kFactor Calibration

In the AWB algorithm, the determination of an outdoor environment is: Exp * kFactor <= 0.12 (where Exp is the exposure).

For example, if 2000 lux is taken as the illumination threshold between outdoor and transition environments, obtain the exposure value (ET *gain) corresponding to this illumination, and calculate: kFactor = 0.12 / (ET* gain).

The larger the kFactor, the stronger the sensor's sensitivity; the smaller the kFactor, the weaker the sensor's sensitivity.

This kFactor parameter is located in the AWB parameters of the XML file and needs to be calculated using the above method and filled in.

### 3.6 WDR

#### 3.6.1 Function Description

During image processing, it is easy to notice insufficient contrast in the image, and there may be a loss of details in both bright and dark areas. The WDR (Wide Dynamic Range) module enhances image contrast using histogram equalization methods while improving detail information in both bright and dark areas.

#### 3.6.2 Main Parameters

| Parameter            | Type and Range    | Description   |
| --------------- | --------------- | ------------------------------------------------------------ |
| enable          | bool           | WDR enable switch |
| contrast        | int -1023~1023 | The larger the value, the stronger the local contrast |
| entropy         | int[20]        | Local weight  |
| entropy_base    | int            | Brightness factor parameter. The larger the base, the smaller the slope, and the stronger the local contrast |
| entropy_slope   | int            | Brightness factor parameter. The larger the base, the smaller the slope, and the stronger the local contrast |
| flat_strength   | int 0~19       | Flat area stretch strength |
| flat_thr        | int 0~20       | Flat area threshold. The larger the value, the flatter the image is judged to be. Less than the threshold is judged as a flat area, greater than the threshold is judged as a texture area |
| gamma_down      | int[20]        | Local weight    |
| gamma_pre      | int[20]        | Local weight     |
| gamma_up        | int[20]        | Global curve     |
| global_strength | int 0~128      | Overall contrast strength |
| high_strength   | int 0~128      | Protection strength for bright areas of the image. The larger the value, the stronger the protection for bright areas in the image |
| low_strength    | int 0~255      | Protection strength for dark areas of the image. The larger the value, the stronger the protection for dark areas in the image |
| strength        | int 0~128      | Total strength |

#### 3.6.3 Debugging Strategy

In linear mode, set Strength to 128. Low Strength is essentially the maximum gain and is used along with High Strength to adjust image brightness. When the dark areas of the image need to be brightened, increase Low Strength. When the bright areas of the image are overexposed and need to be suppressed, increase High Strength. To avoid excessive noise amplification, as the gain increases, Low Strength should gradually decrease, while High Strength can remain the same or gradually increase. Global Strength is used to control overall contrast. When the overall contrast of the image is weak, this parameter can be appropriately increased. Contrast, Flat Strength, and Flat Threshold are used to adjust local contrast. You can start with the default parameters; if the local contrast is not good, you can appropriately increase Contrast. Increasing contrast can make gray shadows in flat areas more pronounced. Currently, adjust Flat Threshold to identify texture and flat areas and increase Flat Strength to smooth flat areas to reduce gray shadows.

### 3.7 GE

#### 3.7.1 Function Description

The main function of green balance is to balance the differences between adjacent Gr and Gb pixels in RAW data, preventing the formation of grid or maze-like patterns in subsequent demosaic interpolation algorithms. This module is located before the DPCC.

#### 3.7.2 Main Parameters

| Parameter        | Type and Range | Description             |
| ----------- | -------------- | ---------------- |
| enable | bool           | Green balance enable switch |
| threshold   | float 0~511.0  | Green balance strength threshold |

### 3.8 DPCC

#### 3.8.1 Function Description

Due to the limitations of sensor manufacturing processes, it is impossible for all pixels to be perfect, especially for lower-cost sensors, which may have more defective pixels. If defective pixels in the sensor are not addressed early, they may be amplified and spread in subsequent demosaic interpolation algorithms. Therefore, this module calibrates defective pixels before the demosaic module. The fixed defect table can accommodate up to 2048 defective pixels. Seven sets of settings are available for selection.

#### 3.8.2 Main Parameters

| Parameter         | Type and Range              | Description               |
| ------------ | --------------------------- | ------------------ |
| enable      | bool                        | DPCC enable switch. <br/> false: Disable DPCC (Default); <br/> true: Enable DPCC |
| bpt_Enable  | bool      | Defect table enable switch |
| bpt_Num | int 0~1024    | Current index of defective pixels in the defect table |
| bpt_out_mode | int 0~14 | Mode selection for correction output median in the defect table |
| bpt_pos_X   | int       | Horizontal address of the defective pixel |
| bpt_pos_Y   | int       | Vertical address of the defective pixel |
| bypass      | bool      | DPCC bypass enable switch. <br/>false: Pass through DPCC <br/>true : Bypass DPCC |
| line_mad_fac | int lineMadFac\[2][3] 0~63 | Mean absolute deviation factor |
| line_thresh | int lineThresh\[2][3] 0~255 | Set row thresholds for R&B&G |
| methods_set | int methodsSet[3] 0~8191 | Selection of defective pixel correction method for each channel. There are two methods for defective pixel correction: median filtering including the center point and median filtering without the center point. |
| out_mode    | int 0~15  | Interpolation mode of the calibration unit |
| pg_fac      | int pgFac\[2][3] 0~63     | Peak gradient factor  |
| rg_fac      | int rgFac\[2][3] 0~63     | Rank gradient factor  |
| rnd_offs    | int rndOffs\[2][3] 0~3    | Rank neighbor difference offset |
| rnd_thresh  | int rndThresh\[2][3] 0~63 | Rank neighbor difference threshold |
| ro_limits   | int roLimits\[2][3] 0~3   | Rank offset limits |
| set_use     | int 1~7                  | Select which set of calibration settings to use |

### 3.9 DPF

#### 3.9.1 Function Description

Bilateral filter denoising.

#### 3.9.2 Main Parameters

| Parameter        | Type and Range      | Description      |
| ----------- | ---------------- | ----------------------------------- |
| enable      | bool             | Enable switch.                           |
| gain        | float 1.0~1000.0 | Sensor gain                         |
| gradient    | float 0.1~128    | Gradient                                |
| min         | float 1.0~128.0  | Strength clip                       |
| offset      | float 0~128.0    | The larger the value, the greater the denoising strength                |
| div         | float 0~64.0     | The larger the value, the smaller the denoising strength                |
| sigma_g     | float 1.0~128.0  | Spatial filtering for the G channel, the larger the value, the greater the weight   |
| sigma_rb    | float 1.0~128.0  | Spatial filtering for the R&B channels, the larger the value, the greater the weight |
| noise_curve | float 0~4095.0   | 17-point curve obtained from the calibration file      |

### 3.10 3DNR

#### 3.10.1 Function Description

Image denoising is an important step in digital image processing, and the denoising effect will affect subsequent image processing. 3DNR (Three-Dimensional Noise Reduction) combines temporal and spatial information to more effectively identify and reduce noise, with motion detection to ensure that the denoising process does not affect the details and clarity of moving objects.

#### 3.10.2 Main Parameters

| Parameter        | Type and Range      | Description      |
| ---------------- | --------------- | ------------------------------------------------------------ |
| enable           | bool            | Master enable switch for 2DNR and 3DNR                                         |
| tnr_en           | bool            | 3DNR enable switch                                                 |
| nlm_en           | bool            | 2DNR enable switch                                                 |
| sigma            | float 0.1~16.0  | 2DNR strength, the larger the value, the greater the denoising strength                               |
| strength         | float 0~128.0   | 2DNR strength, the larger the value, the greater the denoising strength                               |
| blend_motion     | float 0~100.0   | Represents the weight of the frame processed by 2DNR and the tnr output frame. Changing it will affect the denoising strength, but motion estimation remains unchanged |
| blend_slope      | float 0.1~32.0  | Blending slope; the larger the value, the greater the weight of the NLM image. 2DNR blending weight slope. The smaller the value, the higher the static blending weight; the larger the value, the higher the motion blending weight.|
| blend_static     | float 0~100.0   | Represents the weight of the frame processed by 2DNR in the static area and the tnr output frame |
| dialte_h         | float           | Width of the 3DNR motion dilation window |
| filter_len       | float 0~1024    | Temporal filter window length, indicating how many frames of information are referenced |
| filter_len2      | float 0~100     | Length of the motion history frame |
| motion_dilate_en | bool            | Enable switch for motion dilation |
| motion_erode_en  | bool            | Enable switch for motion erosion |
| noise_level      | float 0~1024    | Motion detection threshold; values greater than this are considered motion areas |
| noisemodel_a     | float           | Slope of the custom pregamma curve |
| noisemodel_b     | float           | Offset value of the custom pregamma curve |
| pregamma_en      | bool            | Enable switch for pregamma transformation |
| preweight        | float           | Weight of the previous frame's motion information |
| range_h          | float           | Radius of the motion detection window in the horizontal direction, 7 represents using a 15x15 window |
| range_v          | float           | Radius of the motion detection window in the vertical direction, 7 represents using a 15x15 window |
| sadweight        | float           | Sets the weight of motion difference type a; the final motion detection is the weighted sum of two types of motion differences, a parameter for calculating block diff |
| thr_motion_slope | float           | Transition segment, beyond the slope is considered a 100% motion area |

#### 3.10.3 Debugging Strategy

1. First, enable tnr, nlm, dilate, erode, and pregamma;
1. Set filter_len to control the damping ratio of the reference frame;
1. Set filter_len2 to control the damping ratio of the motion frame;
1. Use noise_level to distinguish between foreground and background;
1. Set thr_motion_slope, sad weight, and preweight to calculate the motion area.

Please note: When enabling TNR, the ISP requires the sensor/ISP Hblank to be no less than 180 pixel clocks (recommended to set to 256 pixel clocks), and Vblank should be no less than 60 sensor ET lines.

### 3.11 Demosaic

#### 3.11.1 Function Description

The Demosaic module primarily converts input Bayer format data into RGB format data using interpolation algorithms. It also supports noise reduction, sharpening, moiré removal, and purple fringe removal.

#### 3.11.2 Main Parameters

| Parameter        | Type and Range      | Description      |
| ---------------- | ------------------- | ---------------- |
| demosaic_enable  | bool                | Enable switch for demosaic |
| demosaic_thr     | int 0~255           | Interpolation threshold for the R and B channels; below this value, non-directional interpolation is performed |
| dmsc_dir_thr_min | int 0~4095          | Interpolation for the G channel in dark areas |
| dmsc_dir_thr_max | int 0~4095          | Interpolation for the G channel in bright areas |
| dmsc_denoise_strength | int 0~31       | Low-frequency filtering noise reduction strength |
| dmsc_sharpen_enable | bool             | Enable switch for sharpening |
| dmsc_sharpen_clip_black | int 0~2047   | Black edge sharpening limit parameter |
| dmsc_sharpen_clip_white | int 0~2047   | White edge sharpening limit parameter |
| dmsc_sharpen_factor_black | int 0~511  | Sharpening enhancement for black edges; the larger the value, the more pronounced the sharpening effect |
| dmsc_sharpen_factor_white | int 0~511  | Sharpening enhancement for white edges; the larger the value, the more pronounced the sharpening effect |
| dmsc_sharpen_line_enable | bool        | Enable switch for adjacent short lines in the image |
| dmsc_sharpen_line_r1 | int 0~255       | / |
| dmsc_sharpen_line_r2 | int 0~255       | / |
| dmsc_sharpen_line_strength | int 0~4095| The larger the value, the greater the sharpening strength for lines |
| dmsc_sharpen_line_thr | int            | Line sharpening threshold |
| dmsc_sharpen_line_thr_shift1 | int 0~10| / |
| dmsc_sharpen_r1 | int 0~256            | Sharpening curve parameter |
| dmsc_sharpen_r2 | int 0~256            | Sharpening curve parameter |
| dmsc_sharpen_r3 | int 0~256            | Sharpening curve parameter |
| dmsc_sharpen_size | int 0~16           | Indicates the presentation of high-frequency signals. The smaller the value, the more details in the sharpened area, and the more small details will be sharpened |
| dmsc_sharpen_t1 | int 0~2047           | Sharpening curve parameter |
| dmsc_sharpen_t2_shift | int 0~11       | Sharpening curve parameter |
| dmsc_sharpen_t3 | int 0~2047           | Sharpening curve parameter |
| dmsc_sharpen_t4_shift | int 0~11       | Sharpening curve parameter |
| dmsc_demoire_area_thr | int 0~32        | Moiré removal area threshold; only areas larger than this threshold undergo moiré removal |
| dmsc_demoire_enable | bool              | Enable switch for moiré removal |
| dmsc_demoire_r1 | int 0~255             | Moiré removal strength curve parameter |
| dmsc_demoire_r2 | int 0~255             | Moiré removal strength curve parameter |
| dmsc_demoire_t1 | int 0~255             | Moiré removal strength curve parameter |
| dmsc_demoire_t2_shift | int 0~8         | Moiré removal strength curve parameter |
| demoire_edge_r1 | int 0~255             | Moiré conversion curve parameter |
| demoire_edge_r2 | int 0~255             | Moiré conversion curve parameter |
| demoire_edge_t1 | int 0~511             | Moiré conversion curve parameter |
| demoire_edge_t2_shift | int 0~9         | Moiré conversion curve parameter |
| dmsc_demoire_sat_shrink | int 0~32      | The larger the value, the stronger the saturation reduction in the moiré area |
| dmsc_depurple_cbcr_mode | int [0,1,2,3] | Depurple channel mode. 0: Disable depurple, 1: R channel depurple, 2: B channel depurple, 3: R&B channel depurple |
| dmsc_depurple_enable | bool              | Enable switch for depurple |
| dmsc_depurple_sat_shrink | int 0~8       | Saturation reduction value in the purple fringe area. The larger the value, the stronger the saturation reduction |
| dmsc_depurple_thr | int 8~255           | Detection threshold for purple fringe intensity. The smaller the value, the more pixels are considered purple fringes |

#### 3.11.3 Debugging Strategy

1. Interpolation

   For 12-bit raw, the interpolation threshold corresponding to the value 0 is dir_thr_min, and the interpolation threshold corresponding to the value 4095 is dir_thr_max. Values in between correspond to points on the line segment determined by dir_thr_min and dir_thr_max.

   ![image-20230828143338539](../../../../zh/01_software/pc/ISP_tuning/images/18.png)

   Setting demosaic_thr: Gradient difference > threshold, directional interpolation; gradient difference < threshold, average interpolation. Smaller values mean more false colors in high-frequency areas.

1. Sharpening and Noise Reduction

   denoise_strength represents the strength of low-frequency noise filtering. When set to 0, it is equivalent to turning off the noise reduction function. Generally, noise reduction is turned off in the demosaic module, and it is only used when the image noise is particularly high.

   Setting sharpening curve parameters: The steeper the curve, the greater the sharpening strength.

   ![image-20230828145740677](../../../../zh/01_software/pc/ISP_tuning/images/19.png)

   Setting sharpen_line: When the image noise is relatively high and you want the edges to be smooth and continuous, you can enable sharpen_line. The basic effect of sharpen_line is to smooth lines or textures in the horizontal or vertical direction. The larger the values of sharpen_line_r1 and sharpen_line_r2, the more the sharpening result approaches directional (horizontal or vertical) enhancement. Additionally, more points are incorrectly connected, which may lead to errors in high-frequency details.

   Setting sharpen_factor & clip: The larger the factor value, the stronger the sharpening effect; the larger the clip value, the weaker the truncation effect, and the more details are retained. It is advisable to avoid setting factor > clip as much as possible, as this would result in less detail retention while having high sharpening strength, leading to a lack of gradation.

1. Moire Removal

   Moire conversion curve:

   ![image-20230904094148683](../../../../zh/01_software/pc/ISP_tuning/images/20.png)

   Moire calibration curve:

   ![image-20230904094333522](../../../../zh/01_software/pc/ISP_tuning/images/21.png)

### 3.12 ManualWB

#### 3.12.1 Function Description

Manually set the gain values for white balance.

#### 3.12.2 Main Parameters

| Parameter    | Type and Range      | Description                       |
| ------------ | ------------------- | --------------------------------- |
| driver_load  | bool                | Indicates whether to load the parameters under this module |
| gain         | float [4] 1.0~3.999 | White balance gain values for four channels |

### 3.13 CCM

#### 3.13.1 Function Description

Complete linear correction of the color space using a standard 3×3 matrix and vector offset. The 3x3 matrix of CCM converts the sensor's color space to the sRGB standard color space.

#### 3.13.2 Main Parameters

| Parameter    | Type and Range                 | Description      |
| ------------ | ------------------------------ | ---------------- |
| enable       | bool                           | Enable switch for CCM |
| ccmatrix     | float ccMatrix[9] -8.0~7.996   | Color calibration matrix |
| ccoffset     | ccOffset[3] -2048~2047 (12bit) | Offset value |

### 3.14 Gamma

#### 3.14.1 Function Description

The Gamma module primarily performs nonlinear transformation of the brightness space to adapt to general output devices.

#### 3.14.2 Main Parameters

| Parameter    | Type and Range  | Description                       |
| ------------ | --------------- | --------------------------------- |
| enable       | bool            | Enable switch for gamma |
| standard     | bool            | Enable switch for standard gamma  |
| standard_val | float           | Value of gamma, default is 2.2    |
| curve        | int [64]        | 64-point gamma curve              |

#### 3.14.3 Debugging Strategy

By default, use the gamma value of 2.2. Users can customize the gamma curve as needed.

### 3.15 EE

#### 3.15.1 Function Description

The EE module is used to enhance the sharpening of image details and textures, improving image clarity. While sharpening the image edges, controlling related parameters can also suppress black and white edges.

#### 3.15.2 Main Parameters

| Parameter        | Type and Range      | Description      |
| ---------------- | ------------------- | ---------------- |
| enable           | bool                | Enable control for EE functionality |
| ee_strength      | int 0~128           | EE strength |
| ee_src_strength  | int 0~255           | The larger the value, the greater the noise reduction strength. Default is set to 1 |
| ee_y_up_gain     | int 0~10000         | Gain strength for bright edges |
| ee_y_down_gain   | int 0~10000         | Gain strength for dark edges |
| ee_uv_gain       | int 0~1024          | Control of edge color saturation; the larger the value, the more significant the saturation reduction |
| ee_edge_gain     | int 0~10000         | Detection strength of edge details. The larger the gain value, the more edge details are detected |

### 3.16 CA

#### 3.16.1 Function Description

The CA module adjusts image saturation based on the UV gain curve. Its main function is to eliminate color noise in dark areas or low saturation areas. In practical applications, it can help eliminate false colors caused by the nonlinearity of the R/G/B channels in overexposed areas and white balance deviations in low saturation areas.

#### 3.16.2 Main Parameters

| Parameter    | Type and Range  | Description      |
| ------------ | --------------- | ---------------- |
| ca_en        | bool            | Enable switch for the CA module |
| curve_en     | bool            | Enable switch for ca_curve and dci_curve |
| ca_mode      | int [0,1,2]     | 0: Adjust saturation based on brightness; 1: Adjust saturation based on original saturation; 2: Adjust saturation based on brightness and original saturation |
| ca_curve     | float           | 64-point ca curve |

### 3.17 DCI

#### 3.17.1 Function Description

Dynamic Contrast Improve is used to adjust the global contrast of the image.

### 3.17.2 Main Parameters

| Parameter  | Type and Range | Description          |
| ---------- | -------------- | -------------------- |
| dci_en     | bool           | DCI enable switch    |
| dci_curve  | float          | 64-point DCI curve   |

### 3.18 CProcess (Color Processing)

#### 3.18.1 Function Description

Processes the color of the image in the YUV domain.

#### 3.18.2 Main Parameters

| Parameter    | Type and Range      | Description                                                   |
| ------------ | ------------------- | ------------------------------------------------------------- |
| enable       | bool                | CProcess enable switch                                        |
| luma_in      | int                 | Luminance input range. 0: Y_in range [64..940], 1: Y_in full range [0..1023] |
| luma_out     | int                 | Luminance output clipping range. 0: Y_out clipping range [16..235], 1: Y_out clipping range [0..255] |
| chroma_out   | int                 | Chrominance pixel clipping range at output. 0: CbCr_out clipping range [16..240], 1: Full UV_out clipping range [0..255] |
| bright       | float -128~127      | Brightness adjustment value                                    |
| contrast     | float 0.3~1.9921875 | Contrast adjustment value                                      |
| hue          | float -90~89        | Hue adjustment value                                           |
| saturation   | float 0~1.9921875   | Saturation adjustment value                                    |

### 3.19 Compand

#### 3.19.1 Function Description

Data compression and stretching module. Used for data compression and stretching processing.

#### 3.19.2 Main Parameters

| Parameter              | Type and Range      | Description                                  |
| ---------------------- | ------------------- | -------------------------------------------- |
| enable                 | bool                | Data compression/expansion enable switch     |
| compress_enable        | bool                | Data compression enable switch               |
| compress_curve_x       | int[64] 0~31        | Data compression x-axis distance curve       |
| compress_use_out_y_curve | bool             | Data compression output Y-axis curve enable switch |
| compress_curve_y       | int[64] 0~16777216  | Data compression y-axis value curve          |
| expand_enable          | bool                | Data expansion enable switch                 |
| expand_curve_x         | int[64] 0~31        | Data expansion x-axis distance curve         |
| expand_use_out_y_curve | bool                | Data expansion output Y-axis curve enable switch |
| expand_curve_y         | int[64] 0~16777216  | Data expansion y-axis value curve            |

### 3.20 CAC (Chromatic Aberration Correction)

#### 3.20.1 Function Description

This module is used for chromatic aberration correction.

#### 3.20.2 Main Parameters

| Parameter      | Type and Range      | Description                                                  |
| -------------- | ------------------- | ------------------------------------------------------------ |
| a_blue         | float -16~15.9375   | Radial blue shift calculation parameter, calculated according to the formula (a_blue *r + b_blue* r^2 + c_blue * r^3) |
| a_red          | float -16~15.9375   | Radial red shift calculation parameter, calculated according to the formula (a_red *r + b_red* r^2 + c_red * r^3)  |
| b_blue         | float -16~15.9375   | Radial blue shift calculation parameter, calculated according to the formula (a_blue *r + b_blue* r^2 + c_blue * r^3)  |
| b_red          | float -16~15.9375   | Radial red shift calculation parameter, calculated according to the formula (a_red *r + b_red* r^2 + c_red * r^3)  |
| c_blue         | float -16~15.9375   | Radial blue shift calculation parameter, calculated according to the formula (a_blue *r + b_blue* r^2 + c_blue * r^3)  |
| c_red          | float -16~15.9375   | Radial red shift calculation parameter, calculated according to the formula (a_red *r + b_red* r^2 + c_red * r^3)  |
| cac_enable     | bool                | CAC enable switch                                             |
| center_h_offs  | int                 | Horizontal distance between the image center and the optical center |
| center_v_offs  | int                 | Vertical distance between the image center and the optical center |

a_blue, b_blue, c_blue can be obtained from the blue_parameters field in the xml file's CAC section, a_red, b_red, c_red can be obtained from the red_parameters field in the xml file's CAC section, center_h_offs can be obtained from the x_offset field in the xml file's CAC section, and center_v_offs can be obtained from the y_offset field in the xml file's CAC section.
