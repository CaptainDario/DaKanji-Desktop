import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from kanji import Kanji


if __name__ == "__main__":

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    engine.load("main.qml")

    sys.exit(app.exec_())