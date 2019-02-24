""" A-Close: Closed Frequent Itemsets Mining Algorithm """

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


def generateClosures(transactions, generators):
	""" Generate the closures of the generators 

	transactions : list of sets
		The list of transactions

	generators : lists of lists
		The list of generator itemsets whose closures need to be computed

	Returns
	-------
	list of sets
		The list of closures mapped from the generators
	"""

	# The indices of transactions where generators occur
	generators_trans_indices = [[] for _ in range(len(generators))]

	for trans_index, transaction in enumerate(transactions):
		for generator_index, generator in enumerate(generators):
			if all(_item in transaction for _item in generator):
				generators_trans_indices[generator_index].append(trans_index)

	generators_closures = []
	for generator_trans_indices in generators_trans_indices:

		if generator_trans_indices:
			closure = transactions[generator_trans_indices[0]].copy()
			
		else:
			closure = set()

		for trans_index in generator_trans_indices[1:]:
			closure.intersection_update(transactions[trans_index])
		generators_closures.append(closure)

	return generators_closures


def AClose(transactions, min_support):
	""" Extract the closed frequent itemsets from the transactions

	Parameters
	----------
	transactions : list of sets
		The list of transactions

	min_support : int
		The minimum support threshold

	Returns
	-------
	list of sets
		closed frequent itemsets mined from the transactions that have support greater than the minimum threshold
	"""

	items = set()
	for transaction in transactions:
		items.update(transaction)
	items = sorted(list(items))

	# The list of all generator from whose closure we can derive all CFIs
	generators = []

	level_k = 1

	prev_level_freq_itemsets_cnts = [] # Level 0: Frequent Itemsets and its support counts
	candidate_frequent_itemsets = [[item] for item in items] # Level 1: Candidate Itemsets

	while candidate_frequent_itemsets:

		print("LEVEL {}:".format(level_k))

		# Count the support of all candidate frequent itemsets
		candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

		for transaction in transactions:
			for i, itemset in enumerate(candidate_frequent_itemsets):
				if all(_item in transaction for _item in itemset):
					candidate_freq_itemsets_cnts[i] += 1

		print("C{}: ".format(level_k), end='')
		for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts):
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		# Generate the frequent itemsets of level k by pruning infrequent itemsets
		level_frequent_itemsets_cnts = [(itemset,support) for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support]

		print("L{}: ".format(level_k), end='')
		for itemset, support in level_frequent_itemsets_cnts:
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		# Prune the frequent itemsets of level k which have same support as some frequent subset in level k-1
		print("Itemsets Pruned from L{}: ".format(level_k), end='')
		for level_freq_itemset, level_freq_itemset_sup in level_frequent_itemsets_cnts.copy():
			for prev_level_freq_itemset, prev_level_freq_itemset_sup in prev_level_freq_itemsets_cnts:

				# If the previous level itemset is a subset of current level itemset and both have same support
				if all(_item in level_freq_itemset for _item in prev_level_freq_itemset) and prev_level_freq_itemset_sup == level_freq_itemset_sup:
					print(level_freq_itemset, end=', ')
					level_frequent_itemsets_cnts.remove((level_freq_itemset, level_freq_itemset_sup))
					break
		print()

		print("L{} After Pruning: ".format(level_k), end='')
		for itemset, support in level_frequent_itemsets_cnts:
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		# Generate candidate sets of level k+1 using frequent itemsets of level k
		level_frequent_itemsets = [itemset for itemset,support in level_frequent_itemsets_cnts]
		candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)
		generators.extend(level_frequent_itemsets)

		level_k += 1

		prev_level_freq_itemsets_cnts = level_frequent_itemsets_cnts
		print()

	# Generate the closure of the generators
	generators_closures = generateClosures(transactions, generators)

	closed_frequent_itemsets = []

	# Remove the duplicates from the list of closures
	for generator_closure in generators_closures:
		if generator_closure not in closed_frequent_itemsets:
			closed_frequent_itemsets.append(generator_closure)

	return closed_frequent_itemsets


if __name__ == '__main__':

	""" Example discussed in class """
	transactions = [
		{'A', 'C', 'D'},
		{'B', 'C', 'E'},
		{'A', 'B', 'C', 'E'},
		{'B', 'E'},
		{'A', 'B', 'C', 'E'},
	]

	closed_frequent_itemsets = AClose(transactions, 3)
	
	print("Closed Frequent Itemsets (CFIs)")
	for itemset in closed_frequent_itemsets:
		print(itemset)