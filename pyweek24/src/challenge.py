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
		((0, -30), (xend, -30)),
	)
	state.addhill(thing.Hill(x = x0, y = 0, z = 0, spec = spec))

	x0 += xend + 5
	for h in getdata(cname):
		x = x0 + h["x"]
		state.addhill(thing.Hill(x = x, y = h["y"], z = h["z"],
			spec = hill.getspec(h)))

