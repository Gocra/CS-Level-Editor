import pygame
from config import *
from util import getFilenamesInFolder

def getSprites(directory):

    spritesFileNames = getFilenamesInFolder(directory)

    filenames = []
    for filename in spritesFileNames:
        filenames.append(int(filename.split(".")[0]))
    filenames.sort()

    sprites = []

    for filename in filenames:
        # render sprite onto surface
        spritesheet = pygame.image.load(f"{directory}/{filename}.png")
        sprite = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
        sprite.blit(spritesheet, (0,0), (IDLE_ANIM[0] * TILE_SIZE, IDLE_ANIM[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        sprites.append(sprite)

    return sprites

def renderSprites(screen, sprites, spriteArray, offsetX):
    for sprite in spriteArray:
        rect = sprite.get('rect')
        screen.blit(sprites[sprite.get('type')], (rect.x - offsetX, rect.y, rect.w, rect.h))

def newSprite(rect, selectedSprite):
    return ({
        'rect' : rect,
        'type' : selectedSprite
    })