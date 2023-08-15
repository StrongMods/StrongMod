from internal.game_controller import get_unit_owner, get_all_units, get_unit_id, get_unit_type


class UnitDoesNotExistException(Exception):
    def __init__(self, unit_id):
        self.unit_id = unit_id

    def __str__(self):
        return f"Unit {self.unit_id} doesn't exist."


class Unit:
    def __init__(self, unit_id, index):
        self._id = unit_id
        self._index = index

    def get_id(self):
        return self._id

    def get_owner(self):
        self._throw_exception_if_unit_does_not_exist()
        return get_unit_owner(self._index)

    def is_exist(self):
        return get_unit_id(self._index) == self._id

    @classmethod
    def get_all_units(cls):
        units = []
        for unit in get_all_units():
            units.append(Unit(unit[1], unit[0]))
        return units

    def get_unit_type(self):
        self._throw_exception_if_unit_does_not_exist()
        return get_unit_type(self._index)

    def _throw_exception_if_unit_does_not_exist(self):
        if not self.is_exist():
            raise UnitDoesNotExistException(self._id)
