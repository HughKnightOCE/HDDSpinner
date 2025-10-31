import os
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import ttkbootstrap as tb
from datetime import datetime, timedelta

APP_NAME = "Drive Spinner Utility"
VERSION = "v2.1"
AUTHOR = "Hugh Knight"
LOG_FILE = "access_log.txt"

class DriveSpinnerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_NAME)
        self.root.geometry("600x450")
        self.is_running = False
        self.interval = tk.IntVar(value=30)
        self.folder_path_1 = tk.StringVar()
        self.folder_path_2 = tk.StringVar()
        self.current_target = 1
        self.start_time = None
        self.total_accesses = self.load_access_count()

        # Modern Style
        self.style = tb.Style("flatly")
        self.style.configure("TButton", font=("Segoe UI", 11), padding=10)
        self.style.configure("TLabel", font=("Segoe UI", 11))
        self.style.configure("TCombobox", font=("Segoe UI", 11))

        # Folder 1 Selector
        path1_frame = tb.Frame(root)
        path1_frame.pack(pady=5)
        tb.Label(path1_frame, text="Target Folder 1:").pack(side="left", padx=5)
        tb.Entry(path1_frame, textvariable=self.folder_path_1, width=40).pack(side="left")
        tb.Button(path1_frame, text="Browse", bootstyle="secondary", command=lambda: self.browse_folder(self.folder_path_1)).pack(side="left", padx=5)

        # Folder 2 Selector
        path2_frame = tb.Frame(root)
        path2_frame.pack(pady=5)
        tb.Label(path2_frame, text="Target Folder 2:").pack(side="left", padx=5)
        tb.Entry(path2_frame, textvariable=self.folder_path_2, width=40).pack(side="left")
        tb.Button(path2_frame, text="Browse", bootstyle="secondary", command=lambda: self.browse_folder(self.folder_path_2)).pack(side="left", padx=5)

        # Interval Dropdown
        interval_frame = tb.Frame(root)
        interval_frame.pack(pady=10)
        tb.Label(interval_frame, text="Access Interval (sec):").pack(side="left", padx=5)
        tb.Combobox(interval_frame, textvariable=self.interval, values=[10, 20, 30, 60], width=5).pack(side="left")

        # Start / Stop Buttons
        button_frame = tb.Frame(root)
        button_frame.pack(pady=15)
        self.start_button = tb.Button(button_frame, text="Start", bootstyle="success", command=self.start_process)
        self.start_button.pack(side="left", padx=10)
        self.stop_button = tb.Button(button_frame, text="Stop", bootstyle="danger", command=self.stop_process, state="disabled")
        self.stop_button.pack(side="left", padx=10)
        tb.Button(button_frame, text="Info", bootstyle="info", command=self.show_info).pack(side="left", padx=10)

        # Console Output (Scrolled Text)
        console_frame = tb.Frame(root)
        console_frame.pack(pady=10, fill="both", expand=True)
        self.console_output = scrolledtext.ScrolledText(console_frame, height=10, state="disabled", font=("Consolas", 10))
        self.console_output.pack(fill="both", expand=True, padx=10, pady=5)

        # Status & Timer Label
        self.status_label = tb.Label(root, text="Status: Idle")
        self.status_label.pack(side="bottom", pady=2)
        self.timer_label = tb.Label(root, text="Runtime: 00:00:00")
        self.timer_label.pack(side="bottom", pady=2)

        # Start runtime timer update loop
        self.update_timer()

    def browse_folder(self, target_var):
        folder = filedialog.askdirectory()
        if folder:
            target_var.set(folder)

    def start_process(self):
        if not self.folder_path_1.get() or not self.folder_path_2.get():
            messagebox.showerror("Error", "Please select both target folders.")
            return
        self.is_running = True
        self.start_time = datetime.now()
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.status_label.config(text="Status: Running...")
        threading.Thread(target=self.poke_drive_loop, daemon=True).start()

    def stop_process(self):
        self.is_running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")

    def poke_drive_loop(self):
        while self.is_running:
            target_folder = self.folder_path_1.get() if self.current_target == 1 else self.folder_path_2.get()
            timestamp = datetime.now().strftime("%H:%M:%S")
            try:
                files = os.listdir(target_folder)
                log_msg = f"[{timestamp}] Accessed {target_folder} - {len(files)} items found."
            except Exception as e:
                log_msg = f"[{timestamp}] Error accessing {target_folder}: {e}"

            self.total_accesses += 1
            self.save_access_count()
            self.print_to_console(log_msg)

            # Switch to other folder for next loop
            self.current_target = 2 if self.current_target == 1 else 1
            time.sleep(self.interval.get())

    def print_to_console(self, message):
        self.console_output.config(state="normal")
        self.console_output.insert("end", f"{message}\n")
        self.console_output.see("end")
        self.console_output.config(state="disabled")

    def update_timer(self):
        if self.is_running and self.start_time:
            elapsed = datetime.now() - self.start_time
            self.timer_label.config(text=f"Runtime: {str(elapsed).split('.')[0]}")
        self.root.after(1000, self.update_timer)  # Update every 1 second

    def show_info(self):
        info_text = f"{APP_NAME}\nVersion: {VERSION}\nDeveloper: {AUTHOR}\n\n" \
                    "Start: Begins drive poking process.\n" \
                    "Stop: Halts drive activity.\n" \
                    "Interval: Sets how often the drive is accessed.\n" \
                    "Folders: Two target directories to alternate access.\n" \
                    f"Total Accesses: {self.total_accesses}"
        messagebox.showinfo("About", info_text)

    def load_access_count(self):
        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w') as f:
                f.write("0")
            return 0
        with open(LOG_FILE, 'r') as f:
            return int(f.read().strip())

    def save_access_count(self):
        with open(LOG_FILE, 'w') as f:
            f.write(str(self.total_accesses))

if __name__ == "__main__":
    root = tb.Window(themename="flatly")
    app = DriveSpinnerApp(root)
    root.mainloop()
