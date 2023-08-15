from internal.image_converter.image import TgxTokenType


class TgxImageBuilder:

    def build(self, image):
        buffer = b""

        tokens = self.convert_to_tokens(image)
        for token in tokens:
            if token[0] == TgxTokenType.STREAM:
                buffer += self.binary_string_to_byte(TgxTokenType.STREAM + bin(token[1])[2:].zfill(5))
                for color in token[2]:
                    red_binary = bin(round(color.red / 255 * 31))[2:]
                    green_binary = bin(round(color.green / 255 * 31))[2:]
                    blue_binary = bin(round(color.blue / 255 * 31))[2:]
                    red_binary = red_binary.zfill(5)
                    green_binary = green_binary.zfill(5)
                    blue_binary = blue_binary.zfill(5)

                    buffer += self.binary_string_to_byte(green_binary[3:] + blue_binary) + \
                              self.binary_string_to_byte(red_binary + green_binary[:3])
            elif token[0] == TgxTokenType.REPEATER:
                # print(token[1], bin(token[1]), TgxTokenType.REPEATER + bin(token[1])[2:].zfill(5))
                buffer += self.binary_string_to_byte(TgxTokenType.REPEATER + bin(token[1])[2:].zfill(5))
                red_binary = bin(round(token[2].red / 255 * 31))[2:]
                green_binary = bin(round(token[2].green / 255 * 31))[2:]
                blue_binary = bin(round(token[2].blue / 255 * 31))[2:]
                red_binary = red_binary.zfill(5)
                green_binary = green_binary.zfill(5)
                blue_binary = blue_binary.zfill(5)
                buffer += self.binary_string_to_byte(green_binary[3:] + blue_binary) + \
                          self.binary_string_to_byte(red_binary + green_binary[:3])
            elif token[0] == TgxTokenType.NEW_LINE:
                buffer += self.binary_string_to_byte(TgxTokenType.NEW_LINE + "00000")

        return buffer + b"\x80\x80"

    def binary_string_to_byte(self, binary_string):
        if int(binary_string) == 0:
            return b"\x00"
        byte_value = int(binary_string, 2)
        return byte_value.to_bytes((byte_value.bit_length() + 7) // 8, "big")

    def is_last_pixel(self, position, width, height):
        return True if position + 1 == (width * height) else False

    def convert_to_tokens(self, image):
        pixels = image.pixels

        width = image.width
        height = image.height

        tokens = []

        stream_colors = []
        current_length = -1
        current_token = TgxTokenType.STREAM

        for position in range(width * height):
            if position == 0:
                current_length += 1
                stream_colors.append(pixels[position].color)
                current_token = TgxTokenType.STREAM
                continue

            if current_token == TgxTokenType.STREAM and not self.is_width_completed(position, width):
                if self.is_exist(pixels, position + 1):
                    if pixels[position].color == pixels[position + 1].color:
                        current_length, stream_colors = self.stream_completed(current_length, stream_colors, tokens)
                        current_token = TgxTokenType.REPEATER

            if current_token == TgxTokenType.REPEATER and not self.is_width_completed(position, width):
                if self.is_exist(pixels, position + 1):
                    if pixels[position].color != pixels[position + 1].color:
                        current_length = self.repeater_completed(current_length, pixels[position].color, tokens)
                        current_token = TgxTokenType.STREAM

            if current_token == TgxTokenType.REPEATER:
                if current_length == 31:
                    current_length = self.repeater_completed(current_length, pixels[position].color, tokens)

                if position != 0 and self.is_width_completed(position, width) and current_length != -1:
                    current_length = self.repeater_completed(current_length, pixels[position].color, tokens)
                    tokens.append((TgxTokenType.NEW_LINE,))

                current_length += 1

            elif current_token == TgxTokenType.STREAM:
                if current_length == 31:
                    current_length, stream_colors = self.stream_completed(current_length, stream_colors, tokens)

                if position != 0 and self.is_width_completed(position, width):
                    current_length, stream_colors = self.stream_completed(current_length, stream_colors, tokens)
                    tokens.append((TgxTokenType.NEW_LINE,))

                current_length += 1
                stream_colors.append(pixels[position].color)

        if current_token == TgxTokenType.STREAM:
            _, _ = self.stream_completed(current_length, stream_colors, tokens)
        elif current_token == TgxTokenType.REPEATER:
            _ = self.repeater_completed(current_length, pixels[-1].color, tokens)

        return tokens

    def is_exist(self, pixels, position):
        try:
            _ = pixels[position]
            return True
        except IndexError:
            return False

    def is_width_completed(self, position, width):
        return position % width == 0

    def stream_completed(self, current_length, stream_colors, tokens):
        tokens.append((TgxTokenType.STREAM, current_length, stream_colors))
        current_length = -1
        stream_colors = []
        return current_length, stream_colors

    def repeater_completed(self, current_length, color, tokens):
        tokens.append((TgxTokenType.REPEATER, current_length, color))
        current_length = -1
        return current_length

    def get_next_pixel(self, pixels, position, width, height):
        if not self.is_last_pixel(position, width, height):
            next_pixel = pixels[position + 1]
        else:
            next_pixel = None
        return next_pixel

    def get_current_pixel(self, pixels, position):
        return pixels[position]
