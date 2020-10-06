# author : @tassosblackg #

import pandas as pd
import matplotlib as mpt
import numpy as np
from sklearn import preprocessing as pp
from sklearn.linear_model import LogisticRegressionCV

# read data and load
df = pd.read_csv('wdbc.data',
                            names=['id','Diagnosis',
                                    'mean_radius','mean_texture','mean_perimeter','mean_area','mean_smoothness','mean_compactness','mean_concavity','mean_concave_points','mean_symmetry','mean_fractal_dim',
                                    'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se','compactness_se', 'concavity_se', 'concave points_se', 'symmetry_se','fractal_dimension_se',
                                    'radius_worst', 'texture_worst','perimeter_worst', 'area_worst', 'smoothness_worst','compactness_worst', 'concavity_worst', 'concave points_worst','symmetry_worst', 'fractal_dimension_worst'])
# df = pd.read_csv('wdbc.data')
#print(df.head())

#Get Labels aka classes
y = df.Diagnosis
# print(y)
# convert letters to numbers
lb = pp.LabelBinarizer()
Y=lb.fit_transform(y)
# print(Y)


# split to input_d, out_label


#drop id_col
