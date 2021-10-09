# Evolving-spiking-neuron-cellular-automata-and-networks-to-emulate-in-vitro-neuronal-activity
Code accompanying paper-ID 1415 submitted to the SSCI 2021 conference.

STRUCTURE:\
There are two folders in the main directory. Resources contains the datafiles for the neural recordings as .txt files.
These are structured as one row per spike with the first column being the timestamp and the second being the electrode
id. 

The project code is found in the src-folder. The code to run the models and evolutionary algorithm is found here.
Additionally there is a separate folder for plotting results.

RUNNING SINGLE MODEL:\
A single model with desired parameters can be run with the Model.py file. Parameters are set at the top of this file.

RUNNING EVOLUTIONARY ALGORITHM:\
To run the evolutionary algorithm, the Main.py file is run and parameters are set in the default_parameters dict.

RUNNING SAVED MODEL:\
To run a saved model, the RunSavedModel.py files is run from terminal with the first argument being the GraphML file
and the second argument being simulation duration in seconds.

RUNNING BATCH FILES:\
Multiple simulations can be run by passing batch files as arguments when running Main.py. Batch files must be .csv
files. An example can be seen in batch_example.csv. Each row is a separate run.

EXTERNAL LIBRARIES:
- Pandas
- Numpy
- NetworkX
- Scipy
- Matplotlib
- Pylab
- Seaborn
- Pandas
