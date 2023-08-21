from common.singleton import Singleton
from internal.game_controller import set_on_ui_tick_listener, show_image, get_mouse_position, is_mouse_clicked, \
    disable_mouse_in_game
from common.image_converter.bmp_parser import BMPParser
from common.image_converter.tgx_builder import TgxImageBuilder


class Image:
    def __init__(self, width, height, tokens):
        self.width = width
        self.height = height
        self.tokens = tokens


class Ui(metaclass=Singleton):
    def __init__(self):
        self.tick_listeners = []
        set_on_ui_tick_listener(self.publish)

    def publish(self):
        for tick_listener in self.tick_listeners:
            tick_listener()

    def set_on_tick_listener(self, tick_listener):
        self.tick_listeners.append(tick_listener)

    @staticmethod
    def load_image(image_path):
        bmp_parser = BMPParser()
        with open(image_path, 'rb') as bmp:
            image = bmp_parser.parse(bmp.read())
        builder = TgxImageBuilder()
        tokens = builder.build(image)
        return Image(image.width, image.height, tokens)

    @staticmethod
    def is_mouse_on_image(mouse_x, mouse_y, image_x, image_y, image_width, image_height):
        image_right = image_x + image_width
        image_bottom = image_y + image_height
        return image_x <= mouse_x <= image_right and image_y <= mouse_y <= image_bottom

    @staticmethod
    def image_button(image, x, y):
        show_image(image.tokens, image.height, image.width, x, y)
        if Ui.is_mouse_on_image(get_mouse_position().x, get_mouse_position().y, x, y, image.width, image.height):
            disable_mouse_in_game()

        if is_mouse_clicked() is True and Ui.is_mouse_on_image(get_mouse_position().x, get_mouse_position().y, x, y, image.width, image.height):
            return True

        return False
