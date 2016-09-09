import pygame, os.path, random


pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=4096)

sounds = {}
def getsound(sname, dirname = "sfx", ext = "ogg"):
	if sname in sounds:
		return sounds[sname]
	filename = os.path.join("data", dirname, sname + "." + ext)
	if not os.path.exists(filename):
		raise ValueError(filename)
	sounds[sname] = sound = pygame.mixer.Sound(open(filename, "rb"))
	return sound


sversions = {
	"click": ["click1"],
	"yes": ["yes4"],
	"no": ["no1", "no2"],
	"die": ["die4_1"],
	"tick": ["tick3"],
}

def playsfx(sname):
	sname = random.choice(sversions.get(sname, [sname]))
	sound = getsound(sname, ext = "wav")
	for jchannel in (2, 3, 4, 5, 6, 7):
		channel = pygame.mixer.Channel(jchannel)
		if channel.get_busy():
			continue
		channel.play(sound)
		break

if __name__ == "__main__":
	pygame.init()
	pygame.display.set_mode((600, 600))
	toplay = "yes no die".split()
	for p in toplay:
		for _ in range(5):
			playsfx(p)
			print(p)
			while any(pygame.mixer.Channel(j).get_busy() for j in (2, 3, 4, 5, 6, 7)):
				pass
	pygame.quit()
