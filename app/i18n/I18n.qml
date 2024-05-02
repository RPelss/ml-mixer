import QtQuick

import "lv.mjs" as Lv
import "en.mjs" as En

QtObject {
    property var t: {Lv.t}

    property var languages: ({
        lv: (Lv.t),
        en: (En.t)
    })

    property var changeLanguage: (to) => {
        t = to
    }
}
