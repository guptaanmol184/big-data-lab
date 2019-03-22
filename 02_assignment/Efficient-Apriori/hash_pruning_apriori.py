""" Efficient variant of Apriori using Hash Pruning
"""

from itertools import combinations

class hashTable:
    def __init__(self, hash_table_size):
        self.hash_table = [0] * hash_table_size

    def add_itemset(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        self.hash_table[hash_index] += 1

    def get_itemset_count(self, itemset):
        hash_index = (itemset[0]*10+itemset[1])%7
        return self.hash_table[hash_index]

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

        # Intialize the hash table
        hash_tb = hashTable(7)

        while candidate_frequent_itemsets:

                # Count the support of all candidate frequent itemsets and remove transactions using transaction reduction
                candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)

                for transaction in transactions:
                        # add the count of itemsets of size 2 to hashtable
                        if level_k == 1:
                            for itemset in combinations(transaction, 2):
                                hash_tb.add_itemset(itemset)

                        for i, itemset in enumerate(candidate_frequent_itemsets):
                                if all(_item in transaction for _item in itemset):
                                        candidate_freq_itemsets_cnts[i] += 1

                # Generate the frequent itemsets of level k by pruning infrequent itemsets
                level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support_count]
                frequent_itemsets.extend([set(level_frequent_itemset) for level_frequent_itemset in level_frequent_itemsets])

                # Generate candidates Ck+1 from Ck (using generate and prune)
                candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)
                level_k += 1

                # prune C_2 using hash table generated during L_1
                if level_k == 2:
                    for itemset in candidate_frequent_itemsets:
                        if hash_tb.get_itemset_count(itemset) < min_support_count:
                            print('Pruned itemset', itemset)
                            candidate_frequent_itemsets.remove(itemset)

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
                {1, 2, 5},
                {2, 4},
                {2, 3},
                {1, 2, 4},
                {1, 3},
                {2, 3},
                {1, 3},
                {1, 2, 3, 5},
                {1, 2, 3},
                {1, 2},
                {1, 3, 5}
        ]

        min_support_count = 3

        # Generate list of all frequent itemsets using Transaction Reduction based Apriori
        frequent_itemsets = aprioriAlgorithm(transactions, min_support_count)

        print("\nFREQUENT ITEMSETS (Min Support Count = {})".format(min_support_count))
        for frequent_itemset in frequent_itemsets:
                print(frequent_itemset)
