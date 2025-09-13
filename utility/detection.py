import os
import cv2
import numpy as np
import keyboard
import time
from functools import lru_cache
from mss import mss
from ultralytics import YOLO
from library.keys import get_key
from utility.aimbot import aimbot

WEIGHTS_PATH = os.path.join(os.path.dirname(__file__), "..", "weights", "yolov8n_cs2.pt")

@lru_cache(maxsize=1)
def get_model():
    return YOLO(WEIGHTS_PATH)

def get_detections(results, scale_x=1.0, scale_y=1.0):
    detections = []
    names = results[0].names  # class id -> class name mapping

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        cls_name = names[cls_id]

        # Scale coords back to full resolution
        x1, x2 = int(x1 * scale_x), int(x2 * scale_x)
        y1, y2 = int(y1 * scale_y), int(y2 * scale_y)

        # Center X always
        cx = (x1 + x2) // 2

        if cls_name in ["th", "ch"]:  # head classes
            cy = int(y1 + (y2 - y1) * 0.5)  # mid-head
        else:  # body classes
            cy = int(y1 + (y2 - y1) * 0.2)  # neck area fallback

        detections.append((cx, cy, cls_name))
    return detections

def run_detection(fov=90, smooth=5, debug=False):
    """
    Run detection loop.
    If debug=True → show annotated window with FPS counter.
    If debug=False → run headless (aimbot only, no OpenCV window).
    """
    model = get_model()
    monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
    sct = mss()

    # Target inference size (smaller = faster)
    target_w, target_h = 960, 540
    scale_x = monitor["width"] / target_w
    scale_y = monitor["height"] / target_h

    if debug:
        window_name = f"0Dx-Monitor (press '{get_key('exit_detection')}' to quit)"
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 854, 480)

        prev_time = time.time()
        fps, frame_count = 0, 0

    while True:
        frame = np.array(sct.grab(monitor))

        # Faster resize on GPU
        gpu_mat = cv2.cuda_GpuMat()
        gpu_mat.upload(frame)
        gpu_mat = cv2.cuda.cvtColor(gpu_mat, cv2.COLOR_BGRA2BGR)
        gpu_mat = cv2.cuda.resize(gpu_mat, (target_w, target_h))
        frame_small = gpu_mat.download()

        # Inference
        results = model(frame_small, verbose=False)

        detections = get_detections(results, scale_x, scale_y)

        # Run aimbot on detections
        aimbot(
            detections,
            screen_w=monitor["width"],
            screen_h=monitor["height"],
            fov=fov,
            smooth=smooth,
        )

        if debug:
            # Annotated debug view
            annotated = results[0].plot()
            display_frame = cv2.resize(annotated, (854, 480))

            # FPS counter
            frame_count += 1
            if frame_count >= 10:
                curr_time = time.time()
                fps = frame_count / (curr_time - prev_time)
                prev_time = curr_time
                frame_count = 0

            cv2.putText(display_frame, f"FPS: {fps:.1f}", (10, 25),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.imshow(window_name, display_frame)

            if cv2.waitKey(1) == 46:  # Delete key
                break

        # Exit hotkey works in both modes
        if keyboard.is_pressed(get_key("exit_detection")):
            break

    if debug:
        cv2.destroyAllWindows()
