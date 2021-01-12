import urllib.request

import numpy as np
from PIL import Image
import PySide2
from PySide2 import QtCore
from PySide2.QtGui import QClipboard

from prediction_button import PredictionButton
from predictor import Predictor



class Ui(QtCore.QObject):
    """ A Bridge class between UML and python.

    Attributes:
        context                (QQmlContext) : The QQmlContext of the application.
        pred_count                     (int) : How many of the likeliest
                                               predictions should be used.
        predictor                (Predictor) : Predictor instace which
                                               runs the inference tasks.
        prediction_btns ([PredictionButton]) : List with PredictionButton
                                               instances connected to the
                                               QML buttons.
        clipboard               (QClipboard) : The OS's clipboard.
    """


    prediction_changed = QtCore.Signal(str)

    def __init__(self, clipboard : QClipboard, context : PySide2.QtQml.QQmlContext) -> None:
        QtCore.QObject.__init__(self)
        
        self.context         = context
        self.pred_count      = 10
        self.predictor       = Predictor()
        self.prediction_btns = [PredictionButton(clipboard) for i in range(10)]
        self.clipboard       = clipboard

        self.connect_py_and_qml()


    def connect_py_and_qml(self) -> None:
        """ Connect the python objects and attributes with QML.
        """
        
        #connect the canvas
        self.context.setContextProperty("ui", self)
        
        #connect the PredictionButtons
        for i in range(self.pred_count):
            name = "prediction_button_" + str(i + 1)
            self.context.setContextProperty(name, self.prediction_btns[i])


    @QtCore.Slot(str)
    def predict_from_image(self, data_uri_image):
        """ Predict the character on the QML Canvas.
        
        First converts the "data_uri"-image to a numpy array.
        Afterwards runs inference on the tf_lite model and saves predictions.

        Note:
            This method gets called everytime the user finished drawing a stroke on the canvas.

        Args:
            data_uri_image (str): The data_uri which contains the image from the QMLCanvas.
        """
        
        # convert the image from data_uri to PIL.Image
        img_base_64 = urllib.request.urlopen(data_uri_image)
        image = Image.open(img_base_64.file)

        # check that image is not empty
        if(image.getbbox()):
            image = image.resize(size=(64, 64), resample=Image.ANTIALIAS, reducing_gap=2.0)

            # convert image to np.array and make it grayscale
            image = np.array(image).astype("float32")
        
            # 'convert' image to grayscale and normalize between (0, 1)
            image = image[..., -1]
            image[image > 50] = 255
            image = image / image.max()

            image = image.reshape(1, 64, 64, 1)

            # predict
            predictions = self.predictor.predict(image, self.pred_count)
            for cnt, pred in enumerate(predictions):
                self.prediction_btns[cnt].character = pred

            