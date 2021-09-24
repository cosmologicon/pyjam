import pickle, math
from . import geometry

points, allwalls, regions, locks, objs, checkpoints = pickle.load(open("gamemap.pkl", "rb"))

def fuzzpos(pos):
	x, y = pos
	return x + 1e-6 * math.fuzz(x, y, 0), y + 1e-6 * math.fuzz(x, y, 1)

walls = []

for p0, p1 in allwalls:
#	if p0 not in locks and p1 not in locks:
	walls.append((fuzzpos(p0), fuzzpos(p1)))

data = []
headstart = 0


toclaim = set(fuzzpos(lock) for lock in locks)
lockps = []


for jregion, region in enumerate(regions):
	def inregion(p):
		return geometry.polywind(region, p) != 0
	def nearregion(p0, r = 3):
		return any(inregion(p) for p in math.CSround(12, r = r, jtheta0 = math.phi, center = p0))
	ldata = {}
	data.append(ldata)
	ldata["region"] = region
	cps = [cp for cp in checkpoints if inregion(cp)]
	assert len(cps) == 1
	ldata["youpos"] = fuzzpos(cps[0])
	ldata["youtheta"] = checkpoints[cps[0]] * math.tau / 24
	ldata["headstart"] = headstart

	ldata["energy"] = []
	ldata["keys"] = []
	ldata["stars"] = []
	for objpos, objtype in objs.items():
		objpos = fuzzpos(objpos)
		if not inregion(objpos):
			continue
		numreq = 2 if "2" in objtype else 3 if "3" in objtype else 4 if "4" in objtype else -1 if "X" in objtype else 0
		windreq = -1 if "R" in objtype else 1 if "L" in objtype else None
		r = 2.5 if "big" in objtype else 1.2
		objspec = {
			"pos": objpos,
			"numreq": numreq,
			"windreq": windreq,
			"r": r,
		}
		if objtype == "+":
			headstart += 1
			ldata["energy"].append(objpos)
		elif "X" in objtype:
			ldata["stars"].append(objspec)
		else:
			ldata["keys"].append(objspec)

	for lockpos in set(toclaim):
		if nearregion(lockpos):
			lockps.append((lockpos, jregion))
			toclaim.remove(lockpos)
#	lockps = set(a for p in ldata["locks"] for a in p)
#	ldata["lockwalls"] = [wall for wall in allwalls if lockps & set(wall)]
	
maxstage = len(regions)



