import math
import operator
import random


#Memory:
memory = {}
OBSERVE_THRESHOLD = 5
def observe(me, matrix,players):
    x,y = me["x"], me["y"]
    observing = []
    for p in players:
        if p["id"] != me["id"]:
            px, py = p["x"], p["y"]

            d = math.sqrt(math.pow(x-px,2)+math.pow(y-py,2))
            if d < OBSERVE_THRESHOLD:
                print("Found: ", p["id"])
                observing.append((p, d))
    if observing:
        observing.sort(key=operator.itemgetter(1))
        return list(zip(*observing))[0]
    else:
        return observing

def orient(me, matrix, players):
    pass

def decide(me, matrix, players):
    pass

def act(me, matrix, players):
    #move towards closest
    moved = False
    if players:
        closest = players[0]

        xc, yc = closest["x"], closest["y"]

        dx = me["x"] - xc
        dy = me["y"] - yc
        
        if abs(dx) > 1:
            me["x"] = int(me["x"] - (dx/abs(dx)))
            moved = True
        if abs(dy) > 1:
            me["y"] = int(me["y"] - (dy/abs(dy)))
            moved = True

        if not moved:
        # attack
            
            p_attack = 1 - (me["health"]/100)

            if random.random() > p_attack:
                closest["health"] = closest["health"] - random.randint(0,3)
                
            
            

