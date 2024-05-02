const t = {
    common: {
        about: "About",
        cancel: "Cancel",
        new: "Start separation",
        open: "Open",
        save: "Save",
    },
    languages: {
        title: "Language:",
        en: "English",
        lv: "Latviešu"
    },
    modelState: [
        "Initializing model", // INITIALISING, 
        "Pre-processing audio", // PRE_PROCESSING, 
        "Waiting for results from model", // WAITING_FROM_MODEL, 
        "Post-processing model results", // POST_PROCESSING, 
        "...", // IDLING
    ],
    tracks: {
        bass: "Bass",
        drums: "Drums",
        mix: "Mix",
        other: "Other",
        vocals: "Vocals"
    },
    fileDialog: {
        openFolder: "Select folder",
    },
    credits: "<p>This program and the machine learning model used by it was developed by Rūdolfs Pelšs for his LBTU bachelor thesis in 2024.</p>" 
    + "Model was trained with <a href='https://www.tensorflow.org' target='_blank'>Tensorflow</a> using <a href='https://sigsep.github.io/datasets/musdb.html' target='_blank'>MUSDB18</a> dataset." 
    + "<br>UI was implemented using <a href='https://riverbankcomputing.com/software/pyqt' target='_blank'>PyQt6</a>."
    + "<br>Icons were taken from <a href='https://www.svgrepo.com' target='_blank'>SVG Repo</a>."
};

export {t}
