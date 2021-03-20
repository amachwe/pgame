import numpy as np
import entity

V = None
def prop_sel(arr):
    select = np.random.uniform(0,1)
    sum = np.sum(arr)
    arr = np.array(arr)/sum
    total = 0
    print(arr, select)
    for idx, i in enumerate(arr):
        if select < total:
            print(idx-1)
            return idx-1
        total = i + total
    return len(arr)-1
    

def inform(me, players, matrix, grid):
    
    state = entity.extract_state(me, players, grid, matrix)
    real_state = (state[0], state[2], state[5])
    health = state[0]
    food = int(state[1]>0)
    cell_state = state[2]
    dragon = state[5]
    arr = []
    acts = []
    # attack
    v_attack = V.get((health, food, cell_state, dragon-1))
    if v_attack:
        arr.append(v_attack)
        acts.append(["attack"])

    #food
    v_food = V.get((health, food, cell_state+1, dragon))

    if v_food:
        arr.append(v_food)
        acts.append(["grow"])

    #health
    v_health = V.get((health+1, food, cell_state, dragon))

    if v_health:
        arr.append(v_health)
        acts.append(["search", "rest"])
     
 
    if arr:
        min = np.min(arr)
    else:
        min = 0
    for an in entity.action_names:
        if an not in acts:
            if min == 0:
                arr.append(1/len(entity.action_names))
            else:
                arr.append(min/2)
            acts.append([an])
    


    

    ca = acts[prop_sel(arr)]
    print(ca)
    return ca
    




    acts = entity.action_names[np.random.randint(0, len(entity.action_names))]

    return [acts]


def state(doc):
    #return (doc["new_state_health"], doc["new_state_food"], doc["new_x"], doc["new_y"], doc["new_state"], doc["new_type"], doc["new_dragon_health"])
    #return (doc["new_state_health"], doc["new_x"], doc["new_y"], doc["new_state"], doc["new_type"], doc["new_dragon_health"])
    return (doc["new_state_health"] , int(doc["new_state_food"]>0),doc["new_state"], doc["new_dragon_health"])


if __name__ == "__main__" or V==None:

    import pymongo
    from matplotlib import pyplot as plt

    mc = pymongo.MongoClient().get_database("drl").get_collection("games")

    games = [game_id["_id"]
             for game_id in mc.aggregate([{"$group": {"_id": "$game_id"}}])]
    V = {}
    Vs0 = {}
    s0_ = None
    gamma = 0.98
    alpha = 0.01
    for p in [1,2]:
        for g in games:

            player_moves = [move for move in mc.find(
                {"game_id": g, "player_id": p}).sort("time", direction=pymongo.ASCENDING)]

            steps = [state(p) for p in player_moves]

            s0 = steps.pop()
            
            while len(steps) > 1:
                G = 0
                if not V.get(s0):
                    V[s0] = 0
                for idx, s in enumerate(steps):

                    G = G + pow(gamma, idx)*((s[0]/10)+s[1])

                V[s0] = V[s0] + (alpha*(G-V[s0]))
                l = Vs0.get(s0,[])
                l.append(V[s0])
                Vs0[s0] = l

                #print(g, " - ", len(player_moves), " Vs0:", V[s0])
                s0 = steps.pop()

        
            print()
    print(len(V))
    o =sorted(Vs0.items(), key=lambda x:len(x[1]))
    if o:
        print(len(o))
        plt.plot(o[-1][1])
        plt.plot(o[-2][1])
        plt.plot(o[-3][1])
        plt.show()
