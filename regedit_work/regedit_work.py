import winreg
import time
from pathlib import Path
from datetime import datetime

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"

def list_startup_programs():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ)
        print("Startup Programs:")
        i = 0
        while True:
            try:
                name, path, regtype = winreg.EnumValue(key, i)
                print(f"  {i+1}. {name} \nPath: {path}")
                i += 1
            except OSError:
                break
        winreg.CloseKey(key)
    except PermissionError:
        print("Permission denied!")

def add_startup_program(name, path):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, name, 0, winreg.REG_SZ, path)
        winreg.CloseKey(key)
        print(f"Program '{name}' added to startup.")
    except PermissionError:
        print("Permission denied!")

def remove_startup_program(name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE)
        winreg.DeleteValue(key, name)
        winreg.CloseKey(key)
        print(f"️Program '{name}' removed from startup.")
    except FileNotFoundError:
        print(f"Program '{name}' not found in startup.")
    except PermissionError:
        print("Permission denied!")

def check_startup_program(name):
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ)
        try:
            path, regtype = winreg.QueryValueEx(key, name)
            print(f"Program '{name}' found in startup: {path}")
        except FileNotFoundError:
            print(f"Program '{name}' not found in startup.")
        finally:
            winreg.CloseKey(key)
    except PermissionError:
        print("Permission denied!")

def ensure_logs_folder():
    folder_path = Path(__file__).parent / "data"
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path

def read_usage_time(file_path):
    if file_path.exists():
        with open(file_path, "r") as f:
            try:
                return int(f.read())
            except ValueError:
                return 0.0
    return 0.0

def save_usage_time(file_path, seconds):
    with open(file_path, "w") as f:
        f.write(str(seconds))

def main():
    folder_path = ensure_logs_folder()  
    file_path = folder_path / "trial_checker.txt"
    file_path.touch(exist_ok=True)

    total_usage_time = read_usage_time(file_path)

    start_time = time.time()
    while True:
        print("\n--- Startup Manager ---")
        print("1. List all startup programs")
        print("2. Add a startup program")
        print("3. Remove a startup program")
        print("4. Check a startup program")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "1":
            list_startup_programs()
        elif choice == "2":
            name = input("Enter program name: ")
            path = input("Enter full path to program: ")
            add_startup_program(name, path)
        elif choice == "3":
            name = input("Enter program name to remove: ")
            remove_startup_program(name)
        elif choice == "4":
            name = input("Enter program name to check: ")
            check_startup_program(name)
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Try again.")
    end_time = time.time()
    session_time = end_time - start_time
    total_usage_time = int(total_usage_time + session_time)
    save_usage_time(file_path, total_usage_time)
    print(f"Total usage time: {total_usage_time} seconds")

main()
