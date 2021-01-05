import urllib.request

import numpy as np
from PIL import Image
import PySide6
from PySide6 import QtCore

from prediction_button import PredictionButton
from predictor import Predictor



class UI(QtCore.QObject):


    prediction_changed = QtCore.Signal(str)

    def __init__(self, context : PySide6.QtQml.QQmlContext) -> None:
        QtCore.QObject.__init__(self)
        
        self.context      = context
        self.pred_count   = 10
        self.predictor    = Predictor()
        
        self.prediction_btns = [PredictionButton("") for i in range(10)]

        self.connect_py_and_qml()


    def connect_py_and_qml(self) -> None:
        """ Con
        """
        
        #connect the canvas
        self.context.setContextProperty("ui", self)
        
        #connect the PredictionButtons
        for i in range(self.pred_count):
            name = "prediction_button_" + str(i + 1)
            self.context.setContextProperty(name, self.prediction_btns[i])
