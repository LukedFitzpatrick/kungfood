from constants import *
from gameobject import *
import random

def spawnFruit(objects):
   fruitwidth = 16
   x = random.choice([0, GAME_WIDTH-fruitwidth])
   y = random.choice([0, GAME_HEIGHT-fruitwidth])
   
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

