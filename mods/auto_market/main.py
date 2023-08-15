import api
from api import ui, game

load_image = ui.load_image

main_menu = ui.load_image("./mods/auto_market/images/main_menu.bmp")

wood = ui.load_image("./mods/auto_market/images/wood.bmp")
hops = ui.load_image("./mods/auto_market/images/hops.bmp")
stone = ui.load_image("./mods/auto_market/images/stone.bmp")
iron = ui.load_image("./mods/auto_market/images/iron.bmp")
pitch = ui.load_image("./mods/auto_market/images/pitch.bmp")
wheat = ui.load_image("./mods/auto_market/images/wheat.bmp")
bread = ui.load_image("./mods/auto_market/images/bread.bmp")
cheese = ui.load_image("./mods/auto_market/images/cheese.bmp")
meat = ui.load_image("./mods/auto_market/images/meat.bmp")
fruit = ui.load_image("./mods/auto_market/images/fruit.bmp")
ale = ui.load_image("./mods/auto_market/images/ale.bmp")
flour = ui.load_image("./mods/auto_market/images/flour.bmp")
bows = ui.load_image("./mods/auto_market/images/bows.bmp")
crossbows = ui.load_image("./mods/auto_market/images/crossbows.bmp")
spears = ui.load_image("./mods/auto_market/images/spears.bmp")
pikes = ui.load_image("./mods/auto_market/images/pikes.bmp")
maces = ui.load_image("./mods/auto_market/images/maces.bmp")
swords = ui.load_image("./mods/auto_market/images/swords.bmp")
leather_armor = ui.load_image("./mods/auto_market/images/leather_armor.bmp")
metal_armor = ui.load_image("./mods/auto_market/images/metal_armor.bmp")

auto_market_icon = ui.load_image("./mods/auto_market/images/auto_market_icon.bmp")
close = ui.load_image("./mods/auto_market/images/close.bmp")
good_selected_menu = ui.load_image("./mods/auto_market/images/good_selected_menu.bmp")

unselected_number = ui.load_image("./mods/auto_market/images/unselected_number.bmp")
selected_number = ui.load_image("./mods/auto_market/images/selected_number.bmp")

number_5 = ui.load_image("./mods/auto_market/images/5.bmp")
number_10 = ui.load_image("./mods/auto_market/images/10.bmp")
number_15 = ui.load_image("./mods/auto_market/images/15.bmp")
number_20 = ui.load_image("./mods/auto_market/images/20.bmp")
number_25 = ui.load_image("./mods/auto_market/images/25.bmp")
number_30 = ui.load_image("./mods/auto_market/images/30.bmp")
number_35 = ui.load_image("./mods/auto_market/images/35.bmp")
number_40 = ui.load_image("./mods/auto_market/images/40.bmp")
number_45 = ui.load_image("./mods/auto_market/images/45.bmp")
number_50 = ui.load_image("./mods/auto_market/images/50.bmp")
number_55 = ui.load_image("./mods/auto_market/images/55.bmp")
number_60 = ui.load_image("./mods/auto_market/images/60.bmp")
number_65 = ui.load_image("./mods/auto_market/images/65.bmp")
number_70 = ui.load_image("./mods/auto_market/images/70.bmp")
number_75 = ui.load_image("./mods/auto_market/images/75.bmp")
number_80 = ui.load_image("./mods/auto_market/images/80.bmp")
number_85 = ui.load_image("./mods/auto_market/images/85.bmp")
number_90 = ui.load_image("./mods/auto_market/images/90.bmp")
number_95 = ui.load_image("./mods/auto_market/images/95.bmp")
number_100 = ui.load_image("./mods/auto_market/images/100.bmp")

numbers = {5: number_5, 10: number_10, 15: number_15, 20: number_20, 25: number_25, 30: number_30, 35: number_35,
           40: number_40, 45: number_45, 50: number_50, 55: number_55, 60: number_60, 65: number_65, 70: number_70,
           75: number_75, 80: number_80, 85: number_85, 90: number_90, 95: number_95, 100: number_100}
sell = ui.load_image("./mods/auto_market/images/sell.bmp")
buy = ui.load_image("./mods/auto_market/images/buy.bmp")

reset = ui.load_image("./mods/auto_market/images/reset.bmp")

