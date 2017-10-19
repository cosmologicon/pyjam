# Add a challenge segment to the state

import json, math, os.path
from . import state, view, thing, hill

data = {}
def getdata(cname):
	if cname in data:
		return data[cname]
	data[cname] = json.load(open(os.path.join("leveldata", cname + ".json"), "r"))
	return data[cname]


def addchallenge(cname):
	# Add connector hill to reset to 0
	lasthill = max(state.hills, key = lambda h: view.xmatchatplayer(h.hilltopend()[0], h.z, 0))
	lastx, lasty = lasthill.hilltopend()
	lastz = lasthill.z
	x0 = view.xmatchatplayer(lastx, lastz, 0) + 5
	ystart = lasty - 5
	xend = 10 + 2 * abs(ystart)
	fracs = [0, 0.2, 0.4, 0.6, 0.8, 1]
	spec = (
		tuple((f * xend, ystart * math.cos(f * math.tau / 4) ** 2) for f in fracs),
		((0.5, ystart - 5), (xend/4, ystart*2/3 - 5), (xend*0.75, ystart/3 - 5), (xend - 0.5, -5)),
		((0, ystart - 10), (xend, -10)),
		((-2, ystart - 20), (xend + 2, -20)),
		((-5, -30), (xend + 5, -30)),
	)
	state.addhill(thing.Hill(x = x0, y = 0, z = 0, spec = spec))

	x0 += xend + 5

	hills, hazards = getdata(cname)
	for h in hills:
		x = x0 + h["x"]
		state.addhill(thing.Hill(x = x, y = h["y"], z = h["z"],
			spec = hill.getspec(h)))
	for h in hazards:
		X0 = x0 + h["X0"]
		state.hazards.append(thing.Hazard(x = h["x"] - h["X0"], y = h["y"], z = h["z"] - 0.0001,
			vx = h["vx"], vy = h["vy"],
			r = h["r"],
			X0 = X0))


