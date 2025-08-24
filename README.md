# AI_mbot (A_m)
Non-intrusive aimbot

## Brief Summary
A_m uses image image processing, computer vision and object detection algorithm to identify in-game models in realtime.
### Libraries
#### - YOLOv8
#### - OpenCV 

### Models (Step-by-step)
#### - Data Collection: Gather different random screenshots
#### - Data annotation through CVAT for object detection
#### - Train data in YOLOv8

## Pre-requisite
### Important libraries required, __very important!__
1. NVIDIA graphic card(s) with CUDA support
1. Python 3.x
2. OpenCV with CUDA
   - DO NOT USE pip library, use CMAKE to build OpenCV with CUDA!
   - Refernces: [**Quick and Easy OpenCV Python Installation with Cuda GPU in Under 10 Minutes**](https://www.youtube.com/watch?v=d8Jx6zO1yw0&t=475s&pp=ygUQb3BlbmN2IHdpdGggY3VkYQ%3D%3D)

## Introduction
### Dataset
<!-- ![t](https://github.com/firdauzbk/AI_mbot/assets/100037523/603ecc3e-efaa-40c1-aacd-5673b2511b37) ![ct](https://github.com/firdauzbk/AI_mbot/assets/100037523/2103c72b-d6fd-4f34-a2f4-2314f22d4cce) -->
### Data annotation (categorisation)




# Credits
[Ultralytics - YOLOv8](https://docs.ultralytics.com/usage/python/)

[OpenCV](https://opencv.org/)

[CS2-Object-Detection by Vombit](https://huggingface.co/Vombit/yolov8n_cs2)