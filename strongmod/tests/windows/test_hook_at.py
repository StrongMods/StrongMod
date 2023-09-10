import ctypes
import sys
import unittest


class FunctionHooker:
    def __init__(self, library_path):
        self.lib = ctypes.CDLL(library_path)

    def hook(self, original_func, hook_func):
        self.lib.hook_at(ctypes.cast(original_func, ctypes.c_void_p).value,
                         ctypes.cast(hook_func, ctypes.c_void_p).value)


@unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
class TestFunctionHook(unittest.TestCase):

    def test_hook(self):
        hooker = FunctionHooker('./game_controller.dll')

        @ctypes.CFUNCTYPE(ctypes.c_int)
        def original():
            return False

        @ctypes.CFUNCTYPE(ctypes.c_int)
        def hook():
            return True

        self.assertFalse(original())

        hooker.hook(original, hook)

        self.assertTrue(original())


if __name__ == '__main__':
    unittest.main()
