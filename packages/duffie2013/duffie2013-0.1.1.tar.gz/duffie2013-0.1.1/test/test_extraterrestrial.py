from datetime import datetime, timedelta
from math import pi, radians

import pytest
from duffie2013.extraterrestrial import (daily_incident_ground, incident_ground, incident_toa, rg_daily, rg_ground,
                                         rg_hourly)
from duffie2013.sun import declination, sunset_hour_angle


def test_incident_toa_varies_between_1320_and_1420():  # ref fig1.4.1
    for doy in range(1, 366):
        assert 1320 < incident_toa(doy, standard=True) < 1420
        assert 1320 < incident_toa(doy, standard=False) < 1420


def test_incident_ground_smaller_than_toa():
    for doy in range(1, 366, 30):
        decl = declination(doy)
        for latitude in (0, 10, 45):
            lat = radians(latitude)
            ws = sunset_hour_angle(lat, decl)
            for ind in range(-12, 12):
                assert 0 <= incident_ground(doy, lat, decl, ws * ind / 24) <= incident_toa(doy)


def test_incident_ground_sums_to_daily_incident_ground():
    for doy in range(1, 366, 30):
        decl = declination(doy)
        for latitude in (0, 10, 45):
            lat = radians(latitude)
            ws = sunset_hour_angle(lat, decl)
            rg_day = daily_incident_ground(doy, lat, decl, ws)

            sunrise = -ws * 12 / pi
            sunset = ws * 12 / pi
            rg_sum = sum(incident_ground(doy, lat, decl, h * pi / 12) * 3600e-6 if sunrise <= h <= sunset else 0
                         for h in range(-12, 12))

            assert rg_sum == pytest.approx(rg_day, abs=0.3)


def test_rg_daily_decreases_northward_in_winter():
    day = datetime(2020, 1, 1)
    rgs = [rg_daily(day, radians(latitude)) for latitude in (0, 15, 45, 50)]

    assert sorted(rgs, reverse=True) == rgs


def test_rg_daily_compares_to_table1_10_1():
    latitude = radians(45)
    for ind, rg_ref in enumerate([12.2, 17.4, 25.1, 33.2, 39.2, 41.7, 40.4, 35.3, 27.8, 19.6, 13.3, 10.7]):
        day = datetime(2020, ind + 1, 15)
        assert rg_daily(day, latitude) == pytest.approx(rg_ref, abs=0.5)


def test_rg_ground_sums_to_rg_daily():
    day = datetime(2020, 1, 1)
    latitude = radians(40)

    rg_day = rg_daily(day, latitude)
    rg_sum = sum(sum(rg_ground(day + timedelta(hours=h), latitude, longitude=0.)) * 3600e-6 for h in range(0, 24))

    assert rg_sum == pytest.approx(rg_day, abs=0.3)


def test_rg_hourly_equals_integration_of_rg_ground():
    date = datetime(2020, 6, 1, 10)
    latitude = radians(40)
    dt = timedelta(minutes=1)

    rg_h = sum(rg_hourly(date, latitude))
    rg_int = sum(sum(rg_ground(date + dt * i, latitude)) for i in range(60)) * dt.total_seconds() * 1e-6

    assert rg_h == pytest.approx(rg_int, abs=0.01)
