import pickle, os
from . import grid, playscene, settings, thing

def init():
    global homes, you, gettables, maxfuel, bank, totalbank, artifacts
    homes = [thing.Home()]
    you = thing.You((0, 0))
    gettables = {}
    maxfuel = 6
    bank = 0
    totalbank = 0
    artifacts = 0

def addgettable(obj):
    gettables[obj.pos] = obj

fuelcosts = [0] * 6 + [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711]
fuelcosts = [0] * 6 + [1, 2, 3, 5, 7, 10, 15, 20, 30, 50, 70, 100, 150, 200, 300, 500, 700, 1000, 1500, 2000]
turbinefuel = [3, 3, 6, 12]
turbinelevel = [0, 0, 1, 3]
maxturbine = 1

def getstate():
    return grid.wind, grid.strength, homes, you, gettables, maxfuel, bank, totalbank, artifacts

def setstate(obj):
    global homes, you, gettables, maxfuel, bank, totalbank, artifacts
    grid.wind, grid.strength, homes, you, gettables, maxfuel, bank, totalbank, artifacts = obj

def reset():
    if os.path.exists(settings.savegame):
        os.path.remove(settings.savegame)

def save():
    pickle.dump(getstate(), open(settings.savegame, "wb"))

def load():
    if os.path.exists(settings.savegame):
        setstate(pickle.load(open(settings.savegame, "rb")))
        you.snapto()

def softsave():
    if not os.path.exists(settings.savegame):
        save()

