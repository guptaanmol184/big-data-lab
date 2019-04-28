""" Simple Neural Network Library
Creating and Training Neural Networks using Backpropogation Algorithm

Author: R Mukesh <reghu.mukesh@gmail.com>
		IIITDM Kancheepuram

References
----------
1. Data Mining: Concepts and Techniques (Jiawei Han and Micheline Kamber)
   [ Section 6.6: Classification by Backpropogation ]

2. Interface design inspired by Synaptic.js library
   [ https://github.com/cazala/synaptic/wiki/Networks#propagate ]

Notes
-----
This code requires python 3.6+, since it uses 'f-Strings' for string formatting.
"""

import numpy as np


class Neuron:
	""" Class representing a neuron with logistic sigmoid activation function """

	def __init__(self, n_inputs=None, weights=None):
		""" Creates a neuron with numbers of inputs as specified by either parameters ``n_inputs`` or ``weights``
		
		Parameters
		----------
		n_inputs : int (default None, which implies infer from parameter ``weights``)
			Number of inputs to neuron
		weights : :obj:`numpy.ndarray` of numbers
			Initial weights (to inputs and bias) of neuron
		"""

		if (n_inputs is None) and (weights is None):
			raise Exception("Either parameter 'n_inputs' or 'weights' must be specified")

		if n_inputs is not None:
			if n_inputs <= 0:
				raise Exception("Number of inputs to a layer must be positive")
			elif (weights is not None) and (n_inputs != len(weights)-1):
				raise Exception(f"Number of inputs specified in parameter 'n_inputs' ({n_inputs}) and 'weights' ({len(weights)}) don't match")

		if weights is not None:
			self.weights = weights
			self.n_inputs = len(self.weights)-1

		elif n_inputs:
			self.n_inputs = n_inputs
			self.weights = np.random.rand(n_inputs+1)


class Layer:
	""" Class representing a layer in a Multi-Layer Feed Forward Neural Network """

	def __init__(self, n_neurons, n_inputs):
		""" Create a fully-connected layer with ``n_neurons`` neurons each connected to ``n_inputs`` inputs 

		Parameters
		----------
		n_neurons : int
			Number of neurons in the layer
		n_inputs : int
			Number of inputs to each neuron in the layer (excluding bias term)
		"""

		if n_neurons <= 0:
			raise Exception("Number of neurons in a layer must be positive")

		if n_inputs <= 0:
			raise Exception("Number of inputs to a layer must be positive")

		self.n_neurons = n_neurons
		self.n_inputs = n_inputs

		self.weights = np.random.rand(n_neurons, n_inputs+1)

		# Alternative way of accessing and interactive with neuron weights
		self.neurons = []
		for i_neuron in range(n_neurons):
			neuron = Neuron(weights=self.weights[i_neuron])
			self.neurons.append(neuron)

		
	def activate(self, input):
		""" Activates the layer with given input ``input`` and computes output 
		
		Parameters
		----------
		input : 1-D array_like
			Inputs to the neurons in the layer

		Returns
		-------
		1-D :obj:`numpy.ndarray` of numbers
			Outputs from the neurons in the layer
		"""

		if len(input) != self.n_inputs:
			raise Exception(f"Number of inputs given ({len(input)}) doesn't match specified value ({self.n_inputs}) for layer")

		input = np.append(input, 1)
		net_input = self.weights.dot(input)
		output = 1/(1 + np.exp(-net_input)) # Apply logisitic sigmoid on 'net_inputs'

		# store the output for the most recent activation of the layer
		self.output = output

		return output


