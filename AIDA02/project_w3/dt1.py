import pandas as pd
import numpy as np
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier as DT

# read titanic data set
df = pd.read_excel("Data/Titanic.xlsx","Sheet1",header=0)
df = df.drop(df.index[0:2]) # drop two rows with nan data
df = df.reset_index(drop=True) # re-arrange indeces stasting from 0,
print(df.head)

# split to input and labels
