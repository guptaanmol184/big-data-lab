#!/usr/bin/python

#  efficient_hac.py
#  Copyright (C) 2019 ag <ag@archie>
#  Distributed under terms of the MIT license.

# Efficient Hierarchical Agglomerative Clustering - using priority queues
# Uses single linkage to merge two clusters together
# Time complexity = O(n^2 * logn)

# Input Format: Takes in a file of the format specified below
# First line: the labels of n nodes, delimited by a space, note: node labels should not contain a whitespace
# The next n lines:
# Distance matrix of size n x n. The matrix has to be a similar matrix.
# Each line corresponds to the distance of a single node to all the other nodes. Space is used as a delimiter.

# Output is a stepwise dendrogram
# every row has 4 values
# ( 1, 2, 3, 4)
# 1,2 represent the items being clustered
# 4 represents the new label assigned to the cluster of 1,2
# 3 is the level of the kth cluster

import sys
import numpy as np
import heapq
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

def efficient_hac(input_file, linkage='single'):
    # load distance matrix from file
    distance_matrix = np.loadtxt(input_file, dtype=np.float, skiprows=1)
    if (distance_matrix.ndim != 2  or
       distance_matrix.shape[0] != distance_matrix.shape[1] or
       np.any(distance_matrix != distance_matrix.T) ):
        raise ValueError('Input is not a SQUARE SYMMETRIC matrix.')

    item_count = distance_matrix.shape[0]
    # define indicator variables, to indicate which nodes are clusters
    indicator_list = [1] * item_count
    # set up the priority queues for all the clusters
    p = []
    for i in range(item_count):
        temp_heap = []
        # create min heap (using similarity as key) for the i'th item
        for j in range(len(distance_matrix[i, :])):
            if i != j: # don't add distance to self
                heapq.heappush(temp_heap, (distance_matrix[i, j], j))
        p.append(temp_heap)

    dendrogram = []

    for i in range(item_count - 1):

        # find the min distance between two clusters
        min_index = 0
        min_value = np.inf
        for i in range(len(p)):
            if indicator_list[i] == 0:
                continue
            if p[i][0][0] < min_value:
                min_value = p[i][0][0]
                min_index = i

        index1 = min_index
        index2 = p[min_index][0][1]

        # we'll merge index2 into index1, so indicate that cluster index2 is not a cluster
        indicator_list[index2] = 0

        # we are going to fill in all the new updated distance values
        # for the combined cluster to index1
        # so, inditialize it as empty
        p[index1] = []

        # perform the merge
        for i in range(item_count):
            if indicator_list[i] == 1 and i != index1 and i != index2:
                # remove the distance values of removed cluster from
                # priority queues of all other clusters
                p[i].remove((distance_matrix[i, index1], index1))
                p[i].remove((distance_matrix[i, index2], index2))

                # update distance_matrix with the combined cluster to cluster index1 for all others
                distance_matrix[i, index1] = min( distance_matrix[i, index1], distance_matrix[i, index2] )
                # insert back cluster index1 to priority queues of all others
                heapq.heappush( p[i], (distance_matrix[i, index1], index1) )

                # update distance_matrix with the combined cluster index1 for cluster index1
                distance_matrix[index1, i] = distance_matrix[i, index1]
                # add the updated distance value to the priority queue for cluster index1
                heapq.heappush( p[index1], (distance_matrix[index1, i], i) )

        # add it to the dendrogram
        dendrogram.append((index1, index2, min_value, index1))

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
        dendrogram = efficient_hac(sys.argv[1])
        print('Stepwise Dendrogram:')
        print(dendrogram)

        with open(sys.argv[1]) as f:
            labels = f.readline().strip().split()

        z = convert_dendrogram_to_matlab(dendrogram)
        print('matplotlib format dendrogram')
        print(z)

        # plot figure in using matplotlib
        plt.figure()
        hierarchy.dendrogram(z, labels=labels)
        plt.show()


if __name__ == '__main__':
    main()
