""" Efficient variant of Apriori using Transaction Reduction 

References:
	Data Mining Concepts and Techniques - Jaiwei Han and Micheline Kamber
		Section: 5.2.3 Improving the Efficieny of Apriori (Pg No. 240)
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


def aprioriTransactionReduction(transactions, min_support_count, verbose=False):
	""" Extract frequent itemsets from transactions using Transaction Reduction based Apriori Algorithm
	
	Parameters
	----------
	transactions : a list of sets
		The list of transactions

	min_support_count : int
		The minimum support count for an itemset to be considered frequent

	verbose : bool
		Indicates whether verbose trace of the algorithm should be printed

	Returns
	-------
	list of sets
		The list of frequent itemsets extracted from the transactions
	"""

	if verbose:
		print("Database Transactions")
		for transaction in transactions:
			print(transaction)
	print("Number of Transactions = {}".format(len(transactions)))

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
		
		if verbose:

			print("\n==================================================================")

			# Print the frequent itemsets of level k-1
			print("Level {}: Frequent Itemsets".format(level_k-1))
			for level_frequent_itemset in level_frequent_itemsets:
				print(level_frequent_itemset)
			print()

			print("Level {}: Pruned Transactions".format(level_k))

		# Count the support of all candidate frequent itemsets and remove transactions using transaction reduction
		candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

		current_trans_index = 0

		for transaction in transactions:

			# Count the number of candidate itemsets that are part of the transaction
			trans_n_candidate_itemsets = 0

			for i, itemset in enumerate(candidate_frequent_itemsets):
				if all(_item in transaction for _item in itemset):
					candidate_freq_itemsets_cnts[i] += 1
					trans_n_candidate_itemsets += 1

			# Retain only transactions that contains atleast two candidate itemsets in it
			if trans_n_candidate_itemsets > 1:
				transactions[current_trans_index] = transaction
				current_trans_index += 1

			elif verbose:
				print(transaction)
	
		if verbose:
			print("Number of transactions pruned = {}".format(len(transactions)-current_trans_index), end='\n\n')

		transactions = transactions[:current_trans_index]
		print("After Level {}: Number of Transactions = {}".format(level_k, current_trans_index))

		if verbose:
			print("==================================================================")

		# Generate the frequent itemsets of level k by pruning infrequent itemsets
		level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support_count]
		frequent_itemsets.extend([set(level_frequent_itemset) for level_frequent_itemset in level_frequent_itemsets])

		# Generate candidates Ck+1 from Ck (using generate and prune)
		candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)

		level_k += 1

	return frequent_itemsets


if __name__ == '__main__':

	""" Load the standard market basket dataset from datasets module """
	'''
	from os.path import abspath, dirname

	file_path = dirname(abspath(__file__))
	datasets_module_path = dirname(dirname(file_path))

	import sys
	sys.path.append(datasets_module_path)

	import datasets

	transactions = datasets.load_market_basket()

	min_support_count = 100
	verbose = False
	'''

	""" Example 4.4: Data Mining - Arjun K Pujari """
	transactions = [
		{1, 5, 6, 8},
		{2, 4, 8},
		{4, 5, 7},
		{2, 3},
		{5, 6, 7},
		{2, 3, 4},
		{2, 6, 7, 9},
		{5},
		{8},
		{3, 5, 7},
		{3, 5, 7},
		{5, 6, 8},
		{2, 4, 6, 7},
		{1, 3, 5, 7},
		{2, 3, 9},
	]

	min_support_count = 3
	verbose = True

	# Generate list of all frequent itemsets using Transaction Reduction based Apriori
	frequent_itemsets = aprioriTransactionReduction(transactions, min_support_count, verbose=verbose)

	print("\nFREQUENT ITEMSETS (Min Support Count = {})".format(min_support_count))
	for frequent_itemset in frequent_itemsets:
		print(frequent_itemset)