import urllib.request

from matplotlib import pyplot as plt
import  numpy as np
from PIL import Image

from PySide6 import QtCore



class Canvas(QtCore.QObject):
    
    image = None
    
    def __init__(self):
        QtCore.QObject.__init__(self)

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
            image = np.array(image)
        
            # 'convert' image to grayscale and normalize between (0, 1)
            image = image[..., -1]
            image[image > 50] = 255
            image = image / image.max()

            print("Image converted in python")
