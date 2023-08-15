import struct

from internal.image_converter.image import Pixel, Color, Image


class BMPParser:
    def parse(self, buffer):
        image = Image()
        image.width = struct.unpack("<i", buffer[18:22])[0]
        image.height = struct.unpack("<i", buffer[22:26])[0]
        pixel_array_offset = struct.unpack("<i", buffer[10:14])[0]

        if image.height < 0:
            image.height = -image.height

        if image.width < 0:
            image.width = -image.width

        pixels = []

        offset = pixel_array_offset  # Start of pixel data
        for y in range(image.height):
            new_line_pixels = []
            for x in range(image.width):
                blue = buffer[offset]
                green = buffer[offset + 1]
                red = buffer[offset + 2]
                alpha = buffer[offset + 3]

                pixel = Pixel((x, y), Color(red, green, blue, alpha))
                new_line_pixels.append(pixel)

                offset += 4  # Each pixel is represented by 4 bytes (RGBA)

            if image.width > 0:
                new_line_pixels.reverse()

            pixels.extend(new_line_pixels)
        if image.height > 0:
            pixels.reverse()

        image.pixels = pixels
        return image


if __name__ == '__main__':
    bmp_parser = BMPParser()
    with open("test.bmp", 'rb') as bmp:
        parsed_image = bmp_parser.parse(bmp.read())
        with open("test.ppm", "w") as tgx:
            tgx.write("P3\n")
            tgx.write("# test.ppm\n")
            tgx.write(f"{parsed_image.width} {parsed_image.height}\n")
            tgx.write("255\n")
            for i in parsed_image.pixels:
                tgx.write(str(i.color.red) + " ")
                tgx.write(str(i.color.green) + " ")
                tgx.write(str(i.color.blue) + " ")
