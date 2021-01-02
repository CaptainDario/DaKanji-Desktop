import random

import pyperclip

from PySide6 import QtCore

class PredictionButton(QtCore.QObject):

    def __init__(self, character):
        QtCore.QObject.__init__(self)
        self.character = character

    def generate_random_hanzi(self) -> str:
        """Generates a random chinese character.
            This is a placeholder until for developing the UI while no CNN is available.

        Returns:
            str: The randomly generated chinese character.
        """
        
        random_char = ""

        common, rare = range(0x4e00, 0xa000), range(0x3400, 0x4e00)
        chars = list(map(chr, common))
        random_char = chars[random.randint(0, len(chars))]

        return random_char


    @QtCore.Slot(result=str)
    def button_pressed(self) -> str:
        """This method gets called everytime a user clicks on this "prediction"-button.

        Returns:
            str: The character which is shown on this button.
        """

        pyperclip.copy(self.character)

        #placeholder until CNN prediction is implemented
        ###
        self.character = self.generate_random_hanzi()
        print(self.character)
        return self.character
        ###

    def __str__(self):
        return self.character

