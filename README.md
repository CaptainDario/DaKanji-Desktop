# DaKanjiRecognizer
<img src="./media/social_preview.png" style="display:block;margin-left:auto;margin-right:auto;" width="60%"/>

## What is this?

A simple app which can predict japanese kanji characters which were drawn by hand.
The predictions can than be copied and used elsewhere. <br/>
Currently ~3000 kanji characters are supported.

<img src="./media/preview.gif" style="display:block;margin-left:auto;margin-right:auto;" width="35%"/>

## What the users say:
* "Your program is like magic! Thank you so much!" - saszai2
* "Well thank you for this software! It seems to try and guess in a more "guess-y" way than jisho and even Google which is usually pretty good at guessing, and it just saved me today!" - princess_daphie
* "... I tried the program for the same kanji [some kanji], not only did all of them work but it was able to guess what I was going for before I finished too." - swolenkamel

## Getting started

### Running the exe
This is the recommended way of running the application. <br/>
You only have to head over to the [releases section](https://github.com/CaptainDario/DaKanjiRecognizer/releases) and download the latest release.
Unzip it and run the DaKanjiRecognizer executable inside the folder.<br/>

That's it!

### Running from source

**Note: Windows (10) and Linux (Ubuntu 20.4) is currently being supported.**
**If you want to use this app on MacOS try to run the code from source (untested).**

Running the application from source is a little bit harder because you have to install all the necessary packages yourself.<br/>
You can install all packages from the 'requirements.txt' (it is recommended to do this in a separate environment):

```
python -m pip install -r requirements.txt
```

Afterwards you have to install tensorflow_lite matching your os. <br/>
Windows:
```
python -m pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp38-cp38-win_amd64.whl
```

Linux:
```
python -m pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp38-cp38-linux_x86_64.whl
```

MacOS:
```
python -m pip install https://github.com/google-coral/pycoral/releases/download/release-frogfish/tflite_runtime-2.5.0-cp38-cp38-macosx_10_15_x86_64.whl
```

Now you should be able to run the application with:
```
python .\src\main.py
```

## Usage
Draw a character and the app tries to classify it.
The predictions can be copied by clicking on the buttons.<br/> 

On the settings page a dictionary can be selected.
When long pressing a button the prediction will be opened in this dictionary.

## Development Notes

Python 3.8 with Qt (PySide2) were used for development.
First you need to install all packages from the 'requirements.txt':

```
python -m pip install -r requirements.txt
```

## PyInstaller
For freezing the app with PyInstaller you have to run the 'build'-script in the main folder:
```
.venv_rel\Scripts\python.exe build.py
```

## Next steps and ideas
The next features which will be implemented can be found [here](https://github.com/CaptainDario/DaKanjiRecognizer-Desktop/projects).

## Common issues
* on Ubuntu 20.04 LTS exists a bug in PySide2 and the following command needs to be run to install dependencies:
```bash
sudo apt-get install -y libxcb-xinerama0
```

## Credits
  
Icons were taken from the [material icon set](https://material.io/resources/icons/?style=baseline).
