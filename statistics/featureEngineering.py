# Feature Extraction with RFE
from pandas import read_csv
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.decomposition import PCA
from sklearn.feature_selection import RFE, SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import ExtraTreesClassifier
from sklearn import preprocessing
from sklearn import utils

def RFE(gui, guybrush, X, Y):
    # load data
    #filename = 'pima-indians-diabetes.data.csv'
    #names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
    #dataframe = read_csv(filename, names=names)
    #array = dataframe.values
    #X = array[:,0:8]
    #Y = array[:,8]

    # feature extraction
    model = LogisticRegression()
    rfe = RFE(model, 3)
    fit = rfe.fit(X, Y)
    print("Num Features: %d") % fit.n_features_
    print("Selected Features: %s") % fit.support_
    print("Feature Ranking: %s") % fit.ranking_

def kBest(gui, guybrush, X, Y):
    print("kmean")    
    test = SelectKBest(score_func=chi2, k=int(gui.lineEdit_kWindow.currentText()))
    fit = test.fit(X, Y)
    # summarize scores
    set_printoptions(precision=3)
    print(fit.scores_)
    features = fit.transform(X)
    # summarize selected features
    print(features[0:5,:])

def PCA_feature(gui, guybrush, X, Y):
    # load data
    #filename = 'pima-indians-diabetes.data.csv'
    #names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
    #dataframe = read_csv(filename, names=names)
    #array = dataframe.values
    #X = array[:,0:8]
    #Y = array[:,8]
    # feature extraction
    pca = PCA(n_components=int(gui.lineEdit_kWindow.currentText()))
    fit = pca.fit(X)
    # summarize components
    print("Explained Variance: %s") % fit.explained_variance_ratio_
    print(fit.components_)


def featureImportance(gui, guybrush):
    # load data
    #filename = 'pima-indians-diabetes.data.csv'
    #names = ['preg', 'plas', 'pres', 'skin', 'test', 'mass', 'pedi', 'age', 'class']
    #dataframe = read_csv(filename, names=names)
    #array = dataframe.values
    #X = array[:,0:8]
    #Y = array[:,8]

    labels = guybrush.mst_labels

    out_features = [x.row() for x in gui.listOutput.selectedIndexes()]
    in_features = [x.row() for x in gui.listInput.selectedIndexes()]
    labels_in_features = [labels[i] for i in in_features]
    labels_out_features = [labels[i] for i in out_features]

    

    #labels = list()
    #for i in range(len(in_features)):
    #    if(i in guybrush.mst_labels):
    #        labels.append(guybrush.mst_labels[i])

    filename = guybrush.file

    dataframe = read_csv(filename, names=labels_in_features, skiprows=1)
    X = dataframe.values

    dataframe2 = read_csv(filename, names=labels_out_features, skiprows=1)
    Y = dataframe2.values

    #for feat in out_features:
    #    labels.pop(feat)

    # feature extraction
    clf = ExtraTreesClassifier()
    clf.fit(X, Y)
    model = SelectFromModel(clf, prefit=True)
    X_new = model.transform(X)
    print(list(zip(labels_in_features,clf.feature_importances_)))
    
    