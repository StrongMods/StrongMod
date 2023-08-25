import copy

from api import Lord
from api import GoodType
from api import Ui
from api import Game

ui = Ui()
game = Game()

load_image = ui.load_image

images_path = "./mods/auto_market/images"

load_images = ui.load_images

# Load good images
good_image_names = [good_type.name.lower() for good_type in GoodType]
loaded_good_images = load_images(images_path, good_image_names)
loaded_good_images = {GoodType[good_type.upper()]: image for good_type, image in loaded_good_images.items()}

# Load number images
number_image_names = [f"{i}" for i in range(5, 105, 5)]
loaded_number_images = load_images(images_path, number_image_names)


# Load other specific images
loaded_other_images = load_images(images_path, ["auto_market_icon", "close", "good_selected_menu", "unselected_number",
                                                "selected_number", "sell", "buy", "reset", "back", "main_menu"])

# Combine all loaded images into a single dictionary
loaded_images = {}
loaded_images.update(loaded_good_images)
loaded_images.update(loaded_other_images)
loaded_images.update(loaded_number_images)

default_list_of_number_of_goods = {
    good_type: -1 for good_type in GoodType
}


class MenuStatus:
    is_market_menu_open = False
    is_good_selected = False
    selected_good = None
    list_of_number_of_goods_to_sell = copy.copy(default_list_of_number_of_goods)
    list_of_number_of_goods_to_buy = copy.copy(default_list_of_number_of_goods)


