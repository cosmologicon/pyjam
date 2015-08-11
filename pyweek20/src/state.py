import json, os.path

worlddata = json.load(open(os.path.join("data", "worlddata.json")))
R = worlddata["R"]
Rcore = worlddata["Rcore"]

you = None
ships = []
objs = []
filaments = []
hazards = []

goals = []


