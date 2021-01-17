
import pygame
from pygame import locals
from entity import Behavior as Bhev

k_up = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_UP, mod=pygame.locals.KMOD_NONE)
k_down = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_DOWN, mod=pygame.locals.KMOD_NONE)  
k_left = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_LEFT, mod=pygame.locals.KMOD_NONE)
k_right = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_RIGHT, mod=pygame.locals.KMOD_NONE)
k_rest = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_r, mod=pygame.locals.KMOD_NONE)
k_search = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_s, mod=pygame.locals.KMOD_NONE)
k_grow = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_g, mod=pygame.locals.KMOD_NONE)

def search(player, grid, matrix):
    Bhev.search(player, grid, matrix)
    Bhev.moved(player)

def rest(player, grid=None, matrix=None):
    Bhev.rest(player)
    Bhev.moved(player)

def grow(player, grid, matrix):
    Bhev.farm(player, grid, matrix)
    Bhev.moved(player)

def move(player, grid=None, matrix=None):
    Bhev.moved(player)

actions = [ ("down", k_down, move), ("left", k_left, move), ("rest", k_rest, move), ("right",k_right, move), ("up", k_up, move),("search",k_search, search), ("grow", k_grow, move)]
actions_map = {i[0]:i[1] for i in actions}
action_names = list([action[0] for action in actions])
move_actions = [("down", k_down), ("left", k_left), ("right",k_right), ("up", k_up) ]

