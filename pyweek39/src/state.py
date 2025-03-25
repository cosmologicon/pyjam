import pickle, os
from . import grid, playscene, settings, thing

def init():
    global homes, you, gettables, maxfuel, bank, artifacts
    homes = [thing.Home()]
    you = thing.You((0, 0))
    gettables = []
    maxfuel = 8
    bank = 0
    artifacts = 0

fuelcosts = [0] * 6 + [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
turbinefuel = [3, 3, 6, 12]
maxturbine = 3

def getstate():
    return grid.wind, grid.strength, homes, you, gettables, maxfuel, bank, artifacts

def setstate(obj):
    global homes, you, gettables, maxfuel, bank, artifacts
    grid.wind, grid.strength, homes, you, gettables, maxfuel, bank, artifacts = obj

def reset():
    if os.path.exists(settings.savegame):
        os.path.remove(settings.savegame)

def save():
    pickle.dump(getstate(), open(settings.savegame, "wb"))

def load():
    if os.path.exists(settings.savegame):
        setstate(pickle.load(open(settings.savegame, "rb")))

