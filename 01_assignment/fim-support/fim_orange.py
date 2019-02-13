#!/usr/bin/python

#Orange3-Associate package provides frequent_itemsets() function based on FP-growth algorithm.
import Orange
from orangecontrib.associate.fpgrowth import *
#data = Orange.data.Table("market-basket.basket")
dataset =[
            [1,    3, 4   ],
            [   2, 3,    5],
            [1, 2, 3,    5],
            [   2,       5]
        ]

itemsets = frequent_itemsets(dataset, 2)
#rules = Orange.associate.AssociationRulesSparseInducer(data, support=0.3)
#print("%4s %4s  %s" % ("Supp", "Conf", "Rule") )
#for r in rules[:5]:
#   print("%4.1f %4.1f  %s" % (r.support, r.confidence, r))
print(list(itemsets))
