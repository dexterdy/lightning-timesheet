import QtQuick
import QtQuick.Controls
import GithubIssuesModel 1.0

Item {
    implicitWidth: input.implicitWidth
    implicitHeight: input.implicitHeight
    TextField {
        id: input
        anchors.fill: parent
        placeholderText: "Ticket Title"
        onPressed: openPopup()
        onTextEdited: {
            issuesList.model.filterIssues(this.text)
            openPopup()
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
                id: issuesList
                clip: true
                model: GithubIssuesModel {}
                delegate: Button {
                    text: title
                }
            }
        }
    }
    function openPopup()
    {
        if (!popup.opened)
        {
            popup.open()
        }
    }
}