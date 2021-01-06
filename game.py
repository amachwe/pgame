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

VIDEO = True



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


def draw_all(matrix):
    for p in players:
        mtx = matrix[p["x"]][p["y"]]
        draw_img(p["image"],mtx[0],mtx[1])

def text_objects(text, font):
    textSurface = font.render(text, True, en.white)
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

    if VIDEO:
        save_screen = make_video(screen,game_id)

    # Grid has the play grid for drawing. Matrix is an indexed representation for movement purposes - entities track movement using matrix which is then translated to the grid when
    # drawing things.
    grid, matrix = bl.build_grid(cell_size, screen_size)


    players = [en.knight1,en.knight2, en.dragon]
    pygame.draw.rect(screen, en.black, [0, screen_size[1], display_size[0], display_size[1]])

    total_moves = 0
    while pygame.time.wait(100):
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
                text, gen_event = player_ga.inform(game_id, player, matrix,grid, players)
                print(gen_event, text)
                try:
                    plr = player.copy()
                    del plr["image"]
                    #asyncio.get_event_loop().run_until_complete(post_step(text,json.dumps(plr)))
                except:
                    pass

                done_event = False
            
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
                        ev.search(player, grid, matrix)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_r:
                        # rest
                        ev.rest(player)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_g:
                        # grow
                        ev.grow(player, grid, matrix)

                        turn_id = take_turn(turn_id)
                    elif event.key == pygame.K_l:
                        # look - work in progress
                        # Bhev.look(players[turn_id], grid, matrix)
                        # Bhev.moved(players[turn_id])

                        turn_id = take_turn(turn_id)
                    

            if pos_ != 0:
                
                if en.turn(pos_, player, players, matrix):
                    ev.move(player)
            

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

        pygame.draw.rect(screen, en.black, [0, screen_size[1], display_size[0], display_size[1]])

        turn_display(f"{players[turn_id]['name']}    Moves:  {total_moves}/{MAX_MOVES}")
        control_display("(S)earch, (A)ttack (R)est (G)row (L)ook")

        dt = ""
        for p in players:
            dt = dt + f"{p['name']}: {p['food']}/{p['health']}    "

        message_display(dt)

        draw_all(matrix)
        if VIDEO:
            next(save_screen)
        pygame.display.flip()