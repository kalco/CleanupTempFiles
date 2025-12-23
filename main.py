import os
import shutil
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox, scrolledtext

# Admin check

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


if not is_admin():
    relaunch_as_admin()

# Cleanup logic
def delete_contents(path):
    if not os.path.exists(path):
        log(f"[SKIP] {path} does not exist")
        return

    error = False
    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        try:
            if os.path.isfile(full_path) or os.path.islink(full_path):
                os.unlink(full_path)
            else:
                shutil.rmtree(full_path, ignore_errors=True)
        except Exception:
            error = True

    if error:
        log(f"[ERROR] Failed deleting some files in {path}")
    else:
        log(f"[OK] Cleaned {path}")

def start_cleaning():
    log("=============================================")
    log("Starting temporary files cleaning process...")
    log("=============================================")

    delete_contents(os.environ.get("TEMP", ""))
    delete_contents(r"C:\Windows\Temp")
    delete_contents(r"C:\Windows\Prefetch")
    delete_contents(os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp"))

    log("=============================================")
    log("Temporary files cleaning process completed.")
    log("=============================================")

    messagebox.showinfo("Cleaning Completed", "Temporary files have been cleaned successfully!")

def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    root.update_idletasks()


# GUI

root = tk.Tk()
root.title("Cleaning temporary files by Kalco")
root.geometry("640x420")
root.resizable(False, False)

tk.Label(root, text="Cleaning temporary files", font=("Sagoe UI", 14)).pack(pady=10)
    
log_box = scrolledtext.ScrolledText(root, width=75, height=15, font=("Consoles", 10), state='normal')
log_box.pack(padx=10, pady=5)

tk.Button(root, text="Start Cleaning", font=("Sagoe UI", 11), width=25, command=start_cleaning).pack(pady=10)

root.mainloop()
