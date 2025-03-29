import pygame, math
from . import ocean, pview, ptext, settings, grid, state, thing, view
from .pview import T

class self:
    ...

def init():
    self.t = 0

def canquit():
    return False

def finish():
    from . import scene, playscene
    scene.current = playscene

def think(dt, kdowns):
    self.t += dt
    if "turbine" in kdowns or "quit" in kdowns or "flow" in kdowns:
        finish()

def draw():
    ocean.draw()
    ptext.draw(f"{settings.gamename}: How to Play", midtop = T(640, 10), fontsize = T(50),
        color = (200, 200, 240))
    text = " ".join([
        "Use arrow keys or WASD to move.",
        "Each step requires 1 fuel.",
        "Return to Anyport (starting point) to refuel.",
        "On wind tiles you must move downstream (in the direction of the wind), but this does not use fuel.",
        "\n\nPress Space (or Enter) to activate the turbine.",
        "When the turbine is active, press a direction to create a wind stream in that direction.",
        "Costs 3 fuel.",
        "You can redirect existing wind streams with the turbine.",
        "Stronger winds require more fuel to redirect, and can only be done after collecting enough artifacts.",
        "\n\nYou can also press Space again when the turbine is active to dispel wind (change it to a calm tile).",
        "\n\nPress Tab when on a wind tile to flow.",
        "You will move downstream and repeat until you get to a calm tile.",
        "\n\nThe game auto-saves whenever you return to Anyport.",
        "Press Esc at any time to reload the last save. Press Esc again to quit the game.",
    ])
    ptext.draw(text, topleft = T(40, 100), width = T(500), fontsize = T(20), color = (200, 200, 240))


    for strength in (1, 2, 3):
        f = pygame.time.get_ticks() * 0.001 * 0.5 * strength
        tile = grid.windtile(strength, T(140), f, grid.E)
        y = 280 + 120 * strength
        pview.screen.blit(tile, tile.get_rect(center = T(680, y)))
        text = f"{state.turbinefuel[strength]} fuel to redirect"
        if state.turbinelevel[strength]:
            text += f"\nRequires {state.turbinelevel[strength]} Artifact"
        ptext.draw(text, center = T(860, y), fontsize = T(20), color = (200, 200, 200))

    text = " ".join([
        "Collect nimbite gas and bring it back to Anyport to upgrade the fuel tank.",
        "Collect artifacts and bring them back to Anyport to upgrade the turbine.",
        "The first 4 artifacts can be found directly North, South, East, and West of Anyport.",
    ])
    ptext.draw(text, topleft = T(580, 100), width = T(400), fontsize = T(22), color = (200, 200, 240))

    view.camera.x0 = 0
    view.camera.y0 = 0
    view.camera.scale = 100
    gtypes = thing.Copper, thing.Silver, thing.Gold, thing.Jewel, thing.Artifact
    for j, gtype in enumerate(gtypes):
        thing.drawgettable((4, 1.2 - j), gtype.color, gtype.size, True, j)
        text = "Artifact" if gtype is thing.Artifact else f"{gtype.value} Nimbite"
        color = "white" if gtype is thing.Artifact else gtype.color
        ptext.draw(text, center = T(1170, 240 + 100 * j), fontsize = T(24), color = color)
    alpha = int(math.interp(self.t, 0, 255, 0.5, 0))
    if alpha:
        pview.fill((0, 0, 20, alpha))

