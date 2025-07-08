import subprocess
import threading

def run_command(cmd):
    subprocess.run(cmd, shell=True)

t1 = threading.Thread(target=run_command, args=("pyinstaller --onefile --noconsole .\\updater.py",))
t2 = threading.Thread(target=run_command, args=("pyinstaller --onefile --noconsole .\\bot.py",))

t1.start()
t2.start()