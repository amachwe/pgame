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
import copy


experience = []



collection = pymongo.MongoClient().get_database("drl").get_collection("games")
AI = True
actions = events.actions




def extract_state(me, grid, matrix):
    health = me["health"]
    food = me["food"]
    state = entity.get_cell_data(me, matrix, grid)
    # return health, food, cell state, cell type
    return (health, food, state[0],state[1], (me["x"], me["y"]))


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
    
    #Health, Food, Cell_Food, Movement
    return (curr_state[0]-old_state[0])+4*(curr_state[1]-old_state[1])+4*(curr_state[2]-old_state[2])+0.5*((abs(xy[0]-old_xy[0])+abs(xy[1]-old_xy[1])))
    

def transition(me, players, grid, matrix, act):
        _me = en_copy(me)
        _grid = copy.deepcopy(grid)
        if act == "search":
            
            events.search(_me, _grid, matrix)
         
        elif act == "grow":
            
            events.grow(_me, _grid, matrix)
          
        elif act == "rest":
             
            events.rest(_me)
            
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

            entity.turn(pos, _me, players, matrix)
            events.move(_me)
        
        return _me, _grid

def evaluate(me, players, grid, matrix):
    discount = 0.9
    old_state = extract_state(me, grid, matrix)

    act_reward = {}
    max_reward = -100000
    next_act = ""
    
    for act in events.action_names:

        _me, _grid = transition(me, players, grid, matrix, act)
        
        curr_state = extract_state(_me, _grid, matrix)
    
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


def inform(game_id, me, matrix, grid, players, player_count = 2):
    
    #random actions
    action_index = random.randint(0,len(actions)-1)
    action_data = actions[action_index]
    curr_state = extract_state(me, grid, matrix)
    
    if len(experience) >= player_count:
               
        experience[-player_count]["new_state_health"] = curr_state[0]
        experience[-player_count]["new_state_food"] = curr_state[1]
        experience[-player_count]["new_x"] = me["x"]
        experience[-player_count]["new_y"] = me["y"]
        experience[-player_count]["new_state"] = curr_state[2]
        experience[-player_count]["new_type"] = curr_state[3]

        old_act = experience[-player_count]["action"]
        x = me["x"]
        y = me["y"]
        old_x = experience[-player_count]["x"]
        old_y = experience[-player_count]["y"]

        
        old_state = (experience[-player_count]["curr_state_health"],experience[-player_count]["curr_state_food"],experience[-player_count]["state"])
        
        experience[-player_count]["reward"] = reward(curr_state, old_state, (x,y),(old_x,old_y))
        # use AI if active - otherwise persist with random
        tile_state = (experience[-player_count]["state"],experience[-player_count]["type"])
        
        if AI:
            next_act = evaluate(me, players, grid, matrix)
            
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
