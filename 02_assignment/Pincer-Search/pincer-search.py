""" Pincer Search: An algorithm for Maximal Frequent Itemset (MFI) mining

References:
	1. Data Mining
		- Arjun K Pujari
	2. Pincer Search: A New Algorithm for Discovering the Maximum Frequent Set
		- Dao-I-Lin, Zvi M. Kedem
"""

from itertools import combinations

def generateMFCS(MFCS, infrequent_itemsets):
	""" Generate the updated MFCS by modifing itemsets that have infrequent itemsets as its subset

	Parameters
	----------
	MFCS : list of lists
		The list of Maximal Frequent Candidate Sets

	infrequent_itemsets : list of lists
		The list of infrequent itemsets

	Returns
	-------
	lists of lists
		Updated MFCS
	"""

	MFCS = MFCS.copy()

	for infrequent_itemset in infrequent_itemsets:

		for MFCS_itemset in MFCS.copy():
			
			# If infrequent itemset is a subset of MFCS itemset
			if all(_item in MFCS_itemset for _item in infrequent_itemset):
				MFCS.remove(MFCS_itemset)
				
				for item in infrequent_itemset:
					updated_MFCS_itemset = MFCS_itemset.copy()
					updated_MFCS_itemset.remove(item)

					if not any(all(_item in _MFCS_itemset for _item in updated_MFCS_itemset) for _MFCS_itemset in MFCS):
						MFCS.append(updated_MFCS_itemset)

	return MFCS


def pruneCandidatesUsingMFS(candidate_itemsets, MFS):
	""" Prune the candidate itemsets that are subsets of MFS itemsets

	Parameters
	----------
	candidate_itemsets : lists of lists
		The list of candidate itemsets

	MFS : lists of lists
		The list of Maximal Frequent Itemsets

	Returns
	-------
	lists of lists
		The list of candidate itemsets with are not subsets of any itemset in MFS
	"""

	candidate_itemsets = candidate_itemsets.copy()

	for itemset in candidate_itemsets.copy():
		if any(all(_item in _MFS_itemset for _item in itemset) for _MFS_itemset in MFS):
			candidate_itemsets.remove(itemset)

	return candidate_itemsets


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


def pruneCandidatesUsingMFCS(candidate_itemsets, MFCS):
	""" Prune the candidate itemsets that are not subsets of any itemsets in current MFCS 

	Parameters
	----------
	candidate_itemsets : lists of lists
		The list of candidate itemsets

	MFCS : lists of lists
		The list of Maximal Frequent Candidate Itemsets

	Returns
	-------
	lists of lists
		The list of candidate itemsets that are subsets of some itemsets in current MFCS 
	"""

	candidate_itemsets = candidate_itemsets.copy()

	for itemset in candidate_itemsets.copy():
		if not any(all(_item in _MFCS_itemset for _item in itemset) for _MFCS_itemset in MFCS):
			candidate_itemsets.remove(itemset)

	return candidate_itemsets


def pincerSearch(transactions, min_support):
	""" Extract the Maximal Frequent Itemsets (MFI) from the transactions 
	
	Parameters
	----------
	transactions : a list of sets
		The list of transactions

	min_support : int
		The minimum support for an itemset to be considered frequent

	Returns
	-------
	list of lists
		The list of MFS which contains all maximal frequent itemsets
	"""

	# Extract the list of items in the transactions
	items = set()
	for transaction in transactions:
		items.update(transaction)
	items = sorted(list(items))
	
	level_k = 1 # The current level number

	level_frequent_itemsets = [] # Level 0: Frequent itemsets
	candidate_frequent_itemsets = [[item] for item in items] # Level 1: Candidate itemsets
	level_infrequent_itemsets = [] # Level 0: Infrequent itemsets

	MFCS = [items.copy()] # Maximal Frequent Candidate Sets
	MFS = [] # Maximal Frequent Sets

	print("MFCS = {}".format(MFCS))
	print("MFS = {}\n".format(MFS))

	while candidate_frequent_itemsets:
		
		print("LEVEL {}: ".format(level_k))
		print("C{} = {}".format(level_k, candidate_frequent_itemsets))

		candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)
		MFCS_itemsets_cnts = [0]*len(MFCS)

		# Step 1: Read the database and count supports for Ck and MFCS
		for transaction in transactions:
			
			for i, itemset in enumerate(candidate_frequent_itemsets):
				if all(_item in transaction for _item in itemset):
					candidate_freq_itemsets_cnts[i] += 1

			for i, itemset in enumerate(MFCS):
				if all(_item in transaction for _item in itemset):
					MFCS_itemsets_cnts[i] += 1

		for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts):
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		for itemset, support in zip(MFCS, MFCS_itemsets_cnts):
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		# Step 2: MFS := MFS U {frequent itemsets in MFCS}
		MFS.extend([itemset for itemset, support in zip(MFCS, MFCS_itemsets_cnts) if ((support >= min_support) and (itemset not in MFS))])
		print("MFS = {}".format(MFS))

		# Step 3: Sk := {infrequent itemsets in Ck}
		level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support]
		level_infrequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support < min_support]

		print("L{} = {}".format(level_k, level_frequent_itemsets))
		print("S{} = {}".format(level_k, level_infrequent_itemsets))

		# Step 4: call MFCS-gen algorithm if Sk != NULL
		MFCS = generateMFCS(MFCS, level_infrequent_itemsets)
		print("MFCS = {}\n".format(MFCS))

		# Step 5: call MFS-pruning procedure
		level_frequent_itemsets = pruneCandidatesUsingMFS(level_frequent_itemsets, MFS)

		# Step 6: Generate candidates Ck+1 from Ck (using generate and prune)
		candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)

		# Step 7: If any frequents itemsets in Ck is removed in MFS-pruning procedure
		# Call the recovery procedure to recover candidates to Ck+1

		# Step 8: call MFCS-prune procedure to prune candidates in Ck+1
		candidate_frequent_itemsets = pruneCandidatesUsingMFCS(candidate_frequent_itemsets, MFCS)

		# Step 9: k := k+1
		level_k += 1

	return MFS

if __name__ == '__main__':

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

	""" Example 4.5: Data Mining - Arjun K Pujari """
	'''
	transactions = [
		{1, 5, 6, 8},
		{2, 4, 8},
		{4, 5, 7},
		{3},
		{5, 6, 7},
		{2, 3, 4},
		{2, 6, 7, 9},
		{5},
		{8},
		{3, 4, 5, 7},
		{3, 4, 5, 7},
		{5, 6, 8},
		{2, 3, 4, 6, 7},
		{1, 3, 4, 5, 7},
		{2, 3, 9},
	]
	'''


	MFS = pincerSearch(transactions, 3)
	print("MFS = {}".format(MFS))