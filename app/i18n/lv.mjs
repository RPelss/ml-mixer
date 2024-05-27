const t = {
    common: {
        about: "Par",
        cancel: "Atcelt",
        new: "Sākt atdalīt",
        open: "Atvērt",
        save: "Saglabāt",
    },
    fileFilters: {
        mp3: "Audio faili (*.wav *.mp3)",
        mp4: "Audio faili (*.mp4)"
    },
    languages: {
        title: "Valoda:",
        en: "English",
        lv: "Latviešu"
    },
    modelState: [
        "Inicializē modeli", // INITIALISING, 
        "Apstrādā audio nodošanai modelim", // PRE_PROCESSING, 
        "Gaida rezultātus no modeļa", // WAITING_FROM_MODEL, 
        "Apstrādā modeļa rezultātus", // POST_PROCESSING, 
        "...", // IDLING
    ],
    tracks: {
        bass: "Bass",
        drums: "Bungas",
        mix: "Kopā",
        other: "Citi",
        vocals: "Vokāli"
    },
    about: {
        credits: "<p>Šo programmu un šeit izmantoto mašīnmācīšanās modeli izstrādāja Rūdolfs Pelšs 2024. gadā priekš LBTU bakalaura darba.</p>" 
        + "Modelis tika izstrādāts ar <a href='https://www.tensorflow.org' target='_blank'>Tensorflow</a>, izmantojot <a href='https://sigsep.github.io/datasets/musdb.html' target='_blank'>MUSDB18</a> datu kopu." 
        + "<br>Vizuālā saskarne tika izstrādāta ar <a href='https://riverbankcomputing.com/software/pyqt' target='_blank'>PyQt6</a>."
        + "<br>Ikonas tika ņemtas no <a href='https://www.svgrepo.com' target='_blank'>SVG Repo</a>.",
        version: "Versija: "
    }
};

export {t}
