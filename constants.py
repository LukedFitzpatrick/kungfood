from pygame.locals import *
import pygame

SCREEN_WIDTH = 512
SCREEN_HEIGHT = 192
GAME_WIDTH = 512
GAME_HEIGHT = 192

FPS = 60

FRUIT_SPAWN_RATE = 100 # 1 in n frames produces fruit
MIN_FRUIT_V = 2
MAX_FRUIT_V = 4

HEARTS_Y = 20
HEARTS_X = 20

STAND = 0
WALK = 1
KICK = 2
PUNCH = 3
BLOCK = 4
CROUCH = 5

JUMPV = -10
GRAVITY = 1
FRUIT_GRAVITY = 0.5
FRUIT_FRICTION = 0.05

WALK_SPEED = 5

LEFT_K = pygame.K_a
RIGHT_K = pygame.K_d
CROUCH_K = pygame.K_s
JUMP_K = pygame.K_w

PUNCH_K = pygame.K_j
KICK_K = pygame.K_k
BLOCK_K = pygame.K_SPACE

DISPLAY_HITBOXES = True
