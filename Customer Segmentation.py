# -*- coding: utf-8 -*-
"""
Customer Segmentation with K-Means Clustering

Segments customers using Age, Gender, Category, and PreviousPurchases.

Fix: earlier versions of this script built a feature matrix from
Age, Gender, Category and PreviousPurchases, but then overwrote it
with only the one-hot-encoded Gender column right before scaling, so
the model was effectively clustering on gender alone. This version
keeps all four features in the matrix that actually gets scaled and
clustered.
"""

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

data = pd.read_csv('shopping_trends_updated.csv')

print(data.columns)
print(data.head())

# Select the features we want to cluster on
features = data[["Age", "Gender", "Category", "PreviousPurchases"]].copy()

# One-hot encode the categorical columns and keep the numeric ones alongside them
categorical_cols = ["Gender", "Category"]
numeric_cols = ["Age", "PreviousPurchases"]

encoded = pd.get_dummies(features[categorical_cols], drop_first=True)
X = pd.concat([features[numeric_cols], encoded], axis=1)

# Standardise all features so no single column dominates the distance metric
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Elbow method to choose the number of clusters
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)

plt.plot(range(1, 11), wcss)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

# Fit K-Means with the chosen number of clusters
kmeans = KMeans(n_clusters=4, init='k-means++', random_state=42)
clusters = kmeans.fit_predict(X_scaled)

data['Cluster'] = clusters
print(data['Cluster'].value_counts())

# Visualise clusters (Age vs. Previous Purchases, standardised)
plt.scatter(X_scaled[:500, 0], X_scaled[:500, 1], c=clusters[:500], cmap='viridis')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s=300, c='red', marker='x')
plt.title('Customer Segmentation')
plt.xlabel('Age (standardised)')
plt.ylabel('Previous Purchases (standardised)')
plt.show()
