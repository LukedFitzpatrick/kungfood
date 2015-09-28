from pygame.locals import *
import pygame

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 192

STAND = 0
WALK = 1
KICK = 2
PUNCH = 3
BLOCK = 4
CROUCH = 5

WALK_SPEED = 10

LEFT_K = pygame.K_a
RIGHT_K = pygame.K_d
CROUCH_K = pygame.K_s
PUNCH_K = pygame.K_j
KICK_K = pygame.K_k
BLOCK_K = pygame.K_SPACE
