import pymongo
import time

exp_collection = pymongo.MongoClient().get_database("drl").get_collection("games")
game_data_coll = pymongo.MongoClient().get_database("drl").get_collection("game_data")

def record_data(experience, curr_state, game_id, me, total_moves, act="", player_count=3, AI=True):
    
    
    if len(experience) >= player_count:
               
        experience[-player_count]["new_state_health"] = curr_state[0]
        experience[-player_count]["new_state_food"] = curr_state[1]
        experience[-player_count]["new_x"] = me["x"]
        experience[-player_count]["new_y"] = me["y"]
        experience[-player_count]["new_state"] = curr_state[2]
        experience[-player_count]["new_type"] = curr_state[3]
        experience[-player_count]["new_dragon_health"] = curr_state[5]

        
        x = me["x"]
        y = me["y"]
        
    
        experience[-player_count]["AI"] = AI
        exp_collection.insert_one(experience[-player_count])
    
    


    experience.append({
        "move_id":total_moves,
        "player_id":me["id"],
        "game_id":game_id,
        "time":time.time(),
        "curr_state_health": curr_state[0],
        "curr_state_food": curr_state[1],
        "action": act,
        "x": me["x"],
        "y": me["y"],
        "state": curr_state[2],
        "type": curr_state[3],
        "dragon_health": curr_state[5]
        
    })

def write_game_data(game_data):

    game_data_coll.insert_one(game_data)