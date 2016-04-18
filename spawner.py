from constants import *
from gameobject import *
import random

def spawnFruit(objects):
   fruitwidth = 16
   x = random.choice([0, GAME_WIDTH-fruitwidth])
   y = random.choice([0, GAME_HEIGHT-(fruitwidth*5)])
   
   if(x==0):
      xv = random.randint(MIN_FRUIT_V, MAX_FRUIT_V)
   else:
      xv = random.randint(-MAX_FRUIT_V, -MIN_FRUIT_V)
   if(y==0):
      yv = random.randint(MIN_FRUIT_V, MAX_FRUIT_V)
   else:
      yv = random.randint(-MAX_FRUIT_V, -MIN_FRUIT_V)

  
   orange = GameObject("orange.png", x, y, xv, yv, True, True)
   objects.append(orange)
   return objects

def spawnPixel(objects, x, y, xv, yv):
   pixelwidth = 2
   px = random.choice(range(-3, 3)) + x
   py = random.choice(range(-3, 3)) + y
   
   pxv =  xv * random.choice(range(10,100))/10
   pyv =  yv * random.choice(range(10,100))/10

   if pxv == 0:
      pxv = 5
   

   p = GameObject("redpixel.png", px, py, pxv, pyv, True, False)

   p.pixel = True
   p.width = random.randint(2, 5)
   p.height = random.randint(2, 5)
   p.colour = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
   
   objects.append(p)
   return objects
