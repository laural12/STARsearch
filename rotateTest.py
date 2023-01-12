import sys
import time

path = "/home/odroid/.local/lib/python3.10/site-packages"
sys.path.insert(0,path)
import odroid_wiringpi as wpi

OUTPUT = 1
HIGH = 1
LOW = 0

# Set GPIO numbering mode - this means you want to use the number listed as GPIO(#number)
wpi.wiringPiSetupGpio()

# Set GPIO 24 as an output, and set servo1 as GPIO 24 as PWM
wpi.pinMode(24, OUTPUT)
wpi.pinMode(21, OUTPUT)
wpi.pinMode(22, OUTPUT)
wpi.pinMode(19, OUTPUT) 
wpi.pinMode(28, OUTPUT)
wpi.pinMode(30, OUTPUT)
wpi.pinMode(31, OUTPUT)
wpi.pinMode(25, OUTPUT)


class Rotation:
    def rotate(self):
        #### retract the linear actuator
        print("Called function rotate()")
        wpi.digitalWrite(21, LOW)
        wpi.digitalWrite(22, HIGH)
        
        
        wpi.digitalWrite(24, HIGH) # PWM to move motor
        
        #while True:
        #    time.sleep(10)
        #wpi.digitalWrite(24, LOW)
        
def main():
    myrotate = Rotation()
    
    myrotate.rotate()
    
    
if __name__ == "__main__":
    main()
