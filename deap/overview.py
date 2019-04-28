""" DEAP Overview
Reference: https://deap.readthedocs.io/en/master/overview.html
"""

""" Build your own type using the creator """

from deap import base, creator

# Create a new class :class:'FitnessMin' from :class:`deap.base.Fitness` with attribute :attr:`weights` initialised to (-1.0,)
creator.create('FitnessMin', base.Fitness, weights=(-1.0,))

# Create a new class :class:`Individual` from :class:`builtins.list` with attribute :attr:`fitness` initialised to the value returned by __init__ of :class:`creator.FitnessMin`
creator.create('Individual', list, fitness=creator.FitnessMin)

""" Initializing the created types
Create functions to initialize population from individuals that are themselves initialized with random float values
"""
import random
from deap import tools

# The number of floating point numbers in 'Individual'
IND_SIZE = 10

# Create a toolbox instance
toolbox = base.Toolbox()

# Register function :func:`random.random` under the alias 'attribute' with no default arguments
toolbox.register('attribute', random.random)

# Register the function :func:`deap.tools.initRepeat` with default arguments (creator.Individual, toolbox.attribute, n=IND_SIZE)
""" deap.tools.initRepeat(container /* to put data from func*/, func /*function to be called n times to fill container*/, n /*number of times to call func*/) """
toolbox.register('individual', tools.initRepeat, creator.Individual, toolbox.attribute, n=IND_SIZE)

# Register the function :func:`deap.tools.initRepeat` with default arguments list, toolbox.Individual
toolbox.register('population', tools.initRepeat, list, toolbox.individual)

""" Registering the choosen operators in the toolbox """

# Register the function :func:`deap.tools.cxTwoPoint` under the alias 'mate' with no defailt arguments
toolbox.register('mate', tools.cxTwoPoint)

# Register the function :func:`deap.tools.mutGaussian` under alias 'mutate' with default arguments (mu=0, sigma=1, indpb=0.1)
toolbox.register('mutate', tools.mutGaussian, mu=0, sigma=1, indpb=0.1)

# Register the function :func:`tools.selTournament` under alias 'select' with default argument (tournsize=3)
toolbox.register('select', tools.selTournament, tournsize=3)

# Register the function :func:`evaluate` under the alias evaluate

def evaluate(individual):
	return sum(individual), # Fitness value (tuple) must be iterable

toolbox.register('evaluate', evaluate)


""" Write our own algorithm """
def main():

	# Create a population with 50 individuals where each individual is composed of 10 random floating point numbers
	pop = toolbox.population(n=50)

	crossover_prob = 0.5 # Crossover probability
	mutation_prob = 0.2 # Mutation probability
	n_generations = 40 # Number of generations

	# Evaluate the entire population
	fitnesses = map(toolbox.evaluate, pop)
	for individual, ind_fitness in zip(pop, fitnesses):
		individual.fitness.values = ind_fitness

	# Let the population evolve through generations
	for i_generation in range(n_generations):

		# Select the next generation individual
		offspring = toolbox.select(pop, len(pop))

		# Clone the selected individuals
		offspring = list(map(toolbox.clone, offspring))
	
		# Apply crossover on the offspring
		for child1, child2 in zip(offspring[::2], offspring[1::2]):
			if random.random() < crossover_prob:
				toolbox.mate(child1, child2)
				del child1.fitness.values
				del child2.fitness.values

		# Apply mutation on the offspring
		for mutant in offspring:
			if random.random() < mutation_prob:
				toolbox.mutate(mutant)
				del mutant.fitness.values

		# Evaluate individuals with invalid fitness
		invalid_individuals = [individual for individual in offspring if not individual.fitness.valid]
		fitnesses = map(toolbox.evaluate, invalid_individuals)

		for individual, fitness in zip(invalid_individuals, fitnesses):
			individual.fitness.values = fitness

		# The population is entirely replaced by offspring
		pop[:] = offspring

	return pop

if __name__ == '__main__':

	main()
