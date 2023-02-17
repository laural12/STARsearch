import sys
from datetime import datetime
import time
import threading

path = "/home/odroid/.local/lib/python3.10/site-packages"
# path = "/home/laura/.local/lib/python3.8/site-packages"
sys.path.insert(0, path)
import odroid_wiringpi as wpi

wpi.wiringPiSetupGpio()

# input pins
AZ_ENC1 = 31
i = 0
current_val = wpi.digitalRead(AZ_ENC1)

def azTickCounter():
    print ("here")
    
def azTickCounter2():
    print ("here2")

def threadFunction():
    current_val = wpi.digitalRead(AZ_ENC1)
    old_val = current_val
    i = 0
    
    while(True):
        time.sleep(.1)
        old_val = current_val
        current_val = wpi.digitalRead(AZ_ENC1)
        if (current_val != old_val):
            i += 1
            print("i is: ", i)
        

#wpi.pinMode(AZ_ENC1, 1)
wpi.pinMode(AZ_ENC1, 0)

x = threading.Thread(target = threadFunction)
x.start()

#wpi.wiringPiISR(AZ_ENC1, wpi.INT_EDGE_RISING, azTickCounter)
while (True):
    time.sleep(1)
    #print(wpi.digitalRead(AZ_ENC1))
    #print("i is: ", i)