class NeuralNetwork:
	""" Class representing Multi-Layer Feed Forward Neural Network """

	def __init__(self, *n_nodes):
		""" Creates a neural network with neuron counts in each layer as specified by parameter ``n_nodes``

		Parameters
		----------
		n_nodes : :obj:`list` of :obj:`int`
			Specifies the number of nodes in input layer, hidden layers and output layer in sequence
		"""

		if len(n_nodes) < 3:
			raise Exception("Neural network must have minimum 3 layers: Input, Hidden and Output")

		if any(n_node <= 0 for n_node in n_nodes):
			raise Exception("Number of nodes in any layer must be positive")

		# Input Layer
		self.n_inputs = n_nodes[0]
		self.n_outputs = n_nodes[-1]

		# Neural Network Layers
		self.layers = []
		for n_inputs, n_neurons in zip(n_nodes, n_nodes[1:]):
			layer = Layer(n_neurons, n_inputs)
			self.layers.append(layer)


	def activate(self, input):
		""" Activates the neural network with given input ``input`` and compute output 

		Parameters
		----------
		input : 1-D array_like
			Inputs to the neural network

		Returns
		-------
		:obj:`numpy.ndarray` of numbers
			Outputs from the neural network
		"""

		if len(input) != self.n_inputs:
			raise Exception(f"Number of inputs given ({len(input)}) doesn't match specified value ({self.n_inputs}) for network")

		layer_input = input

		for layer in self.layers:
			layer_output = layer.activate(layer_input)
			# output of current layer is input for next layer
			layer_input = layer_output

		# store the input, output for the most recent activation of the network
		self.input = np.array(input)
		self.output = layer_output

		return layer_output


	def propagate(self, learning_rate, target):
		""" Backpropogate errors and adjust weights for most recent activation of neural network 

		Parameters
		----------
		learning_rate : float
			Learning rate for back propogation algorithm

		target : 1-D array_like
			Target value for most recent input to neural network
		"""

		if not hasattr(self, 'output'):
			raise Exception("Activate neural network with a training sample before calling 'propogate'")

		if len(target) != self.n_outputs:
			raise Exception(f"Number of outputs given ({len(target)}) doesn't match specified value ({self.n_outputs}) for network")

		# Compute the error for the output layer
		output_layer = self.layers[-1]
		output_layer.error = self.output * (1 - self.output) * (target - self.output)

		# Compute the error for hidden layers, from last to first
		for hidden_layer, next_higher_layer in zip(self.layers[-2::-1], self.layers[-1:0:-1]):
			hidden_layer.error = hidden_layer.output * (1 - hidden_layer.output) * (next_higher_layer.weights.T[:-1].dot(next_higher_layer.error))

		# Update the weights for first hidden layer
		first_hidden_layer = self.layers[0]
		first_hidden_layer_delta_weights = learning_rate * first_hidden_layer.error.reshape((-1,1)).dot(self.input.reshape(1, -1))
		first_hidden_layer.weights[:, :-1] += first_hidden_layer_delta_weights

		# Update the weights for all the other hidden layers
		for hidden_layer, previous_lower_layer in zip(self.layers[1:], self.layers):
			hidden_layer_delta_weights = learning_rate * hidden_layer.error.reshape((-1,1)).dot(previous_lower_layer.output.reshape(1, -1))
			hidden_layer.weights[:, :-1] += hidden_layer_delta_weights

		# Update the weights for all layers in the network
		for layer in self.layers:
			layer_delta_bias = learning_rate*layer.error
			layer.weights[:, -1] += layer_delta_bias

		# Delete the temporary attributes 'output' and 'error' from each layer
		for layer in self.layers:
			del layer.output
			del layer.error

		del self.input, self.output


if __name__ == '__main__':
	""" Train an neural network for learning XOR function """

	neural_network = NeuralNetwork(2, 3, 1)

	learning_rate = 0.3
	n_iterations = 20000

	for i_iteration in range(n_iterations):

		# 0,0 => 0
		neural_network.activate([0,0])
		neural_network.propagate(learning_rate, [0])

		# 0,1 => 1
		neural_network.activate([0,1])
		neural_network.propagate(learning_rate, [1])

		# 1,0 => 1
		neural_network.activate([1,0])
		neural_network.propagate(learning_rate, [1])

		# 1,1 => 0
		neural_network.activate([1,1])
		neural_network.propagate(learning_rate, [0])

	# test the XOR neural network
	print("Output of neural network trained for XOR function")

	input = [0, 0]
	print(f"input: {input}, output:{neural_network.activate(input)}")

	input = [0, 1]
	print(f"input: {input}, output:{neural_network.activate(input)}")

	input = [1, 0]
	print(f"input: {input}, output:{neural_network.activate(input)}")

	input = [1, 1]
	print(f"input: {input}, output:{neural_network.activate(input)}")