#!/usr/bin/env python

#  simple_hierarchical_clustering.py
#  Copyright (C) 2019 ag <ag@archie>
#  Distributed under terms of the MIT license.

# Simple Hierarchical Agglomerative  Clustering
# Time complexity = O(n^3)

# Input Format: Takes in a distance matrix of size n x n. The matrix has to be a similar matrix.
# Each line corresponds to the distance of a single node to all the other nodes. Space is used as a delimiter.
# We assume the initial node labels to be 0..n-1, where n is the total number of items

# Output is a stepwise dendrogram
# every row has 4 values
# ( 1, 2, 3, 4)
# 1,2 represent the items being clustered
# 4 represents the new label assigned to the cluster of 1,2
# 3 is the level of the kth cluster

import sys
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

def hierarchical_clustering(input_file, linkage='single'):
    # load data from file
    distance_matrix = np.loadtxt(input_file, dtype=np.float)
    if (distance_matrix.ndim != 2  or
       distance_matrix.shape[0] != distance_matrix.shape[1] or
       np.any(distance_matrix != distance_matrix.T) ):
        raise ValueError('Input is not a SQUARE SYMMETRIC matrix.')

    # make diagonal infinity
    np.fill_diagonal(distance_matrix, np.inf)
    item_count = distance_matrix.shape[0]

    dendrogram = []

    for i in range( item_count-1 ):

        # find index of minimum value in matrix
        # note that min index will always be of the form (smaller_number, larger_number)
        # in the case of a symmetric matrix
        min_value = distance_matrix.min()
        min_index = np.unravel_index(distance_matrix.argmin(), distance_matrix.shape)
        small_index, big_index = min_index

        small_index_row = distance_matrix[small_index, :]
        big_index_row = distance_matrix[big_index, :]

        # merge small_index_row and big_index_row and update it to small_index_row as new cluster
        if linkage == 'single':
            # take the smaller values for single linkage
            mask = small_index_row < big_index_row
        elif linkage == 'complete':
            # take the larger values for single linkage
            mask = small_index_row > big_index_row

        # update row1 (small index row) of distance matrix as the cluster
        distance_matrix[small_index, :] = np.where(mask, small_index_row, big_index_row)
        # restore the overwritten value on the diagonal to infinity
        distance_matrix[small_index, small_index] = np.inf

        # update big_index_row to infinity as it's been merged with small_index_row
        distance_matrix[big_index, :] = np.inf
        distance_matrix[:, big_index] = np.inf

        # add it to the stepwise dendrogram
        dendrogram.append((small_index, big_index, min_value, small_index))

    return dendrogram

# converts a dendrogram in my format to matplotlib format, so that we can plot it
# give me that eye candy :)
def convert_dendrogram_to_matlab(dendrogram):
    items_count = len(dendrogram) + 1
    cluster_count = {}
    for i in range(items_count):
        cluster_count[i] = 1

    mapping_dict = {}
    z = np.ones((items_count-1)*4).reshape(items_count-1, 4)
    ctr = items_count-1 # initialize ctr to label of last original cluster
    for index, val in enumerate(dendrogram):

        # update cluster count of combined cluster
        cluster_count[val[3]] = cluster_count[val[0]] + cluster_count[val[1]]
        z[index, 0] = val[0]
        z[index, 1] = val[1]
        z[index, 2] = val[2]
        z[index, 3] = cluster_count[val[3]]

        # update rows using mapping dict
        if val[0] in mapping_dict:
            z[index, 0] = mapping_dict[val[0]]
        if val[1] in mapping_dict:
            z[index, 1] = mapping_dict[val[1]]

        ctr += 1 # increment count
        # update table
        mapping_dict[val[3]] = ctr

    return z

def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: {} <input_file>'.format(sys.argv[0]))
    else:
        dendrogram = hierarchical_clustering(sys.argv[1])
        print('Stepwise Dendrogram:')
        print(dendrogram)

        z = convert_dendrogram_to_matlab(dendrogram)
        print('matplotlib format dendrogram')
        print(z)

        # plot figure in using matplotlib
        plt.figure()
        hierarchy.dendrogram(z)
        plt.show()


main()
