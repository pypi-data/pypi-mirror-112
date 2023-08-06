import math


class _MATH_CONST:
    PI = 3.1415926535898
    RAD2DEG = 180.0 / PI
    DEG2RAD = PI / 180.0
    TWOPI = 2.0 * PI


class _NZTM_PARAMETERS:
    NZTM_A = 6378137
    NZTM_RF = 298.257222101

    NZTM_CM = 173.0
    NZTM_OLAT = 0.0
    NZTM_SF = 0.9996
    NZTM_FE = 1600000.0
    NZTM_FN = 10000000.0


class _NZTM_PROJECTION:
    def __init__(self):
        a = _NZTM_PARAMETERS.NZTM_A
        rf = _NZTM_PARAMETERS.NZTM_RF
        cm = _NZTM_PARAMETERS.NZTM_CM / _MATH_CONST.RAD2DEG
        sf = _NZTM_PARAMETERS.NZTM_SF
        lto = _NZTM_PARAMETERS.NZTM_OLAT / _MATH_CONST.RAD2DEG
        fe = _NZTM_PARAMETERS.NZTM_FE
        fn = _NZTM_PARAMETERS.NZTM_FN
        utom = 1.0

        self.meridian = cm
        self.scalef = sf
        self.orglat = lto
        self.falsee = fe
        self.falsen = fn
        self.utom = utom
        f = 1.0 / rf if rf != 0.0 else 0.0
        self.a = a
        self.rf = rf
        self.f = f
        self.e2 = 2.0 * self.f - self.f * self.f
        self.ep2 = self.e2 / (1.0 - self.e2)

        self.om = self.meridianArc(self.orglat)

    def meridianArc(self, lt):
        e2 = self.e2
        a = self.a

        e4 = e2 * e2
        e6 = e4 * e2

        A0 = 1 - (e2 / 4.0) - (3.0 * e4 / 64.0) - (5.0 * e6 / 256.0)
        A2 = (3.0 / 8.0) * (e2 + e4 / 4.0 + 15.0 * e6 / 128.0)
        A4 = (15.0 / 256.0) * (e4 + 3.0 * e6 / 4.0)
        A6 = 35.0 * e6 / 3072.0

        return a * (
            A0 * lt
            - A2 * math.sin(2 * lt)
            + A4 * math.sin(4 * lt)
            - A6 * math.sin(6 * lt)
        )


_nztmProjection = _NZTM_PROJECTION()


