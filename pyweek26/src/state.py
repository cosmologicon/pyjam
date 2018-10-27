from __future__ import print_function
import datetime, os
from . import dialog, settings

try:
	import cPickle as pickle
except ImportError:
	import pickle

# animation objects
animation = None
# Player character
you = None
# Current amount of fish food
food = 0
foodmax = 1
# Sewer sections
sections = []
# Floating game objects - will rename once we know what will be there
objs = []
# Non-interactive special effects
effects = []

# Dialog triggers - when the player enters this section the corresponding dialog will play.
dtriggers = {}
# Dialog that's already been triggered once.
dtriggered = set()

# For all sections where the music is not regular gameplay music.
musics = {}

# To avoid spamming the "game saved" message, we keep track of how long the player has spent in
# "save" areas and "non-save" areas since the last save.
tsave = 0
tnosave = 0

# Section IDs of places you've visited, that show up unfaded on the map.
explored = set()

# For the purpose of triggering, every section of a tunnel has the same trigger logic.
def triggermatch(id0, id1):
	j0, k0 = id0
	j1, k1 = id1
	return j0 == j1 and (j0 != "pool" or k0 == k1)

def currentmusic():
	for sectionid, track in musics.items():
		if triggermatch(you.section.sectionid, sectionid):
			return track
	return "level"

def think(dt):
	global tsave, tnosave, explored
	explored.add(you.section.sectionid)
	if you.section.label == "pool":
		cansave = you.section.cansave
		if cansave:
			tsave += dt
			if tsave > 3 and tnosave > 1:
				save()
		else:
			tsave = 0
			tnosave += dt
		
	for convo, sectionid in dtriggers.items():
		if convo in dtriggered:
			continue
		if triggermatch(you.section.sectionid, sectionid):
			dtriggered.add(convo)
			dialog.trigger(convo)

def getstate():
	return you, food, foodmax, sections, objs, effects, dtriggers, dtriggered, musics, explored, animation

def setstate(s):
	global you, food, foodmax, sections, objs, effects, dtriggers, dtriggered, musics, explored
	you, food, foodmax, sections, objs, effects, dtriggers, dtriggered, musics, explored, animation = s

def save():
	global tsave, tnosave
	tsave = 0
	tnosave = 0
	# TODO: onscreen save message
	if settings.DEBUG:
		print("saving")
	asavename = datetime.datetime.now().strftime(settings.asavename)
	for fname in (settings.savename, asavename):
		if not os.path.exists(os.path.dirname(fname)):
			os.makedirs(os.path.dirname(fname))
		pickle.dump(getstate(), open(fname, "wb"))

def load():
	if not os.path.exists(settings.savename):
		return
	setstate(pickle.load(open(settings.savename, "rb")))

def mapcolor(sectionid):
	return (0.3, 0.3, 1, 1) if sectionid in explored else (0, 0, 0.4, 1)

load()
