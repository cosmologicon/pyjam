Timestealer
===========

Entry in PyWeek 42  <http://www.pyweek.org/42/>
URL: https://www.pyweek.org/e/unifac42/
Team: Universe Factory 42
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

Avoid hazards to escape. Charge the Timestealer device by speeding up time
during the easy moments, and discharge it to slow down time for the most
dangerous moments.

4 short stages. +1 health at the end of each stage. Very simple, short,
incomplete entry. You can beat it in 3 minutes if you're good at this sort of
action game. If it's too easy, try to win without taking damage.

How it fits the theme (Borrowed Time): The main mechanic is a device that
"borrows" time and stores it up to be used later.

Requirements
------------

Python 3, Pygame, and Numpy. Developed using Python 3.12.3, Pygame 2.5.2, and
Numpy 1.26.4

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame python3-numpy

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

Controls
--------

* Arrow keys or WASD: move.
* Space or Enter: Activate the Timestealer. If it's charged it will discharge
  until empty, and if it's discharged it will charge until full.
* Esc: quit. Progress is not saved.
* F1: skip to next stage.
* F10: change resolution.
* F11: toggle fullscreen.
* F12: take screenshot.

AI Disclosure
-------------

No generative AI, including AI-powered development tools and web search results,
was used in the creation of this game.
