import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from cluster.core.vehicle_state import VehicleState
from cluster.sim.simulator import Simulator


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    state = VehicleState()
    sim = Simulator(state)     # fake data for now
    engine.rootContext().setContextProperty("vehicle", state)

    qml_file = Path(__file__).parent / "ui" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()