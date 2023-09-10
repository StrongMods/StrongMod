import importlib.util


class ModLoader:
    def __init__(self, mod_repository):
        self.mod_repository = mod_repository

    def load_mods(self):
        for mod in self.mod_repository.find_all_mods():
            spec = importlib.util.spec_from_file_location("", mod.path + "/" + "main.py")
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)
