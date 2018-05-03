
# coding: utf-8
"""
Created on Tue Apr 10 17:20:06 2018

@author: Snigdha Siddula
Impact of SMOTE and Sample on ML-Classifier's Performace - Occupancy Dataset
"""
# In[204]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy
import time
from datetime import datetime
from sklearn import preprocessing
from imblearn.over_sampling import SMOTE
from collections import Counter


# In[205]:


# change working directory
os.chdir('C:/Users/Snigs/Desktop/Internship/occupancy_data')


# In[206]:


# read datafile and check dimensions
d_ns = pd.read_csv('data_NS.csv')
d_ns.shape


# In[207]:


d_ns.head(5)


# In[208]:


d_ns.dtypes


# In[209]:


d_ns['date'] = pd.DatetimeIndex(d_ns.date)
d_ns.dtypes


# In[210]:


d_ns['Occupancy'] = d_ns.Occupancy.astype('category')
d_ns.dtypes


# In[211]:


# checking level-counts of target
d_ns['Occupancy'].value_counts()


# In[212]:


y = d_ns['Occupancy']
y.head(5)


# In[213]:


x = d_ns[['Temperature','Humidity','Light','CO2','HumidityRatio','year','month','day_of_week','hour_of_day']]
x.head(5)


# In[214]:


# Train Test Split
from sklearn.cross_validation import train_test_split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.3,stratify=y,random_state=123)


# ### SMOTE

# In[215]:


# Over-sampling the minority class
X_resampled, y_resampled = SMOTE().fit_sample(X_train, y_train)
print(sorted(Counter(y_resampled).items()))


# In[216]:


type(X_resampled)


# In[217]:


X_resampled = pd.DataFrame(X_resampled)
X_resampled.head()


# In[218]:


type(y_resampled)


# In[219]:


y_resampled = pd.DataFrame(y_resampled)
y_resampled.head()


# In[220]:


# Merge resampled X and y 
train = pd.concat([X_resampled,y_resampled],axis=1)
train.columns = ['Temperature', 'Humidity', 'Light','CO2','HumidityRatio','year','month','day_of_week','hour_of_day','Occupancy']


# In[221]:


train.head()


# In[222]:


train_0 = train[train['Occupancy']==0]
train_0.shape


# In[223]:


train_1 = train[train['Occupancy']==1]
train_1.shape


# ### SMOTE Sample Ratios

# In[224]:


train_0_samp = train_0.sample(frac=0.30,random_state=123)
train_0_samp.head()


# In[225]:


train_1_samp = train_1.sample(frac=0.70,random_state=123)
train_1_samp.head()


# ### splitting train

# In[226]:


X_train = pd.concat([train_0_samp.iloc[:,0:9],train_1_samp.iloc[:,0:9]],axis=0)
X_train.head()


# In[227]:


y_train = pd.concat([train_0_samp['Occupancy'],train_1_samp['Occupancy']],axis=0)
y_train.head()


# ### CLASSIFICATION MODELLING

# In[228]:


from sklearn import linear_model
from sklearn.naive_bayes import GaussianNB
from sklearn import tree
from sklearn.metrics import confusion_matrix
from sklearn.metrics import recall_score, precision_score, accuracy_score


# ### 1. Logistic Regression

# In[229]:


start_time = time.time()
logreg_train = linear_model.LogisticRegression()
lr_model = logreg_train.fit(X_train, y_train)
end_time = time.time()
print(end_time - start_time)


# In[230]:


pred_lr_train = lr_model.predict(X_train)
pred_lr_test = lr_model.predict(X_test)
accuracy_score(y_test,pred_lr_test)


# ### 2. Naive Bayes

# In[231]:


start_time = time.time()
nb_train = GaussianNB()
nb_model = nb_train.fit(X_train, y_train)
end_time = time.time()
print(end_time -  start_time)


# In[232]:


pred_nb_train = nb_model.predict(X_train)
pred_nb_test = nb_model.predict(X_test)
accuracy_score(y_test,pred_nb_test)


# ### 3. Decision Tree

# In[233]:


start_time = time.time()
dt = tree.DecisionTreeClassifier()
dt_model = dt.fit(X_train, y_train)
end_time = time.time()
print(end_time - start_time)


# In[234]:


pred_dt_test = dt_model.predict(X_test)
pred_dt_train = dt_model.predict(X_train)
accuracy_score(y_test,pred_dt_test)


# ### 4. SVM

# In[235]:


from sklearn import svm
start_time = time.time()
svm = svm.SVC()
svm_model = svm.fit(X_train, y_train)
end_time = time.time()
print(end_time - start_time)


# In[236]:


pred_svm_test = svm_model.predict(X_test)
pred_svm_train = svm_model.predict(X_train)
accuracy_score(y_test,pred_svm_test)

