from ElevationHallSensorsComplex import ElevationHallSensors
from AzimuthHallSensorsComplex import AzimuthHallSensors

azTolerance = .1 #az tolerance in degrees
elTolerance = .1 #el tolerance in degrees

azDesired = input("What is your desired Azimuth?  ")
elDesired = input("What is your desired Elevation?  ")

#Initialize the hall sensors with initial angle values and hall sensor readings
#Note this will need to be updated
# hall1Initial = (read pin here)
# hall2Initial = (read pin here)
# azInitial = Limit switch value
# elInitial = Limit switch value

#I'm just initializing the hall sensors with all zeroes for now
AzimuthSensors = AzimuthHallSensors(az0 = 0, hall1 = 0, hall2 = 0)
ElevationSensors = ElevationHallSensors(el0 = 0, hall1 = 0, hall2 = 0)

#Calculate Errors
azError = AzimuthSensors.get_azimuth() - azDesired
elError = ElevationSensors.get_elevation_angle() - elDesired


#We need to add interrupts to update the hall sensors in here somewhere

#Control Loop
while (abs(azError) > azTolerance and abs(elError) > elTolerance):
    if (AzimuthSensors.get_azimuth() > azDesired+azTolerance):
        #turn counterclockwise
        pass
    elif (AzimuthSensors.get_azimuth() < azDesired-azTolerance):
        #turn clockwise
        pass
    else:
        #Dont move az
        pass
    if (ElevationSensors.get_elevation_angle > elDesired + elTolerance):
        #extend actuator / Lower Elevation
        pass
    elif (ElevationSensors.get_elevation_angle > elDesired + elTolerance):
        #retract actuator / Raise Elevation
        pass
    else:
        #Don't move Elevation
        pass
    #recalculate errors
    azError = AzimuthSensors.get_azimuth() - azDesired
    elError = ElevationSensors.get_elevation_angle() - elDesired
