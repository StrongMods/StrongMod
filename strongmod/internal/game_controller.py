import ctypes

from internal.game_controller_maker import GameControllerMaker

gameControllerMaker = GameControllerMaker()
_game_controller = gameControllerMaker.make_game_controller()

free = _game_controller.free_memory


class Message(ctypes.Structure):
    _fields_ = [("context", ctypes.c_char_p),
                ("player", ctypes.c_int)]


def show_message(message):
    _game_controller.show_message.argtypes = [ctypes.c_char_p]
    _game_controller.show_message(str(message).encode())


train_unit = _game_controller.train_unit
train_unit.argtypes = [ctypes.c_int, ctypes.c_int]

last_message = Message()
get_last_message = _game_controller.get_last_message
get_last_message.restype = Message

_game_controller.place_wall.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
_game_controller.place_wall.restype = ctypes.c_int
place_wall = _game_controller.place_wall

_game_controller.place_building.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
_game_controller.place_building.restype = ctypes.c_int
place_building = _game_controller.place_building

_game_controller.get_unit_owner.argtypes = [ctypes.c_int]
_game_controller.get_unit_owner.restype = ctypes.c_int
get_unit_owner = _game_controller.get_unit_owner

_game_controller.is_game_loaded.argtypes = []
_game_controller.is_game_loaded.restype = ctypes.c_bool
is_game_loaded = _game_controller.is_game_loaded

_game_controller.set_game_speed.argtypes = [ctypes.c_int]
set_game_speed = _game_controller.set_game_speed

zoom_in = _game_controller.zoom_in

zoom_out = _game_controller.zoom_out

_game_controller.buy.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
buy = _game_controller.buy

_game_controller.sell.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
sell = _game_controller.sell

_game_controller.is_iron_ore.restype = ctypes.c_int
_game_controller.is_iron_ore.argtypes = [ctypes.c_int, ctypes.c_int]
is_iron = _game_controller.is_iron_ore

_game_controller.is_unit_exist.restype = ctypes.c_int
_game_controller.is_unit_exist.argtypes = [ctypes.c_int]
is_unit_exist = _game_controller.is_unit_exist

_game_controller.get_unit_id.restype = ctypes.c_int
_game_controller.get_unit_id.argtypes = [ctypes.c_int]
get_unit_id = _game_controller.get_unit_id

_game_controller.get_building_id.restype = ctypes.c_int
_game_controller.get_building_id.argtypes = [ctypes.c_int]
get_building_id = _game_controller.get_building_id


class BuildingIndexAndId(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_int),
        ('id', ctypes.c_int)
    ]


_game_controller.get_keep_building.restype = BuildingIndexAndId
_game_controller.get_keep_building.argtypes = [ctypes.c_int]
get_keep_building = _game_controller.get_keep_building

_game_controller.count_golds.restype = ctypes.c_int
_game_controller.count_golds.argtypes = [ctypes.c_int]
count_golds = _game_controller.count_golds

_game_controller.count_woods.restype = ctypes.c_int
_game_controller.count_woods.argtypes = [ctypes.c_int]
count_woods = _game_controller.count_woods

_game_controller.count_hops.restype = ctypes.c_int
_game_controller.count_hops.argtypes = [ctypes.c_int]
count_hops = _game_controller.count_hops

_game_controller.count_stones.restype = ctypes.c_int
_game_controller.count_golds.argtypes = [ctypes.c_int]
count_stones = _game_controller.count_stones

_game_controller.count_irons.restype = ctypes.c_int
_game_controller.count_irons.argtypes = [ctypes.c_int]
count_irons = _game_controller.count_irons

_game_controller.count_pitches.restype = ctypes.c_int
_game_controller.count_pitches.argtypes = [ctypes.c_int]
count_pitches = _game_controller.count_pitches

_game_controller.count_wheats.restype = ctypes.c_int
_game_controller.count_wheats.argtypes = [ctypes.c_int]
count_wheats = _game_controller.count_wheats

_game_controller.count_ales.restype = ctypes.c_int
_game_controller.count_ales.argtypes = [ctypes.c_int]
count_ales = _game_controller.count_ales

_game_controller.count_flours.restype = ctypes.c_int
_game_controller.count_flours.argtypes = [ctypes.c_int]
count_flours = _game_controller.count_flours

_game_controller.count_breads.restype = ctypes.c_int
_game_controller.count_breads.argtypes = [ctypes.c_int]
count_breads = _game_controller.count_breads

_game_controller.count_cheeses.restype = ctypes.c_int
_game_controller.count_cheeses.argtypes = [ctypes.c_int]
count_cheeses = _game_controller.count_cheeses

