###############################################
## To run this program, first run the command
## pip install altazrange
###############################################

from re import A
import AltAzRange

satellite = AltAzRange.AltAzimuthRange()

prompt_input = True

# Default values. If you want to change values directly in this file, change them here and set prompt_input = False
ob_lat, ob_lon, ob_alt = 0.0, 0.0, 0.0
sat_lat, sat_lon, sat_alt = 0.0, 0.0, 0.0

if prompt_input:
    # Take input
    ob_lat, ob_lon, ob_alt = [float(x) for x in input("Enter latitude, longitude, altitude of observer as comma-space-separated list: ").split(", ")]
    sat_lat, sat_lon, sat_alt = [float(x) for x in input("Enter latitude, longitude, altitude of satellite as comma-space-separated list: ").split(", ")]

satellite.observer(ob_lat, ob_lon, ob_alt)  # Params: lat, lon, altitude
satellite.target(sat_lat, sat_lon, sat_alt)  # Params: lat, lon, altitude

output = satellite.calculate()

# Hard-coded - if all lat/lon are zero, the above code will produce "None" for the angles. We correct this here
if ob_lat == 0.0 and ob_lat == 0.0 and ob_lat == 0.0 and ob_lat == 0.0:
    output["azimuth"] = 0.0
    output["elevation"] = 90.0

print("\n", output)

# Inputs: 46.947, 7.4442, 1387 and 0, 13, 35800000
# Outputs: {'azimuth': 172.39, 'elevation': 35.78, 'distance': 38121332.3}
