import os
import dataclasses


@dataclasses.dataclass
class Mod:
    name: str
    description: str
    path: str


class DirectoryManager:
    def get_all_directories(self, path):
        return os.listdir(path)


class ModRepository:
    def __init__(self, mods_path, directory, file):
        self.file = file
        self.directory = directory
        self.mods_path = mods_path

    def find_all_mods(self):
        mods = []
        for mod_directory_name in self.directory.get_all_directories(self.mods_path):
            if not self.find_mod_if_exists(mod_directory_name) is None:
                mods.append(self.find_mod_if_exists(mod_directory_name))

        return mods

    def find_mod_if_exists(self, mod_directory_name):
        if self.file.is_exists(self.mods_path + "/" + mod_directory_name + "/" + "main.py"):
            return Mod(name=mod_directory_name, description=self._get_description(mod_directory_name),
                       path=self.mods_path + "/" + mod_directory_name)
        else:
            return None

    def _get_description(self, mod_directory_name):
        try:
            return self.file.read(self.mods_path + "/" + mod_directory_name + "/" + "description.txt")
        except FileNotFoundError:
            return ""
