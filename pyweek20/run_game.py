import math
math.tau = 2 * math.pi
# Modulo an angle in radians toward zero
math.Xmod = lambda dX: (dX + math.pi) % math.tau - math.pi
math.clamp = lambda x, a, b: a if x < a else b if x > b else x

from src import main
