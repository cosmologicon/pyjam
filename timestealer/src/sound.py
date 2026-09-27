import pygame, numpy, sys, os
from functools import cache, lru_cache
from . import state

freq = 22050  # Pygame mixer frequency
tsegment = 0.3  # Time (seconds) for each segment of audio

for arg in sys.argv:
	if arg.startswith("--freq="):
		freq = int(arg[7:])
	if arg.startswith("--tseg="):
		tsegment = float(arg[4:])

pygame.mixer.pre_init(frequency=freq, size=-16, channels=1, buffer=1)

@cache
def loadsound(fname, ext="ogg"):
	path = os.path.join("sound", f"{fname}.{ext}")
	return pygame.mixer.Sound(path)

def resample(arr, n):
	idxs = (numpy.arange(n) / n * len(arr)).astype(int)
	return arr[idxs]

factors = [0.5, 0.6, 0.7, 0.85, 1.0, 1.2, 1.4, 1.7, 2.0]
segs = {}

def init():
	global music, nsegment, music_channel
	pygame.mixer.init()
	music = loadsound("flawless", ext="wav")
	arr = pygame.sndarray.array(music)
	segsample = int(round(tsegment * freq))
	nsample = arr.shape[0]
	nsegment = int(nsample / segsample)
	segarrs = [arr[j * segsample: (j + 1) * segsample] for j in range(nsegment)]
	for f in factors:
		n = int(round(segsample / f))
		farrs = [resample(segarr, n) for segarr in segarrs]
		segs[f] = [pygame.sndarray.make_sound(arr) for arr in farrs]
	music_channel = pygame.mixer.Channel(1)
	music_channel.play(segs[state.musicfactor()][0])

curr_segment = 1
queued_factor = None

def think(dt):
	global curr_segment, queued_factor
	curr_factor = state.musicfactor()
	if curr_factor != queued_factor:
		music_channel.queue(segs[curr_factor][curr_segment])
		queued_factor = curr_factor
	if music_channel.get_queue() is None:
		curr_segment += 1
		curr_segment %= nsegment
		music_channel.queue(segs[curr_factor][curr_segment])


