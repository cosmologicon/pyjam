from __future__ import division
import pygame, math, random
from . import scene, pview, view, ptext, draw, state, worldmap, things, dialog, quest,sound,playscene
from .pview import T

t = 0
point_list =[]


class Title(scene.Scene):
    def __init__(self):
        super(Title,self).__init__()
        sound.playmusic('carnivalrides')


    def think(self,dt, kpressed, kdowns, mpos, mdown, mup):
        if kdowns:
            scene.set(playscene.PlayScene())

    def draw(self):

        draw.atmosphere()
        ptext.draw('The Really Really Big Tower',center = pview.center,fontname = 'space Xrebron',fontsize = T(60))
        ptext.draw('press any key to continue',T(800,500))
        global t
        t += 0.01
        r = 10 * (1 + t)
        if r % 20 >= 10:
            x = r*math.cos(t*360)+pview.center[0]+286
            y = r*math.sin(t*360)+pview.center[1]+4
        else:
            x = r*math.sin(t*360)+pview.center[0]+286
            y = r*math.cos(t*360)+pview.center[1]+4
        point_list.append([x,y])
        if len(point_list) >= 2:
            for i in point_list:
                pygame.draw.line(pview.screen,(255,255,255),i,i,2)
