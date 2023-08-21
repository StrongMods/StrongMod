import struct

from common.image_converter.image import Image, Pixel, Color, TgxTokenType


class TgxImageParser:
    def parse(self, buffer):

        image = Image()
        width, height = TgxImageParser.extract_image_dimension(buffer)

        image.width = width
        image.height = height

        offset = 8

        pixels = TgxImageParser.make_pixels(height, width)

        y = 0
        x = 0
        while offset < len(buffer):
            token, length = TgxImageParser.extract_token(buffer, offset)

            if token == TgxTokenType.NEW_LINE:
                y = y + 1
                x = x - image.width
                offset = offset + 1

            elif token == TgxTokenType.REPEATER:
                color = TgxImageParser.get_color(buffer, offset + 1)
                for i in range(length):
                    pixels[(x + (y * width))] = Pixel((x, y), color[0])
                    x = x + 1

                offset = offset + 3

            elif token == TgxTokenType.STREAM:
                colors = TgxImageParser.get_color(buffer, offset + 1, length)
                for color in colors:
                    pixels[(x + (y * width))] = Pixel((x, y), color)
                    x = x + 1
                offset += 1 + length * 2

            elif token == TgxTokenType.TRANSPARENT:
                x = x + length
                offset = offset + 1

            else:
                raise ValueError(f"Encountered an unknown TGX token type: {token}")

        image.pixels = pixels
        return image

    @staticmethod
    def make_pixels(height, width):
        pixels = []
        for y in range(height):
            for x in range(width):
                pixels.append(Pixel((x, y), Color(0, 0, 0, 0)))
        return pixels

    @staticmethod
    def extract_image_dimension(buffer):
        width = struct.unpack('<H', buffer[0:2])[0]
        height = struct.unpack('<H', buffer[4:6])[0]
        return width, height

    @staticmethod
    def extract_token(buffer, offset=0):
        token_header = buffer[offset]
        token_type = f"{(token_header & 0b11100000) >> 5:03b}"
        length = (token_header & 0b00011111) + 1
        return token_type, length

    @staticmethod
    def get_color(buffer, start, length=1):
        colors = []
        for i in range(length):
            color_buffer = buffer[start + i * 2: start + i * 2 + 2]
            binary_color_buffer = "{0:08b}".format(color_buffer[0]) + "{0:08b}".format(color_buffer[1])
            multiplier = 8.2258

            red = round(int(binary_color_buffer[9:14], 2) * multiplier)
            green = round((int(binary_color_buffer[14: 16] + binary_color_buffer[0: 3], 2)) * multiplier)
            blue = round(int(binary_color_buffer[3: 8], 2) * multiplier)

            colors.append(Color(red, green, blue, 255))
        return colors


if __name__ == '__main__':

    with open('armys1.tgx', 'rb') as file:
        buffer = file.read()
        tgx_image_converter = TgxImageParser()
        parsed_image = tgx_image_converter.parse(buffer)

        with open("test.bmp", 'wb') as bmp:
            # Write the bmp header
            bmp.write(b'BM')
            bmp.write((0).to_bytes(4, 'little'))  # File size
            bmp.write(b'\x00\x00')  # Reserved
            bmp.write(b'\x00\x00')  # Reserved
            bmp.write((54).to_bytes(4, 'little'))  # Offset

            # Write the dib header
            bmp.write((40).to_bytes(4, 'little'))  # DIB header size
            bmp.write(parsed_image.width.to_bytes(4, 'little'))  # Image width
            bmp.write(struct.pack("<i", -parsed_image.height))  # Image height
            bmp.write((1).to_bytes(2, 'little'))  # Color planes
            bmp.write((32).to_bytes(2, 'little'))  # Bits per pixel
            bmp.write((0).to_bytes(4, 'little'))  # Compression method
            bmp.write((0).to_bytes(4, 'little'))  # Image size (uncompressed)
            bmp.write((0).to_bytes(4, 'little'))  # Horizontal resolution
            bmp.write((0).to_bytes(4, 'little'))  # Vertical resolution
            bmp.write((0).to_bytes(4, 'little'))  # Number of colors in the palette
            bmp.write((0).to_bytes(4, 'little'))  # Number of important colors

            # Write the image data in reverse order (BGR)
            for pixel in parsed_image.pixels:
                bmp.write(struct.pack("BBBB", pixel.color.blue, pixel.color.green, pixel.color.red, pixel.color.alpha))
            file_size = bmp.tell()
