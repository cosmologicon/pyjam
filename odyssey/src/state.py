from __future__ import print_function
import datetime, os, pygame
from collections import OrderedDict
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
sections_by_id = OrderedDict()
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
tlastsave = 0
tlastqsave = 0

# Section IDs of places you've visited, that show up unfaded on the map.
explored = set()

notetriggers = {}
currentnotes = {}

# For the purpose of triggering, every section of a tunnel has the same trigger logic.
def triggermatch(id0, id1):
	j0, k0 = id0
	j1, k1 = id1
	return j0 == j1 and (j0 != "pool" or k0 == k1)

def currentmusic():
	if not musics:
		return "intro"
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
		progress = len(sections_by_id[("pool", 0)].drainers)
		return "levelA" if progress % 2 else "levelB"
	return musics["current"]

def think(dt):
	global tsave, tnosave, tlastsave, tlastqsave, explored, dtotrigger
	explored.add(you.section.sectionid)
	if you.section.label == "pool":
#		print(tsave, tnosave, you.section.sectionid, you.section.cansave, (you.section in sections), sections[0].sectionid, sections[0].cansave, sections[0].pos)
		cansave = you.section.cansave
		if cansave:
			tsave += dt
			if tsave > 3 and tnosave > 1:
				save()
		else:
			tsave = 0
			tnosave += dt
	tlastsave += dt
	tlastqsave += dt

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

	for sectionid, (notename, value) in notetriggers.items():
		if triggermatch(you.section.sectionid, sectionid):
			currentnotes[notename] = value

def currentnote():
	for notename, value in currentnotes.items():
		if value:
			return notename
	return None

def getstate():
	return you, food, foodmax, sections, sections_by_id, objs, effects, dtriggers, dtriggered, musics, explored, animation

def setstate(s):
	global you, food, foodmax, sections, sections_by_id, objs, effects, dtriggers, dtriggered, musics, explored, animation
	you, food, foodmax, sections, sections_by_id, objs, effects, dtriggers, dtriggered, musics, explored, animation = s

def save():
	global tsave, tnosave, tlastsave
	tsave = 0
	tnosave = 0
	tlastsave = 0
	# TODO: onscreen save message
	if settings.DEBUG:
		print("saving")
	asavename = datetime.datetime.now().strftime(settings.asavename)
	for fname in (settings.savename, asavename):
		if not os.path.exists(os.path.dirname(fname)):
			os.makedirs(os.path.dirname(fname))
		pickle.dump(getstate(), open(fname, "wb"))

# TODO: quicksave

def load():
	if os.path.exists(settings.qsavename):
		setstate(pickle.load(open(settings.qsavename, "rb")))
	elif os.path.exists(settings.savename):
		setstate(pickle.load(open(settings.savename, "rb")))

def reset():
	if os.path.exists(settings.savename):
		os.remove(settings.savename)
	if os.path.exists(settings.qsavename):
		os.remove(settings.qsavename)

def clean():
	if os.path.exists(settings.qsavename):
		os.remove(settings.qsavename)

def mapcolor(sectionid):
	return (0.5, 0.5, 1, 1) if sectionid in explored else (0.1, 0.1, 0.6, 1)


def teleport(where):
	jpool = {
		"home": 0,
		"NE": 1,
		"NW": 2,
		"SW": 3,
		"SE": 4,
	}[where]
	if ("pool", jpool) not in sections_by_id:
		return
	you.section = sections_by_id[("pool", jpool)]
	you.pos = you.section.pos + pygame.math.Vector3(0, 0, 3)

