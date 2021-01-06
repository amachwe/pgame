
import pygame
# colors
darkgreen = pygame.colordict.THECOLORS["chartreuse4"]
darkbrown = pygame.colordict.THECOLORS["saddlebrown"]
black = pygame.colordict.THECOLORS["black"]
white = pygame.colordict.THECOLORS["white"]
sand = pygame.colordict.THECOLORS["darkgoldenrod1"]

#images
kn = pygame.transform.scale(pygame.image.load("kn.jpg"), (14,14))
dr = pygame.transform.scale(pygame.image.load("dr.png"), (14,14))

MAX_FOOD = 10
MAX_HEALTH = 10

def get_cell_from_matrix(entity, matrix, grid):
    mtx = matrix[entity["x"]][entity["y"]]
    return grid[mtx[0]][mtx[1]]

def get_cell_state(entity,matrix, grid):
    return get_cell_from_matrix(entity, matrix, grid).get("state", 0)

def get_cell_data(entity,matrix, grid):
    data = get_cell_from_matrix(entity, matrix, grid)

    return (data.get("state", 0), data.get("type", ""))

class Behavior(object):

    @staticmethod
    def look(entity, grid, matrix):
        cell = get_cell_from_matrix(entity, matrix, grid)
        print(cell)

    @staticmethod
    def rest(entity):

        
        if entity["food"] > 0 and entity["health"] < MAX_HEALTH:
            entity["health"] = entity["health"] + 1      
    
    @staticmethod
    def moved(entity):
        
        if entity["food"] > 0:
            entity["food"] = entity["food"] - 1
        elif entity["health"] > 0:
            entity["health"] = entity["health"] - 1


    @staticmethod
    def search(entity, grid, matrix):
        
        cell = get_cell_from_matrix(entity, matrix, grid)

        if cell["type"] == "grass" and cell["state"] > 0:
            entity["food"] = entity["food"] + 2
            Behavior.degrade(cell)

    @staticmethod
    def farm(entity, grid, matrix):

        cell = get_cell_from_matrix(entity, matrix, grid)
        
        if cell["type"] == "grass" and cell["state"] <= cell["max_state"]:
            cell["state"] = cell["state"] + 2
            if cell["state"] >= cell["max_state"]:
                cell["color"] = darkgreen

    @staticmethod
    def degrade(cell):
        
        if cell["type"] == "grass":
            cell["state"] = cell["state"] - 2
            if cell["state"] <= 0:
                cell["color"] = sand
def turn(pos_, player, players, matrix):
  

    _x, _y = move(matrix, player["x"], player["y"], pos_)
    for p in players:
      
        if p["id"] != player["id"] and p["x"] == _x and p["y"] == _y:
            # Blocked
            
            return False
    player["x"] = _x
    player["y"] = _y
    return True

def move(matrix, x,y, slot):
    _x = x
    _y = y
    if slot == 1:
        _y = y-1
        
    # elif slot == 2:
    #     _x = x-1
    #     _y = y-1
    elif slot == 3:
        _x = x+1
    # elif slot == 4:
    #     _x = x+1
    #     _y = y+1
    elif slot == 5:
        _y = y+1
    # elif slot == 6:
    #     _y = y-1
    #     _x = x+1
    elif slot == 7:
        _x = x-1
    # elif slot == 8:
    #     _y = y-1
    #     _x= x-1


    return _x,_y


#entity
knight1 = {
    "id": 1,
    "name": "Knight",
    "x": 10,
    "y": 10,
    "image": kn,
    "player":True,
    "food": MAX_FOOD,
    "health": MAX_HEALTH,
    "moves": 0,
    "total_steps": 0
}

knight2 = {
    "id": 2,
    "name": "Knight",
    "x": 12,
    "y": 12,
    "image": kn,
    "player":True,
    "food": MAX_FOOD,
    "health": MAX_HEALTH,
    "moves": 0,
    "total_steps": 0
}

dragon = {
    "id":3,
    "name": "Dragon",
    "x": 20,
    "y": 20,
    "image": dr,
    "player": False,
    "food": MAX_FOOD,
    "health": MAX_HEALTH
}

hill = {
        "color": pygame.color.THECOLORS["chocolate4"], 
        "filled": 0,
        "type": "hill"
    }

grass = {
        "color": pygame.color.THECOLORS["chartreuse4"], 
        "filled": 0,
        "type": "grass",
        "state": 10,
        "max_state": 10

    }

water = {
        "color": pygame.color.THECOLORS["blue"], 
        "filled": 0,
        "type": "water",
        "state": 10,
        "max_state": 10
    }