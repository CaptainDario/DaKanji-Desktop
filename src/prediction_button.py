import webbrowser

from PySide2 import QtCore
from PySide2.QtGui import QClipboard


class PredictionButton(QtCore.QObject):
    """ Python Class for connecting to QML PredictionButtons.

    Attributes:
        _character (        str) : The character which is currently being
                                   showed on the connected QML-button.
        clipboard   (QClipboard) : The OS's clipboard.
    """

    # signal which will be emitted when 'character' changed.
    character_changed = QtCore.Signal(str)

    def __init__(self, clipboard : QClipboard):
        QtCore.QObject.__init__(self)
        self._character = ""
        self.clipboard = clipboard
    

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

        self.clipboard.setText(self.character)
        
        if (self.clipboard.supportsSelection()): 
            self.clipboard.setText(self.character, QClipboard.Selection)
        
    
    @QtCore.Slot()
    def button_long_pressed(self):
        """ Opens the character in the dictionary of choice.
        """

        if(self.character != ""):
            webbrowser.open("https://jisho.org/search/" + self.character + "%23kanji")

