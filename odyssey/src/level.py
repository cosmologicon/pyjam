from __future__ import print_function
import os
from collections import defaultdict, OrderedDict
from pygame.math import Vector3

from . import state, section, thing, settings, graphics

# Map from section id to list of section ids that this section is connected to
connection_ids = defaultdict(list)

def load():
	state.sections_by_id = OrderedDict()
	filename = "data/%s.csv" % settings.leveldataname
	for line in open(filename, "r"):
		fields = line.split()
#		if settings.DEBUG:
#			print(*fields)
		if fields[0] == "pool":
			loadpool(*fields)
		if fields[0] == "pipe":
			loadpipe(*fields)
		if fields[0] == "straight":
			loadstraight(*fields)
		if fields[0] == "slope":
			loadslope(*fields)
		if fields[0] == "curve":
			loadcurve(*fields)
	for sectionid, section in state.sections_by_id.items():
		state.sections.append(section)
		section.sectionid = sectionid
	connectsections()
	state.you.section = state.sections[0]
	state.you.pos = 1 * state.you.section.pos

	loadtriggers("data/%s-triggers.csv" % settings.leveldataname)		

def loadpool(pool, jpool, cx, cy, cz, r, pressure0, drainable):
	sectionid = parseid(pool, jpool)
	center = Vector3(float(cx), float(cy), float(cz))
	r = float(r)
	pressure0 = int(pressure0)
	drainable = drainable == "True"
	state.sections_by_id[sectionid] = section.Pool(center, r, pressure0, drainable)

def maybeint(j):
	return int(j) if j.isdigit() else j

def parseid(j, k):
	return maybeint(j), int(k)

def gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto):
	sectionid = parseid(jtunnel, jsection)
	fromid = parseid(jfrom, kfrom)
	toid = parseid(jto, kto)
	return sectionid, fromid, toid

def tunnelconnect(sectionid, fromid, toid, oneway = False):
	connection_ids[sectionid].append(fromid)
	connection_ids[sectionid].append(toid)
	if fromid[0] == "pool":
		connection_ids[fromid].append(sectionid)
	if toid[0] == "pool" and not oneway:
		connection_ids[toid].append(sectionid)

def loadpipe(pipe, jpipe, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w):
	sectionid, fromid, toid = gettunnelids("pipe", jpipe, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	w = float(w)
	state.sections_by_id[sectionid] = section.Pipe(p0, p1, width=w)
	tunnelconnect(sectionid, fromid, toid, oneway = True)

def loadstraight(straight, jtunnel, jsection, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w):
	sectionid, fromid, toid = gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	w = float(w)
	state.sections_by_id[sectionid] = section.StraightConnector(p0, p1, width=w)
	tunnelconnect(sectionid, fromid, toid)

def loadslope(slope, jtunnel, jsection, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w):
	sectionid, fromid, toid = gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	w = float(w)
	state.sections_by_id[sectionid] = section.SlopeConnector(p0, p1, width=w)
	tunnelconnect(sectionid, fromid, toid)

def loadcurve(curve, jtunnel, jsection, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w, cx, cy, cz, beta, right, R):
	sectionid, fromid, toid = gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	center = Vector3(float(cx), float(cy), float(cz))
	w = float(w)
	R = float(R)
	beta = float(beta)
	right = right == "True"
	state.sections_by_id[sectionid] = section.CurvedConnector(p0, p1, center, beta, right, R, width=w)
	tunnelconnect(sectionid, fromid, toid)

# One everything is loaded, connect everything to the appropriate section objects
def connectsections():
	for sectionid, conids in connection_ids.items():
		state.sections_by_id[sectionid].connections = [state.sections_by_id[conid] for conid in conids]
	for sect in state.sections:
		if isinstance(sect, section.Connector):
			sect.setpools()

# The triggers file has dialog trigger locations and various other things I couldn't be bothered
# to implement in the level editor - just have to make it manually.
def loadtriggers(filename):
	if not os.path.exists(filename):
		return
	for line in open(filename, "r"):
		line = line.split("#")[0].strip()
		if not line:
			continue
		fields = line.split()
		if fields[0] == "start":
			triggerstart(*fields)
		if fields[0] == "food":
			triggerfood(*fields)
		if fields[0] == "whirl":
			triggerwhirl(*fields)
		if fields[0] == "drain":
			triggerdrain(*fields)
		if fields[0] == "rapid":
			triggerrapid(*fields)
		if fields[0] == "fmode":
			triggerfmode(*fields)
		if fields[0] == "dialog":
			triggerdialog(*fields)
		if fields[0] == "music":
			triggermusic(*fields)
		if fields[0] == "endboss":
			triggerendboss(*fields)
		if fields[0] == "save":
			triggersave(*fields)
		if fields[0] == "ocean":
			triggerocean(*fields)
		if fields[0] == "note":
			triggernote(*fields)

def triggerstart(start, j, k):
	section = state.sections_by_id[parseid(j, k)]
	state.you.section = section
	state.you.pos = 1 * section.pos

def triggerfood(start, j, k):
	section = state.sections_by_id[parseid(j, k)]
	section.hasfood = True

def triggerwhirl(whirl, j, k, strength):
	section = state.sections_by_id[parseid(j, k)]
	section.whirl = float(strength)
	section.addvortex()

def triggerdrain(drain, j, k):
	section = state.sections_by_id[parseid(j, k)]
	section.drainable = True
	section.drain(silent = True)

def triggerrapid(rapid, j0, amount):
	j0 = int(j0)
	amount = float(amount)
	for (j, k), section in state.sections_by_id.items():
		if j == j0:
			section.rapid = amount

def triggerdialog(dialog, convo, j, k):
	state.dtriggers[convo] = parseid(j, k)

def triggermusic(music, track, j, k):
	state.musics[parseid(j, k)] = track

def triggerendboss(endboss, j, k):
	section = state.sections_by_id[parseid(j, k)]
	state.effects.append(thing.Tentacles(section))
	state.objs.append(thing.BossHitbox(section))
	section.final = True
	section.bmode = True
	section.addvortex()

def triggersave(save, k):
	section = state.sections_by_id[parseid("pool", k)]
	section.cansave = True

def triggerfmode(fmode, j, k, value):
	value = value == "True"
	section = state.sections_by_id[parseid(j, k)]
	section.fmode = value

def triggerocean(ocean, j, k):
	section = state.sections_by_id[parseid(j, k)]
	section.ocean = True

def triggernote(note, name, j, k, value):
	value = value == "True"
	state.notetriggers[parseid(j, k)] = name, value

