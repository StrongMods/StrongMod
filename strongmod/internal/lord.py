from internal.game_controller import train_unit, move_units, place_wall, place_building, buy, sell, get_tax, set_tax, \
    set_rations, get_rations, count_golds, count_woods, count_hops, count_stones, count_irons, count_pitches, \
    count_wheats, count_ales, count_flours, count_breads, count_cheeses, count_meats, count_apples, count_bows, \
    count_spears, count_maces, count_crossbows, count_pikes, count_leather_armor, count_metal_armor, is_lord_exist, \
    has_market, get_my_lord, get_bot


class LordDoesNotExistException(Exception):
    def __init__(self, lord_id):
        self.lord_id = lord_id

    def __str__(self):
        return f"Lord {self.lord_id} doesn't exist."


class Lord:
    def __init__(self, lord_id):
        self.lord_id = lord_id
        if not self.is_exist():
            raise LordDoesNotExistException(lord_id)

    def get_id(self):
        return self.lord_id

    @classmethod
    def get_lord(cls, lord_id):
        return Lord(lord_id)

    @classmethod
    def get_my_lord(cls):
        return Lord.get_lord(get_my_lord())

    def is_exist(self):
        return is_lord_exist(self.lord_id) and (9 > self.lord_id > 0)

    def _lord_should_exist(self):
        if not self.is_exist():
            raise LordDoesNotExistException(self.lord_id)

    def train_unit(self, unit):
        self._lord_should_exist()
        train_unit(self.lord_id, unit)

    def move_units(self, units, x, y):
        self._lord_should_exist()
        move_units(units, x, y)

    def place_wall(self, x, y):
        self._lord_should_exist()
        place_wall(self.lord_id, x, y)

    def place_building(self, building, y, x):
        self._lord_should_exist()
        place_building(self.lord_id, building, x, y)

    def buy(self, good, number_of_good_to_buy):
        self._lord_should_exist()
        buy(number_of_good_to_buy, good, self.lord_id)

    def sell(self, good, number_of_good_to_sell):
        self._lord_should_exist()
        sell(number_of_good_to_sell, good, self.lord_id)

    def get_tax(self):
        self._lord_should_exist()
        return get_tax(self.lord_id)

    def set_tax(self, tax):
        self._lord_should_exist()
        set_tax(self.lord_id, tax)

    def set_rations(self, rations):
        self._lord_should_exist()
        set_rations(self.lord_id, rations)

    def get_rations(self):
        self._lord_should_exist()
        return get_rations(self.lord_id)

    def count_golds(self):
        self._lord_should_exist()
        return count_golds(self.lord_id)

    def count_woods(self):
        self._lord_should_exist()
        return count_woods(self.lord_id)

    def count_hops(self):
        self._lord_should_exist()
        return count_hops(self.lord_id)

    def count_stones(self):
        self._lord_should_exist()
        return count_stones(self.lord_id)

    def count_irons(self):
        self._lord_should_exist()
        return count_irons(self.lord_id)

    def count_pitches(self):
        self._lord_should_exist()
        return count_pitches(self.lord_id)

    def count_wheats(self):
        self._lord_should_exist()
        return count_wheats(self.lord_id)

    def count_ales(self):
        self._lord_should_exist()
        return count_ales(self.lord_id)

    def count_flours(self):
        self._lord_should_exist()
        return count_flours(self.lord_id)

    def count_breads(self):
        self._lord_should_exist()
        return count_breads(self.lord_id)

    def count_cheeses(self):
        self._lord_should_exist()
        return count_cheeses(self.lord_id)

    def count_meats(self):
        self._lord_should_exist()
        return count_meats(self.lord_id)

    def count_apples(self):
        self._lord_should_exist()
        return count_apples(self.lord_id)

    def count_bows(self):
        self._lord_should_exist()
        return count_bows(self.lord_id)

    def count_spears(self):
        self._lord_should_exist()
        return count_spears(self.lord_id)

    def count_maces(self):
        self._lord_should_exist()
        return count_maces(self.lord_id)

    def count_crossbows(self):
        self._lord_should_exist()
        return count_crossbows(self.lord_id)

    def count_pikes(self):
        self._lord_should_exist()
        return count_pikes(self.lord_id)

    def count_leather_armor(self):
        self._lord_should_exist()
        return count_leather_armor(self.lord_id)

    def count_metal_armor(self):
        self._lord_should_exist()
        return count_metal_armor(self.lord_id)

    def has_market(self):
        self._lord_should_exist()
        return has_market(self.lord_id)

    def get_bot(self):
        self._lord_should_exist()
        return get_bot(self.lord_id)
