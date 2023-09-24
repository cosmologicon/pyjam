The Mystery of the Unmatter
==========================

Entry in PyWeek 36  <http://www.pyweek.org/36/>
URL: https://www.pyweek.org/e/unifac36/
Team: Universe Factory 36
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

This is a top-down (Asteroids-like) space exploration game. The main challenge involves picking out
black objects against a dark background. Pilot your ship around to find pieces of "unmatter". The
more you discover the more tech you'll unlock.

It is highly recommended that you use the in-game feature adjust so that the main challenge is not
too easy or too difficult for you. Press F9 at any time in the game.

Before judging for PyWeek, I recommend that you play at least until you've unlocked the Xazer beam
and discovered two gravity wells. This is roughly where the tutorial ends, and should take 10-15
minutes. At that point you've gotten the gist of the game, so only keep playing if you're still
having fun. The entire game might take 45-60 minutes to finish, and the ending is underwhelming.

How it fits the theme: the game is about finding dark objects in space that are difficult to see,
very loosely inspried by real-world dark matter.

Requirements
------------

Python 3 and Pygame. Developed using Python 3.10.12 and Pygame 2.1.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

Controls
--------

Use the keyboard for the main game and the mouse for the menu. To customize keys, change the
variable `keys` in `src/settings.py`. (The following keys will not work until you unlock the
corresponding tech.)

* WASD or arrow keys: fly ship
* Space or Enter: throw gravity net (does not use charge)
* 1: use Xazer beam (uses charge, lasts until next gravnet)
* 2: use Linz flare (uses charge)
* 3: use Searchlight (uses charge, lasts until next gravnet)
* 4: activate Hyperdrive (uses charge, lasts until next gravnet, also grants invulnerability)
* Hold 5 or M: open map (does not use charge)
* Backspace: warp back to station (does not use charge)

Settings keys:

* Tab: adjust zoom level
* F9: calibrate difficulty
* F10: adjust resolution
* F11: toggle fullscreen
* F12: screenshot
