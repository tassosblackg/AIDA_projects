# author : @tassosblackg
# create Logistic Regression classifier
# for breast cancer dataset from UCI


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from operator import itemgetter as itemg
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression as lr

# read data and load
df = pd.read_csv('../a1-logit/wdbc.data',
                            names=['id','Diagnosis',
                                    'mean_radius','mean_texture','mean_perimeter','mean_area','mean_smoothness','mean_compactness','mean_concavity','mean_concave_points','mean_symmetry','mean_fractal_dim',
                                    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se','compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se','fractal_dimension_se',
                                    'radius_worst', 'texture_worst','perimeter_worst', 'area_worst', 'smoothness_worst','compactness_worst', 'concavity_worst', 'concave points_worst','symmetry_worst', 'fractal_dimension_worst'])
# df = pd.read_csv('wdbc.data')
#print(df.head())

# Drop columns, get features
x = df.drop(labels=['id','Diagnosis'], axis=1)
features_tags = x.columns # features' names by column
X = x.to_numpy()
# standarization of data before moving further
X = pp.StandardScaler().fit_transform(X)

#--------- Dimensionality reduction

'''
------------non-standarized X before PCA------------------------
for n=2, variance ratio was 0.982 0.016 => ~0.99
for n=3, variance ratio was +0.001 xxx
-------------standarized X before PCA----------------------------
for n=2, variance ratio was 0.442,0.1897 => ~0.63
for n=3, variance ratio was 0.442,0.1897 0.093 => ~0.72
for n=4, variance ratio was 0.442,0.1897 0.093 0.066 => ~0.79
for n=5, variance ratio was  "     "      "   "    0.054 => ~0.84
tested up to n=7 with variance ratio ~ 0.9
-----------------------------------------------------------------
'''
pca = PCA(n_components=6)
X_pca = pca.fit_transform(X)
# print(pca.explained_variance_ratio_)

# --- Get Labels Data
y = df.Diagnosis #df.iloc[:,1]
# print(y)

# Convert letters to numbers
lb = pp.LabelBinarizer()
Y=lb.fit_transform(y)

# train test split with keeping the balance  but using X without applying PCA, as was the first week's model
x_train1, x_test1, y_train1, y_test1 = train_test_split(X,Y,test_size=0.15,shuffle=True, random_state= 1, stratify=Y)
logReg1 = lr(max_iter=1000).fit(x_train1,y_train1.ravel())
score1 = logReg1.score(x_test1,y_test1)

# split dataset to train and test, shuffle with seed 1 and stratify according Y to balance the split
x_train2, x_test2, y_train2, y_test2 = train_test_split(X_pca,Y,test_size=0.15,shuffle=True, random_state= 1, stratify=Y)
logReg2 = lr(max_iter=1000).fit(x_train2,y_train2.ravel())
score2 = logReg2.score(x_test2,y_test2)


print('\nScore logit without PCA = ',score1,'\nScore logit with PCA = ',score2 )
'''
For n=2 , the test_score_pca = ~0.941, & test_score_without_pca ~= 0.976 [not good -0.03]
For n=3,4 , the test_score_pca = ~0.953, & test_score_without_pca ~= 0.976 [not good -0.02]

For n=5 , the test_score_pca = ~0.965, & test_score_without_pca ~= 0.976 [not good but close]

-> For n=6 , the test_score_pca = ~0.976, & test_score_without_pca ~= 0.976 [same, that's good] <-
For n=7,8 still the same as n=6
'''
