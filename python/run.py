from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import sys
import os
from os import path

def docomp(pathToInputs, pathToOutputs):

    # Create output directory if necessary
    try:
        os.makedirs(pathToOutputs)
    except:
        print "Error making directory"
        pass

    datasets = os.listdir(pathToInputs);
    for dataset in datasets:
        trainDataPath = path.join(pathToInputs, dataset, dataset + "_train.data")
        solDataPath = path.join(pathToInputs, dataset, dataset + "_train.solution")
        testDataPath = path.join(pathToInputs, dataset, dataset + "_test.data")
        outputDataPath = path.join(pathToOutputs, dataset + "_test_000.predict")
        datamine(trainDataPath, solDataPath, testDataPath, outputDataPath)

def datamine(pathToTrain, pathToSol, pathToTest, pathToOutput):
    # PARSE DATA
    def cleanVal(x):
        if x == '1':return 1
        if x == '0':return 0
        try:
            return float(x)
        except:
            return 0

    def pickem(ar,indices):
        nar = []
        for i in indices:
            nar.append(ar[i])
        return nar

    training_data = map(lambda x: map(cleanVal, x.split(" ")), open(pathToTrain).read().split("\n"))[:-1]
    sol_data = map(cleanVal, open(pathToSol).read().split("\n"))[:-1]



    # TESTING
    # -----------------------------------------------------
    # Cross validation
    if pathToTest == None:
        kf = cross_validation.KFold(len(training_data), n_folds=10)

        predictions = []
        answers = []

        for tri, tsi in kf:
            model = RandomForestClassifier(n_estimators=100)
            model.fit(pickem(training_data,tri), pickem(sol_data,tri))
            predictions += list(model.predict(pickem(training_data,tsi)))
            answers += pickem(sol_data, tsi)

        print(metrics.classification_report(answers, predictions))
        print(metrics.confusion_matrix(answers, predictions))
    # -----------------------------------------------------



    # Apply to test data
    # -----------------------------------------------------
    # Load the test data
    test_data = map(lambda x: map(cleanVal, x.split(" ")), open(pathToTest).read().split("\n"))[:-1]
    # Create the model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(training_data, sol_data)

    solutions = model.predict(test_data)
    open(pathToOutput,'w').write("\n".join(map(str,solutions)))
    # -----------------------------------------------------

if len(sys.argv) != 3:
    print "Please provide arguments\nautoml.py <pathToInputs> <pathToOutputDir>"
    sys.exit()

docomp(sys.argv[1],sys.argv[2])
