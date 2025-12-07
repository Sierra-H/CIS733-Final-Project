from pandas import DataFrame, read_csv
import pandas as pd
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor as lof
import numpy as np
import sys

#There must be 6 arguments
#
#[1] = Legit Majority File
#[2] = Phishing Majority File
#[3] = Legit Majority SVM Output File
#[4] = Phishing Majority SVM Output File
#[5] = Legit Majority LOF Output File
#[6] = Phishing Majority LOF Output File
targetNumArgs = 7
errorOutNumArgs = "Incorrect Number of Args.\nSyntax\npython outlier.py legitMajorityFile phishingMajorityFile legitMajoritySVMOutputFile phishingMajoritySVMOutputFile legitMajorityLOFOutputFile phishingMajorityLOFOutputFile"
legitSVMOutLabels = "gamma,legit nonoutliers detected,legit nonoutliers mislabeled,phishing outliers detected,phishing outliers missed,nonoutlier detection ratio,outlier detection ratio\n"
phishingSVMOutLabels = "gamma,phishing nonoutliers detected,phishing nonoutliers mislabeled,legit outliers detected,legit outliers missed,nonoutlier detection ratio,outlier detection ratio\n"
legitLOFOutLabels = "neighbors,legit nonoutliers detected,legit nonoutliers mislabeled,phishing outliers detected,phishing outliers missed,nonoutlier detection ratio,outlier detection ratio\n"
phishingLOFOutLabels = "neighbors,phishing nonoutliers detected,phishing nonoutliers mislabeled,legit outliers detected,legit outliers missed,nonoutlier detection ratio,outlier detection ratio\n"
gammas = np.arange(0,1,0.01).tolist()
neighborValues = np.arange(1,100,1).tolist()
minoritySize = 50

if(len(sys.argv) != targetNumArgs):
    print(errorOutNumArgs)
