# kanji-recognizer
A simple Qt and Tensorflow app which classifies kanji characters which the user can hand draw.


# Development Notes
For development and training the network are other packages necessary than just for executing the application.
Therefore this project has two different "requirements.txt".

| name | usage |
|---|---|
| requirements_rel.txt | All packages which are necessary to run the application from source. |
| requirements_dev.txt | The packages which are necessary to develop and deploy the application.</br> Includes also the packages necessary to train the network and run the provided Jupyter notebook(s). |

How the network was setup and developed can be seen in the "jupyter"-folder.


# Credits
The data on which the neural network was trained on was kindly provided by [ETL Character Database](http://etlcdb.db.aist.go.jp/obtaining-etl-character-database)