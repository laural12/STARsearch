# import WiringPi.GPIO as GPIO


import sys
import time

path = "/home/odroid/.local/lib/python3.10/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi


OUTPUT = 1
HIGH = 1
LOW = 0

EL_PWM = 24
EL_LEFT_EN = 21
EL_RIGHT_EN = 22
AZ_PWM = 19
AZ_LEFT_EN = 28
AZ_RIGHT_EN = 30
FILLER_1 = 31
FILLER_2 = 25

# # Set GPIO numbering mode
wpi.wiringPiSetupGpio()

# Set pin 22 as an output, and set servo1 as pin 22 as PWM
wpi.pinMode(EL_PWM, OUTPUT)  # CHOOSE NEW PIN: GPIO 24
wpi.pinMode(EL_LEFT_EN, OUTPUT)  # GPIO 21
wpi.pinMode(EL_RIGHT_EN, OUTPUT)  # GPIO 22
wpi.pinMode(AZ_PWM, OUTPUT)  # GPIO 19
wpi.pinMode(AZ_LEFT_EN, OUTPUT)  # GPIO 28
wpi.pinMode(AZ_RIGHT_EN, OUTPUT)  # GPIO 30
wpi.pinMode(FILLER_1, OUTPUT)  # GPIO 31
wpi.pinMode(FILLER_2, OUTPUT)  # CHOOSE NEW PIN: GPIO 25


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        #wpi.digitalWrite(EL_LEFT_EN, LOW)
        #wpi.digitalWrite(EL_RIGHT_EN, HIGH)

        wpi.digitalWrite(EL_PWM, LOW)  # PWM to move motor

    def azLeftEn(self):
        print("Called function azLeftEn()")
        wpi.digitalWrite(AZ_LEFT_EN, HIGH)  # Az left enable

    def azRightEn(self):
        print("Called function azRightEn()")
        wpi.digitalWrite(AZ_RIGHT_EN, HIGH)  # Az right enable

    def elLeftEn(self):
        print("Called function elLeftEn()")
        wpi.digitalWrite(EL_LEFT_EN, HIGH)  # El left enable

    def elRightEn(self):
        print("Called function elRightEn()")
        wpi.digitalWrite(EL_RIGHT_EN, HIGH)  # El right enable

    def azStart(self):
        print("Called function azStart()")
        wpi.digitalWrite(AZ_PWM, HIGH)  # az start

    def elStart(self):
        print("Called function elStart()")
        wpi.digitalWrite(EL_PWM, HIGH)  # El start

    def azReset(self):
        print("Called function azReset()")

        # reset everything
        wpi.digitalWrite(AZ_PWM, LOW)  # az start
        wpi.digitalWrite(AZ_LEFT_EN, LOW)  # Az left disable
        wpi.digitalWrite(AZ_RIGHT_EN, LOW)  # Az left disable

    def elReset(self):
        print("Called function elReset()")

        # reset everything
        wpi.digitalWrite(EL_PWM, LOW)  # el start
        wpi.digitalWrite(EL_LEFT_EN, LOW)  # el left disable
        wpi.digitalWrite(EL_RIGHT_EN, LOW)  # el left disable


def main():
    myrotate = Rotation()

    myrotate.rotate()


if __name__ == "__main__":
    main()
