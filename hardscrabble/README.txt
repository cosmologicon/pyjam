Planet Hardscrabble
===================

Entry in PyWeek 37  <http://www.pyweek.org/37/>
URL: https://www.pyweek.org/e/unifac37/
Team: Universe Factory 37
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

How it fits the theme (Tube): The main mechanic is building tube-like conduits
between habitats.

I recommend playing through at least the Tutorial (which should take 5-10
minutes) and 5 minutes of Easy Mode before rating the game.

Requirements
------------

Python 3 and Pygame. Developed using Python 3.10.12 and Pygame 2.1.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Game Mode
---------

There are a total of 38 habitats in Easy Mode. It takes me about 10 minutes to
complete. Hard Mode is much harder. I don't recommend it unless you find Easy
Mode to be trivial. The story is the same in either mode.

How to play
-----------

Just play the in-game tutorial, and only read this section if something is
unclear.

Control with the mouse. If you have a right mouse button then the keyboard is
optional.

Conduits (tubes) carry one resource in one direction from one habitat (dome) to
another. To place a conduit, left click on the starting habitat, then left click
on tiles to draw a path to the second habitat. To undo the last tile, just click
it again. You can also drag to create paths. Paths may not make a sharp turn.

Select a conduit by left clicking on it. Use the buttons on the lower left to
change the conduit's resource and direction. Remove it by pressing Backspace.

Most habitats start out inactive, and they require certain resources (indicated
in the top left) to become active. Once activated, they provide certain
resources (indicated in the bottom right) to other habitats. Activate all the
habitats to win.

Conduits may not cross rocks or each other. However, you can use habitats that
have been activated to route resources past each other. Any resources passed
into an activated habitat (other than the ones it requires) will be available
as output, in any direction as long as there's room.

The five symbol buttons in the top left let you highlight a certain type of
resource. Hover over a button or click on it to darken all resources except for
that one. Click again to deselect.

Met Demand: this button toggles the visibility of resources that a habitat
needs (top left) which it has received. Can be set to OFF, DIM (visible but
darker), or ON.

Claimed Supply: this button toggles the visibility of resources that a habitat
is producing (bottom right) which has been claimed by some conduit. Can be set
to OFF, DIM, or ON.

Once you understand the mechanics, I recommend setting both of these to OFF
while you're building out to new areas. However, it might help to turn them back
on when you're rerouting existing conduits through a dense area.

Strategy tips: start with habitats that are far from their suppliers, for
example habitats that require circles but are far from any habitat that produces
circles. You'll probably need to route a few things through the center of the
board later on. Try to avoid long conduits through the center, as they can cut
off one side of the board from the other.

Control reference
-----------------

* Tab: show/hide controls
* Left click or drag: build conduit
* Right click: cancel build
* Right drag, WASD, arrow keys: pan
* Scroll wheel or 1 and 2 keys: zoom
* Backspace: delete selected conduit
* F10: change resolution
* F11: toggle fullscreen
* F12: screenshot
* Esc: quit back to menu (progress is saved)

Settings
--------

Some of the variables in src/settings.py may be tweaked to your liking:

* `autosave_seconds`: time between autosaves while playing.
* `sfxvolume` and `musicvolume`: set to any value between 0 and 1
* `keys`: add or change pygame key codes for game controls
* `height`: vertical resolution in pixels (e.g. 720). Do not change `size0`.
* `forceres`: whether to maintain the specified resolution in fullscreen mode.
* `PALETTES`: selectable color palettes. If you want to customize the symbol
	colors in the game, add a palette object and define the keys "R", "O", "Y",
	"G", and "B" with the corresponding color codes.

To delete your saved game and start over: just remove the corresponding
save-*.pkl file. Your preferences including color palette are stored in
settings.pkl, which you can delete if you want to reset them.


