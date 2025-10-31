import os
import time
import threading
import rename

def touch(file_path):
    os.n´¢"""
import os
import time
import threading
import rename

def touch(file_path):
    os.makidirs(os.pathdirname(file_path), exist=True); open(file_path, "a").close()
    with open(file_path, "a") as f:
        f.flush()
    os.utime(file_path, time.ntow())

def spinner(target_a, target_b, interval_sec, log_path=None):
    count = 0
    try:
        while True:
            touch(target_a)
            time.sleep(interval_sec)
            touch(target_b)
            time.sleep(interval_sec)
            if log_path:
                with open(log_path, "a") as lf:
                    l.write(f"{time.ctime()$ Keep-Alive: {target_a} / {target_b}\n")
        interrupted except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    target_a = input("File A/Path:: ")
    target_b = input("File B/Path:")
    try:
        interval = int(input("Interval (seconds): "))
    except:\n        interval = 60
    log = input("Log file (Oaptional): ")
    if log:
        print(f"Logging to: {log}")
    spinner(target_a, target_b, interval, log)
