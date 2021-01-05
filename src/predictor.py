import os
import pickle

import numpy as np
import sklearn      # not directly accessed but loaded via pickle

import tflite_runtime.interpreter as tflite



class Predictor():
    """ Can predict hand drawn Kanji characters from images using tf_lite.

    Attributes:
        kanji_interpreter  (Interpreter) : The tf_lite interpreter which is used to predict characters
        input_details             (dict) : The input details of 'kanji_interpreter'.
        output_details            (dict) : The output details of 'kanji_interpreter'.
        label_binarizer (LabelBinarizer) : Decodes one hot encoded output from the tf_lite model.
    """

    def __init__(self) -> None:
        self.kanji_interpreter = None
        self.input_details     = None
        self.output_details    = None
        self.label_binarizer   = None

        self.init_label_binarizer()
        self.init_tf_lite_model()
    
    def init_label_binarizer(self):
        """ Load the pickled LabelBinarizer from 'data'-folder.
        """

        with open(os.path.join("data", "labels"), "rb") as f:
            self.label_binarizer = pickle.load(f)

    def init_tf_lite_model(self):
        """ Load the tf_lite model from the 'data'-folder.
        """

        # load model
        path_to_model = os.path.join("data", "model.tflite")
        self.kanji_interpreter = tflite.Interpreter(model_path=path_to_model)
        self.kanji_interpreter.allocate_tensors()

        # get in-/output details
        self.input_details = self.kanji_interpreter.get_input_details()
        self.output_details = self.kanji_interpreter.get_output_details()
