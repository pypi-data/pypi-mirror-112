from datetime import datetime, timedelta
from math import cos, radians

import pytest
from duffie2013.clear_sky import atm_transmittance, rg_ground


def test_atm_transmittance_is_between_0_and_1():
    for zen in (0, 30, 45, 60, 90):
        for alt in (0, 100, 400, 1000, 2500):
            assert 0 <= atm_transmittance(cos(radians(zen)), alt) <= 1


def test_atm_transmittance_increases_with_altitude():
    cos_zenith = cos(radians(45))
    trs = [atm_transmittance(cos_zenith, alt) for alt in (0, 100, 400, 1000, 2500)]

    assert sorted(trs) == trs


def test_atm_transmittance_decreases_with_zenith_angle():
    trs = [atm_transmittance(cos(radians(zen)), 100) for zen in (0, 30, 45, 60, 90)]

    assert sorted(trs, reverse=True) == trs


def test_rg_ground_compares_to_ex2_8_1():
    rgb, rgd = rg_ground(datetime(2020, 8, 21, 11, 30), radians(43), altitude=270)

    assert rgb == pytest.approx(702, abs=1)
    assert rgd == pytest.approx(101, abs=1)


def test_rg_ground_compares_to_ex2_8_2():
    latitude = radians(43)
    altitude = 270
    day = datetime(2020, 8, 21)  # why not 22? don't know

    for h, rgd_ref, rg_ref in [(11.5, 0.36, 2.89),
                               (10.5, 0.35, 2.69),
                               (9.5, 0.34, 2.31),
                               (8.5, 0.32, 1.78),
                               (7.5, 0.28, 1.15),
                               (6.5, 0.20, 0.53),
                               (5.5, 0.05, 0.07),
                               ]:
        rgb, rgd = rg_ground(day + timedelta(hours=h), latitude, altitude)

        assert rgd * 3600e-6 == pytest.approx(rgd_ref, abs=1)
        assert (rgb + rgd) * 3600e-6 == pytest.approx(rg_ref, abs=1)
