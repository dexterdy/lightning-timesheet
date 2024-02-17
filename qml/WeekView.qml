import QtQuick
import WeekDaysModel
import LogsModel

Row {
    height: 2400
    width: parent.width
    Repeater {
        model: WeekDaysModel {
            id: days
        }
        delegate: Item {
            width: scroller.width / 7
            height: parent.height
            Repeater {
                model: LogsModel {
                    logs: dayLogs
                }
                Rectangle {
                    color: "red"
                    width: parent.width
                    y: parent.height * fromTime
                    height: parent.height * tillTime - parent.height * fromTime
                    border.color: "black"
                    border.width: 1
                }
            }
        }
    }
}
