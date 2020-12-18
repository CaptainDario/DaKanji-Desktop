import random

import pyperclip

from PySide6 import QtCore

class Kanji(QtCore.QObject):

    def __init__(self, character):
        QtCore.QObject.__init__(self)
        self.character = character

    def generate_random_hanzi(self):
        
        random_word = ""

        common, rare = range(0x4e00, 0xa000), range(0x3400, 0x4e00)
        chars = list(map(chr, common))
        random_word = chars[random.randint(0, len(chars))]

        return random_word

    @QtCore.Slot(result=str)
    def copy_character(self):

        self.character = self.generate_random_hanzi()

        pyperclip.copy(self.character)
        print(self.character)

        return self.character

    def __str__(self):
        return 'Person "{}" {}'.format(self.character, self.number)

