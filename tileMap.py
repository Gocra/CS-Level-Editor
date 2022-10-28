import pygame
from config import *
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH + SELECTION_AREA_WIDTH, WINDOW_HEIGHT))

def setupTileMap(tiles):
    tilemap = []
    
    for i in range(len(tiles)):
        x = i
        while x >= SELECTION_AREA_TILES_PER_ROW:
            x -= SELECTION_AREA_TILES_PER_ROW
        row = int(i / SELECTION_AREA_TILES_PER_ROW)
        left = x * (SELECTION_AREA_GRID_GAP + SELECTION_AREA_TILE_SIZE)
        top = (2 * SELECTION_AREA_PADDING_TOP) + BUTTON_HEIGHT + (SELECTION_AREA_TILE_SIZE + SELECTION_AREA_GRID_GAP) * row
        tilemap.append(pygame.Rect(SELECTION_AREA_TOP_LEFT + left, top, SELECTION_AREA_TILE_SIZE, SELECTION_AREA_TILE_SIZE))
    
    return tilemap

def renderTileMap(screen, tiles, tilemap, selectedTile = -1):
    for i, tile in enumerate(tilemap):
        screen.blit(tiles[i], tile)

        # outline selected tile
        if selectedTile == i:
            pygame.draw.rect(screen, (255, 0, 0), tile, 3)

def convertTileMap2Tiles(tilemap, tileSize, TILE_SIZE):
    tiles = []
    tilemapWidth, tilemapHeight = tilemap.get_width(), tilemap.get_height()
    
    for y in range(int(tilemapHeight / tileSize)):
        for x in range(int(tilemapWidth / tileSize)):
            tile = pygame.Surface([tileSize, tileSize], pygame.SRCALPHA).convert_alpha()
            tile.blit(tilemap, (0,0), (x * tileSize, y * tileSize, tileSize, tileSize))
            tile = pygame.transform.scale(tile, (TILE_SIZE, TILE_SIZE))
            tiles.append(tile)
    
    return tiles