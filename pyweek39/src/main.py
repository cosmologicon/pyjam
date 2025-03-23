import pygame
from . import settings, view
from . import scene, playscene, state

pygame.init()

scene.current = playscene
scene.current.init()
state.load()

view.init()
clock = pygame.time.Clock()
playing = True
while playing:
    dt = min(0.001 * clock.tick(settings.maxfps), 1 / settings.minfps)
    kdowns = set()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:
            for kname, values in settings.keys.items():
                if event.key in values:
                    kdowns.add(kname)
    if "quit" in kdowns:
        playing = False
            
    current = scene.current
    current.think(dt, kdowns)
    current.draw()

    pygame.display.flip()


