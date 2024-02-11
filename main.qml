import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    maximumWidth: 700
    maximumHeight: 700
    minimumWidth: 700
    minimumHeight: 700
    title: "Lightning Timesheet"
    FontLoader {
        id: iconFont
        source: "./fonts/MaterialIcons-Regular.ttf"
    }
    LogTimeModal {}
}