import numpy as np
import sys
from datetime import datetime
import threading
import time


path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi

class AzimuthHallSensors:

    az = 0.0 #stores current azimuth in degrees
    currentHallValue = 0
    previousHallValue = 0
    checkingFrequency = 200 #Hz
    pinNum = 31
    movingClockwise = True
    degreesPerEdgeSingleSensor = 360.0/(575.0 * 80.0 * 4.0) #Degrees per edge in a single sensor
    degreesPerHighSingleSensor = 360.0/(575.0 * 80.0 * 2.0) #Degrees per high pulse in a single sensor

    def __init__(self, azInitial, pinNum):
        self.az = azInitial
        self.pinNum = pinNum
        self.currentHallValue = wpi.digitalRead(self.pinNum)
        self.previousHallValue = wpi.digitalRead(self.pinNum)

        sensorThread = threading.Thread(target = self.thread_function, daemon=True)
        sensorThread.start()

    def get_azimuth(self):
        return self.az

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
