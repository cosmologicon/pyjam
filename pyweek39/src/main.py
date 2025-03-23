import pygame
from . import settings, view
from . import scene, playscene

pygame.init()

scene.current = playscene
scene.current.init()

view.init()
clock = pygame.time.Clock()
playing = True
while playing:
    dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            playing = False
    kdowns = pygame.key.get_pressed()
    current = scene.current
    current.think(dt, kdowns)
    current.draw()

    pygame.display.flip()


