import os


class FileSystem:
    def read(self, file_name):
        file = open(file_name, "r")
        contents = file.read()
        file.close()
        return contents

    def is_exists(self, file_name):
        return os.path.exists(file_name)
