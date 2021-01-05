import sys
import os
import hidden_import

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

from ui import Ui



if __name__ == "__main__":

    # init app
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    # connect QML and python
    ui = Ui(engine.rootContext())
    
    # setup and load QML
    engine.load(os.path.join("ui", "main.qml"))
    app.setWindowIcon(QIcon("./icons/icon_eye_only.ico"))

    sys.exit(app.exec_())