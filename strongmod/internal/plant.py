from internal.game_controller import get_all_plants, is_tree, get_plant_position, can_woodcutter_cut


class Plant:
    def __init__(self, plant_id, index):
        self._id = plant_id
        self._index = index

    def get_id(self):
        return self._id

    def get_position(self):
        position = get_plant_position(self._index)
        return position.x, position.y

    def is_tree(self):
        return is_tree(self._index)

    def can_woodcutter_cut(self):
        return can_woodcutter_cut(self._index)

    @classmethod
    def get_all_plants(cls):
        plants = []
        for plant in get_all_plants():
            plants.append(Plant(plant[1], plant[0]))
        return plants
