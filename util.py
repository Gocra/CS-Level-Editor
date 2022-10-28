import pygame
from os import walk
import json
import ast
from config import MAIN_BG_COLOR, TILE_SIZE, WINDOW_HEIGHT, WINDOW_WIDTH
import tkinter.filedialog

def getFilenamesInFolder(dir):
    filenames = next(walk(dir), (None, None, []))[2]  # [] if no file
    return filenames

def clamp(l, v, u):
    return l if l >= v else u if u <= v else v

def drawText(screen, text, font, pos, color = (255,255,255)):
    textSurface = font.render(text, True, color)
    screen.blit(textSurface, dest=pos)

def getJSONFromFile(filename):
    contents = get_file_contents(filename)
    try:
        data = json.loads(contents)
        return data
    except:
        raise Exception("Invalid JSON Format")
    
def get_file_contents(filename):
    try:
        file = open(filename)
        contents = file.read()
        return contents
    except:
        raise Exception("Failed to open file")

def convertFromStringImportData(levelMap, playerArray, enemyArray, interactableTilesArray):
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            levelMap[y][x]['rect'] = convertDictToPygameRect(ast.literal_eval(levelMap[y][x]['rect']))
    
    for i in range(len(playerArray)):
        playerArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(playerArray[i]['rect']))

    for i in range(len(enemyArray)):
        enemyArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(enemyArray[i]['rect']))

    for i in range(len(interactableTilesArray)):
        interactableTilesArray[i]['rect'] = convertDictToPygameRect(ast.literal_eval(interactableTilesArray[i]['rect']))
    
    return levelMap, playerArray, enemyArray, interactableTilesArray

def convertDictToPygameRect(rect):
    return pygame.Rect(rect.get("x"), rect.get("y"), rect.get("w"), rect.get("h"))

def printScreen(levelMap, playerArray, playerSpriteArray, enemyArray, enemySpriteArray, interactableTiles, interactableTilesArray, offsetX):
    # create image
    image = pygame.Surface([WINDOW_WIDTH, WINDOW_HEIGHT], pygame.SRCALPHA).convert_alpha()
    # add background to image
    image.fill(MAIN_BG_COLOR)

    # copy level map on to image
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            if tile['tile'] != None:
                image.blit(tile['tile'], ((x * TILE_SIZE) - offsetX, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # copy player on to image
    for i in range(len(playerArray)):
        rect = playerArray[i]['rect']
        image.blit(playerSpriteArray[playerArray[i]['type']], (rect.x - offsetX, rect.y, rect.w, rect.h))
    
    # copy enemies on to image
    for i in range(len(enemyArray)):
        rect = enemyArray[i]['rect']
        image.blit(enemySpriteArray[enemyArray[i]['type']], (rect.x - offsetX, rect.y, rect.w, rect.h))

    # copy interactable tiles on to image
    for i in range(len(interactableTilesArray)):
        rect = interactableTilesArray[i]['rect']
        image.blit(interactableTiles[interactableTilesArray[i]['type']], (rect.x - offsetX, rect.y, rect.w, rect.h))
    
    # get save location
    filepath = tkinter.filedialog.asksaveasfilename(
        defaultextension='.png', filetypes=[("PNG", '*.png')],
        title="Save Image As"
    )
    try:
        pygame.image.save(image, filepath)
    except:
        pass

    