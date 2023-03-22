import numpy as np
import sys
from datetime import datetime
import threading
import time

path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi

class ElevationHallSensors:

    a = 0. #Current length of a in inches
    b = 24.67 #measured length of b
    c = 20.65 #measured length of c
    A = 0. #Current angle A in degrees
    ADesired = 0. #Desired angle A in degrees
    DminusF = 4.73
    #D = 0. #measured angle of D in degrees
    E = 0. #current elevation angle in degrees
    EDesired = 0. #desired angle of elevation in degrees
    #F = 0. #measured angle F in degrees

    raising = True
    currentHallValue = 0
    previousHallValue = 0
    pulsesPerInch = 2263.0
    inchesPerEdge = 1.0/(2.0*pulsesPerInch) #edges per inch using one sensor
    pinNum = 25
    checkingFrequency = 1000.0

    def __init__(self, EInitial, pinNum):
        
        #Calculate initial values
        self.E = EInitial
        self.A = 90 - EInitial + self.DminusF
        self.a = np.sqrt(self.b**2 + self.c**2 - 2*self.b*self.c*np.cos(np.pi/180.*self.A))

        self.pinNum = pinNum
        self.currentHallValue = wpi.digitalRead(self.pinNum)
        self.previousHallValue = wpi.digitalRead(self.pinNum)

        sensorThread = threading.Thread(target = self.thread_function, daemon=True)
        sensorThread.start()

    def thread_function(self):
        while (True):
            self.previousHallValue = self.currentHallValue
            self.currentHallValue = wpi.digitalRead(self.pinNum)
            if (self.previousHallValue != self.currentHallValue):
                if (self.raising):
                    self.a -= self.inchesPerEdge
                else:
                    self.a += self.inchesPerEdge
            time.sleep(1.0/self.checkingFrequency)
    
    def get_elevation_angle(self):
        self.calculate_E()
        return self.E

    def get_length_a(self):
        return self.a
    
    def calculate_E(self):
        self.calculate_A()
        self.E = 90 - self.A + self.DminusF
    
    def calculate_A(self):
        self.A = 180.0/np.pi * np.arccos((self.a**2-self.b**2-self.c**2)/(-2*self.b*self.c))
    
    def find_required_a(self, EDesired):
        ARequired = 90 - EDesired + self.DminusF
        aRequired = np.sqrt(self.b**2 + self.c**2 - 2.0*self.b*self.c*np.cos(np.pi/180.*ARequired))
        return aRequired
        
    def set_direction(self, raising):
        self.raising = raising
