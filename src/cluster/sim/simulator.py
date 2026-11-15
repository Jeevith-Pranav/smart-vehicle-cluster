import math
from PySide6.QtCore import QTimer

STEPS = [
    (3, "MG Road"),
    (6, "Church Street"),
    (1, "Brigade Road"),
    (9, "Trinity Circle"),
    (10, "Destination"),
]


class Simulator:
    def __init__(self, state):
        self.state = state
        self.t = 0.0
        self.step = 0
        self.distance = 300

        state.bleConnected = True
        state.navActive = True

        self.timer = QTimer()          # keep as self.timer so it isn't deleted
        self.timer.timeout.connect(self.tick)
        self.timer.start(100)          # every 0.1 second

    def tick(self):
        self.t += 0.1
        s = self.state

        s.battery = 55 + 45 * math.sin(self.t / 8)
        s.fuel = 50 + 50 * math.sin(self.t / 6 + 1)
        s.speed = 40 + 30 * math.sin(self.t / 3)

        # Fake navigation: count down distance, then go to the next turn
        self.distance -= 5
        if self.distance <= 0:
            self.step = (self.step + 1) % len(STEPS)
            self.distance = 300
        maneuver, street = STEPS[self.step]
        s.navManeuver = maneuver
        s.navStreet = street
        s.navDistance = self.distance