back = ui.load_image("./mods/auto_market/images/back.bmp")


class MenuStatus:
    is_market_menu_open = False
    is_good_selected = False
    selected_good = None
    list_of_number_of_goods_to_sell = {"wood": -1, "stone": -1,
                                       "hops": -1,
                                       "iron": -1,
                                       "pitch": -1,
                                       "wheat": -1,
                                       "bread": -1,
                                       "cheese": -1,
                                       "meat": -1,
                                       "fruit": -1,
                                       "ale": -1,
                                       "flour": -1,
                                       "bows": -1,
                                       "crossbows": -1,
                                       "spears": -1,
                                       "pikes": -1,
                                       "maces": -1,
                                       "swords": -1,
                                       "leather_armor": -1,
                                       "metal_armor": -1}
    list_of_number_of_goods_to_buy = {"wood": -1, "stone": -1,
                                      "hops": -1,
                                      "iron": -1,
                                      "pitch": -1,
                                      "wheat": -1,
                                      "bread": -1,
                                      "cheese": -1,
                                      "meat": -1,
                                      "fruit": -1,
                                      "ale": -1,
                                      "flour": -1,
                                      "bows": -1,
                                      "crossbows": -1,
                                      "spears": -1,
                                      "pikes": -1,
                                      "maces": -1,
                                      "swords": -1,
                                      "leather_armor": -1,
                                      "metal_armor": -1}


