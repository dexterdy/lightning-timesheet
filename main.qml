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
        color: "#444444"

        Grid {
            anchors.margins: 10
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            columns: 2
            columnSpacing: 5
            rowSpacing: 5
            Label {
                width: parent.width / 2 - 2.5
                text: "User Story:"
            }
            TextField {
                width: parent.width / 2 - 2.5
                placeholderText: "Number or Title"
            }
            Label {
                width: parent.width / 2 - 2.5
                text: "Sub-Ticket (optional):"
            }
            TextField {
                width: parent.width / 2 - 2.5
                placeholderText: "Number or Title"
            }
            Label {
                width: parent.width / 2 - 2.5
                text: "Date:"
            }
            Item {
                width: parent.width / 2 - 2.5
                height: parent.width / 2 - 2.5

                MonthGrid {
                    width: parent.width
                    height: parent.height

                    month: 10
                    year: 2023
                    locale: Qt.locale("en_US")
                }
            }
        }
    }
    RectangularGlow {
        color: "#353535"
        anchors.fill: logModal
        z: -1
        cornerRadius: 8.0
        glowRadius: 15
    }
}