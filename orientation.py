# this will ensure the antenna is properly oriented
from rotation import Rotation
import time

class Orientation:
    az = 0
    el = 0
    
    def __init__(self):
      rot = Rotation(GUI_test = False)

      self.AZ_LIMIT_ORIENTATION = 200 #this is the orientation at the limit switch
      self.EL_LIMIT_ORIENTATION = 0 #this is the orientation at the limit switch

    def orientation_init():
      
      
      wpi.wiringPiISR(LIMIT_ENC_AZ, wpi.INT_EDGE_BOTH, self.azLimitswitchHit)
      wpi.wiringPiISR(LIMIT_ENC_EL, wpi.INT_EDGE_BOTH, self.elLimitswitchHit)

      rot.azTurnLeft()
      rot.elTurnDown()

    def orientToPoint(antLat, antLong, antElevation, satLat, satLong):
      #math equation

      #if az angle 0-180 turn right
      #else 181-360 turn left or smth like that

      rot.elTurnUp() #until reaches correct angle

    def azLimitswitchHit():
      rot.azReset()
      Orientation.az = AZ_LIMIT_ORIENTATION


    def elLimitswitchHit():
      rot.elReset()
      Orientation.el = EL_LIMIT_ORIENTATION
