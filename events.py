
import pygame
from pygame import locals

k_up = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_UP, mod=pygame.locals.KMOD_NONE)
k_down = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_DOWN, mod=pygame.locals.KMOD_NONE)  
k_left = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_LEFT, mod=pygame.locals.KMOD_NONE)
k_right = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_RIGHT, mod=pygame.locals.KMOD_NONE)
k_rest = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_r, mod=pygame.locals.KMOD_NONE)
k_search = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_s, mod=pygame.locals.KMOD_NONE)
k_grow = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_g, mod=pygame.locals.KMOD_NONE)
k_attack = pygame.event.Event(pygame.locals.KEYDOWN, key=locals.K_a, mod=pygame.locals.KMOD_NONE)



actions = [ ("down", k_down), ("left", k_left), ("rest", k_rest), ("right",k_right), ("up", k_up),("search",k_search), ("grow", k_grow), ("attack", k_attack)]
actions_map = {i[0]:i[1] for i in actions}
action_names = list([i[0] for i in actions])
move_actions = [("down", k_down), ("left", k_left), ("right",k_right), ("up", k_up) ]

