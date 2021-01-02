import sys
import os

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine

from prediction_button import PredictionButton
from canvas import Canvas


from etl_data_reader import ETL_data_reader
from etl_data_names import ETL_data_names
from etl_character_groups import ETL_character_groups



predictionButtons = []
nr_kanji = 10
python_canvas = Canvas()

if __name__ == "__main__":

    reader = ETL_data_reader(r"E:\projects\DaKanjiRecognizer\dataset")
    imgs, labels = reader.read_dataset_whole(ETL_character_groups.kanji)

    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()

    ctx = engine.rootContext()
    #set kanji object references
    for i in range(nr_kanji):
        predictionButtons.append(PredictionButton(""))
        ctx.setContextProperty("predictionButton_" + str(i), predictionButtons[i])

    #set the canvas object reference
    ctx.setContextProperty("python_canvas", python_canvas)

    engine.load("main.qml")

    sys.exit(app.exec_())