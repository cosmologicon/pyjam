from collections import defaultdict, OrderedDict
from pygame.math import Vector3

from . import state, section, thing

# Map from section id to section object
sections_by_id = OrderedDict()
# Map from section id to list of section ids that this section is connected to
connection_ids = defaultdict(list)

def load():
	filename = "data/leveldata.csv"
	for line in open(filename, "r"):
		fields = line.split()
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
	state.sections = list(sections_by_id.values())
	connectsections()
	state.you.section = state.sections[2]
	state.you.pos = 1 * state.you.section.pos

def loadpool(pool, jpool, cx, cy, cz, r, pressure0, drainable):
	sectionid = pool, int(jpool)
	center = Vector3(float(cx), float(cy), float(cz))
	r = float(r)
	pressure0 = int(pressure0)
	drainable = drainable == "True"
	sections_by_id[sectionid] = section.Pool(center, r, pressure0, drainable)

def maybeint(j):
	return int(j) if j.isdigit() else j

def gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto):
	sectionid = maybeint(jtunnel), int(jsection)
	fromid = maybeint(jfrom), int(kfrom)
	toid = maybeint(jto), int(kto)
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
	sections_by_id[sectionid] = section.Pipe(p0, p1, width=w)
	tunnelconnect(sectionid, fromid, toid, oneway = True)

def loadstraight(straight, jtunnel, jsection, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w):
	sectionid, fromid, toid = gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	w = float(w)
	sections_by_id[sectionid] = section.StraightConnector(p0, p1, width=w)
	tunnelconnect(sectionid, fromid, toid)

def loadslope(slope, jtunnel, jsection, jfrom, kfrom, jto, kto, x0, y0, z0, x1, y1, z1, w):
	sectionid, fromid, toid = gettunnelids(jtunnel, jsection, jfrom, kfrom, jto, kto)
	p0 = Vector3(float(x0), float(y0), float(z0))
	p1 = Vector3(float(x1), float(y1), float(z1))
	w = float(w)
	sections_by_id[sectionid] = section.SlopeConnector(p0, p1, width=w)
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
	sections_by_id[sectionid] = section.CurvedConnector(p0, p1, center, beta, right, R, width=w)
	tunnelconnect(sectionid, fromid, toid)

# One everything is loaded, connect everything to the appropriate section objects
def connectsections():
	for sectionid, conids in connection_ids.items():
		sections_by_id[sectionid].connections = [sections_by_id[conid] for conid in conids]
	for sect in state.sections:
		if isinstance(sect, section.Connector):
			sect.setpools()

