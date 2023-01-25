# this will ensure the antenna is properly oriented
from rotation import Rotation
import time

rot = Rotation(GUI_test = False)

def orientation_init():
  rot.azTurnLeft()
  while (not azLimitswitchHit())
    time.sleep(1)
  rot.azReset()
    
  rot.elTurnDown()
  while (not elLimitswitchHit())
    time.sleep(1)
  rot.elReset()
  
  #set orientation to default orientation
  
def orientToPoint(antLat, antLong, antElevation, satLat, satLong):
  #math equation
   
  #if az angle 0-180 turn right
  #else 181-360 turn left or smth like that
  
  rot.elTurnUp() #until reaches correct angle
