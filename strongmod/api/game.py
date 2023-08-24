from common.singleton import Singleton
from internal.game_controller import set_on_tick_listener, is_game_created, get_resolution, disable_bot, show_message, \
    set_on_game_begin_listener
from api.lord import Lord, LordDoesNotExistException


class Game(metaclass=Singleton):
    def __init__(self):
        self.tick_listeners = []
        set_on_game_begin_listener(self.publish_game_begin)
        self.game_begin_listeners = []
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

    def show_message(self, title, message):
        """
         Display a message in the chat.

         This method allows the game to show a message in the chat

        :param title: The title of the message.
        :type title: str

        :param message: The content of the message.
        :type message: str

        :Example:
         game = Game()

         game.show_message("hello,", "world")
        """
        show_message(title, message)

    def publish_game_begin(self):
        for game_begin_listener in self.game_begin_listeners:
            game_begin_listener()

    def register_game_begin_listener(self, game_begin_listener):
        """
        Register a listener to be notified when the game begins.

        The registered listener will be called when the game begins, such as when
        a saved game is loaded or when the game editor starts, etc.

        :param game_begin_listener: A callable object, such as a
            function or method, to be notified when the game begins.
        :type game_begin_listener: callable

        :Example:
            game = Game()

            def game_begin_listener():
                game.show_message("hello,", "world")

            game.register_game_begin_listener(game_begin_listener)
        """
        self.game_begin_listeners.append(game_begin_listener)
