# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 12:31:55 2017

@author: kaust
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier,RandomForestRegressor
from sklearn.calibration import CalibratedClassifierCV
#import xgboost as xgb
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LogisticRegression
from sklearn import svm
import datetime
import pickle
from sklearn.naive_bayes import GaussianNB

AfterDate = datetime.date(2012,1,1)

NIFTY = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTY.csv")
NIFTY['Date'] = pd.to_datetime(NIFTY['Date'])
NIFTY = NIFTY[(NIFTY.Date > AfterDate) & (NIFTY.Date < datetime.date(2017,7,25)) ]
NIFTY = NIFTY.as_matrix(["Change %"])
NIFTY = np.flipud(NIFTY)

NIFTYAUTO = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYAUTO.csv")
NIFTYAUTO['Date'] = pd.to_datetime(NIFTYAUTO['Date'])
NIFTYAUTO = NIFTYAUTO[NIFTYAUTO.Date > AfterDate ]
NIFTYAUTO = NIFTYAUTO.as_matrix(["Change %"])
NIFTYAUTO = np.flipud(NIFTYAUTO)

NIFTYBANK = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYBANK.csv")
NIFTYBANK['Date'] = pd.to_datetime(NIFTYBANK['Date'])
NIFTYBANK = NIFTYBANK[NIFTYBANK.Date > AfterDate ]
NIFTYBANK = NIFTYBANK.as_matrix(["Change %"])
NIFTYBANK = np.flipud(NIFTYBANK)

NIFTYFIN = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYFIN.csv")
NIFTYFIN['Date'] = pd.to_datetime(NIFTYFIN['Date'])
NIFTYFIN = NIFTYFIN[NIFTYFIN.Date > AfterDate ]
NIFTYFIN = NIFTYFIN.as_matrix(["Change %"])
NIFTYFIN = np.flipud(NIFTYFIN)

NIFTYFMCG = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYFMCG.csv")
NIFTYFMCG['Date'] = pd.to_datetime(NIFTYFMCG['Date'])
NIFTYFMCG = NIFTYFMCG[NIFTYFMCG.Date > AfterDate ]
NIFTYFMCG = NIFTYFMCG.as_matrix(["Change %"])
NIFTYFMCG = np.flipud(NIFTYFMCG)

NIFTYIT = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYIT.csv")
NIFTYIT['Date'] = pd.to_datetime(NIFTYIT['Date'])
NIFTYIT = NIFTYIT[NIFTYIT.Date > AfterDate ]
NIFTYIT = NIFTYIT.as_matrix(["Change %"])
NIFTYIT = np.flipud(NIFTYIT)

NIFTYMEDIA = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYMEDIA.csv")
NIFTYMEDIA['Date'] = pd.to_datetime(NIFTYMEDIA['Date'])
NIFTYMEDIA = NIFTYMEDIA[NIFTYMEDIA.Date > AfterDate ]
NIFTYMEDIA = NIFTYMEDIA.as_matrix(["Change %"])
NIFTYMEDIA = np.flipud(NIFTYMEDIA)

NIFTYMETAL = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYMETAL.csv")
NIFTYMETAL['Date'] = pd.to_datetime(NIFTYMETAL['Date'])
NIFTYMETAL = NIFTYMETAL[NIFTYMETAL.Date > AfterDate ]
NIFTYMETAL = NIFTYMETAL.as_matrix(["Change %"])
NIFTYMETAL = np.flipud(NIFTYMETAL)

NIFTYPHARMA = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYPHARMA.csv")
NIFTYPHARMA['Date'] = pd.to_datetime(NIFTYPHARMA['Date'])
NIFTYPHARMA = NIFTYPHARMA[NIFTYPHARMA.Date > AfterDate ]
NIFTYPHARMA = NIFTYPHARMA.as_matrix(["Change %"])
NIFTYPHARMA = np.flipud(NIFTYPHARMA)

NIFTYPSU = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYPSU.csv")
NIFTYPSU['Date'] = pd.to_datetime(NIFTYPSU['Date'])
NIFTYPSU = NIFTYPSU[NIFTYPSU.Date > AfterDate ]
NIFTYPSU = NIFTYPSU.as_matrix(["Change %"])
NIFTYPSU = np.flipud(NIFTYPSU)

NIFTYREALITY = pd.read_csv("F:\\FinanceRepo\\Deep-Learning-Time-Series-Prediction-using-LSTM-Recurrent-Neural-Networks-master\\NIFTYREALITY.csv")
NIFTYREALITY['Date'] = pd.to_datetime(NIFTYREALITY['Date'])
NIFTYREALITY = NIFTYREALITY[NIFTYREALITY.Date > AfterDate ]
NIFTYREALITY = NIFTYREALITY.as_matrix(["Change %"])
NIFTYREALITY = np.flipud(NIFTYREALITY)


