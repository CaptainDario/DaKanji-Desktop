import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from kanji import Kanji
from canvas import Canvas

kanjis = []
nr_kanji = 10
python_canvas = Canvas()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()
    #set kanji object references
    for i in range(nr_kanji):
        kanjis.append(Kanji(""))
        ctx.setContextProperty("kanji_" + str(i), kanjis[i])

    #set the canvas object reference
    ctx.setContextProperty("python_canvas", python_canvas)

    engine.load("main.qml")

    sys.exit(app.exec_())