import pygame
import sys
from config import *
from levelMap import setupLevelMap, renderLevelMap, increaseLevelMap, getLevelMapLength, assignTileByIndex
from tileMap import setupTileMap, renderTileMap, convertTileMap2Tiles
from sprites import getSprites, renderSprites, newSprite
from port import newExportData, export, importLevel, promptImport
from Button import Button
from Camera import Camera
from util import printScreen

class TileType:
    TILES = 0
    INTERACTABLE_TILE = 1
    ENEMY = 2
    PLAYER = 3

currentTile = TileType.TILES

# tile variables
levelMap = setupLevelMap()
tilemapImage = pygame.image.load("assets/tilemap.png")
TILE_COUNT = int((tilemapImage.get_width() / TILEMAP_TILE_SIZE) * (tilemapImage.get_height() / TILEMAP_TILE_SIZE))
tiles = convertTileMap2Tiles(tilemapImage, TILEMAP_TILE_SIZE, SELECTION_AREA_TILE_SIZE)
tilemap = setupTileMap(tiles)
selectedTile = -1
selectedTileImage = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()

# interactable tile variables
interactabletilemapImage = pygame.image.load("assets/interactableTilemap.png")
INTERACTABLE_TILE_COUNT = int((interactabletilemapImage.get_width() / TILEMAP_TILE_SIZE) * (interactabletilemapImage.get_height() / TILEMAP_TILE_SIZE))
interactableTiles = convertTileMap2Tiles(interactabletilemapImage, TILEMAP_TILE_SIZE, SELECTION_AREA_TILE_SIZE)
interactableTilesTilemap = setupTileMap(interactableTiles)
selectedInteractableTile = -1
selectedInteractableTileImage = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
interactableTilesArray = []

# enemy variables
enemySprites = getSprites(ENEMY_DIR)
enemyTilemap = setupTileMap(enemySprites)
selectedEnemy = -1
selectedEnemyImage = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
enemyArray = []

# player variables
playerSprites = getSprites(PLAYER_DIR)
playerTilemap = setupTileMap(playerSprites)
selectedPlayer = -1
selectedPlayerImage = pygame.Surface([TILE_SIZE, TILE_SIZE], pygame.SRCALPHA).convert_alpha()
playerArray = []

MAIN_WINDOW_RECT = pygame.Rect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT)

showGrid = True

# fonts
FONT = pygame.font.SysFont('Arial', 28)

# buttons to swap between tilemap, player and enemies sheets
tilemapButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (0 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), SELECTION_AREA_PADDING_TOP), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "tiles")
interactableTilemapButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (1 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), SELECTION_AREA_PADDING_TOP), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "int")
enemyButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (2 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), SELECTION_AREA_PADDING_TOP), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "enemies")
playerButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (3 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), SELECTION_AREA_PADDING_TOP), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "player")

# import / export buttons
importButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (0 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), WINDOW_HEIGHT - SELECTION_AREA_PADDING_TOP - BUTTON_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "Import")
exportButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (1 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), WINDOW_HEIGHT - SELECTION_AREA_PADDING_TOP - BUTTON_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "Export")

# print screen button
printScreenButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (2 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), WINDOW_HEIGHT - SELECTION_AREA_PADDING_TOP - BUTTON_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "Print")

# button to increase level size
increaseLevelMapButton = Button((WINDOW_WIDTH + SELECTION_AREA_PADDING_LEFT + (3 * (BUTTON_MARGIN_LEFT + BUTTON_WIDTH)), WINDOW_HEIGHT - SELECTION_AREA_PADDING_TOP - BUTTON_HEIGHT), BUTTON_WIDTH, BUTTON_HEIGHT, FONT, "+")

