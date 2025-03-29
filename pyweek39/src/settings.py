import pygame

gamename = "Anyport"
savegame = "save.pkl"

resolution = 1280, 720  # DO NOT CHANGE

# If you want a different resolution, add it to this list and press F10 in the game.
heights = 360, 480, 720, 1080

# Set between 0 and 1. 0 to disable sound.
sfxvol = 0.8
musicvol = 0.8

minfps, maxfps = 5, 120

# Shows the FPS counter
DEBUG = False

# Set to False to disable the lightning effect.
lightning = True

# Add alternate keys to the corresponding list as desired.
keys = {
    "up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
    "left": [pygame.K_LEFT, pygame.K_a],
    "right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
    "down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
    "flow": [pygame.K_TAB],
    "quit": [pygame.K_ESCAPE],
    "turbine": [pygame.K_SPACE, pygame.K_RETURN],
    "howto": [pygame.K_1, pygame.K_F1],
    "zoom": [pygame.K_2, pygame.K_F2],
    "cheat": [pygame.K_3, pygame.K_F3],
    "cycleres": [pygame.K_F10],
    "fullscreen": [pygame.K_F11],
    "screenshot": [pygame.K_F12],
}

