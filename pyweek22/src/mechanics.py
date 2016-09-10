# CONTROLS

tclick = 0.3  # maximum time the mouse can be held down and still count as a click, in seconds
dclick = 4  # maximum distance the mouse can move and still count as a click, in pixels
tdoubleclick = 0.6  # maximum time between clicks in a double click

# ORGANELLES

Xcost1 = 5
Xcost2 = 0
Ycost1 = 5
Ycost2 = 0
Zcost1 = 10
Zcost2 = 3

Xthatch = 8
Ythatch = 12
Zthatch = 20

## TOWERS

towerinfo = {
	# level 1
	"X": "Weak defensive antibody, good for small enemies\nTargets closest virus to cell",
	# level 2
	"XX": "Medium-strength defensive antibody\nTargets strongest virus",
	# level 3
	"Y": "Generates RNA over time",
	"XY": "Weak defensive antibody.\nGets more RNA from viruses.\nGenerates RNA over time.\nTargets closest to cell.",
	# level 4
	"YY": "Auto-collects nearby RNA and DNA.",
	"XXX": "High-speed weak defensive antibody\nTargets closest to cell.",
	"XXY": "Long-distance medium defensive antibody",
	"XYY": "Medium defensive antibody that knocks back viruses",
	# level 5
	"YYY": "Generates DNA over time.",
	"Z": "Speeds up recovery of nearby antibodies",
	# level 6
	"XZ": "Area-of-effect defensive antibody that damages nearby viruses when it hits",
	"YZ": "Rapidly generates DNA over time",
	"ZZ": "Fires lasers (can hit fast-moving viruses)",
	# level 7
	"XXZ": "Mega area-of-effect antibody!",
	"YYZ": "Mega auto-collect!",
	# level 8
	"XZZ": "Mega laser!",
	"YZZ": "Mega recover!\nAll nearby towers instantly heal when infected.",
	# level 9
	"XYZ": "Explosive that deals damage to nearby viruses.\nDouble-click to activate!",
	# Endless
	"ZZZ": "Mega explosive!\nDouble-click to activate!",
}

# Guns

Xrecharge = 2  # shot rechange time in seconds
Xrange = 40
Xstrength = 1
Xrewardprob = 0.2, 0  # probability that an enemy killed by this tower will drop ATP1 and ATP2
Xkick = 0  # How far back an enemy gets kicked when hit by this tower

XXrecharge = 4
XXrange = 50
XXstrength = 10
XXrewardprob = 0.2, 0
XXkick = 20

XYrecharge = 1.5
XYrange = 40
XYstrength = 1
XYrewardprob = 1, 0
XYkick = 20

XXXrecharge = 0.35
XXXrange = 40
XXXstrength = 1
XXXrewardprob = 0.2, 0
XXXkick = 20

XXYrecharge = 5
XXYrange = 200
XXYstrength = 10
XXYrewardprob = 0.2, 0
XXYkick = 20

XYYrecharge = 2
XYYrange = 40
XYYstrength = 1
XYYrewardprob = 0.1, 0
XYYkick = 100

# Area-of-effect towers

XZrecharge = 1
XZrange = 60
XZstrength = 10
XZaoestrength = 5
XZaoesize = 20
XZrewardprob = 0.1, 0
XZkick = 40

XXZrecharge = 3
XXZrange = 75
XXZstrength = 40
XXZaoestrength = 20
XXZaoesize = 50
XXZrewardprob = 0, 0
XXZkick = 100

# Lasers

ZZrecharge = 1
ZZrange = 50
ZZstrength = 5
ZZrewardprob = 0, 0
ZZkick = 0

XZZrecharge = 3
XZZrange = 70
XZZstrength = 25
XZZrewardprob = 0, 0
XZZkick = 0

# ATP generation

Yrecharge = 6  # ATP generation recharge time in seconds
Ykick = 40  # Approximate distance than the ATP is kicked out by the tower when generated

XYrecharge = 12
XYatpkick = 40

YYYrecharge = 15
YYYkick = 40

YZrecharge = 5
YZkick = 40

# ATP collection

YYrange = 80

YYZrange = 240

# healing

Zrecharge = 0.3  # Time between heal rays
Zrange = 30
Zstrength = 2  # Number of seconds removed from recovery time by each heal ray

YZZrecharge = 0.1
YZZrange = 30
YZZstrength = 99999

# bomb

XYZstrength = 100
XYZwavesize = 50

ZZZstrength = 200
ZZZwavesize = 80

# WEAPONS

bulletspeed = 80
healrayspeed = 120

# ENEMIES

anthp = 1
antspeed = 10
antdamage = 1
antsize = 6

Lanthp = 20
Lantspeed = 5
Lantdamage = 10
Lantcarried = 5
Lantsize = 12

beehp = 2
beespeed = 10
beedamage = 2
beesize = 6
beetdisable = 20

Lbeehp = 10
Lbeespeed = 4
Lbeedamage = 10
Lbeecarried = 3
Lbeesize = 12

fleahp = 30
fleatkick = 8
fleadamage = 10

# Bosses

wasphp = 200
waspspeed = 25
waspspawntime = 6
waspstages = 50, 0
waspsizes = 16, 10

hornethp = 600
hornetspeed = 25
hornetspawntime = 6
hornetstages = 300, 100, 0
hornetsizes = 21, 14, 7

crickethp = 2000
cricketspeed = 20
cricketspawntime = 2
cricketstages = 1000, 500, 200, 0
cricketsizes = 24, 18, 12, 6