else:
    #Read Input Files
    legitFile = pd.read_csv(sys.argv[1])
    phishingFile = pd.read_csv(sys.argv[2])

    #Setup Output Files
    legitSVMOut = open(sys.argv[3],"w")
    phishingSVMOut = open(sys.argv[4],"w")
    legitLOFOut = open(sys.argv[5],"w")
    phishingLOFOut = open(sys.argv[6],"w")

    #Output Queues
    legitSVMQueue = []
    phishingSVMQueue = []
    legitLOFQueue = []
    phishingLOFQueue = []

    #Remove Path and Class from each.
    legitFile = legitFile.drop(['Path'],axis=1)
    legitFile = legitFile.drop(['Class'],axis=1)
    phishingFile = phishingFile.drop(['Path'],axis=1)
    phishingFile = phishingFile.drop(['Class'],axis=1)

    #Train Each Input
    train_legit = legitFile.values.tolist()
    train_phishing = phishingFile.values.tolist()

    #For Each Gamma
    for gamma in gammas:

        #OneClassSVM Esitmators
        ocsvm_legit = svm.OneClassSVM(nu=0.1,kernel="rbf",gamma=gamma)
        ocsvm_phishing = svm.OneClassSVM(nu=0.1,kernel="rbf",gamma=gamma)

        #Fit The Estimators
        ocsvm_legit.fit(train_legit)
        ocsvm_phishing.fit(train_phishing)

        #Predict
        pred_ocsvm_legit = ocsvm_legit.predict(train_legit)
        pred_ocsvm_phishing = ocsvm_phishing.predict(train_phishing)

        #Calc Values In Pred Legit
        index = 0
        outliers_detected = 0
        outliers_missed = 0
        nonoutliers_detected = 0
        nonoutliers_missed = 0
        for v in pred_ocsvm_legit:
            if(index < minoritySize):
                if(v == -1): #is an outlier
                    outliers_detected = outliers_detected + 1
                else:
                    outliers_missed = outliers_missed + 1
            else:
                if(v == -1):
                    nonoutliers_missed = nonoutliers_missed + 1
                else:
                    nonoutliers_detected = nonoutliers_detected + 1
            index = index + 1
        legitSVMQueue.append(
            str(gamma)+","+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed))+"\n")
        print(
            "SVM(legit,"+str(gamma)+"): "+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed)))

        #Calc Values In Pred Phishing
        index = 0
        outliers_detected = 0
        outliers_missed = 0
        nonoutliers_detected = 0
        nonoutliers_missed = 0
        for v in pred_ocsvm_phishing:
            if(index < minoritySize):
                if(v == -1): #is an outlier
                    outliers_detected = outliers_detected + 1
                else:
                    outliers_missed = outliers_missed + 1
            else:
                if(v == -1):
                    nonoutliers_missed = nonoutliers_missed + 1
                else:
                    nonoutliers_detected = nonoutliers_detected + 1
            index = index + 1
        phishingSVMQueue.append(
            str(gamma)+","+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed))+"\n")
        print(
            "SVM(phishing,"+str(gamma)+"): "+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed)))

    #For Each Neighbor Value
    for neighbors in neighborValues:

        #LOF Esitmators
        lof_legit = lof(n_neighbors=neighbors)
        lof_phishing = lof(n_neighbors=neighbors)

        #Fit The Estimators
        #lof_legit.fit(train_legit)
        #lof_phishing.fit(train_phishing)

        #Predict
        pred_lof_legit = lof_legit.fit_predict(train_legit)
        pred_lof_phishing = lof_phishing.fit_predict(train_phishing)

        #Minority Elements
        minor_legit = pred_lof_legit[slice(minoritySize)]
        minor_phishing = pred_lof_phishing[slice(minoritySize)]

        #Calc Values In Pred Legit
        index = 0
        outliers_detected = 0
        outliers_missed = 0
        nonoutliers_detected = 0
        nonoutliers_missed = 0
        for v in pred_lof_legit:
            if(index < minoritySize):
                if(v == -1): #is an outlier
                    outliers_detected = outliers_detected + 1
                else:
                    outliers_missed = outliers_missed + 1
            else:
                if(v == -1):
                    nonoutliers_missed = nonoutliers_missed + 1
                else:
                    nonoutliers_detected = nonoutliers_detected + 1
            index = index + 1
        legitLOFQueue.append(
            str(neighbors)+","+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed))+"\n")
        print(
            "LOF(legit,"+str(neighbors)+"): "+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed)))

        #Calc Values In Pred Phishing
        index = 0
        outliers_detected = 0
        outliers_missed = 0
        nonoutliers_detected = 0
        nonoutliers_missed = 0
        for v in pred_lof_phishing:
            if(index < minoritySize):
                if(v == -1): #is an outlier
                    outliers_detected = outliers_detected + 1
                else:
                    outliers_missed = outliers_missed + 1
            else:
                if(v == -1):
                    nonoutliers_missed = nonoutliers_missed + 1
                else:
                    nonoutliers_detected = nonoutliers_detected + 1
            index = index + 1
        phishingLOFQueue.append(
            str(neighbors)+","+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed))+"\n")
        print(
            "LOF(phishing,"+str(neighbors)+"): "+
            str(nonoutliers_detected)+","+
            str(nonoutliers_missed)+","+
            str(outliers_detected)+","+
            str(outliers_missed)+","+
            str(nonoutliers_detected/(nonoutliers_detected+nonoutliers_missed))+","+
            str(outliers_detected/(outliers_detected+outliers_missed)))

    #Print to Files

    #Print to Legit SVM
    legitSVMOut.write(legitSVMOutLabels)
    for e in legitSVMQueue:
        legitSVMOut.write(e)
    legitSVMOut.close()

    #Print to Phishing SVM
    phishingSVMOut.write(phishingSVMOutLabels)
    for e in phishingSVMQueue:
        phishingSVMOut.write(e)
    phishingSVMOut.close()

    #Print to Legit LOF
    legitLOFOut.write(legitLOFOutLabels)
    for e in legitLOFQueue:
        legitLOFOut.write(e)
    legitLOFOut.close()

    #Print to Phishing LOF
    phishingLOFOut.write(phishingLOFOutLabels)
    for e in phishingLOFQueue:
        phishingLOFOut.write(e)
    phishingLOFOut.close()
