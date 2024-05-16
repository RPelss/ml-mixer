import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {
    id: root
    anchors.fill: parent
    color: Colors.translucentBackground
    
    signal close()
    signal open()

    MouseArea {
        hoverEnabled: true
        anchors.fill: parent
        onClicked: root.close()
    }

    Rectangle {
        id: modal
        radius: 20
        color: Colors.white
        anchors.centerIn: parent
        width: layout.implicitWidth + 20
        height: layout.implicitHeight + 20

        MouseArea { anchors.fill: parent }

        ColumnLayout {
            id: layout
            spacing: 10
            anchors.centerIn: parent

            RowLayout {
                Layout.fillWidth: true

                Text {
                    id: title
                    font.pixelSize: 24
                    Layout.fillWidth: true
                    text: i18n.t.common.about
                    font.family: balooChettan.font.family
                }

                CustomButton {
                    id: closeButton
                    icon: "../assets/icons/close.svg"
                    onButtonClicked: root.close()
                }
            }

            Text {
                id: credits
                font.pixelSize: 16
                text: i18n.t.credits
                wrapMode: Text.WordWrap
                textFormat: Text.StyledText
                linkColor: Colors.accentDark
                font.family: balooChettan.font.family
                onLinkActivated: Qt.openUrlExternally(link)
                Layout.maximumWidth: languageSwitch.implicitWidth
            }

            LanguageSwitch { id: languageSwitch }
        }
    }
}