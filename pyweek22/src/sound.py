import pygame, os.path


pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)

sounds = {}
def getsound(sname, dirname = "sfx"):
	if sname in sounds:
		return sounds[sname]
	filename = os.path.join("data", dirname, sname + ".ogg")
	sounds[sname] = sound = pygame.mixer.Sound(filename)
	return sound

