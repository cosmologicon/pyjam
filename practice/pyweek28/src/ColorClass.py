
class ColorClass:
    def __init__(self):
        self.BLACK = (  0,  0,  0)
        self.WHITE = (255,255,255)
        self.BROWN = (200,113, 55)
        self.GREY = (150,150,150)
        self.GREEN = (  0,255,  0)
        self.BLUE = (  0,  0,255)
        self.RED = (255,  0,  0)
        self.YELLOW = (255,255,  0)
        self.PURPLE = (255,  0,255)
        self.CYAN = (  0,255,255)
        self.VIOLET = (136,  0,255)
        self.ORANGE = (255,136,  0)

        self.DARKBROWN = (160, 90, 44)
        self.LIGHTBROWN = (211,141, 95)
        self.LIGHTGREY = (100,100,100)
        self.DARKGREY = (200,200,200)
        self.LIGHTRED = (255,128,120)
        self.DARKRED = (170,0  ,0  )
        self.LIGHTGREEN = (100,200,128)
        self.DARKGREEN = (0  ,128,50 )
        self.LIGHTBLUE = ( 85,255,150)
        self.DARKBLUE = (0  , 60,170)
        self.LIGHTGREY = (100,100,100)
        self.DARKGREY = (200,200,200)
        self.DARKYELLOW = (200,200,  0)
        self.LIGHTYELLOW = (255,255,150)

    def set_alpha(self, colorRBG, alphaVal = 0):
        '''
        sets alpha value for color 
        '''
        color_list = list(colorRBG)
        color_list.append(alphaVal)
        colorRBGA = tuple(color_list)
        return colorRBGA
