""" Efficient variant of Apriori using Partitioning Technique 

Reference
---------
Data Mining Concepts and Techniques - Jaiwei Han and Micheline Kamber
	Section: 5.2.3 Improving the Efficieny of Apriori (Pg No. 240)

Acknowledgements
----------------
The author would like to appreciate the efforts of the `MPI for Python <https://mpi4py.readthedocs.io/>`_ development 
team for making MPI more effortless and accessible to use.

How to execute the program
--------------------------
- Install the MPI system packages and `mpi4py <https://mpi4py.readthedocs.io>`_ python package
- Execute the following command in the terminal:
	$ mpiexec -n <number of processes> python <python program filename>
"""

from itertools import combinations

def generateCandidateItemsets(level_k, level_frequent_itemsets):
	""" Generate and prune the candidate itemsets for next level using the frequent itemsets of the current level 
	
	Parameters
	----------
	level_k : int
		The current level number

	level_frequent_itemsets : list of lists
		The list of frequent itemsets of current level

	Returns
	-------
	list of lists
		The candidate itemsets of the next level
	"""

	n_frequent_itemsets = len(level_frequent_itemsets)

	candidate_frequent_itemsets = []

	for i in range(n_frequent_itemsets):
		j = i+1
		while (j<n_frequent_itemsets) and (level_frequent_itemsets[i][:level_k-1] == level_frequent_itemsets[j][:level_k-1]):
			
			candidate_itemset = level_frequent_itemsets[i][:level_k-1] + [level_frequent_itemsets[i][level_k-1]] + [level_frequent_itemsets[j][level_k-1]]
			candidate_itemset_pass = False

			if level_k == 1:
				candidate_itemset_pass = True
				
			elif (level_k == 2) and (candidate_itemset[-2:] in level_frequent_itemsets):
				candidate_itemset_pass = True

			elif all((list(_)+candidate_itemset[-2:]) in level_frequent_itemsets for _ in combinations(candidate_itemset[:-2], level_k-2)):
				candidate_itemset_pass = True
				
			if candidate_itemset_pass:
				candidate_frequent_itemsets.append(candidate_itemset)

			j += 1

	return candidate_frequent_itemsets


def aprioriAlgorithm(transactions, min_support_count):
	""" Extract frequent itemsets from transactions using Apriori Algorithm
	
	Parameters
	----------
	transactions : a list of sets
		The list of transactions

	min_support_count : int
		The minimum support count for an itemset to be considered frequent

	Returns
	-------
	list of sets
		The list of frequent itemsets extracted from the transactions
	"""

	# Extract the list of items in the transactions
	items = set()
	for transaction in transactions:
		items.update(transaction)
	items = sorted(list(items))

	# The list of frequent itemsets in the transaction
	frequent_itemsets = []

	level_k = 1 # The current level number

	level_frequent_itemsets = [] # Level 0: Frequent itemsets
	candidate_frequent_itemsets = [[item] for item in items] # Level 1: Candidate itemsets

	while candidate_frequent_itemsets:

		# Count the support of all candidate frequent itemsets and remove transactions using transaction reduction
		candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

		for transaction in transactions:
			for i, itemset in enumerate(candidate_frequent_itemsets):
				if all(_item in transaction for _item in itemset):
					candidate_freq_itemsets_cnts[i] += 1

		# Generate the frequent itemsets of level k by pruning infrequent itemsets
		level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support_count]
		frequent_itemsets.extend([set(level_frequent_itemset) for level_frequent_itemset in level_frequent_itemsets])

		# Generate candidates Ck+1 from Ck (using generate and prune)
		candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)

		level_k += 1

	return frequent_itemsets


def __customListsReduce(new_list, reduced_list):
	''' Custom Reduce Operation that reduces two lists by taking their union '''
	for item in new_list:
		if item not in reduced_list:
			reduced_list.append(item)
	return reduced_list

from math import floor
from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
comm_size = comm.Get_size()

if rank == 0:
	
	from os.path import abspath, dirname, join
	dataset_filename = join(dirname(dirname(dirname(abspath(__file__)))), 'datasets', 'data', 'market_basket.csv')

	dataset_file = open(dataset_filename)
	
	# Count the number of transactions in the dataset file
	n_transactions = 0
	for line in dataset_file:
		n_transactions += 1

	print("Number of Transactions = {}".format(n_transactions))

	# Read and broadcast the min support to all processes
	min_support = float(input("Please enter the minimum support (as fraction) : "))
	comm.bcast(min_support, root=0)

	n_trans_root = n_transactions%(comm_size-1)
	n_trans_per_worker = n_transactions//(comm_size-1)

	# Read chunks of data from file and send to each worker
	dataset_file.seek(0, 0)
	for i_process in range(1, comm_size):
		transactions = [set(next(dataset_file).strip().split(',')) for x in range(n_trans_per_worker)]
		# Using blocking send to avoid memory overflow in case of congested networks
		comm.send(transactions, dest=i_process, tag=0)
		del transactions

	# Read the chunk of data for root node
	transactions = [set(next(dataset_file).strip().split(',')) for x in range(n_trans_root)]
	local_min_support_count = floor(min_support*n_trans_root)

	# Extract the frequent itemset for transactions in the root
	local_frequent_itemsets = aprioriAlgorithm(transactions, local_min_support_count)

	# Reduce the local frequent itemsets from all nodes at root into candidate_frequent_itemsets
	candidate_frequent_itemsets = comm.reduce(local_frequent_itemsets, op=__customListsReduce, root=0)

	global_min_support_count = floor(min_support*n_transactions)
	candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

	# Count the support of all itemsets in the candidate frequent itemset
	dataset_file.seek(0, 0)
	for transaction_str in dataset_file:
		transaction = set(transaction_str.strip().split(','))
		for i, itemset in enumerate(candidate_frequent_itemsets):
				if itemset <= transaction:
					candidate_freq_itemsets_cnts[i] += 1

	global_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= global_min_support_count]

	print("\nFREQUENT ITEMSETS")
	for frequent_itemset in global_frequent_itemsets:
		print(frequent_itemset)

else:
	min_support = comm.bcast(None, root=0)
	transactions = comm.recv(source=0, tag=0)

	worker_n_trans = len(transactions)
	local_min_support_count = floor(min_support*worker_n_trans)

	# Extract the frequent itemset for transactions in the worker node
	local_frequent_itemsets = aprioriAlgorithm(transactions, local_min_support_count)

	# Reduce the frequent itemsets from all nodes at root
	comm.reduce(local_frequent_itemsets, op=__customListsReduce, root=0)