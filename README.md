# AI_mbot (A_m)
Non-intrusive aimbot (research / proof-of-concept)

## Brief Summary
A_m uses **image processing**, **computer vision**, and a **YOLOv8 object detection model** to identify in-game models in real time.  
It includes a custom GUI built with Tkinter for configuring **keybinds, aimbot settings (FOV & smoothing), and triggerbot delay**.

### Disclaimer: This project is for **educational and research purposes only** (computer vision + automation).  

---

## Libraries & Tools
- [Ultralytics YOLOv8](https://docs.ultralytics.com/usage/python/) – object detection  
- [OpenCV](https://opencv.org/) – image processing  
- [MSS](https://python-mss.readthedocs.io/) – fast screen capture  
- [Tkinter](https://docs.python.org/3/library/tkinter.html) – graphical user interface  
- `keyboard` – keyboard hotkey handling  
- `win32api` – mouse button detection (hybrid input handling)  
- `numpy` – frame & bounding box math  

---

## Project Overview
- **run.py** – entry point (launches the GUI)  
- **utility/** – contains detection, aimbot, triggerbot logic  
- **library/** – GUI, keybind system, requirements.txt  
- **weights/** – trained YOLOv8 model (`yolov8n_cs.pt`). Credit goes to [Vombit](https://huggingface.co/Vombit/yolov8n_cs2)

---

## Features
- **Screen capture** with `mss` (1920×1080)  
- **YOLOv8 detection** with annotated bounding boxes (`ch`, `th` classes for CT/T heads)  
- **Aimbot**: aims at head detections (`ch`/`th`), configurable FOV & smoothing  
- **Triggerbot**: fires on detected enemies with adjustable delay  
- **Keybinds**: user-editable via GUI (stored in JSON)  
- **GUI**: clean Tkinter interface  
  - Tabs: `Config`, `Aimbot`, `Triggerbot`  
  - Sliders for FOV, smoothing, trigger delay  
  - Keybind editor  
  - Start/Quit buttons  

---

## 📦 Installation
### Pre-requisites
1. NVIDIA GPU with CUDA support  
2. Python 3.9+ recommended  
3. OpenCV **built with CUDA**  
   - Do **NOT** install via `pip install opencv-python`  
   - Build manually with CMake for GPU acceleration  
   - Reference: [Quick and Easy OpenCV with CUDA (YouTube)](https://www.youtube.com/watch?v=d8Jx6zO1yw0&t=475s)

### Install Python requirements
```bash
pip install -r library/requirements.txt
```

### Usage
1. Open a command prompt go to a desired directory
2. Type in:
```
git clone https://github.com/firdauzbk/AI_mbot
```
3. Go into the directory
```
cd AI_mbot
```
4. Launch
```
python run.py
```

## Credits
[Ultralytics - YOLOv8](https://docs.ultralytics.com/usage/python/)

[OpenCV](https://opencv.org/)

[CS2-Object-Detection by Vombit](https://huggingface.co/Vombit/yolov8n_cs2)