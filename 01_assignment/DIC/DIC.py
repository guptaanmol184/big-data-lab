"""
This is the basic implementation of DIC(Dynamic itemset algotithm)
Referred from : http://www2.cs.uregina.ca/~dbd/cs831/notes/itemsets/DIC.html
"""

import numpy as np
import itertools 
import copy
			

def subset_generator(S,n):
	"""
	takes in a set S and size of the subsets to generate.
	generates all subsets of size len(s)-1
	"""
	#print(S)
	a = itertools.combinations(S,n)
	result = []
	for i in a:
		result.append(set(i))
	return(result)	

def superset_generator(S,unique_itemset):
	"""
	Takes in a set S and generates it's 
	immediate superset from the unique itemset
	"""
	#print(S)
	result = []
	a = set()
	for i in unique_itemset:
		if i.intersection(S)==set():
			a = i.union(S)
			result.append(a)
			a = set()

	return(result)		

def subset_checker(S,FIS):
	"""
	takes in a set S and check if all if its len(s)-1 subsets 
	are there in FIS
	"""
	subset = subset_generator(S,len(S)-1)
	flag = 1
	temp = []

	for i in FIS:
		temp.append(i[0])

	FIS = temp
	for i in subset:
		if i not in FIS:
			flag=0
			break

	if flag:
		return(True)
	else:
		return(False)

def transaction_to_itemset(T):
	"""
	Converts each record of a database in to a itemset format
	"""
	result = set()
	for i in range(len(T)):
		if T[i]!=0:
			result.add(i+1)

	return(result)		



database = [[1,1,0],[1,0,0],[0,1,1],[0,0,0]]
unique_itemset =[{1},{2},{3}]
# database = [[1,1,0,1,1],[0,1,1,0,1],[1,1,0,1,1],[1,1,1,0,1],[1,1,1,1,1],[0,1,1,1,0]]
# unique_itemset =[{1},{2},{3},{4},{5}]
min_supp = 1
M = 2
size = len(database)

#4 lists are simplemented which store the state if itemsers in the database
DC = []
DS = []	
SC = []
SS = []

# 	update the DC set with all the unique items along with their counters in the database
# 	initially all their counters with 0
# 	itemset is in the form [a,b,c] -> a is itemset , b is its count , c is no_iter
DC = [[i,0,0] for i in unique_itemset]
print("Initial DC:",DC,"\n")

counter = 0
T = []
while DC!=[] or DS!=[]:
#for p in range(6):
	for i in range(counter,counter+M):				#updating counter var in each itemset
		index = i%size
		T = transaction_to_itemset(database[index])
		print("Transaction :",T)

		for item in DC:
			item[2]+=1
			if item[0].issubset(T):
				item[1]+=1
		for item in DS:
			item[2]+=1
			if item[0].issubset(T):
				item[1]+=1		

	for item in copy.copy(DC):								#transfer itemsets from DC to DS basef on min_supp
		if(item[1]>=min_supp):
			DS.append(item)
			DC.remove(item)

	for item in copy.copy(DS):								#transfer itemsets from DS to SS if it's count=size
		if(item[2]==size):
			SS.append(item)
			DS.remove(item)			
	for item in copy.copy(DC):								#transfer itemsets from DC to SC if it's count=size
		if(item[2]==size):
			SC.append(item)
			DC.remove(item)
	#print(DC)
	
	FIS = copy.copy(DS)
	FIS.extend(SS)								#check if all subsets are there in FIS for immediate supersets
	for item in FIS:
		S = superset_generator(item[0],unique_itemset)
		for i in S:
			if subset_checker(i,FIS):
				flag=1
				for x in DC:
					if x[0]==i:
						flag=0
				for x in DS:
					if x[0]==i:
						flag=0
				for x in SC:
					if x[0]==i:
						flag=0
				for x in SS:
					if x[0]==i:
						flag=0						
				if flag:
					DC.append([i,0,0])		

	counter+=M
	print("DS: ",DS)
	print("DC: ",DC)
	print("SS: ",SS)
	print("SC: ",SC,"\n")

