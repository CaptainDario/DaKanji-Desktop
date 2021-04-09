import os
import tempfile

from PySide2 import QtCore

import about


class Settings(QtCore.QObject):
    """
    testse
    """

    dict_changed = QtCore.Signal(str)
    mode_changed = QtCore.Signal(int)
    invert_presses_changed = QtCore.Signal(bool)
    version_changed = QtCore.Signal(str)


    def __init__(self) -> None:
        QtCore.QObject.__init__(self)
        
        self._dict = r"https://jisho.org/search/%X%"
        self._mode = 0
        self._invert_presses = False 
        self._version = about.version

    def __str__(self):
        return self.dict + "\n" + str(self.mode) + "\n" + str(self.invert_presses)


    @QtCore.Property(str, notify=dict_changed)
    def dict(self):
        return self._dict

    @dict.setter
    def dict(self, dict):
        self._dict = dict
        self.dict_changed.emit(dict)
        self.save()
    
    @QtCore.Property(int, notify=mode_changed)
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        self._mode = mode
        self.mode_changed.emit(mode)
        self.save()
    
    @QtCore.Property(bool, notify=invert_presses_changed)
    def invert_presses(self):
        return self._invert_presses

    @invert_presses.setter
    def invert_presses(self, invert_presses):
        self._invert_presses = invert_presses
        self.mode_changed.emit(invert_presses)
        self.save()
    
    @QtCore.Property(str, notify=version_changed)
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version
        self.version_changed.emit(version)
        self.save()


    def save(self):
        """ Saves this settings object to the temp dir.
        """

        temp_path = os.path.join(tempfile.gettempdir(), "DaKanji")
        settings_file = os.path.join(temp_path, "settings.dk")

        # if there is on directory for DaKanji in the temp folder create one
        if(not os.path.isdir(temp_path)):
            os.mkdir(temp_path)

        with open(settings_file, "w+") as f:
            f.write(str(self))

    def load(self):
        """ Loads a settings object from tempdir.
        """
        temp_path = os.path.join(tempfile.gettempdir(), "DaKanji")
        settings_file = os.path.join(temp_path, "settings.dk")

        # if there is no directory for DaKanji in the temp folder create one
        if(not os.path.isdir(temp_path)):
            os.mkdir(temp_path)

        # if no settings file exists create one
        if(not os.path.exists(settings_file)):
            self.save()

        # load the settings from file
        with open(settings_file, "r+") as f:
            lines = f.readlines()
            self.dict = lines[0].rstrip("\n")
            self.mode = int(lines[1].rstrip("\n"))
            self.invert_presses = bool(lines[2].rstrip("\n"))

