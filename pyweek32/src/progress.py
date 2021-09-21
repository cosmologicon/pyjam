import pickle, os
from . import settings


endless = 0


def save():
	obj = endless
	pickle.dump(obj, open(settings.savename, "wb"))
def load():
	global endless
	if not os.path.exists(settings.savename): return
	obj = pickle.load(open(settings.savename, "rb"))
	endless = obj
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

