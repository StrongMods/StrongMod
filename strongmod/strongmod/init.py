import ctypes
import sys
from ctypes import CDLL
import time

from common.file_system import FileSystem
from internal.mod_loader import ModLoader
from internal.mod_repository import ModRepository, DirectoryManager

_game_controller = CDLL("./strongmod/game_controller.dll")
if _game_controller.is_extreme() == 1:
    _game_controller = CDLL("./strongmod/game_controller_extreme.dll")


kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
kernel32.AllocConsole()

sys.stdout = open('CONOUT$', 'w')
sys.stderr = open('CONOUT$', 'w')

sys.stdin = open('CONIN$', 'r')


@ctypes.CFUNCTYPE(ctypes.c_void_p)
def handle_ui_tick_event():
    pass


_game_controller.execute_callback_on_ui_tick(handle_ui_tick_event)
directory_manager = DirectoryManager()
file_manager = FileSystem()


ModLoader(ModRepository("./strongmod/mods", directory_manager, file_manager)).load_mods()

while True:
    time.sleep(1)
