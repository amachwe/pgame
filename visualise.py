import pymongo
import sys
from matplotlib import pyplot as plt

client = pymongo.MongoClient()
GAME_ID = int(sys.argv[1])
PLAYER_ID = 0
if len(sys.argv) ==3:
    PLAYER_ID = int(sys.argv[2])
print("Game: ", GAME_ID)
#GAME_ID = 1610841820 #1610841632#1610237606#1610236731# 1609633058#1609544526#1609180123# 1609175947#move=0.5,  1609175091 #1609173245 #1609171369 #1609164037 # 1609162254 mpve = 0.2, # 1609161968 move = 0.9 # 1609114921 move = 0.9 # 1609114181 move = 0.5

q1 = {"player_id":1, "game_id": GAME_ID}
q2 = {"player_id":2, "game_id": GAME_ID}

collection = client.get_database("drl").get_collection("games")
# print("Output:")
# for i in collection.aggregate([{"$group" : {
#     "_id":"$game_id",
#     "count": {"$sum": 1}
# }}]):
#     print(i)

health1 = []
food1 = []
health2 = []
food2 = []

if PLAYER_ID == 0 or PLAYER_ID == 1:
    for i in collection.find(q1).sort("time"):
        health1.append(i["curr_state_health"])
        food1.append(i["curr_state_food"])

if PLAYER_ID == 0 or PLAYER_ID == 2:
    for i in collection.find(q2).sort("time"):
        health2.append(i["curr_state_health"])
        food2.append(i["curr_state_food"])


ax1 = plt.plot(health1,label="Health: Knight 1 against Time")
ax2 = plt.plot(health2, label="Health: Knight 2 against Time")
ax3 = plt.plot(food1, label="Food: Knight 1 against Time")
ax4 = plt.plot(food2, label="Food: Knight 2 against Time")
plt.legend()
plt.show()


