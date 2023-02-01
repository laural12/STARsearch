# this will ensure the antenna is properly oriented
from rotation import Rotation
import time
import sys


path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi

class Orientation:
    az = 0
    el = 0
    
    def __init__(self):
      self.rot = Rotation(GUI_test = False)
      self.AZ_LIMIT_ORIENTATION = 200 #this is the orientation at the limit switch
      self.EL_LIMIT_ORIENTATION = 0 #this is the orientation at the limit switch

    def orientation_init(self):   
      print("orientation_init")
      wpi.wiringPiISR(self.rot.LIMIT_ENC_AZ, wpi.INT_EDGE_BOTH, self.azLimitswitchHit)
      # wpi.wiringPiISR(self.rot.LIMIT_ENC_EL, wpi.INT_EDGE_BOTH, self.elLimitswitchHit)
      # rot.azTurnLeft()
      # rot.elTurnDown()

    def orientToPoint(self, antLat, antLong, antElevation, satLat, satLong):
      #math equation
      #if az angle 0-180 turn right
      #else 181-360 turn left or smth like that
      self.rot.elTurnUp() #until reaches correct angle

    def azLimitswitchHit(self):
      print("here az 0")
      self.rot.azReset()
      print("here az")
      Orientation.az = AZ_LIMIT_ORIENTATION

    def elLimitswitchHit(self):
      print("here el 0")
      self.rot.elReset()
      print("here el")
      Orientation.el = EL_LIMIT_ORIENTATION
