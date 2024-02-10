import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtQuick.Layouts
import QtLocation
import QtQml
import "MaterialDesign.js" as MD

Item {
    anchors.fill: parent
    Rectangle {
        id: logModal
        width: 500
        height: 500
        radius: 8.0
        anchors.centerIn: parent
        color: "#444444"

        Icon {
            id: exit
            icon: MD.icons.close
            anchors.right: parent.right
        }
        HoverHandler {
            parent: exit
            cursorShape: Qt.PointingHandCursor
        }

        Rectangle {
            anchors.top: parent.top
            ListView {
                width: 100
                height: 100
                model: backend.issues
                delegate: Text {
                    text: title
                }
            }
        }

        ColumnLayout {
            anchors.margins: 50
            anchors.leftMargin: 75
            anchors.rightMargin: 75
            anchors.fill: parent
            Item {
                Layout.alignment: Qt.AlignTop
                Layout.preferredWidth: parent.width
                ColumnLayout {
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    Label {
                        Layout.bottomMargin: 5
                        text: "User Story:"
                    }
                    TextField {
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        placeholderText: "Number or Title"
                    }
                    Label {
                        Layout.bottomMargin: 5
                        text: "Sub-Ticket (optional):"
                    }
                    TextField {
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        placeholderText: "Number or Title"
                    }
                    Label {
                        Layout.bottomMargin: 5
                        text: "Date:"
                    }
                    Row {
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        spacing: 5
                        TextField {
                            validator: IntValidator {}
                            maximumLength: 4
                            width: parent.width / 2 - 10 / 3
                            placeholderText: "YYYY"
                        }
                        TextField {
                            validator: IntValidator {}
                            maximumLength: 2
                            width: parent.width / 4 - 10 / 3
                            placeholderText: "MM"
                        }
                        TextField {
                            validator: IntValidator {}
                            maximumLength: 2
                            width: parent.width / 4 - 10 / 3
                            placeholderText: "DD"
                        }
                    }
                    Row {
                        Layout.preferredWidth: parent.width
                        Column {
                            width: parent.width / 2
                            spacing: 7
                            Label {
                                text: "from:"
                            }
                            Row {
                                width: parent.width
                                spacing: 7
                                TextField {
                                    validator: IntValidator {}
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "HH"
                                }
                                TextField {
                                    validator: IntValidator {}
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "MM"
                                }
                            }
                        }
                        Column {
                            width: parent.width / 2
                            spacing: 10
                            Label {
                                text: "till:"
                            }
                            Row {
                                width: parent.width
                                spacing: 7
                                TextField {
                                    validator: IntValidator {}
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "HH"
                                }
                                TextField {
                                    validator: IntValidator {}
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "MM"
                                }
                            }
                        }
                    }
                }
            }
            Row {
                Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                spacing: 5
                Button {
                    text: "Save"
                }
                Button {
                    text: "Cancel"
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