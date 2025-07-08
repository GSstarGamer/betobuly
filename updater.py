import requests
import sys
import os
import subprocess

def main():
    exe_dir = get_original_exe_path()
    exe_path = os.path.join(exe_dir, "bot.exe")

    headers = {
        'Accept': 'application/vnd.github+json',
    }

    response = requests.get('https://api.github.com/repos/GSstarGamer/betobuly/releases/latest', headers=headers)
    response.raise_for_status()

    while True:
        with requests.get(getLatestURL(response.json()), stream=True) as r:
            try:
                with open(exe_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                break
            except PermissionError:
                pass
    
    subprocess.Popen(exe_path,
    creationflags=subprocess.CREATE_NO_WINDOW)
    return
           


def get_original_exe_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.argv[0])
    else:
        return os.path.dirname(os.path.abspath(__file__))
    

def getLatestURL(json):
    for asset in json["assets"]:
        if asset["name"] == "bot.exe":
            return asset["browser_download_url"]

if __name__ == "__main__":
    main()