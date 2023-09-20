import pygame, statistics
from collections import defaultdict
from . import settings


t0 = {}
dts = defaultdict(list)

def start(pname):
	if not settings.DEBUG: return
	t0[pname] = pygame.time.get_ticks()
	
def stop(pname):
	if not settings.DEBUG: return
	t = pygame.time.get_ticks()
	dt = t - t0[pname]
	dts[pname].append((t, dt))
	while dts[pname][0][0] < t - 1000:
		del dts[pname][0]

last_print = -1000
def print_report(dt = 1):
	global last_print
	if not settings.DEBUG: return
	if 0.001 * pygame.time.get_ticks() < last_print + dt:
		return
	last_print = 0.001 * pygame.time.get_ticks()
	for pname, pdts in sorted(dts.items()):
		ds = [dt for t, dt in pdts]
		print(pname, f"{statistics.mean(ds):.1f}")