_game_controller.count_meats.restype = ctypes.c_int
_game_controller.count_meats.argtypes = [ctypes.c_int]
count_meats = _game_controller.count_meats

_game_controller.count_apples.restype = ctypes.c_int
_game_controller.count_apples.argtypes = [ctypes.c_int]
count_apples = _game_controller.count_apples

_game_controller.count_bows.restype = ctypes.c_int
_game_controller.count_bows.argtypes = [ctypes.c_int]
count_bows = _game_controller.count_bows

_game_controller.count_spears.restype = ctypes.c_int
_game_controller.count_spears.argtypes = [ctypes.c_int]
count_spears = _game_controller.count_spears

_game_controller.count_maces.restype = ctypes.c_int
_game_controller.count_maces.argtypes = [ctypes.c_int]
count_maces = _game_controller.count_maces

_game_controller.count_crossbows.restype = ctypes.c_int
_game_controller.count_crossbows.argtypes = [ctypes.c_int]
count_crossbows = _game_controller.count_crossbows

_game_controller.count_pikes.restype = ctypes.c_int
_game_controller.count_pikes.argtypes = [ctypes.c_int]
count_pikes = _game_controller.count_pikes

_game_controller.count_leather_armor.restype = ctypes.c_int
_game_controller.count_leather_armor.argtypes = [ctypes.c_int]
count_leather_armor = _game_controller.count_leather_armor

_game_controller.count_metal_armor.restype = ctypes.c_int
_game_controller.count_metal_armor.argtypes = [ctypes.c_int]
count_metal_armor = _game_controller.count_metal_armor

_game_controller.set_tax.argtypes = [ctypes.c_int, ctypes.c_int]
set_tax = _game_controller.set_tax

_game_controller.get_tax.restype = ctypes.c_int
_game_controller.get_tax.argtypes = [ctypes.c_int]
get_tax = _game_controller.get_tax

_game_controller.set_rations.argtypes = [ctypes.c_int, ctypes.c_int]
set_rations = _game_controller.set_rations

_game_controller.get_rations.restype = ctypes.c_int
_game_controller.get_rations.argtypes = [ctypes.c_int]
get_rations = _game_controller.get_rations


class Position(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_int),
        ('y', ctypes.c_int)
    ]


_game_controller.get_building_position.argtypes = [ctypes.c_int]
_game_controller.get_building_position.restype = Position
get_building_position = _game_controller.get_building_position

_game_controller.is_lord_exist.restype = ctypes.c_bool
_game_controller.is_lord_exist.argtypes = [ctypes.c_int]
is_lord_exist = _game_controller.is_lord_exist

_game_controller.count_lords.restype = ctypes.c_int
count_lords = _game_controller.count_lords

_game_controller.count_units.restype = ctypes.c_int
count_units = _game_controller.count_units

_game_controller.enable_chat()


class UnitIndexAndId(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_int),
        ('id', ctypes.c_int)
    ]


class UnitIndexAndIdList(ctypes.Structure):
    _fields_ = [
        ('unitIndexAndId', UnitIndexAndId * 2500),
        ('size', ctypes.c_int)
    ]


def get_all_units():
    _game_controller.get_all_units.restype = UnitIndexAndIdList
    c_units_p = _game_controller.get_all_units()
    c_units = c_units_p
    units = []
    for i in range(c_units.size):
        index = c_units.unitIndexAndId[i].index
        id_ = c_units.unitIndexAndId[i].id
        units.append((index, id_))
    return units


_game_controller.get_unit_type.restype = ctypes.c_int
_game_controller.get_unit_type.argtypes = [ctypes.c_int]
get_unit_type = _game_controller.get_unit_type


class Listener:
    listener = None


@ctypes.CFUNCTYPE(ctypes.c_void_p)
def handle_game_tick_event():
    Listener.listener()


def set_on_tick_listener(listener):
    Listener.listener = listener

    _game_controller.execute_callback_on_game_tick(handle_game_tick_event)


class UiListener:
    listener = None


@ctypes.CFUNCTYPE(ctypes.c_void_p)
def handle_ui_tick_event():
    UiListener.listener()


def set_on_ui_tick_listener(listener):
    UiListener.listener = listener

    _game_controller.execute_callback_on_ui_tick(handle_ui_tick_event)


_game_controller.set_accessible_position_update_limit.argtypes = [ctypes.c_char]
set_accessible_position_update_limit = _game_controller.set_accessible_position_update_limit

disable_engineer_deselect = _game_controller.disable_engineer_deselect

_game_controller.is_human_lord.restype = ctypes.c_int
_game_controller.is_human_lord.argtypes = [ctypes.c_int]
is_human_lord = _game_controller.is_human_lord

disable_auto_place_stockpile = _game_controller.disable_auto_place_stockpile

