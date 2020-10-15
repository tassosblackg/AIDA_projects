# author : @tassosblackg
# create Logistic Regression classifier
# for breast cancer dataset from UCI
# IMPORTANT plots are show at the end after Regression calculations

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

#dimensionality reduction
pca = PCA(n_components=7)
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

X_pca = pca.fit_transform(X)
print(pca.explained_variance_ratio_)
