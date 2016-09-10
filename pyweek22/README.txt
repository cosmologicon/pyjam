Dr. Zome's Laboratory
=====================

Entry in PyWeek 22  <http://www.pyweek.org/22/>
URL: https://pyweek.org/e/unifac22/
Team: Universe Factory 22
Members:
	* Christopher Night (Cosmologicon)
	* Charles McPillan (EnigmaticArcher)
	* Mary Bichner (marybee)
	* Randy Parcel
	* Pat Bordenave
	* Samantha Thompson
	* Jordan Gray
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.3+
	pygame 1.9+

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

See below for available command-line arguments.

Playing the Game
----------------

Use the mouse to follow the in-game instructions. For strategy, tips, and discussion, please see our
entry page at:

    https://pyweek.org/e/unifac22/

Keyboard commands:

	Esc: quit
	F11: toggle fullscreen
	F12: take screenshot
	Space: skip dialog line
	Tab: skip dialog conversation
	1/2: zoom
	Ctrl-click: acts as right-click

Command-line arguments
----------------------

    --fullscreen : start in fullscreen mode
    --res=### : set the verical resolution (defaults to 480), e.g. --res=640
    --big : equivalent to --res=960
    --loweffect : disable some special effects for a better framerate
    --noeffect : disable all special effects for best framerate
    --reset : delete save game
