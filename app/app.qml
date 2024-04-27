import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs

ApplicationWindow {
    visible: true
    width: 600
    height: 500
    title: "HelloApp"
    property QtObject backend
    property string songTitle: "-"

    Connections {
        target: backend

        function onSetNewSong(title, sampleCount) {
            songTitle = title
        }

        function onShowOpenAudioFileDialog() {
            openAudioFileDialog.open()
        }
    }

    GridLayout  {
        columns: 4
        anchors.fill: parent

        // Title
        Text {
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 4
            text: songTitle
            font.pixelSize: 48
        }

        // Progress bar
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 4
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 0.25
                onMoved: backend.onSongProgressBarChanged(value);
            }
        }

        // Volume sliders
        Rectangle {
            width: 100; height: 100
            color: "red"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onClicked("red")
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "blue"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onClicked("blue")
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "green"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onClicked("green")
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "yellow"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onClicked("yellow")
            }
        }
    }

    FileDialog {
        id: openAudioFileDialog
        acceptLabel: "Open"
        rejectLabel: "Cancel"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Audio files (*.wav *.mp3)"]
        onAccepted: backend.onFileDialogAccept(selectedFile)
    }
}