import QtQuick

Item {
    id: gauge
    property real value: 0          // 0 to 100
    property string label: ""
    property real shown: value      // smoothed value used for drawing

    Behavior on shown { NumberAnimation { duration: 250 } }

    // green normally, amber at 20% or less, red at 10% or less
    readonly property color arcColor:
        value <= 10 ? "#ff3b30" : (value <= 20 ? "#ffb300" : "#2ecc71")

    onShownChanged: canvas.requestPaint()
    onArcColorChanged: canvas.requestPaint()

    Canvas {
        id: canvas
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            var cx = width / 2
            var cy = height / 2
            var r = width / 2 - 16
            var start = 0.75 * Math.PI      // bottom-left
            var sweep = 1.5 * Math.PI       // 270 degrees
            ctx.lineWidth = 18
            ctx.lineCap = "round"

            // background track
            ctx.strokeStyle = "#1e2630"
            ctx.beginPath()
            ctx.arc(cx, cy, r, start, start + sweep, false)
            ctx.stroke()

            // value arc
            if (gauge.shown > 0.5) {
                ctx.strokeStyle = gauge.arcColor
                ctx.beginPath()
                ctx.arc(cx, cy, r, start, start + sweep * gauge.shown / 100, false)
                ctx.stroke()
            }
        }
    }

    Text {
        anchors.centerIn: parent
        text: Math.round(gauge.value) + "%"
        color: "white"
        font.pixelSize: 44
        font.bold: true
    }

    Text {
        anchors.horizontalCenter: parent.horizontalCenter
        y: parent.height * 0.66
        text: gauge.label
        color: "#8a96a3"
        font.pixelSize: 16
        font.letterSpacing: 2
    }
}