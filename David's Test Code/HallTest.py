#Note: This script is only for testing my hall sensor classes

from ElevationHallSensorsComplex import ElevationHallSensors
from AzimuthHallSensorsComplex import AzimuthHallSensors

azHall1 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
azHall2 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
elHall1 = [0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]
elHall2 = [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0]

ElSensor = ElevationHallSensors(EInitial=0, hall1=0, hall2=0)
AzSensor = AzimuthHallSensors(azInitial=0, hall1=0, hall2= 0)


# while (True):
#     command = int(input("Hall 1 Value: "))
#     AzSensor.sensor_one_change(command)
#     print("New Azimuth is: ", AzSensor.get_azimuth())

#     command = int(input("Hall 2 Value: "))
#     AzSensor.sensor_two_change(command)
#     print("New Azimuth is: ", AzSensor.get_azimuth())

while (True):
    command = int(input("Hall 1 Value: "))
    ElSensor.sensor_one_change(command)
    print("New Length is: ", ElSensor.get_length_a())

    command = int(input("Hall 2 Value: "))
    ElSensor.sensor_two_change(command)
    print("New Length is: ", ElSensor.get_length_a())
