import numpy as np
import json

class Neural_Net(object):
    
    def __init__(self, layers):
        self.layers = layers
   
        # Set random weights initially
        self.weights = [np.random.randn(x, y) for x, y in zip(layers[1:], layers[:-1])]
        self.biases = [np.zeros([x, 1]) for x in layers[1:]]

        # Activation functions
        self.activation = sigmoid
        self.activation_derivative = sigmoid_derivative

        # Cost functions
        self.cost = mse
        self.cost_derivative = mse_derivative


    def feed_forward(self, X):
        a = np.reshape(X, [len(X),-1])
        
        for bias, weight in zip(self.biases, self.weights):
            z = np.dot(weight, a) + bias
            a = self.activation(z)

        # Tranpose on return for readability
        return a.T

    
    def forward_backward_prop(self, x, y, learning_rate):
        zs = [] # Weighted input vector of every layer 
        acts = [] # Output vector of every layer
        ds = [] # Error vector of every layer

        # Reshape x and y to be of the form [n, 1]
        x = np.reshape(x, [len(x),-1])
        y = np.reshape(y, [len(y),-1])

        # Feed forward to get weighted input vector and output vector
        for bias, weight in zip(self.biases, self.weights):
            acts.append(x)

            z = np.dot(weight, x) + bias
            zs.append(z)
            x = self.activation(z)

        # Error in output layer
        delta_L = np.multiply(self.cost_derivative(x, y), self.activation_derivative(zs[-1]))

        ds.append(delta_L)

        # Value of cost function
        #print("error: " + str(np.linalg.norm(self.cost(input, y))))

        # Backprop to get error in previous layers
        for l in range(len(self.layers)-3, -1, -1):
            w_L = np.transpose(self.weights[l+1])
            next_layer = np.dot(w_L, delta_L)

            delta_L = np.multiply(next_layer, self.activation_derivative(zs[l]))

            # Prepend error of the layer
            ds = [delta_L] + ds

        # Updates weights and biases
        self.weights = [w - learning_rate * np.dot(d, np.array(a).T) for w, d, a in zip(self.weights, ds, acts)]
        self.biases = [b - learning_rate * d for b, d in zip(self.biases, ds)]


    def train(self, training_data, learning_rate, epochs, debug=False):
        for i in range(epochs):
            for (x, y) in training_data:
                self.forward_backward_prop(x, y, learning_rate)

            if debug and i % 100 == 0:
                output = self.feed_forward(x)
                print("Epoch " + str(i) + " - Error: " + str(np.linalg.norm(self.cost(output, y))))

   
    def export(self):
        network = {}
        network["nr_inputs"] = self.layers[0]
        network["nr_outputs"] = self.layers[-1]
        network["nr_layers"] = len(self.layers)

        layers = []

        for l in range(len(self.layers) - 1):
            layer = {}
            layer["nr_nodes"] = self.layers[l+1]
            layer["activation_function"] = { "type": "sigmoid" }
            layer["input_weights"] = self.weights[l].tolist()
            layer["input_biases"] = self.biases[l].tolist()

            layers.append(layer)

        network["layers"] = layers 

        return json.dumps(network)
        

# Activation functions
def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return (sigmoid(x) * (1 - sigmoid(x)))

def tanh(x):
    return (np.tanh(x))

def tanh_derivative(x):
    return (1 - np.square(tanh(x)))


# Cost functions
def mse(actual, expected):
    return 0.5 * np.square(actual - expected)

def mse_derivative(actual, expected):
    return (actual - expected)

def cross_entropy(actual, expected):
    return -(expected * np.log(actual) + (1 - expected)*np.log(1 - actual))

def cross_entropy_derivative(actual, expected):
    return (actual - expected) / ((1 - actual)*actual)
