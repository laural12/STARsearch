#initialization
  # orientation sensor
# use a compass to determine azimuth, elevation
# store heading data on power down

  # gps installation
#figure out how to get lat, long, elev from the gps

  # position data
#load antenna lat,long, elevation
lat_pr = 40.246638
long_pr = -111.646856
alt_pr = 1439 #meters
#az_ant = ?  
#el_ant = ?

# acquisition
  # user input
# Satellite to acquire
  # satellite lat, long, elev(35,786 km), polarization
  # find from a database somewhere??
  # TLE????

# calculate new az/el
    # math

# desired db threshold
  # also from a database??
  # vary w satellite

# Hall sensors
  # figure out how to read the data from teh sensors
  # if blue goes high first it is turning left/up
  # if yellow goes high first it is turning right/down
  # count number of pulses to figure how far it has moved
    # convert that to degrees moved/ elevaion change

# move az/el
  # compass data, hall sensors - inputs
  # move until compass/hall sensors are correct location
  
# focus antenna using db threshold
  # something using polarization which we dont understand???
  # do something like 30% 70% on the polarization sensors

# output: signal strength, current, heading, connected satellite
  # continuous while moving, update 1/loop
  # GUI - what library to make using?

# maintain gain
  # check every x hr?/min? to see if gain has changed
    # is it caused by atmospheric interference or drift?
      # check weather ??? is this necessary????
  # change if known gain loss is drift
  
  # repeat finding peak gain (if we dont care about other sources of loss)

# await further commands
  # sm state
  
  
  # possible sm setup
  
  """
  states:
    initializaion
    user input
    calculate
    move to calculated location
    find peak gain
    stationkeeping
    await commands
    
  Always allow for user input to restart the sm
  
  """
