import pygame, sys
from pygame.locals import *
from constants import *
from gameobject import *
from spawner import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))



objects = []
for x in range(0, GAME_WIDTH/32):
    for y in range(0, GAME_HEIGHT/32):
      if(x%4 == 0):
         tile = GameObject("bluetile.png", x*32, y*32, 0, 0)
      else:
         tile = GameObject("purpletile.png", x*32, y*32, 0, 0)
      objects.append(tile)

longwalk = []
for i in range(0, 5): longwalk.append("walk1.png")
for i in range(0, 5): longwalk.append("walk2.png")
man = PlayerObject(longwalk, ["kick1.png"],
               ["punch1.png"], ["block1.png"], ["crouch1.png"], 
               ["jump1.png"])
objects.append(man)

clock = pygame.time.Clock()
mainloop = True
playtime = 0.0
keysdown = []

camerax = SCREEN_WIDTH/2

spawncounter = 0
while mainloop:
   # Do not go faster than this framerate.
   milliseconds = clock.tick(FPS) 
   playtime += milliseconds / 1000.0 
   spawncounter += 1

   
   if (spawncounter % FRUIT_SPAWN_RATE) == 0:
       objects = spawnFruit(objects)
   
   for event in pygame.event.get():
      # User presses QUIT-button.
      if event.type == pygame.QUIT:
         mainloop = False 
      elif event.type == pygame.KEYDOWN:
         keysdown.append(event.key)
      elif event.type == pygame.KEYUP:
         keysdown.remove(event.key)

   if pygame.K_ESCAPE in keysdown:
      mainloop = False
   elif CROUCH_K in keysdown:
      man.crouch()
   elif BLOCK_K in keysdown:
      man.block()
   elif PUNCH_K in keysdown:
      man.punch()
   elif KICK_K in keysdown:
      man.kick()
   elif LEFT_K in keysdown:
      man.left()
   elif RIGHT_K in keysdown:
      man.right()
   else:
      man.stop()

   if JUMP_K in keysdown:
      man.jump()
            
   text="FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(),playtime)
   pygame.display.set_caption(text)

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0, 0, 0))
   screen.blit(background, (0, 0))

   # collision detection
   px = man.x - (camerax-SCREEN_WIDTH/2)
   # first remove any fruit colliding with hitboxes
   for o in objects:
      if not o is man and o.alive:
         for h in man.hitboxes:
            hrect = pygame.Rect(man.x+h.left, man.y+h.top,h.width, h.height)
            orect = pygame.Rect(o.x, o.y, o.width, o.height)
            if(hrect.colliderect(orect)):
               print "killed fruit"
               objects.remove(o)
        
         if(o in objects):
            orect = pygame.Rect(o.x, o.y, o.width, o.height)
            mrect = pygame.Rect(man.x, man.y, man.width, man.height)
            if(orect.colliderect(mrect)):
                man.health -= 1
                objects.remove(o)
       


   for o in objects:
      displayx = o.x - (camerax-SCREEN_WIDTH/2)
      o.display(screen, o.x - (camerax-SCREEN_WIDTH/2), o.y)
      o.update()
      if o.kill:
         objects.remove(o)


   # update camera
   camerax = man.x
   camerax = max(camerax, SCREEN_WIDTH/2)
   camerax = min(camerax, GAME_WIDTH - (SCREEN_WIDTH/2))

   # display the health
   heart = pygame.image.load(os.path.join("graphics/heart.png"))
   for i in range(0, man.health):
       screen.blit(heart, (HEARTS_X+(i*heart.get_width()),HEARTS_Y))
   
   
   pygame.display.flip()

pygame.quit()
