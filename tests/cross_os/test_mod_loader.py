from unittest import TestCase

from cross_os.call_recorder import CallRecorder
from internal.mod_loader import ModLoader
from internal.mod_repository import ModRepository, DirectoryManager
from common.file_system import FileSystem


class TestModLoader(TestCase):
    def test_load(self):
        CallRecorder.reset()
        directory_manager = DirectoryManager()
        file_manager = FileSystem()

        mod_repository = ModRepository("./tests/cross_os/mods", directory_manager, file_manager)

        mod_loader = ModLoader(mod_repository)
        mod_loader.load_mods()

        self.assertEqual(2, CallRecorder.get_called())

    def test_load_disable_mods_should_not_load(self):
        CallRecorder.reset()
        directory_manager = DirectoryManager()
        file_manager = FileSystem()

        mod_repository = ModRepository("./tests/cross_os/mods2", directory_manager, file_manager)

        mod_loader = ModLoader(mod_repository)
        mod_loader.load_mods()

        self.assertEqual(3, CallRecorder.get_called())
