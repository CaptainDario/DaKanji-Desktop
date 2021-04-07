import os
import ast

import numpy as np

import tflite_runtime.interpreter as tflite

from pyinstaller import resource_path


class Predictor():
    """ Can predict hand drawn Kanji characters from images using tf_lite.

    Attributes:
        kanji_interpreter  (Interpreter) : The tf_lite interpreter which is used to predict characters
        input_details             (dict) : The input details of 'kanji_interpreter'.
        output_details            (dict) : The output details of 'kanji_interpreter'.
        labels          (LabelBinarizer) : A list of all labels the CNN can recognize (ordered).
    """

    def __init__(self) -> None:
        self.kanji_interpreter = None
        self.input_details     = None
        self.output_details    = None
        self.labels   = None

        self.init_labels()
        self.init_tf_lite_model()
    
    def init_labels(self):
        """ Load the list of labels which the CNN can recognize
        """

        with open(resource_path(os.path.join("data", "labels_python_list.txt")), "r", encoding="utf8") as f:
            self.labels = ast.literal_eval(f.read())

    def init_tf_lite_model(self):
        """ Load the tf_lite model from the 'data'-folder.
        """

        # load model
        path_to_model = resource_path(os.path.join("data", "model.tflite"))
        self.kanji_interpreter = tflite.Interpreter(model_path=path_to_model)
        self.kanji_interpreter.allocate_tensors()

        # get in-/output details
        self.input_details = self.kanji_interpreter.get_input_details()
        self.output_details = self.kanji_interpreter.get_output_details()


    def predict(self, image : np.array, cnt_predictions : int) -> [str]:
        """ Predict a character from an input image.

        Args:
            image      (np.array) : A numpy array with shape (1, 64, 64, 1) and dtype 'float32' 
            cnt_predictions (int) : How many predictions should be returned ('cnt_predictions' most likely ones)

        Returns:
            A list with the 'cnt_predictions' most confident predictions.
        """

        # make prediction 
        self.kanji_interpreter.set_tensor(self.input_details[0]["index"], image)
        self.kanji_interpreter.invoke()
        output_data = self.kanji_interpreter.get_tensor(self.output_details[0]["index"])
        out_np = np.array(output_data)

        # get the 'cnt_predictions' most confident predictions
        preds = []
        for i in range(cnt_predictions):
            pred = self.labels[out_np.argmax()]
            preds.append(pred[0])

            # 'remove' this prediction from all
            out_np[out_np.max() == out_np] = 0.0

        return preds