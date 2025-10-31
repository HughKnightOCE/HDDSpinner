import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as tb

# App Info
APP_NAME = "Drive Spinner Utility"
VERSION = "v1.0"
AUTHOR = "Hugh Knight"

class DriveSpinnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("500x300")

        # Variables
        self.folder_path = tk.StringVar()
        self.is_running = False
        self.interval = tk.IntVar(value=30)

        # Style
        self.style = tb.Style("superhero")  # Modern theme
        self.style.configure("TButton", font=("Segoe UI", 12))
        self.style.configure("TLabel", font=("Segoe UI", 12))
        self.style.configure("TCombobox", font=("Segoe UI", 12))

        # Folder Selector
        folder_frame = tb.Frame(root)
        folder_frame.pack(pady=10)
        tb.Label(folder_frame, text="Target Folder:").pack(side="left", padx=5)
        tb.Entry(folder_frame, textvariable=self.folder_path, width=40).pack(side="left")
        tb.Button(folder_frame, text="Browse", bootstyle="secondary", command=self.browse_folder).pack(side="left", padx=5)

        # Interval Dropdown
        interval_frame = tb.Frame(root)
        interval_frame.pack(pady=10)
        tb.Label(interval_frame, text="Access Interval (sec):").pack(side="left", padx=5)
        self.interval_dropdown = tb.Combobox(interval_frame, textvariable=self.interval, values=[10, 20, 30, 60], width=5)
        self.interval_dropdown.pack(side="left")

        # Start / Stop Buttons
        button_frame = tb.Frame(root)
        button_frame.pack(pady=20)
        self.start_button = tb.Button(button_frame, text="Start", bootstyle="success", command=self.start_process)
        self.start_button.pack(side="left", padx=10)
        self.stop_button = tb.Button(button_frame, text="Stop", bootstyle="danger", command=self.stop_process, state="disabled")
        self.stop_button.pack(side="left", padx=10)

        # Info Button
        tb.Button(root, text="Info", bootstyle="info-outline", command=self.show_info).pack(side="bottom", pady=10)

        # Status Label
        self.status_label = tb.Label(root, text="Status: Idle", foreground="purple")
        self.status_label.pack(side="bottom")

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.set(folder)

    def start_process(self):
        if not self.folder_path.get():
            messagebox.showerror("Error", "Please select a target folder.")
            return
        self.is_running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Running...", foreground="purple")
        threading.Thread(target=self.poke_drive_loop, daemon=True).start()

    def stop_process(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped", foreground="grey")

    def poke_drive_loop(self):
        while self.is_running:
            try:
                files = os.listdir(self.folder_path.get())
                print(f"Accessed {self.folder_path.get()} - {len(files)} items found.")
            except Exception as e:
                print(f"Error: {e}")
            time.sleep(self.interval.get())

    def show_info(self):
        info_text = f"{APP_NAME}\nVersion: {VERSION}\nDeveloper: {AUTHOR}\n\n" \
                    "Start: Begins drive poking process.\n" \
                    "Stop: Halts drive activity.\n" \
                    "Interval: Sets how often the drive is accessed.\n" \
                    "Folder: Target directory on your HDD."
        messagebox.showinfo("About", info_text)

if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = DriveSpinnerApp(root)
    root.mainloop()
