import pygame, os
from . import settings

pygame.mixer.pre_init(frequency=22050, size=16, channels=1, buffer=10)

class self:
	track = None
	sounds = {}

def playmusic(track):
	if settings.nomusic:
		return
	if track == self.track:
		return
	self.track = track
	pygame.mixer.music.set_volume(0.6)
	pygame.mixer.music.load(os.path.join("music", "%s.mp3" % track))
	pygame.mixer.music.play(-1)

def play(sound):
	if settings.nosfx:
		return
	if sound not in self.sounds:
		self.sounds[sound] = pygame.mixer.Sound(os.path.join("sfx", "%s.ogg" % sound))
		self.sounds[sound].set_volume(0.5)
	self.sounds[sound].play()

