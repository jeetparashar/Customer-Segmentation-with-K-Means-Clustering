# -*- coding: utf-8 -*-
"""Task-1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zS9XhnKQpq_XUzLyafFb1VsfLci5kHii
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt

data = pd.read_csv('/content/shopping_trends_updated.csv')

print(data.columns)

print(data.head())

X = data[["Age","Gender","Category","PreviousPurchases"]]

le = LabelEncoder()
X["Gender"] = le.fit_transform(X["Gender"])
ohe = OneHotEncoder(sparse = False)
X = pd.DataFrame(ohe.fit_transform(X[["Gender"]]))

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

wcss = []
for i in range(1, 11):
  kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
  kmeans.fit(X_scaled)
  wcss.append(kmeans.inertia_)

plt.plot(range(1,11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('wcss')
plt.show()

kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state=42)
clusters = kmeans.fit_predict(X_scaled)

data['Cluster'] = clusters

print(data['Cluster'].value_counts())

plt.scatter(X_scaled[:500, 0], X_scaled[:500, 1], c=clusters[:500], cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:,0], kmeans.cluster_centers_[:,1], s=300, c = 'red' , marker = 'x')
plt.title('Customer Segmentation')
plt.xlabel('Amount of money spent')
plt.ylabel('% of purchase made')
plt.show()

