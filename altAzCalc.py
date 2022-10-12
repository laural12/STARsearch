# import numpy as np

# rxLon = 7.4442 * np.pi / 180
# rxLat = 46.947 * np.pi / 180

# satLon = 13 * np.pi / 180
# # satLat = 0

# R0 = 6370  # km
# # All geostationary satellites at approx 35800 km
# h = 3580  # km

# azRx = np.arctan((np.tan(rxLon - satLon) / np.sin(rxLat))) + 180

# elRx = np.arctan(
#     (np.cos(rxLat) * np.cos(rxLon - satLon) - (R0 / (R0 + h)))
#     / np.sqrt(1 - (np.cos(rxLat) * np.cos(rxLon - satLon)) ** 2)
# )

# print("az:", azRx * 180 / np.pi)
# print("el:", elRx * 180 / np.pi)

from AltAzRange import AltAzimuthRange

satellite = AltAzimuthRange()
satellite.observer(46.947, 7.4442, 1387)
satellite.target(0, 13, 35800000)

print(satellite.calculate())
