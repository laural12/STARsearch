###############################################
## To run this program, first run the command
## pip install altazrange
###############################################

from AltAzRange import AltAzimuthRange

satellite = AltAzimuthRange()
satellite.observer(46.947, 7.4442, 1387)
satellite.target(0, 13, 35800000)

print(satellite.calculate())
