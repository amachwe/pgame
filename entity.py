import random
action_names = ['down', 'left', 'rest', 'right', 'up', 'search', 'grow','attack']

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

class Transitions(object):
    @staticmethod
    def search(player, grid, matrix):
        Behavior.search(player, grid, matrix)
        Behavior.moved(player)

    @staticmethod
    def rest(player, grid=None, matrix=None):
        Behavior.rest(player)
        Behavior.moved(player)

    @staticmethod
    def grow(player, grid, matrix):
        Behavior.farm(player, grid, matrix)
        Behavior.moved(player)

    @staticmethod
    def move(player, grid=None, matrix=None):
        Behavior.moved(player)

    @staticmethod
    def attack(player, players, grid=None, matrix=None):
        Behavior.attack(player,players)
        Behavior.moved(player)


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
            entity["food"] = entity["food"] + 2 #random.randint(0,3)
            Behavior.degrade(cell)

    @staticmethod
    def farm(entity, grid, matrix):

        cell = get_cell_from_matrix(entity, matrix, grid)
        
        if cell["type"] == "grass" and cell["state"] <= cell["max_state"]:
            cell["state"] = cell["state"] + 2 #random.randint(0,3)
            if cell["state"] >= cell["max_state"]:
                cell["color"] = (69, 139, 0, 255)
    
    @staticmethod
    def attack(entity, entities):
        for e in entities:
            if not e["player"] and e != entity:
                if abs(e["x"]-entity["x"])<=1 and abs(e["y"]-entity["y"])<=1 and e["health"] > 0:
                    e["health"] = e["health"] -1
                    print(e["name"], " attacked by ",entity["id"])


    @staticmethod
    def degrade(cell):
        
        if cell["type"] == "grass":
            cell["state"] = cell["state"] - 2
            if cell["state"] <= 0:
                cell["color"] = (255, 185, 15, 255)
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
    "player":True,
    "food": MAX_FOOD,
    "health": MAX_HEALTH,
    "moves": 0,
    "total_steps": 0,
    "show": True
}

knight2 = {
    "id": 2,
    "name": "Knight",
    "x": 12,
    "y": 12,
    "player":True,
    "food": MAX_FOOD,
    "health": MAX_HEALTH,
    "moves": 0,
    "total_steps": 0,
    "show": True
}

dragon = {
    "id":3,
    "name": "Dragon",
    "x": 15,
    "y": 15,
    "player": False,
    "food": MAX_FOOD,
    "health": MAX_HEALTH + 20,
    "show": True
}

hill = {
        "color": (139, 69, 19, 255), 
        "filled": 0,
        "type": "hill"
    }

grass = {
        "color": (69, 139, 0, 255), 
        "filled": 0,
        "type": "grass",
        "state": 10,
        "max_state": 10

    }

water = {
        "color": (0, 0, 255, 255), 
        "filled": 0,
        "type": "water",
        "state": 10,
        "max_state": 10
    }