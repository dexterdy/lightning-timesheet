import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects

ApplicationWindow {
    visible: true
    width: 1200
    height: 1000
    title: "Lightning Timesheet"
    Rectangle {
        id: logModal
        width: 500
        height: 750
        radius: 8.0
        anchors.centerIn: parent
        color: "grey"
    }
    RectangularGlow {
        color: "#A9A9A9"
        anchors.fill: logModal
        z: -1
        cornerRadius: 8.0
        glowRadius: 10
    }
}