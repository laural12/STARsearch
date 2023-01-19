import WiringPi.GPIO as GPIO


# import sys
# import time

# path = "/home/odroid/.local/lib/python3.10/site-packages"
# sys.path.insert(0, path)
# # import odroid_wiringpi as wpi


OUTPUT = 1
HIGH = 1
LOW = 0

EL_PWM = 22
EL_LEFT_EN = 13
EL_RIGHT_EN = 15
AZ_PWM = 16
AZ_LEFT_EN = 29
AZ_RIGHT_EN = 31
FILLER_1 = 33
FILLER_2 = 26

# # Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 22 as an output, and set servo1 as pin 22 as PWM
GPIO.setup(EL_PWM, GPIO.OUT)  # CHOOSE NEW PIN: GPIO 24
GPIO.setup(EL_LEFT_EN, GPIO.OUT)  # GPIO 21
GPIO.setup(EL_RIGHT_EN, GPIO.OUT)  # GPIO 22
GPIO.setup(AZ_PWM, GPIO.OUT)  # GPIO 19
GPIO.setup(AZ_LEFT_EN, GPIO.OUT)  # GPIO 28
GPIO.setup(AZ_RIGHT_EN, GPIO.OUT)  # GPIO 30
GPIO.setup(FILLER_1, GPIO.OUT)  # GPIO 31
GPIO.setup(FILLER_2, GPIO.OUT)  # CHOOSE NEW PIN: GPIO 25


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        # wpi.digitalWrite(EL_LEFT_EN, LOW)
        # wpi.digitalWrite(EL_RIGHT_EN, HIGH)

        # wpi.digitalWrite(EL_PWM, HIGH)  # PWM to move motor

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
        # wpi.digitalWrite(AZ_PWM, HIGH)  # az start

    def elStart(self):
        print("Called function elStart()")
        # wpi.digitalWrite(EL_PWM, HIGH)  # El start

    def azStop(self):
        print("Called function azStop()")

        # reset everything
        # wpi.digitalWrite(AZ_PWM, LOW)  # az start
        # wpi.digitalWrite(AZ_LEFT_EN, LOW)  # Az left disable
        # wpi.digitalWrite(AZ_RIGHT_EN, LOW)  # Az left disable

    def azStop(self):
        print("Called function elStop()")

        # reset everything
        # wpi.digitalWrite(EL_PWM, LOW)  # el start
        # wpi.digitalWrite(EL_LEFT_EN, LOW)  # el left disable
        # wpi.digitalWrite(EL_RIGHT_EN, LOW)  # el left disable


def main():
    myrotate = Rotation()

    myrotate.rotate()


if __name__ == "__main__":
    main()
