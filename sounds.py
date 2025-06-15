import pygame as pg
import os

class SoundManager : 
    def __init__(self) :
        pg.mixer.init()
        self.hit_sound = pg.mixer.Sound(os.path.join("sounds", "sfx_hit.wav"))
        self.point_sound = pg.mixer.Sound(os.path.join("sounds", "sfx_point.wav"))

    def play_hit(self) :
        self.hit_sound.play()

    def play_point(self) :
        self.point_sound.play()        