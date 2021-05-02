import pygame, math, os.path
from functools import lru_cache
from . import settings

class self:
	mvolume = 0
	mtarget = 0
	mtrack = 1
	mtracktarget = 1
	
	wlevel = 0
	wtarget = 0

def init():
	pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=2)
	self.wchannel = pygame.mixer.Channel(6)
	self.water = get("water")
	self.wchannel.set_volume(0)
	self.wchannel.play(self.water, -1)

	self.musics = {
		1: get("music1"),
		2: get("music2"),
		3: get("music3"),
	}

	self.mchannel = pygame.mixer.Channel(5)
	self.mchannel.set_volume(0)
	self.mchannel.play(self.musics[1], -1)

def setwater():
	from . import state, thing
	nsplash = sum(isinstance(effect, thing.Splash) for effect in state.effects)
	fsplash = math.fadebetween(nsplash, 1, 0, 10, 1)
	ftide = math.fadebetween(state.tide, 3, 0, 12, 1)
	self.wtarget = max(fsplash, ftide)

def playmusic(n, v):
	self.mtarget = v
	self.mtracktarget = n

@lru_cache(None)
def get(sname):
	path = "sound/%s.ogg" % sname
	if os.path.exists(path):
		s = pygame.mixer.Sound(path)
		if "find" in sname:
			s.set_volume(0.5)
		return s

def play(sname):
	sound = get(sname)
	if sound is not None:
		sound.play()

def think(dt):
	if self.mtrack != self.mtracktarget:
		self.mvolume = math.approach(self.mvolume, 0, dt)
		if self.mvolume == 0:
			self.mtrack = self.mtracktarget
			self.mchannel.play(self.musics[self.mtrack], -1)
	else:
		self.mvolume = math.approach(self.mvolume, self.mtarget, dt)
	self.mchannel.set_volume(math.clamp(settings.musicvolume * self.mvolume, 0, 1))
	setwater()
	self.wlevel = math.approach(self.wlevel, self.wtarget, 1 * dt)
	self.wchannel.set_volume(0.4 * self.wlevel)

def getstate():
	return self.mvolume, self.mtarget, self.mtrack, self.mtracktarget, self.wlevel, self.wtarget
def setstate(obj):
	self.mvolume, self.mtarget, self.mtrack, self.mtracktarget, self.wlevel, self.wtarget = obj
	self.mtrack = None



