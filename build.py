import random
import pygame
import entity as en

def build_cell(i, j, cell_size, context=None, prev=None):

    #print(context)
    if prev:
        #print(len(context))
        if 'hill' in context and random.random() < 0.05:
            return build_hill(i, j, cell_size)
        elif 'water' in context and random.random() < 0.06:
            return build_water(i, j, cell_size)
        
        return prev
        
    else:
        num = random.random()
        if num >= 0.01:
            return build_grass(i, j, cell_size)
        
        elif num <0.01 and num >= 0.001:
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


def build_grid(cell_size, _size):
    
    grid = {}
    row = []
    col = []
    for s in range(0, 10):
        for i in range(0, _size[0], cell_size):
            row.append(i)
            _g = grid.setdefault(i, {})
            for j in range(0, _size[1]-cell_size, cell_size):
                col.append(j)
                cntxt = []
                for t in range(i-(2*cell_size), i+(cell_size), cell_size):
                    for u in range(j-(2*cell_size), j+(cell_size), cell_size):
                    
                        r = grid.get(t)
                        if r:
                            c = r.get(u)
                            if c:
                        
                                cntxt.append(c["type"])
                curr_cell = None
                r = grid.get(i)
                if r:
                    curr_cell = r.get(j)

                _g[j] = build_cell(i,j, cell_size,context=cntxt, prev = curr_cell)
        
    matrix = []

    for i, r in enumerate(row):
        matrix.append([])
        for j, c in enumerate(col):
            matrix[i].append((r,c))
    
    return grid, matrix
            


