import numpy as np

class AzimuthHallSensors:

    az = 0.0 #stores current azimuth in degrees
    moving_clockwise = True
    currentHallState = [0,0] #First value is hall 1, second value is hall 2
    previousHallState = [0,0] #First value is hall 1, second value is hall 2
    degreesPerEdge = 360.0/4600.0 #Degrees per change in either hall sensor

    def __init__(self, azInitial, hall1, hall2):
        self.az = azInitial
        self.currentHallState = [hall1,hall2]
        self.previousHallState = [hall1,hall2]

    def get_azimuth(self):
        return self.az

    def sensor_one_change(self, sensorOneVal):
        self.previousHallState[0] = self.currentHallState[0]
        self.previousHallState[1] = self.currentHallState[1]
        self.currentHallState[0] = sensorOneVal
        self.update_az()

    def sensor_two_change(self, sensorTwoVal):
        self.previousHallState[0] = self.currentHallState[0]
        self.previousHallState[1] = self.currentHallState[1]
        self.currentHallState[1] = sensorTwoVal
        self.update_az()

    def update_az(self):
        #Debugging
        # print("Previous: ", self.previousHallState)
        # print("Current:  ", self.currentHallState)

        if (self.currentHallState == [0,0]):
            if (self.previousHallState == [0,1]):
                self.moving_clockwise = False
                self.az -= self.degreesPerEdge
            elif (self.previousHallState == [1,0]):
                self.moving_clockwise = True
                self.az += self.degreesPerEdge

        elif (self.currentHallState == [0,1]):
            if (self.previousHallState == [1,1]):
                self.moving_clockwise = False
                self.az -= self.degreesPerEdge
            elif (self.previousHallState == [0,0]):
                self.moving_clockwise = True
                self.az += self.degreesPerEdge

        elif (self.currentHallState == [1,1]):
            if (self.previousHallState == [1,0]):
                self.moving_clockwise = False
                self.az -= self.degreesPerEdge
            elif (self.previousHallState == [0,1]):
                self.moving_clockwise = True
                self.az += self.degreesPerEdge
        
        elif (self.currentHallState == [1,0]):
            if (self.previousHallState == [0,0]):
                self.moving_clockwise = False
                self.az -= self.degreesPerEdge
            elif (self.previousHallState == [1,1]):
                self.moving_clockwise = True
                self.az += self.degreesPerEdge
        else:
            print("Azimuth Hall Sensor Error")