import pygame
from . import settings, view, ptext, state, pview
from . import scene, playscene, howtoscene

ptext.FONT_NAME_TEMPLATE = "fonts/%s.ttf"
ptext.DEFAULT_FONT_NAME = "Rye"
ptext.DEFAULT_OUTLINE_WIDTH = 0.5
ptext.DEFAULT_SHADOW_OFFSET = 1, 1
pygame.init()

scene.current = playscene
howtoscene.init()
playscene.init()
state.load()
playscene.returnhome()

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
    current = scene.current
    if "quit" in kdowns and current.canquit():
        kdowns.remove("quit")
        playing = False
    current.think(dt, kdowns)
    current.draw()

    ptext.draw(f"{clock.get_fps():.1f}fps", bottomright = pview.T(1270, 710), fontsize = pview.T(30), owidth = 1)
    pygame.display.flip()


