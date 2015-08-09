import json, os.path

worlddata = json.load(open(os.path.join("data", "worlddata.json")))
R = worlddata["R"]
Rcore = worlddata["Rcore"]

