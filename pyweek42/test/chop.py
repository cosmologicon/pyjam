# Sound chop test, PyWeek42
# Requirements: pygame, numpy
# Requires ZombiesAreComing.wav in the current directory.
# To test: python3 chop.py --freq=22050 --t=0.3
# Adjust speed with left and right.
# Does the audio skip?
# Is there noticeable lag between the arrow key being pressed and the audio speed changing?
# Try adjusting the t parameter on the command line.
# Lower (e.g. 0.1) may result in audio skipping, especially at high speeds.
# Higher (e.g. 1.0) may result in more lag, especially at low speeds.


import pygame, numpy, sys

freq = 22050  # Pygame mixer frequency
tsegment = 0.3  # Time (seconds) for each segment of audio

for arg in sys.argv:
	if arg.startswith("--freq="):
		freq = int(arg[7:])
	if arg.startswith("--t="):
		tsegment = float(arg[4:])


# Music from https://opengameart.org/content/zombies-march
musicname = "ZombiesAreComing.wav"

pygame.mixer.pre_init(frequency=freq, size=-16, channels=1, buffer=1)
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("PyWeek42 sound speed test")
font = pygame.font.Font(None, 32)
def drawtext(text, pos, color = (255, 255, 255)):
	screen.blit(font.render(text, True, color), pos)

sound0 = pygame.mixer.Sound(musicname)
arr0 = pygame.sndarray.array(sound0)

segsample = int(round(tsegment * freq))
nsample = arr0.shape[0]
nsegment = int(nsample / segsample)

def resample(arr, n):
	idxs = (numpy.arange(n) / n * len(arr)).astype(int)
	return arr[idxs]

segarrs = [arr0[j * segsample: (j + 1) * segsample] for j in range(nsegment)]

factors = [0.5, 0.6, 0.7, 0.85, 1.0, 1.2, 1.4, 1.7, 2.0]
curr_factor = 1.0

def step(value, values, nstep, wrap=False):
	if nstep == 0: return value
	n = len(values)
	j = values.index(value) + nstep
	j = j % n if wrap else min(max(j, 0), n - 1)
	return values[j]

segs = {}
for f in factors:
	n = int(round(segsample / f))
	farrs = [resample(segarr, n) for segarr in segarrs]
	segs[f] = [pygame.sndarray.make_sound(arr) for arr in farrs]
	del farrs


curr_segment = 0
channel = pygame.mixer.Channel(1)
channel.play(segs[curr_factor][0])

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

	if channel.get_queue() is None:
		curr_segment += 1
		curr_segment %= nsegment
		channel.queue(segs[curr_factor][curr_segment])


	t = 0.001 * (pygame.time.get_ticks() - t0)
	if dfactor != 0:
		curr_factor = step(curr_factor, factors, dfactor)

	screen.fill((0, 0, 0))
	text = [
		f"Current speed: {round(curr_factor*100,1):.1f}%",
		"Left/right: adjust speed",
		f"Current segment: {curr_segment}/{nsegment}",
	]

	for j, line in enumerate(text):
		pos = 10, 10 + 32 * j
		drawtext(line, pos)

	pygame.display.flip()


