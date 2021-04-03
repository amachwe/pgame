from os import stat
import numpy as np
import entity

state_tx = None
V = {}
import random
    

def inform(me, players, matrix, grid):
    state = entity.extract_state(me, players,grid, matrix)
    health = state[0]
    food = int(state[1]>0)
    enemy = state[-1]
    cell = state[2]
    explored = 0



    state = (health, food, cell, enemy, state[-2][0],state[-2][1])

    acts = state_tx.get(state, {})
    pop = {k: len(v) for k,v in acts.items()}
    
    # explored = []
    # act_list = []
    # next_state = []

    sel_act = ""
    #sel_act_idx = None
    if len(pop) == len(entity.action_names):
    
        # for a, count in pop.items():
        #     act_list.append(a)
        #     explored.append(count)
        # sel_act_idx = np.argmax(explored)
        # sel_act = act_list[sel_act_idx]
        act_value = []
        act_avg_value = []
        for a,ss in acts.items():
            totalV = 0
            avg_v = 0
            for s in ss:
                totalV += V.get(s,0)
            if ss:
                avg_v = totalV/len(ss)
        
            act_value.append(a)
            act_avg_value.append(avg_v)
        max_val_idx = np.argmax(act_avg_value)
        max_val_act = act_value[max_val_idx]
        print(max_val_act, act_avg_value[max_val_idx])
        # print(sel_act, "   max: ", max_val_act, act_avg_value, act_value)
        # diff = abs(act_avg_value[sel_act_idx]-act_avg_value[max_val_idx])
        # print(diff)
        
        sel_act = max_val_act
        print(">",sel_act)
    else:

        used_acts = set(pop.keys())
        all_acts = set(entity.action_names)

        unused_acts = all_acts - used_acts
        
        sel_act = random.choice(list(unused_acts))
        explored = 1

        print(">>",sel_act)

    # if random.random()<0.05:
    #      sel_act = random.choice(entity.action_names)
    #      print(">>>", sel_act)
    #      explored = 0

    return [sel_act], explored


    


def state(doc):
   
    return (doc["curr_state_health"],int(doc["curr_state_food"]>0),doc["state"],doc["dragon_health"], doc["x"],doc["y"]), \
    doc["action"], \
    (doc["new_state_health"] , int(doc["new_state_food"]>0),doc["new_state"], doc["new_dragon_health"], doc["new_x"],doc["new_y"])


if __name__ == "__main__" or state_tx==None:

    import pymongo
    from matplotlib import pyplot as plt

    mc = pymongo.MongoClient().get_database("drl").get_collection("games")

    games = [game_id["_id"]
             for game_id in mc.aggregate([{"$group": {"_id": "$game_id"}}])]
    print("Games:",len(games))
    # '_id', 'move_id', 'player_id', 'game_id', 'time', 'curr_state_health', 'curr_state_food', 'action', 'x', 'y', 'state', 'type', 'dragon_health', 
    # 'new_state_health', 'new_state_food', 'new_x', 'new_y', 'new_state', 'new_type', 'new_dragon_health', 'AI'
    gamma = 0.8
    alpha = 0.1
    game_len = []
    game_id = []
    state_tx = {}

    ALPHA = 0.1
    GAMMA = 0.98
    
    for g in games:
        game_id.append(str(g))
        game_len.append(mc.count({"game_id": g}))
        for p in [1,2]:

            player_moves = [move for move in mc.find({"game_id": g, "player_id": p}).sort("time", direction=pymongo.ASCENDING)]

            for i in player_moves:
                p,act,n = state(i)
                if n[0] > 10:
                    print(p, n, g,"\n", i,"\n")
                state_tx.setdefault(p,{}).setdefault(act,[]).append(n)

                Vp0 = V.get(p,0)
                Vn0 = V.get(n,0)
                R1 = int(n[0]==10) #+ abs(n[-2]-p[-2])+abs(n[-1]-p[-1])
                V[p] = Vp0 + ALPHA*(R1+(GAMMA*Vn0)-Vp0)

    print(V)
    #print(state_tx)




        


    

        


    
# plt.hist(game_len)
# plt.show()

