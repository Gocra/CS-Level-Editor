import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from util import clamp

class Camera:
    def __init__(self, levelMapLength):
        self.offsetX = 0
        self.levelMapLength = levelMapLength

        # constraints
        self.MIN_X = 0
        self.MAX_X = self.levelMapLength - WINDOW_WIDTH
        self.speed = 4
    
    def scroll(self, velocityX):
        # get camera offset from players position
        self.offsetX = (self.offsetX + velocityX * self.speed)

        # clamp offset
        if self.levelMapLength > WINDOW_WIDTH: # cannot scroll right
            # singularly increment offset - prevent screen shaking
            for i in range(self.speed):
                self.offsetX = self.offsetX + velocityX
                if self.offsetX >= self.MAX_X:
                    self.offsetX = self.MAX_X
                else:
                    self.offsetX = clamp(self.MIN_X, self.offsetX, self.MAX_X)
        else:
            self.offsetX = self.MIN_X
    
    def updateLevelMapLength(self, length):
        self.levelMapLength = length
        self.MAX_X = self.levelMapLength - WINDOW_WIDTH
    
    def setPos(self, pos):
        self.offsetX = clamp(self.MIN_X, pos, self.MAX_X)