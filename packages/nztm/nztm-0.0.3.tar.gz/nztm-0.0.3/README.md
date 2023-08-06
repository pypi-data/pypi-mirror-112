# nztm
Geo coordinate conversion library between NZTM2000 and WGS84.

## Usage:

```
# from nztm2000 to lat/long
wgs64 = nztm.NZTMToWGS84(
        NZTMCoordinates(easting=easting, northing=northing))
# access lat/long by
lat, long = wgs64.latitude, wgs64.longitude
```
