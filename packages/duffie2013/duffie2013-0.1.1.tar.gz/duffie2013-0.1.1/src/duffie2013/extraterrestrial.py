"""
Amount of extraterrestrial radiation reaching the Earth
"""
from datetime import datetime
from math import cos, pi, sin

from .sun import declination as sun_declination, solar_constant, solar_hour_angle, sunset_hour_angle


def incident_toa(doy, standard=True):
    """Incident energy reaching top of atmosphere on given day.

    References: eq1.4.1

    Args:
        doy (int): day of year
        standard (bool): whether to use standard (default) or precise computation

    Returns:
        (float): [W.m-2]
    """
    if standard:
        e0 = (1 + 0.033 * cos(2 * pi * doy / 365))
    else:
        gamma = 2 * pi * (doy - 1) / 365
        e0 = (1.000110
              + 0.034221 * cos(gamma) + 0.001280 * sin(gamma)
              + 0.000719 * cos(2 * gamma) + 0.000077 * sin(2 * gamma))

    return solar_constant * e0


def incident_ground(doy, latitude, declination, time, standard=True):
    """Incident energy reaching flat ground not considering effects of atmosphere.

    References: eq1.10.2

    Args:
        doy (int): day of year
        latitude (float): [rad] latitude of ground
        declination (float): [rad] sun declination that day
        time (float): [rad] solar hour angle
        standard (bool): whether to use standard (default) or precise computation

    Returns:
        (float): [W.m-2] energy reaching the ground on specific time
    """
    proj = cos(latitude) * cos(declination) * cos(time) + sin(latitude) * sin(declination)

    return incident_toa(doy, standard) * proj


def daily_incident_ground(doy, latitude, declination, sunset, standard=True):
    """Daily amount of energy reaching flat ground not considering effects of atmosphere.

    Args:
        doy (int): day of year
        latitude (float): [rad] Latitude north of the Equator
        declination (float): [rad] sun declination that day
        sunset (float): [rad] solar hour angle of sunset that day
        standard (bool): whether to use standard (default) or precise computation

    Returns:
        (float): [MJ.m-2] energy reaching the ground integrated over the day
    """
    proj = cos(latitude) * cos(declination) * sin(sunset) + sunset * sin(latitude) * sin(declination)

    return 24 * 3600e-6 / pi * incident_toa(doy, standard) * proj


def rg_ground(date, latitude, longitude=None):
    """Incident energy reaching flat ground not considering effects of atmosphere.

    Notes: convenience API for :func:`incident_ground`

    Args:
        date (datetime): date and time of computation (solar time if longitude=None else UTC)
        latitude (float): [rad] Latitude north of the Equator
        longitude (float): [rad] Longitude positive East of Greenwich

    Returns:
        (float, float): [W.m-2] beam and diffuse energy reaching the ground on specific time
    """
    doy = date.timetuple().tm_yday
    rg = incident_ground(doy=doy,
                         latitude=latitude,
                         declination=sun_declination(doy),
                         time=solar_hour_angle(date, longitude))
    return max(0., rg), 0.


def rg_daily(day, latitude):
    """Daily amount of energy reaching flat ground not considering effects of atmosphere.

    Notes: convenience API for :func:`daily_incident_ground`

    Args:
        day (datetime): day of computation (the HH:MM:SS will be removed)
        latitude (float): [rad] Latitude north of the Equator

    Returns:
        (float): [MJ.m-2] total energy reaching the ground integrated over the day
    """
    doy = day.timetuple().tm_yday
    decl = sun_declination(doy)
    return daily_incident_ground(doy=doy,
                                 latitude=latitude,
                                 declination=decl,
                                 sunset=sunset_hour_angle(latitude, decl))


def rg_hourly(date, latitude, longitude=None):
    """Incident energy reaching flat ground not considering effects of atmosphere.

    Notes: integrate :func:`incident_ground` over one hour

    Args:
        date (datetime): date and time of computation (solar time if longitude=None else UTC)
        latitude (float): [rad] Latitude north of the Equator
        longitude (float): [rad] Longitude positive East of Greenwich

    Returns:
        (float, float): [MJ.m-2] hourly beam and diffuse energy reaching the
                        ground on specific time
    """
    doy = date.timetuple().tm_yday
    declination = sun_declination(doy)
    w1 = solar_hour_angle(date, longitude)
    w2 = w1 + pi / 12  # one hour later

    proj_int = 12 / pi * (cos(latitude) * cos(declination) * (sin(w2) - sin(w1))
                          + (w2 - w1) * sin(latitude) * sin(declination))

    return max(0., incident_toa(doy) * proj_int * 3600e-6), 0.