def on_ui_tick_listener():
    if game.is_game_created():
        my_lord = api.get_my_lord()

        if not my_lord.has_market():
            return

        if not MenuStatus.is_market_menu_open:
            if ui.image_button(auto_market_icon, game.get_resolution().width - auto_market_icon.width, 1):
                MenuStatus.is_market_menu_open = True
                MenuStatus.is_good_selected = False
        elif MenuStatus.is_good_selected is False and MenuStatus.is_market_menu_open:
            x_offset = game.get_resolution().width / 2
            y_offset = (game.get_resolution().height / 2) - 50
            ui.image_button(main_menu, int(x_offset - (main_menu.width / 2)),
                            int(y_offset - (main_menu.height / 2)))

            if ui.image_button(close, ((int(x_offset - (main_menu.width / 2)) + main_menu.width) - close.width),
                               int(y_offset - (main_menu.height / 2))):
                MenuStatus.is_market_menu_open = False
            elif ui.image_button(wood, int(x_offset - (wood.width / 2) - (wood.width * 1)),
                                 int(y_offset - (wood.height / 2)) - (wood.height * 2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "wood"

            elif ui.image_button(stone, int(x_offset - (stone.width / 2) - (stone.width * 0)),
                                 int(y_offset - (stone.height / 2)) - (stone.height * 2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "stone"

            elif ui.image_button(hops, int(x_offset - (hops.width / 2) - (hops.width * -1)),
                                 int(y_offset - (hops.height / 2)) - (hops.height * 2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "hops"

            elif ui.image_button(iron, int(x_offset - (iron.width / 2) - (iron.width * 1)),
                                 int(y_offset - (iron.height / 2)) - (iron.height * 1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "iron"

            elif ui.image_button(pitch, int(x_offset - (pitch.width / 2) - (pitch.width * 0)),
                                 int(y_offset - (pitch.height / 2)) - (pitch.height * 1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "pitch"

            elif ui.image_button(wheat, int(x_offset - (wheat.width / 2) - (wheat.width * -1)),
                                 int(y_offset - (wheat.height / 2)) - (wheat.height * 1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "wheat"

            elif ui.image_button(bread, int(x_offset - (bread.width / 2) - (bread.width * 1)),
                                 int(y_offset - (bread.height / 2)) - (bread.height * 0)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "bread"

            elif ui.image_button(cheese, int(x_offset - (cheese.width / 2) - (cheese.width * 0)),
                                 int(y_offset - (cheese.height / 2)) - (cheese.height * 0)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "cheese"

            elif ui.image_button(meat, int(x_offset - (meat.width / 2) - (meat.width * -1)),
                                 int(y_offset - (meat.height / 2)) - (meat.height * 0)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "meat"

            elif ui.image_button(fruit, int(x_offset - (fruit.width / 2) - (fruit.width * 1)),
                                 int(y_offset - (fruit.height / 2)) - (fruit.height * -1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "fruit"

            elif ui.image_button(ale, int(x_offset - (ale.width / 2) - (ale.width * 0)),
                                 int(y_offset - (ale.height / 2)) - (ale.height * -1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "ale"

            elif ui.image_button(flour, int(x_offset - (flour.width / 2) - (flour.width * -1)),
                                 int(y_offset - (flour.height / 2)) - (flour.height * -1)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "flour"

            elif ui.image_button(bows, int(x_offset - (bows.width / 2) - (bows.width * 1)),
                                 int(y_offset - (bows.height / 2)) - (bows.height * -2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "bows"

            elif ui.image_button(crossbows, int(x_offset - (crossbows.width / 2) - (crossbows.width * 0)),
                                 int(y_offset - (crossbows.height / 2)) - (crossbows.height * -2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "crossbows"


            elif ui.image_button(spears, int(x_offset - (spears.width / 2) - (spears.width * -1)),
                                 int(y_offset - (spears.height / 2)) - (spears.height * -2)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "spears"


            elif ui.image_button(pikes, int(x_offset - (pikes.width / 2) - (pikes.width * 0)),
                                 int(y_offset - (pikes.height / 2)) - (pikes.height * -3)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "pikes"

            elif ui.image_button(maces, int(x_offset - (maces.width / 2) - (maces.width * 1)),
                                 int(y_offset - (maces.height / 2)) - (maces.height * -3)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "maces"

            elif ui.image_button(swords, int(x_offset - (swords.width / 2) - (swords.width * -1)),
                                 int(y_offset - (swords.height / 2)) - (swords.height * -3)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "swords"

            elif ui.image_button(leather_armor, int(x_offset - (leather_armor.width / 2) - (leather_armor.width * 0)),
                                 int(y_offset - (leather_armor.height / 2)) - (leather_armor.height * -4)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "leather_armor"

            elif ui.image_button(metal_armor, int(x_offset - (metal_armor.width / 2) - (metal_armor.width * 1)),
                                 int(y_offset - (metal_armor.height / 2)) - (metal_armor.height * -4)):
                MenuStatus.is_good_selected = True
                MenuStatus.selected_good = "metal_armor"

        elif MenuStatus.is_good_selected is True and MenuStatus.is_market_menu_open:
            x_offset = game.get_resolution().width / 2
            y_offset = (game.get_resolution().height / 2) - 50
            ui.image_button(good_selected_menu, int(x_offset - (good_selected_menu.width / 2)),
                            int(y_offset - (good_selected_menu.height / 2)))

            if ui.image_button(back, (
                    (int(x_offset - (good_selected_menu.width / 2))) - back.width),
                               int(y_offset - (good_selected_menu.height / 2))):
                MenuStatus.is_good_selected = False

            if ui.image_button(close, (
                    (int(x_offset - (good_selected_menu.width / 2)) + good_selected_menu.width) - close.width),
                               int(y_offset - (good_selected_menu.height / 2))):
                MenuStatus.is_market_menu_open = False
                MenuStatus.is_good_selected = False

            ui.image_button(sell, int(x_offset - (sell.width / 2)) - 290,
                            int(y_offset - (sell.height / 2)) - (sell.height * 2) + 20)

            if ui.image_button(reset, int(x_offset - (sell.width / 2)) - 290,
                               int(y_offset - (sell.height / 2)) - (sell.height * 2) + 20 - 30):
                MenuStatus.list_of_number_of_goods_to_sell[MenuStatus.selected_good] = -1

            ui.image_button(buy, int(x_offset - (buy.width / 2)) - 290,
                            int(y_offset - (buy.height / 2)) + ((buy.height * 1) + 10))

            if ui.image_button(reset, int(x_offset - (buy.width / 2)) - 290,
                               int(y_offset - (buy.height / 2)) + ((buy.height * 1) + 10) - 30):
                MenuStatus.list_of_number_of_goods_to_buy[MenuStatus.selected_good] = -1

            for j, k in enumerate(range(5, 100, 5)):

                ui.image_button(numbers.get(k), (int(x_offset - sell.width) - 230) + (j * (sell.width - 10)),
                                int(y_offset - (sell.height / 2)) - (sell.height * 2) + 20)
                if MenuStatus.list_of_number_of_goods_to_sell.get(MenuStatus.selected_good) == k:
                    ui.image_button(selected_number, (int(x_offset - sell.width) - 230) + (j * (sell.width - 10)),
                                    int(y_offset - (sell.height / 2)) - (sell.height * 2) + 40)
                else:
                    if ui.image_button(unselected_number, (int(x_offset - sell.width) - 230) + (j * (sell.width - 10)),
                                       int(y_offset - (sell.height / 2)) - (sell.height * 2) + 40):
                        MenuStatus.list_of_number_of_goods_to_sell[MenuStatus.selected_good] = k

            for j, k in enumerate(range(5, 100, 5)):

                ui.image_button(numbers.get(k), (int(x_offset - buy.width) - 230) + (j * (buy.width - 10)),
                                int(y_offset - (buy.height / 2)) + (buy.height * 1) + 10)
                if MenuStatus.list_of_number_of_goods_to_buy.get(MenuStatus.selected_good) == k:
                    ui.image_button(selected_number, (int(x_offset - buy.width) - 230) + (j * (buy.width - 10)),
                                    int(y_offset - (buy.height / 2)) + (buy.height * 1) + 30)
                else:
                    if ui.image_button(unselected_number, (int(x_offset - buy.width) - 230) + (j * (buy.width - 10)),
                                       int(y_offset - (buy.height / 2)) + (buy.height * 1) + 30):
                        MenuStatus.list_of_number_of_goods_to_buy[MenuStatus.selected_good] = k


def on_game_tick_listener():
    my_lord = api.get_my_lord()
    for good, number_of_good_to_sell in MenuStatus.list_of_number_of_goods_to_sell.items():
        if good == "wood" and number_of_good_to_sell != -1 and my_lord.count_woods() >= number_of_good_to_sell:
            my_lord.sell(2, 5)
        if good == "hops" and number_of_good_to_sell != -1 and my_lord.count_hops() >= number_of_good_to_sell:
            my_lord.sell(3, 5)

        if good == "stone" and number_of_good_to_sell != -1 and my_lord.count_stones() >= number_of_good_to_sell:
            my_lord.sell(4, 5)

        if good == "iron" and number_of_good_to_sell != -1 and my_lord.count_irons() >= number_of_good_to_sell:
            my_lord.sell(6, 5)

        if good == "pitch" and number_of_good_to_sell != -1 and my_lord.count_pitches() >= number_of_good_to_sell:
            my_lord.sell(7, 5)

        if good == "wheat" and number_of_good_to_sell != -1 and my_lord.count_wheats() >= number_of_good_to_sell:
            my_lord.sell(9, 5)

        if good == "bread" and number_of_good_to_sell != -1 and my_lord.count_breads() >= number_of_good_to_sell:
            my_lord.sell(10, 5)

        if good == "cheese" and number_of_good_to_sell != -1 and my_lord.count_cheeses() >= number_of_good_to_sell:
            my_lord.sell(11, 5)

        if good == "meat" and number_of_good_to_sell != -1 and my_lord.count_meats() >= number_of_good_to_sell:
            my_lord.sell(12, 5)

        if good == "fruit" and number_of_good_to_sell != -1 and my_lord.count_apples() >= number_of_good_to_sell:
            my_lord.sell(13, 5)

        if good == "ale" and number_of_good_to_sell != -1 and my_lord.count_ales() >= number_of_good_to_sell:
            my_lord.sell(14, 5)

        if good == "flour" and number_of_good_to_sell != -1 and my_lord.count_flours() >= number_of_good_to_sell:
            my_lord.sell(16, 5)

        if good == "bows" and number_of_good_to_sell != -1 and my_lord.count_bows() >= number_of_good_to_sell:
            my_lord.sell(17, 5)

        if good == "crossbows" and number_of_good_to_sell != -1 and my_lord.count_crossbows() >= number_of_good_to_sell:
            my_lord.sell(18, 5)

        if good == "spears" and number_of_good_to_sell != -1 and my_lord.count_spears() >= number_of_good_to_sell:
            my_lord.sell(19, 5)

        if good == "pikes" and number_of_good_to_sell != -1 and my_lord.count_pikes() >= number_of_good_to_sell:
            my_lord.sell(20, 5)

        if good == "maces" and number_of_good_to_sell != -1 and my_lord.count_maces() >= number_of_good_to_sell:
            my_lord.sell(21, 5)

        # if good == "swords" and number_of_good_to_sell != -1 and my_lord.count_() >= number_of_good_to_sell:
        #     my_lord.sell(2, 5)

        if good == "leather_armor" and number_of_good_to_sell != -1 and my_lord.count_leather_armor() >= number_of_good_to_sell:
            my_lord.sell(23, 5)

        if good == "metal_armor" and number_of_good_to_sell != -1 and my_lord.count_metal_armor() >= number_of_good_to_sell:
            my_lord.sell(24, 5)

    for good, number_of_good_to_buy in MenuStatus.list_of_number_of_goods_to_buy.items():
        if good == "wood" and number_of_good_to_buy != -1 and my_lord.count_woods() <= number_of_good_to_buy:
            my_lord.buy(2, 5)
        if good == "hops" and number_of_good_to_buy != -1 and my_lord.count_hops() <= number_of_good_to_buy:
            my_lord.buy(3, 5)

        if good == "stone" and number_of_good_to_buy != -1 and my_lord.count_stones() <= number_of_good_to_buy:
            my_lord.buy(4, 5)

        if good == "iron" and number_of_good_to_buy != -1 and my_lord.count_irons() <= number_of_good_to_buy:
            my_lord.buy(6, 5)

        if good == "pitch" and number_of_good_to_buy != -1 and my_lord.count_pitches() <= number_of_good_to_buy:
            my_lord.buy(7, 5)

        if good == "wheat" and number_of_good_to_buy != -1 and my_lord.count_wheats() <= number_of_good_to_buy:
            my_lord.buy(9, 5)

        if good == "bread" and number_of_good_to_buy != -1 and my_lord.count_breads() <= number_of_good_to_buy:
            my_lord.buy(10, 5)

        if good == "cheese" and number_of_good_to_buy != -1 and my_lord.count_cheeses() <= number_of_good_to_buy:
            my_lord.buy(11, 5)

        if good == "meat" and number_of_good_to_buy != -1 and my_lord.count_meats() <= number_of_good_to_buy:
            my_lord.buy(12, 5)

        if good == "fruit" and number_of_good_to_buy != -1 and my_lord.count_apples() <= number_of_good_to_buy:
            my_lord.buy(13, 5)

        if good == "ale" and number_of_good_to_buy != -1 and my_lord.count_ales() <= number_of_good_to_buy:
            my_lord.buy(14, 5)

        if good == "flour" and number_of_good_to_buy != -1 and my_lord.count_flours() <= number_of_good_to_buy:
            my_lord.buy(16, 5)

        if good == "bows" and number_of_good_to_buy != -1 and my_lord.count_bows() <= number_of_good_to_buy:
            my_lord.buy(17, 5)

        if good == "crossbows" and number_of_good_to_buy != -1 and my_lord.count_crossbows() <= number_of_good_to_buy:
            my_lord.buy(18, 5)

        if good == "spears" and number_of_good_to_buy != -1 and my_lord.count_spears() <= number_of_good_to_buy:
            my_lord.buy(19, 5)

        if good == "pikes" and number_of_good_to_buy != -1 and my_lord.count_pikes() <= number_of_good_to_buy:
            my_lord.buy(20, 5)

        if good == "maces" and number_of_good_to_buy != -1 and my_lord.count_maces() <= number_of_good_to_buy:
            my_lord.buy(21, 5)

        # if good == "swords" and number_of_good_to_buy != -1 and my_lord.count_() <= number_of_good_to_buy:
        #     my_lord.buy(2, 5)

        if good == "leather_armor" and number_of_good_to_buy != -1 and my_lord.count_leather_armor() <= number_of_good_to_buy:
            my_lord.buy(23, 5)

        if good == "metal_armor" and number_of_good_to_buy != -1 and my_lord.count_metal_armor() <= number_of_good_to_buy:
            my_lord.buy(24, 5)


ui.set_on_tick_listener(on_ui_tick_listener)
game.set_on_tick_listener(on_game_tick_listener)
