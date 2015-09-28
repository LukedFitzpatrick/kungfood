import pygame, os, random
from constants import *

class GameObject:
    def __init__(self, image, x, y):
        self.image = pygame.image.load(os.path.join("graphics/"+image))
        self.image.convert()
        self.x = x
        self.y = y
        

    def display(self, screen, x, y):
        screen.blit(self.image, (x, y))

    def update(self):
        pass


class PlayerObject:
    def __init__ (self, walkframes, kickframes, punchframes, 
                  blockframes, crouchframes):
        self.walkframes = []
        self.kickframes = []
        self.punchframes = []
        self.blockframes = []
        self.crouchframes = []

        paths = [walkframes, kickframes, punchframes,
                 blockframes, crouchframes]
        images = [self.walkframes, self.kickframes, self.punchframes,
                  self.blockframes, self.crouchframes]

        for i in range(0, len(paths)):
            for f in paths[i]:
                t = pygame.image.load(os.path.join("graphics/"+f))
                t.convert()
                images[i].append(t)

        self.currentframe = self.walkframes[0]
        self.frameindex = 0
        self.state = STAND
        self.x = SCREEN_WIDTH/2
        self.y = SCREEN_HEIGHT - self.currentframe.get_height()
        self.xv = 0
        self.flip = False

    def display(self, screen, x, y):
        if self.flip:
            flip=pygame.transform.flip(self.currentframe, True, False)
            screen.blit(flip, (x, y))
        else:
            screen.blit(self.currentframe, (x, y))

    def right(self):
        if(self.state != WALK):
            self.state = WALK
            self.frameindex = 0
        self.xv = WALK_SPEED
        self.flip = True
    
    def left(self):
        if(self.state != WALK):
            self.state = WALK
            self.frameindex = 0
        self.xv = -WALK_SPEED
        self.flip = False

    def stop(self):
        self.state = STAND
        self.xv = 0
    
    def punch(self):
        if(self.state != PUNCH):
            self.state = PUNCH
            self.xv = 0

    def kick(self):
        if(self.state != KICK):
            self.state = KICK
            self.xv = 0
    
    def block(self):
        self.state = BLOCK
        self.xv = 0
    
    def crouch(self):
        self.state = CROUCH
        self.xv = 0

    def update(self):
        if(self.state == STAND):
            self.currentframe = self.walkframes[0]
        else:
            frames = []
            if(self.state == WALK):
                frames = self.walkframes
            elif(self.state == KICK):
                frames = self.kickframes
            elif(self.state == PUNCH):
                frames = self.punchframes
            elif(self.state == BLOCK):
                frames = self.blockframes
            elif(self.state == CROUCH):
                frames = self.crouchframes
                
            self.frameindex += 1
            if self.frameindex >= len(frames):
                self.frameindex = 0

            self.currentframe = frames[self.frameindex]
        
        self.y = SCREEN_HEIGHT - self.currentframe.get_height()
        self.x += self.xv

