from enum import Enum

from internal.game_controller import get_building_position, get_all_buildings, get_building_type, get_building_owner, \
    get_keep_building
from api.lord import Lord


class BuildingType(Enum):
    UNKNOWN = 0
    WOODCUTTER = 1


class Building:
    def __init__(self, building_id, index=None):
        self._id = building_id
        self._index = index

    def get_id(self):
        return self._id

    def get_position(self):
        position = get_building_position(self._index)
        return position.x, position.y

    @classmethod
    def get_all_buildings(cls):
        buildings = []
        for plant in get_all_buildings():
            buildings.append(Building(plant[1], plant[0]))
        return buildings

    def get_lord_keep(self, lord):
        keep = get_keep_building(lord.get_id())
        return Building(keep.id, keep.index)

    def get_building_type(self):
        if get_building_type(self._index) == 3:
            return BuildingType.WOODCUTTER
        else:
            return BuildingType.UNKNOWN

    def get_owner(self):
        return Lord.get_lord(get_building_owner(self._index))
