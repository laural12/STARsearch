# THIS SCRIPT TO BE RUN THE FIRST TIME YOU INSTALL AN ANTENNA
#

import pickle

antData = {}

# PROMPT USER FOR ANTENNA NUMBER, LAT, LONG, AND ORIENT CALIBRATION
antData["antNum"] = input("What is the number of this antenna? ")
antData["lat"] = input("What is the latitude of this antenna? ")
antData["lon"] = input("What is the longitude of this antenna? ")
antData["calAz"] = input(
    "What is the azimuth calibration orientation of this antenna? "
)
antData["calEl"] = input(
    "What is the elevation calibration orientation of this antenna? "
)

with open("antConstants.pickle", "wb") as handle:
    pickle.dump(antData, handle, protocol=pickle.HIGHEST_PROTOCOL)

# with open('filename.pickle', 'rb') as handle:
#     b = pickle.load(handle)
