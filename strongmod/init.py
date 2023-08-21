import ctypes
from ctypes import CDLL
from ctypes import CFUNCTYPE, c_void_p
from threading import Thread

from internal.mod_loader import ModLoader
from internal.mod_repository import ModRepository, DirectoryManager, FileManager

_game_controller = CDLL("game_controller.dll")

entry = 0x0584026
t = Thread(target=CFUNCTYPE(c_void_p)(entry))
t.start()


@ctypes.CFUNCTYPE(ctypes.c_void_p)
def handle_ui_tick_event():
    pass


_game_controller.execute_callback_on_ui_tick(handle_ui_tick_event)
directory_manager = DirectoryManager()
file_manager = FileManager()


ModLoader(ModRepository("./mods", directory_manager, file_manager)).load_mods()
t.join()
