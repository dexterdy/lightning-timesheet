import QtQuick.Controls
import QtQuick
import WeekDaysModel
import LogsModel

//TODO: Add days of the week at the top
//TODO: add time and column markers
//TODO: add ticket title to time box
//TODO: make time box clickable
//TODO: enter into edit mode
//TODO: make sure that any changes to timesheet is reflected graphically
//TODO: make week selector and other important ui elements
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
                    Text {
                        clip: true
                        x: 5
                        y: 5
                        width: parent.width - 10
                        height: parent.height - 10
                        text: title
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
    }
}
