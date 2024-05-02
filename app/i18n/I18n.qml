import QtQuick

import "lv.mjs" as Lv
import "en.mjs" as En

QtObject {
    property var t: {Lv.t}

    property var swap: () => {
        t = t === Lv.t ? En.t : Lv.t
    }
}
