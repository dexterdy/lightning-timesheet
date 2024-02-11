import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml

ApplicationWindow {
    visible: true
    maximumWidth: 700
    maximumHeight: 700
    minimumWidth: 700
    minimumHeight: 700
    title: "Lightning Timesheet"
    FontLoader {
        id: iconFont
        source: "../icons/MaterialIcons-Regular.ttf"
    }
    Item {
        anchors.fill: parent
        anchors.margins: 10
        Button {
            text: "Log activity"
            onClicked: {
                modal.open();
            }
        }
        Button {
            id: markdown
            anchors.right: parent.right
            text: "Export as markdown"
            onClicked: backend.export(1)
        }
        Button {
            anchors.rightMargin: 10
            anchors.right: markdown.left
            Layout.alignment: Qt.AlignRight
            text: "Export as excel"
            onClicked: backend.export(2)
        }
        LogTimeModal {
            id: modal
        }
    }
}
