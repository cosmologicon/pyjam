from . import dialog

# Player character
you = None
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

# For the purpose of triggering, every section of a tunnel has the same trigger logic.
def triggermatch(id0, id1):
	j0, k0 = id0
	j1, k1 = id1
	return j0 == j1 and (j0 != "pool" or k0 == k1)

def currentmusic():
	for sectionid, track in musics.items():
		if triggermatch(you.section.id, sectionid):
			return track
	return "level"

def think(dt):
	for convo, sectionid in dtriggers.items():
		if convo in dtriggered:
			continue
		if triggermatch(you.section.sectionid, sectionid):
			dtriggered.add(convo)
			dialog.trigger(convo)

