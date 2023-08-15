from internal.game_controller import set_on_tick_listener, is_game_created, get_resolution, disable_bot
from internal.lord import Lord, LordDoesNotExistException


class Game:
    def __init__(self):
        self.tick_listeners = []
        set_on_tick_listener(self.publish)
        self.replaced_default_bots = {}
        self.set_on_tick_listener(self.tick_replaced_default_bots)

    def replace_default_bot(self, default_bot, new_bot):
        if default_bot not in self.replaced_default_bots:
            self.disable_bot(default_bot)
            self.replaced_default_bots[default_bot] = new_bot

    def tick_replaced_default_bots(self):
        for i in range(1, 9):
            try:
                lord = Lord.get_lord(i)
                if lord.get_bot() in self.replaced_default_bots:
                    self.replaced_default_bots[lord.get_bot()].tick(lord)
            except LordDoesNotExistException:
                pass


    def is_game_loaded(self):
        pass

    def set_game_speed(self, speed):
        pass

    def zoom_in(self):
        pass

    def zoom_out(self):
        pass

    def publish(self):
        for tick_listener in self.tick_listeners:
            tick_listener()

    def set_on_tick_listener(self, tick_listener):
        self.tick_listeners.append(tick_listener)

    def is_game_created(self):
        return is_game_created()

    def get_resolution(self):
        return get_resolution()

    def disable_bot(self, bot_id):
        disable_bot(bot_id)
