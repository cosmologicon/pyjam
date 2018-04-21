
def name(levelname):
	if levelname == "act0.level1":
		return "Tutorial 1"
	if levelname == "act0.level2":
		return "Tutorial 2"
	if levelname == "act0.level3":
		return "Tutorial 3"
	if levelname == "act0.level5":
		return "Tutorial 4"
	if levelname.endswith("level1"):
		return "Not alone"
	if levelname.endswith("level2"):
		return "One another"
	if levelname.endswith("level3"):
		return "Race to win"
	if levelname.endswith("level5"):
		return "The End"

class act0:
	pass
class act1:
	pass
class act2:
	pass
class act3:
	pass

act0.level1 = """
xP	x	x	xX
"""

act0.level2 = """
xX	x	x3	x	xP
x		x		x
x1	x	x	x	x5
x		x		x
xP	x	x11	x	xP
"""

act0.level3 = """
xX	x	x	32	P
.		x		.
.		x		.
.	x	x9	x	.
.		x		.
.		x		.
16	.	xP	x10	xP
"""

act0.level5 = """
yP	y	y	xX
"""

act1.level1 = """
		x	x	dP	y12	y		
	x	x8	x8	x	.	y	y	
x	x	x8	xX	x	x	cyP	y	y
x	x	x	x	x	.	y	y	y
x	x	x	x	aP	y	y	y	y
x	x	x	.	y	y	y	y	y
x	x	exP	y	y	yY	y8	y	y
	x	x	.	y	y8	y8	y	
		x	x12	bP	y	y		
"""

act1.level2 = """
		yY		
		y		
	.	y	.	
bP	y	y	.	eP
cP	.	aP	11	fP
dP	.	x	x	gP
	.	x	.	
		x		
		xX		
"""

act1.level3 = """
y	y	y	dy	10	.	.	cP
y	.	.	y	10	.	.	.
y	.	.	y	10	.	.	.
yY	.	.	y	10	10	10	10
x	x	x	bP	x	x	x	x
x	.	.	y	.	.	.	x
x	.	.	y	.	.	.	x
aP	y	y	y	xX	x	x	x
"""

act1.level5 = """
			y	.			
	P	y	.	.	x	cP	
	.	xX	.	y	.	x	
P	x	.	P	x	.	bP	.
x	y	y	.	aP	x	x	y
	x	.	y	.	Y	.	
	.	.	x	.	.	y	
			dP	y			
"""

act1.level6 = """
			y	xdP			
	xeP	y	x	ys	x	y	
	y	x	xs	yc	ybP	x	
xX	x	y	xs	xS	xa	y	y
x	x	y	x	y	xs	y	yY
	x	fP	y	x	y	x	
	ys	y	xs	y	gP	ys	
			y	ys			
"""

act2.level1 = """
		x	x	dP	y12	y		
	x	x8	x8	x	.	y	y	
x	x	x8	xX	x	x	cyP	y	y
x	x	x	x	kx	.	y	y	y
x	x	x	jx	aP	y	y	y	y
x	x	x	.	y	y	y	y	y
x	x	exP	y	y	yY	y8	y	y
	x	x	.	y	y8	y8	y	
		x	x12	bP	y	y		
"""

act2.level2 = """
		yY		
		y		
	.	y	.	
fP	y	y	.	eP
gP	10	aP	8	bP
cP	.	x	x	dP
	.	x	.	
		x		
		xX		
"""

act2.level3 = """
y	y	y	y	11	.	.	P
y	.	.	y	11	.	.	.
y	.	.	y	11	.	.	.
yY	.	.	y	11	11	11	11
x	x	x	aP	x	x	x	x
x	.	.	y	.	.	.	x
x	.	.	y	.	.	.	x
bP	y	y	y	xX	x	x	x
"""


act2.level5 = """
			y	.			
	fP	y	.	.	x	cP	
	.	xX	.	y	.	x	
gP	x	.	eP	x	.	bP	.
x	y	y	.	aP	x	x	y
	x	.	y	.	yY	.	
	.	h	x	.	.	y	
			dP	y			
"""

act3.level1 = act1.level1
act3.level2 = act1.level2
act3.level3 = act1.level3
act3.level5 = act1.level5
act3.level6 = act1.level6


