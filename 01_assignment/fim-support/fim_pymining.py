#!/usr/bin/python

# relim for fim from pymining
# pymining currently supports relim, sam and fp-growth
from pymining import itemmining

# FIM
transactions = (('a', 'b', 'c'), ('b'), ('a'), ('a', 'c', 'd'), ('b', 'c'), ('b', 'c'))
print(transactions)
relim_input = itemmining.get_relim_input(transactions)
report = itemmining.relim(relim_input, min_support=2)
print(report)
