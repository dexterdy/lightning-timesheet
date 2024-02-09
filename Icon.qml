import QtQuick
Text {
    required property string icon
    default property int size: 32
    font.family: iconFont.name
    font.pixelSize: size
    text: icon
}