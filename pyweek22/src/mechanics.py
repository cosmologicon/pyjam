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
	"XY": "Weak defensive antibody\n4x chance of collecting RNA from viruses.\nTargets closest to cell",
	# level 4
	"XXX": "High-speed weak defensive antibody\nTargets closest to cell.",
	"XXY": "Long-distance medium defensive antibody",
	"XYY": "Medium defensive antibody that knocks back viruses",
	# level 5
	"YYY": "Generates DNA over time.",
	"Z": "Speeds up recovery of nearby antibodies",



#	"ZZ": "Very rapid recovery for nearby antibodies",
	"XZ": "Defensive antibody that damages nearby viruses when it hits",
	"YZ": "Generates DNA over time",
	"XYZ": "Explosive that deals damage to nearby viruses.\nDouble-click to activate!",
	"ZZZ": "Explosive that deals massive damage to nearby viruses.\nDouble-click to activate!",
}

# Lasers

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
XYrewardprob = 0.8, 0
XYkick = 20

XXXrecharge = 0.2
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
XZstrength = 2
XZaoestrength = 1
XZaoesize = 20
XZrewardprob = 0.1, 0
XZkick = 40

# ATP generation

Yrecharge = 6  # ATP generation recharge time in seconds
Ykick = 40  # Approximate distance than the ATP is kicked out by the tower when generated

YYYrecharge = 15
YYYkick = 40

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


wasphp = 200
waspspeed = 25
waspspawntime = 6
waspstages = 50, 0
waspsizes = 16, 10

fleahp = 30
fleatkick = 8
fleadamage = 10

