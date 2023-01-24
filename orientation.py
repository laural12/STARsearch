# this will ensure the antenna is properly oriented
import rotation as rot
import time

def orientation_init():
  rot.azTurnLeft()
  while (!azLimitswitchHit())
    time.sleep(1)
  rot.azReset()
    
  rot.elTurnDown()
  while (!elLimitswitchHit())
    time.sleep(1)
  rot.elReset()
   
  
