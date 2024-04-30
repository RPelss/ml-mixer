import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    width: 100; height: 100
    color: "white"
    Layout.fillHeight: true
    Layout.fillWidth: true

    property string text: ""
    signal buttonClicked()

    MouseArea {
        anchors.fill: parent
        onClicked: root.buttonClicked
    }
    Text {
        font.pixelSize: 24
        text: root.text
    }
}