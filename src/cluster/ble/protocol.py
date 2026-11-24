"""Byte layout of BLE messages. Must match docs/ble-spec.md."""
import struct
from dataclasses import dataclass

MANEUVERS = {
    0: "none", 1: "straight", 2: "slight left", 3: "left", 4: "sharp left",
    5: "slight right", 6: "right", 7: "sharp right", 8: "u-turn",
    9: "roundabout", 10: "arrive",
}
MAX_STREET_BYTES = 16   # safe size with the default BLE packet size


@dataclass
class NavInstruction:
    seq: int
    maneuver: int
    distance_m: int
    street: str


def encode_nav_instruction(n: NavInstruction) -> bytes:
    """Used by tests and (in Dart form) by the phone app."""
    street = n.street.encode("utf-8")[:MAX_STREET_BYTES]
    return struct.pack("<BBH", n.seq & 0xFF, n.maneuver, n.distance_m) + street


def parse_nav_instruction(data: bytes) -> NavInstruction:
    """Turns received bytes into a NavInstruction. Rejects bad data."""
    if len(data) < 4:
        raise ValueError("nav packet too short")
    seq, maneuver, distance = struct.unpack_from("<BBH", data, 0)
    if maneuver not in MANEUVERS:
        raise ValueError(f"unknown maneuver {maneuver}")
    street = data[4:].decode("utf-8", errors="ignore").rstrip("\x00")
    return NavInstruction(seq, maneuver, distance, street)


def encode_percent(value: int) -> bytes:
    """Battery / fuel notification: one byte, 0-100."""
    return struct.pack("<B", max(0, min(100, int(value))))  