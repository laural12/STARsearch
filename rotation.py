# import WiringPi.GPIO as GPIO


import sys
from datetime import datetime

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
    polDegreesPerVolt = maxAngle/maxVoltage
    VoltsPerADCVal = 1.8/(2**10 - 1) # about 0.00176V/ADC

    EL_LEFT_PWM = 21 # UP
    EL_RIGHT_PWM = 22 # DOWN
    AZ_LEFT_PWM = 28
    AZ_RIGHT_PWM = 30       

    # input pins
    AZ_ENC1 = 31
    # AZ_ENC2 =
    EL_ENC1 = 25
    # EL_ENC2 =
    LIMIT_ENC_AZ = 29
    LIMIT_ENC_EL = 24
    POL_LEFT_PWM = 19
    POL_RIGHT_PWM = 18
    POL_POTENTIOMETER = 0 #AIN0 ???????

    def __init__(self, GUI_test=False):
        self.GUI_test = GUI_test
        self.azTicks = 0
        self.elTicks = 0
        self.initialAz = 150.0
        self.initialEl = 0.0
       

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
            self.azHall = AzimuthHallSensors(self.initialAz, self.AZ_ENC1)
            self.elHall = ElevationHallSensors(self.initialEl, self.EL_ENC1)


    def initialize_orientation(self):
        print("Called function initialize_orientation()")
        self.azTurnLeft()
        while ()

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

        # wpi.digitalWrite(EL_ENABLE, HIGH)  # el enable
        # wpi.digitalWrite(EL_LEFT_PWM, LOW)  # el set left low
        # wpi.digitalWrite(EL_RIGHT_PWM, HIGH)  # el set right high
        
        self.elHall.set_direction(raising = True)
        
        self.elReset()
        self.elEnable()
        self.elLeftPWM()
        #self.elRightPWM()

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
        print("Called function polTurnRight()")
        self.polReset()
        self.write(self.POL_RIGHT_PWM, self.HIGH)

    def polTurnLeft(self):
        print("Called function polTurnLeft()")
        self.polReset()
        self.write(self.POL_LEFT_PWM, self.HIGH)   

    # READ FUNCTIONS
    def readLimEl(self):
        print("Called function readLimEl()")

        print("El limit switch returned:")

        return datetime.now().strftime(
            "%H:%M:%S"
        )  # FIXME: I DON'T WANT TO READ TWICE SO GET RID OF PRINT ONCE VERIFIED
        # return self.read(LIMIT_ENC_EL)

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
        
        #voltage = self.VoltsPerADCVal * wpi.analogRead(POL_POTENTIOMETER)
        #return(voltage*self.polDegreesPerVolt)
        return wpi.analogRead(self.POL_POTENTIOMETER)
        

class Rotation(RotationBase, metaclass=Singleton):
    pass

