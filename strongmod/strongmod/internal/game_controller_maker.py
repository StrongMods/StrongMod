from ctypes import CDLL


class GameControllerMaker:
    def make_game_controller(self):
        _game_controller = CDLL("./strongmod/game_controller.dll")
        if _game_controller.is_extreme() == 1:
            _game_controller = CDLL("./strongmod/game_controller_extreme.dll")
        return _game_controller
