# Unity-RefractiveFlowRender
Render refractive objects in Unity HDRP (High Definition Rendering Pipeline), generate corresponding semantic masks and refractive flow.

## Usage

### 1. Generate refractive RGB images

Open the `HDRPRefraction` Unity project. There are three scenes: SampleScene, RGB and Calibration. The first scene will not be used in this project, please just ignore it. In this step, open the `RGB` scene, and click the `controller` gameObject. In `Inspector` window, check all options and make sure all is well. For example,  this will decide you want to generate training set or valid set, and also decide how many images you want to generate (Denote the number of images as `N`). After checking, click `Run` button on the middle-top of screen. Unity will generate `N` group of images and records. A group of images and records include an image in `rgb` folder, an image in `background` folder, as well as a record in `recorder` folder.

### 2. Generate calibration images

In the same Unity project as the last step, open `Calibration` scene. In the `Inspector` window of `controller` gameObject, check you want to calibrate for train set or valid set. After checking, click `Run` button. This scene will read the record information in `recorder` folder and generate the graycode for refractive flow. All gray code images will be saved in `calibration` folder.

### 3. Generate binary mask and semantic segmentation mask

Open the `RefractiveMask` Unity project, and open `Mask` scene. After checking options in `Inspector` window of `controller` gameObject, click `Run`. This scene will read the record information in `recorder` to generate a binary mask and a semantic mask. The former image will be saved in `calibration` folder, since it will be used to generate refractive flow, while the latter image will be saved in `mask` folder.

### 4. Generate refractive flow

Until now, Unity has finished its task. We will use python in this step. Open a new terminal and use one of the following command to generate refractive flows.

```
# This is used to generate for training set
python generate_refractive_flow.py train

# This is used to generate for validation set
python generate_refractive_flow.py valid
```

This command will generate ground truth for refractive flow. All ground truths will be saved in `calibration/refractive_flow` folder.
