import os
import shutil
import ctypes
import sys

# ---------------- ADMIN CHECK ----------------

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, params, None, 1
    )
    sys.exit(0)


if not is_admin():
    relaunch_as_admin()

# ---------------- CLEANUP LOGIC ----------------

def log(message):
    print(message)


def delete_contents(path):
    if not path or not os.path.exists(path):
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
        log(f"[ERROR] Some files could not be deleted in {path}")
    else:
        log(f"[OK] Cleaned {path}")

# ---------------- PATH OPTIONS ----------------

PATHS = [
    ("User TEMP", os.environ.get("TEMP", "")),
    ("Windows TEMP", r"C:\Windows\Temp"),
    ("Windows Prefetch", r"C:\Windows\Prefetch"),
    ("LocalAppData TEMP", os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp")),
]

def show_menu():
    print("\n=== Temporary Files Cleaner ===")
    for i, (name, path) in enumerate(PATHS, start=1):
        print(f"{i}. {name} -> {path}")
    print("A. Clean ALL")
    print("Q. Quit")


def start_cleaning(selected_indexes):
    log("\n=============================================")
    log("Starting temporary files cleaning process...")
    log("=============================================")

    for i in selected_indexes:
        name, path = PATHS[i]
        log(f"\n>>> Cleaning: {name}")
        delete_contents(path)

    log("\n=============================================")
    log("Cleaning process completed.")
    log("=============================================")


# ---------------- MAIN LOOP ----------------

while True:
    show_menu()
    choice = input("\nChoose option(s) (e.g. 1,2 or A): ").strip().lower()

    if choice == "q":
        print("Exiting...")
        break

    if choice == "a":
        start_cleaning(range(len(PATHS)))
        continue

    try:
        selections = [int(x.strip()) - 1 for x in choice.split(",")]
        valid = [i for i in selections if 0 <= i < len(PATHS)]

        if not valid:
            print("Invalid selection.")
            continue

        start_cleaning(valid)

    except ValueError:
        print("Invalid input. Use numbers like 1,2 or A.")
