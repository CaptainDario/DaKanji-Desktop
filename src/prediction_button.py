import pyperclip

from PySide2 import QtCore

class PredictionButton(QtCore.QObject):
    """ Python Class for connecting to QML PredictionButtons.

    Attributes:
        _character (str) : The character which is currently being showed on the
                            connected QML-button.
    """

    # signal which will be emitted when 'character' changed.
    character_changed = QtCore.Signal(str)

    def __init__(self, character):
        QtCore.QObject.__init__(self)
        self._character = character
    

    @QtCore.Property(str, notify=character_changed)
    def character(self):
        return self._character

    @character.setter
    def character(self, char):
        self._character = char
        self.character_changed.emit(char)

    @QtCore.Slot()
    def button_pressed(self):
        """ Copies the button's character to clipboard
        """

        pyperclip.copy(self.character)


