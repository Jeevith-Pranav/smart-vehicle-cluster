import pytest
from cluster.ble.protocol import (
    NavInstruction, encode_nav_instruction, parse_nav_instruction, encode_percent,
)


def test_nav_round_trip():
    n = NavInstruction(seq=7, maneuver=3, distance_m=200, street="MG Road")
    assert parse_nav_instruction(encode_nav_instruction(n)) == n


def test_too_short_is_rejected():
    with pytest.raises(ValueError):
        parse_nav_instruction(b"\x01\x03")


def test_unknown_maneuver_is_rejected():
    with pytest.raises(ValueError):
        parse_nav_instruction(bytes([1, 99, 0, 0]))


def test_long_street_is_cut_not_crashed():
    n = NavInstruction(1, 1, 50, "A very very long street name indeed")
    assert len(encode_nav_instruction(n)) == 4 + 16


def test_percent_is_clamped():
    assert encode_percent(150) == b"\x64"
    assert encode_percent(-5) == b"\x00"