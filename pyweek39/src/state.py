import pickle, os
from . import grid, playscene, settings, thing

stepcosts = { n: n for n in range(100) }
enginecosts = { n: 10 * n for n in range(100) }


def init():
    global homes, you, gettables, maxsteps, maxengine, bank
    homes = [thing.Home()]
    you = thing.You((0, 0))
    gettables = []
    maxsteps = 10
    maxengine = 2
    bank = 0


def getstate():
    return grid.wind, homes, you, gettables, maxsteps, maxengine, bank

def setstate(obj):
    global homes, you, gettables, maxsteps, maxengine, bank
    grid.wind, homes, you, gettables, maxsteps, maxengine, bank = obj

def reset():
    if os.path.exists(settings.savegame):
        os.path.remove(settings.savegame)

def save():
    pickle.dump(getstate(), open(settings.savegame, "wb"))

def load():
    if os.path.exists(settings.savegame):
        setstate(pickle.load(open(settings.savegame, "rb")))

