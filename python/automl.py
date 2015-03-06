from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation
import sys

if len(sys.argv) < 3:
    print "ARGUMENTS: path/to/train_data path/to/sol_data [path/to/test_data]"
    print "If path/to/final is specified, the solution will be written to stdout"
    print "otherwise, a confusion matrix and stats will be shown from cross validation testing"
    sys.exit()

# Get args
pathToTrain =  sys.argv[1]
pathToSol = sys.argv[2]
pathToTestData = None
if len(sys.argv) >= 4:
    pathToTestData = sys.argv[3]

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
if pathToTestData == None:
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
if pathToTestData != None:
    # Load the test data
    test_data = map(lambda x: map(cleanVal, x.split(" ")), open(pathToTestData).read().split("\n"))[:-1]
    # Create the model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(training_data, sol_data)

    solutions = model.predict(test_data)
    print "\n".join(map(str,solutions))


# -----------------------------------------------------
