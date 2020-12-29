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
import math

#pygame.event.post(newevent)
model = tf.keras.models.load_model("../pgame/model_complex")
experience = []



collection = pymongo.MongoClient().get_database("drl").get_collection("games")
AI = True
actions = events.actions
action_c = ml.CategoryToOneHot(events.action_names)

OBJECTIVE_COUNT = 2
move_rate = 0.5


def distance(xy):
    return math.sqrt(math.pow(xy[0],2)+math.pow(xy[1],2))

def evaluate(curr_health, curr_food, state, prev_action, prev_reward, eval_data):
        
    data = [curr_food/ml.MAX_FOOD,curr_health/ml.MAX_HEALTH, state/ml.MAX_STATE]
    data.extend(action_c.to_one_hot(prev_action))
    base_len = len(data)
    
    predicted_max_obj = list([0 for i in range(0,OBJECTIVE_COUNT)])
    next_acts = list(["" for i in range(0,OBJECTIVE_COUNT)])
    for act in events.action_names:
    
        data.extend(action_c.to_one_hot(act))
        
        #evaluate possible next actions for predicted obj score
        res = model.predict([data])[0]

        # align objectives against predicted for action
        for i, m in enumerate(zip(predicted_max_obj, res)):
            if m[0]<m[1]:
                predicted_max_obj[i] = m[1]
                next_acts[i] =act 

        del data[base_len:]
    
    next_act = next_acts[0]
    if prev_reward > predicted_max_obj[0]:
        # predicted reward is decreasing so try other actions
        for na in next_acts:
            if na != prev_action:
                next_act = na
                break

    eval_data["total_steps"] += 1
    
    if eval_data["moves"]/eval_data["total_steps"] <= move_rate:
        eval_data["moves"] += 1
        next_act = events.move_actions[random.randint(0, len(events.move_actions)-1)][0]
    return next_act


def inform(game_id, me, matrix, grid, players, player_count = 2):
    health = me["health"]
    food = me["food"]
    x, y = me["x"], me["y"]
    state = entity.get_cell_state(me, matrix, grid)
    #random actions
    action_index = random.randint(0,len(actions)-1)
    action_data = actions[action_index]
    curr_state = (health, food)
    if len(experience) >= player_count:
               
        experience[-player_count]["new_state_health"] = curr_state[0]
        experience[-player_count]["new_state_food"] = curr_state[1]
        experience[-player_count]["new_x"] = x
        experience[-player_count]["new_y"] = y
        experience[-player_count]["new_state"] = state
        old_state = (experience[-player_count]["curr_state_health"],experience[-player_count]["curr_state_food"])
        experience[-player_count]["reward"] = (curr_state[0]-old_state[0])+(curr_state[1]-old_state[1])
        # use AI if active - otherwise persist with random
        if AI:
            next_act = evaluate(experience[-player_count]["curr_state_health"], experience[-player_count]["curr_state_food"],experience[-player_count]["state"], experience[-player_count]["action"], experience[-player_count]["reward"], me)
            
            for action in actions:
                if action[0] == next_act:
                    action_data = action
                    print("Selected: ", action_data[0])
                    break

        
        collection.insert_one(experience[-player_count])
        
    
    experience.append({
        "player_id":me["id"],
        "game_id":game_id,
        "time":time.time(),
        "curr_state_health": curr_state[0],
        "curr_state_food": curr_state[1],
        "action": action_data[0],
        "x": x,
        "y": y,
        "state": state
        
    })

    
    return action_data[0], action_data[1]
   

def correct(orig, correct, me, matrix):
    pass

