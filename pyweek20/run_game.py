# Yeah that's right, I tack my numerical utility functions right onto the math module. Who's gonna
# stop me?
import math
math.tau = 2 * math.pi
# Modulo an angle in radians toward zero
math.Xmod = lambda dX: (dX + math.pi) % math.tau - math.pi
math.clamp = lambda x, a, b: a if x < a else b if x > b else x

from src import main
