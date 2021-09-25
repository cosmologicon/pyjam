import pygame, math
from . import settings

starts = {}
times = {}
updates = {}

def start(pname):
	if not settings.DEBUG:
		return
	starts[pname] = pygame.time.get_ticks()

def stop(pname):
	if not settings.DEBUG:
		return
	t = pygame.time.get_ticks()
	dt = t - starts[pname]
	if pname in times:
		f = math.exp(-(t - updates[pname]) / 500)
		times[pname] = math.mix(times[pname], dt, f)
	else:
		times[pname] = dt
	updates[pname] = t

def status():
	if not settings.DEBUG:
		return ""
	return "  ".join("%s:%d" % (k, v) for k, v in sorted(times.items()))


