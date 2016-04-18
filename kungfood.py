import pygame, sys

from constants import *
from gameobject import *
from spawner import *

def drawRect(p, screen, screenshake):
    r = pygame.Rect(p.x+screenshake, p.y+screenshake,
                    p.width, p.height)
    pygame.draw.rect(screen, p.colour, r)


#pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
pygame.mixer.init()
pygame.display.init()
#pygame.init()

hutSounds = []
hitSounds = []
for i in range(1, 6):
    s1 = pygame.mixer.Sound(os.path.join("sound/hut"+str(i)+".wav"))
    s2 = pygame.mixer.Sound(os.path.join("sound/hit"+str(i)+".wav"))
    hutSounds.append(s1)
    hitSounds.append(s2)
    


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))




objects = []
#for x in range(0, GAME_WIDTH/32):
#    for y in range(0, GAME_HEIGHT/32):
#       tile = GameObject("backtile.png", x*32, y*32, 0, 0)
#       objects.append(tile)

tile = GameObject("dojo.png", 0, 0, 0, 0)
objects.append(tile)

longwalk = []
for i in range(0, 5): longwalk.append("newwalk1.png")
for i in range(0, 5): longwalk.append("newwalk2.png")
man = PlayerObject(longwalk, ["kick1.png"],
               ["punch1.png"], ["block1.png"], ["crouch1.png"], 
               ["jump1.png"])
objects.append(man)

clock = pygame.time.Clock()
mainloop = True
playtime = 0.0
keysdown = []


screenshake = 0

camerax = SCREEN_WIDTH/2

spawncounter = 0
bullettimecounter = 0
FPS = NORMAL_FPS
controllock = False

pygame.mixer.music.load('sound/soundtrack.mp3')
pygame.mixer.music.play(0)


while mainloop:
   pygame.event.pump()
   # Do not go faster than this framerate.
   milliseconds = clock.tick(FPS)
   playtime += milliseconds / 1000.0 
   spawncounter += 1

   screenshake *= -1
   #screenshake += random.choice([-1, 0, 0, 1])
   
   if (spawncounter % FRUIT_SPAWN_RATE) == 0:
       objects = spawnFruit(objects)
   
   #if not controllock: 
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           mainloop = False 
       elif event.type == pygame.KEYDOWN:
           keysdown.append(event.key)
       elif event.type == pygame.KEYUP:
           if event.key in keysdown:
               keysdown.remove(event.key)

   if pygame.K_ESCAPE in keysdown:
      mainloop = False
   elif KICK_K in keysdown:
      man.kick()
      if not pygame.mixer.get_busy():
          random.choice(hutSounds).play()

   elif LEFT_K in keysdown:
      man.left()
   elif RIGHT_K in keysdown:
      man.right()
   else:
      man.stop()

   if not KICK_K in keysdown:
       man.pickedUpKickKey = True

   if JUMP_K in keysdown:
      man.jump()
      
   
   text="FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(),playtime)
   pygame.display.set_caption(text)

   background = pygame.Surface(screen.get_size())
   background = background.convert()
   background.fill((0, 0, 0))
   screen.blit(background, (0, 0))

   if(bullettimecounter > 0):
       bullettimecounter -= 1
       

   if(bullettimecounter <= 0):
       FPS = NORMAL_FPS
       controllock = False
       screenshake = 0

   # collision detection
   px = man.x - (camerax-SCREEN_WIDTH/2)

   # first remove any fruit colliding with hitboxes
   for o in objects:
      if not o is man and o.alive:
         for h in man.hitboxes:
            hrect = pygame.Rect(man.x+h.left, man.y+h.top,h.width, h.height)
            orect = pygame.Rect(o.x, o.y, o.width, o.height)
            if(hrect.colliderect(orect)):
               objects.remove(o)
               bullettimecounter = BULLET_TIME_COUNTDOWN
               #controllock = True
               FPS = BULLET_TIME_FPS
               screenshake = 2
               burstSeedX = random.choice(range(20, 40))/10*man.xv
               burstSeedY = random.choice(range(20, 40))/10*man.yv
               toSpawn = random.randint(PIXEL_MIN_SPAWN_AMOUNT,
                                      PIXEL_MAX_SPAWN_AMOUNT)
               random.choice(hitSounds).play()
               for i in range(0, toSpawn):
                   objects = spawnPixel(objects, o.x, o.y, 
                                        burstSeedX, burstSeedY)

               
        
         if(o in objects):
            orect = pygame.Rect(o.x, o.y, o.width, o.height)
            mrect = pygame.Rect(man.x, man.y, man.width, man.height)
            if(orect.colliderect(mrect)):
                o.xv *= -1
                


   for o in objects:
      displayx = o.x - (camerax-SCREEN_WIDTH/2)
      if not o.pixel:
          o.display(screen, o.x - (camerax-SCREEN_WIDTH/2), o.y, screenshake)
      else:
          drawRect(o, screen, screenshake)
      o.update()
      if o.kill:
         objects.remove(o)


   # update camera
   camerax = man.x
   camerax = max(camerax, SCREEN_WIDTH/2)
   camerax = min(camerax, GAME_WIDTH - (SCREEN_WIDTH/2))
     
   pygame.display.flip()



pygame.quit()
sys.exit()
