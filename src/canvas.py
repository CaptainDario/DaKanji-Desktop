import urllib.request
import pickle
import os

import numpy as np
from PIL import Image

from PySide6 import QtCore

import tflite_runtime.interpreter as tflite


class Canvas(QtCore.QObject):
    
    image = None

    def __init__(self):
        QtCore.QObject.__init__(self)

        self.init_tf_lite_model()
        self.init_label_binarizer()

    def init_tf_lite_model(self):

        path_to_model = r"E:\projects\DaKanjiRecognizer\model\tf\kanji_only\model.tflite"
        self.kanji_interpreter = tflite.Interpreter(model_path=path_to_model)
        self.kanji_interpreter.allocate_tensors()

        self.input_details = self.kanji_interpreter.get_input_details()
        self.output_details = self.kanji_interpreter.get_output_details()

    def init_label_binarizer(self):

        print(os.getcwd())

        with open(os.path.join("data", "labels"), "rb") as f:
            self.label_binarizer = pickle.load(f)


    @QtCore.Slot(str)
    def get_current_image(self, data_uri_image):
        """ This method gets called everytime the user finished drawing a stroke on the canvas.

        Args:
            data_uri_image (str): The data_uri which contains the image from the QMLCanvas.
        """
        
        #convert the image from data_uri to PIL.Image
        img_base_64 = urllib.request.urlopen(data_uri_image)
        image = Image.open(img_base_64.file)

        #check that image is not empty
        if(image.getbbox()):
            image = image.resize(size=(64, 64), resample=Image.ANTIALIAS, reducing_gap=2.0)

            #convert image to np.array and make it grayscale
            image = np.array(image).astype("float32")
        
            # 'convert' image to grayscale and normalize between (0, 1)
            image = image[..., -1]
            image[image > 50] = 255
            image = image / image.max()

            image = image.reshape(1, 64, 64, 1)

            print("Image converted in python")

            self.kanji_interpreter.set_tensor(self.input_details[0]["index"], image)
            self.kanji_interpreter.invoke()
            output_data = self.kanji_interpreter.get_tensor(self.output_details[0]["index"])

            out_np = np.array(output_data)

            #print the 10 most confident predictions
            for i in range(10):
                print("confidence:", out_np.max(), " --> ", self.label_binarizer.inverse_transform(out_np))

                out_np[out_np.max() == out_np] = 0.0
