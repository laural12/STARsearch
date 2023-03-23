from ElevationHallSensors import ElevationHallSensors
from AzimuthHallSensors import AzimuthHallSensors
from rotation import Rotation

azTolerance = .1 #az tolerance in degrees
elTolerance = .1 #el tolerance in degrees

azDes = float(input("What is your desired Azimuth?  "))
elDes = float(input("What is your desired Elevation?  "))

#Initialize the rotation class. This class has all the low level movement functions
#and also contains the hall sensors which store the az/el angles
myRotation = Rotation()

def autoFind(azDesired,elDesired,myRotation):
    #Calculate Errors
    azError = float(myRotation.getAzAngle()) - azDesired
    elError = float(myRotation.getElAngle()) - elDesired
    
    
    try:

        #Control Loop
        while (abs(azError) > azTolerance or abs(elError) > elTolerance):
            print("Angles")
            print(myRotation.getAzAngle())
            print(myRotation.getElAngle())
            if (myRotation.getAzAngle() > azDesired+azTolerance):
                #turn counterclockwise
                myRotation.azTurnLeft()
            elif (myRotation.getAzAngle() < azDesired-azTolerance):
                #turn clockwise
                myRotation.azTurnRight()
            else:
                myRotation.azReset()

            if (myRotation.getElAngle() < elDesired - elTolerance):
                #extend actuator / Lower Elevation
                myRotation.elTurnUp()
            elif (myRotation.getElAngle() > elDesired + elTolerance):
                #retract actuator / Raise Elevation
                myRotation.elTurnDown()
            else:
                myRotation.elReset()

            #recalculate errors
            azError = float(myRotation.getAzAngle()) - azDesired
            elError = float(myRotation.getElAngle()) - elDesired
            
        myRotation.azReset()
        myRotation.elReset()
        
    except KeyboardInterrupt:
        myRotation.azReset()
        myRotation.elReset()

autoFind(azDes, elDes, myRotation)
