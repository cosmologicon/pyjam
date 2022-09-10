Ares Firma
==========

Entry in PyWeek 34  <http://www.pyweek.org/34/>
URL: https://www.pyweek.org/e/unifac34/
Team: Universe Factory 34
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

The young planet Mars is covered with oceans. Use solar radiation to boil them off. Do it quick,
before life evolves and takes over!

There are 5 quick stages to introduce the mechanics, then a challenge stage, and a final optional
bonus stage that's a little more fast-paced. The goal in each stage is to reduce ocean cover below
1%. There's no save game, but see Controls to skip between stages as desired.

Completing the bonus stage doesn't get you anything but a score. Can you get lower than 1000 million
years?

I recommend at least finishing the tutorial and trying the Challenge stage before rating the game.
This should take about 5 minutes of gameplay.

How it fits the theme: This game depicts the story of how Mars became the red planet.

Requirements
------------

Requires Python 3, pygame, and numpy. Tested using:

* Python 3.8.10 with pygame 1.9.6 and numpy 1.17.4
* Python 3.9.5 with pygame 2.1.2 and numpy 1.23.3

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

If the game runs slowly you can try swapping to a lower resolution with F10, or lowering the
variable mapres on line 7 of src/settings.py. 

Controls
--------

See src/settings.py line 20 to change keyboard controls as desired.

* Left click or left click and drag: Use current tool.
* Right click: Swap to tool with the highest charge.
* Tab: Swap to next tool in the order.
* 1/2/3/4: Swap to tool.
* Esc: Quit.
* F1/F2: Jump between stages.
* F10: Change resolution.
* F11: Toggle fullscreen.
* F12: screenshot.

