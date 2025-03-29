import pygame

gamename = "Anyport"
savegame = "save.pkl"

resolution = 1280, 720
heights = 360, 480, 720, 1080

minfps, maxfps = 5, 120

lightning = True

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

