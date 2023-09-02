import os
import dataclasses


@dataclasses.dataclass
class Mod:
    name: str
    description: str
    path: str
    enabled: bool = False


class DirectoryManager:
    def get_all_directories(self, path):
        return os.listdir(path)


class ModRepository:
    def __init__(self, mods_path, directory, file):
        self.file = file
        self.directory = directory
        self.mods_path = mods_path
        self.enabled_mods_path = self.mods_path + "/" + "enabled_mods.txt"

    def find_all_mods(self):
        mods = []
        for mod_directory_name in self.directory.get_all_directories(self.mods_path):
            if not self.find_mod_if_exists(mod_directory_name) is None:
                mods.append(self.find_mod_if_exists(mod_directory_name))

        return mods

    def find_mod_if_exists(self, mod_directory_name):
        name_of_enabled_mods = self.find_name_of_enabled_mods()
        if self.file.is_exists(self.mods_path + "/" + mod_directory_name + "/" + "main.py"):
            return Mod(name=mod_directory_name, description=self._get_description(mod_directory_name),
                       path=self.mods_path + "/" + mod_directory_name,
                       enabled=True if mod_directory_name in name_of_enabled_mods else False)
        else:
            return None

    def _get_description(self, mod_directory_name):
        try:
            return self.file.read(self.mods_path + "/" + mod_directory_name + "/" + "description.txt")
        except FileNotFoundError:
            return ""

    def find_name_of_enabled_mods(self):
        try:
            return self.file.read(self.mods_path + "/" + "enabled_mods.txt").split("\n")
        except FileNotFoundError:
            return []

    def find_all_enabled_mods(self):
        return list(filter(lambda mod: mod.enabled, self.find_all_mods()))

    def disable_mod(self, mod_name):
        enabled_mod_names = self.find_name_of_enabled_mods()

        if mod_name in enabled_mod_names:
            enabled_mod_names.remove(mod_name)

        self.file.write(self.enabled_mods_path, "\n".join(enabled_mod_names))

    def enable_mod(self, mod_name):
        enabled_mod_names = self.find_name_of_enabled_mods()

        if mod_name not in enabled_mod_names:
            enabled_mod_names.append(mod_name)

        self.file.write(self.enabled_mods_path, "\n".join(enabled_mod_names))

