import pygame, os
from . import settings, dialogue
from .util import debug

# Channels 1/2/3 reserved for sound effects
# Channel 4 reserved for music

sounds = {}
def getsound(sname):
	if sname not in sounds:
		fname = "data/" + sname
		if sname.startswith("dialogue"):
			fname += "." + settings.dialogueext
		elif sname.startswith("music"):
			fname += "." + settings.musicext
		else:
			fname += "." + settings.sfxext
		if os.path.exists(fname):
			sounds[sname] = pygame.mixer.Sound(fname)
			if "ACK" in sname:
				sounds[sname].set_volume(settings.volumes["ack"])
			elif "NARRATOR" in sname:
				sounds[sname].set_volume(settings.volumes["narrator"])
			elif "dialogues" in sname:
				sounds[sname].set_volume(settings.volumes["dialogue"])
			elif "music" in sname:
				sounds[sname].set_volume(1)
			else:
				sounds[sname].set_volume(settings.volumes["sfx"])
		else:
			sounds[sname] = None
			debug("Missing sound:", sname)
	return sounds[sname]

def play(sname, channel = None):
	sound = getsound(sname)
	if sound is None:
		return
	if channel is not None:
		pygame.mixer.Channel(channel).play(sound)
	else:
		for channel in (1, 2, 3):
			c = pygame.mixer.Channel(channel)
			if not c.get_busy():
				c.play(sound)
				break

targetjmusic = None
targetvolume = None
currentvolume = 0
currentjmusic = None
def playmusic(jmusic, volume):
	global targetjmusic, targetvolume, currentvolume, currentjmusic
	musics = [getsound("music%d" % j) for j in (1, 2)]
	channel = pygame.mixer.Channel(4)
	if jmusic != currentjmusic:
		currentjmusic = jmusic
		channel.play(musics[jmusic], -1)
	volume = settings.volumes["music"]
	if dialogue.tquiet < 0.1:
		volume *= settings.volumes["ssh"]
	channel.set_volume(volume)
