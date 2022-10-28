import pygame
from util import drawText

class Button:
    def __init__(self, pos, width, height, font, text):
        self.rect = pygame.Rect(pos, (width, height))
        self.text = text
        self.font = font

        # text position
        textWidth, textHeight = self.font.size(self.text)
        self.textPos = pygame.Vector2(
            self.rect.x + ((self.rect.w - textWidth) / 2),
            self.rect.y + ((self.rect.h - textHeight) / 2)
        )

        self.isClicked = False

    def render(self, screen):
        # render button
        pygame.draw.rect(screen, (255, 0, 0), self.rect)
        
        # draw text
        drawText(screen, self.text, self.font, self.textPos, (255,255,255))
    
    def update(self, leftClick, mousePos):
        self.isClicked = False

        if self.rect.collidepoint(mousePos):
            if leftClick:
                self.isClicked = True