""" Base IO code for loading datasets """

from os.path import dirname
import pandas as pd

def load_market_basket():
	""" Load and return a market basket dataset (Frequent Itemset Mining)
	
	======================	====
	Number of transactions	7501
	Number of items			 120
	======================	====
	
	Dataset from Tutorial: 
			Association Rule Mining via Apriori Algorithm in Python. Link: https://stackabuse.com/association-rule-mining-via-apriori-algorithm-in-python/
		
	Dataset link: https://drive.google.com/file/d/1y5DYn0dGoSbC22xowBq2d4po6h1JxcTQ/view?usp=sharing

	Returns
	-------
	list of sets
		The list of transactions in the market basket database
	"""

	module_path = dirname(__file__)
	dataset_filename = 'market_basket.csv'
	dataset_file_url = '{}/data/{}'.format(module_path, dataset_filename)

	dataset = pd.read_csv(dataset_file_url, header=None)

	# Preprocessing the dataset
	transactions = []
	for index, data in dataset.iterrows():
		transaction = pd.Series.tolist(data[~pd.isnull(data)])
		transactions.append(set(transaction))

	return transactions