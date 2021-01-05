import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from prediction_button import PredictionButton
from canvas import Canvas


predictionButtons = []
nr_kanji = 10
python_canvas = Canvas()

if __name__ == "__main__":

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()
    #set kanji object references
    for i in range(nr_kanji):
        predictionButtons.append(PredictionButton(""))
        ctx.setContextProperty("predictionButton_" + str(i), predictionButtons[i])

    #set the canvas object reference
    ctx.setContextProperty("python_canvas", python_canvas)

    engine.load(os.path.join("ui", "main.qml"))

    sys.exit(app.exec_())