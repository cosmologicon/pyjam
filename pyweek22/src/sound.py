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
	"bigdie": ["bigdie4"],
	"tick": ["tick3"],
	"blobup": ["blobup1"],
	"blobdown": ["blobdown1"],
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

music = None
def playmusic(song, intro = None):
	global music
	channel = pygame.mixer.Channel(0)
	channel.play(getsound(intro or song, dirname = "music"))
	music = song and getsound(song, dirname = "music")
	
def think(dt):
	from . import dialog
	channel = pygame.mixer.Channel(0)
	if music and not channel.get_busy():
		channel.play(music, -1)
	if channel.get_busy():
		if dialog.tquiet > 0.5:
			channel.set_volume(0.8)
		else:
			channel.set_volume(0.3)

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
