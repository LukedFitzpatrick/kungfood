import pygame, os, random
from constants import *

class GameObject:
   def __init__(self, image, x, y, xv, yv, gravity=False, alive=False):
      self.image = pygame.image.load(os.path.join("graphics/"+image))
      self.image.convert()
      self.x = x
      self.y = y
      self.xv = xv
      self.yv = yv
      self.width = self.image.get_width()
      self.height = self.image.get_height()
      self.alive = alive
      self.gravity = gravity
      self.kill = False

   def display(self, screen, x, y):
      screen.blit(self.image, (x, y))

   def update(self):
      self.x += int(self.xv)
      self.y += int(self.yv)

      if self.gravity:
          self.yv += FRUIT_GRAVITY
      if(self.x > GAME_WIDTH-self.width or self.x < 0):
          self.kill = True
      if(self.y >= GAME_HEIGHT-self.height):
          self.yv *= -1
          self.y = GAME_HEIGHT-self.height
      if(self.y <= 0):
          self.yv *= -1
          self.y = 0

      if(self.yv > 0): 
          self.yv -= min(FRUIT_FRICTION, self.yv)
      elif(self.yv < 0):
          self.yv += min(FRUIT_FRICTION, abs(self.yv))


class PlayerObject:
   def __init__ (self, walkframes, kickframes, punchframes, 
              blockframes, crouchframes, jumpframes):
      self.walkframes = []
      self.kickframes = []
      self.punchframes = []
      self.blockframes = []
      self.crouchframes = []
      self.jumpframes = []
      

      paths = [walkframes, kickframes, punchframes,
             blockframes, crouchframes, jumpframes]
      images = [self.walkframes, self.kickframes, self.punchframes,
              self.blockframes, self.crouchframes, self.jumpframes]

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
      self.yv = 0
      self.flip = False
      self.jumping = False

      self.width = self.currentframe.get_width()
      self.height = self.currentframe.get_height()


      self.hitboxes = []
      self.kill = False

      self.health = 5



   def display(self, screen, x, y):
      if self.flip:
         flip=pygame.transform.flip(self.currentframe, True, False)
         screen.blit(flip, (x, y))
      else:
         screen.blit(self.currentframe, (x, y))
      
      if DISPLAY_HITBOXES:
         for h in self.hitboxes:
            newh = pygame.Rect(h.left+x, h.top+y,
                           h.width, h.height)
            pygame.draw.rect(screen, (255, 0, 0), newh)
                        

   def right(self):
      if(self.state != WALK):
         self.state = WALK
         self.frameindex = 0
      self.xv = WALK_SPEED
      self.flip = True
      self.hitboxes = []
   
   def left(self):
      if(self.state != WALK):
         self.state = WALK
         self.frameindex = 0
      self.xv = -WALK_SPEED
      self.flip = False
      self.hitboxes = []

   def stop(self):
      self.state = STAND
      self.xv = 0
      self.hitboxes = []
   
   def punch(self):
      if(self.state != PUNCH):
         self.state = PUNCH
         # hitboxes: values relative to self.x, self.y
         if self.flip:
            h = pygame.Rect(self.punchframes[0].get_width()-30,
                        14, 30, 14)
         else:
            h = pygame.Rect(0, 14, 30, 14)
         
         self.hitboxes = [h]
         self.xv = 0

   def kick(self):
      if(self.state != KICK):
         self.state = KICK
         # hitboxes: values relative to self.x, self.y
         if self.flip:
            h = pygame.Rect(self.kickframes[0].get_width()-30,
                        18, 30, 14)
         else:
            h = pygame.Rect(0, 18, 30, 14)
         
         self.hitboxes = [h]
         self.xv = 0
   
   def block(self):
      self.state = BLOCK
      self.xv = 0
      self.hitboxes = []
   
   def crouch(self):
      self.state = CROUCH
      self.xv = 0
      self.hitboxes = []

   def jump(self):
      if not self.jumping:
         self.jumping = True
         self.yv = JUMPV
         self.hitboxes = []
      
   def update(self):
      
      frames = []
      if(self.state == KICK):
         frames = self.kickframes
      elif(self.state == PUNCH):
         frames = self.punchframes
      elif(self.jumping):
         frames = self.jumpframes
      elif(self.state == WALK):
         frames = self.walkframes
      elif(self.state == CROUCH):
         frames = self.crouchframes
      elif(self.state == STAND):
         frames = [self.walkframes[0]]
      elif(self.state == BLOCK):
         frames = self.blockframes
            
      self.frameindex += 1
      if self.frameindex >= len(frames):
         self.frameindex = 0

      self.currentframe = frames[self.frameindex]
      
      if self.jumping:
         self.y += self.yv
         self.yv += GRAVITY
         if(self.y >= SCREEN_HEIGHT - self.currentframe.get_height()):
            self.jumping = False
            self.y = SCREEN_HEIGHT - self.currentframe.get_height()
            self.yv = 0
      else:
         self.y = SCREEN_HEIGHT - self.currentframe.get_height()

      self.x += self.xv
      self.x = min(self.x, GAME_WIDTH-self.currentframe.get_width())
      self.x = max(self.x, 0)
      
      self.width = self.currentframe.get_width()
      self.height = self.currentframe.get_height()
      
      if self.health < 0:
          self.kill = True
