from enum import Enum

from internal.game_controller import train_unit, place_wall, place_building, buy, sell, get_tax, set_tax, \
    set_rations, get_rations, count_golds, count_woods, count_hops, count_stones, count_irons, count_pitches, \
    count_wheats, count_ales, count_flours, count_breads, count_cheeses, count_meats, count_apples, count_bows, \
    count_spears, count_maces, count_crossbows, count_pikes, count_leather_armor, count_metal_armor, is_lord_exist, \
    has_market, get_my_lord, get_bot


class LordDoesNotExistException(Exception):
    def __init__(self, lord_id):
        self.lord_id = lord_id

    def __str__(self):
        return f"Lord {self.lord_id} doesn't exist."


class GoodType(Enum):
    WOOD = 2
    HOP = 3
    STONE = 4
    IRON = 6
    PITCH = 7
    WHEAT = 9
    BREAD = 10
    CHEESE = 11
    MEAT = 12
    FRUIT = 13
    ALE = 14
    FLOUR = 16
    BOW = 17
    CROSSBOW = 18
    SPEAR = 19
    PIKE = 20
    MACE = 21
    SWORD = 22
    LEATHER_ARMOR = 23
    METAL_ARMOR = 24


class Lord:
    """
    Represents a lord with a unique identifier.

    :param lord_id: The identifier for the lord.
    :type lord_id: int

    :raises LordDoesNotExistException: If the lord with the given ID does not exist.
    """

    def __init__(self, lord_id):
        self.lord_id = lord_id
        if not self.is_exist():
            raise LordDoesNotExistException(lord_id)
        self.count_methods = {
            GoodType.WOOD: self.count_woods,
            GoodType.STONE: self.count_stones,
            GoodType.HOP: self.count_hops,
            GoodType.IRON: self.count_irons,
            GoodType.PITCH: self.count_pitches,
            GoodType.WHEAT: self.count_wheats,
            GoodType.BREAD: self.count_breads,
            GoodType.CHEESE: self.count_cheeses,
            GoodType.MEAT: self.count_meats,
            GoodType.FRUIT: self.count_apples,
            GoodType.ALE: self.count_ales,
            GoodType.FLOUR: self.count_flours,
            GoodType.BOW: self.count_bows,
            GoodType.CROSSBOW: self.count_crossbows,
            GoodType.SPEAR: self.count_spears,
            GoodType.PIKE: self.count_pikes,
            GoodType.MACE: self.count_maces,
            GoodType.LEATHER_ARMOR: self.count_leather_armor,
            GoodType.METAL_ARMOR: self.count_metal_armor,
        }

    def get_id(self):
        """
        Get the identifier of the lord.

        :return: The identifier of the lord.
        :rtype: int
        """
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


    def place_wall(self, x, y):
        self._lord_should_exist()
        place_wall(self.lord_id, x, y)

    def place_building(self, building, y, x):
        self._lord_should_exist()
        place_building(self.lord_id, building, x, y)

    def buy(self, good_type: GoodType, number_of_good_to_buy):
        self._lord_should_exist()
        buy(number_of_good_to_buy, good_type.value, self.lord_id)

    def sell(self, good_type: GoodType, number_of_good_to_sell):
        self._lord_should_exist()
        sell(number_of_good_to_sell, good_type.value, self.lord_id)

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
        """
        Count the amount of golds owned by the lord.

        :return: The count of golds.
        :rtype: int
        """
        self._lord_should_exist()
        return count_golds(self.lord_id)

    def count_woods(self):
        """
        Count the amount of woods owned by the lord.

        :return: The count of woods.
        :rtype: int
        """
        self._lord_should_exist()
        return count_woods(self.lord_id)

    def count_hops(self):
        """
        Count the amount of hops owned by the lord.

        :return: The count of hops.
        :rtype: int
        """
        self._lord_should_exist()
        return count_hops(self.lord_id)

    def count_stones(self):
        """
        Count the amount of stones owned by the lord.

        :return: The count of stones.
        :rtype: int
        """
        self._lord_should_exist()
        return count_stones(self.lord_id)

    def count_irons(self):
        """
        Count the amount of irons owned by the lord.

        :return: The count of irons.
        :rtype: int
        """
        self._lord_should_exist()
        return count_irons(self.lord_id)

    def count_pitches(self):
        """
        Count the amount of pitches owned by the lord.

        :return: The count of pitches.
        :rtype: int
        """
        self._lord_should_exist()
        return count_pitches(self.lord_id)

    def count_wheats(self):
        """
        Count the amount of wheats owned by the lord.

        :return: The count of wheats.
        :rtype: int
        """
        self._lord_should_exist()
        return count_wheats(self.lord_id)

    def count_ales(self):
        """
        Count the amount of ales owned by the lord.

        :return: The count of ales.
        :rtype: int
        """
        self._lord_should_exist()
        return count_ales(self.lord_id)

    def count_flours(self):
        """
        Count the amount of flours owned by the lord.

        :return: The count of flours.
        :rtype: int
        """
        self._lord_should_exist()
        return count_flours(self.lord_id)

    def count_breads(self):
        """
        Count the amount of breads owned by the lord.

        :return: The count of breads.
        :rtype: int
        """
        self._lord_should_exist()
        return count_breads(self.lord_id)

    def count_cheeses(self):
        """
        Count the amount of cheeses owned by the lord.

        :return: The count of cheeses.
        :rtype: int
        """
        self._lord_should_exist()
        return count_cheeses(self.lord_id)

    def count_meats(self):
        """
        Count the amount of meats owned by the lord.

        :return: The count of meats.
        :rtype: int
        """
        self._lord_should_exist()
        return count_meats(self.lord_id)

    def count_apples(self):
        """
        Count the amount of apples owned by the lord.

        :return: The count of apples.
        :rtype: int
        """
        self._lord_should_exist()
        return count_apples(self.lord_id)

    def count_bows(self):
        """
        Count the amount of bows owned by the lord.

        :return: The count of bows.
        :rtype: int
        """
        self._lord_should_exist()
        return count_bows(self.lord_id)

    def count_spears(self):
        """
        Count the amount of spears owned by the lord.

        :return: The count of spears.
        :rtype: int
        """
        self._lord_should_exist()
        return count_spears(self.lord_id)

    def count_maces(self):
        """
        Count the amount of maces owned by the lord.

        :return: The count of maces.
        :rtype: int
        """
        self._lord_should_exist()
        return count_maces(self.lord_id)

    def count_crossbows(self):
        """
        Count the amount of crossbows owned by the lord.

        :return: The count of crossbows.
        :rtype: int
        """
        self._lord_should_exist()
        return count_crossbows(self.lord_id)

    def count_pikes(self):
        """
        Count the amount of pikes owned by the lord.

        :return: The count of pikes.
        :rtype: int
        """
        self._lord_should_exist()
        return count_pikes(self.lord_id)

    def count_leather_armor(self):
        """
        Count the amount of leather armor owned by the lord.

        :return: The count of leather_armor.
        :rtype: int
        """
        self._lord_should_exist()
        return count_leather_armor(self.lord_id)

    def count_metal_armor(self):
        """
        Count the amount of metal armor owned by the lord.

        :return: The count of metal armor.
        :rtype: int
        """
        self._lord_should_exist()
        return count_metal_armor(self.lord_id)

    def count_good(self, good_type: GoodType) -> int:
        """
        Get the amount of a specific type of good owned by the lord.

        :param good_type: The type of the good.
        :type good_type: GoodType

        :return: The amount of the specified good.
        :rtype int
        """
        count_method = self.count_methods.get(good_type)

        if count_method:
            return count_method()
        else:
            raise ValueError("Invalid good type")

    def has_market(self):
        self._lord_should_exist()
        return has_market(self.lord_id)

    def get_bot(self):
        self._lord_should_exist()
        return get_bot(self.lord_id)
