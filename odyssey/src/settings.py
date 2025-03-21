from pygame.locals import *
import sys, os

DEBUG = "--DEBUG" in sys.argv

gamename = "Storm Drain Odyssey"

resolution0 = 1280, 720
heights = 360, 480, 720, 1080

fullscreen = "--fullscreen" in sys.argv

leveldataname = "game"

manualcamera = False

maxfps = 120
minfps = 10

savename = os.path.join("savegame", "save.pkl")
asavename = os.path.join("savegame", "save-%Y%m%d%H%M%S.pkl")
qsavename = os.path.join("savegame", "quicksave.pkl")
qsavetime = 10
reset = "--reset" in sys.argv

debug_graphics = "--debuggfx" in sys.argv
usefasterobj = "--usefasterobj" in sys.argv
allowgfxpickle = "--allowgfxpickle" in sys.argv

# if set to true, on start-up outputs to file OpenSCAD scripts to generate section model 
# files in current map. Function to do this is "build_openscad_commands" in graphics.py,
# and it reads from the currently loaded section data (load up in debug mode) to generate
# CAD commands
GenerateOpenSCADScripts = "--build" in sys.argv
openscad_path = '/Applications/OpenSCAD_2018.app/Contents/MacOS/OpenSCAD' # varies on different systems
if not os.path.exists(openscad_path):
	openscad_path = "/snap/bin/openscad-nightly"

# Bash scripts/OpenSCAD files go to: tools/generated_section_models/scad. Run "openscad_script.sh"
# to build all models as stl.
# stl files then end up in: tools/generated_section_models/stl. Run "tools/finalise_models.py" to 
# do post processing (materials and textures). Final obj files appear in tools/generated_section_models/obj
# move the objs into to "models/<level_name>", and these will be read from when running <level_name>
#
# You should clear these three folders (obj, stl and scad) before re-generating new level data

for arg in sys.argv:
	if "=" in arg:
		oname, ovalue = arg.lstrip("-").split("=")
		if oname == "level":
			leveldataname = ovalue

keymap = {
	# Dvorak key layout too.
	"up": [K_UP, K_w, K_COMMA],
	"down": [K_DOWN, K_s, K_o],
	"left": [K_LEFT, K_a],
	"right": [K_RIGHT, K_d, K_e],
	"turn": [K_LSHIFT, K_z, K_SEMICOLON],
	"act": [K_SPACE, K_RETURN],
	
	"map": [K_m],
	"quit": [K_ESCAPE],
	
	"debugspeed": [K_F1],
}

