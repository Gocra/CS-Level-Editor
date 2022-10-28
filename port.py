import tkinter.filedialog
import json
from config import TILE_SIZE
from levelMap import emptyTile
from sprites import newSprite
from util import getJSONFromFile, convertFromStringImportData

# rect that can is formatted in a way that can be JSON serialized
class serializableRect():
    def __init__(self, rect):
        self.x = rect.x
        self.y = rect.y
        self.w = rect.w
        self.h = rect.h
    
    # serialize the rect data to JSON
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

def newExportData(levelMap, playerArray, enemyArray, interactableTilesArray):
    # create empty copies of required data
    newLevelMap = [
        [emptyTile(x, y) for x in range(int(levelMap[0][-1].get('rect').right / TILE_SIZE))]
        for y in range(int(levelMap[-1][-1].get('rect').bottom / TILE_SIZE))]
    newPlayerArray = [newSprite(None, playerArray[i].get("type")) for i in range(len(playerArray))]
    newEnemyArray = [newSprite(None, enemyArray[i].get("type")) for i in range(len(enemyArray))]
    newInteractableTilesArray = [newSprite(None, interactableTilesArray[i].get("type")) for i in range(len(interactableTilesArray))]

    # add only necessary data to copies
    # prevents changing data in original variable
    for y, row in enumerate(levelMap):
        for x, tile in enumerate(row):
            newLevelMap[y][x]['tileIndex'] = tile.get('tileIndex')
            newLevelMap[y][x]['rect'] = serializableRect(tile.get('rect')).toJSON()
    
    for i in range(len(newPlayerArray)):
        newPlayerArray[i]['rect'] = serializableRect(playerArray[i].get('rect')).toJSON()

    for i in range(len(newEnemyArray)):
        newEnemyArray[i]['rect'] = serializableRect(enemyArray[i].get('rect')).toJSON()
    
    for i in range(len(newInteractableTilesArray)):
        newInteractableTilesArray[i]['rect'] = serializableRect(interactableTilesArray[i].get('rect')).toJSON()

    # return the new data
    return {
        "levelMap" : newLevelMap,
        "playerArray" : newPlayerArray,
        "enemyArray" : newEnemyArray,
        "interactableTilesArray" : newInteractableTilesArray
    }

def export(data):
    filepath = tkinter.filedialog.asksaveasfilename(
        defaultextension='.json', filetypes=[("JSON", '*.json')],
        title="Save Level Data"
    )
    try:
        with open(filepath, 'w') as f:
            f.write(json.dumps(data))
    except:
        pass

def importLevel(filename):
    JSONData = getJSONFromFile(filename)
    return JSONData.get('levelMap', []), JSONData.get('playerArray', []), JSONData.get('enemyArray', []), JSONData.get('interactableTilesArray', [])

def promptImport(levelMap, playerArray, enemyArray, interactableTilesArray):
    filename = tkinter.filedialog.askopenfilename(
        title='Open a file',
        filetypes=[("JSON", '*.json')]
    )

    """
    lm levelMap
    pa playerArray
    ea enemyArray
    ita interactableTilesArray
    """

    try:
        lm, pa, ea, ita = importLevel(filename)
        lm, pa, ea, ita = convertFromStringImportData(lm, pa, ea, ita)
        return lm, pa, ea, ita
    except:
        return levelMap, playerArray, enemyArray, interactableTilesArray