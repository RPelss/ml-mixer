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
    property double timeSliderTo: 1 
    property int maxColumns: 5

    Connections {
        target: backend

        function onSetNewSong(title, sampleCount) {
            songTitle = title
            timeSliderTo = sampleCount
        }

        function onSetPlayerProgressBarValue(newValue) {
            progressBarSlider.value = newValue
        }

        function onShowOpenAudioFileDialog() {
            openAudioFileDialog.open()
        }
    }

    GridLayout  {
        columns: maxColumns
        anchors.fill: parent

        /** 
            Buttons 
        **/
        // Open
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onFileOpenClicked()
            }
            Text {
                font.pixelSize: 24
                text: "Open"
            }
        }

        // Play / Pause / Resume
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onPlayPauseClicked()
            }
            Text {
                font.pixelSize: 24
                text: "Play"
            }
        }

        // Stop
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            MouseArea {
                anchors.fill: parent
                onClicked: backend.onStopClicked()
            }
            Text {
                font.pixelSize: 24
                text: "Stop"
            }
        }

        // Title
        Text {
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: 4
            text: songTitle
            font.pixelSize: 24
        }

        // Progress bar
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Layout.columnSpan: maxColumns
            Slider {
                id: progressBarSlider
                objectName: "progressBarSlider"
                anchors.fill: parent
                from: 0
                to: timeSliderTo
                value: 0.25
                stepSize: 1.0
                // live: false
                onMoved: backend.onSongProgressBarChanged(value);
            }
        }

        // Volume sliders
        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 1
                orientation: Qt.Vertical
                onMoved: backend.onVolumeSliderChanged("MIX", value);
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 1
                orientation: Qt.Vertical
                onMoved: backend.onVolumeSliderChanged("DRUMS", value);
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 1
                orientation: Qt.Vertical
                onMoved: backend.onVolumeSliderChanged("BASS", value);
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 1
                orientation: Qt.Vertical
                onMoved: backend.onVolumeSliderChanged("VOCALS", value);
            }
        }

        Rectangle {
            width: 100; height: 100
            color: "white"
            Layout.fillHeight: true
            Layout.fillWidth: true
            Slider {
                anchors.fill: parent
                from: 0
                to: 1
                value: 1
                orientation: Qt.Vertical
                onMoved: backend.onVolumeSliderChanged("OTHER", value);
            }
        }
    }

    FileDialog {
        id: openAudioFileDialog
        acceptLabel: "Open"
        rejectLabel: "Cancel"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Audio files (*.wav *.mp3)"]
        onAccepted: backend.onFileDialogAccept(selectedFile.toString().replace(/^(file:\/{3})/, ""))
    }
}