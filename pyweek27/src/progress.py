from __future__ import division
import os, json
from . import settings, stagedata

donestory = False
donebonus = False

# Unlocked in free play mode
shapes = ["Shard", "Blade", "Bar", "Branch"]
colors = ["#ffffff"]
sizes = [2]

stage = 1
stageshapes = 1
stagecolors = 1
stagesizes = 1

maxshapes = 6

beaten = []

tocheck = True

def beat(stagename):
	global stage, donestory, donebonus, stageshapes, stagecolors, stagesizes, maxshapes, tocheck
	if stagename in beaten:
		return
	beaten.append(stagename)
	if stagename == "stage1":
		stage = max(stage, 2)
	if stagename == "stage2":
		stage = max(stage, 3)
	if stagename == "stage3":
		stage = max(stage, 4)
	if stagename == "stage4":
		stage = max(stage, 5)
	if stagename == "stage5":
		stage = max(stage, 6)
	if stagename == "stage6":
		donestory = True
	if stagename == "shape1":
		stageshapes = max(stageshapes, 2)
		if "Claw" not in shapes:
			shapes.append("Claw")
	if stagename == "shape2":
		stageshapes = max(stageshapes, 3)
		if "Cusp" not in shapes:
			shapes.append("Cusp")
	if stagename == "shape3":
		if "Star" not in shapes:
			shapes.append("Star")
	if stagename == "color1":
		stagecolors = max(stagecolors, 2)
		for color in ["#999999", "#ffaaaa", "#aaffaa", "#aaaaff"]:
			if color not in colors:
				colors.append(color)
	if stagename == "color2":
		stagecolors = max(stagecolors, 3)
		for color in ["#ffbb99", "#feff77", "#aa77ff"]:
			if color not in colors:
				colors.append(color)
	if stagename == "color3":
		for color in ["?"]:
			if color not in colors:
				colors.append(color)
	if stagename == "size1":
		stagesizes = max(stagesizes, 2)
		for size in [3]:
			if size not in sizes:
				sizes.append(size)
	if stagename == "size2":
		stagesizes = max(stagesizes, 3)
		for size in [1]:
			if size not in sizes:
				sizes.append(size)
	if stagename == "size3":
		for size in [0, 4]:
			if size not in sizes:
				sizes.append(size)
	colors.sort()
	sizes.sort()

	donebonus = all(s in beaten for s in ["color3", "shape3", "size3"])
	points = len(beaten) + len([s for s in beaten if "size" in s])
	maxshapes = max(maxshapes, points)
	save()
	tocheck = True

def check():
	global tocheck
	r = tocheck
	tocheck = False
	return r

def save():
	state = donestory, donebonus, shapes, colors, sizes, stage, stageshapes, stagecolors, stagesizes, maxshapes, beaten
	json.dump(state, open(settings.savefilename, "w"))

def canload():
	return os.path.exists(settings.savefilename)

def load():
	global donestory, donebonus, shapes, colors, sizes, stage, stageshapes, stagecolors, stagesizes, maxshapes, beaten
	state = json.load(open(settings.savefilename, "r"))
	donestory, donebonus, shapes, colors, sizes, stage, stageshapes, stagecolors, stagesizes, maxshapes, beaten = state

if settings.unlockall:
	for stagename in stagedata.store:
		beat(stagename)



