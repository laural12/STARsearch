# this will ensure the antenna is properly oriented
from rotation import Rotation
import time
import sys


path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi


class Orientation:
    # az = 0
    # el = 0

    def __init__(self):
        # init variables
        self.rot = Rotation(GUI_test=False)
        self.AZ_LIMIT_ORIENTATION = 200  # this is the orientation at the limit switch
        self.EL_LIMIT_ORIENTATION = 0  # this is the orientation at the limit switch
        self.DEBOUNCE_VAL = (
            1  # Arbitrary; how many triggers to wait before trusting the limit switch
        )

        self.azLimTriggers = 0
        self.elLimTriggers = 0
        self.azOrientDone = True
        self.elOrientDone = True

        # Function setup
        wpi.wiringPiISR(
            self.rot.LIMIT_ENC_AZ, wpi.INT_EDGE_RISING, self.azLimitswitchHit
        )
        # wpi.wiringPiISR(self.rot.LIMIT_ENC_EL, wpi.INT_EDGE_RISING, self.elLimitswitchHit)

    def orientation_init(self):
        print("orientation_init")
        self.azOrientDone = False
        self.elOrientDone = False

        self.rot.azTurnLeft()
        self.rot.elTurnDown()

    def orientToPoint(self, antLat, antLong, antElevation, satLat, satLong):
        # math equation
        # if az angle 0-180 turn right
        # else 181-360 turn left or smth like that
        self.rot.elTurnUp()  # until reaches correct angle

    def azLimitswitchHit(self):
        print("Called azLimitswitchHit()")
        if not self.azOrientDone:  # Don't run this if we aren't in orient init mode
            self.azLimTriggers += 1

            if self.azLimTriggers > self.DEBOUNCE_VAL:
                self.azOrientDone = True
                self.azLimTriggers = 0
                self.rot.azReset()
                Orientation.az = self.AZ_LIMIT_ORIENTATION

    def elLimitswitchHit(self):
        print("Called elLimitswitchHit()")
        if not self.elOrientDone:  # Don't run this if we aren't in orient init mode
            self.elLimTriggers += 1

            if self.elLimTriggers > self.DEBOUNCE_VAL:
                self.elOrientDone = True
                self.elLimTriggers = 0
                self.rot.elReset()
                Orientation.el = self.EL_LIMIT_ORIENTATION
