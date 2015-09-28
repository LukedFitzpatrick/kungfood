import pygame, sys
from pygame.locals import *
from constants import *
from gameobject import *

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

objects = []
for x in range(0, SCREEN_WIDTH/32):
    for y in range(0, SCREEN_HEIGHT/32):
        if(x%4 == 0):
            tile = GameObject("bluetile.png", x*32, y*32)
        else:
            tile = GameObject("purpletile.png", x*32, y*32)
        objects.append(tile)

man = PlayerObject(["walk1.png","walk2.png"],["kick1.png"],
                   ["punch1.png"], ["block1.png"], ["crouch1.png"])
objects.append(man)

clock = pygame.time.Clock()
mainloop = True
FPS = 15
playtime = 0.0
keysdown = []
while mainloop:
    # Do not go faster than this framerate.
    milliseconds = clock.tick(FPS) 
    playtime += milliseconds / 1000.0 
    
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
    
    if CROUCH_K in keysdown:
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


                
    # Print framerate and playtime in titlebar.
    text="FPS: {0:.2f}  Playtime: {1:.2f}".format(clock.get_fps(),playtime)
    pygame.display.set_caption(text)

    for o in objects:
        o.display(screen, o.x, o.y)
        o.update()



    #Update Pygame display.
    pygame.display.flip()

# Finish Pygame.  
pygame.quit()
