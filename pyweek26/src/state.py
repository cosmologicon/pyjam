from __future__ import print_function
import datetime, os, pygame
from . import dialog, settings

try:
	import cPickle as pickle
except ImportError:
	import pickle
"""
def get2(self):
	return self.x, self.y
def set2(self, obj):
	self.x, self.y = obj
def get3(self):
	return self.x, self.y, self.z
def set3(self, obj):
	self.x, self.y, self.z = obj
pygame.math.Vector2.__getstate__ = get2
pygame.math.Vector2.__setstate__ = set2
pygame.math.Vector3.__getstate__ = get3
pygame.math.Vector3.__setstate__ = set3
"""

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
dtotrigger = []

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
	current = None
	for sectionid, track in musics.items():
		if sectionid == "current":
			continue
		if triggermatch(you.section.sectionid, sectionid):
			current = track
	if current is not None:
		musics["current"] = current
	elif "current" not in musics:
		musics["current"] = "level"

	if musics["current"] == "level":
		return "levelA"
	return musics["current"]

def think(dt):
	global tsave, tnosave, explored, dtotrigger
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
			t = 0
			if convo in "AH":
				t = 2
			dtotrigger.append([t, convo])

	dtotrigger = [(t - dt, convo) for t, convo in dtotrigger]
	for t, convo in dtotrigger:
		if t <= 0:
			dialog.trigger(convo)
	dtotrigger = [(t, convo) for t, convo in dtotrigger if t > 0]

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
		pickle.dump(getstate(), open(fname, "wb"), protocol=2, fix_imports=True)

def load():
	return
	if not os.path.exists(settings.savename):
		return
	setstate(pickle.load(open(settings.savename, "rb")))

def mapcolor(sectionid):
	return (0.3, 0.3, 1, 1) if sectionid in explored else (0, 0, 0.4, 1)


