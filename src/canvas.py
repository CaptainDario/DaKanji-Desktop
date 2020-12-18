from binascii import a2b_base64
import urllib.request

from PySide6 import QtCore



class Canvas(QtCore.QObject):
    
    image = None
    
    def __init__(self):
        QtCore.QObject.__init__(self)

    @QtCore.Slot(str)
    def get_current_image(self, data_uri_image):
        
        binary = urllib.request.urlopen(data_uri_image)

        with open("image.png", "wb") as f:
            f.write(binary.file.read())

        print("Image handed to python")
