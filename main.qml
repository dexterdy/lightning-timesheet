import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 1200
    height: 1000
    title: "Lightning Timesheet"
    property QtObject backend
    FontLoader {
        id: iconFont
        source: "./fonts/MaterialIcons-Regular.ttf"
    }
    Loader {
        anchors.fill: parent
        source: backend ? "LogTimeModal.qml" : ""
    }
}