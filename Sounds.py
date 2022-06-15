import os


class Sound:
    def __init__(self, name, dir_id, path):
        self.name = name
        self.path = path + "/" + name
        self.dir_id = dir_id + "/" + name

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name.split(".")[0].replace("-", " ")

    def get_id(self):
        return self.dir_id


class SoundDirectory:

    def __init__(self, directory_name, path):
        self.dir_name = directory_name
        self.path = path
        self.sounds = list()

        for sound_name in sorted([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))]):
            self.sounds.append(Sound(name=sound_name, dir_id=self.dir_name, path=self.path))

    def get_id(self):
        return "".join(str(self.dir_name).split("-"))

    def get_name(self):
        return " ".join(str(self.dir_name).split("-")).upper()

    def get_sounds(self):
        return self.sounds
