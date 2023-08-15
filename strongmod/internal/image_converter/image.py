class Image:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.pixels = []


class Pixel:
    def __init__(self, position, color):
        self.position = position
        self.color = color

    def __repr__(self):
        return "position: " + str(self.position) + ", " + str(self.color)

    def __eq__(self, other):
        return self.position == other.position and self.color == other.color


class Color:
    def __init__(self, red, green, blue, alpha):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue and \
               self.alpha == other.alpha

    def __repr__(self):
        return "Color(" + "red: " + str(self.red) + ", green:" + str(self.green) + ", blue:" + str(self.blue) \
               + ", alpha:" + str(self.alpha) + ")"


class TgxTokenType:
    STREAM = '000'
    NEW_LINE = '100'
    REPEATER = '010'
    TRANSPARENT = '001'
