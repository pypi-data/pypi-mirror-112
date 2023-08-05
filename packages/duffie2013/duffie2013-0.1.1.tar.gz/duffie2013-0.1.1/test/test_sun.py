from datetime import datetime
from math import pi, radians

import pytest
from duffie2013.sun import day_length, declination, solar_time, sunrise_hour_angle, sunset_hour_angle


def test_declination_stays_between_both_tropics():  # fig1.6.3
    cancer = radians(23.4365)
    capricorn = radians(-23.4365)

    for doy in range(1, 366, 30):
        assert capricorn <= declination(doy, True) <= cancer
        assert capricorn <= declination(doy, False) <= cancer


def test_sunset_hour_angle_works_correctly():  # fig1.6.3
    sunset_ref = (19 + 50 / 60 - 12) * pi / 12
    assert sunset_hour_angle(radians(50), radians(21)) == pytest.approx(sunset_ref, abs=0.01)
    sunset_ref = (16 + 10 / 60 - 12) * pi / 12
    assert sunset_hour_angle(radians(50), -radians(21)) == pytest.approx(sunset_ref, abs=0.01)


def test_sunrise_hour_angle_is_before_sunset_hour_angle():
    assert sunrise_hour_angle(radians(50), radians(21)) < sunset_hour_angle(radians(50), radians(21))


def test_day_length_works_correctly():  # fig1.6.3
    assert day_length(radians(50), radians(21)) == pytest.approx(15.7, abs=0.1)
    assert day_length(radians(50), -radians(21)) == pytest.approx(8.3, abs=0.1)


def test_solar_time_equals_utc_when_longitude_equal_0():
    for date in (datetime(2020, 6, 1, 12),
                 datetime(1978, 3, 1, 10),
                 datetime(2000, 9, 12, 20),
                 datetime(2019, 12, 31, 23, 59)):
        assert abs(solar_time(date, 0.) - date).total_seconds() / 60 < 16  # fig1.5.1


def test_solar_time_increases_eastward():
    for date in (datetime(2020, 6, 1, 12),
                 datetime(1978, 3, 1, 10),
                 datetime(2000, 9, 12, 20),
                 datetime(2019, 12, 31, 23, 59)):
        sts = [solar_time(date, radians(longitude)) for longitude in (-45, -30, -15, 0, 10, 50)]

        assert sorted(sts) == sts
