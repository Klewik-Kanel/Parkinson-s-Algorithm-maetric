# -*- coding: utf-8 -*-
"""Parkinsons.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19gkQSTVIGoR9xv-PrcE7sTKkL757E2Wo
"""

#!pip install lux

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import os, sys

from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

#loading data
df=pd.read_csv('parkinsons.data')
df.head(n=10)

df.shape

df.describe()

#finding null values

df.isnull().sum()

df.dtypes

for i in df.columns:
  print("*****************************************************************",i,"*********************************************************")
  print()
  print(set(df[i].tolist()))
  print()

import pandas as pd
import matplotlib.pyplot as plot
import seaborn as sns

# Rebuild df (if needed for testing)
# df = pd.DataFrame({'status': ['Active', 'Inactive', 'Active', 'Pending', 'Inactive', 'Active']})

# Create value counts DataFrame
temp = df["status"].value_counts()
temp_df = pd.DataFrame({'status': temp.index, 'values': temp.values})
temp_df.to_csv("temp_clean.csv", index=False)
temp_df = pd.read_csv("temp_clean.csv")


print(temp_df)
print(temp_df.columns)
print(type(temp_df))

sns.barplot(x='status', y='values', data=temp_df)
plot.show()

sns.pairplot(df)

def distplots(col):
  sns.distplot(df[col])
  plot.show()

for i in list(df.columns)[1:]:
  distplots(i)

def boxplots(col):
  sns.boxplot(df[col])
  plot.show()

for i in list(df.select_dtypes(exclude=["object"]).columns)[1:]:
  boxplots(i)

import seaborn as sns
import matplotlib.pyplot as plt

# Visualizing the distribution of 'status' using violin plot
#plt.figure(figsize=(10,6))

for i in list(df.select_dtypes(exclude=["object"]).columns)[1:]:
  sns.violinplot(x='status', y=i, data=df, hue="status")
  plt.title('Distribution of Status')
  plt.xlabel('Status')
  plt.ylabel(i)
  plt.show()

#finding correlation
non_numeric_cols = df.select_dtypes(include='object').columns
df_numeric = df.drop(non_numeric_cols, axis=1)

plot.figure(figsize=(20,20))
corr = df_numeric.corr()
sns.heatmap(corr,annot=True)

#seperating dependent and independent variables
x=df.drop(["status", "name"],axis=1)
y=df["status"]

#lets detect the label balance
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter

print(Counter(y))

ros = RandomOverSampler()

x_ros, y_ros = ros.fit_resample(x,y)
print(Counter(y_ros))

#scaling the data
scaler = MinMaxScaler((-1,1))
#scaler = StandardScaler()
x=scaler.fit_transform(x_ros)
y = y_ros

from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

pca = PCA(.95)
x_PCA = pca.fit_transform(x)
#lda = LinearDiscriminantAnalysis("svd")
#x_LDA = lda.fit_transform(x,y)
print(x.shape)
print(x_PCA.shape)

x_train,x_test,y_train,y_test=train_test_split(x_PCA, y, test_size=0.3, random_state=7)

#starting with algorithms
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, precision_score, recall_score

list_met=[]
list_accuracy=[]

#apply logistic_regression
from sklearn.linear_model import LogisticRegression

classifier = LogisticRegression(C=0.4, max_iter=1000, solver='liblinear')
lr=classifier.fit(x_train, y_train)
#prediction
y_pred = classifier.predict(x_test)
#accuracy
accuracy_LR = accuracy_score(y_test, y_pred)


#apply decision tree

from sklearn.tree import DecisionTreeClassifier

classifier2 = DecisionTreeClassifier(random_state=14)
dt=classifier2.fit(x_train, y_train)
#prediction
y_pred2 = classifier2.predict(x_test)
accuracy_DT = accuracy_score(y_test, y_pred2)



#apply Random-Forest criteria=information gain

from sklearn.ensemble import RandomForestClassifier

classifier3 = RandomForestClassifier(random_state=14)
rfi = classifier3.fit(x_train, y_train)
#prediction
y_pred3 = classifier3.predict(x_test)
#accuracy
accuracy_RFI = accuracy_score(y_test, y_pred3)




#apply Random-Forest criteria=entropy

from sklearn.ensemble import RandomForestClassifier

