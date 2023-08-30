import ctypes

from api import Game
from internal.game_controller import get_last_message, last_message, show_message, \
    place_wall, train_unit, zoom_in, zoom_out, buy, sell, set_game_speed, \
    get_unit_owner, place_building


class SaveOldLastMessage:
    old_last_message = ""


def on_tick_listener():
    get_last_message(ctypes.byref(last_message))
    context = last_message.context.decode()
    player = last_message.player
    if last_message.context.decode() != SaveOldLastMessage.old_last_message:
        SaveOldLastMessage.old_last_message = last_message.context.decode()
        if len(context.split()) == 3 and context.split()[0] == "train_unit":
            show_message(str(train_unit(int(context.split()[1]), int(context.split()[2]))).encode())
        elif len(context.split()) == 4 and context.split()[0] == "place_wall":
            show_message(str(place_wall(int(context.split()[1]), int(context.split()[2]),
                                        int(context.split()[3]))).encode())
        elif len(context.split()) == 4 and context.split()[0] == "place_20_walls":
            for i in range(int(context.split()[2]), int(context.split()[2]) + 20):
                show_message(str(place_wall(int(context.split()[1]), i, int(context.split()[3]))).encode())
            for i in range(int(context.split()[2]), int(context.split()[2]) + 20):
                show_message(str(place_wall(int(context.split()[1]), i, int(context.split()[3]) + 20)).encode())
            for i in range(int(context.split()[3]), int(context.split()[3]) + 20):
                show_message(str(place_wall(int(context.split()[1]), int(context.split()[2]) + 20, i)).encode())
            for i in range(int(context.split()[3]), int(context.split()[3]) + 20):
                show_message(str(place_wall(int(context.split()[1]), int(context.split()[2]), i)).encode())
        elif len(context.split()) == 2 and context.split()[0] == "get_character_owner":
            show_message(str(get_unit_owner(int(context.split()[1]))).encode())
        elif len(context.split()) == 1 and context.split()[0] == "zoom_in":
            show_message(str(zoom_in().encode()))
        elif len(context.split()) == 1 and context.split()[0] == "zoom_out":
            show_message(str(zoom_out().encode()))
        elif len(context.split()) == 4 and context.split()[0] == "buy":
            show_message(str(buy(int(context.split()[1]), int(context.split()[2]), int(context.split()[3]))).encode())
        elif len(context.split()) == 4 and context.split()[0] == "sell":
            show_message(str(sell(int(context.split()[1]), int(context.split()[2]), int(context.split()[3]))).encode())
        elif len(context.split()) == 2 and context.split()[0] == "set_game_speed":
            show_message(str(set_game_speed(int(context.split()[1]))).encode())
        elif len(context.split()) == 5 and context.split()[0] == "place_building":
            show_message(str(place_building(int(context.split()[1]), int(context.split()[2]),
                                            int(context.split()[3]),
                                            int(context.split()[4]))).encode())


game = Game()
game.set_on_tick_listener(on_tick_listener)
