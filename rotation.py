# import WiringPi.GPIO as GPIO


import sys
from datetime import datetime

# path = "/home/odroid/.local/lib/python3.10/site-packages"
path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi

GUI_TEST = True

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

# input pins
AZ_ENC1 = 31
# AZ_ENC2 =
EL_ENC1 = 25
# EL_ENC2 =
# LIMIT_ENC_AZ =
# LIMIT_ENC_EL =
# ANTENNA_INPUT = # ????


class Rotation:
    def __init__(self, GUI_test=False):
        self.GUI_test = GUI_test
        self.azTicks = 0
        self.elTicks = 0

        if not self.GUI_test:
            # Set GPIO numbering mode
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

            wpi.wiringPiISR(AZ_ENC1, wpi.INT_EDGE_BOTH, self.azTickCounter)
            wpi.wiringPiISR(EL_ENC1, wpi.INT_EDGE_BOTH, self.elTickCounter)

            # Set input pins

            # MAYBE DON'T SET THESE? MAYBE WIRINGPIISR DOES THIS ITSELF?
            # wpi.pinMode(AZ_ENC1, INPUT)  # GPIO
            # wpi.pinMode(AZ_ENC2, INPUT)  # GPIO
            # wpi.pinMode(EL_ENC1, INPUT)  # GPIO
            # wpi.pinMode(EL_ENC2, INPUT)  # GPIO

            # wpi.pinMode(LIMIT_ENC_AZ, INPUT)  # GPIO
            # wpi.pinMode(LIMIT_ENC_EL, INPUT)  # GPIO
            # wpi.pinMode(ANTENNA_INPUT, INPUT)  # GPIO

    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        # wpi.digitalWrite(EL_LEFT_EN, LOW)
        # wpi.digitalWrite(EL_RIGHT_EN, HIGH)

        # wpi.digitalWrite(EL_ENABLE, LOW)  # PWM to move motor
        self.write(EL_ENABLE, LOW, GUI_TEST)

    def write(self, pinNum, writeVal):
        if not self.GUI_test:
            wpi.digitalWrite(pinNum, writeVal)

    def read(self, pinNum):
        if not self.GUI_test:
            return wpi.digitalRead(pinNum)
        else:
            return None

    def azLeftPWM(self):
        print("Called function azLeftPWM()")
        # wpi.digitalWrite(AZ_LEFT_PWM, HIGH)  # Az left PWM
        self.write(AZ_LEFT_PWM, HIGH)

    def azRightPWM(self):
        print("Called function azRightPWM()")
        # wpi.digitalWrite(AZ_RIGHT_PWM, HIGH)  # Az right PWM
        self.write(AZ_RIGHT_PWM, HIGH)

    def elLeftPWM(self):
        print("Called function elLeftPWM()")
        # wpi.digitalWrite(EL_LEFT_PWM, HIGH)  # El left PWM
        self.write(EL_LEFT_PWM, HIGH)

    def elRightPWM(self):
        print("Called function elRightPWM()")
        # wpi.digitalWrite(EL_RIGHT_PWM, HIGH)  # El right PWM
        self.write(EL_RIGHT_PWM, HIGH)

    def azEnable(self):
        print("Called function azEnable()")
        # wpi.digitalWrite(AZ_ENABLE, HIGH)  # az enable (left and right)
        self.write(AZ_ENABLE, HIGH)

    def elEnable(self):
        print("Called function elEnable()")
        # wpi.digitalWrite(EL_ENABLE, HIGH)  # El enable
        self.write(EL_ENABLE, HIGH)

    def azReset(self):
        print("Called function azReset()")

        # reset everything
        # wpi.digitalWrite(AZ_ENABLE, LOW)  # az disable
        # wpi.digitalWrite(AZ_LEFT_PWM, LOW)  # Az left disable
        # wpi.digitalWrite(AZ_RIGHT_PWM, LOW)  # Az right disable
        self.write(AZ_ENABLE, LOW)
        self.write(AZ_LEFT_PWM, LOW)
        self.write(AZ_RIGHT_PWM, LOW)

    def elReset(self):
        print("Called function elReset()")

        # reset everything
        # wpi.digitalWrite(EL_ENABLE, LOW)  # el start
        # wpi.digitalWrite(EL_LEFT_PWM, LOW)  # el left disable
        # wpi.digitalWrite(EL_RIGHT_PWM, LOW)  # el right disable
        self.write(EL_ENABLE, LOW)  # el start
        self.write(EL_LEFT_PWM, LOW)  # el left disable
        self.write(EL_RIGHT_PWM, LOW)  # el right disable

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
        # print(self.read(LIMIT_ENC_EL))

        return datetime.now().strftime(
            "%H:%M:%S"
        )  # FIXME: I DON'T WANT TO READ TWICE SO GET RID OF PRINT ONCE VERIFIED

    def readLimAz(self):
        print("Called function readLimAz()")

        print("Az limit switch returned:")
        # print(self.read(LIMIT_ENC_Az))

        return datetime.now().strftime(
            "%H:%M:%S"
        )  # FIXME: I DON'T WANT TO READ TWICE SO GET RID OF PRINT ONCE VERIFIED

    def azTickCounter(self):
        self.azTicks += 1

    def elTickCounter(self):
        self.elTicks += 1

    def getAzTicks(self):
        return (
            self.azTicks
        )  # FIXME: IN THE END WE WANT TO DISPLAY SOMETHING MORE MEANINGFUL

    def getElTicks(self):
        return (
            self.elTicks
        )  # FIXME: IN THE END WE WANT TO DISPLAY SOMETHING MORE MEANINGFUL


def main():
    myrotate = Rotation()

    myrotate.rotate()


if __name__ == "__main__":
    main()
