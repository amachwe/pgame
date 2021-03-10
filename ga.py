
import random
import player_ga
import entity as en
SEQ_LEN = 1
NUM_SOLS = 5
MAX_GENS = 7
THRESHOLD = 3
def mutate_seq(seq, action_names, rate=0.6):

    _seq = []

    for i, s in enumerate(seq):
        if random.random() < rate:
            _seq.append(action_names[random.randint(0,6)])
        else:
            _seq.append(s)

    
    return _seq

def ga(action_names,me, players, grid, matrix):
    seqs = []
    fitness = []
    for j in range(0, NUM_SOLS):
            seq = []
            for i in range(0,SEQ_LEN):
                seq.append(action_names[random.randint(0,6)])
            
            seqs.append(seq)
    best = []
    max_f = 0
    for i in range(0, MAX_GENS):
        sel = {}
        fitness = []
        for idx, s in enumerate(seqs):
            f = player_ga.evaluate_sequence(me.copy(), players.copy(), grid.copy(), matrix,s)
            sel[idx] = f
            fitness.append(f)
        
        sel = sorted(sel.items(), key=lambda x: x[1])
        #print(sel[-1][1],numpy.array(fitness).mean(),"\n", sel)
        best = seqs[sel[-1][0]]
        max_f = sel[-1][1]
        
        leaders = []
        for i in range(0, THRESHOLD):
            seqs[i] = seqs[sel[-(1+i)][0]]
            leaders.append(seqs[i])
        
        for i in range(THRESHOLD, len(sel)):
            seqs[i] = mutate_seq(leaders[random.randint(0, len(leaders)-1)], en.action_names)
    print(best, "  ", max_f)
    return best
        


if __name__ == '__main__':


    import build as bl

    





    grid, matrix = bl.build_grid()


    players = [en.knight1,en.knight2, en.dragon]

    print(ga(en.action_names, players[0], players, grid, matrix))
    




    # for i in range(0, 10):
    #     for i, seq in enumerate(seqs):
    #         seqs[i] = mutate_seq(seq)
    #         fitness.append(player_ga.evaluate_sequence(players[0], players, grid, matrix, seq))



    


            
            
     
