Anyport
=======

Entry in PyWeek 39  <http://www.pyweek.org/39/>
URL: https://www.pyweek.org/e/unifac39/
Team: Universe Factory 39
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

Game Info
---------

Set off from Anyport in your airship and collect resources above a stormy sea.
Upgrade your fuel tank and build jet streams to reach farther.

How it fits the theme: the main mechanic involves moving downstream in windy areas.
It seems like an obstacle at first, but it may be used to your advantage.

Requirements
------------

Python 3 and Pygame. Developed using Python 3.12.3 and Pygame 2.5.2.

To install the requirements on Ubuntu:

	sudo apt-get install python python-pygame

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python run_game.py

How to Play
-----------

Press 1 in the game at any time to bring up this info.

MOVING: Use arrow keys or WASD to move. Each step requires 1 fuel. Return to Anyport (starting
point) to refuel. On wind tiles you must move downstream (in the direction of the wind), but this
does not use fuel.

TURBINE: Press Space (or Enter) to activate the turbine. When the turbine is active, press a
direction to create a wind stream in that direction. Costs 3 fuel. You can redirect existing wind
streams with the turbine. Stronger winds require more fuel to redirect, and can only be done after
collecting enough artifacts. Level 2 costs 6 fuel and requires at least 1 artifact. Level 3 costs 12
fuel and requires at least 3 artifacts.

You can also press Space again when the turbine is active to dispel wind (change it to a calm tile).

FLOW: Press Tab when on a wind tile to flow. You will move downstream and repeat until you get to a
calm tile.

RELOAD: The game auto-saves whenever you return to Anyport. Press Esc at any time to reload the last
save. Press Esc again to quit the game.

NIMBITE: Collect nimbite gas and bring it back to Anyport to upgrade the fuel tank. The four types
of nimbite are worth 1, 3, 6, and 12.

ARTIFACTS: Collect artifacts and bring them back to Anyport for other upgrades. The first 4
artifacts can be found directly North, South, East, and West of Anyport. Upgrades:

* 1 artifact: upgrade turbine to level 2
* 2 artifacts: unlock the map. While at Anyport, you will be zoomed out. Press 2 to toggle.
* 3 artifacts: upgrade turbine to level 3
* 5 artifacts: collecting nimbite refuels (+1, +2, +3, +4)
* 7 artifacts: collecting nimbite refuels (+1, +3, +6, +12)
* 8 artifacts: end of the game

Additional options
------------------

* F10: change resolution
* F11: toggle fullscreen
* F12: quit

Delete the file `save.pkl` to start over.

There's a flashing lightning effect (visible on the title screen) in the game. If you want to
disable this, set `lightning` to `False` in `src/settings.py`.

`settings.py` also contains variables that can be used to pick a different resolution, change the
sound and music volume, and the key map. See the file for more details.



