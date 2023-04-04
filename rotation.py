# import WiringPi.GPIO as GPIO

import numpy as np
import time
import sys
import pickle
from datetime import datetime

from fieldFox import FieldFox
ff = FieldFox()

path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi
from AzimuthHallSensors import AzimuthHallSensors
from ElevationHallSensors import ElevationHallSensors

GUI_TEST = True


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RotationBase:
    INPUT = 0
    OUTPUT = 1
    HIGH = 1
    LOW = 0

    maxAngle = 360.0 #Unknown needs calibration
    maxVoltage = 1.8 #Assumed
    azTolerance = 0.05
    elTolerance = 0.05
    polDegreesPerVolt = 180.0/.424
    polDegOffset = -112.0
    VoltsPerADCVal = .424/(1580.0-606.0) # about 0.00176V/ADC

    EL_LEFT_PWM = 21 # UP
    EL_RIGHT_PWM = 22 # DOWN
    AZ_LEFT_PWM = 28
    AZ_RIGHT_PWM = 30
    POL_RIGHT_PWM = 19
    POL_LEFT_PWM = 18
    POL_POTENTIOMETER = 0 #AIN0 ???????      

    # input pins
    AZ_ENC1 = 31
    # AZ_ENC2 =
    EL_ENC1 = 25
    # EL_ENC2 =
    LIMIT_ENC_AZ = 29
    LIMIT_ENC_EL = 24

    def __init__(self, GUI_test=False):
        self.GUI_test = GUI_test
        self.azTicks = 0
        self.elTicks = 0
        self.azOfAzLimitSwitch = 133.5 # 134.5
        self.elOfElLimitSwitch = 12.65 # 12.85
        self.azOfElLimitSwitch = 168.47 # 169.47
        self.avgDeg = 0.0
        self.volts=0.0
        self.ADC = 0.0
        self.isRunning = False
       

        if not self.GUI_test:
            # Set GPIO numbering mode
            wpi.wiringPiSetupGpio()

            #Set output pins
            wpi.pinMode(self.EL_LEFT_PWM, self.OUTPUT)  # GPIO 21
            wpi.pinMode(self.EL_RIGHT_PWM, self.OUTPUT)  # GPIO 22
            wpi.pinMode(self.AZ_LEFT_PWM, self.OUTPUT)  # GPIO 28
            wpi.pinMode(self.AZ_RIGHT_PWM, self.OUTPUT)  # GPIO 30
            wpi.pinMode(self.POL_LEFT_PWM, self.OUTPUT)  # GPIO 19
            wpi.pinMode(self.POL_RIGHT_PWM, self.OUTPUT)  # GPIO 18
            
            #Initializing Hall Sensors
            with open('currOrient.pickle', 'rb') as handle:
                currOrient = pickle.load(handle)
                
            self.azHall = AzimuthHallSensors(currOrient["az"], self.AZ_ENC1)
            self.elHall = ElevationHallSensors(currOrient["el"], self.EL_ENC1)


    def initialize_orientation(self):
        print("Called function initialize_orientation()")
        
        #Turn left until hitting limit switch
        self.azTurnLeft()
        while (self.readLimAz() == 0):
            print("turning left until limit switch")
            #pass

        #Stop after hitting limit switch and reset az encoder
        self.azReset()
        self.azHall.reset(self.azOfAzLimitSwitch)
        
        #Turn right until reaching elevation limit switch azimuth
        self.azTurnRight()
        while(self.getAzAngle() < self.azOfElLimitSwitch):
            print("turning right to el limit switch")
        self.azReset()
        
        #Turn down until hitting el limit switch
        self.elTurnDown()
        while(self.readLimEl() == 0):
            print("Turning down")
        #Stop hall sensors and reinitialize limit switch
        self.elReset()
        self.elHall.reset(self.elOfElLimitSwitch)
    
    def autoFind(self, azDesired, elDesired):
        #Calculate Errors
        azError = self.getAzAngle() - azDesired
        elError = self.getElAngle() - elDesired

        try:
            #Control Loop
            while (abs(azError) > self.azTolerance or abs(elError) > self.elTolerance):
                print("Angles")
                print(self.getAzAngle())
                print(self.getElAngle())
                if (self.getAzAngle() > azDesired + self.azTolerance):
                    #turn counterclockwise
                    self.azTurnLeft()
                elif (self.getAzAngle() < azDesired-self.azTolerance):
                    #turn clockwise
                    self.azTurnRight()
                else:
                    self.azReset()

                if (self.getElAngle() < elDesired - self.elTolerance):
                    #extend actuator / Lower Elevation
                    self.elTurnUp()
                elif (self.getElAngle() > elDesired + self.elTolerance):
                    #retract actuator / Raise Elevation
                    self.elTurnDown()
                else:
                    self.elReset()

                #recalculate errors
                azError = self.getAzAngle() - azDesired
                elError = self.getElAngle() - elDesired
            
            self.azReset()
            self.elReset()
        
        except KeyboardInterrupt:
            self.azReset()
            self.elReset()

    def write(self, pinNum, writeVal):
        if not self.GUI_test:
            wpi.digitalWrite(pinNum, writeVal)

    def read(self, pinNum):
        if not self.GUI_test:
            return wpi.digitalRead(pinNum)
        else:
            return None

    def azLeftPWM(self):
        print("Called function azLeftPWM()")
        # wpi.digitalWrite(AZ_LEFT_PWM, HIGH)  # Az left PWM
        self.write(self.AZ_LEFT_PWM, self.HIGH)

    def azRightPWM(self):
        print("Called function azRightPWM()")
        # wpi.digitalWrite(AZ_RIGHT_PWM, HIGH)  # Az right PWM
        self.write(self.AZ_RIGHT_PWM, self.HIGH)

    def elLeftPWM(self):
        print("Called function elLeftPWM()")
        # wpi.digitalWrite(self.EL_LEFT_PWM, self.HIGH)  # El left PWM
        self.write(self.EL_LEFT_PWM, self.HIGH)

    def elRightPWM(self):
        print("Called function elRightPWM()")
        # wpi.digitalWrite(EL_RIGHT_PWM, HIGH)  # El right PWM
        self.write(self.EL_RIGHT_PWM, self.HIGH)

    def azReset(self):
        print("Called function azReset()")

        # reset everything
        # wpi.digitalWrite(AZ_ENABLE, LOW)  # az disable
        # wpi.digitalWrite(AZ_LEFT_PWM, LOW)  # Az left disable
        # wpi.digitalWrite(AZ_RIGHT_PWM, LOW)  # Az right disable
        #self.write(self.AZ_ENABLE, self.LOW)
        self.write(self.AZ_LEFT_PWM, self.LOW)
        self.write(self.AZ_RIGHT_PWM, self.LOW)

    def elReset(self):
        print("Called function elReset()")

        # reset everything
        # wpi.digitalWrite(EL_ENABLE, LOW)  # el start
        # wpi.digitalWrite(EL_LEFT_PWM, LOW)  # el left disable
        # wpi.digitalWrite(EL_RIGHT_PWM, LOW)  # el right disable
        #self.write(self.EL_ENABLE, self.LOW)  # el start
        self.write(self.EL_LEFT_PWM, self.LOW)  # el left disable
        self.write(self.EL_RIGHT_PWM, self.LOW)  # el right disable

    def elTurnUp(self):
        print("Called function elTurnUp()")
        
        self.elHall.set_direction(raising = True)
        self.elReset()

        self.elLeftPWM()


    def elTurnDown(self):
        print("Called function elTurnDown()")
        self.elHall.set_direction(raising = False)
        self.elReset()
        self.elRightPWM()


    def azTurnRight(self):
        print("Called function azTurnRight()")        
        self.azHall.set_direction(clockwise = True) 
        self.azReset()
        self.azRightPWM()

    def azTurnLeft(self):
        print("Called function azTurnLeft()")
        self.azHall.set_direction(clockwise = False)
        self.azReset()
        self.azLeftPWM()

    def polReset(self):
        print("Called function polReset()")

        self.write(self.POL_LEFT_PWM, self.LOW)  # el left disable
        self.write(self.POL_RIGHT_PWM, self.LOW)  # el right disable

    def polTurnRight(self):
        self.polReset()
        print("Called function polTurnRight()")
        self.write(self.POL_RIGHT_PWM, self.HIGH)

    def polTurnLeft(self):
        self.polReset()
        print("Called function polTurnLeft()")
        self.write(self.POL_LEFT_PWM, self.HIGH)   

    # READ FUNCTIONS
    def readLimEl(self):
        #print("Called function readLimEl()")

        #print("El limit switch returned:")

        #return datetime.now().strftime(
        #    "%H:%M:%S"
        #)  # FIXME: I DON'T WANT TO READ TWICE SO GET RID OF PRINT ONCE VERIFIED
        return self.read(self.LIMIT_ENC_EL)

    def readLimAz(self):
        # print("Called function readLimAz()")

        # print("Az limit switch returned:")
        # print(self.read(LIMIT_ENC_AZ))

        # return datetime.now().strftime("%H:%M:%S")
        return self.read(self.LIMIT_ENC_AZ)

    def azTickCounter(self):
        print("here")
        self.azTicks += 1

    def elTickCounter(self):
        self.elTicks += 1

    def getAzAngle(self):
        return (
            self.azHall.get_azimuth()
            #self.read(self.AZ_ENC1)
        )  # FIXME: IN THE END WE WANT TO DISPLAY SOMETHING MORE MEANINGFUL

    def getElAngle(self):
        return (
            self.elHall.get_elevation_angle()
        )  # FIXME: IN THE END WE WANT TO DISPLAY SOMETHING MORE MEANINGFUL
    
    def getPolAngle(self):
        alpha = 0.995
        
        adc = wpi.analogRead(self.POL_POTENTIOMETER)
        voltage = self.VoltsPerADCVal * wpi.analogRead(self.POL_POTENTIOMETER)
        degrees = (voltage*self.polDegreesPerVolt)
        
        self.avgDeg = (1 - alpha) * degrees + alpha * self.avgDeg
        self.volts = (1 - alpha) * voltage + alpha * self.volts
        self.ADC = (1 - alpha) * adc + alpha * self.ADC
        
        return self.avgDeg + self.polDegOffset
        #return wpi.analogRead(self.POL_POTENTIOMETER)
    
    def autoPeak(self, freq):
        # First make sure we look at the right freq
        ff.setCenterFreq(freq)
    
        # Maximize power over azimuth
        # Might instead want a certain window size - related to time it takes to move x degrees?
        initAz = self.getAzAngle()
        

        windSize = 10
        window = np.repeat(0.0, windSize)
        pwrLevels = np.array([])
        azAngles = np.array([])
        print(f"az angle: {self.getAzAngle()}")
        self.azTurnRight()  # Clockwise is positive
        while self.getAzAngle() < initAz + ff.azWindow:
            # Exponential weighted moving average - higher alpha means the average is more resistant to change
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = ff.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            azAngles = np.append(
                azAngles, self.getAzAngle()
            )  # and record corresponding azimuth angle

        print(f"az angle: {self.getAzAngle()}")
        self.azTurnLeft()  # CCW is negative
        
        while self.getAzAngle() > initAz - ff.azWindow:
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = ff.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            azAngles = np.append(
                azAngles, self.getAzAngle()
            )  # and record corresponding azimuth angle

        print(f"max pwr: {np.max(pwrLevels)}")
        print(f"len pwrLevels = {len(pwrLevels)}")
        bestAz = azAngles[np.argmax(pwrLevels[11:]) + 11]
        print(f"best az angle: {bestAz}")
        self.azTurnRight()
        while self.getAzAngle() < bestAz:
            time.sleep(
                0.001
            )  # 0.5*(1/64) = .0078 second resolution on the azimuth hall sensors
        self.azReset()

        # Now maximize power over elevation
        initEl = self.getElAngle()
        

        windSize = 10
        window = np.repeat(0.0, windSize)
        pwrLevels = np.array([])
        elAngles = np.array([])
        print(f"el angle: {self.getElAngle()}")
        self.elTurnUp()  # Up is positive
        while self.getElAngle() < initEl + ff.elWindow:
            # Exponential weighted moving average - higher alpha means the average is more resistant to change
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = ff.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            elAngles = np.append(
                elAngles, self.getElAngle()
            )  # and record corresponding azimuth angle

        print(f"el angle: {self.getElAngle()}")
        self.elTurnDown()  # Down is negative
        while self.getElAngle() > initEl - ff.elWindow:
            # self.powerLevel = (1 - self.alpha) * self.readSig() + self.alpha * self.powerLevel
            window[:-1] = window[1:]
            window[-1] = ff.readSig()

            # Record average power at this level
            pwrLevels = np.append(pwrLevels, np.mean(window))
            elAngles = np.append(
                elAngles, self.getElAngle()
            )  # and record corresponding azimuth angle

        print(f"max pwr: {np.max(pwrLevels)}")
        print(f"len pwrLevels = {len(pwrLevels)}")
        bestEl = elAngles[np.argmax(pwrLevels[11:]) + 11]
        print(f"best el angle: {bestEl}")
        self.elTurnUp()
        while self.getElAngle() < bestEl:
            time.sleep(
                0.001
            )  # 0.5*(1/184) = .0027 second resolution on the elevation hall sensors
            
        self.elReset()
        
        print(f"power: {ff.readSig()}")
        
    def getChPower(self):
        return ff.readSig()
        
    def autoPol(self, expectedPol):
        # ----------------- This section only uses math -----------------------------
        polTolerance = 1 # degrees
        if self.getPolAngle() > expectedPol + polTolerance:
            self.polTurnLeft()
            while self.getPolAngle() > expectedPol + polTolerance:
                # print(self.getPolAngle())
                time.sleep(
                    0.01
                )  # Change the time sleeping to increase resolution. Replace with "pass" for best resolution
        else:
            self.polTurnRight()
            while self.getPolAngle() < expectedPol - polTolerance:
                # print(self.getPolAngle())
                time.sleep(
                    0.01
                )  # Change the time sleeping to increase resolution. Replace with "pass" for best resolution
                
        self.polReset()

        

class Rotation(RotationBase, metaclass=Singleton):
    pass

