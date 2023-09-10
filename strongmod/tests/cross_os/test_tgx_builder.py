from unittest import TestCase

from common.image_converter.image import TgxTokenType, Image, Pixel, Color
from common.image_converter.tgx_builder import TgxImageBuilder


class TestTgxBuilder(TestCase):
    def test_build(self):
        image = Image()
        image.width = 4
        image.height = 2
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(255, 255, 0, 255)),  # Yellow
            Pixel((2, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((3, 0), Color(255, 255, 0, 255)),  # Yellow

            Pixel((0, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 1), Color(255, 255, 0, 255)),  # Yellow
            Pixel((2, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((3, 1), Color(255, 255, 0, 255))  # Yellow
        ]

        builder = TgxImageBuilder()
        tokens = builder.build(image)

        # 00000100__00011111_00000000__11100000_01111111__00011111_00000000__11100000_01111111__10000000__
        # 00000100__00011111_00000000__11100000_01111111__00011111_00000000__11100000_01111111
        self.assertEqual(b"\x03\x1F\x00\x60\xff\x1F\x00\x60\xff\x80\x03\x1F\x00\x60\xff\x1F\x00\x60\xff\x80\x80", tokens)

    # \x60\xff
    def test_repeater_build(self):
        image = Image()
        image.width = 4
        image.height = 2
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((2, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((3, 0), Color(0, 0, 255, 255)),  # Blue

            Pixel((0, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((2, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((3, 1), Color(0, 0, 255, 255))  # Blue
        ]

        builder = TgxImageBuilder()
        tokens = builder.build(image)

        self.assertEqual(b"\x00\x1F\x00\x42\x1F\x00\x80\x43\x1F\x00\x80\x80", tokens)

    def test_convert_to_tokens_one_pixel(self):
        image = Image()
        image.width = 1
        image.height = 1
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 0, [Color(0, 0, 255, 255)])]
        self.assertListEqual(expected_tokens, tokens)

    def test_convert_to_tokens_two_pixel(self):
        image = Image()
        image.width = 2
        image.height = 1
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(255, 255, 0, 255))  # Yellow
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 1, [Color(0, 0, 255, 255), Color(255, 255, 0, 255)])]
        self.assertListEqual(expected_tokens, tokens)

    def test_convert_to_tokens_two_pixel_in_two_row(self):
        image = Image()
        image.width = 1
        image.height = 2
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((0, 1), Color(255, 255, 0, 255))  # Yellow
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 0, [Color(0, 0, 255, 255)]),
                           (TgxTokenType.NEW_LINE,),
                           (TgxTokenType.STREAM, 0, [Color(255, 255, 0, 255)])]
        self.assertListEqual(expected_tokens, tokens)

    def test_convert_to_tokens_four_pixel_two_row_and_two_column(self):
        image = Image()
        image.width = 2
        image.height = 2
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(255, 255, 0, 255)),  # Yellow

            Pixel((0, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 1), Color(255, 255, 0, 255))  # Yellow
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 1, [Color(0, 0, 255, 255),
                                                     Color(255, 255, 0, 255)]),
                           (TgxTokenType.NEW_LINE,),
                           (TgxTokenType.STREAM, 1, [Color(0, 0, 255, 255),
                                                     Color(255, 255, 0, 255)])]
        self.assertListEqual(expected_tokens, tokens)

    def test_convert_to_tokens_four_repeated_color(self):
        image = Image()
        image.width = 4
        image.height = 1
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((2, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((3, 0), Color(0, 0, 255, 255))   # Blue
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 0, [Color(0, 0, 255, 255)]), (TgxTokenType.REPEATER, 2, Color(0, 0, 255, 255))]
        self.assertListEqual(expected_tokens, tokens)

    def test_convert_to_tokens_repeater_four_pixel_two_row_and_two_column(self):
        image = Image()
        image.width = 2
        image.height = 2
        image.pixels = [
            Pixel((0, 0), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 0), Color(0, 0, 255, 255)),  # Blue

            Pixel((0, 1), Color(0, 0, 255, 255)),  # Blue
            Pixel((1, 1), Color(0, 0, 255, 255))   # Blue
        ]

        builder = TgxImageBuilder()
        tokens = builder.convert_to_tokens(image)
        expected_tokens = [(TgxTokenType.STREAM, 0, [Color(0, 0, 255, 255)]),
                           (TgxTokenType.REPEATER, 0, Color(0, 0, 255, 255)),
                           (TgxTokenType.NEW_LINE,),
                           (TgxTokenType.REPEATER, 1, Color(0, 0, 255, 255))]
        self.assertListEqual(expected_tokens, tokens)
