import sys
import unittest
import ctypes


class JumpCodeGenerator:
    def __init__(self, library_path):
        self.lib = ctypes.CDLL(library_path)

    def generate_code(self, target_address, instruction_location):
        machine_code = self.lib.generate_jump_near_machine_code(target_address, instruction_location)
        size = 5
        machine_code_bytes = ctypes.string_at(machine_code, size)
        self.lib.free_memory(machine_code)
        return machine_code_bytes


@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
class TestJumpCodeGenerator(unittest.TestCase):
    def setUp(self):
        self.jump_code_generator = JumpCodeGenerator('./game_controller.dll')

    def test_jump_code_generation(self):
        target_address = 0x123456
        instruction_location = 0x0

        machine_code_bytes = self.jump_code_generator.generate_code(target_address, instruction_location)

        self.assertEqual(machine_code_bytes, b'\xe9\x51\x34\x12\x00')

    def test_jump_code_generation_with_instruction_location(self):
        target_address = 0x123456
        instruction_location = 0x00021000

        machine_code_bytes = self.jump_code_generator.generate_code(target_address, instruction_location)

        self.assertEqual(machine_code_bytes, b'\xe9\x51\x24\x10\x00')


if __name__ == '__main__':
    unittest.main()
