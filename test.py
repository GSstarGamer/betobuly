# import os
# import psutil
# import time

# def list_bot_exe_instances(exe_name="bot.exe"):
#     current_pid = os.getpid()
#     matches = []

#     for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
#         try:
#             if proc.pid == current_pid:
#                 continue  # Skip self

#             if proc.name().lower() == exe_name.lower():
#                 # Convert create_time (timestamp) to readable string
#                 start_time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(proc.create_time()))
#                 matches.append({
#                     'pid': proc.pid,
#                     'exe': proc.info.get('exe'),
#                     'cmdline': proc.info.get('cmdline'),
#                     'start_time': start_time_str
#                 })

#         except (psutil.NoSuchProcess, psutil.AccessDenied):
#             continue

#     return matches

# # Example usage
# if __name__ == "__main__":
#     instances = list_bot_exe_instances()
#     if not instances:
#         print("No other instances of bot.exe are running.")
#     else:
#         print("Other bot.exe instances found:")
#         for inst in instances:
#             print(f"PID: {inst['pid']}, STARTED: {inst['start_time']}, EXE: {inst['exe']}, CMD: {' '.join(inst['cmdline'] or [])}")

import os
import psutil

def kill_other_bot_exes(exe_name="bot.exe"):
    current_pid = os.getpid()
    killed = []

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.pid == current_pid:
                continue  # Skip current process

            if proc.name().lower() == exe_name.lower():
                proc.kill()
                killed.append(proc.pid)

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return killed

# Example usage
if __name__ == "__main__":
    killed_pids = kill_other_bot_exes()
    if killed_pids:
        print(f"Killed other bot.exe instances: {killed_pids}")
    else:
        print("No other bot.exe instances were found.")
