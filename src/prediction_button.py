import random

import pyperclip

from PySide6 import QtCore

class PredictionButton(QtCore.QObject):
    """ 

    Attributes:
        _character (str) : The character which is currently being showed on this button.
    """

    character_changed = QtCore.Signal(str)

    def __init__(self, character):
        QtCore.QObject.__init__(self)
        self._character = character

    def __str__(self):
        return self.character
    
    
    @QtCore.Property(str, notify=character_changed)
    def character(self):
        return self._character

    @character.setter
    def character(self, char):
        self._character = char
        self.character_changed.emit(char)

    @QtCore.Slot()
    def button_pressed(self):
        """This method gets called everytime a user clicks on this "prediction"-button.
        """

        pyperclip.copy(self.character)


