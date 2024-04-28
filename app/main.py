import sys
import os

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

from backend import Backend

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('./app.qml')

backend = Backend(engine)

engine.rootObjects()[0].setProperty('backend', backend)

sys.exit(app.exec())