def on_ui_tick_listener():
    if game.is_game_created():
        my_lord = Lord.get_my_lord()

        if not my_lord.has_market():
            return

        if not MenuStatus.is_market_menu_open:
            if ui.image_button(loaded_images.get("auto_market_icon"),
                               game.get_resolution().width - loaded_images.get("auto_market_icon").width, 1):
                MenuStatus.is_market_menu_open = True
                MenuStatus.is_good_selected = False
        elif MenuStatus.is_good_selected is False and MenuStatus.is_market_menu_open:
            x_offset = game.get_resolution().width / 2
            y_offset = (game.get_resolution().height / 2) - 50
            ui.image_button(loaded_images.get("main_menu"), int(x_offset - (loaded_images.get("main_menu").width / 2)),
                            int(y_offset - (loaded_images.get("main_menu").height / 2)))

            if ui.image_button(loaded_images.get("close"),
                               ((int(x_offset - (loaded_images.get("main_menu").width / 2)) +
                                 loaded_images.get("main_menu").width) -
                                loaded_images.get("close").width),
                               int(y_offset - (loaded_images.get("main_menu").height / 2))):
                MenuStatus.is_market_menu_open = False

            for i, good_type in enumerate(GoodType):
                x_offset_multiplier = i % 3 - 1
                y_offset_multiplier = -(i // 3) + 2
                if ui.image_button(loaded_good_images.get(good_type),
                                   int(x_offset - (loaded_good_images.get(good_type).width / 2) -
                                       (loaded_good_images.get(good_type).width * x_offset_multiplier)),
                                   int(y_offset - loaded_good_images.get(good_type).height) -
                                   (loaded_good_images.get(good_type).height * y_offset_multiplier)):
                    MenuStatus.is_good_selected = True
                    MenuStatus.selected_good = good_type

        elif MenuStatus.is_good_selected is True and MenuStatus.is_market_menu_open:
            x_offset = game.get_resolution().width / 2
            y_offset = (game.get_resolution().height / 2) - 50
            ui.image_button(loaded_images.get("good_selected_menu"),
                            int(x_offset - (loaded_images.get("good_selected_menu").width / 2)),
                            int(y_offset - (loaded_images.get("good_selected_menu").height / 2)))

            if ui.image_button(loaded_images.get("back"), (
                    (int(x_offset - (loaded_images.get("good_selected_menu").width / 2)))
                    - loaded_images.get("back").width),
                               int(y_offset - (loaded_images.get("good_selected_menu").height / 2))):
                MenuStatus.is_good_selected = False

            if ui.image_button(loaded_images.get("close"), (
                    (int(x_offset - (loaded_images.get("good_selected_menu").width / 2))
                     + loaded_images.get("good_selected_menu").width) - loaded_images.get("close").width),
                               int(y_offset - (loaded_images.get("good_selected_menu").height / 2))):
                MenuStatus.is_market_menu_open = False
                MenuStatus.is_good_selected = False

            ui.image_button(loaded_images.get("sell"), int(x_offset - (loaded_images.get("sell").width / 2)) - 290,
                            int(y_offset - (loaded_images.get("sell").height / 2)) -
                            (loaded_images.get("sell").height * 2) + 20)

            if ui.image_button(loaded_images.get("reset"), int(x_offset - (loaded_images.get("sell").width / 2)) - 290,
                               int(y_offset - (loaded_images.get("sell").height / 2)) -
                               (loaded_images.get("sell").height * 2) + 20 - 30):
                MenuStatus.list_of_number_of_goods_to_sell[MenuStatus.selected_good] = -1

            ui.image_button(loaded_images.get("buy"), int(x_offset - (loaded_images.get("buy").width / 2)) - 290,
                            int(y_offset - (loaded_images.get("buy").height / 2)) +
                            ((loaded_images.get("buy").height * 1) + 10))

            if ui.image_button(loaded_images.get("reset"), int(x_offset - (loaded_images.get("buy").width / 2)) - 290,
                               int(y_offset - (loaded_images.get("buy").height / 2)) +
                               ((loaded_images.get("buy").height * 1) + 10) - 30):
                MenuStatus.list_of_number_of_goods_to_buy[MenuStatus.selected_good] = -1

            for j, k in enumerate(range(5, 100, 5)):

                ui.image_button(loaded_images.get(str(k)),
                                (int(x_offset - loaded_images.get("sell").width) - 230) +
                                (j * (loaded_images.get("sell").width - 10)),
                                int(y_offset - (loaded_images.get("sell").height / 2)) -
                                (loaded_images.get("sell").height * 2) + 20)
                if MenuStatus.list_of_number_of_goods_to_sell.get(MenuStatus.selected_good) == k:
                    ui.image_button(loaded_images.get("selected_number"),
                                    (int(x_offset - loaded_images.get("sell").width) - 230) +
                                    (j * (loaded_images.get("sell").width - 10)),
                                    int(y_offset - (loaded_images.get("sell").height / 2)) -
                                    (loaded_images.get("sell").height * 2) + 40)
                else:
                    if ui.image_button(loaded_images.get("unselected_number"),
                                       (int(x_offset - loaded_images.get("sell").width) - 230) +
                                       (j * (loaded_images.get("sell").width - 10)),
                                       int(y_offset - (loaded_images.get("sell").height / 2)) -
                                       (loaded_images.get("sell").height * 2) + 40):
                        MenuStatus.list_of_number_of_goods_to_sell[MenuStatus.selected_good] = k

            for j, k in enumerate(range(5, 100, 5)):

                ui.image_button(loaded_images.get(str(k)),
                                (int(x_offset - loaded_images.get("buy").width) - 230) +
                                (j * (loaded_images.get("buy").width - 10)),
                                int(y_offset - (loaded_images.get("buy").height / 2)) +
                                (loaded_images.get("buy").height * 1) + 10)
                if MenuStatus.list_of_number_of_goods_to_buy.get(MenuStatus.selected_good) == k:
                    ui.image_button(loaded_images.get("selected_number"),
                                    (int(x_offset - loaded_images.get("buy").width) - 230) +
                                    (j * (loaded_images.get("buy").width - 10)),
                                    int(y_offset - (loaded_images.get("buy").height / 2)) +
                                    (loaded_images.get("buy").height * 1) + 30)
                else:
                    if ui.image_button(loaded_images.get("unselected_number"),
                                       (int(x_offset - loaded_images.get("buy").width) - 230) +
                                       (j * (loaded_images.get("buy").width - 10)),
                                       int(y_offset - (loaded_images.get("buy").height / 2)) +
                                       (loaded_images.get("buy").height * 1) + 30):
                        MenuStatus.list_of_number_of_goods_to_buy[MenuStatus.selected_good] = k


def on_game_tick_listener():
    my_lord = Lord.get_my_lord()
    for good_type, number_of_good_to_sell in MenuStatus.list_of_number_of_goods_to_sell.items():
        if number_of_good_to_sell != -1:
            count = my_lord.count_good(good_type)
            if count >= number_of_good_to_sell:
                my_lord.sell(good_type, 5)

    for good_type, number_of_good_to_buy in MenuStatus.list_of_number_of_goods_to_buy.items():
        if number_of_good_to_buy != -1:
            count = my_lord.count_good(good_type)
            if count <= number_of_good_to_buy:
                my_lord.buy(good_type, 5)


def on_game_begin():
    # Rest auto market state
    MenuStatus.list_of_number_of_goods_to_sell = copy.copy(default_list_of_number_of_goods)
    MenuStatus.list_of_number_of_goods_to_buy = copy.copy(default_list_of_number_of_goods)


ui.set_on_tick_listener(on_ui_tick_listener)
game.set_on_tick_listener(on_game_tick_listener)
game.register_game_begin_listener(on_game_begin)
