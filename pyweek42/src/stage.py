
"""
			"top5": thing.TopSalvo5,
			"x": thing.XSalvo,
			"sweepr": thing.SweepSalvoR,
			"sweepd": thing.SweepSalvoD,
			"rlr": thing.SalvoRLR,
			"mega": thing.MegaSalvo,
			"z": thing.SalvoZ,

top5: 3 sec
rlr: 2 sec
x: 2 sec
"""

delay = {
	"top5": 3,
	"rlr": 2,
	"x": 2,
	"sweepr": 4.5,
	"sweepd": 2,
	"mega": 4,
	"edges": 2,
	"z": 4,
}
def getdelay(salvo):
	if salvo.startswith("H") or salvo.startswith("V"):
		return getdelay(salvo[1:])
	return delay[salvo]

def makespec(tstart, salvos, leeway):
	t = tstart
	spec = []
	for sset in salvos:
		for salvo in sset:
			spec.append((t, salvo))
		t += leeway + max(getdelay(salvo) for salvo in sset)
#		print(sset, max(getdelay(salvo) for salvo in sset), t)
	return spec, t + 2

def addstage(stagename, tstart, leeway, salvos):
	spec, t = makespec(tstart, salvos, leeway)
	stages[stagename] = {
		"t": t,
		"salvos": spec,
	}

stages = {}

addstage(1, 3, 0.5, [["sweepr"], ["sweepd"], ["HVsweepr"], ["HVsweepd"]])
addstage(2, 1, 0, [["top5"], ["rlr"], ["Htop5"], ["x"], ["Hrlr"], ["Vx"], ["Vtop5"], ["x", "Vx"]])
addstage(3, 1, 0, [
	["mega"],
	["Hmega"],
	["Hsweepr"],
	["rlr", "edges"],
	["sweepr", "HVsweepr"],
	["top5"],
	["x", "Vx"],
])
addstage(4, 1, 0, [
	["z"],
	["x", "Vx"],
	["rlr", "Vedges"],
	["Vmega"],
	["top5"],
	["Vrlr"],
	["top5", "Vrlr"],
	["x", "Vx"],
	["z"],
	["top5", "Vtop5"],
])


