import numpy as np
a = 0. #Current length of a in inches
a0 = 33.8 #length of a at E=3 degrees
b = 24.75 #measured length of b
c = 20.5 #measured length of c
A = 55. #Current angle A in degrees
ADesired = 0. #Desired angle A in degrees
D = 0. #measured angle of D in degrees
E = 3. #current elevation angle in degrees
EDesired = 0. #desired angle of elevation in degrees
F = 0. #measured angle F in degrees
C = 55

#Find D-F
DminusF = A+E-90
print("DminusF: ", DminusF)

AHorizontal = 90 - 0 + DminusF
print("AHorizontal: ", AHorizontal)

ARequired = 58
aRequired = np.sqrt(b**2 + c**2 - 2*b*c*np.cos(np.pi/180.0 * ARequired))
print("a Required: ", aRequired)