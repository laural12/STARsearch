#####################################################################
## NOTE: To generate docstring HTML documentation for this file, type 
##          python3 -m pydoc -w pseudocode
## into the command line. (I only tested with a linux command line, 
## it might also work with windows.)
#####################################################################

import AltAzRange
  # gps installation
#figure out how to get lat, long, elev from the gps - maybe can be manually loaded on installation

  # position data
#load antenna lat,long, elevation
lat_pr = 40.246638
long_pr = -111.646856
alt_pr = 1439 #meters
az_ant = 0
el_ant = 0

# acquisition
  # user input
def ui(satellite, antenna, threshold):
  """This function receives interactions from the user and calls all the rest of the code"""
  #initialization
  # orientation sensor
  # use a compass to determine azimuth, elevation
  # store heading data on power down  
  orient()
  #acquire new satellite
  acquire(satellite, antenna, threshold)
  # output: signal strength, current, heading, connected satellite
  # continuous while moving, update 1/loop
  # GUI - what library to make using?
  maintain()


def getLat(TLE):
  """Uses TLE to get latitude of the satellite"""

def getLong(TLE):
  """Uses TLE to get longitude of the satellite"""

def acquire(TLE, antenna, threshold):
  """acquires and focuses in on new antenna"""
  latSat = getLat(TLE)
  longSat = getLong(TLE)
  # Satellite to acquire
    # satellite lat, long, elev(35,786 km), polarization
    # find from a database somewhere??
    # TLE????
  orient = getNewOrientation(latSat,longSat)

  move(findShortestAngle(az_ant - orient["azimuth"]), el_ant - orient["elevation"])
  polarization()
  focus()

def findShortestAngle(angle):
  """ Finds angle between -180 and 180 to turn to achieve desired angle. EX: findShortestAngle(270) returns -90 """
  if (angle > 180):
    angle = angle -360
  elif (angle < -180):
    angle = angle + 360
  return angle

def orient():
  """orients itself, saves as global variables"""
  global az_ant, el_ant
  az_ant = 0#antenna azimuth
  el_ant = 0#antenna elevation

def getNewOrientation(latSat,longSat):
  """uses AltAzRange to calculate the new orientation for the antenna"""
  satellite = AltAzRange.AltAzimuthRange()
  satellite.observer(lat_pr,long_pr,alt_pr)
  satellite.target(latSat, longSat, 35786000)
  # calculate new az/el
      # math
  return satellite.calculate()#orient is a dictionary

# desired db threshold
  # also from a database??
  # vary w satellite

# Hall sensors
  # figure out how to read the data from teh sensors
  # if blue goes high first it is turning left/up
  # if yellow goes high first it is turning right/down
  # count number of pulses to figure how far it has moved
    # convert that to degrees moved/ elevaion change

def move(az, el):
  """moves actuators to the right place - only rough moving"""
# move az/el
  # compass data, hall sensors - inputs
  # move until compass/hall sensors are correct location
  moveAz(az)
  moveEl(el)

def moveAz(az):
  """moves slew drive"""

def moveEl(el):
  """moves linear actuator"""
  
def focus():
  """focuses antenna on the satellite"""
# focus antenna using db threshold

def polarization():
  """matches polarization to the satellite"""
  # something using polarization which we dont understand???
  # do something like 30% 70% on the polarization sensors

def maintain():
  """maintains gain by constantly focusing in on peak or threshold, awaits further commands"""
  # maintain gain
    # check every x hr?/min? to see if gain has changed
      # is it caused by atmospheric interference or drift?
        # check weather ??? is this necessary????
    # change if known gain loss is drift

    #maybe repeat focus()
  focus()
    
    # repeat finding peak gain (if we dont care about other sources of loss)

  # await further commands
    # sm state
  if (furtherCommand):
    ui(TLE, antenna, dB)
  
  
  # possible sm setup
  

  '''states:
    initializaion
    user input
    calculate
    move to calculated location
    find peak gain
    stationkeeping
    await commands
    
  Always allow for user input to restart the sm'''
