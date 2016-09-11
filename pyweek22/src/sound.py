import pygame, os.path, random, math


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
	"blobup": ["blobup1", "die6"],
	"blobdown": ["blobdown1"],
	"get": "get1 get2 get3 get4".split(),
	"laser": "laser1 laser2 laser3 laser4 laser5 laser6 laser7".split(),
	"boom": "boom1 boom2 boom3 boom4 boom5".split(),
	"3up": "3up1".split(),
	"hatch": ["die5"],
}
sfxsuppression = {}

def getvolume(sname):
	from . import dialog
	volume = 0.5
	if not dialog.quiet():
		volume *= 0.3
	if sname in sfxsuppression:
		volume *= math.exp(-sfxsuppression[sname])
	return volume

def playsfx(sname):
	volume = getvolume(sname)
	sfxsuppression[sname] = sfxsuppression.get(sname, 0) + 1
	sname = random.choice(sversions.get(sname, [sname]))
	sound = getsound(sname, ext = "wav")
	sound.set_volume(volume)
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
	from . import dialog, state, scene, menuscene, playscene
	channel = pygame.mixer.Channel(0)
	if music and not channel.get_queue():
		channel.queue(music)
	if channel.get_busy():
		volume = 0.8
		if dialog.tquiet < 0.5:
			volume = 0.3 + dialog.tquiet
		if scene.top() is playscene:
			if state.twin or state.tlose:
				f = math.clamp(1 - 0.5 * max(state.twin, state.tlose), 0, 1)
				volume *= f
		elif scene.top() is menuscene:
			volume *= menuscene.fade
		channel.set_volume(volume)
	for sname, sfactor in sfxsuppression.items():
		sfxsuppression[sname] *= math.exp(-2 * dt)

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
