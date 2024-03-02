import QtQuick
import QtQuick.Controls
import Qt5Compat.GraphicalEffects
import QtQuick.Layouts
import QtQml
import "../icons/MaterialDesign.js" as MD

Popup {
    id: modalContainer
    parent: Overlay.overlay
    modal: true
    visible: false
    width: 500
    height: 620
    anchors.centerIn: parent
    Rectangle {
        id: logModal
        anchors.fill: parent
        radius: 8.0
        color: systemPalette.light

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
                        text: "Ticket:"
                    }
                    TicketInput {
                        id: ticketInput
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        onSelect: number => backend.selectTicket(number)
                    }
                    Label {
                        Layout.bottomMargin: 5
                        text: "User Story (optional):"
                    }
                    TicketInput {
                        id: userStoryInput
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        onSelect: number => backend.selectUserStory(number)
                    }
                    Label {
                        Layout.bottomMargin: 5
                        text: "Date (optional, defaults to today):"
                    }
                    Row {
                        Layout.preferredWidth: parent.width
                        Layout.bottomMargin: 15
                        spacing: 5
                        TextField {
                            id: year
                            validator: IntValidator {
                            }
                            maximumLength: 4
                            width: parent.width / 2 - 10 / 3
                            placeholderText: "YYYY"
                        }
                        TextField {
                            id: month
                            validator: IntValidator {
                            }
                            maximumLength: 2
                            width: parent.width / 4 - 10 / 3
                            placeholderText: "MM"
                        }
                        TextField {
                            id: day
                            validator: IntValidator {
                            }
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
                                text: "From:"
                            }
                            Row {
                                width: parent.width
                                spacing: 7
                                TextField {
                                    id: fromHour
                                    validator: IntValidator {
                                    }
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "HH"
                                }
                                TextField {
                                    id: fromMinute
                                    validator: IntValidator {
                                    }
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
                                text: "Till:"
                            }
                            Row {
                                width: parent.width
                                spacing: 7
                                TextField {
                                    id: tillHour
                                    validator: IntValidator {
                                    }
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "HH"
                                }
                                TextField {
                                    id: tillMinute
                                    validator: IntValidator {
                                    }
                                    maximumLength: 2
                                    width: 40
                                    placeholderText: "MM"
                                }
                            }
                        }
                    }
                    Row {
                        Layout.preferredWidth: parent.width
                        Layout.preferredHeight: atOffice.height
                        CheckBox {
                            id: atOffice
                        }
                        Label {
                            text: "At the office"
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                    Label {
                        Layout.bottomMargin: 5
                        text: "Description (optional):"
                    }
                    TextField {
                        id: description
                        verticalAlignment: TextInput.AlignTop
                        Layout.preferredWidth: parent.width
                        width: parent.width
                        Layout.preferredHeight: 100
                        wrapMode: TextInput.Wrap
                        Layout.bottomMargin: 15
                    }
                    Label {
                        id: error
                        width: parent.width
                        Layout.bottomMargin: 5
                        text: ""
                        color: "red"
                        wrapMode: Text.Wrap
                    }
                }
            }
            Row {
                Layout.alignment: Qt.AlignBottom | Qt.AlignRight
                spacing: 5
                Button {
                    text: "Save"
                    onClicked: {
                        let err = checkRequiredFields();
                        if (err === "")
                            err = backend.setDate(Number(year.text), Number(month.text), Number(day.text));
                        if (err === "")
                            err = backend.setFromTime(Number(fromHour.text), Number(fromMinute.text));
                        if (err === "")
                            err = backend.setTillTime(Number(tillHour.text), Number(tillMinute.text));
                        backend.setDescription(description.text);
                        backend.setAtOffice(atOffice.checkState === Qt.Checked);
                        if (err === "")
                            err = backend.submit();
                        error.text = err;
                        if (err === "")
                            close();
                    }
                }
                Button {
                    text: "Cancel"
                    onClicked: {
                        backend.reset();
                        close();
                    }
                }
            }
        }
    }
    RectangularGlow {
        color: "#151515"
        anchors.fill: logModal
        z: -1
        cornerRadius: 8.0
        glowRadius: 15
    }
    function openModal() {
        modalContainer.open();
        ticketInput.updateIssues();
        userStoryInput.updateIssues();
        resetUI();
    }
    function checkRequiredFields() {
        let error = false;
        error = ticketInput.text === "";
        error = fromHour.text === "";
        error = fromMinute.text === "";
        error = tillHour.text === "";
        error = tillMinute.text === "";
        if (error)
            return "All required fields must be set before submission.";
        return "";
    }
    function resetUI() {
        ticketInput.reset();
        userStoryInput.reset();
        ticketInput.text = backend.initialTicketText();
        userStoryInput.text = backend.initialUserStoryText();
        year.text = backend.initialYear();
        month.text = backend.initialMonth();
        day.text = backend.initialDay();
        fromHour.text = backend.initialFromHour();
        fromMinute.text = backend.initialFromMinute();
        tillHour.text = backend.initialTillHour();
        tillMinute.text = backend.initialTillMinute();
        description.text = backend.initialDescription();
        atOffice.checkState = backend.initialAtOffice() ? Qt.Checked : Qt.Unchecked;
    }
}
