
costs = {
	"segment": 1,
	"office": 10,
	"spire": 20,
}

maxheight = 0
money = 100
maxmoney = 100
things = []

def getcost(costtype):
	if costtype == "grow":
		return growcost()
	else:
		return costs[costtype]

def spend(costtype):
	global money
	amount = getcost(costtype)
	if money < amount:
		return False
	money -= amount
	return True

def earn(amount):
	global money
	money = min(money + amount, maxmoney)

def growcost():
	return maxheight

def growto(h):
	global maxheight
	from . import grid
	maxheight = h
	for y in range(0, h):
		segs = ((0, y), (0, y + 1)), ((y, y), (y + 1, y + 1))
		for seg in segs:
			grid.addsegment(seg)

def grow():
	if not spend("grow"):
		return False
	growto(maxheight + 1)

def inbounds(pG):
	xG, yG = pG
	return yG <= maxheight


