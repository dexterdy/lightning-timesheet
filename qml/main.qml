import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQml
import WeekDaysModel
import LogsModel

ApplicationWindow {
    id: window
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
    LogTimeModal {
        id: modal
    }
    ColumnLayout {
        anchors.fill: parent
        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: markdown.height
            Layout.margins: 10
            Layout.alignment: Qt.AlignTop
            Button {
                text: "Log activity"
                onClicked: {
                    modal.openModal();
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
        Item {
            ScrollView {
                ListView {
                    model: WeekDaysModel {
                        id: days
                    }
                    delegate: ListView {
                        model: LogsModel {
                            logs: dayLogs
                        }
                        delegate: Text {
                            text: "hello"
                        }
                    }
                }
            }
        }
    }
}
