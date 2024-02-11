import QtQuick
import QtQuick.Controls
import GithubIssuesModel

Item {
    id: root
    signal select(int number)
    property alias text: input.text
    implicitWidth: input.implicitWidth
    implicitHeight: input.implicitHeight
    TextField {
        id: input
        anchors.fill: parent
        placeholderText: "Ticket Title"
        onPressed: {
            if (this.readOnly) {
                this.text = "";
                this.readOnly = false;
            }
            openPopup();
        }
        onTextEdited: {
            issues.filterIssues(this.text);
            openPopup();
        }
    }
    Popup {
        id: popup
        y: parent.height
        x: 0
        width: parent.width
        height: 200
        modal: true
        ScrollView {
            anchors.fill: parent
            ListView {
                clip: true
                model: GithubIssuesModel {
                    id: issues
                }
                delegate: Button {
                    text: title
                    onClicked: {
                        input.text = title;
                        input.readOnly = true;
                        root.select(number);
                    }
                }
            }
        }
    }
    function openPopup() {
        if (!popup.opened) {
            popup.open();
        }
    }
    function reset() {
        input.readOnly = false;
        input.text = "";
    }
    function updateIssues() {
        issues.updateIssues();
    }
}
