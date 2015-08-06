Testing for PyWeek
------------------

This subdirectory is to test pygame functions so that collaborators can check that the game will run
on their system before the competition starts.

Run the test "game" from the command line:

	python run_game.py

Or if you have pygame for python3 installed:

	python3 run_game.py

Things to check (all should be "yes"):

	1. Does pressing Esc quit the game?
	2. Can you close the window to quit the game (not in fullscreen mode)?
	3. Does fullscreen mode actually take up most of your screen?
	4. Does quitting the game in fullscreen (press Esc) affect your desktop resolution settings, even after the game is closed?
	5. Is the mouse cursor visible when the mouse moves over the window? Also in fullscreen?
	6. Does the appearance of the window match the reference image (screenshot.png)?
	7. Does the white circle appear circular (not stretched or squashed)?
	8. Do the color filters of the Earth image match the reference image?
	9. Does the Earth image appear within a black square, and the egg not appear within any rectangle?
	10. Does the egg lack resizing artifacts around the edge?
	11. Does the sound play when you click the button without a noticeable delay?
	12. Does the sound play without being clipped or cut off?
	13. Does the sound play at about the same volume as when you open the sound file directly (in the data directory)?

