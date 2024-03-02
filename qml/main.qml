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
                    backend.weekBackward();
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
                    backend.weekForward();
                }
            }
            Text {
                id: timeThisWeek
                anchors.right: excel.left
                anchors.rightMargin: 10
                height: parent.height
                color: systemPalette.buttonText
                verticalAlignment: Text.AlignVCenter
                text: {
                    const time = backend.hours;
                    return `${time[0]} hours ${time[1]} minutes`;
                }
            }
            Button {
                id: excel
                anchors.rightMargin: 10
                anchors.right: markdown.left
                text: "Export as excel"
                onClicked: backend.export(2)
            }
            Button {
                id: markdown
                anchors.right: parent.right
                text: "Export as markdown"
                onClicked: backend.export(1)
            }
        }
        ScrollView {
            id: scroller
            Layout.fillWidth: true
            Layout.fillHeight: true
            contentHeight: 2400
            contentWidth: parent.width
            clip: true
            ScrollBar.vertical.position: (1 - ScrollBar.vertical.size) - 0.35
            WeekView {
                id: weekView
            }
        }
    }
}
