On the Nature of Reflections
============================

Entry in PyWeek 33  <http://www.pyweek.org/33/>
URL: https://www.pyweek.org/e/unifac33/
Team: Universe Factory 33
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Requirements
------------

Requires Python 3 and Pygame 1.9. Tested on Ubuntu using Python 3.8 with Pygame 1.9.6, and
Python 3.9 with Pygame 2.1.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Or if you have pip installed:

	pip install -r requirements

To Run
------

From the game directory:

	pygame run_game.py

About the Game
--------------

You play a theoretical physicist who is transported to a realm where he may explore the nature of
reflections. Move mirrors to align lines of sight so that you and your reflection may work together.

How it fits the theme: the physicist sees his reflection as his evil twin, countering his every
move.

There are 8 quick stages, with the last one being very optional. Expect 5-10 minutes of gameplay.
If you get stuck at any point, hold Shift for a tip, and skip any stage you don't want to play.

The game uses a lot of unoptimized draw calls to implement the reflections. You may have performance
issues especially in the later levels. Pressing F10 to reduce the resolution may help. The game
should be playable even down to 5fps or so, but feel free to skip any levels you don't want to play.

Controls
--------

To change the controls, edit src/settings.py starting at line 11.

* Arrow keys or WASD: move
* Space or Enter: grab/place statue and mirrors, activate plates
* Hold Shift: display tip
* Hold Ctrl: zoom out
* 1/2: skip to previous/next stage
* Tab: hide/show controls
* Esc: quit
* F10: cycle resolution
* F11: toggle fullscreen
* F12: screenshot


Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py
