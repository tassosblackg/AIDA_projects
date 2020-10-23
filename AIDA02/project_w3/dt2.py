import pandas as pd
import numpy as np
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn import tree
import graphviz

# read Cardiology data set
df = pd.read_excel("Data/Cardiology.xlsx","Sheet1",header=0)
df = df.rename(columns={"class":"Labels"}) # rename column 'class' bad naming for python
# print(df.Labels)
# print(df.dtypes)

# split to input and labels
x = df.drop(labels=['Labels'],axis=1)
# print(x.dtypes)

# Get all categorical columns names
categorical_columns = x.select_dtypes(include=['object','bool']).copy()
# print(categorical_columns.columns)

# OneHotEncoder by using pandas [some columns are categorical dtype]
X = pd.get_dummies(x,columns=categorical_columns.columns)
# print(X.head(6))

#  Get labels
y = df.Labels
Y = pp.LabelEncoder().fit_transform(y)
# print(y.head)
# print(Y)

# split 2 train & test set
x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.25,shuffle=True, random_state= 5, stratify=Y)
#
dtree = DT().fit(x_train,y_train)
acc = dtree.score(x_test,y_test)
print("Acc_test= ",acc)

# Make predictions up on the x_test
y_pred = dtree.predict(x_test)

print(confusion_matrix(y_test, y_pred) )
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("[TN= ",tn,"|FP= ", fp, "|FN= ", fn, "|TP= ", tp,"]")

# Visualize DTree
dot_data = tree.export_graphviz(dtree, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("Cardiology")
