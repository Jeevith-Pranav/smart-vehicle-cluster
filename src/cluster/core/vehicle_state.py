from PySide6.QtCore import QObject, Property, Signal


def _setter(attr, signal_name, kind, lo=None, hi=None):
    """Makes a setter that cleans the value and tells the UI when it changes."""
    def setter(self, value):
        value = kind(value)
        if lo is not None:
            value = max(lo, min(hi, value))
        if getattr(self, attr) != value:
            setattr(self, attr, value)
            getattr(self, signal_name).emit()
    return setter


class VehicleState(QObject):
    batteryChanged = Signal()
    fuelChanged = Signal()
    speedChanged = Signal()
    bleChanged = Signal()
    navChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._battery = 100      # percent
        self._fuel = 100         # percent
        self._speed = 0          # km/h
        self._ble = False        # phone connected?
        self._nav_active = False
        self._nav_maneuver = 0   # see maneuver codes below
        self._nav_distance = 0   # metres
        self._nav_street = ""

    # Maneuver codes: 0 none, 1 straight, 2 slight left, 3 left, 4 sharp left,
    # 5 slight right, 6 right, 7 sharp right, 8 U-turn, 9 roundabout, 10 arrive

    battery = Property(int, lambda s: s._battery,
                       _setter("_battery", "batteryChanged", int, 0, 100),
                       notify=batteryChanged)
    fuel = Property(int, lambda s: s._fuel,
                    _setter("_fuel", "fuelChanged", int, 0, 100),
                    notify=fuelChanged)
    speed = Property(int, lambda s: s._speed,
                     _setter("_speed", "speedChanged", int, 0, 300),
                     notify=speedChanged)
    bleConnected = Property(bool, lambda s: s._ble,
                            _setter("_ble", "bleChanged", bool),
                            notify=bleChanged)
    navActive = Property(bool, lambda s: s._nav_active,
                         _setter("_nav_active", "navChanged", bool),
                         notify=navChanged)
    navManeuver = Property(int, lambda s: s._nav_maneuver,
                           _setter("_nav_maneuver", "navChanged", int),
                           notify=navChanged)
    navDistance = Property(int, lambda s: s._nav_distance,
                           _setter("_nav_distance", "navChanged", int),
                           notify=navChanged)
    navStreet = Property(str, lambda s: s._nav_street,
                         _setter("_nav_street", "navChanged", str),
                         notify=navChanged)