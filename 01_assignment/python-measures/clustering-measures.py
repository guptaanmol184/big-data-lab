#!/usr/bin/python

from sklearn import datasets
#from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans
from sklearn import metrics
import numpy as np

iris = datasets.load_iris()
x, y = iris.data, iris.target

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)

k_means = KMeans(n_clusters=3)
#k_means.fit(x_train)
k_means.fit(x)
print({i: np.where(k_means.labels_ == i)[0] for i in range(k_means.n_clusters)})

#y_train_pred = k_means.predict(x_train)
#y_test_pred = k_means.predict(x_test)
y_pred = k_means.predict(x)

# for all the available meterics for evaluation of clustering performance in sklearn
# use: https://scikit-learn.org/stable/modules/clustering.html#clustering-performance-evaluation

# ADJUSTED RAND SCORE
# https://scikit-learn.org/stable/modules/clustering.html#adjusted-rand-index
print('--> adjusted rand score')
#print('adjusted rand score on training set: {}'.format(metrics.adjusted_rand_score(y_train, y_train_pred)))
#print('adjusted rand score on testing set: {}'.format(metrics.adjusted_rand_score(y_test, y_test_pred)))
print('adjusted rand score: {}'.format(metrics.adjusted_rand_score(y, y_pred)))

# HOMOGENEITY
# https://scikit-learn.org/stable/modules/clustering.html#homogeneity-completeness-and-v-measure
# homogeneity: each cluster contains only members of a single class.
print('--> homogeneity: each cluster contains only members of a single class.')
# print('homogeneity score on training set: {}'.format(metrics.homogeneity_score(y_train, y_train_pred)))
# print('homogeneity score on testing set: {}'.format(metrics.homogeneity_score(y_test, y_test_pred)))
print('homogeneity score: {}'.format(metrics.homogeneity_score(y, y_pred)))

# COMPLETENESS
# https://scikit-learn.org/stable/modules/clustering.html#homogeneity-completeness-and-v-measure
# completeness: all members of a given class are assigned to the same cluster.
print('--> completeness: all members of a given class are assigned to the same cluster.')
# print('completeness score on training set: {}'.format(metrics.completeness_score(y_train, y_train_pred)))
# print('completeness score on testing set: {}'.format(metrics.completeness_score(y_test, y_test_pred)))
print('completeness score: {}'.format(metrics.completeness_score(y, y_pred)))

# FOWLKES MALLOWS SCORES
# https://scikit-learn.org/stable/modules/clustering.html#fowlkes-mallows-scores
print('--> fowlkes mallows score: The Fowlkes-Mallows score FMI is defined as the geometric mean of the pairwise precision and recall.')
# print('fowlkes mallows score on training set: {}'.format(metrics.fowlkes_mallows_score(y_train, y_train_pred)))
# print('fowlkes mallows  score on testing set: {}'.format(metrics.fowlkes_mallows_score(y_test, y_test_pred)))
print('fowlkes mallows score: {}'.format(metrics.fowlkes_mallows_score(y, y_pred)))

# SILHOUETTE COEFFICIENT
# https://scikit-learn.org/stable/modules/clustering.html#silhouette-coefficient
# Used when true labels are not known beforehand
print('--> silhouette coefficient')
# print('silhouette coefficient on training set: {}'.format(metrics.silhouette_score(x_train, y_train_pred, metric="euclidean")))
# print('silhouette coefficient on testing set: {}'.format(metrics.silhouette_score(x_test, y_test_pred, metric="euclidean")))
print('silhouette coefficient: {}'.format(metrics.silhouette_score(x, y_pred, metric="euclidean")))


# CLUSTER RADIUS
print("RADIUS")
'''looping over clusters and calculate Euclidian distance of
each point within that cluster from its centroid and
pick the maximum which is the radius of that cluster'''

clusters_centroids=dict()
clusters_radii= dict()
#for cluster in list(set(y_train)):
for cluster in list(set(y)):

    clusters_centroids[cluster]=k_means.cluster_centers_[cluster]
    clusters_radii[cluster] = 0
    for i in x[y_pred == cluster]:
        distance = np.linalg.norm(i - clusters_centroids[cluster])
        if distance > clusters_radii[cluster]:
            clusters_radii[cluster] = distance
    print('Cluster {} radius: {}'.format(cluster, clusters_radii[cluster]))

# DIAMETER
print("DIAMETER")
'''looping over clusters and calculate Euclidian distance of
each point within that cluster from other points within the cluster and
pick the maximum for the cluster which is the diameter of that cluster'''

cluster_dia = dict()
for cluster in range(k_means.n_clusters):
    indices = list(np.where(k_means.labels_ == cluster)[0])
    values = [x[i] for i in indices]

    cluster_dia[cluster] = 0
    for i in range(len(values)-1):
        for j in range(i+1, len(values)):
            distance = np.linalg.norm(values[i] - values[j])
            if distance > cluster_dia[cluster]:
                cluster_dia[cluster] = distance

    print('Cluster {} diameter: {}'.format(cluster, cluster_dia[cluster]))
