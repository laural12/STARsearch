from ElevationHallSensors import ElevationHallSensors
from AzimuthHallSensors import AzimuthHallSensors
from rotation import Rotation

azTolerance = .1 #az tolerance in degrees
elTolerance = .1 #el tolerance in degrees

azDes = input("What is your desired Azimuth?  ")
elDes = input("What is your desired Elevation?  ")

#Initialize the rotation class. This class has all the low level movement functions
#and also contains the hall sensors which store the az/el angles
myRotation = Rotation()

def autoFind(azDesired,elDesired,myRotation):
    #Calculate Errors
    azError = myRotation.getAzAngle() - azDesired
    elError = myRotation.getElAngle() - elDesired

    #Control Loop
    while (abs(azError) > azTolerance and abs(elError) > elTolerance):
        if (myRotation.getAzAngle() > azDesired+azTolerance):
            #turn counterclockwise
            myRotation.azTurnLeft
        elif (myRotation.getAzAngle()() < azDesired-azTolerance):
            #turn clockwise
            myRotation.azTurnRight

        if (myRotation.getElAngle() > elDesired + elTolerance):
            #extend actuator / Lower Elevation
            myRotation.elTurnUp()
        elif (myRotation.getElAngle() > elDesired + elTolerance):
            #retract actuator / Raise Elevation
            myRotation.elTurnDown()

        #recalculate errors
        azError = myRotation.getAzAngle() - azDesired
        elError = myRotation.getElAngle() - elDesired

autoFind(azDes, elDes, myRotation)
