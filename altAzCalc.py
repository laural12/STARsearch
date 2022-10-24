###############################################
## To run this program, first run the command
## pip install altazrange
###############################################

import AltAzRange

satellite = AltAzRange.AltAzimuthRange()
satellite.observer(46.947, 7.4442, 1387)  # Params: lat, lon, altitude
satellite.target(0, 13, 35800000)  # Params: lat, lon, altitude

print(satellite.calculate())

# Outputs: {'azimuth': 172.39, 'elevation': 35.78, 'distance': 38121332.3}
