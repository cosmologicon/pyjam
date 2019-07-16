import pygame, os.path
import settings

music = None

sounds = {}

def load(sname):
	if sname not in sounds:
		filename = "data/%s.ogg" % sname
		if not os.path.exists(filename):
			print "Missing sound:", sname
			sounds[sname] = None
			return
		sounds[sname] = pygame.mixer.Sound(filename)

def play(sname):
	load(sname)
	if not sounds[sname]:
		return
	sounds[sname].play()

def playmusic(sname):
	global music
	load(sname)
	if not sounds[sname]:
		return
	if sounds[sname] is music:
		return
	if music:
		music.fadeout(500)
	music = sounds[sname]
	music.play(-1, 0, 500)


