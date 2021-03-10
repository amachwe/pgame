from operator import le
import pygame, sys
import random
import numpy as np
import entity as en
import events as ev
import build as bl
import ai 
import player_ga
import aiohttp
import json
import asyncio

# colors
darkgreen = pygame.colordict.THECOLORS["chartreuse4"]
darkbrown = pygame.colordict.THECOLORS["saddlebrown"]
black = pygame.colordict.THECOLORS["black"]
white = pygame.colordict.THECOLORS["white"]
sand = pygame.colordict.THECOLORS["darkgoldenrod1"]


#images
kn = pygame.transform.scale(pygame.image.load("kn.jpg"), (14,14))
dr = pygame.transform.scale(pygame.image.load("dr.png"), (14,14))

pygame.init()
size = width, height = 1021, 700
cell_size = 14
screen_size = 1021, 641
display_size = 1021, 700-screen_size[1]

clock = pygame.time.Clock()

speed = [2, 2]
black = 0, 0, 0

MAX_MOVES = 500

screen = pygame.display.set_mode(size)

VIDEO = False



def draw_img(im, x,y):
    screen.blit(im,(x,y))

def make_video(screen,game_id, interval=100):

    _image_num = 0
    import os

    os.mkdir(f"./video/{game_id}")
    slot = 500/interval
    counter = 0
    while True:
        counter+= 1
        if counter == slot:
            _image_num += 1
            str_num = "000" + str(_image_num)
            file_name = f"./video/{game_id}/image" + str_num[-4:] + ".jpg"
            
            pygame.image.save(screen, file_name)
            counter = 0
        
        yield

def take_turn(_turn_id):
    _turn_id = _turn_id + 1
            
    if _turn_id >= len(players):
            _turn_id = 0
    
    return _turn_id

def draw_all(matrix, image_player_map):
    for p in players:
        mtx = matrix[p["x"]][p["y"]]
        draw_img(image_player_map[p["id"]],mtx[0],mtx[1])

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def turn_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = 1, 642 
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = 499, 662 
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

def control_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.topleft = 1, 672 
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

async def post_step(step, player):
    
    async with aiohttp.ClientSession() as sess:
        async with sess.post(f"http://localhost:8080/event/{player}/{step}") as response:
            pass

pos_ = 0
turn_id = 0

if __name__ == "__main__":

    import time
    game_id = int(time.time())

    with open("game_record.txt", "a+") as fh:
        fh.write(str(game_id))
        fh.write(", ")
        fh.write(str(time.localtime()))
        fh.write("\n")

    if VIDEO:
        save_screen = make_video(screen,game_id)

    # Grid has the play grid for drawing. Matrix is an indexed representation for movement purposes - entities track movement using matrix which is then translated to the grid when
    # drawing things.
    grid, matrix = bl.build_grid(cell_size, screen_size)


    players = [en.knight1,en.knight2, en.dragon]
    player_img_map = {
        en.knight1["id"]: kn,
        en.knight2["id"]: kn,
        en.dragon["id"]: dr
    }
    pygame.draw.rect(screen, black, [0, screen_size[1], display_size[0], display_size[1]])

    total_moves = 0
    left_moves = []
    gen_event = None
    while pygame.time.wait(10):
        pos_=0
        
        done_event = True
        # Player turn -> AI turn
        if players[turn_id]["player"]:
            player = players[turn_id]
            total_moves += 1
            if player["health"] <= 0:
                print("Player: ", player["id"], " is dead. GAME OVER")
                sys.exit()
            if total_moves> MAX_MOVES:
                print("Players survived.   Well done! GAME OVER")
                sys.exit()

            if done_event == True:
                if len(left_moves) == 0:
                    
                    left_moves = player_ga.inform(player, matrix,grid, players)

                done_event = False
                act = left_moves.pop(0)
                gen_event = ev.actions_map[act]
                player_ga.record_data(game_id, player, matrix, grid, players, act)
                pygame.event.post(gen_event)
            
            # player AI generate events
            for event in pygame.event.get():
                if gen_event == event:
                    done_event == True
                    
                if event.type == pygame.QUIT: sys.exit()
                elif event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_DOWN:
                        pos_ = 5
                    elif event.key == pygame.K_UP:
                        pos_ = 1
                    elif event.key == pygame.K_RIGHT:
                        pos_ = 3
                    elif event.key == pygame.K_LEFT:
                        pos_ = 7
                    elif event.key == pygame.K_s:
                        # search
                        en.Transitions.search(player, grid, matrix)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_r:
                        # rest
                        en.Transitions.rest(player)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_g:
                        # grow
                        en.Transitions.grow(player, grid, matrix)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_l:
                        # look - work in progress
                        # Bhev.look(players[turn_id], grid, matrix)
                        # Bhev.moved(players[turn_id])

                        turn_id = take_turn(turn_id)
                    

            if pos_ != 0:
                
                if en.turn(pos_, player, players, matrix):
                    en.Transitions.move(player)
            

                turn_id = take_turn(turn_id)
                
        else:
            # AI
            
            #rule based 'dragon'
            
            obs = ai.observe(players[turn_id], matrix, players)
            ai.orient(players[turn_id], matrix, obs)
            ai.decide(players[turn_id], matrix, obs)
            ai.act(players[turn_id], matrix, obs)

            turn_id = take_turn(turn_id)

        # Groom world Draw
        for i in grid.keys():
            for k,v in grid[i].items():
                
                pygame.draw.rect(screen, v["color"], v["coord"], v["filled"])

        pygame.draw.rect(screen, black, [0, screen_size[1], display_size[0], display_size[1]])

        turn_display(f"{players[turn_id]['name']}    Moves:  {total_moves}/{MAX_MOVES}")
        control_display("(S)earch, (A)ttack (R)est (G)row (L)ook")

        dt = ""
        for p in players:
            dt = dt + f"{p['name']}: {p['food']}/{p['health']}    "

        message_display(dt)

        draw_all(matrix, player_img_map)
        if VIDEO:
            next(save_screen)
        pygame.display.flip()