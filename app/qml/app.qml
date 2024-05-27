import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Layouts
import QtQuick.Dialogs

import AudioPlayer 1.0
import MLModel 1.0
import "../i18n"
import "."

ApplicationWindow {
    id: app
    width: 800
    height: 600
    visible: true
    title: "MM Mikseris"
    color: Colors.background

    minimumWidth: Math.max(fileButtonRow.implicitWidth, volumeSliders.implicitWidth) + 25
    minimumHeight: 500

    property QtObject backend
    property int playerState: Player.NO_TRACK
    property int modelState: Model.INITIALISING

    function urlToPath(url) {
        return url.toString().replace(/^(file:\/{3})/, "")
    }

    Connections {
        target: backend

        function onModelStateChanged(newState) {
            modelState = newState
        }

        function onSetNewSong(title, songLengthSeconds) {
            loadingScreen.close()
            songTitle.text = title
            progressBar.maxValueSeconds = songLengthSeconds
        }

        function onSetPlayerProgressBarValue(newValueSeconds) {
            progressBar.valueSeconds = newValueSeconds
        }

        function onShowOpenAudioFileDialog() {
            openAudioFileDialog.open()
        }

        function onShowExportAudioFileDialog(defaultFile) {
            exportAudioFileDialog.selectedFile = defaultFile
            exportAudioFileDialog.open()
        }

        function onShowImportAudioFileDialog() {
            importAudioFileDialog.open()
        }

        function onSongStateChanged(newState) {
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
            id: fileButtonRow
            spacing: 10
            Layout.fillWidth: true
            Layout.preferredHeight: 50

            // New
            CustomButton {
                text: i18n.t.common.new
                icon: "../assets/icons/plus.svg"
                onButtonClicked: backend.onFileOpenClicked()
            }

            // Export
            CustomButton {
                text: i18n.t.common.save
                icon: "../assets/icons/save.svg"
                enabled: playerState !== Player.NO_TRACK
                onButtonClicked: backend.onExportClicked()
            }

            // Import
            CustomButton {
                text: i18n.t.common.open
                icon: "../assets/icons/open.svg"
                onButtonClicked: backend.onImportClicked()
            }

            // About
            CustomButton {
                text: i18n.t.common.about
                icon: "../assets/icons/info.svg"
                onButtonClicked: aboutModal.open()
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
                icon: playerState === Player.PLAYING ? "../assets/icons/pause.svg" : "../assets/icons/play.svg"
                onButtonClicked: backend.onPlayPauseClicked()
            }

            // Stop
            CustomButton {
                iconSize: 80
                icon: "../assets/icons/stop.svg"
                enabled: playerState !== Player.NO_TRACK
                onButtonClicked: backend.onStopClicked()
            }

            // Title
            SongTitleCard {
                id: songTitle
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
            id: volumeSliders
            spacing: 10
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignHCenter

            // Mix
            VolumeSlider {
                text: i18n.t.tracks.mix
                icon: "../assets/icons/mix.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.MIX, value);
            }
            // Drums
            VolumeSlider {
                text: i18n.t.tracks.drums
                icon: "../assets/icons/drums.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.DRUMS, value);
            }
            // Bass
            VolumeSlider {
                text: i18n.t.tracks.bass
                icon: "../assets/icons/guitar.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.BASS, value);
            }
            // Vocals
            VolumeSlider {
                text: i18n.t.tracks.vocals
                icon: "../assets/icons/microphone.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.VOCALS, value);
            }
            // Others
            VolumeSlider {
                text: i18n.t.tracks.other
                icon: "../assets/icons/piano.svg"
                enabled: playerState !== Player.NO_TRACK
                onMoved: backend.onVolumeSliderChanged(Player.OTHER, value);
            }
        }
    }

    LoadingScreen {
        id: loadingScreen
        visible: false
        statusText: i18n.t.modelState[modelState]
        onOpen: visible = true;
        onClose: visible = false;
    }

    AboutModal {
        id: aboutModal
        visible: false
        onOpen: visible = true;
        onClose: visible = false;
    }

    FontLoader { 
        id: balooChettan
        source: "../assets/fonts/BalooChettan2-VariableFont_wght.ttf" 
    }

    I18n {id: i18n}

    FileDialog {
        id: openAudioFileDialog
        acceptLabel: i18n.t.common.open
        rejectLabel: i18n.t.common.cancel
        fileMode: FileDialog.OpenFile
        nameFilters: [i18n.t.fileFilters.mp3]
        onAccepted: {
            loadingScreen.open()
            backend.onFileDialogAccept(urlToPath(selectedFile))
        }
    }

    FileDialog {
        id: importAudioFileDialog
        acceptLabel: i18n.t.common.open
        rejectLabel: i18n.t.common.cancel
        fileMode: FileDialog.OpenFile
        nameFilters: [i18n.t.fileFilters.mp4]
        onAccepted: backend.onImportFileAccept(urlToPath(selectedFile))
    }

    FileDialog {
        id: exportAudioFileDialog
        defaultSuffix: "mp4"
        acceptLabel: i18n.t.common.save
        rejectLabel: i18n.t.common.cancel
        fileMode: FileDialog.SaveFile
        nameFilters: [i18n.t.fileFilters.mp4]
        onAccepted: backend.onExportFileAccept(urlToPath(selectedFile))
    }
}