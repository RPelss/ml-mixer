import sys
from os import environ, pathsep

from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import QQmlApplicationEngine

from utils import getFullPath

environ["PATH"] += pathsep + getFullPath('ffmpeg/')

from backend import Backend

app = QGuiApplication(sys.argv)

app.setWindowIcon(QIcon(getFullPath('assets/icon.ico')))

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

engine.load(getFullPath('qml/app.qml'))

backend = Backend()

engine.rootObjects()[0].setProperty('backend', backend)

sys.exit(app.exec())