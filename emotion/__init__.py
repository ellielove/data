import json
import os


class Vec4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w


class Emotion:
    def __init__(self, name, arousal, valance, stance, time):
        self.name = name

        # arousal - the "energy level" of an emotion; eg: high energy vs low energy
        self.arousal = arousal

        # valance - the positivity of an emotion; how pleasant it is
        self.valance = valance

        # stance - a person's openness to the experience; open vs closed
        self.stance = stance

        # time - a future, present, or past experience
        self.time = time


class EmotionLibrary:
    @staticmethod
    def save_to_file(data, path):
        with open(path, 'w') as outfile:
            json.dump(data, outfile, indent=4, sort_keys=True)
            return os.path.isfile(path)

    @staticmethod
    def load_from_file(path):
        if not os.path.isfile(path):
            return {'error': f'path is not valid! path={path}'}
        with open(path, 'r') as infile:
            return json.load(infile)

    def __init__(self, path):
        self.library = None

        if os.path.isfile(path):
            self.library = self.load_from_file(path)
            if 'error' in self.library:
                print(self.library['error'])
                self.library = None

    def add_emotion(self, name, vec4):
        self.library[name] = Emotion(name, vec4.x, vec4.y, vec4.z, vec4.w)

