import numpy as np
import itertools 
import copy


def CHARM(item,Data,min_sup):
	nodes = []
	CFI = []
	t = set()
	for i in range(len(item)):
		t = set()
		for j in range(len(Data)):
			if Data[j][i]==1:
				t = t.union({j})
		if len(t)>=min_sup:
			nodes.append([{item[i]},t])
	nodes.sort(key = lambda x: len(x[1]))					
	CHARM_EXTEND(nodes,CFI,min_sup)
	return(CFI)		

def CHARM_EXTEND(nodes,CFI,min_sup):
	for item in nodes:
		new_nodes = []
		X = item
		for item_ in nodes: 
			if len(item[1]) > len(item_[1]) :
				X = [item[0].union(item_[0]),item[1].intersection(item_[1])]			
				CHARM_PROPERTY(nodes,new_nodes,X,item,item_,min_sup)
		if new_nodes != []:
			new_nodes.sort(key = lambda x: len(x[1])) 
			CHARM_EXTEND(new_nodes,CFI,min_sup)
		if X not in CFI :
			CFI.append(X)
	return(CFI)

def CHARM_PROPERTY(nodes,new_nodes,X,item,item_,min_sup):
	if len(X[1])>= min_sup:
		if item[1]==item_[1]:
			nodes.remove(item_)
			for i in range(len(nodes)):
				if nodes[i]==item:
					nodes[i] == X
		elif item[1].issubset(item_[1]):
			for i in range(len(nodes)):
				if nodes[i]==item:
					nodes[i] == X
		elif item_[1].issubset(item[1]):
			nodes.remove(item_)
			new_nodes.append(X)
		elif item[1]!=item_[1]:
			new_nodes.append(X)							 					


Data = [[1,1,0],[1,0,0],[0,1,1],[0,0,0]]
unique_itemset =[1,2,3]	
min_sup = 1

print(CHARM(unique_itemset,Data,min_sup))	