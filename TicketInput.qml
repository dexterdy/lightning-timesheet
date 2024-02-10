import QtQuick
import QtQuick.Controls

Item {
    implicitWidth: input.implicitWidth
    implicitHeight: input.implicitHeight
    TextField {
        id: input
        anchors.fill: parent
        placeholderText: "Number or Title"
        onPressed: openPopup()
        onTextEdited: openPopup()
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
                model: backend.issues
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