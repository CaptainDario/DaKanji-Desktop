# kanji-recognizer
A simple Qt and Tensorflow app which classifies kanji characters which the user can hand draw.


# Development Notes
Python 3.8 and vs code with the jupyter extension were used for development.

For development and training the network are other packages necessary than just for executing the application.
Therefore this project has two different "requirements.txt".

| name | usage |
|---|---|
| requirements_rel.txt | All packages which are necessary to run the application from source. |
| requirements_dev.txt | The packages which are necessary to develop and deploy the application.</br> Includes also the packages necessary to train the network and run the provided Jupyter notebook(s). |

How the network was setup and developed can be seen in the "jupyter"-folder.


# Credits
The data on which the neural network was trained on was kindly provided by [ETL Character Database](http://etlcdb.db.aist.go.jp/obtaining-etl-character-database) <br/>
Papers:<br/>
[Recognizing Handwritten Japanese Characters Using Deep Convolutional Neural Networks](http://cs231n.stanford.edu/reports/2016/pdfs/262_Report.pdf) <br/>
[A neural framework for online recognition of handwritten Kanji characters](https://www.researchgate.net/publication/327893142_A_neural_framework_for_online_recognition_of_handwritten_Kanji_characters) <br/>
[Online Handwritten Kanji Recognition Based on Inter-stroke Grammar](https://www.researchgate.net/publication/4288187_Online_Handwritten_Kanji_Recognition_Based_on_Inter-stroke_Grammar) <br/>