from enum import IntEnum

from internal.building import Building, BuildingType
from internal.game import Game
from internal.plant import Plant
from internal.ui import Ui
from internal.unit import Unit
from internal.lord import Lord

unit = Unit
plant = Plant
building = Building
get_lord = Lord.get_lord
get_my_lord = Lord.get_my_lord
game = Game()
ui = Ui()


class DefaultBots(IntEnum):
    RAT = 1


class Bot:
    def tick(self, lord):
        pass


BuildingType = BuildingType
