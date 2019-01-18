#!/usr/bin/env python
# Single Linkage Hierarchical Clustering
# Input Format: Takes in a distance matrix of size n x n. The matrix has to be a similar matrix.
# Each line corresponds to the distance of a single node to all the other nodes. Space is used as a delimiter.

# Output is a stepwise dendrogram
# every row has 4 values
# ( 1, 2, 3, 4)
# 1,2 represent the items being clustered
# 4 represents the new label assigned to the cluster of 1,2
# 3 is the level of the kth cluster

# Runtime complexity = O(n^3)

import sys
import numpy as np

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
            mask = small_index_row < big_index_row
        elif linkage == 'complete':
            mask = small_index_row > big_index_row

        # update row1 (small index row) of distance matrix as the cluster
        # we use single linkage
        distance_matrix[small_index, :] = np.where(mask, small_index_row, big_index_row)
        # restore the overwritten value on the diagonal to infinity
        distance_matrix[small_index, small_index] = np.inf

        # update big_index_row to infinity as it's been merged with small_index_row
        distance_matrix[big_index, :] = np.inf
        distance_matrix[:, big_index] = np.inf

        # add it to the stepwise dendrogram
        dendrogram.append((small_index, big_index, min_value, small_index))

    return dendrogram

def main():
    if len(sys.argv) != 2:
        sys.exit('Usage: {} <input_file>'.format(sys.argv[0]))
    else:
        dendrogram = hierarchical_clustering(sys.argv[1])
        print('Stepwise Dendrogram:')
        print(dendrogram)

main()
