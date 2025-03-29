import pygame.mixer, os.path
from functools import cache
from . import settings

pygame.mixer.pre_init(frequency=22050, size=-16, channels=1, buffer=1)

def pathname(sname):
    return os.path.join("sound", f"{sname}.ogg")

@cache
def loadfile(sname):
    path = pathname(sname)
    if not os.path.exists(path):
        print(f"MISSING SOUND: {sname}")
        return None
    return pygame.mixer.Sound(path)

def getvolume(sname):
    f = {
        "get": 0.5
    }.get(sname, 1.0)
    return f * settings.sfxvol ** 1.8


def play(sname):
    if sname == "move":
        return
    s = loadfile(sname)
    if s is None:
        return
    s.set_volume(getvolume(sname))
    s.play()

def init():
    pygame.mixer.music.load(pathname("decline"))
    pygame.mixer.music.set_volume(settings.musicvol ** 1.8)
    pygame.mixer.music.play(-1)
    

