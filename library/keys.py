import json
import os
import win32api
import win32con

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "keybinds.json")

# Default hotkeys
default_keybinds = {
    "exit_detection": "delete",   # handled by keyboard lib
    "aimbot": "mouse1",           # handled by win32api
    "triggerbot": "mouse2",       # handled by win32api
}

# Load existing config or defaults
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r") as f:
        keybinds = json.load(f)
else:
    keybinds = default_keybinds.copy()

def get_key(action: str) -> str:
    return keybinds.get(action, default_keybinds.get(action))

def set_key(action: str, key: str):
    keybinds[action] = key.lower()
    save_keys()

def save_keys():
    with open(CONFIG_FILE, "w") as f:
        json.dump(keybinds, f, indent=4)

# ---- Extra: Mouse helpers ----
def is_mouse_pressed(key: str) -> bool:
    if key == "mouse1":
        return win32api.GetAsyncKeyState(win32con.VK_LBUTTON) < 0
    elif key == "mouse2":
        return win32api.GetAsyncKeyState(win32con.VK_RBUTTON) < 0
    elif key == "mouse3":
        return win32api.GetAsyncKeyState(win32con.VK_MBUTTON) < 0
    return False