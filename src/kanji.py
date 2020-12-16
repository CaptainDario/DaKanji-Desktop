import pyperclip

from PySide6 import QtCore

class Kanji(QtCore.QObject):

    def __init__(self, character):
        QtCore.QObject.__init__(self)
        self.character = character
        self.number = 12

    @QtCore.Slot()
    def out(self):
        pyperclip.copy(self.character)
        print(self.character)

    def __str__(self):
        return 'Person "{}" {}'.format(self.character, self.number)

