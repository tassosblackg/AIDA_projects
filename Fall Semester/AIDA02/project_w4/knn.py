import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report
from sklearn import preprocessing as pp

from sklearn.neighbors import KNeighborsClassifier as KNN
import seaborn as sns

# KNN Param
k=7


def reshuffle_missclass(x_train,y_train,x_test,y_test,y_pred):
    # Retrain phase
    missclass1 = np.where(y_test !=y_pred)[0]
    #remove last n from x_train
    dropped_x_train = x_train[-missclass1.shape[0]:,]
    dropped_y_train = y_train[-missclass1.shape[0]:,]

    x_train = x_train[:(x_train.shape[0]-missclass1.shape[0]),]
    y_train = y_train[:y_train.shape[0]-missclass1.shape[0]]

    # print(dropped_x_train.shape)
    x_train = np.concatenate((x_train,x_test[missclass1]),axis=0)
    y_train = np.concatenate((y_train,y_test[missclass1]),axis=0)

    rest_x_test = np.delete(x_test,missclass1,axis=0)
    rest_y_test = np.delete(y_test,missclass1,axis=0)

    #
    x_test = np.concatenate((rest_x_test,dropped_x_train),axis=0)
    y_test = np.concatenate((rest_y_test,dropped_y_train),axis=0)

    return (x_train,y_train,x_test,y_test)


df = pd.read_csv("diabetes_data.csv")
# print(df.dtypes)


X = df.drop(labels=["Outcome"],axis=1)
X[['BMI','DiabetesPedigreeFunction']] = pp.StandardScaler().fit_transform(X[['BMI','DiabetesPedigreeFunction']])
X = X.to_numpy()

print(X.shape)

Y = df.Outcome # has 1, or 0 so no encode needed
Y =Y.to_numpy()

# split 2 train & test set
x_train, x_test, y_train, y_test = train_test_split(X,Y,test_size=0.2,shuffle=True, random_state= 5, stratify=Y)
print(x_train.shape,x_test.shape)

print("\n------| KNN Results for k=",k, " |-------------------\n ")

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
print("\n---------|STATS Before Re-shuffling missclassified : |--------------------------------\n")
print("\nAccuracy[k=",k, ",\"euclidean\"] = ",acc1)
print("\nAccuracy[k=",k ,",\"manhattan\"] = ",acc2)
print("\nAccuracy[k=",k,",\"chebyshev\"] = ",acc3)
print("\nAccuracy[k=",k,",\"minkowski\"] = ",acc4)

y_pred1 = knn_res1.predict(x_test)
print("confusion Matrix KNN(euclidean) =\n",confusion_matrix(y_test, y_pred1) )
y_pred2 = knn_res2.predict(x_test)
print("confusion Matrix KNN(manhattan) =\n",confusion_matrix(y_test, y_pred2) )
y_pred3 = knn_res3.predict(x_test)
print("confusion Matrix KNN(chebyshev) =\n",confusion_matrix(y_test, y_pred3) )
y_pred4 = knn_res4.predict(x_test)
print("confusion Matrix KNN(minkowski) =\n",confusion_matrix(y_test, y_pred4) )

print("\n-------------------------------------------------------------------------------------\n\n")

print("\n --------|STATS after reshuffle_missclass: |------------------------------------------\n")

x_train,y_train,x_test,y_test = reshuffle_missclass(x_train, y_train, x_test, y_test, y_pred1)
knn_res1b = knn_model_eucl.fit(x_train, y_train)

x_train,y_train,x_test,y_test = reshuffle_missclass(x_train, y_train, x_test, y_test, y_pred2)
knn_res2b = knn_model_man.fit(x_train, y_train)

x_train,y_train,x_test,y_test = reshuffle_missclass(x_train, y_train, x_test, y_test, y_pred3)
knn_res3b = knn_model_cheb.fit(x_train, y_train)

x_train,y_train,x_test,y_test = reshuffle_missclass(x_train, y_train, x_test, y_test, y_pred3)
knn_res4b = knn_model_mink.fit(x_train, y_train)

print("\nNEW Accuracy[k=",k, ",\"euclidean\"] =",knn_res1b.score(x_test,y_test),"\n")
y_pred1b = knn_res1b.predict(x_test)
print("NEW confusion Matrix KNN(eucl) =\n",confusion_matrix(y_test, y_pred1b) )


print("\nNEW Accuracy[k=",k ,",\"manhattan\"] =",knn_res2b.score(x_test,y_test),"\n")
y_pred2b = knn_res2b.predict(x_test)
print("NEW confusion Matrix KNN(manhattan) =\n",confusion_matrix(y_test, y_pred2b) )

print("\nNEW Accuracy[k=",k ,",\"chebyshev\"] =",knn_res3b.score(x_test,y_test),"\n")
y_pred3b = knn_res3b.predict(x_test)
print("NEW confusion Matrix KNN(cheb) =\n",confusion_matrix(y_test, y_pred3b) )

print("\nNEW Accuracy[k=",k ,",\"minkowski\"] =",knn_res4b.score(x_test,y_test),"\n")
y_pred4b = knn_res4b.predict(x_test)
print("NEW confusion Matrix KNN(mink) =\n",confusion_matrix(y_test, y_pred4b) )
print("\n-------------------------------------------------------------------------------------\n\n")
