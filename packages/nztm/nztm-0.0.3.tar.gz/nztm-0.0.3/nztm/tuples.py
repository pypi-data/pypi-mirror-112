from collections import namedtuple

WGS84Coordinates = namedtuple("WGS84Coordinates", ("latitude", "longitude", "unit"))
NZTMCoordinates = namedtuple("NZTMCoordinates", ("easting", "northing"))