disable_can_not_place_building_on_units = _game_controller.disable_can_not_place_building_on_units


def show_image(image, width, height, x, y):
    ubuffer = (ctypes.c_ubyte * len(image)).from_buffer(bytearray(image))
    _game_controller.show_image.argtypes = [ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_int, ctypes.c_int,
                                            ctypes.c_int]
    _game_controller.show_image(ubuffer, width, height, x, y)


class MousePosition(ctypes.Structure):
    _fields_ = [
        ('x', ctypes.c_int),
        ('y', ctypes.c_int)
    ]


_game_controller.get_mouse_position.restype = Position
get_mouse_position = _game_controller.get_mouse_position

_game_controller.is_mouse_clicked.restype = ctypes.c_bool
is_mouse_clicked = _game_controller.is_mouse_clicked


class Resolution(ctypes.Structure):
    _fields_ = [
        ('width', ctypes.c_int),
        ('height', ctypes.c_int)
    ]


_game_controller.get_resolution.restype = Resolution
get_resolution = _game_controller.get_resolution

disable_mouse_in_game = _game_controller.disable_mouse_in_game

_game_controller.is_game_created.restype = ctypes.c_bool
is_game_created = _game_controller.is_game_created

_game_controller.has_market.restype = ctypes.c_bool
_game_controller.has_market.argtypes = [ctypes.c_int]
has_market = _game_controller.has_market

_game_controller.get_my_lord.restype = ctypes.c_int
get_my_lord = _game_controller.get_my_lord

_game_controller.is_custom_game_open.restype = ctypes.c_bool
is_custom_game_open = _game_controller.is_custom_game_open

_game_controller.get_bot.restype = ctypes.c_int
_game_controller.get_bot.argtypes = [ctypes.c_int]
get_bot = _game_controller.get_bot

_game_controller.disable_bot.argtypes = [ctypes.c_int]
disable_bot = _game_controller.disable_bot


class PlantIndexAndId(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_int),
        ('id', ctypes.c_int)
    ]


class PlantIndexAndIdList(ctypes.Structure):
    _fields_ = [
        ('plantIndexAndId', PlantIndexAndId * 2000),
        ('size', ctypes.c_int)
    ]


def get_all_plants():
    _game_controller.get_all_plants.restype = PlantIndexAndIdList
    c_plants_p = _game_controller.get_all_plants()
    c_plants = c_plants_p
    plants = []
    for i in range(c_plants.size):
        index = c_plants.plantIndexAndId[i].index
        id_ = c_plants.plantIndexAndId[i].id
        plants.append((index, id_))
    return plants


_game_controller.is_tree.restype = ctypes.c_bool
_game_controller.is_tree.argtypes = [ctypes.c_int]
is_tree = _game_controller.is_tree

_game_controller.get_plant_position.argtypes = [ctypes.c_int]
_game_controller.get_plant_position.restype = Position
get_plant_position = _game_controller.get_plant_position

_game_controller.can_woodcutter_cut.restype = ctypes.c_bool
_game_controller.can_woodcutter_cut.argtypes = [ctypes.c_int]
can_woodcutter_cut = _game_controller.can_woodcutter_cut


class BuildingIndexAndId(ctypes.Structure):
    _fields_ = [
        ('index', ctypes.c_int),
        ('id', ctypes.c_int)
    ]


class BuildingIndexAndIdList(ctypes.Structure):
    _fields_ = [
        ('buildingIndexAndId', BuildingIndexAndId * 2000),
        ('size', ctypes.c_int)
    ]


def get_all_buildings():
    _game_controller.get_all_buildings.restype = BuildingIndexAndIdList
    c_buildings_p = _game_controller.get_all_buildings()
    c_buildings = c_buildings_p
    buildings = []
    for i in range(c_buildings.size):
        index = c_buildings.buildingIndexAndId[i].index
        id_ = c_buildings.buildingIndexAndId[i].id
        buildings.append((index, id_))
    return buildings


_game_controller.get_building_type.restype = ctypes.c_int
_game_controller.get_building_type.argtypes = [ctypes.c_int]
get_building_type = _game_controller.get_building_type

_game_controller.get_building_owner.restype = ctypes.c_short
_game_controller.get_building_owner.argtypes = [ctypes.c_int]
get_building_owner = _game_controller.get_building_owner

_game_controller.show_text.restype = ctypes.c_void_p
show_text = _game_controller.show_text


class GameBeginListener:
    listener = None


@ctypes.CFUNCTYPE(ctypes.c_void_p)
def handle_game_begin_event():
    GameBeginListener.listener()


def set_on_game_begin_listener(listener):
    GameBeginListener.listener = listener

    _game_controller.execute_callback_on_game_begin(handle_game_begin_event)
