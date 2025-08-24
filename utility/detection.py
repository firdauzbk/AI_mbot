import os
import cv2
import numpy as np
import keyboard
from functools import lru_cache
from mss import mss
from ultralytics import YOLO
from library.keys import get_key
from utility.aimbot import aimbot

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "..", "weights", "yolov8n_cs2.pt")

@lru_cache(maxsize=1)
def get_model():
    return YOLO(WEIGHTS_PATH)

def get_detections(results):

    detections = []
    names = results[0].names  # class id -> class name mapping

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        cls_name = names[cls_id]

        # X always center
        cx = (x1 + x2) // 2

        if cls_name in ["th", "ch"]:
            cy = int(y1 + (y2 - y1) * 0.5)  # mid-head
        else:
            cy = int(y1 + (y2 - y1) * 0.2)  # neck area fallback

        detections.append((cx, cy, cls_name))
    return detections

def run_detection(fov=90, smooth=5):
    model = get_model()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = mss()
    
    window_name = f"0Dx-Monitor (press '{get_key('exit_detection')}' to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 854, 480)
    
    while True:
        frame = np.array(sct.grab(monitor))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

        results = model(frame, verbose=False)
        detections = get_detections(results)

        aimbot(detections,
               screen_w=monitor["width"],
               screen_h=monitor["height"],
               fov=fov,
               smooth=smooth)
        
        annotated = results[0].plot()

        display_frame = cv2.resize(annotated, (854, 480))

        cv2.imshow(window_name, display_frame)
        
        if keyboard.is_pressed(get_key("exit_detection")):
            break
        if cv2.waitKey(1) == 46:
            break
        
    cv2.destroyAllWindows()