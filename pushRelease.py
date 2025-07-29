import os
import re
import subprocess



BOT_FILE = "bot.py"
DIST_EXE = os.path.join("dist", "bot.exe")

def extract_version(BOT_FILE):
    with open(BOT_FILE, encoding="utf-8") as f:
        for line in f:
            if line.strip().startswith("VERSION"):
                return line.split("=", 1)[1].strip().strip("\"'")

    raise ValueError("VERSION not found in bot.py")

print(extract_version(BOT_FILE))
def build_bot():
    print("Building bot.exe...")
    subprocess.run(["pyinstaller", "--onefile", "--noconsole", BOT_FILE], check=True)
    if not os.path.exists(DIST_EXE):
        raise FileNotFoundError("bot.exe not found after build")

def create_release_with_gh(version, exe_path):
    subprocess.run([
        "gh", "release", "create", version,
        exe_path,
        "--title", version,
        "--notes", f"Auto-release for version {version}",
        "--draft=false"  # ⬅️ Add this
    ], check=True)
    print("Release uploaded successfully.")

def main():
    version = extract_version(BOT_FILE)
    build_bot()
    create_release_with_gh(version, DIST_EXE)

if __name__ == "__main__":
    main()
