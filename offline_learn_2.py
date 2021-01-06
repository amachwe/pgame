import tensorflow as tf
import numpy as np
import pymongo
from matplotlib import pyplot as plt
from tensorflow.python.keras.layers.core import Dropout
import events
import math

MAX_FOOD = 100
MAX_HEALTH = 10
MAX_STATE = 10


class CategoryToOneHot(object):
    cats = {}
    def __init__(self, _cats):
   
        for idx, i in enumerate(_cats):
            self.cats[i] = list([float(0) for j in range(0,len(_cats))])
            self.cats[i][idx] = 1.0

    
    def to_one_hot(self,cat):
        return self.cats.get(cat)
    
action_c = CategoryToOneHot(events.action_names)
action_t = CategoryToOneHot(["hill", "grass", "water"])

def build_reward(reward):

    if reward+4 > 0:
        return 1
    else:
        return 0
   


def dataprep():

    client = pymongo.MongoClient()

    one_count = 0
    collection = client.get_database("drl").get_collection("games")
    raw_X = []
    raw_Y = []

    
    for i in collection.find():
    
        d=[i['curr_state_food']/MAX_FOOD,i['curr_state_health']/MAX_HEALTH, i["state"]/MAX_STATE#, i["x"], i["y"],
        
        ]
        # i['new_state_food']/MAX_FOOD,i['new_state_health']/MAX_HEALTH, i["new_state"]/MAX_STATE, i["new_x"], i["new_y"]
        
        d.extend(action_c.to_one_hot(i["action"]))
        d.extend(action_t.to_one_hot(i["type"]))
        raw_X.append(d)
        reward = build_reward(i["reward"])
        one_count = reward+one_count
        raw_Y.append(reward)


    print("Ones: ", one_count*100/len(raw_Y), "Zeroes: ", (len(raw_Y)-one_count)*100/len(raw_Y))

    return raw_X, raw_Y




if __name__ == '__main__':
    raw_X, raw_Y = dataprep()
    print(f"Input: {len(raw_X[0])}")
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Dense(len(raw_X[0])),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(50),
            tf.keras.layers.Dense(1)
        ]
    )



    train_size = int(len(raw_X)*.7)


    train_X = raw_X[:train_size]
    train_Y = raw_Y[:train_size]

    test_X = raw_X[train_size:]
    test_Y = raw_Y[train_size:]

    print("\n Data: ",len(train_X), len(train_Y), np.array(train_Y).sum()/len(train_Y), len(test_X), len(test_Y), np.array(test_Y).sum()/len(test_Y),"\n")

    model.compile(optimizer='sgd', loss=tf.keras.losses.MeanAbsoluteError(), metrics=["accuracy"])

    model.fit(train_X, train_Y, epochs=30)

    print("Result of testing: ",model.evaluate(test_X, test_Y, batch_size=20))

    model.save("../pgame/model_complex")



        