import QtQuick.Controls
import QtQuick
import QtQuick.Window

Window {
    id: root
    width: 800
    height: 480
    visible: true
    visibility: startFullscreen ? Window.FullScreen : Window.Windowed
    color: "#0b0f14"
    title: "Smart Cluster"

    // maneuver code -> arrow symbol
    readonly property var arrows: ["", "↑", "↖", "←", "↙", "↗", "→", "↘", "↩", "⟳", "⚑"]

    // ---------- Top status bar ----------
    Text {
        id: clock
        x: 24; y: 16
        color: "white"
        font.pixelSize: 24
        text: Qt.formatTime(new Date(), "hh:mm")
    }
    Timer {
        interval: 1000; running: true; repeat: true
        onTriggered: clock.text = Qt.formatTime(new Date(), "hh:mm")
    }

    Row {
        anchors.right: parent.right
        anchors.rightMargin: 24
        y: 18
        spacing: 8
        Rectangle {
            width: 16; height: 16; radius: 8
            anchors.verticalCenter: parent.verticalCenter
            color: vehicle.bleConnected ? "#2e9bff" : "#555b63"
        }
        Text {
            color: vehicle.bleConnected ? "#2e9bff" : "#8a96a3"
            font.pixelSize: 20
            text: vehicle.bleConnected ? "Phone connected" : "Phone disconnected"
        }
    }

    // ---------- Gauges ----------
    Gauge {
        x: 30; y: 100; width: 230; height: 230
        value: vehicle.battery
        label: "BATTERY"
    }
    Gauge {
        x: 540; y: 100; width: 230; height: 230
        value: vehicle.fuel
        label: "FUEL"
    }

    // ---------- Speed ----------
    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 70
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: vehicle.speed
            color: "white"
            font.pixelSize: 110
            font.bold: true
        }
        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "km/h"
            color: "#8a96a3"
            font.pixelSize: 22
        }
    }

    // ---------- Navigation card ----------
    Rectangle {
        x: 275; y: 300
        width: 250; height: 120
        radius: 16
        color: "#141b24"
        border.color: "#243040"

        Row {
            anchors.centerIn: parent
            spacing: 18
            visible: vehicle.navActive

            Text {
                text: root.arrows[vehicle.navManeuver]
                color: "#2e9bff"
                font.pixelSize: 64
                anchors.verticalCenter: parent.verticalCenter
            }
            Column {
                anchors.verticalCenter: parent.verticalCenter
                Text {
                    text: vehicle.navDistance + " m"
                    color: "white"
                    font.pixelSize: 30
                    font.bold: true
                }
                Text {
                    text: vehicle.navStreet
                    color: "#8a96a3"
                    font.pixelSize: 18
                    width: 130
                    elide: Text.ElideRight
                }
            }
        }

        Text {
            anchors.centerIn: parent
            visible: !vehicle.navActive
            text: "No route"
            color: "#555b63"
            font.pixelSize: 22
        }
    }

    // ---------- Warning bar ----------
    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: 438
        font.pixelSize: 22
        font.bold: true
        text: vehicle.fuel <= 10 ? "⚠ LOW FUEL"
            : vehicle.battery <= 10 ? "⚠ LOW BATTERY"
            : ""
        color: "#ff3b30"
    }
    
        // ---------- Manual test sliders (only with --source manual) ----------
    Slider {
        visible: testMode
        x: 30; y: 350; width: 230
        from: 0; to: 100
        value: vehicle.battery
        onMoved: vehicle.battery = value
    }
    Slider {
        visible: testMode
        x: 540; y: 350; width: 230
        from: 0; to: 100
        value: vehicle.fuel
        onMoved: vehicle.fuel = value
    }
}