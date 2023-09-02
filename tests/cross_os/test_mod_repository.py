from unittest import TestCase, skip

from internal.mod_repository import ModRepository, Mod


class DirectoryManagerMock:
    def __init__(self, directories):
        self.directories = directories
        self.path = ""

    def get_all_directories(self, path):
        self.path = path
        return self.directories


class FakeFileManager:
    def __init__(self, files):
        self.files = files

    def read(self, path):
        contents = self.files.get(path)
        if contents is not None:
            return contents
        else:
            raise FileNotFoundError

    def write(self, path, content):
        self.files[path] = content

    def is_exists(self, file_name):
        return True


class StubFileManager:
    def read(self, path):
        return ""

    def is_exists(self, file_name):
        return False


class TestModRepository(TestCase):
    def setUp(self):
        self.mods_path = "./mods"

    def test_find_all_mods(self):
        mod1_name = "mod1"
        mod1_description = "mod1 description"
        mod1_full_path = f"{self.mods_path}/{mod1_name}"
        mod1 = Mod(mod1_name, mod1_description, mod1_full_path)

        mod2_name = "mod2"
        mod2_description = "mod2 description"
        mod2_full_path = f"{self.mods_path}/{mod2_name}"
        mod2 = Mod(mod2_name, mod2_description, mod2_full_path)

        directory_manager = DirectoryManagerMock([mod1.name, mod2.name])
        file_manager = FakeFileManager({f"{self.mods_path}/{mod1_name}/description.txt": mod1_description,
                                        f"{self.mods_path}/{mod2_name}/description.txt": mod2_description,
                                        f"{self.mods_path}/{mod1_name}/main.py": "",
                                        f"{self.mods_path}/{mod2_name}/main.py": ""})
        mod_repository = ModRepository(self.mods_path, directory_manager, file_manager)

        returned_mods = mod_repository.find_all_mods()

        self.assertEqual(self.mods_path, directory_manager.path)
        returned_mod1 = returned_mods[0]
        self.assertEqual(mod1.name, returned_mod1.name)
        self.assertEqual(mod1.description, returned_mod1.description)
        self.assertEqual(mod1.path, returned_mod1.path)
        returned_mod2 = returned_mods[1]
        self.assertEqual(mod2.name, returned_mod2.name)
        self.assertEqual(mod2.description, returned_mod2.description)
        self.assertEqual(mod2.path, returned_mod2.path)

    def test_find_mod_with_no_description(self):
        directory = DirectoryManagerMock(["mod1"])
        file = FakeFileManager({f"{self.mods_path}/mod1/main.py": ""})
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)

        mod = mod_repository.find_mod_if_exists("mod1")

        self.assertEqual("mod1", mod.name)
        self.assertEqual("", mod.description)
        self.assertEqual(f"{self.mods_path}/mod1", mod.path)

    def test_directory_is_not_mod_if_does_not_have_main_file(self):
        directory = DirectoryManagerMock(["mod1"])
        file = StubFileManager()
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)

        mods = mod_repository.find_all_mods()
        mod = mod_repository.find_mod_if_exists("mod1")

        self.assertListEqual([], mods)
        self.assertTrue(mod is None)

    def test_find_name_of_enabled_mods(self):
        directory = DirectoryManagerMock([])
        file = FakeFileManager({f"{self.mods_path}/enabled_mods.txt": "mod1\nmod2\nmod3"})
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)

        name_mods = mod_repository.find_name_of_enabled_mods()

        self.assertListEqual(["mod1", "mod2", "mod3"], name_mods)

    def test_find_mod_enabled_attribute(self):
        directory = DirectoryManagerMock(["mod1", "mod2", "mod3", "mod4", "mod8"])
        file = FakeFileManager({f"{self.mods_path}/mod1/main.py": "",
                                f"{self.mods_path}/mod2/main.py": "",
                                f"{self.mods_path}/mod3/main.py": "",
                                f"{self.mods_path}/mod4/main.py": "",
                                f"{self.mods_path}/mod8/main.py": "",
                                f"{self.mods_path}/enabled_mods.txt": "mod3\nmod8\nmod2"})
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)

        returned_mods = mod_repository.find_all_mods()

        self.assertEqual("mod1", returned_mods[0].name)
        self.assertFalse(returned_mods[0].enabled)

        self.assertEqual("mod2", returned_mods[1].name)
        self.assertTrue(returned_mods[1].enabled)

        self.assertEqual("mod3", returned_mods[2].name)
        self.assertTrue(returned_mods[2].enabled)

        self.assertEqual("mod4", returned_mods[3].name)
        self.assertFalse(returned_mods[3].enabled)

        self.assertEqual("mod8", returned_mods[4].name)
        self.assertTrue(returned_mods[4].enabled)

    def test_find_all_enabled_mods(self):
        directory = DirectoryManagerMock(["mod1", "mod2", "mod3", "mod4", "mod8"])
        file = FakeFileManager({f"{self.mods_path}/mod1/main.py": "",
                                f"{self.mods_path}/mod2/main.py": "",
                                f"{self.mods_path}/mod3/main.py": "",
                                f"{self.mods_path}/mod4/main.py": "",
                                f"{self.mods_path}/mod8/main.py": "",
                                f"{self.mods_path}/enabled_mods.txt": "mod3\nmod8\nmod2"})
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)

        returned_mods = mod_repository.find_all_enabled_mods()

        self.assertEqual("mod2", returned_mods[0].name)
        self.assertTrue(returned_mods[0].enabled)

        self.assertEqual("mod3", returned_mods[1].name)
        self.assertTrue(returned_mods[1].enabled)

        self.assertEqual("mod8", returned_mods[2].name)
        self.assertTrue(returned_mods[2].enabled)

    def test_enable_and_disable_mod(self):
        directory = DirectoryManagerMock(["mod1", "mod2", "mod3", "mod4", "mod8"])
        file = FakeFileManager({f"{self.mods_path}/mod1/main.py": "",
                                f"{self.mods_path}/mod2/main.py": "",
                                f"{self.mods_path}/mod3/main.py": "",
                                f"{self.mods_path}/mod4/main.py": "",
                                f"{self.mods_path}/mod8/main.py": "",
                                f"{self.mods_path}/enabled_mods.txt": ""})
        mod_repository = ModRepository(f"{self.mods_path}", directory, file)
        mod_repository.enable_mod("mod1")
        mod_repository.disable_mod("mod3")
        mod_repository.enable_mod("mod8")
        mod_repository.enable_mod("mod4")
        mod_repository.disable_mod("mod2")
        returned_mods = mod_repository.find_all_enabled_mods()

        self.assertEqual(3, len(returned_mods))

        self.assertEqual("mod1", returned_mods[0].name)
        self.assertTrue(returned_mods[0].enabled)

        self.assertEqual("mod4", returned_mods[1].name)
        self.assertTrue(returned_mods[1].enabled)

        self.assertEqual("mod8", returned_mods[2].name)
        self.assertTrue(returned_mods[2].enabled)
