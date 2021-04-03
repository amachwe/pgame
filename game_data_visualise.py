import pymongo
from matplotlib import pyplot as plt


game_data = pymongo.MongoClient().get_database("drl").get_collection("game_data")
# 0.1 1617204491.76774
# 0.01 1617191596.5538063
# 0 1617192405.677702
# 0.5 1617205127.6059365
explore = []
game_len = []
r = []
pr = [0, 0.01, 0.1, 0.5]#, 0.05]
run_ids = ["1617192405.677702", "1617191596.5538063","1617204491.76774","1617205127.6059365"]#,"1617281282.9496772"]
for idx, ri in enumerate(run_ids):
    r = []
    game_len = []
    explore = []
    for i in game_data.find({"run_id":ri}):
        game_len.append(i["total_moves"])
        explore.append(i["explored"])
        r.append(i["explored"]/i["total_moves"])
    plt.plot(game_len,label="game len"+str(pr[idx]))
    #plt.plot(explore, label="explore"+str(pr[idx]))
    #plt.plot(r , label= pr[idx])
plt.legend()
plt.show()