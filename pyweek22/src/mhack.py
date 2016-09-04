import math

math.tau = 2 * math.pi
math.clamp = lambda x, a, b: a if x < a else b if x > b else x
math.smoothstep = lambda f: 0 if f < 0 else 1 if f > 1 else f * f * (3 - 2 * f)

