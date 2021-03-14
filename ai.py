import math
import operator
import numpy as np


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
                #print("Found: ", p["id"])
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

def act(me, matrix, closest, p_attack=0.5):
    #move towards closest
    moved = False
    if closest:

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
            
            p_attack = 0.5 # 1 - (me["health"]/11)

            if attack(p_attack):
                closest["health"] = closest["health"] - 1

def attack(p_attack, loc=0.5):
    return np.random.normal(loc) < p_attack


if __name__ == "__main__":

    p = 0.0
    MAX_YES = 0
    MIN_YES = 1000
    PL = None
    PLM = None
    while p < 1:
        l = 0.0
        while l<1:
            yes = 0
            
            for k in range(0,100):
                if attack(p):
                    yes += 1
                
            print(round(p,2), round(l,2), "  Y:",yes,"   N:",100-yes)
            if MAX_YES < yes:
                MAX_YES = yes
                PL = (p,l)
            if MIN_YES > yes:
                MIN_YES = yes
                PLM = (p,l)
            l = l+0.1
        p = p+0.1

    print(MAX_YES, PL)
    print(MIN_YES, PLM)

                
            
            

