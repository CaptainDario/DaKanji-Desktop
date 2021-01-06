# list of hidden imports for pyinstaller
from scipy.spatial.transform import _rotation_groups

#normal packages
import os, sys

# function to convert paths for pyinstaller onefile-mode
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)