Airscraper
==========

Entry in PyWeek 40  <http://www.pyweek.org/40/>
URL: https://www.pyweek.org/e/unifac40/
Team: Universe Factory 40
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

How it fits the theme
---------------------

You create an airscraper (underwater skyscraper) out of coral and create a
city-like ecosystem that fish can live and shop in.

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

* Left click: extend the tower. Select structures and place them on the tower.
* Scroll wheel or 1/2: zoom
* Right drag or arrows: pan
* Backspace: enter demolish mode. Click on the structure or part of the tower
  you want to remove. It must not have anything built off it.
* Esc: quit. Your game is not saved.
* F10: adjust screen resolution
* F11: toggle fullscreen
* F12: take screenshot

Gameplay
--------

Extend the tower upward in a tree structure by clicking between the outer walls.
It costs $1 to extend the tower.

To place a structure, click on the structure you want on the ground and then
click on where you want it added to the tower. You must have enough money and
there must not be anything in the way.

To remove structures, press Backspace to enter demolition mode. Click on pieces
of the tower or on structures you want to remove. You cannot remove the outer
walls, or any piece of the tower that has something built off it.

There are two kinds of structures: residences (rainbow) and shops (puple). When
you place a resident some number of fish will automatically move in and be added
to the tower population. Fish will go from their home to the nearest shop and
back, following the branches of the tower. (Nearest means the shop that takes
the fewest steps to get to following the branches.)

Shops require some time to restock. If a fish arrives in a shop and it's
restocked (100%) then the fish will make a purchase and you will gain $5.

There are three sizes of residences and three sizes of shops. Get your
population up to 30 to beat the game.


