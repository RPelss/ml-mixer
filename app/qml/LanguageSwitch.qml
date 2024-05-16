import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts

import "."

Rectangle {

    radius: 20
    color: Colors.background
    implicitWidth: buttons.implicitWidth + 10
    implicitHeight: buttons.implicitHeight + 10

    GridLayout {
        id: buttons
        columns: 2
        rowSpacing: 10
        columnSpacing: 5
        anchors.margins: 10
        anchors.centerIn: parent

        Text {
            id: text
            font.pixelSize: 24
            Layout.columnSpan: 2
            text: i18n.t.languages.title
            font.family: balooChettan.font.family
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
        }

        CustomButton {
            text: i18n.t.languages.en
            enabled: i18n.t !== i18n.languages.en
            onButtonClicked: i18n.changeLanguage(i18n.languages.en)
        }
        
        CustomButton {
            text: i18n.t.languages.lv
            enabled: i18n.t !== i18n.languages.lv
            onButtonClicked: i18n.changeLanguage(i18n.languages.lv)
        }
    }
}