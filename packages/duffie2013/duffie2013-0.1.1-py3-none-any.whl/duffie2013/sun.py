from datetime import datetime, timedelta
from math import acos, cos, pi, radians, sin, tan

solar_constant = 1367
"""[W.m-2] energy from the sun per unit time received on a unit area of surface
perpendicular to the direction of propagation of the radiation at mean earth-sun
distance outside the atmosphere

References: fig1.2.1
"""


def declination(doy, standard=True):
    """Sun declination.

    Angular position of the sun at solar noon (i.e., when the sun is on the
    local meridian) with respect to the plane of the equator.

    References: eq1.6.1a and eq1.6.1b

    Args:
        doy (int): day of year
        standard (bool): whether to use standard (default) or precise computation

    Returns:
        (float): [rad] sun declination that day
    """
    if standard:
        return radians(23.45) * sin(2 * pi * (284 + doy) / 365)
    else:
        gamma = 2 * pi * (doy - 1) / 365
        return (0.006918 - 0.399912 * cos(gamma) + 0.070257 * sin(gamma)
                - 0.006758 * cos(2 * gamma) + 0.000907 * sin(2 * gamma)
                - 0.002697 * cos(3 * gamma) + 0.00148 * sin(3 * gamma))


def sunrise_hour_angle(latitude, decl):
    """Hour angle of sunrise.

    References: eq1.6.10

    Args:
        latitude (float): [rad] latitude of place
        decl (float): [rad] sun declination angle

    Returns:
        (float): [rad] solar hour angle
    """
    return - sunset_hour_angle(latitude, decl)


def sunset_hour_angle(latitude, decl):
    """Hour angle of sunset.

    References: eq1.6.10

    Args:
        latitude (float): [rad] latitude of place
        decl (float): [rad] sun declination angle

    Returns:
        (float): [rad] solar hour angle
    """
    return acos(- tan(latitude) * tan(decl))


def day_length(latitude, decl):
    """Length of daylight.

    References: eq1.6.11

    Args:
        latitude (float): [rad] latitude of place
        decl (float): [rad] sun declination angle

    Returns:
        (float): [h] duration of sun light that day
    """
    return sunset_hour_angle(latitude, decl) * 24 / pi


def solar_time(date, longitude):
    """Convert date in UTC to local solar time.

    References: eq1.5.2 and eq1.5.3

    Args:
        date (datetime): UTC
        longitude (float): [rad] longitude of place (positive Eastward)

    Returns:
        (datetime): same instant but in solar time
    """
    doy = date.timetuple().tm_yday
    gamma = 2 * pi * (doy - 1) / 365  # eq1.4.2
    time_eq = 229.2 * (0.000075 + 0.001868 * cos(gamma) - 0.032077 * sin(gamma)
                       - 0.014615 * cos(2 * gamma) - 0.04089 * sin(2 * gamma))

    return date + timedelta(minutes=time_eq + longitude * 720 / pi)


def solar_hour(date, longitude=None):
    """Position of sun around the earth.

    solar_hour_angle expressed in hours instead of angle.

    Args:
        date (datetime): date and time of computation (solar time if longitude=None else UTC)
        longitude (float): [rad] Longitude positive East of Greenwich

    Returns:
        (float): [h] solar hour to solar noon
    """
    if longitude is not None:
        date = solar_time(date, longitude)

    return (date - date.replace(hour=12, minute=0, second=0, microsecond=0)).total_seconds() / 3600


def solar_hour_angle(date, longitude=None):
    """Position of sun around the earth.

    Observing the sun from earth, the solar hour angle is an expression of time,
    expressed in angular measurement, usually degrees, from solar noon. At solar
    noon the hour angle is zero degrees, with the time before solar noon expressed
    as negative degrees, and the local time after solar noon expressed as positive
    degrees.

    For example, at 10:30 AM local apparent time the hour angle is −22.5°
    (15° per hour times 1.5 hours before noon).

    Args:
        date (datetime): date and time of computation (solar time if longitude=None else UTC)
        longitude (float): [rad] Longitude positive East of Greenwich

    Returns:
        (float): [rad] solar hour angle
    """
    return solar_hour(date, longitude) * pi / 12
