# this will ensure the antenna is properly oriented
from rotation import Rotation
import time

rot = Rotation(GUI_test = False)

def orientation_init():
  rot.azTurnLeft()
  while (!azLimitswitchHit())
    time.sleep(1)
  rot.azReset()
    
  rot.elTurnDown()
  while (!elLimitswitchHit())
    time.sleep(1)
  rot.elReset()
   
  
