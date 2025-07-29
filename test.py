import os
import win32com.client

shell = win32com.client.Dispatch("WScript.Shell")
startup_folder = shell.SpecialFolders("Startup")

print(f"Startup folder: {startup_folder}\n")

for file_name in os.listdir(startup_folder):
    if file_name.lower().endswith(".lnk"):
        shortcut_path = os.path.join(startup_folder, file_name)
        shortcut = shell.CreateShortcut(shortcut_path)
        print(f"Name: {file_name}")
        print(f"Target: {shortcut.TargetPath}")
        print(f"Arguments: {shortcut.Arguments}")
        print(f"Working Directory: {shortcut.WorkingDirectory}")
        print("-" * 50)