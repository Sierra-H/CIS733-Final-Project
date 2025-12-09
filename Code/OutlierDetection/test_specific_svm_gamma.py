from pandas import DataFrame, read_csv
import pandas as pd
from sklearn import svm
from sklearn.neighbors import LocalOutlierFactor as lof
import numpy as np
import sys

#Read in legit majority file
lmf=pd.read_csv(sys.argv[1])
#Open output file
o = open(sys.argv[2],"w")
#Open other output file (non outliers)
nf = open(sys.argv[3],"w")

#Write 1st row
#o.write("gamma,Legit Outliers Detected,Legit Outliers Not Detected,phishing Outliers Detected,phishing Outliers Not Detected,Legit Mislabeled As Outlier,Legit Labeled Correctly,phishing Mislabeled As Outlier,phishing Labeled Correctly\n")

#Different gamma values
# Source for numpy list: https://stackoverflow.com/questions/18265935/how-do-i-create-a-list-with-numbers-between-two-values
gammas = np.arange(0,1,0.01).tolist()

# CREATE SUBSETS (1000 L, 50 P), (1000 P, 50 L)
#remove path and class for each
lmf = lmf.drop(['Path'],axis=1)
lmf = lmf.drop(['Class'],axis=1)

# make train vals
train_lmf = lmf.values.tolist()

#for each gamma value
#for g in gammas:
#initialize estimators
estimator_lmf = svm.OneClassSVM(nu=0.1,kernel="rbf",gamma=0.04)

#fit the estimators
estimator_lmf.fit(train_lmf)

#predict each
pred_lmf = estimator_lmf.predict(train_lmf)

oa = []

count = 0
for x in pred_lmf:
    if(x==-1):
        oa.append(count)
    count = count + 1
# Source Line Reading: https://www.geeksforgeeks.org/python/how-to-read-from-a-file-in-python/
original = open(sys.argv[1])
line = original.readline()
o.write(line)
nf.write(line)
line = original.readline()
count = 0
while line:
    if((count in oa)):
        print(line)
        o.write(line)
    else:
        nf.write(line)
    line = original.readline()
    count = count + 1
o.close()
nf.close()
