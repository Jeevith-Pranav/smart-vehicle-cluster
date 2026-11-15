import argparse
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from cluster.core.vehicle_state import VehicleState


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["sim", "manual", "hardware"], default="sim",
                   help="sim = fake moving data, manual = sliders, hardware = real sensors (Pi only)")
    p.add_argument("--fullscreen", action="store_true")
    return p.parse_args()


def main():
    args = parse_args()
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    state = VehicleState()

    keep_alive = None
    if args.source == "sim":
        from cluster.sim.simulator import Simulator
        keep_alive = Simulator(state)
    elif args.source == "hardware":
        # Added later, Pi only. Imported here so the laptop never loads it.
        raise SystemExit("hardware source is not written yet")
    # "manual": nothing runs, the sliders set the values

    ctx = engine.rootContext()
    ctx.setContextProperty("vehicle", state)
    ctx.setContextProperty("testMode", args.source == "manual")
    ctx.setContextProperty("startFullscreen", args.fullscreen)

    qml_file = Path(__file__).parent / "ui" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_file)))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()