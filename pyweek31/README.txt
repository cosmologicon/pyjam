Gnorman's Copse
===============

Entry in PyWeek 31  <http://www.pyweek.org/31/>
URL: https://www.pyweek.org/e/unifac31/
Team: Universe Factory 31
Members: Christopher Night (Cosmologicon)
License: see LICENSE.txt

About / How to Play
-------------------

copse (noun): a thicket of trees.

Hex-based puzzle game where you help gnomes build copses to collect magic. Control using the mouse.
Open the Help & Settings menu inside the game for full control info and tips.

Requirements
------------

This game was developed on Ubuntu Linux using Python 3.6.9 and pygame 1.9.6. That should be all you
need.

Sorry I couldn't test it on every version. If the game doesn't work for you, please leave a comment
at the URL above, with your version and platform.

Running the Game
----------------

Open a terminal / console and "cd" to the game directory and run:

    python3 run_game.py

Command line options are:

--res=### : vertical resolution in pixels. Can cycle through resolutions in-game with F10.
--fullscreen : enter fullscreen mode. Can be toggled in-game with F11.
--forceres (--noforceres) : keep window resolution when entering fullscreen mode.

--reset : Delete all saved progress.
--resetsettings : Delete saved settings.
--unlockall : Unlock all stages (cheat code).

--silence : disable sound and music
--nofx : disable minor graphical effects. Can be set in the Settings menu in-game.

