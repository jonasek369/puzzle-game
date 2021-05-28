import os
import random
from pygame import mixer

class musicEngine:
    def __init__(self):
        self.vol = 0.1
        self.MUSIC_STATE = "normal"
        self.currently_playing = {"name": "", "state": "n/c"}
        self.normal_dir = (os.path.dirname(os.path.realpath(__file__)) + "\\" + "music\\normal")
        self.normal_listdir = os.listdir(self.normal_dir)

    def start(self):
        is_busy = mixer.music.get_busy()
        mixer.music.set_volume(self.vol)
        if self.MUSIC_STATE != self.currently_playing["state"]:
            mixer.stop()
            if self.MUSIC_STATE == "normal":
                random_song = random.choice(self.normal_listdir)
                playing_dir = self.normal_dir + "\\" + random_song
                self.currently_playing = {"name": random_song, "state": "normal"}
                mixer.music.load(playing_dir)
                mixer.music.play()

        if is_busy == 0:
            if self.MUSIC_STATE == "normal":
                random_song = random.choice(self.normal_listdir)
                if random_song == self.currently_playing["name"]:
                    musicEngine.start(self)
                playing_dir = self.normal_dir + "\\" + random_song
                self.currently_playing = {"name": random_song, "state": "normal"}
                mixer.music.load(playing_dir)
                mixer.music.play()