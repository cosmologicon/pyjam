import pickle, os
from . import grid, playscene, settings, thing

def init():
    global homes, you, gettables, maxsteps, maxengine, bank
    homes = [thing.Home()]
    you = thing.You((0, 0))
    gettables = []
    maxsteps = 6
    maxengine = 2
    bank = 0

stepcosts = [0] * 6 + [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
enginecosts = [0] * 2 + [10, 100, 1000]


def getstate():
    return grid.wind, grid.strength, homes, you, gettables, maxsteps, maxengine, bank

def setstate(obj):
    global homes, you, gettables, maxsteps, maxengine, bank
    grid.wind, grid.strength, homes, you, gettables, maxsteps, maxengine, bank = obj

def reset():
    if os.path.exists(settings.savegame):
        os.path.remove(settings.savegame)

def save():
    pickle.dump(getstate(), open(settings.savegame, "wb"))

def load():
    if os.path.exists(settings.savegame):
        setstate(pickle.load(open(settings.savegame, "rb")))

