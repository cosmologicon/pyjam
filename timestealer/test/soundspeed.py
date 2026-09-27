import pygame, numpy

FREQ0 = 22050
# Sound effect from https://opengameart.org/content/steampunk-fantasy-voices
sfxname = "Hero_Taunt_001.wav"
# Music from https://opengameart.org/content/zombies-march
musicname = "ZombiesAreComing.wav"

def loadarray(factor):
	freq = int(round(FREQ0 / factor))
	pygame.mixer.init(frequency=freq, size=-16, channels=1, buffer=1)
	sound1 = pygame.mixer.Sound(musicname)
	arr = pygame.sndarray.array(sound1)
	print(factor, freq, arr.shape)
	pygame.mixer.quit()
	return arr

factors = [1.1 ** n for n in range(-10, 11)]
factor = 1.0

def step(value, values, nstep, wrap=False):
	if nstep == 0: return value
	n = len(values)
	j = values.index(value) + nstep
	j = j % n if wrap else min(max(j, 0), n - 1)
	return values[j]

def stepfactor(dfactor, t):
	global factor
	factor = step(factor, factors, dfactor)
	pygame.mixer.Channel(1).play(fsounds[factor])
	

pygame.init()
pygame.display.set_mode((600, 400))

pygame.mixer.quit()
arrs = [loadarray(factor) for factor in factors]

pygame.mixer.init(frequency=FREQ0, size=-16, channels=1, buffer=1)
sounds = [pygame.sndarray.make_sound(arr) for arr in arrs]
del arrs
fsounds = dict(zip(factors, sounds))

t0 = pygame.time.get_ticks()
playing = True
while playing:
	dfactor = 0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			playing = False
		if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
			dfactor -= 1
		if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
			dfactor += 1

	t = 0.001 * (pygame.time.get_ticks() - t0)
	if dfactor != 0:
		stepfactor(dfactor, t)
	print(f"{round(factor*100,1):.1f}", f"{t:.3f}")
	pygame.display.flip()


