<div align="center">
<h2>
     MetaSeg: Packaged version of the Segment Anything repository
</h2>
<div>
    <img width="1000" alt="teaser" src="https://github.com/kadirnar/segment-anything-pip/releases/download/v0.2.2/metaseg_demo.gif">
</div>
    <a href="https://pepy.tech/project/metaseg"><img src="https://pepy.tech/badge/metaseg" alt="downloads"></a>
    <a href="https://huggingface.co/spaces/ArtGAN/metaseg-webui"><img src="https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-sm.svg" alt="HuggingFace Spaces"></a>
</div>


<p align="center">
<a href="https://pypi.org/project/metaseg" target="_blank">
    <img src="https://img.shields.io/pypi/v/metaseg?color=%2334D058&label=pypi%20package" alt="Package version">
</a>
<a href="https://pypi.org/project/metaseg" target="_blank">
    <img src="https://img.shields.io/pypi/dm/metaseg?color=red" alt="Download Count">
</a>
<a href="https://pypi.org/project/metaseg" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/metaseg.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://pypi.org/project/metaseg" target="_blank">
    <img src="https://img.shields.io/pypi/status/metaseg?color=orange" alt="Project Status">
</a>
<a href="https://results.pre-commit.ci/latest/github/kadirnar/segment-anything-video/main" target="_blank">
    <img src="https://results.pre-commit.ci/badge/github/kadirnar/segment-anything-video/main.svg" alt="pre-commit.ci">
</a>
</p>


This repo is a packaged version of the [segment-anything](https://github.com/facebookresearch/segment-anything) model.

### Installation
```bash
pip install metaseg
```

### Usage
```python
from metaseg import SegAutoMaskPredictor, SegManualMaskPredictor

# If gpu memory is not enough, reduce the points_per_side and points_per_batch.

# For image
results = SegAutoMaskPredictor().image_predict(
    source="image.jpg",
    model_type="vit_l", # vit_l, vit_h, vit_b
    points_per_side=16,
    points_per_batch=64,
    min_area=0,
    output_path="output.jpg",
    show=True,
    save=False,
)

# For video
results = SegAutoMaskPredictor().video_predict(
    source="video.mp4",
    model_type="vit_l", # vit_l, vit_h, vit_b
    points_per_side=16,
    points_per_batch=64,
    min_area=1000,
    output_path="output.mp4",
)

# For manuel box and point selection

# For image
results = SegManualMaskPredictor().image_predict(
    source="image.jpg",
    model_type="vit_l", # vit_l, vit_h, vit_b
    input_point=[[100, 100], [200, 200]],
    input_label=[0, 1],
    input_box=[100, 100, 200, 200], # or [[100, 100, 200, 200], [100, 100, 200, 200]]
    multimask_output=False,
    random_color=False,
    show=True,
    save=False,
)

# For video

results = SegManualMaskPredictor().video_predict(
    source="video.mp4",
    model_type="vit_l", # vit_l, vit_h, vit_b
    input_point=[0, 0, 100, 100],
    input_label=[0, 1],
    input_box=None,
    multimask_output=False,
    random_color=False,
    output_path="output.mp4",
)
```

### [SAHI](https://github.com/obss/sahi) + Segment Anything

```bash
pip install sahi metaseg
```

```python
from metaseg.sahi_predict import SahiAutoSegmentation, sahi_sliced_predict

image_path = "image.jpg"
boxes = sahi_sliced_predict(
    image_path=image_path,
    detection_model_type="yolov5",  # yolov8, detectron2, mmdetection, torchvision
    detection_model_path="yolov5l6.pt",
    conf_th=0.25,
    image_size=1280,
    slice_height=256,
    slice_width=256,
    overlap_height_ratio=0.2,
    overlap_width_ratio=0.2,
)

SahiAutoSegmentation().image_predict(
    source=image_path,
    model_type="vit_b",
    input_box=boxes,
    multimask_output=False,
    random_color=False,
    show=True,
    save=False,
)
```
<img width="700" alt="teaser" src="https://github.com/kadirnar/segment-anything-pip/releases/download/v0.5.0/sahi_autoseg.png">

### [FalAI(Cloud GPU)](https://docs.fal.ai/fal-serverless/quickstart) + Segment Anything
```bash
pip install metaseg fal_serverless
fal-serverless auth login
```

```python
# For Auto Mask
from metaseg import falai_automask_image

image = falai_automask_image(
    image_path="image.jpg",
    model_type="vit_b",
    points_per_side=16,
    points_per_batch=32,
    min_area=0,
)
image.show() # Show image
image.save("output.jpg") # Save image

# For Manual Mask
from metaseg import falai_manuelmask_image

image = falai_manualmask_image(
    image_path="image.jpg",
    model_type="vit_b",
    input_point=[[100, 100], [200, 200]],
    input_label=[0, 1],
    input_box=[100, 100, 200, 200], # or [[100, 100, 200, 200], [100, 100, 200, 200]],
    multimask_output=False,
    random_color=False,
)
image.show() # Show image
image.save("output.jpg") # Save image
```
# Extra Features

- [x] Support for Yolov5/8, Detectron2, Mmdetection, Torchvision models
- [x] Support for video and web application(Huggingface Spaces)
- [x] Support for manual single multi box and point selection
- [x] Support for pip installation
- [x] Support for SAHI library
- [x] Support for FalAI
