import ctypes
from library.keys import get_key, is_mouse_pressed

SendInput = ctypes.windll.user32.SendInput

# Windows API structs
PUL = ctypes.POINTER(ctypes.c_ulong)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class INPUT(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("mi", MOUSEINPUT)]

def move_mouse(dx, dy):
    extra = ctypes.c_ulong(0)
    ii_ = INPUT(type=0, mi=MOUSEINPUT(dx, dy, 0, 0x0001, 0, ctypes.pointer(extra)))
    SendInput(1, ctypes.pointer(ii_), ctypes.sizeof(ii_))

def get_closest_target(detections, screen_w, screen_h, fov):
    cx, cy = screen_w // 2, screen_h // 2
    closest, min_dist = None, float("inf")

    for (x, y, cls_name) in detections:
        dx, dy = x - cx, y - cy
        dist = (dx**2 + dy**2) ** 0.5
        if dist < min_dist and dist < fov:
            closest, min_dist = (x, y), dist
    return closest

def aimbot(detections, screen_w=1920, screen_h=1080, fov=90, smooth=5):
    aim_key = get_key("aimbot")
    if is_mouse_pressed(aim_key):
        target = get_closest_target(detections, screen_w, screen_h, fov)
        if target:
            cx, cy = screen_w // 2, screen_h // 2
            dx, dy = target[0] - cx, target[1] - cy
            move_mouse(int(dx / smooth), int(dy / smooth))

