# import WiringPi.GPIO as GPIO


import sys
import time

path = "/home/odroid/.local/lib/python3.10/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi


INPUT = 0
OUTPUT = 1
HIGH = 1
LOW = 0

EL_ENABLE = 24
EL_LEFT_PWM = 21
EL_RIGHT_PWM = 22
AZ_ENABLE = 19
AZ_LEFT_PWM = 28
AZ_RIGHT_PWM = 30
# FILLER_1 = 31
# FILLER_2 = 25

# input pins
AZ_ENC1 =
AZ_ENC2 = 
EL_ENC1 =
EL_ENC2 = 
LIMIT_ENC_AZ =
LIMIT_ENC_EL =  
ANTENNA_INPUT = # ???? 

# # Set GPIO numbering mode
wpi.wiringPiSetupGpio()

# Set pin 22 as an output, and set servo1 as pin 22 as PWM
wpi.pinMode(EL_ENABLE, OUTPUT)  # CHOOSE NEW PIN: GPIO 24
wpi.pinMode(EL_LEFT_PWM, OUTPUT)  # GPIO 21
wpi.pinMode(EL_RIGHT_PWM, OUTPUT)  # GPIO 22
wpi.pinMode(AZ_ENABLE, OUTPUT)  # GPIO 19
wpi.pinMode(AZ_LEFT_PWM, OUTPUT)  # GPIO 28
wpi.pinMode(AZ_RIGHT_PWM, OUTPUT)  # GPIO 30
# wpi.pinMode(FILLER_1, OUTPUT)  # GPIO 31
# wpi.pinMode(FILLER_2, OUTPUT)  # CHOOSE NEW PIN: GPIO 25

# Set input pins
wpi.pinMode(AZ_ENC1, INPUT)  # GPIO 
wpi.pinMode(AZ_ENC2, INPUT)  # GPIO 
wpi.pinMode(EL_ENC1, INPUT)  # GPIO 
wpi.pinMode(EL_ENC2, INPUT)  # GPIO 
wpi.pinMode(LIMIT_ENC_AZ, INPUT)  # GPIO 
wpi.pinMode(LIMIT_ENC_EL, INPUT)  # GPIO 
wpi.pinMode(ANTENNA_INPUT, INPUT)  # GPIO 


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        # wpi.digitalWrite(EL_LEFT_EN, LOW)
        # wpi.digitalWrite(EL_RIGHT_EN, HIGH)

        wpi.digitalWrite(EL_ENABLE, LOW)  # PWM to move motor

    def azLeftPWM(self):
        print("Called function azLeftPWM()")
        wpi.digitalWrite(AZ_LEFT_PWM, HIGH)  # Az left PWM

    def azRightPWM(self):
        print("Called function azRightPWM()")
        wpi.digitalWrite(AZ_RIGHT_PWM, HIGH)  # Az right PWM

    def elLeftPWM(self):
        print("Called function elLeftPWM()")
        wpi.digitalWrite(EL_LEFT_PWM, HIGH)  # El left PWM

    def elRightPWM(self):
        print("Called function elRightPWM()")
        wpi.digitalWrite(EL_RIGHT_PWM, HIGH)  # El right PWM

    def azEnable(self):
        print("Called function azEnable()")
        wpi.digitalWrite(AZ_ENABLE, HIGH)  # az enable (left and right)

    def elEnable(self):
        print("Called function elEnable()")
        wpi.digitalWrite(EL_ENABLE, HIGH)  # El enable

    def azReset(self):
        print("Called function azReset()")

        # reset everything
        wpi.digitalWrite(AZ_ENABLE, LOW)  # az disable
        wpi.digitalWrite(AZ_LEFT_PWM, LOW)  # Az left disable
        wpi.digitalWrite(AZ_RIGHT_PWM, LOW)  # Az right disable

    def elReset(self):
        print("Called function elReset()")

        # reset everything
        wpi.digitalWrite(EL_ENABLE, LOW)  # el start
        wpi.digitalWrite(EL_LEFT_PWM, LOW)  # el left disable
        wpi.digitalWrite(EL_RIGHT_PWM, LOW)  # el right disable

    def elTurnRight(self):
        print("Called function elTurnRight()")

        # wpi.digitalWrite(EL_ENABLE, HIGH)  # el enable
        # wpi.digitalWrite(EL_LEFT_PWM, LOW)  # el set left low
        # wpi.digitalWrite(EL_RIGHT_PWM, HIGH)  # el set right high

        self.elReset()
        self.elEnable()
        self.elRightPWM()

    def azTurnRight(self):
        print("Called function azTurnRight()")

        # wpi.digitalWrite(AZ_ENABLE, HIGH)  # az enable
        # wpi.digitalWrite(AZ_LEFT_PWM, LOW)  # az set left low
        # wpi.digitalWrite(AZ_RIGHT_PWM, HIGH)  # az set right high

        self.azReset()
        self.azEnable()
        self.azRightPWM()

    def elTurnLeft(self):
        print("Called function elTurnLeft()")

        # wpi.digitalWrite(EL_ENABLE, HIGH)  # el enable
        # wpi.digitalWrite(EL_LEFT_PWM, HIGH)  # el set left high
        # wpi.digitalWrite(EL_RIGHT_PWM, LOW)  # el set right low
        self.elReset()
        self.elEnable()
        self.elLeftPWM()

    def azTurnLeft(self):
        print("Called function azTurnLeft()")

        # wpi.digitalWrite(AZ_ENABLE, HIGH)  # az enable
        # wpi.digitalWrite(AZ_LEFT_PWM, HIGH)  # az set left high
        # wpi.digitalWrite(AZ_RIGHT_PWM, LOW)  # az set right low

        self.azReset()
        self.azEnable()
        self.azLeftPWM()
        
    
    
    
    # READ FUNCTIONS
    def readLimEl(self):
        print("Called function readLimEl()")
        
        print("El limit switch returned:")
        print(wpi.digitalRead(LIMIT_ENC_EL))
        
        return 0 # FIXME: I DON'T WANT TO READ TWICE SO GET RID OF PRINT ONCE VERIFIED


def main():
    myrotate = Rotation()

    myrotate.rotate()


if __name__ == "__main__":
    main()
