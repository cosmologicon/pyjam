Storm Drain Odyssey
===================

Entry in PyWeek 26  <http://www.pyweek.org/26/>
URL: https://www.pyweek.org/e/unifac26/
Team: Universe Factory 26
Members: Christopher Night (Cosmologicon), Mitch Bryson (mit-mit), Mary Bichner (marybee), Charles McPillan (EnigmaticArcher), Minh Huynh, Jules Van Oosterom
License: see LICENSE.txt

Requirements
------------

	python 2.7+ or 3.5+
	pygame 1.9.2+
	numpy
	pyopengl
	

To install the requirements on Ubuntu:

	sudo apt install python python-pygame python-numpy python-opengl
	sudo apt install python3 python3-pygame python3-numpy python3-opengl

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py
    python3 run_game.py

Command line options:

	--fullscreen: full screen mode
	--reset: delete saved game and start over

Controls
--------

  * Arrow keys or WASD: move
  * Shift or Z: about face
  * Space or Enter: jump
  * Space or Enter: open a drain (when over a drain)
  * Double-tap Space or Enter: dive
  * Esc: quit
  * M: view map
  * Click with mouse: enable/disable manual camera control
  * F10: cycle resolutions (360p, 480p, 720p, 1080p)
  * F11: toggle fullscreen

Cheat codes
-----------

Here's some cheats in case you need to skip ahead. Don't hesitate to use them if you're stuck!

  * 0: go to central room
  * 1: go to end of Northwest challenge (the maze)
  * 2: go to end of Northeast challenge (the rapids)
  * 3: go to end of Southwest challenge (the whirlpools)
  * 4: go to end of Southeast challenge (the puzzle)
  * 5: get fish food

In particular, it's possible to get the Southeast challenge into a state you can't win from, and
there's no way to reset. If that happens to you, just press 4 to skip it!

Mechanics
---------

Make your way through the pipes to safety. Every room has a pressure level. If two rooms are on the
same level, you may go from one room to the next as long as the pressure is not more than one level
higher. So you can't go directly from a room with pressure 2 to one with pressure 4.

Opening a drain above a room will increase the pressure in that room. This will allow you to access
new areas.

Pipes (smaller and higher than tunnels) may only be entered if you're charged up. Find fish food to
get a charge that can take you up one pipe.
