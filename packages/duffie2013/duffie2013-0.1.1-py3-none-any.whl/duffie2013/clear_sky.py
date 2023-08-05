"""
Formalisms to estimate incoming radiations when sky is not clouded.
"""
from datetime import datetime
from math import cos, exp, sin

from . import sun
from .extraterrestrial import incident_ground

corr_fac = dict(
    tropical=(0.95, 0.98, 1.02),
    midlatitude_summer=(0.97, 0.99, 1.02),
    subarctic_summer=(0.99, 0.99, 1.01),
    midlatitude_winter=(1.03, 1.01, 1.00)
)
"""(r0,r1,rk) correction factors

References: table2.8.1
"""


def atm_transmittance(cos_zenith, altitude, climate='midlatitude_summer'):
    """Transmittance of atmosphere for given sun position.

    References: eq2.8.1

    Args:
        cos_zenith (float): [-] cosine of sun zenith position
        altitude (float): [m] Altitude of observer (less than 2500)
        climate (str): type of climate see :obj:`corr_fac`

    Returns:
        (float): [-] transmittance factor
    """
    r0, r1, rk = corr_fac[climate]
    alt = altitude * 1e-3  # [m] to [km]

    a0 = r0 * (0.4237 - 0.00821 * (6 - alt) ** 2)
    a1 = r1 * (0.5055 + 0.00595 * (6.5 - alt) ** 2)
    k = rk * (0.2711 + 0.01858 * (2.5 - alt) ** 2)

    return a0 + a1 * exp(-k / cos_zenith)


def rg_ground(date, latitude, longitude=None, altitude=0., climate='midlatitude_summer'):
    """Incident energy reaching flat ground through atmosphere.

    Args:
        date (datetime): date and time of computation (solar time if longitude=None else UTC)
        latitude (float): [rad] Latitude north of the Equator
        longitude (float): [rad] Longitude positive East of Greenwich
        altitude (float): [m] Altitude of observer (less than 2500)
        climate (str): type of climate see :obj:`corr_fac`

    Returns:
        (float, float): [W.m-2] beam and diffuse energy reaching the ground on specific time
    """
    doy = date.timetuple().tm_yday
    declination = sun.declination(doy)
    time = sun.solar_hour_angle(date, longitude)

    rg_ext = incident_ground(doy, latitude, declination, time)
    if rg_ext <= 0.:
        return 0., 0.

    cos_zenith = cos(latitude) * cos(declination) * cos(time) + sin(latitude) * sin(declination)
    tau_b = atm_transmittance(cos_zenith, altitude, climate)

    rg_beam = rg_ext * tau_b
    rg_diff = rg_ext * (0.271 - 0.294 * tau_b)  # eq2.8.5

    return rg_beam, rg_diff