classifier4 = RandomForestClassifier(criterion='entropy')
rfe=classifier4.fit(x_train, y_train)
#Prediction
y_pred4 = classifier4.predict(x_test)
#accuracy
accuracy_RTE = accuracy_score(y_test, y_pred4)



#similarly apply SVM
from sklearn.svm import SVC
model_svm = SVC (cache_size=100)
svm = model_svm.fit(x_train, y_train)
#Preciction
y_preds = model_svm.predict(x_test)
#Accuracy
accuracy_svc= accuracy_score (y_test, y_preds)


# Apply KNN
from sklearn.neighbors import KNeighborsClassifier
model_knn3 = KNeighborsClassifier (n_neighbors=3)
knn=model_knn3.fit(x_train,y_train)
# Predicting Test Set N=3
pred_knn3= model_knn3.predict(x_test)
#Accuracy
accuracy_KNN = accuracy_score (y_test, pred_knn3)




#Apply Gaussian Naive Bayes
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb=gnb.fit(x_train, y_train)
# Predicting Test Set
pred_gnb = gnb.predict(x_test)
#accuracy
accuracy_GNB = accuracy_score (y_test, pred_gnb)




#Apply Bernoulli Naive Bayes
from sklearn.naive_bayes import BernoulliNB
model = BernoulliNB()
bnb = model.fit(x_train, y_train)
# Predicting Test Set
pred_bnb = model.predict(x_test)
#accuracy
accuracy_BNB = accuracy_score (y_test, pred_bnb)


# Combining all the above using voting classifier
from sklearn.ensemble import VotingClassifier
evc=VotingClassifier (estimators=[('1r', lr), ('rfi', rfi), ('rfe', rfe), ('DT', dt),('svm', svm), ('knn', knn), ('gnb',gnb), ('bnb', bnb)], voting='hard',flatten_transform=True)
model_evc=evc.fit(x_train, y_train)
# Predicting Test Set
pred_evc = evc.predict(x_test)
#accuracy
accuracy_evc = accuracy_score (y_test, pred_gnb)
list1=['Logistic Regression', 'Decison Tree', 'Random Forest (information gain)', 'Random Forest (Entropy)', 'SVM', 'KNN', 'gnb', 'bnb', 'voting classifier']
list2=[accuracy_LR, accuracy_DT, accuracy_RFI, accuracy_RFI, accuracy_svc, accuracy_KNN, accuracy_GNB, accuracy_BNB, accuracy_evc]
list3=[classifier, classifier2, classifier3, classifier4, model_svm, model_knn3, gnb, model]

df_Accuracy = pd.DataFrame({ 'Method Used':list1, 'Accuracy': list2})
print(df_Accuracy)

chart=sns.barplot (x='Method Used',y='Accuracy', data=df_Accuracy)
chart.set_xticklabels (chart.get_xticklabels(), rotation=90)
print(chart)

"""1.   Confusion Matrix  
2.   ROC Curve
3.   Violin Curve
"""

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score
for i in list3:
  print("*************************************",i,"************************************")
  print(classification_report (y_test, i.predict(x_test)))
  print('Confusion Matrix:')
  print(confusion_matrix(y_test, i.predict(x_test)))
  print()

# Visualizing performance with ROC
from sklearn.metrics import roc_curve, auc, confusion_matrix, classification_report, accuracy_score
def plot_roc(model, x_test, y_test):
#calculate the fpr and tpr for all thresholds of the classification
  probabilities = model.predict_proba(np.array(x_test))
  predictions = probabilities
  fpr, tpr, threshold = roc_curve (y_test, predictions[:,1])
  roc_auc = auc(fpr, tpr)

  plot.title('Receiver Operating Characteristic')
  plot.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
  plot.legend(loc= 'lower right')
  plot.plot([0, 1], [0, 1], 'r--')
  plot.xlim([0, 1])
  plot.ylim([0, 1])
  plot.ylabel('True Positive Rate')
  plot.xlabel('False Positive Rate')
  plot.show()

for i in range(0,len (list3)):
  try:
    print()
    print("------------------ ROC FOR ",list1[i]," + PCA ------------------")
    plot_roc(list3[i], x_test, np.array(y_test))
    print()
  except:
    print("roc not valid")