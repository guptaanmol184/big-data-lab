""" MAFIA: A Maximal Frequent Itemset Algorithm (Without any optimization)

Reference: 
	MAFIA: A Maximal Frequent Itemset Algorithm for Transactional Databases
		- Doug Burdick, Manuel Calimlin, Johannes Gehrke (Department of CS, Cornell University)
"""

import numpy as np
from functools import lru_cache

class TransVerticalBitmaps:
	""" Stores transactions as vertical bitmap of individual items and helps count itemset supports efficiently 

	Parameters
	----------
	transactions : list of sets
		The list of transactions

	Attributes
	----------
	transactions : list of sets
		The list of transactions

	n_transactions : int
		The number of transactions

	items : list
		The list of all items in sorted order

	items_vertical_bitmaps : dict
		The dictionary of vertical bitmap representation of transactions indexed by item
	"""

	def __init__(self, transactions):

		self.transactions = transactions
		self.n_transactions = len(self.transactions)

		# Extract the list of items in the transactions
		items = set()
		for transaction in self.transactions:
			items.update(transaction)
		self.items = sorted(items)

		self.items_vertical_bitmaps = {item:np.zeros(shape=(self.n_transactions,), dtype=np.bool) for item in self.items}

		for i_transaction, transaction in enumerate(self.transactions):
			for item in transaction:
				self.items_vertical_bitmaps[item][i_transaction] = True


	@lru_cache(maxsize=32)
	def compVerticalBitmap(self, itemset):
		""" Compute the vertical bitmap of the given itemset
		
		Parameters
		----------
		itemset : tuple
			The tuple of items (or itemset) for which support is to be counted

		Returns
		-------
		np.array(bool)
			Vertical bitmap of transactions in the which itemset is present
		"""
		
		if len(itemset) == 1:
			item = itemset[0]
			return self.items_vertical_bitmaps[item]

		else:
			last_item = itemset[-1]
			return self.compVerticalBitmap(itemset[:-1])&self.items_vertical_bitmaps[last_item]


	def countSupport(self, itemset):
		""" Count the support of the itemset in the transactions 

		Parameters
		----------
		itemset : tuple
			The tuple of items for which support is to be counted

		Returns
		-------
		int
			The support count of the itemset in the transactions
		"""
		
		itemset_vertical_bitmap = self.compVerticalBitmap(itemset)
		itemset_support_count = np.count_nonzero(itemset_vertical_bitmap)

		return itemset_support_count



class MafiaNode:
	""" A node in the MAFIA candidate itemset tree 
	
	Parameters
	----------
	head : set
		The set of all items in head of the node

	tail : tuple
		The tuple of all items in tail of the node

	Attributes
	----------
	head : set
		The set of all items in head of the node

	tail : tuple
		The tuple of all items in tail of the node

	Notes
	-----
		The :attr:`head` is of type tuple as opposed to set or list since it is passed to :meth:`compVerticalBitmap`
		of :class:`transactions` that caches results and therefore requires the inputs to **hashable**.
	"""

	def __init__(self, head, tail):
		self.head = head
		self.tail = tail.copy()


def _mafiaAlgorithm(current_node, MFIs, transactions, min_support_count):

	is_leaf = True

	for i, item in enumerate(current_node.tail):
		new_node_head = current_node.head + (item,)
		if transactions.countSupport(new_node_head) >= min_support_count:
			is_leaf = False
			new_node_tail = current_node.tail[i+1:]
			new_node = MafiaNode(new_node_head, new_node_tail)

			_mafiaAlgorithm(new_node, MFIs, transactions, min_support_count)

	# if current node is a leaf and no superset of current node head in MFIs
	if is_leaf and not any(all(item in mfi for item in current_node.head) for mfi in MFIs):
		MFIs.append(set(current_node.head))


def mafiaAlgorithm(transactions, min_support_count):
	""" Extract the MFIs (Maximal Frequent Itemsets) from transactions with min support count using MAFIA Algorithm

	Parameters
	----------
	transactions : list of sets
		The list of transactions

	min_support_count : int
		The minimum support count threshold

	Returns
	-------
	list of sets
		The list of all maximal frequent itemsets
	"""

	transactions_vertical_bitmaps = TransVerticalBitmaps(transactions)
	MFIs = []

	# Create the root node of MAFIA candidate itemset tree
	mafia_cand_itemset_root = MafiaNode(tuple(), transactions_vertical_bitmaps.items)

	# Perform the MAFIA algorithm
	_mafiaAlgorithm(mafia_cand_itemset_root, MFIs, transactions_vertical_bitmaps, min_support_count)
	return MFIs


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

	min_support_count = 3

	MFIs = mafiaAlgorithm(transactions, min_support_count)

	# Print the list of all maximal frequent itemsets (MFIs)
	print("Maximal Frequent Itemsets (MFIs)")
	for mfi in MFIs:
		print(mfi)