Matrix = np.hstack((NIFTY,NIFTYAUTO,NIFTYBANK,NIFTYFIN,NIFTYFMCG,NIFTYIT,NIFTYMEDIA,NIFTYMETAL,NIFTYPHARMA,NIFTYPSU,NIFTYREALITY))
#data = data.drop(['DATE'],axis=1)
#data.head()
#
#NumpyData = data.as_matrix()
look_back = 4

def convertSeriesToMatrix(vectorSeries, look_back_window):
    matrix=[]
    for i in range(len(vectorSeries)-look_back_window+1):
        A= vectorSeries[i:i+look_back_window]
        A = A.reshape(1,(look_back_window*A.shape[1]))
        matrix.append(A)
    return matrix

Matrix = convertSeriesToMatrix(Matrix,look_back)
Matrix = np.asarray(Matrix)
Matrix = Matrix.reshape(Matrix.shape[0],Matrix.shape[2])

Pandas_Matrix = pd.DataFrame(Matrix)
#for i in range(0,(7*look_back-7),7):
#    Pandas_Matrix = Pandas_Matrix.drop([i,i+1,i+2,i+3,i+4,i+6],axis=1)
#
#Pandas_Matrix = Pandas_Matrix.drop([(7*look_back-7)],axis = 1)
#def f(row):
#    if row[33] > 0:
#        val = 1
#    else:
#        val = 0
#    return val
#
#Pandas_Matrix['Main'] = Pandas_Matrix.apply(f, axis=1)

Pandas_Matrix['MovingAvarage_1'] = pd.rolling_mean(Pandas_Matrix[11], window = 100, min_periods = 100)
Pandas_Matrix['MovingAvarage_2'] = pd.rolling_mean(Pandas_Matrix[11], window = 50, min_periods = 50)
Pandas_Matrix['MovingAvarage_3'] = pd.rolling_mean(Pandas_Matrix[11], window = 10, min_periods = 10)
Pandas_Matrix['MovingAvarage_4'] = pd.rolling_mean(Pandas_Matrix[11], window = 5, min_periods = 5)
Pandas_Matrix['MovingAvarage_5'] = pd.rolling_mean(Pandas_Matrix[11], window = 15, min_periods = 15)
Pandas_Matrix = Pandas_Matrix[100:]

#y = Pandas_Matrix['Main'].values
y = Pandas_Matrix[33].values
Pandas_Matrix = Pandas_Matrix.drop([33,34,35,36,37,38,39,40,41,42,43],axis=1)
X = Pandas_Matrix.values
#Xtrain, Xtest = X[:int(len(X) * 0.90)], X[int(len(X) * 0.90):] 
#ytrain, ytest = y[:int(len(y) * 0.90)], y[int(len(y) * 0.90):] 

Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, test_size=0.01, random_state=35)
print(Xtrain.shape)
print(Xtest.shape)

gadaboost = RandomForestRegressor()
gadaboost.fit(Xtrain, ytrain)

#with open('my_dumped_classifier.pkl', 'wb') as fid:
#    pickle.dump(gadaboost, fid)    
    
y_val_l = gadaboost.predict(Xtest)
for i in range(len(y_val_l)):
    PrintLn = str(y_val_l[i]) + "," + str(ytest[i])
    print(PrintLn)
print("Validation accuracy: ", sum(pd.DataFrame(y_val_l).idxmax(axis=1).values
                                   == ytest)/len(ytest))

target = open('C:\\Users\\kaust\\Downloads\\WinPython-64bit-3.5.2.3Qt5\\myScripts\\out.txt', 'w')
y_pre = pd.DataFrame(y_val_l).idxmax(axis=1).values

Total_Trades = 0
Total_Matched_Trades = 0
Total_False_Positives = 0
Total_False_Negatives = 0

for i in range(Xtest.shape[0]):
    line = str(ytest[i])+','+str(y_pre[i])
    target.write(line)
    target.write('\n')
    Total_Trades = Total_Trades + 1
    if(ytest[i] == y_pre[i] ):
        Total_Matched_Trades = Total_Matched_Trades + 1
    if(ytest[i] == 0 and y_pre[i] == 1):
        Total_False_Positives = Total_False_Positives + 1
    if(ytest[i] == 1 and y_pre[i] == 0):
        Total_False_Negatives = Total_False_Negatives + 1
target.close()

print("Total Trades = "+str(Total_Trades))
print("Total Matched Trades = "+str(Total_Matched_Trades))
print("Total False Positive Trades = "+str(Total_False_Positives))
print("Total False Negative Trades = "+str(Total_False_Negatives))

import numpy as np
indices = np.argsort(gadaboost.feature_importances_)[::-1]

# Print the feature ranking
print('Feature ranking:')

for f in range(Pandas_Matrix.shape[1]):
    print('%d. feature %d %s (%f)' % (f+1 , indices[f], Pandas_Matrix.columns[indices[f]],
                                      gadaboost.feature_importances_[indices[f]]))