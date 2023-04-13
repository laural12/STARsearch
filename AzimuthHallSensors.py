import numpy as np
import sys
from datetime import datetime
import threading
import time

#Python path for ODROID
path = "/home/odroid/.local/lib/python3.10/site-packages"
sys.path.insert(0, path)

#wiringpi contains the functions to read/write to pins
import odroid_wiringpi as wpi

#Azimuth hall sensor class stores the current azimuth angle and updates
#it as it recieves signals from the azimuth hall sensor
class AzimuthHallSensors:

    atLim = 132.0 # azimuth degrees when hitting limit switch
    az = 0.0 #stores current azimuth in degrees
    currentHallValue = 0.0
    previousHallValue = 0
    checkingFrequency = 200 #Hz
    pinNum = 31 #This is the GPIO number that is connected to the hall sensor output
    movingClockwise = True
    degreesPerEdgeSingleSensor = 360.0/(575.0 * 80.0 * 4.0) #Degrees per edge in a single sensor
    degreesPerHighSingleSensor = 360.0/(575.0 * 80.0 * 2.0) #Degrees per high pulse in a single sensor

    #The initialize function initializes all variables and starts a thred to read the hall sensor signal
    def __init__(self, azInitial, pinNum):
        self.az = azInitial
        self.pinNum = pinNum
        self.currentHallValue = wpi.digitalRead(self.pinNum)
        self.previousHallValue = wpi.digitalRead(self.pinNum)

        sensorThread = threading.Thread(target = self.thread_function, daemon=True)
        sensorThread.start()
        
    #This resets the azimuth angle to a given value.
    def reset(self, azInitial):
        self.az = azInitial
    
    def get_azimuth(self):
        return self.az
    
    #The thread will constantly check to see if the voltage on the pin has changed
    #If it has, it will update the azimuth value
    def thread_function(self):
        while (True):
            self.previousHallValue = self.currentHallValue
            self.currentHallValue = wpi.digitalRead(self.pinNum)
            if (self.previousHallValue != self.currentHallValue):
                if (self.movingClockwise):
                    self.az += self.degreesPerEdgeSingleSensor
                else:
                    self.az -= self.degreesPerEdgeSingleSensor
            time.sleep(1.0/self.checkingFrequency)

    def set_direction(self, clockwise):
        self.movingClockwise = clockwise
