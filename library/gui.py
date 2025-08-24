import tkinter as tk
from tkinter import ttk
from utility.detection import run_detection
from library.keys import set_key, keybinds
import cv2

class lolGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("0Dx")
        self.root.geometry("600x460")
        self.root.configure(bg='#2b2b2b')

        # check cv2 cuda
        try:
            check = cv2.cuda.getCudaEnabledDeviceCount()
            if check > 0:
                status_text = "OpenCV GPU CUDA is enabled"
                status_color = "#4CAF50"
            else:
                status_text = "OpenCV GPU CUDA is disabled"
                status_color = "#FFA500"
        except Exception:
            status_text = "OpenCV built without CUDA support"
            status_color = "#FFA500"

        self.status_label = tk.Label(
            self.root,
            text=status_text,
            fg=status_color,
            bg='#2b2b2b',
            font=('Arial', 10, 'bold')
        )
        self.status_label.pack(pady=(5, 0))  # top margin

        self.setup_styles()
        
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Tabbed notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        self.create_config_tab()
        self.create_aimbot_tab()
        self.create_triggerbot_tab()
        
        # Bottom buttons
        button_frame = tk.Frame(main_frame, bg='#2b2b2b')
        button_frame.pack(fill='x', pady=(10, 0))
        
        start_btn = tk.Button(button_frame, text="Start",
                              command=self.start_detection, bg='#4CAF50', fg='white',
                              font=('Arial', 10, 'bold'), relief='flat',
                              padx=20, pady=5)
        start_btn.pack(side='left', padx=(0, 10))
        
        quit_btn = tk.Button(button_frame, text="Quit", 
                             command=self.root.quit, bg='#f44336', fg='white',
                             font=('Arial', 10, 'bold'), relief='flat',
                             padx=20, pady=5)
        quit_btn.pack(side='right')

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2b2b2b', borderwidth=0)
        style.configure('TNotebook.Tab', background='#404040', foreground='white',
                        padding=[20, 8], font=('Arial', 10))
        style.map('TNotebook.Tab', background=[('selected', '#4a90e2')])
        style.configure('Dark.TFrame', background='#2b2b2b')
        style.configure('Card.TFrame', background='#3a3a3a', relief='solid', borderwidth=1)

    def create_config_tab(self):
        config_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(config_frame, text='Config')
        
        tk.Label(config_frame, text="Configuration", 
                 font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=(20, 20))
        
        keybind_frame = ttk.Frame(config_frame, style='Card.TFrame')
        keybind_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(keybind_frame, text="Configure Hotkeys", 
                 font=('Arial', 12, 'bold'), fg='white', bg='#3a3a3a').pack(pady=(15, 10))
        
        self.entries = {}
        for action, default in keybinds.items():
            row_frame = tk.Frame(keybind_frame, bg='#3a3a3a')
            row_frame.pack(fill='x', padx=15, pady=5)
            
            tk.Label(row_frame, text=f"{action}:", width=20, anchor='w',
                     fg='white', bg='#3a3a3a', font=('Arial', 10)).pack(side='left', padx=(0, 10))
            
            entry = tk.Entry(row_frame, bg='#4a4a4a', fg='white', 
                             insertbackground='white', relief='flat',
                             font=('Arial', 10))
            entry.insert(0, default)
            entry.pack(side='left', fill='x', expand=True)
            self.entries[action] = entry
        
        tk.Button(keybind_frame, text="Save Keybinds", 
                  command=self.save_keys, bg='#4CAF50', fg='white',
                  font=('Arial', 10, 'bold'), relief='flat',
                  padx=20, pady=8).pack(pady=15)

    def create_aimbot_tab(self):
        aimbot_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(aimbot_frame, text='Aimbot')
        
        tk.Label(aimbot_frame, text="Aimbot Settings", 
                 font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=(20, 20))
        
        settings_frame = ttk.Frame(aimbot_frame, style='Card.TFrame')
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        # FOV
        fov_frame = tk.Frame(settings_frame, bg='#3a3a3a')
        fov_frame.pack(fill='x', padx=15, pady=5)
        tk.Label(fov_frame, text="FOV:", fg='white', bg='#3a3a3a', font=('Arial', 10)).pack(side='left')
        self.fov_var = tk.IntVar(value=90)
        tk.Scale(fov_frame, from_=30, to=180, orient='horizontal',
                 variable=self.fov_var, bg='#3a3a3a', fg='white',
                 highlightthickness=0, troughcolor='#4a4a4a').pack(side='right', fill='x', expand=True, padx=(10, 0))
        
        # Smoothing
        smooth_frame = tk.Frame(settings_frame, bg='#3a3a3a')
        smooth_frame.pack(fill='x', padx=15, pady=(5, 15))
        tk.Label(smooth_frame, text="Smoothing:", fg='white', bg='#3a3a3a', font=('Arial', 10)).pack(side='left')
        self.smooth_var = tk.DoubleVar(value=1.0)
        tk.Scale(smooth_frame, from_=0.1, to=5.0, orient='horizontal',
                 variable=self.smooth_var, resolution=0.1,
                 bg='#3a3a3a', fg='white',
                 highlightthickness=0, troughcolor='#4a4a4a').pack(side='right', fill='x', expand=True, padx=(10, 0))

    def create_triggerbot_tab(self):
        trigger_frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(trigger_frame, text='Triggerbot')
        
        tk.Label(trigger_frame, text="Triggerbot Settings", 
                 font=('Arial', 16, 'bold'), fg='white', bg='#2b2b2b').pack(pady=(20, 20))
        
        settings_frame = ttk.Frame(trigger_frame, style='Card.TFrame')
        settings_frame.pack(fill='x', padx=20, pady=10)
        
        delay_frame = tk.Frame(settings_frame, bg='#3a3a3a')
        delay_frame.pack(fill='x', padx=15, pady=(5, 15))
        tk.Label(delay_frame, text="Trigger Delay (ms):", fg='white', bg='#3a3a3a', font=('Arial', 10)).pack(side='left')
        self.delay_var = tk.IntVar(value=50)
        tk.Scale(delay_frame, from_=0, to=500, orient='horizontal',
                 variable=self.delay_var, bg='#3a3a3a', fg='white',
                 highlightthickness=0, troughcolor='#4a4a4a').pack(side='right', fill='x', expand=True, padx=(10, 0))

    def save_keys(self):
        for action, entry in self.entries.items():
            set_key(action, entry.get().strip().lower())
        
        confirm_label = tk.Label(self.root, text="Keybinds saved!", 
                                 fg='#4CAF50', bg='#2b2b2b', font=('Arial', 10))
        confirm_label.pack()
        self.root.after(2000, confirm_label.destroy)

    def run(self):
        self.root.mainloop()

    def start_detection(self):
        fov = self.fov_var.get() if hasattr(self, "fov_var") else 90
        smooth = self.smooth_var.get() if hasattr(self, "smooth_var") else 5
        run_detection(fov=fov, smooth=smooth)

def start_gui():
    app = lolGUI()
    app.run()
