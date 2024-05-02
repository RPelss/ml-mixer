import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    width: 80
    radius: 20
    color: Colors.white
    Layout.fillHeight: true

    property real value: 1
    property string text
    property string icon
    property real iconSize: 50
    signal moved()

    function getHandleColor() {
        if (!enabled) return Colors.gray
        if (slider.pressed) return Colors.accentDark
        if (hover.hovered) return Colors.accentLight
        return Colors.accent
    }

    ColumnLayout {
        spacing: 5
        anchors.margins: 10
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter


        Image {
            id: image
            source: root.icon
            fillMode: Image.PreserveAspectFit
            sourceSize: Qt.size(root.iconSize, root.iconSize)
        }
    
        Text {
            id: text
            text: root.text
            font.pixelSize: 16
            Layout.alignment: Qt.AlignHCenter
            font.family: balooCheetah.font.family
        }

        Slider {
            id: slider
            to: 1
            from: 0
            live: true
            value: root.value
            Layout.fillWidth: true
            Layout.fillHeight: true
            orientation: Qt.Vertical

            onMoved: () => {
                root.value = value
                root.moved()
            }

            background: Rectangle {
                radius: 2
                implicitWidth: 4
                width: implicitWidth
                y: slider.topPadding
                height: slider.availableHeight
                color: root.enabled ? Colors.accent : Colors.darkGray
                x: slider.leftPadding + slider.availableWidth / 2 - width / 2

                Behavior on color {
                    ColorAnimation { duration: 100 }
                }

                Rectangle {
                    radius: 2
                    width: parent.width
                    height: slider.visualPosition * parent.height
                    color: root.enabled ? Colors.black : Colors.gray

                    Behavior on color {
                        ColorAnimation { duration: 100 }
                    }
                }
            }

            handle: Rectangle {
                radius: 5
                implicitWidth: 30
                implicitHeight: 10
                color: getHandleColor()
                x: slider.leftPadding + slider.availableWidth / 2 - width / 2
                y: slider.topPadding + slider.visualPosition 
                * (slider.availableHeight - height)

                Behavior on color {
                    ColorAnimation { duration: 100 }
                }
            }

            HoverHandler {
                id: hover
            }
        }   
    }
}
