# CONTROLS

tclick = 0.3  # maximum time the mouse can be held down and still count as a click, in seconds
dclick = 4  # maximum distance the mouse can move and still count as a click, in pixels
tdoubleclick = 0.6  # maximum time between clicks in a double click

# ORGANELLES

Xcost1 = 5
Xcost2 = 0
Ycost1 = 5
Ycost2 = 0
Zcost1 = 20
Zcost2 = 5

Xthatch = 8
Ythatch = 12
Zthatch = 20

## TOWERS

towerinfo = {
	"X": "Basic defensive antibody",
	"Y": "Generates RNA over time",
	"XX": "Medium-strength defensive antibody",
	"XY": "Medium-strength defensive antibody\nDoubles the chance of collecting RNA from viruses.",
	"XXX": "High-speed defensive antibody",
}

# Lasers

Xrecharge = 2  # shot rechange time in seconds
Xrange = 40
Xstrength = 1
Xrewardprob = 0.2, 0  # probability that an enemy killed by this tower will drop ATP1 and ATP2
Xkick = 0  # How far back an enemy gets kicked when hit by this tower

XXrecharge = 4
XXrange = 50
XXstrength = 3
XXrewardprob = 0.2, 0
XXkick = 10

XYrecharge = 5
XYrange = 40
XYstrength = 1
XYrewardprob = 0.4, 0
XYkick = 10

XXXrecharge = 0.5
XXXrange = 40
XXXstrength = 1
XXXrewardprob = 0.2, 0
XXXkick = 10

XXYrecharge = 5
XXYrange = 150
XXYstrength = 5
XXYrewardprob = 0.1, 0
XXYkick = 10

XYrecharge = 2
XYrange = 40
XYstrength = 1
XYrewardprob = 0.1, 0
XYkick = 1000

XZrecharge = 1
XZrange = 60
XZstrength = 2
XZaoestrength = 1
XZaoesize = 20
XZrewardprob = 0.1, 0
XZkick = 100

# ATP generation

Yrecharge = 6  # ATP generation recharge time in seconds
Ykick = 40  # Approximate distance than the ATP is kicked out by the tower when generated

YYrecharge = 15
YYkick = 40

YZrecharge = 5
YZkick = 40

# healing

Zrecharge = 0.5
Zrange = 30
Zstrength = 1.5

# bomb

XYZstrength = 20
XYZwavesize = 40

ZZZstrength = 60
ZZZwavesize = 80

# WEAPONS

bulletspeed = 80
healrayspeed = 120

# ENEMIES

anthp = 1
antspeed = 10
antdamage = 1
antsize = 6

Lanthp = 10
Lantspeed = 5
Lantdamage = 10
Lantcarried = 5
Lantsize = 12

beehp = 1000
beetlehp = 10

wasphp = 40
waspspeed = 25
waspspawntime = 6
waspstages = 10, 0
waspsizes = 16, 10



