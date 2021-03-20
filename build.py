import random
import entity as en
import numpy as np



GRASS_TX = 0.01
def build_cell_random_fn(i, j, cell_size, grid, prev=None):

    cntx = ""
    for t in range(i-(2*cell_size), i+(cell_size), cell_size):
        for u in range(j-(2*cell_size), j+(cell_size), cell_size):
        
            r = grid.get(t)
            if r:
                c = r.get(u)
                if c:
                    if cntx == "" or cntx == "grass":
                        cntx = c["type"]

    #print(context)
    if prev:
        #print(len(context))
        if 'hill' == cntx and random.random() < 0.09:
            return build_hill(i, j, cell_size)
        elif 'water' == cntx and random.random() < 0.09:
            return build_water(i, j, cell_size)
        
        return prev
        
    else:
        num = random.random()
        if num >= GRASS_TX:
            return build_grass(i, j, cell_size)
        
        elif num < GRASS_TX and num >= 0.001:
            return build_hill(i, j, cell_size)

        else:
            return build_water(i, j, cell_size)

def build_hill(i, j, cell_size):
    hill = en.hill.copy()
    hill["coord"]= [i, j,i+cell_size+1, j+cell_size+1]
    return hill

def build_grass(i, j, cell_size):
    grass = en.grass.copy()
    grass["coord"]= [i, j,i+cell_size+1, j+cell_size+1]
    return grass

def build_water(i, j, cell_size):
    water = en.water.copy()
    water["coord"] = [i, j,i+cell_size+1, j+cell_size+1]
    return water

def build_grid_all_grass(cell_size, _size):
    grid = {}
    rc = np.empty((int(_size[0]/cell_size),int(_size[1]/cell_size)),dtype=np.object)
    r = 0
    c = 0
    for i in range(0, _size[0], cell_size):
            
            _g = grid.setdefault(i, {})
            for j in range(0, _size[1], cell_size):
                rc[r,c] = (i,j)
                
                curr_cell = None
                _r = grid.get(i)
                if r:
                    curr_cell = _r.get(j)

                _g[j] = build_grass(i,j, cell_size)
                c = c+1
            r = r+1
            c = 0
        
    
    return grid, rc
            
   

def build_grid_recur(cell_size,_size):
    
    grid = {}
    rc = np.empty((int(_size[0]/cell_size),int(_size[1]/cell_size)),dtype=np.object)
    r = 0
    c = 0
    for s in range(0, 7):
        for i in range(0, _size[0], cell_size):
            
            _g = grid.setdefault(i, {})
            for j in range(0, _size[1], cell_size):
                rc[r,c] = (i,j)
                
                curr_cell = None
                _r = grid.get(i)
                if r:
                    curr_cell = _r.get(j)

                _g[j] = build_cell_random_fn(i,j, cell_size, grid, prev = curr_cell)
                c = c+1
            r = r+1
            c = 0
        
    
    return grid, rc
            


