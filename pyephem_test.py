#%% Basic setup
# To run, do
# pip install ephem
# pip install skyfield

#############################################
## Using ephem
#############################################
import ephem
from skyfield.api import load, wgs84

m = ephem.Mars("1970")
print(ephem.constellation(m))
# Prints: ('Aqr', 'Aquarius')

#%%
line1 = "ISS (ZARYA)"
line2 = "1 25544U 98067A   03097.78853147  .00021906  00000-0  28403-3 0  8652"
line3 = "2 25544  51.6361  13.7980 0004256  35.6671  59.2566 15.58778559250029"
iss = ephem.readtle(line1, line2, line3)

iss.compute(
    "2003/3/23"
)  # Note the epoch - the date on which an element set is most accurate. It will go rapidly out of date
print("%s %s" % (iss.sublong, iss.sublat))


#%%
############################################################
## Using skyfield API
############################################################

# Where to get TLE's from? Can download from multiple places
# Example: celestrak from skyfield
active_sats_url = (
    "http://celestrak.com/NORAD/elements/active.txt"  # active satellites at active.txt
)
satellites = load.tle_file(active_sats_url)
print("Loaded", len(satellites), "satellites")

# Build a dictionary of the satellites so we can access individual ones easily
by_name = {sat.name: sat for sat in satellites}
satellite = by_name["GALAXY 16 (G-16)"]
print("satellite:", satellite)

# Get current time
ts = load.timescale()
t = ts.now()

# Print its position
geocentric = satellite.at(t)
print(geocentric.position.km)

# Convert to lat/lon
lat, lon = wgs84.latlon_of(geocentric)
print("Latitude:", lat)
print("Longitude:", lon)

# %%
