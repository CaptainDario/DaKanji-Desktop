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
        """[summary]

        Args:
            data_uri_image ([type]): [description]
        """
        
        #convert the image from data_uri to PIL.Image
        img_base_64 = urllib.request.urlopen(data_uri_image)
        image = Image.open(img_base_64.file)
        image = image.resize(size=(64, 64), resample=Image.ANTIALIAS, reducing_gap=2.0)

        #convert image to np.array and make it grayscale
        image = np.array(image)
    
        # 'convert' image to grayscale and normalize between (0, 1)
        image = image[..., -1]
        image[image > 50] = 255
        image = image / image.max()

        plt.imshow(image)
        plt.show()

        print("Image converted in python")
