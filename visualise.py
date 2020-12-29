import pymongo
from matplotlib import pyplot as plt

client = pymongo.MongoClient()

GAME_ID = 1609180123# 1609175947#move=0.5,  1609175091 #1609173245 #1609171369 #1609164037 # 1609162254 mpve = 0.2, # 1609161968 move = 0.9 # 1609114921 move = 0.9 # 1609114181 move = 0.5

q1 = {"player_id":1, "game_id": GAME_ID}
q2 = {"player_id":2, "game_id": GAME_ID}

collection = client.get_database("drl").get_collection("games")
print("Output:")
for i in collection.aggregate([{"$group" : {
    "_id":"$game_id",
    "count": {"$sum": 1}
}}]):
    print(i)

health1 = []
health2 = []
for i in collection.find(q1).sort("time"):
    health1.append(i["curr_state_food"])

for i in collection.find(q2).sort("time"):
    health2.append(i["curr_state_food"])


plt.plot(health1)
plt.plot(health2)
plt.show()


