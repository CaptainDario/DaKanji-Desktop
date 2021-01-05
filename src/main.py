import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from ui import Ui



if __name__ == "__main__":

    # init app
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    
    # connect the QML with python
    ui = Ui(engine.rootContext())
    
    # setup and load QML
    engine.load(os.path.join("ui", "main.qml"))


    sys.exit(app.exec_())