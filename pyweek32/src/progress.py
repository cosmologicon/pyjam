import pickle, os
from . import settings


endless = 0
adventure = 0


def save():
	obj = endless, adventure
	pickle.dump(obj, open(settings.savename, "wb"))
def load():
	global endless, adventure
	if not os.path.exists(settings.savename): return
	obj = pickle.load(open(settings.savename, "rb"))
	endless, adventure = obj
def reset():
	if os.path.exists(settings.savename):
		os.remove(settings.savename)
	save()

if settings.reset:
	reset()
else:
	load()


def beatendless(stage):
	global endless
	if stage > endless:
		endless = stage
	save()

def beatadventure(stage):
	global adventure
	if stage > adventure:
		adventure = stage
	save()

