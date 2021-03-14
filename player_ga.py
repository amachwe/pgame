
import random
import entity
import math

AI = True


def state_value(s, a, sd, rewards, vs):
    pass
    
    
def extract_state(me, players,grid, matrix):
    health = me["health"]
    food = me["food"]
    state = entity.get_cell_data(me, matrix, grid)
    enemy = list(filter(lambda x: True if x["name"]=="Dragon" else False, players))
    enemy_health = enemy[0]["health"]
    # return health, food, cell state, cell type
    return (health, food, state[0],state[1], (me["x"], me["y"]), enemy_health)


def en_copy(et):
    return {
        "health": et["health"],
        "food": et["food"],
        "x": et["x"],
        "y": et["y"],
        "id": et["id"]
    }

def is_same(et1, et2):
    
    for k in ["health", "food", "x", "y"]:
        if et1[k] != et2[k]:
            return False
    
    return True
        
def reward(curr_state, old_state, xy, old_xy):
    
    #Health, Food, Cell_Food, Movement Enemy Health
    
    return 6*(curr_state[0]-old_state[0])+4*(curr_state[1]-old_state[1])+(curr_state[2]-old_state[2])+((abs(xy[0]-old_xy[0])+abs(xy[1]-old_xy[1])))+6*(old_state[5]-curr_state[5])
    

def transition(me, players, grid, matrix, act):
        
        if act == "search":
            
            entity.Transitions.search(me, grid, matrix)
         
        elif act == "grow":
            
            entity.Transitions.grow(me, grid, matrix)
          
        elif act == "rest":
             
            entity.Transitions.rest(me)
        
        elif act == "attack":
            entity.Transitions.attack(me, players)
            
        else:
            pos = 0
            if act == "up":
                pos = 1
            elif act == "right":
                pos = 3
            elif act == "down":
                pos = 5
            else:
                pos = 7

            entity.turn(pos, me, players, matrix)
            entity.Transitions.move(me)
        
        return (me, grid, players)


def evaluate_sequence(me, players, grid, matrix, seq):
    discount = 1
    total_reward = 0
    old_state = extract_state(me, players, grid, matrix)
    for i, s in enumerate(seq):
        out = transition(me, players, grid, matrix, s)
        me = out[0]
        grid = out[1]
        curr_state = extract_state(me, out[2], grid, matrix)

        _reward = reward(curr_state, old_state,curr_state[4], old_state[4])
        total_reward += math.pow(discount, i)*_reward
        old_state = curr_state
    
    return total_reward

def evaluate(me, players, grid, matrix):
    
    old_state = extract_state(me, players,grid, matrix)

    act_reward = {}
    max_reward = -100000
    next_act = ""
    
    for act in entity.action_names:

        _me, _grid, _players = transition(me, players, grid, matrix, act)
        
        curr_state = extract_state(_me, _players, _grid, matrix)
    
        _reward = reward(curr_state, old_state,curr_state[4], old_state[4])
        if is_same(_me, me):
            print(f"\n==========================\nWarning leak detected in copy, before and after states same for action {act}:")
            print(_me)
            print(".... same as ....")
            print(me)
            print("\n===========================\n")

        act_reward[act] = _reward
        if _reward > max_reward:
            max_reward = _reward
            next_act = act

    print(act_reward, "   Action: ", next_act, " Max Reward: ", max_reward)

    return next_act

MAX_GEN = 7
LEN = 1 #single action 
def select_strategy(me, players, grid, matrix):


    max_rew = -100000
    next_acts = []
    sum = 0
    rews = []
    
    for action in entity.action_names:

        sol = [action]
        
        rew = evaluate_sequence(me.copy(), players.copy(), grid.copy(), matrix, sol)
        sum += rew
        rews.append(rew)
        if max_rew <= rew:
            max_rew = rew
            
            
    
    for idx, r in enumerate(rews):
        if r == max_rew:
            next_acts.append(entity.action_names[idx])

    sel = next_acts[random.randint(0, len(next_acts)-1)]
    #print(">>", sum/MAX_GEN,"   ", next_acts,"  -->   ", sel, "    Player:", me["id"])
    #print("......  \n")
    return [sel]#ga.ga(entity.action_names, me, players, grid, matrix)
    
def inform(me, matrix, grid, players):
    
    
    action_index = random.randint(0,len(entity.action_names)-1)
    
    next_acts = [entity.action_names[action_index]]
    
        
    if AI:
        next_acts =  select_strategy(me, players, grid, matrix)#evaluate(me, players, grid, matrix)
            
    return [next_acts[0]]

