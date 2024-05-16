import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    clip: true
    radius: 20
    color: getButtonColor()
    Layout.fillWidth: true
    Layout.minimumWidth: 40
    Layout.minimumHeight: 40
    Layout.maximumWidth: implicitWidth
    implicitHeight: layout.implicitHeight
    implicitWidth: layout.implicitWidth + (!!root.text ? 40 : 0 )

    property string text
    property string icon
    property real iconSize: 30
    signal buttonClicked()

    function getButtonColor() {
        if (!enabled) return Colors.gray
        if (area.containsPress) return Colors.accent
        if (area.containsMouse) return Colors.accentLight
        return Colors.white
    }

    Behavior on color {
        ColorAnimation { duration: 100 }
    }

    RowLayout {
        id: layout
        spacing: 10
        uniformCellSizes: false
        anchors.centerIn: parent
        Layout.alignment: Qt.AlignLeft | Qt.AlignVCenter

        Image {
            id: image
            source: root.icon
            visible: !!root.icon
            fillMode: Image.PreserveAspectFit
            sourceSize: Qt.size(root.iconSize, root.iconSize)
        }
    
        Text {
            id: text
            text: root.text
            font.pixelSize: 24
            visible: !!root.text
            font.family: balooChettan.font.family
        }
    }

    MouseArea {
        id: area
        hoverEnabled: true
        anchors.fill: parent
        onClicked: root.buttonClicked()
    }
}
