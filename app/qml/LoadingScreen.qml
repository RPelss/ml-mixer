import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    anchors.fill: parent
    color: Colors.translucentBackground
    
    property string statusText

    signal close()
    signal open()

    MouseArea {
        hoverEnabled: true
        anchors.fill: parent
    }

    Rectangle {
        id: container
        width: size
        height: size
        color: 'transparent'
        anchors.centerIn: parent
        anchors.verticalCenterOffset : - modal.height

        property int size: 120

        Rectangle {
            id: shadow
            radius: 20
            x: rect.x + 5
            y: rect.y + 5
            width: rect.width
            height: rect.height
            color: Colors.black
        }

        Rectangle {
            id: rect
            radius: 20
            width: size
            height: size
            color: Colors.accent

            property int size: 40
            property int duration: 500
            property int easing: Easing.InOutBack

            SequentialAnimation {
                running: root.visible
                loops: Animation.Infinite
                alwaysRunToEnd: true
                PropertyAnimation { target: rect; property: "width"; from: rect.size; to: container.size; duration: rect.duration; easing.type: rect.easing }
                ParallelAnimation {
                    PropertyAnimation { target: rect; property: "width"; from: container.size; to: rect.size; duration: rect.duration; easing.type: rect.easing }
                    PropertyAnimation { target: rect; property: "x"; from: 0; to: container.size - rect.size; duration: rect.duration; easing.type: rect.easing }
                }
                PropertyAnimation { target: rect; property: "height"; from: rect.size; to: container.size; duration: rect.duration; easing.type: rect.easing }
                ParallelAnimation {
                    PropertyAnimation { target: rect; property: "height"; from: container.size; to: rect.size; duration: rect.duration; easing.type: rect.easing }
                    PropertyAnimation { target: rect; property: "y"; from: 0; to: container.size - rect.size; duration: rect.duration; easing.type: rect.easing }
                }
                ParallelAnimation {
                    PropertyAnimation { target: rect; property: "width"; from: rect.size; to: container.size; duration: rect.duration; easing.type: rect.easing }
                    PropertyAnimation { target: rect; property: "x"; from: container.size - rect.size; to: 0; duration: rect.duration; easing.type: rect.easing }
                }
                PropertyAnimation { target: rect; property: "width"; from: container.size; to: rect.size; duration: rect.duration; easing.type: rect.easing }
                ParallelAnimation {
                    PropertyAnimation { target: rect; property: "height"; from: rect.size; to: container.size; duration: rect.duration; easing.type: rect.easing }
                    PropertyAnimation { target: rect; property: "y"; from: container.size - rect.size; to: 0; duration: rect.duration; easing.type: rect.easing }
                }
                PropertyAnimation { target: rect; property: "height"; from: container.size; to: rect.size; duration: rect.duration; easing.type: rect.easing }
            }
        }
    }

    Rectangle {
        id: modal
        radius: 20
        color: Colors.white
        anchors.margins: 20
        anchors.top: container.bottom
        width: text.implicitWidth + 20
        height: text.implicitHeight + 20
        anchors.horizontalCenter: parent.horizontalCenter

        Text {
            id: text
            font.pixelSize: 24
            text: root.statusText
            anchors.centerIn: modal
            wrapMode: Text.WordWrap
            Layout.maximumWidth: 240
            font.family: balooChettan.font.family
            horizontalAlignment: Text.AlignHCenter
        }
    }
}