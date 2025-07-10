import ctypes
import time

# Define necessary structures
class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        class _MOUSEINPUT(ctypes.Structure):
            _fields_ = [
                ("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
            ]
        _fields_ = [("mi", _MOUSEINPUT)]
    _anonymous_ = ("_input",)
    _fields_ = [("type", ctypes.c_ulong), ("_input", _INPUT)]

# Constants
INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_MOVE_RELATIVE = 0x0000  # just for clarity

# Create SendInput function
SendInput = ctypes.windll.user32.SendInput

def move_mouse_relative(dx, dy):
    extra = ctypes.c_ulong(0)
    mi = INPUT._INPUT._MOUSEINPUT(dx=dx, dy=dy, mouseData=0,
                                   dwFlags=MOUSEEVENTF_MOVE,
                                   time=0,
                                   dwExtraInfo=ctypes.pointer(extra))
    inp = INPUT(type=INPUT_MOUSE, _input=INPUT._INPUT(mi=mi))
    SendInput(1, ctypes.pointer(inp), ctypes.sizeof(inp))

# Example: move mouse to the right for 2 seconds

time.sleep(5)

for _ in range(500):
    move_mouse_relative(5, 0)
    time.sleep(0.01)
