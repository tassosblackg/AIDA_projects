# author : @tassosblackg
# create Logistic Regression classifier
# for breast cancer dataset from UCI

import pandas as pd
import matplotlib as mpt
import numpy as np
from operator import itemgetter as itemg
from sklearn import preprocessing as pp
from sklearn.linear_model import LogisticRegressionCV as lr

# read data and load
df = pd.read_csv('wdbc.data',
                            names=['id','Diagnosis',
                                    'mean_radius','mean_texture','mean_perimeter','mean_area','mean_smoothness','mean_compactness','mean_concavity','mean_concave_points','mean_symmetry','mean_fractal_dim',
                                    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se','compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se','fractal_dimension_se',
                                    'radius_worst', 'texture_worst','perimeter_worst', 'area_worst', 'smoothness_worst','compactness_worst', 'concavity_worst', 'concave points_worst','symmetry_worst', 'fractal_dimension_worst'])
# df = pd.read_csv('wdbc.data')
#print(df.head())

# Drop columns, get features
x = df.drop(labels=['id','Diagnosis'], axis=1)
X = x.to_numpy()
# print(x.head())
# print(type(x))
# print(x.shape)
# print(x[:,0])
# print (X)

#---------------------| Get Labels aka classes |-----------------------------------------
y = df.Diagnosis #df.iloc[:,1]
# print(y)

# Convert letters to numbers
lb = pp.LabelBinarizer()
Y=lb.fit_transform(y)
# print(Y)
# print(type(Y))

# ------------------| Calculate Statistics on data |--------------------------------------
_x = df.drop(labels=['id'],axis=1) # get data with
#print(m_x.head())
# row index
Mindx =  _x[_x.Diagnosis == 'M'].index.tolist()
Bindx =  _x[_x.Diagnosis == 'B'].index.tolist()

X_m = X[Mindx] # features values of class ' M '
X_b = X[Bindx] # features values of class ' B '
# print(X_m.shape, X_b.shape)

# mean of features values/// per column /per class
mean_X_m, mean_X_b = np.mean(X_m,axis=0), np.mean(X_b,axis=0)

# std of feature values per column /per class
std_X_m, std_X_b = np.std(X_m,axis=0), np.std(X_b,axis=0)

# variance of features values per column /per class
var_X_m, var_X_b = np.var(X_m,axis=0), np.var(X_b,axis=0)

# median of features values per column /per class
median_X_m, median_X_b = np.median(X_m,axis=0), np.median(X_b,axis=0)
