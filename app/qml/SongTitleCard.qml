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

        anchors.fill: parent
        anchors.leftMargin: 20

        Image {
            id: image
            source: "../assets/icons/note.svg"
            fillMode: Image.PreserveAspectFit
            sourceSize: Qt.size(root.iconSize, root.iconSize)
        }
    
        Rectangle {
            id: textContainer
            clip: true
            color: "transparent"
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignVCenter | Qt.AlignLeft

            function applyTextScroll() {
                if (textContainer.width < text.width) {
                    textScrollAnimation.running = true
                }
                else {
                    textScrollAnimation.running = false
                    text.x = 0
                }
            }

            onWidthChanged: applyTextScroll()

            PropertyAnimation {
                id: textScrollAnimation
                to: 0
                target: text
                property: "x"
                duration: root.text.length * 200
                loops: Animation.Infinite
                from: textDouble.width
            }

            Text {
                id: text
                font.pixelSize: 32
                font.family: balooChettan.font.family
                anchors.verticalCenter: parent.verticalCenter
                text: root.text + (textScrollAnimation.running ? " | " : "")

                onTextChanged: textContainer.applyTextScroll()
            }

            Text {
                id: textDouble
                font.pixelSize: 32
                text: root.text + " | "
                anchors.right: text.left
                visible: textScrollAnimation.running
                font.family: balooChettan.font.family
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
