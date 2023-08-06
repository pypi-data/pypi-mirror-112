from .lib import NZTMToWGS84Lib
from .tuples import NZTMCoordinates, WGS84Coordinates
from .util import NZTMUtil


def NZTMToWGS84(
    nztmCoordinates: NZTMCoordinates, unit=NZTMUtil.DEG
) -> WGS84Coordinates:
    latRad, longRad = NZTMToWGS84Lib.NZTMToGeod(
        nztmCoordinates.easting, nztmCoordinates.northing
    )
    coord = WGS84Coordinates(latitude=latRad, longitude=longRad, unit=NZTMUtil.RAD)
    if unit == NZTMUtil.DEG:
        coord = NZTMUtil.WGS84RadianToDegree(coord)
    return coord


def WGS84toNZTM(wgs64Coordinates: WGS84Coordinates, precision=2) -> NZTMCoordinates:
    if wgs64Coordinates.unit != NZTMUtil.RAD:
        wgs64Coordinates = NZTMUtil.WGS84DegreeToRadian(wgs64Coordinates)
    easting, northing = NZTMToWGS84Lib.GeodToNZTM(
        wgs64Coordinates.longitude, wgs64Coordinates.latitude
    )
    easting, northing = round(easting, precision), round(northing, precision)
    return NZTMCoordinates(easting=easting, northing=northing)
