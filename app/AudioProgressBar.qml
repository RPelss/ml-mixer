import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    radius: 20
    color: Colors.white
    Layout.fillWidth: true
    Layout.minimumHeight: 80

    property real valueSeconds: 0
    property real maxValueSeconds: 1
    signal moved()

    function formatSeconds(seconds) {
        let minutes = Math.floor(seconds / 60)
        seconds = Math.floor(seconds - minutes * 60)
        return `${minutes}:${('0' + seconds).slice(-2)}`
    }

    function getHandleColor() {
        if (!enabled) return Colors.gray
        if (slider.pressed) return Colors.accentDark
        if (hover.hovered) return Colors.accentLight
        return Colors.accent
    }

    Slider {
        id: slider
        from: 0
        live: true
        stepSize: 1.0
        to: root.maxValueSeconds
        value: root.valueSeconds
        anchors.fill: parent
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        onMoved: () => {
            root.valueSeconds = value
            root.moved()
        }

        background: Rectangle {
            radius: 2
            implicitHeight: 4
            x: slider.leftPadding
            height: implicitHeight
            width: slider.availableWidth
            color: root.enabled ? Colors.black : Colors.gray
            y: slider.topPadding + slider.availableHeight / 2 - height / 2

            Behavior on color {
                ColorAnimation { duration: 100 }
            }

            Rectangle {
                radius: 2
                height: parent.height
                width: slider.visualPosition * parent.width
                color: root.enabled ? Colors.accent : Colors.darkGray

                Behavior on color {
                    ColorAnimation { duration: 100 }
                }
            }
        }

        handle: Rectangle {
            radius: 10
            implicitWidth: 20
            implicitHeight: 20
            color: getHandleColor()
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)

            Behavior on color {
                ColorAnimation { duration: 100 }
            }
        }
    }

    Text {
        anchors.top: slider.bottom
        anchors.left: root.left
        anchors.topMargin: -20
        anchors.leftMargin: 20
        font.pixelSize: 16
        text: root.enabled 
        ? `${formatSeconds(root.valueSeconds)} / ${formatSeconds(root.maxValueSeconds)}`
        : '--:-- / --:--'
    }

    HoverHandler {
        id: hover
    }
}
