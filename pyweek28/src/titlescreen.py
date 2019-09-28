from __future__ import division
import pygame, math, random
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest,sound,playscene, settings
from .pview import T

t = 0
point_list =[]


class Title(scene.Scene):
    def __init__(self):
        super(Title,self).__init__()
        sound.playmusic('carnivalrides')


    def think(self,dt, kpressed, kdowns, mpos, mdown, mup):
        if kdowns or mdown:
            scene.set(playscene.PlayScene())

    def draw(self):

        draw.atmosphere()
        global t
        t += 0.01
        r = 10 * (1 + t)
        if r % 20 >= 10:
            x = r*math.cos(t*360)+900
            y = r*math.sin(t*360)+600
        else:
            x = r*math.sin(t*360)+900
            y = r*math.cos(t*360)+600
        point_list.append([x,y])
        if len(point_list) >= 2:
            for i in point_list:
                pygame.draw.line(pview.screen,(255,255,255),T(i),T(i),2)
        ptext.draw(settings.gamename, center = pview.center,fontname = 'space Xrebron',fontsize = T(90), shadow=(1,1))
        ptext.draw('Click to continue',center = T(900,600), fontname = "RobotoCondensed-Bold", fontsize = T(30), owidth = 1)
        ptext.draw('F10: change resolution\nF11: toggle fullscreen', bottomleft = T(40,680), fontname = "RobotoCondensed-Bold", fontsize = T(26), owidth = 1)

