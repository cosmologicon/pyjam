Nightfeel
=========

Entry in PyWeek 41  <http://www.pyweek.org/unifac41/>
URL: https://www.pyweek.org/e/unifac41/
Team: Universe Factory 41
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

A simple puzzle game about the feeling of watching the stars come out after
sunset on a moonless night. Join visible stars together to create
constellations. You'll need to remake them when more stars appear.

The last stage is magnitude 5.5 (60 stars). If you complete it a screenshot
should appear in this directory with your solution.

This game turned out harder than I expected. Once you understand the rules,
feel free to skip ahead with F2 if you're stuck!

Rules
-----

* Links may not cross each other
* Each star has a number 1-4. It must have exactly this many links to other
  stars.
* Stars labeled Y (yellow) require 3 links. In addition, the links must be
  spaced apart by at least 90 degrees from one another. That is, no two links
  may make an acute angle at a Y star.
* Stars labeled X (red) require 4 links. In addition, no two X stars may be
  connected, either directly or indirectly through other stars. That is, at
  most one X star may appear in a constellation.

Requirements
------------

Python 3 and Pygame. Developed using Python 3.12.3 and Pygame 2.5.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

Controls
--------

* Left-click and drag: make a link between two stars.
* Right-click on a star: remove all links to that star.

Additional keys
---------------

* F2: cheat (advance)
* F10: change resolution (cycle through several options)
* F11: toggle fullscreen
* F12: take screenshot
* Esc: quit

AI disclosure
-------------

No generative AI was used in the making of this game.


