from nztm.lib import _MATH_CONST

from nztm.tuples import WGS84Coordinates


class NZTMUtil:
    DEG = "DEGREE"
    RAD = "RADIAN"

    @staticmethod
    def WGS84RadianToDegree(wgs84Coordinates: WGS84Coordinates):
        if wgs84Coordinates.unit == NZTMUtil.DEG:
            return wgs84Coordinates
        lat, long = (
            wgs84Coordinates.latitude * _MATH_CONST.RAD2DEG,
            wgs84Coordinates.longitude * _MATH_CONST.RAD2DEG,
        )
        return WGS84Coordinates(latitude=lat, longitude=long, unit=NZTMUtil.DEG)

    @staticmethod
    def WGS84DegreeToRadian(wgs84Coordinates: WGS84Coordinates):
        if wgs84Coordinates.unit == NZTMUtil.RAD:
            return wgs84Coordinates
        lat, long = (
            wgs84Coordinates.latitude * _MATH_CONST.DEG2RAD,
            wgs84Coordinates.longitude * _MATH_CONST.DEG2RAD,
        )
        return WGS84Coordinates(latitude=lat, longitude=long, unit=NZTMUtil.RAD)
