import pandas as pd
import numpy as np
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier as DT
from sklearn import tree
import graphviz
# read titanic data set
df = pd.read_excel("Data/Titanic.xlsx","Sheet1",header=0)
df = df.drop(df.index[0:2]) # drop two rows with nan data
df = df.reset_index(drop=True) # re-arrange indeces stasting from 0,
# print(df.head)

# split to input and labels
x = df.drop(labels=['Survived'],axis=1)
# categorical to one-hot-encoded
X = pp.OneHotEncoder().fit_transform(x) # returns a sparse matrix  csr format
# print(typr(X))
# print(x.head)


# get labels
y = df.Survived
Y = pp.LabelEncoder().fit_transform(y)
# print(y.head)
# print(Y)

x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.2,shuffle=True, random_state= 5, stratify=Y)

dtree = DT().fit(x_train,y_train)
acc = dtree.score(x_test,y_test)
print("Acc_test= ",acc)
y_pred = dtree.predict(x_test)

print(confusion_matrix(y_test, y_pred) )
tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
print("[TN= ",tn,"|FP= ", fp, "|FN= ", fn, "|TP= ", tp,"]")
# plot_tree(dtree)
# print("Y_predicted : ",y_pred)
# print("\nY_true : ",y_test)
# Graph Tree to pdf
dot_data = tree.export_graphviz(dtree, out_file=None)
graph = graphviz.Source(dot_data)
graph.render("titanic")
