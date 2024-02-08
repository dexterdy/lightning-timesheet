import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtQuick.Layouts
import QtQml

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

        ColumnLayout {
            anchors.margins: 20
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            spacing: 15
            Label {
                Layout.alignment: Qt.AlignHCenter
                text: "User Story:"
            }
            TextField {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: parent.width - 100
                placeholderText: "Number or Title"
            }
            Label {
                Layout.alignment: Qt.AlignHCenter
                width: parent.width
                text: "Sub-Ticket (optional):"
            }
            TextField {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: parent.width - 100
                placeholderText: "Number or Title"
            }
            Label {
                Layout.alignment: Qt.AlignHCenter
                width: parent.width
                text: "Date:"
            }
            Row {
                Layout.alignment: Qt.AlignHCenter
                Layout.preferredWidth: parent.width - 100
                spacing: 5
                TextField {
                    width: parent.width / 2 - 10 / 3
                    placeholderText: "YYYY"
                    inputMask: "9999"
                }
                TextField {
                    width: parent.width / 4 - 10 / 3
                    placeholderText: "MM"
                    inputMask: "99"
                }
                TextField {
                    width: parent.width / 4 - 10 / 3
                    placeholderText: "DD"
                    inputMask: "99"
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