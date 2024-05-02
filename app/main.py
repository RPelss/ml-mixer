import sys
from os import path

from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine

from backend import Backend

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

engine.load(path.abspath(path.join(path.dirname(__file__), 'qml/app.qml')))

backend = Backend(engine)

engine.rootObjects()[0].setProperty('backend', backend)

sys.exit(app.exec())