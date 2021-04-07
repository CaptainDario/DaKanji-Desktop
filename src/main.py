import sys
import os
import pyinstaller 

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from ui import Ui



if __name__ == "__main__":

    # init app
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    clip = app.clipboard()

    # connect QML and python
    ui = Ui(clip, engine.rootContext())

    # setup and load QML
    engine.load(pyinstaller.resource_path(os.path.join("ui", "main.qml")))
    app.setWindowIcon(QIcon(pyinstaller.resource_path(os.path.join("icons", "icon.ico"))))

    sys.exit(app.exec_())