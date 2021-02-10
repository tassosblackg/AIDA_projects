# Thema 1o Final Exams
# Karageorgiadis Anastasios
# aid21002


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statistics as stats
from operator import itemgetter as itemg
from sklearn import preprocessing as pp
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression as lr

#------------------------------------------------|Question 1 | ---------------------------------------------------------------------------------------------------
# read  data set
df = pd.read_excel("ENB2012_data.xlsx",header=0)

# Input Features
x = df.drop(labels=['Y1','Y2'], axis=1)
print(x.columns)
X = x.to_numpy()
print(X.shape)

y1 = df.Y1
y2 = df.Y2
print(y1)

Y1 = y1.to_numpy()
Y2 = y2.to_numpy()
print(Y1.shape)

#------------------------------ | Question 2|------------------------------------------------------------------------------------------------------------------------
# calculate statistics
median_Y1, median_Y2 = np.median(Y1,axis=0), np.median(Y2,axis=0)
var_Y1, var_Y2 = np.var(Y1,axis=0), np.var(Y2,axis=0)
std_Y1, std_Y2 = np.std(Y1,axis=0), np.std(Y2,axis=0)

print('\n \nmedian values of y1 y2 ')
print('\n median_Y1= ',median_Y1, 'median_Y2= ',median_Y2)

print('\n \nVariance_ values of y1 y2 ')
print('\n var_Y1= ',var_Y1, 'var_Y2= ',var_Y2)

print('\n \nstd values of y1 y2')
print('\n std_Y1= ',std_Y1, 'std_Y2= ',std_Y2)

y_tags = ['Y1','Y2']


# --------------------------------------- |Question 4|-------------------------------------------------------------------------------------------------------------------

# Linear Rigression for Y1
X_scal = (X-np.mean(X,axis=0))/np.std(X,axis=0) # z-score, standarization

x_train,x_test,y1_train,y1_test = train_test_split(X_scal,Y1,test_size=0.2,shuffle=True, random_state= 1) # suffle data before spliting them with a random seed 1
linReg1 = lr().fit(x_train,y1_train)

score1 = linReg1.score(x_test,y1_test)
print("Linear Regression test_score1 = ",score1)


# Linear Rigression for Y2

x_train,x_test,y2_train,y2_test = train_test_split(X_scal,Y2,test_size=0.2,shuffle=True, random_state= 1) # suffle data before spliting them with a random seed 1
linReg2 = lr().fit(x_train,y2_train)

score2 = linReg2.score(x_test,y2_test)
print("Linear Regression test_score2 = ",score2)


# -------------------------------------| Question 3|----------------------------------------------------------------------------------------

# ----- Plot graphs ----------------------------------------------
features_indx = np.arange(len(y_tags)) # positive integer xlabel
bar_width = 0.4
plt.figure(1)

plt.bar(features_indx, median_Y1, bar_width, color='red', label='Y1')
plt.bar(features_indx + bar_width, median_Y2, bar_width, color='green', label='Y2')

#plt.yscale('log')
plt.xlabel('Features')
plt.ylabel('Median_Value')
plt.title('Bar diagram of median(Y1,2) ')
plt.xticks(features_indx + bar_width /2,y_tags,rotation=90)
plt.legend(loc='best')

# ----------------------| Plot Bar Diagram for STD Values | ---------------------------------------------------------
plt.figure(2)

plt.bar(features_indx, std_Y1, bar_width, color='red', label='Y1')
plt.bar(features_indx + bar_width, std_Y2, bar_width, color='green', label='Y2')

#plt.yscale('log')
plt.xlabel('Features')
plt.ylabel('std_Value')
plt.title('Bar diagram of std(Y1,2) ')
plt.xticks(features_indx + bar_width /2,y_tags,rotation=90)
plt.legend(loc='best')


plt.show()
