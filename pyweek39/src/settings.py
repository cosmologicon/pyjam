import pygame

gamename = "Downstream"

resolution = 1280, 720
heights = 360, 480, 720, 1080

minfps, maxfps = 5, 120

keys = {
    "up": [pygame.K_UP, pygame.K_w, pygame.K_COMMA],
    "left": [pygame.K_LEFT, pygame.K_a],
    "right": [pygame.K_RIGHT, pygame.K_d, pygame.K_e],
    "down": [pygame.K_DOWN, pygame.K_s, pygame.K_o],
    "quit": [pygame.K_ESCAPE],
}

