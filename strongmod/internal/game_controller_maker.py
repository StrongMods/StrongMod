from ctypes import CDLL


class GameControllerMaker:
    def make_game_controller(self):
        return CDLL("./game_controller.dll")
