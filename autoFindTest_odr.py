from ElevationHallSensors import ElevationHallSensors
from AzimuthHallSensors import AzimuthHallSensors
from rotation import Rotation

azTolerance = .5 #az tolerance in degrees
elTolerance = .5 #el tolerance in degrees

azDes = float(input("What is your desired Azimuth?  "))
elDes = float(input("What is your desired Elevation?  "))

#Initialize the rotation class. This class has all the low level movement functions
#and also contains the hall sensors which store the az/el angles
myRotation = Rotation()

def autoFind(azDesired,elDesired,myRotation):
    #Calculate Errors
    azError = float(myRotation.getAzAngle()) - azDesired
    elError = float(myRotation.getElAngle()) - elDesired

    #Control Loop
    while (abs(azError) > azTolerance or abs(elError) > elTolerance):
        print("az: ", myRotation.getAzAngle())
        print("el: ", myRotation.getElAngle())
        
        if (myRotation.getAzAngle() > azDesired+azTolerance):
            #turn counterclockwise
            myRotation.azTurnLeft()
        elif (myRotation.getAzAngle() < azDesired-azTolerance):
            #turn clockwise
            myRotation.azTurnRight()

        if (myRotation.getElAngle() > elDesired + elTolerance):
            #extend actuator / Lower Elevation
            myRotation.elTurnDown()
        elif (myRotation.getElAngle() < elDesired - elTolerance):
            #retract actuator / Raise Elevation
            myRotation.elTurnUp()

        #recalculate errors
        azError = float(myRotation.getAzAngle()) - azDesired
        elError = float(myRotation.getElAngle()) - elDesired
        
    myRotation.azReset()
    myRotation.elReset()

autoFind(azDes, elDes, myRotation)

myRotation.azReset()
myRotation.elReset()
