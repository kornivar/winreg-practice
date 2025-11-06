import winreg
import time
from datetime import datetime

RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"
TRIAL_KEY = r"Software\TrialChecker"

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

def read_usage_time():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, TRIAL_KEY, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, "UsageTime")
        winreg.CloseKey(key)
        return float(value)
    except FileNotFoundError:
        return 0.0

def save_usage_time(seconds):
    try:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, TRIAL_KEY)
        winreg.SetValueEx(key, "UsageTime", 0, winreg.REG_SZ, str(seconds))
        winreg.CloseKey(key)
    except PermissionError:
        print("Permission denied!")

def read_license_status():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, TRIAL_KEY, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(key, "License")
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        return "trial"

def save_license_status(status):
    key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, TRIAL_KEY)
    winreg.SetValueEx(key, "License", 0, winreg.REG_SZ, status)
    winreg.CloseKey(key)

def check_access(seconds):  
    if read_license_status() == "full":
        print("Full version activated. No trial restrictions.")
        return

    if seconds >= 180:
        print("Trial period expired. Do you want to purchase the full version?(y/n)")
        if input().lower() == 'y':
            get_key_from_user()
        exit()
    else: 
        remaining = 180 - seconds
        print(f"Trial period active. {int(remaining)} seconds remaining.")

def get_key_from_user():
    key = input("Enter your license key: ")
    if key == "wertyui2134987weq":
        print("License key accepted. Full version activated.")
        save_license_status("full")
        save_usage_time(-1)
    else:
        print("Invalid license key.")    

def main():
    total_usage_time = read_usage_time()
    last_save_time = time.time()
    license_status = read_license_status()

    try:
        while True:
            print("\n--- Startup Manager ---")
            print("1. List all startup programs")
            print("2. Add a startup program")
            print("3. Remove a startup program")
            print("4. Check a startup program")
            print("5. Enter a license key")
            print("6. Exit")

            if license_status == "full" or total_usage_time == -1:
                print("Full version activated. No trial restrictions.")
            else:
                current_time = time.time()
                total_usage_time += current_time - last_save_time
                last_save_time = current_time
                check_access(total_usage_time)

            choice = input("Enter your choice (1-6): ")

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
                get_key_from_user()
                license_status = read_license_status()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Try again.")

            if license_status != "full":
                save_usage_time(total_usage_time)

    finally:
        if license_status != "full":
            current_time = time.time()
            total_usage_time += current_time - last_save_time
            save_usage_time(total_usage_time)

main()
