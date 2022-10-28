import pygame
from config import *

def getLevelMapLength(levelMap):
    return levelMap[0][-1].get('rect').right

def emptyTile(x, y):
    return({
        "tile": None,
        "rect": pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE),
        "tileIndex" : -1
    })

def setupLevelMap():
    # setup 2d array of empty tiles that span the whole screen
    levelMap = [[emptyTile(x, y) for x in range(int(WINDOW_WIDTH / TILE_SIZE))] for y in range(int(WINDOW_HEIGHT / TILE_SIZE))]
    return levelMap

def renderLevelMap(screen, levelMap, offsetX, showGrid):

    for row in levelMap:
        for tile in row:

            rect = tile.get("rect")
            tile = tile.get("tile")

            # render tile
            if tile != None:
                screen.blit(tile, (rect.x - offsetX, rect.y, rect.w, rect.h))

            # outline tile
            if showGrid:
                pygame.draw.rect(screen, (255, 255, 255), (rect.x - offsetX, rect.y, rect.w, rect.h), 1)

def increaseLevelMap(levelMap, amount):
    end = levelMap[0][-1].get('rect').right / TILE_SIZE
    
    for y, row in enumerate(levelMap):
        for x in range(amount):
            row.append(emptyTile(x + end, y))

    return levelMap

def assignTileByIndex(tiles, levelMap):
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            if tile['tileIndex'] != -1:
                levelMap[y][x]['tile'] = tiles[levelMap[y][x]['tileIndex']]
    
    return levelMap