Nerdozog's Ascent
=================

Entry in PyWeek 28  <http://www.pyweek.org/28/>
URL: https://www.pyweek.org/e/unifac28/
Team: Universe Factory 28
License: see LICENSE.txt

Team Members
------------

* Christopher Night (Cosmologicon)
* Xinming Zhang (xmzhang1)
* Mike Tamillow (UnicornMarkets)

Requirements
------------

	python 2.7+ or 3.3+
	pygame 1.9+
	numpy

To install the requirements on Ubuntu:

	sudo apt install python3 python3-pygame python3-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Playing the game
----------------

Complete 20 missions to win. You can continue beyond that, but there's no more story. The game is
automatically saved after each mission.

Controls
--------

Use the mouse to drag crew members to their assigned stations in the right-hand panel. Click on
stations and cars in the right-hand panel to move to there. Click on menu buttons to interact and
complete missions. Click on cars that are malfunctioning to fix them.

Optional keyboard controls are:

  * arrow keys or WASD: move between stations
  * C: jump to car on current track
  * B: open/close port when at a station
  * F10: change resolution
  * F11: toggle fullscreen
  * F12: take screenshot

Command line arguments
----------------------

  * `--res=###`, e.g. `--res=900`: specify vertical resolution
  * `--fullscreen`: start in fullscreen mode
  * `--forceres`: resolution will be same in fullscreen mode
  * `--reset`: delete saved game
  * `--nomusic`: disable music
  * `--nosound`: disable sound effects
