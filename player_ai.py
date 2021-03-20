import pygame
import pymongo
import tensorflow as tf
import random
import time

from tensorflow.python.ops.gen_math_ops import sqrt
import entity
import events
import offline_learn_2 as ml
import pprint
import numpy
import math

#pygame.event.post(newevent)
model = tf.keras.models.load_model("../pgame/model_complex")
experience = []



collection = pymongo.MongoClient().get_database("drl").get_collection("games")
AI = True
actions = events.actions
action_c = ml.CategoryToOneHot(events.action_names)
action_t = ml.CategoryToOneHot(["hill", "grass", "water"])

OBJECTIVE_COUNT = 2
move_rate = 0.5




def evaluate(curr_health, curr_food, state, eval_data):
        
    data = [curr_food/ml.MAX_FOOD,curr_health/ml.MAX_HEALTH, state[0]/ml.MAX_STATE]#, x, y]
    base_len = len(data)
    rewarding_acts = {}
    max_rewarding_act = ""
    max_reward = 0
    for act in events.action_names:
    
        data.extend(action_c.to_one_hot(act))
        data.extend(action_t.to_one_hot(state[1]))
        #evaluate possible next actions for predicted obj score
        res = model.predict([data])[0]
        
        
        if max_reward < res:
            max_reward = res
            max_rewarding_act = act
      
        rewarding_acts[act] = res[0]
        
        del data[base_len:]
    
    mean = numpy.mean(list(rewarding_acts.values()))

    print(rewarding_acts)
    p_acts = []
 
    for k,v in rewarding_acts.items():
        if v >= mean:
            p_acts.append(k)
            
    print(p_acts)
    
    selected = p_acts[random.randint(0, len(p_acts))-1]

    
    
    print(f"selected act: {max_rewarding_act}, reward prob: {max_reward}, selected: {selected}")
    return selected

def inform(game_id, me, matrix, grid, players, player_count = 2):
    
    #random actions
    action_index = random.randint(0,len(actions)-1)
    action_data = actions[action_index]
    curr_state = entity.extract_state(me, players, grid, matrix)
    
    if len(experience) >= player_count:
               
        experience[-player_count]["new_state_health"] = curr_state[0]
        experience[-player_count]["new_state_food"] = curr_state[1]
        experience[-player_count]["new_x"] = me["x"]
        experience[-player_count]["new_y"] = me["y"]
        experience[-player_count]["new_state"] = curr_state[2]
        experience[-player_count]["new_type"] = curr_state[3]
        experience[-player_count]["dragon_health"] = curr_state[4]

        old_act = experience[-player_count]["action"]
        x = me["x"]
        y = me["y"]
        old_x = experience[-player_count]["x"]
        old_y = experience[-player_count]["y"]
        old_state = (experience[-player_count]["curr_state_health"],experience[-player_count]["curr_state_food"],experience[-player_count]["state"])
        rew = 4*(curr_state[0]-old_state[0])+3*(curr_state[1]-old_state[1])+(curr_state[2]-old_state[2])+0.5*(abs(x-old_x)+abs(y-old_y))
        experience[-player_count]["reward"] = rew
        # use AI if active - otherwise persist with random
        tile_state = (experience[-player_count]["state"],experience[-player_count]["type"])
        if AI:
            next_act = evaluate(experience[-player_count]["curr_state_health"], experience[-player_count]["curr_state_food"],tile_state, me)
            
            for action in actions:
                if action[0] == next_act:
                    action_data = action
                    print("Selected: ", action_data[0])
                    break

        experience[-player_count]["AI"] = AI
        collection.insert_one(experience[-player_count])
        
    
    experience.append({
        "player_id":me["id"],
        "game_id":game_id,
        "time":time.time(),
        "curr_state_health": curr_state[0],
        "curr_state_food": curr_state[1],
        "action": action_data[0],
        "x": me["x"],
        "y": me["y"],
        "state": curr_state[2],
        "type": curr_state[3]
        
    })

    
    return action_data[0], action_data[1]
   

def correct(orig, correct, me, matrix):
    pass

