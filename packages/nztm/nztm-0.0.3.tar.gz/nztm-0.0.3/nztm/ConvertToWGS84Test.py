import unittest
import collections

from ddt import ddt, data

# Create a format for the test data coordinates and benchmarks
from nztm import NZTMCoordinates, WGS84toNZTM, NZTMUtil, NZTMToWGS84, WGS84Coordinates

TestPair = collections.namedtuple("TestPair", ["output", "benchmark"])


@ddt
class NZTMTests(unittest.TestCase):

    # Convert some coordinates (left) to test against government conversions (right)
    # Benchmarks are generated in Degrees, Minutes, Seconds using:
    # https://www.linz.govt.nz/data/geodetic-services/coordinate-conversion/online-conversions
    # If you plan to add values, note that the site actually outputs N/S where E/W should be used and vice versa
    @data(
        NZTMCoordinates(1576041.15, 6188574.24),
        NZTMCoordinates(1576542.01, 5515331.05),
        NZTMCoordinates(1307103.22, 4826464.86),
    )
    def testTwoWayNZTMConversion(self, nztmCoordinates: NZTMCoordinates):
        eastingFailureMsg = "conversion easting is not correct to 4 decimal places"
        northingFailureMsg = "conversion northing is not correct to 2 decimal places"

        wgs64 = NZTMToWGS84(nztmCoordinates)
        wgs64 = NZTMUtil.WGS84DegreeToRadian(wgs64)
        nztmOutput = WGS84toNZTM(wgs64, precision=2)

        # Test easting
        self.assertEqual(nztmOutput.easting, nztmCoordinates.easting, eastingFailureMsg)

        # Test northing
        self.assertEqual(
            nztmOutput.northing, nztmCoordinates.northing, northingFailureMsg
        )

    @data(
        WGS84Coordinates(
            latitude=-34.39456547270398, longitude=173.01381182821413, unit=NZTMUtil.DEG
        ),
        WGS84Coordinates(
            latitude=-37.68810112626499, longitude=178.5482023374691, unit=NZTMUtil.DEG
        ),
        WGS84Coordinates(
            latitude=-46.62337904004847, longitude=168.32823626421887, unit=NZTMUtil.DEG
        ),
        WGS84Coordinates(
            latitude=-45.99840400939978, longitude=166.4511305004948, unit=NZTMUtil.DEG
        ),
    )
    def testTwoWayWGS84Conversion(self, wgs84Coordinates: WGS84Coordinates):
        nztm = WGS84toNZTM(wgs84Coordinates)
        wgs84 = NZTMToWGS84(nztm, unit=NZTMUtil.DEG)

        # Test latitude
        self.assertAlmostEqual(wgs84.latitude, wgs84Coordinates.latitude, 4)

        # Test longitude
        self.assertAlmostEqual(wgs84.longitude, wgs84Coordinates.longitude, 4)