def main():
    global levelMap
    global selectedTile, selectedTileImage, tiles, TILE_COUNT, currentTile
    global enemyTilemap, enemySprites, selectedEnemy, enemyArray
    global selectedPlayer, playerSprites, playerArray
    global selectedInteractableTile, interactableTiles, interactableTilesTilemap, interactableTilesArray

    pygame.init() # setup pygame

    # settings the title for the window
    PROGRAM_ICON = pygame.image.load("assets/icon.png")

    # settings the icon and title for the window
    pygame.display.set_icon(PROGRAM_ICON)
    pygame.display.set_caption(WINDOW_TITLE)

    # creating the window and clock
    screen = pygame.display.set_mode((WINDOW_WIDTH + SELECTION_AREA_WIDTH, WINDOW_HEIGHT)) # create the window
    clock = pygame.time.Clock()     # create clock for syncing FPS
    camera = Camera(getLevelMapLength(levelMap))

    leftMouseDown = False
    rightMouseDown = False

    while True:
        velocityX = 0

        leftClick = False
        mousePos = pygame.mouse.get_pos()

        # see if user is hovering over level map
        insideSandbox = MAIN_WINDOW_RECT.collidepoint(mousePos)
        
        clock.tick(FPS) # makes loop run at same speed every time

        events = pygame.event.get()

        # check for user input
        for event in events:
            if event.type == pygame.QUIT:   # user closed the window
                pygame.quit() # close the window
                sys.exit(0) # close the program
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                leftMouseDown = True
                leftClick = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                leftMouseDown = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                rightMouseDown = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                rightMouseDown = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    global showGrid
                    showGrid = not showGrid
            # user has clicked onto or off of application
            elif event.type == pygame.WINDOWFOCUSLOST or event.type == pygame.WINDOWFOCUSGAINED:
                leftClick = False
                leftMouseDown = False
                rightMouseDown = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            velocityX = -1
        if keys[pygame.K_RIGHT]:
            velocityX = 1

        camera.scroll(velocityX)

        # check for events from user
        if leftClick:

            # updates
            tilemapButton.update(leftClick, mousePos)
            interactableTilemapButton.update(leftClick, mousePos)
            enemyButton.update(leftClick, mousePos)
            playerButton.update(leftClick, mousePos)
            increaseLevelMapButton.update(leftClick, mousePos)
            importButton.update(leftClick, mousePos)
            exportButton.update(leftClick, mousePos)
            printScreenButton.update(leftClick, mousePos)

            # check for selected tile
            if currentTile == TileType.TILES:
                for i, tile in enumerate(tilemap):
                    if tile.collidepoint(mousePos):

                        # stop user selecting non tiles
                        if i >= TILE_COUNT:
                            break

                        selectedTile = i
                        selectedTileImage.fill(EMPTY) # clear old image
                        selectedTileImage.blit(tiles[i], (0,0)) # render new selected tile
            
            # check for selected tile
            if currentTile == TileType.INTERACTABLE_TILE:
                for i, tile in enumerate(interactableTilesTilemap):
                    if tile.collidepoint(mousePos):
                        selectedInteractableTile = i
                        selectedInteractableTileImage.fill(EMPTY) # clear old image
                        selectedInteractableTileImage.blit(interactableTiles[i], (0,0)) # render new selected tile
                
            # check for selected tile
            if currentTile == TileType.PLAYER:
                for i, player in enumerate(playerTilemap):
                    if player.collidepoint(mousePos):
                        selectedPlayer = i
                        selectedPlayerImage.fill(EMPTY) # clear old image
                        selectedPlayerImage.blit(playerSprites[i], (0,0)) # render new selected tile
            
            # check for selected tile
            if currentTile == TileType.ENEMY:
                for i, enemy in enumerate(enemyTilemap):
                    if enemy.collidepoint(mousePos):
                        selectedEnemy = i
                        selectedEnemyImage.fill(EMPTY) # clear old image
                        selectedEnemyImage.blit(enemySprites[i], (0,0)) # render new selected tile
            
            # button events
            if any([tilemapButton.isClicked, enemyButton.isClicked, playerButton.isClicked, interactableTilemapButton.isClicked]):
                selectedTile = -1
                selectedInteractableTile = -1
                selectedEnemy = -1
                selectedPlayer = -1

                if tilemapButton.isClicked:
                    currentTile = TileType.TILES
                elif interactableTilemapButton.isClicked:
                    currentTile = TileType.INTERACTABLE_TILE
                elif enemyButton.isClicked:
                    currentTile = TileType.ENEMY
                elif playerButton.isClicked:
                    currentTile = TileType.PLAYER
            
            elif increaseLevelMapButton.isClicked:
                levelMap = increaseLevelMap(levelMap, 5)
                camera.updateLevelMapLength(getLevelMapLength(levelMap))
                camera.setPos(camera.MAX_X)
            
            elif exportButton.isClicked:
                leftClick = False
                leftMouseDown = False
                rightMouseDown = False
                export(newExportData(levelMap, playerArray, enemyArray, interactableTilesArray))
            
            elif importButton.isClicked:
                leftClick = False
                leftMouseDown = False
                rightMouseDown = False
                levelMap, playerArray, enemyArray, interactableTilesArray = promptImport(levelMap, playerArray, enemyArray, interactableTilesArray)
                levelMap = assignTileByIndex(tiles, levelMap)
                camera.updateLevelMapLength(getLevelMapLength(levelMap))
                camera.setPos(camera.MIN_X)
            
            elif printScreenButton.isClicked:
                printScreen(levelMap, playerArray, playerSprites, enemyArray, enemySprites, interactableTiles, interactableTilesArray, camera.offsetX)

        if leftMouseDown and insideSandbox:

            # remove entity at clicked tile
            for row in levelMap:
                for tile in row:
                    rect = tile.get("rect")
                    if rect.collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                        # remove tile
                        tile["tile"] = None # remove tile that is there
                        tile["tileIndex"] = -1

                        # remove enemy at that tile
                        for i, enemy in enumerate(enemyArray):
                            if enemy.get('rect').colliderect(rect):
                                enemyArray.pop(i)
                            
                        # remove player at that tile
                        for i, player in enumerate(playerArray):
                            if player.get('rect').colliderect(rect):
                                playerArray.pop(i)

                        # remove interactable tile at that tile
                        for i, tile in enumerate(interactableTilesArray):
                            if tile.get('rect').colliderect(rect):
                                interactableTilesArray.pop(i)
            
            # place entity
            for row in levelMap:
                for tile in row:
                    rect = tile.get("rect")
                    if rect.collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                        # place tile
                        if currentTile == TileType.TILES and selectedTile != -1:
                            tile["tileIndex"] = selectedTile
                            tile["tile"] = pygame.transform.scale(tiles[selectedTile], (TILE_SIZE, TILE_SIZE))

                        # placing interactable tile
                        if currentTile == TileType.INTERACTABLE_TILE and selectedInteractableTile != -1:
                            interactableTilesArray.append(newSprite(rect, selectedInteractableTile))
            
                        # placing enemy
                        if currentTile == TileType.ENEMY and selectedEnemy != -1:
                            enemyArray.append(newSprite(rect, selectedEnemy))
            
                        # placing player
                        if currentTile == TileType.PLAYER and selectedPlayer != -1:
                            # remove current player
                            for i, player in enumerate(playerArray):
                                playerArray.pop(i)
                            
                            # place new player
                            playerArray.append(newSprite(rect, selectedPlayer))
        
        if rightMouseDown:
            # check for tile removal
            for row in levelMap:
                for tile in row:
                    rect = tile.get("rect")
                    if rect.collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                        tile["tile"] = None
                        tile["tileIndex"] = -1
            
            # check for enemy removal
            for i, enemy in enumerate(enemyArray):
                if enemy.get('rect').collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                    enemyArray.pop(i)
            
            # check for player removal
            for i, player in enumerate(playerArray):
                if player.get('rect').collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                    playerArray.pop(i)

            # remove interactable tile at that tile
            for i, tile in enumerate(interactableTilesArray):
                if tile.get('rect').collidepoint((mousePos[0] + camera.offsetX, mousePos[1])):
                    interactableTilesArray.pop(i)

        # render
        # buffer - renders over previous frame to clear the screen
        screen.fill((0,0,0))
        screen.fill((MAIN_BG_COLOR))

        # display level map
        renderLevelMap(screen, levelMap, camera.offsetX, showGrid)
        renderSprites(screen, enemySprites, enemyArray, camera.offsetX)
        renderSprites(screen, playerSprites, playerArray, camera.offsetX)
        renderSprites(screen, interactableTiles, interactableTilesArray, camera.offsetX)

        # display section area
        # background
        screen.fill(SELECTION_AREA_BGC, (WINDOW_WIDTH, 0, SELECTION_AREA_WIDTH, screen.get_height()))

        # buttons
        tilemapButton.render(screen)
        interactableTilemapButton.render(screen)
        enemyButton.render(screen)
        playerButton.render(screen)
        increaseLevelMapButton.render(screen)
        importButton.render(screen)
        exportButton.render(screen)
        printScreenButton.render(screen)

        # current tile type selected
        if currentTile == TileType.TILES:
            # render current tile
            if selectedTile != -1 and insideSandbox:
                screen.blit(selectedTileImage, (mousePos[0] - TILEMAP_TILE_SIZE, mousePos[1] - TILEMAP_TILE_SIZE))
            # draw tile map
            renderTileMap(screen, tiles, tilemap, selectedTile)
        
        # current tile type selected
        elif currentTile == TileType.INTERACTABLE_TILE:
            # render current tile
            if selectedInteractableTile != -1 and insideSandbox:
                screen.blit(selectedInteractableTileImage, (mousePos[0] - TILEMAP_TILE_SIZE, mousePos[1] - TILEMAP_TILE_SIZE))
            # draw tile map
            renderTileMap(screen, interactableTiles, interactableTilesTilemap, selectedInteractableTile)

        elif currentTile == TileType.PLAYER:
            # render current tile
            if selectedPlayer != -1 and insideSandbox:
                screen.blit(selectedPlayerImage, (mousePos[0] - TILEMAP_TILE_SIZE, mousePos[1] - TILEMAP_TILE_SIZE))
            # draw tile map
            renderTileMap(screen, playerSprites, playerTilemap, selectedPlayer)
        else:
            # render current tile
            if selectedEnemy != -1 and insideSandbox:
                screen.blit(selectedEnemyImage, (mousePos[0] - TILEMAP_TILE_SIZE, mousePos[1] - TILEMAP_TILE_SIZE))
            # draw tile map
            renderTileMap(screen, enemySprites, enemyTilemap, selectedEnemy)

        # update the window (render everything)
        pygame.display.update()

if __name__ == "__main__":
    main()
