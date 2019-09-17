import pygame

class TextClass:
    def __init__(self, font_name = None, font_size = 12):
        pygame.font.init()
        self.fontObject = pygame.font.Font(font_name, font_size)

    def render_text(self, text = "", color = (0,0,0), pos = (0,0)):
        text_surf = self.fontObject.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.x, text_rect.y = pos
        return text_surf, text_rect
