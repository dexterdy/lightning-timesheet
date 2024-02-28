import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml
import "../icons/MaterialDesign.js" as MD

ApplicationWindow {
    id: window
    visible: true
    minimumWidth: 700
    minimumHeight: 700
    title: "Lightning Timesheet"
    FontLoader {
        id: iconFont
        source: "../icons/MaterialIcons-Regular.ttf"
    }
    SystemPalette {
        id: systemPalette
    }
    LogTimeModal {
        id: modal
    }
    ColumnLayout {
        id: topColumn
        anchors.fill: parent
        Item {
            id: topRow
            Layout.fillWidth: true
            Layout.preferredHeight: markdown.height
            Layout.margins: 10
            Layout.alignment: Qt.AlignTop
            Button {
                id: logButton
                text: "Log activity"
                onClicked: {
                    modal.openModal();
                }
            }
            Button {
                id: weekBack
                anchors.left: logButton.right
                anchors.leftMargin: 10
                height: parent.height
                width: backIcon.width
                Icon {
                    id: backIcon
                    icon: MD.icons.arrow_back
                    size: 27
                    color: systemPalette.buttonText
                }
                onClicked: {
                    weekView.weekBackward();
                }
            }
            Button {
                id: weekForward
                anchors.left: weekBack.right
                anchors.leftMargin: 10
                height: parent.height
                width: fowardIcon.width
                Icon {
                    id: fowardIcon
                    icon: MD.icons.arrow_forward
                    size: 27
                    color: systemPalette.buttonText
                }
                onClicked: {
                    weekView.weekForward();
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
                text: "Export as excel"
                onClicked: backend.export(2)
            }
        }
        ScrollView {
            id: scroller
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentHeight: 2400
            contentWidth: parent.width
            clip: true
            WeekView {
                id: weekView
            }
        }
    }
}
