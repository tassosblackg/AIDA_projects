import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
from sklearn import preprocessing as pp

from sklearn.neighbors import KNeighborsClassifier as KNN
import seaborn as sns

df = pd.read_csv("diabetes_data.csv")
# print(df.dtypes)


X = df.drop(labels=["Outcome"],axis=1)
mms = pp.MinMaxScaler()

X[['BMI','DiabetesPedigreeFunction']] = pp.StandardScaler().fit_transform(X[['BMI','DiabetesPedigreeFunction']])
# columns_to_scale = X.columns[X.columns!="Age" ]
# Try Min-Max scaling on float attributes
# X[['BMI','DiabetesPedigreeFunction']] = mms.fit_transform(X[['BMI','DiabetesPedigreeFunction']])
# X = X.to_numpy()

Y = df.Outcome # has 1, or 0 so no encode needed

# split 2 train & test set
x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.2,shuffle=True, random_state= 5, stratify=Y)


print("KNN Results for k=5\n ")
k=5
knn_model_eucl = KNN(n_neighbors=k, metric='euclidean')
knn_model_man = KNN(n_neighbors=k, metric='manhattan')
knn_model_cheb = KNN(n_neighbors=k, metric='chebyshev')
knn_model_mink = KNN(n_neighbors=k, metric='minkowski')

knn_res1 = knn_model_eucl.fit(x_train, y_train)
knn_res2 = knn_model_man.fit(x_train, y_train)
knn_res3 = knn_model_cheb.fit(x_train, y_train)
knn_res4 = knn_model_mink.fit(x_train, y_train)

acc1 = knn_res1.score(x_test,y_test)
acc2 = knn_res2.score(x_test,y_test)
acc3 = knn_res2.score(x_test,y_test)
acc4 = knn_res4.score(x_test,y_test)

print("\nAccuracy[k=",k, ",\"euclidean\"] = ",acc1)
print("\nAccuracy[k=",k ,",\"manhattan\"] = ",acc2)
print("\nAccuracy[k=",k,",\"chebyshev\"] = ",acc3)
print("\nAccuracy[k=",k,",\"minkowski\"] = ",acc4)

# Make predictions per model confusion matrix
y_pred1 = knn_res1.predict(x_test)
print("confusion Matrix KNN(euclidean) =\n",confusion_matrix(y_test, y_pred1) )
y_pred2 = knn_res2.predict(x_test)
print("confusion Matrix KNN(manhattan) =\n",confusion_matrix(y_test, y_pred2) )
y_pred3 = knn_res3.predict(x_test)
print("confusion Matrix KNN(chebyshev) =\n",confusion_matrix(y_test, y_pred3) )
y_pred4 = knn_res4.predict(x_test)
print("confusion Matrix KNN(minkowski) =\n",confusion_matrix(y_test, y_pred4) )

# classification report
print("classification Report  KNN(manhattan) =\n",classification_report(y_test, y_pred2) )
print("classification Report KNN(chebyshev) =\n",classification_report(y_test, y_pred3) )

print("KNN Results for k=7\n ")
k=7
knn_model_eucl = KNN(n_neighbors=k, metric='euclidean')
knn_model_man = KNN(n_neighbors=k, metric='manhattan')
knn_model_cheb = KNN(n_neighbors=k, metric='chebyshev')
knn_model_mink = KNN(n_neighbors=k, metric='minkowski')

knn_res1 = knn_model_eucl.fit(x_train, y_train)
knn_res2 = knn_model_man.fit(x_train, y_train)
knn_res3 = knn_model_cheb.fit(x_train, y_train)
knn_res4 = knn_model_mink.fit(x_train, y_train)

acc1 = knn_res1.score(x_test,y_test)
acc2 = knn_res2.score(x_test,y_test)
acc3 = knn_res2.score(x_test,y_test)
acc4 = knn_res4.score(x_test,y_test)

print("\nAccuracy[k=",k, ",\"euclidean\"] = ",acc1)
print("\nAccuracy[k=",k ,",\"manhattan\"] = ",acc2)
print("\nAccuracy[k=",k,",\"chebyshev\"] = ",acc3)
print("\nAccuracy[k=",k,",\"minkowski\"] = ",acc4)

# Make predictions per model confusion matrix
y_pred1 = knn_res1.predict(x_test)
print("confusion Matrix KNN(euclidean) =\n",confusion_matrix(y_test, y_pred1) )
y_pred2 = knn_res2.predict(x_test)
print("confusion Matrix KNN(manhattan) =\n",confusion_matrix(y_test, y_pred2) )
y_pred3 = knn_res3.predict(x_test)
print("confusion Matrix KNN(chebyshev) =\n",confusion_matrix(y_test, y_pred3) )
y_pred4 = knn_res4.predict(x_test)
print("confusion Matrix KNN(minkowski) =\n",confusion_matrix(y_test, y_pred4) )

# Only the best combination of k=7,metrics=manh,cheb
print("classification Report KNN(manhattan) =\n",classification_report(y_test, y_pred2) )
print("classification Report KNN(chebyshev) =\n",classification_report(y_test, y_pred3) )