class NZTMToWGS84Lib:
    """two-way conversion between NZTM and WGS84

    ported from the official c code from LINZ
    download page: https://www.linz.govt.nz/data/geodetic-services/download-geodetic-software
    source code: https://www.linz.govt.nz/system/files_force/media/file-attachments/nztm.zip?download=1
    """

    @classmethod
    def _footPointLat(self, m):
        f = _nztmProjection.f
        a = _nztmProjection.a

        n = f / (2.0 - f)
        n2 = n * n
        n3 = n2 * n
        n4 = n2 * n2

        g = a * (1.0 - n) * (1.0 - n2) * (1 + 9.0 * n2 / 4.0 + 225.0 * n4 / 64.0)
        sig = m / g

        phio = (
            sig
            + (3.0 * n / 2.0 - 27.0 * n3 / 32.0) * math.sin(2.0 * sig)
            + (21.0 * n2 / 16.0 - 55.0 * n4 / 32.0) * math.sin(4.0 * sig)
            + (151.0 * n3 / 96.0) * math.sin(6.0 * sig)
            + (1097.0 * n4 / 512.0) * math.sin(8.0 * sig)
        )

        return phio

    @classmethod
    def NZTMToGeod(cls, ce, cn):
        """Convert NZTM(easting, northing) to WGS84(latitude, longitude)

        :param ce: input easting (metres)
        :param cn: input northing (metres)
        :return: tuple: latitude (radians), longitude (radians)
        """
        fn = _nztmProjection.falsen
        fe = _nztmProjection.falsee
        sf = _nztmProjection.scalef
        e2 = _nztmProjection.e2
        a = _nztmProjection.a
        cm = _nztmProjection.meridian
        om = _nztmProjection.om
        utom = _nztmProjection.utom

        cn1 = (cn - fn) * utom / sf + om
        fphi = cls._footPointLat(cn1)
        slt = math.sin(fphi)
        clt = math.cos(fphi)

        eslt = 1.0 - e2 * slt * slt
        eta = a / math.sqrt(eslt)
        rho = eta * (1.0 - e2) / eslt
        psi = eta / rho

        E = (ce - fe) * utom
        x = E / (eta * sf)
        x2 = x * x

        t = slt / clt
        t2 = t * t
        t4 = t2 * t2

        trm1 = 1.0 / 2.0

        trm2 = ((-4.0 * psi + 9.0 * (1 - t2)) * psi + 12.0 * t2) / 24.0

        trm3 = (
            (
                (
                    (8.0 * (11.0 - 24.0 * t2) * psi - 12.0 * (21.0 - 71.0 * t2)) * psi
                    + 15.0 * ((15.0 * t2 - 98.0) * t2 + 15)
                )
                * psi
                + 180.0 * ((-3.0 * t2 + 5.0) * t2)
            )
            * psi
            + 360.0 * t4
        ) / 720.0

        trm4 = (((1575.0 * t2 + 4095.0) * t2 + 3633.0) * t2 + 1385.0) / 40320.0

        # latitude (radians)
        lt = fphi + (t * x * E / (sf * rho)) * (
            ((trm4 * x2 - trm3) * x2 + trm2) * x2 - trm1
        )

        trm1 = 1.0

        trm2 = (psi + 2.0 * t2) / 6.0

        trm3 = (
            ((-4.0 * (1.0 - 6.0 * t2) * psi + (9.0 - 68.0 * t2)) * psi + 72.0 * t2)
            * psi
            + 24.0 * t4
        ) / 120.0

        trm4 = (((720.0 * t2 + 1320.0) * t2 + 662.0) * t2 + 61.0) / 5040.0

        # longitude (radians)
        ln = cm - (x / clt) * (((trm4 * x2 - trm3) * x2 + trm2) * x2 - trm1)

        # latitude, longitude
        return lt, ln

    @classmethod
    def GeodToNZTM(cls, ln, lt):
        """Convert WGS84(latitude, longitude) to NZTM(easting, northing)

        :param ln: longitude (radians)
        :param lt: latitude (radians)
        :return: tuple: easting (metres), northing (metres)
        """
        fn = _nztmProjection.falsen
        fe = _nztmProjection.falsee
        sf = _nztmProjection.scalef
        e2 = _nztmProjection.e2
        a = _nztmProjection.a
        cm = _nztmProjection.meridian
        om = _nztmProjection.om
        utom = _nztmProjection.utom

        dlon = ln - cm

        while dlon > _MATH_CONST.PI:
            dlon -= _MATH_CONST.TWOPI

        while dlon < -_MATH_CONST.PI:
            dlon += _MATH_CONST.TWOPI

        m = _nztmProjection.meridianArc(lt)

        slt = math.sin(lt)

        eslt = 1.0 - e2 * slt * slt
        eta = a / math.sqrt(eslt)
        rho = eta * (1.0 - e2) / eslt
        psi = eta / rho

        clt = math.cos(lt)
        w = dlon

        wc = clt * w
        wc2 = wc * wc

        t = slt / clt
        t2 = t * t
        t4 = t2 * t2
        t6 = t2 * t4

        trm1 = (psi - t2) / 6.0

        trm2 = (
            ((4.0 * (1.0 - 6.0 * t2) * psi + (1.0 + 8.0 * t2)) * psi - 2.0 * t2) * psi
            + t4
        ) / 120.0

        trm3 = (61 - 479.0 * t2 + 179.0 * t4 - t6) / 5040.0

        gce = (sf * eta * dlon * clt) * (((trm3 * wc2 + trm2) * wc2 + trm1) * wc2 + 1.0)
        ce = gce / utom + fe

        trm1 = 1.0 / 2.0

        trm2 = ((4.0 * psi + 1) * psi - t2) / 24.0

        trm3 = (
            (
                (
                    (8.0 * (11.0 - 24.0 * t2) * psi - 28.0 * (1.0 - 6.0 * t2)) * psi
                    + (1.0 - 32.0 * t2)
                )
                * psi
                - 2.0 * t2
            )
            * psi
            + t4
        ) / 720.0

        trm4 = (1385.0 - 3111.0 * t2 + 543.0 * t4 - t6) / 40320.0

        gcn = (eta * t) * ((((trm4 * wc2 + trm3) * wc2 + trm2) * wc2 + trm1) * wc2)
        cn = (gcn + m - om) * sf / utom + fn

        return ce, cn
