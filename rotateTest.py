import sys
import time

path = "/home/odroid/.local/lib/python3.10/site-packages"
sys.path.insert(0, path)
# import odroid_wiringpi as wpi

OUTPUT = 1
HIGH = 1
LOW = 0

EL_MOVE = 24
EL_LEFT_EN = 21
EL_RIGHT_EN = 22
AZ_MOVE = 19
AZ_LEFT_EN = 28
AZ_RIGHT_EN = 30

# Set GPIO numbering mode - this means you want to use the number listed as GPIO(#number)
# wpi.wiringPiSetupGpio()

# # Set GPIO 24 as an output, and set servo1 as GPIO 24 as PWM
# wpi.pinMode(24, OUTPUT)  # Move El motor
# wpi.pinMode(21, OUTPUT)  # El left enable
# wpi.pinMode(22, OUTPUT)  # El right enable
# wpi.pinMode(19, OUTPUT)  # Move Az motor
# wpi.pinMode(28, OUTPUT)  # Az left enable
# wpi.pinMode(30, OUTPUT)  # Az right enable
# wpi.pinMode(31, OUTPUT)
# wpi.pinMode(25, OUTPUT)


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        # wpi.digitalWrite(EL_LEFT_EN, LOW)
        # wpi.digitalWrite(EL_RIGHT_EN, HIGH)

        # wpi.digitalWrite(EL_MOVE, HIGH)  # PWM to move motor

        # while True:
        #    time.sleep(10)
        # wpi.digitalWrite(24, LOW)

    def azLeftEn(self):
        print("Called function azLeftEn()")
        # wpi.digitalWrite(AZ_LEFT_EN, HIGH)  # Az left enable

    def azRightEn(self):
        print("Called function azRightEn()")
        # wpi.digitalWrite(AZ_RIGHT_EN, HIGH)  # Az right enable

    def elLeftEn(self):
        print("Called function elLeftEn()")
        # wpi.digitalWrite(EL_LEFT_EN, HIGH)  # El left enable

    def elRightEn(self):
        print("Called function elRightEn()")
        # wpi.digitalWrite(EL_RIGHT_EN, HIGH)  # El right enable

    def azStart(self):
        print("Called function azStart()")
        # wpi.digitalWrite(AZ_MOVE, HIGH)  # az start

    def elStart(self):
        print("Called function elStart()")
        # wpi.digitalWrite(EL_MOVE, HIGH)  # El start

    def azStop(self):
        print("Called function azStop()")

        # reset everything
        # wpi.digitalWrite(AZ_MOVE, LOW)  # az start
        # wpi.digitalWrite(AZ_LEFT_EN, LOW)  # Az left disable
        # wpi.digitalWrite(AZ_RIGHT_EN, LOW)  # Az left disable

    def azStop(self):
        print("Called function elStop()")

        # reset everything
        # wpi.digitalWrite(EL_MOVE, LOW)  # el start
        # wpi.digitalWrite(EL_LEFT_EN, LOW)  # el left disable
        # wpi.digitalWrite(EL_RIGHT_EN, LOW)  # el left disable


def main():
    myrotate = Rotation()

    myrotate.rotate()


if __name__ == "__main__":
    main()
