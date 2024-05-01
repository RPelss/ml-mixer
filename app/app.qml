import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Dialogs

import AudioPlayer 1.0
import "."

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "HelloApp"
    color: Colors.background

    property QtObject backend
    property int maxColumns: 5
    property int playerState: Player.NO_TRACK

    function urlToPath(url) {
        return url.toString().replace(/^(file:\/{3})/, "")
    }

    Connections {
        target: backend

        function onSetNewSong(title, songLengthSeconds) {
            songTitle.text = title
            progressBar.maxValueSeconds = songLengthSeconds
        }

        function onSetPlayerProgressBarValue(newValueSeconds) {
            progressBar.valueSeconds = newValueSeconds
        }

        function onShowOpenAudioFileDialog() {
            openAudioFileDialog.open()
        }

        function onShowExportAudioFolderDialog() {
            exportAudioFileDialog.open()
        }

        function onShowImportAudioFileDialog() {
            importAudioFileDialog.open()
        }

        function onSongStateChange(newState) {
            playerState = newState
        }
    }

    ColumnLayout  {
        spacing: 10
        anchors.margins: 10
        anchors.fill: parent

        /** 
            File Buttons 
        **/
        RowLayout {
            spacing: 10
            id: fileButtonRow
            Layout.fillWidth: true
            Layout.preferredHeight: 50

            // Open
            CustomButton {
                text: "Open"
                icon: "icons/plus.svg"
                onButtonClicked: backend.onFileOpenClicked()
            }

            // Export
            CustomButton {
                text: "Export"
                icon: "icons/save.svg"
                enabled: playerState !== Player.NO_TRACK
                onButtonClicked: backend.onExportClicked()
            }

            // Import
            CustomButton {
                text: "Import"
                icon: "icons/open.svg"
                onButtonClicked: backend.onImportClicked()
            }
        }

        /** 
            Play, Stop, Name 
        **/
        RowLayout {
            spacing: 10
            Layout.fillWidth: true
            implicitHeight: playButton.implicitHeight

            // Play / Pause / Resume
            CustomButton {
                id: playButton
                iconSize: 80
                enabled: playerState !== Player.NO_TRACK
                icon: playerState === Player.PLAYING ? "icons/pause.svg" : "icons/play.svg"
                onButtonClicked: backend.onPlayPauseClicked()
            }

            // Stop
            CustomButton {
                iconSize: 80
                icon: "icons/stop.svg"
                enabled: playerState !== Player.NO_TRACK
                onButtonClicked: backend.onStopClicked()
            }

            // Title
            SongTitleCard {
                id: songTitle
                text: songTitle
            }
        }

        // Progress bar
        AudioProgressBar {
            id: progressBar
            enabled: playerState !== Player.NO_TRACK
            onMoved: backend.onSongProgressBarChanged(valueSeconds); 
        }

        /** 
            Volume sliders 
        **/
        RowLayout {
            spacing: 10
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignHCenter

            // Mix
            VolumeSlider {
                text: "Mix"
                icon: "icons/mix.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.MIX, value);
            }
            // Drums
            VolumeSlider {
                text: "Drums"
                icon: "icons/drums.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.DRUMS, value);
            }
            // Bass
            VolumeSlider {
                text: "Bass"
                icon: "icons/guitar.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.BASS, value);
            }
            // Vocals
            VolumeSlider {
                text: "Vocals"
                icon: "icons/microphone.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.VOCALS, value);
            }
            // Others
            VolumeSlider {
                text: "Others"
                icon: "icons/piano.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.OTHER, value);
            }
        }
    }
    FileDialog {
        id: openAudioFileDialog
        acceptLabel: "Open"
        rejectLabel: "Cancel"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Audio files (*.wav *.mp3)"]
        onAccepted: backend.onFileDialogAccept(urlToPath(selectedFile))
    }
    FileDialog {
        id: importAudioFileDialog
        acceptLabel: "Open"
        rejectLabel: "Cancel"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Audio files (*.mp4 *.m4a)"]
        onAccepted: backend.onImportFileAccept(urlToPath(selectedFile))
    }
    FolderDialog {
        id: exportAudioFileDialog
        acceptLabel: "Select Folder"
        rejectLabel: "Cancel"
        onAccepted: backend.onExportFolderAccept(urlToPath(selectedFolder))
    }
}