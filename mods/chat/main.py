import ctypes

from api.game import Game
from internal.game_controller import get_last_message, last_message, send_message, \
    place_wall, train_unit, zoom_in, zoom_out, buy, sell, set_game_speed, \
    get_unit_owner, move_units, place_building


class SaveOldLastMessage:
    old_last_message = ""


def on_tick_listener():
    get_last_message(ctypes.byref(last_message))
    context = last_message.context.decode()
    player = last_message.player
    if last_message.context.decode() != SaveOldLastMessage.old_last_message:
        SaveOldLastMessage.old_last_message = last_message.context.decode()
        print(player, context)
        if len(context.split()) == 3 and context.split()[0] == "train_unit":
            send_message(b"train_unit", str(train_unit(int(context.split()[1]), int(context.split()[2]))).encode())

        elif len(context.split()) == 4 and context.split()[0] == "move_units":
            print(move_units([int(context.split()[1])], int(context.split()[2]), int(context.split()[3])))

        elif len(context.split()) == 4 and context.split()[0] == "place_wall":
            send_message(b"place_wall", str(place_wall(int(context.split()[1]), int(context.split()[2]),
                                                       int(context.split()[3]))).encode())
        elif len(context.split()) == 4 and context.split()[0] == "place_20_walls":
            for i in range(int(context.split()[2]), int(context.split()[2]) + 20):
                send_message(b"place_20_walls",
                             str(place_wall(int(context.split()[1]), i, int(context.split()[3]))).encode())
            for i in range(int(context.split()[2]), int(context.split()[2]) + 20):
                send_message(b"place_20_walls",
                             str(place_wall(int(context.split()[1]), i, int(context.split()[3]) + 20)).encode())
            for i in range(int(context.split()[3]), int(context.split()[3]) + 20):
                send_message(b"place_20_walls",
                             str(place_wall(int(context.split()[1]), int(context.split()[2]) + 20, i)).encode())
            for i in range(int(context.split()[3]), int(context.split()[3]) + 20):
                send_message(b"place_20_walls",
                             str(place_wall(int(context.split()[1]), int(context.split()[2]), i)).encode())
        elif len(context.split()) == 2 and context.split()[0] == "get_character_owner":
            send_message(b"get_character_owner", str(get_unit_owner(int(context.split()[1]))).encode())
        elif len(context.split()) == 1 and context.split()[0] == "zoom_in":
            send_message(b"zoom_in", str(zoom_in().encode()))
        elif len(context.split()) == 1 and context.split()[0] == "zoom_out":
            send_message(b"zoom_out", str(zoom_out().encode()))
        elif len(context.split()) == 4 and context.split()[0] == "buy":
            send_message(b"buy",
                         str(buy(int(context.split()[1]), int(context.split()[2]), int(context.split()[3]))).encode())
        elif len(context.split()) == 4 and context.split()[0] == "sell":
            send_message(b"sell",
                         str(sell(int(context.split()[1]), int(context.split()[2]), int(context.split()[3]))).encode())
        elif len(context.split()) == 2 and context.split()[0] == "set_game_speed":
            send_message(b"set_game_speed", str(set_game_speed(int(context.split()[1]))).encode())
        elif len(context.split()) == 5 and context.split()[0] == "place_building":
            send_message(b"place_building", str(place_building(int(context.split()[1]), int(context.split()[2]),
                                                               int(context.split()[3]),
                                                               int(context.split()[4]))).encode())


game = Game()
game.set_on_tick_listener(on_tick_listener)
