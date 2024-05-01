import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    radius: 20
    color: Colors.gray

    Layout.minimumHeight: 80
    Layout.fillWidth: true

    property string text: "-"
    property real iconSize: 50

    RowLayout {
        id: layout
        spacing: 20
        uniformCellSizes: false

        anchors.left: parent.left
        anchors.verticalCenter: parent.verticalCenter
        anchors.leftMargin: 20

        Image {
            id: image
            source: "icons/note.svg"
            sourceSize: Qt.size(root.iconSize, root.iconSize)
            fillMode: Image.PreserveAspectFit
        }
    
        Text {
            id: text
            font.pixelSize: 32
            text: root.text
        }
    }
}
