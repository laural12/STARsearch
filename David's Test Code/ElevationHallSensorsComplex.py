import numpy as np

class ElevationHallSensors:

    a = 0. #Current length of a in inches
    a0 = 33.8 #length of a at E=3 degrees
    b = 24.75 #measured length of b
    c = 20.5 #measured length of c
    A = 0. #Current angle A in degrees
    ADesired = 0. #Desired angle A in degrees
    D = 0. #measured angle of D in degrees
    E = 0. #current elevation angle in degrees
    EDesired = 0. #desired angle of elevation in degrees
    F = 0. #measured angle F in degrees

    extending = True
    currentHallState = [0,0] #First value is hall 1, second value is hall 2
    previousHallState = [0,0] #First value is hall 1, second value is hall 2
    edgesMoved = 0.0 #sum of edges moved since initialization. Negative implies contracting, positive extending

    edgesPerInch = 9052.0 #edges per inch using two sensors

    def __init__(self, EInitial, hall1, hall2):
        
        #Calculate initial values
        self.A = 90 - EInitial - self.F + self.D
        self.a = np.sqrt(self.b**2 + self.c**2 - 2*self.b*self.c*np.cos(np.pi/180.*self.A))

        self.previousHallState = [hall1, hall2]
        self.currentHallState = [hall1, hall2]

    def get_elevation_angle(self):
        self.calculate_E()
        return self.E

    def get_length_a(self):
        self.calculate_a()
        return self.a

    def get_edges_moved(self):
        return self.edgesMoved    
    
    def calculate_E(self):
        self.calculate_A()
        self.E = 90 - self.F - self.A + self.D
    
    def calculate_A(self):
        self.calculate_a()
        self.A = 180.0/np.pi * np.arccos((self.a**2-self.b**2-self.c**2)/(-2*self.b*self.c))

    def calculate_a(self):
        self.a = self.a0 + self.edgesMoved/self.edgesPerInch

    # def find_required_A(self, EDesired):
    #     ARequired = 90 - EDesired - self.F + self.D
    #     return ARequired
    
    def find_required_a(self, EDesired):
        ARequired = 90 - EDesired - self.F + self.D
        aRequired = np.sqrt(self.b**2 + self.c**2 - 2*self.b*self.c*np.cos(np.pi/180.*ARequired))
        return aRequired

    def sensor_one_change(self, sensorOneVal):
        self.previousHallState[0] = self.currentHallState[0]
        self.previousHallState[1] = self.currentHallState[1]
        self.currentHallState[0] = sensorOneVal
        self.update_edges_moved()

    def sensor_two_change(self, sensorTwoVal):
        self.previousHallState[0] = self.currentHallState[0]
        self.previousHallState[1] = self.currentHallState[1]
        self.currentHallState[1] = sensorTwoVal
        self.update_edges_moved()

    def update_edges_moved(self):

        if (self.currentHallState == [0,0]):
            if (self.previousHallState == [0,1]):
                self.extending = False
                self.edgesMoved -= 1
            elif (self.previousHallState == [1,0]):
                self.extending = True
                self.edgesMoved += 1

        elif (self.currentHallState == [0,1]):
            if (self.previousHallState == [1,1]):
                self.extending = False
                self.edgesMoved -= 1
            elif (self.previousHallState == [0,0]):
                self.extending = True
                self.edgesMoved += 1

        elif (self.currentHallState == [1,1]):
            if (self.previousHallState == [1,0]):
                self.extending = False
                self.edgesMoved -= 1
            elif (self.previousHallState == [0,1]):
                self.extending = True
                self.edgesMoved += 1
        
        elif (self.currentHallState == [1,0]):
            if (self.previousHallState == [0,0]):
                self.extending = False
                self.edgesMoved -= 1
            elif (self.previousHallState == [1,1]):
                self.extending = True
                self.edgesMoved += 1
        else:
            print("Elevation Hall Sensor Error")