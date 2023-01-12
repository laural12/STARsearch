import WiringPi.GPIO as GPIO


# # Set GPIO numbering mode
GPIO.setmode(GPIO.BOARD)

# Set pin 22 as an output, and set servo1 as pin 22 as PWM
GPIO.setup(22, GPIO.OUT)  # CHOOSE NEW PIN: GPIO 24
GPIO.setup(13, GPIO.OUT)  # GPIO 21
GPIO.setup(15, GPIO.OUT)  # GPIO 22
GPIO.setup(16, GPIO.OUT)  # GPIO 19
GPIO.setup(29, GPIO.OUT)  # GPIO 28
GPIO.setup(31, GPIO.OUT)  # GPIO 30
GPIO.setup(33, GPIO.OUT)  # GPIO 31
GPIO.setup(26, GPIO.OUT)  # CHOOSE NEW PIN: GPIO 25


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        GPIO.output(22, GPIO.HIGH)
