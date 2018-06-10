import sys, random , csv
from sys import argv
import numpy as np
import pandas as pd
def sigmoid(net):
    return 1.0 / (1.0 + np.exp(-net))

class Neuron:
    def __init__(self, no_inputs=0,inputs = []):
        self.number_of_inputs = no_inputs
        self.all_the_inputs = inputs
        self.neuron_weights = []
        self.neuron_weights_diff = []
        self.error_obtained = 0.0
        self.output = 0.0
        self.weight_delta = 0.0
        for i in range((no_inputs + 1)):
            self.weights += [random.uniform(0, 1)]
            self.weights_diff += [0]
        self.net = self.weights[0]
    def net_id(self,inputs):
        self.net = self.weights[0]
        for i in range(len(inputs)):
            self.net +=   self.weights[i + 1] * inputs[i]
        self.output = sigmoid(self.net)
        self.inputs = inputs
        return self.output

class NeuralLayer:
    def __init__(self, no_neurons=None, no_inputs= 0, inputs= None):
        self.number_of_neurons = no_neurons
        self.number_of_inputs = no_inputs
        self.neurons = []
        self.inputs = inputs
        self.net = 0.0
        self.output = []
        self.target = [0,1]
        for i in range(no_neurons):
            self.neurons += [Neuron(no_inputs=no_inputs)]
        for i in self.neurons:
            self.output += [i.output]

class NeuralNetwork:
    def __init__(self, no_inputs=None, no_outputs=None, no_hidden_layers=0, no_neurons_list= [],input_data = []):
        self.number_of_inputs = no_inputs
        self.number_of_outputs = no_outputs
        self.number_of_hiddenlayers = no_hidden_layers
        self.num_of_neuronslist = no_neurons_list
        self.input_data = input_data
        self.build_network()

    def build_network(self):
        if self.no_hidden_layers > 0:
            self.layers = [NeuralLayer(no_neurons= self.no_neurons_list[0], no_inputs= self.no_inputs)]
            if self.no_hidden_layers > 1:
                for i in range((self.no_hidden_layers - 1)):
                    self.layers += [NeuralLayer(no_neurons= self.no_neurons_list[i + 1], no_inputs= self.no_neurons_list[i])]
            self.layers += [NeuralLayer(no_neurons= self.no_outputs, no_inputs= self.no_neurons_list[-1])]
        else:
            self.layers = [NeuralLayer(no_neurons = self.no_outputs, no_inputs= self.no_inputs)]

def print_weights(NN):

    for i,layer in enumerate(NN.layers):

        if (i + 1) != (len(NN.layers)):
            print ("Hidden_layer___", i + 1, " : ")
            for j,neuron in enumerate(layer.neurons):
                print ("\tNeuron__",j+1,"__weights are :",neuron.weights)

    print ("Output Layer_____ : ")
    for k,neuron in enumerate(NN.layers[-1].neurons):
        print ("\tNeuron___", k+1, "__weights are :", neuron.weights)

def forward_feed(NN,input_data):
    input = input_data
    for layer in NN.layers:
        output = []
        layer.inputs = input
        for neuron in layer.neurons:
            output += [neuron.net_id(input)]
        layer.output = output
        input = output

def backward_propagation(NN,target_value,n):


    #output layer
    for i,neuron in enumerate(NN.layers[-1].neurons):
        neuron.delta = neuron.output * (1 - neuron.output) * (target_value[i] - neuron.output)

    for i in range((len(NN.layers) - 2) , -1,-1):
        for j, neuron in enumerate(NN.layers[i].neurons):
            sigma1 = 0.0
            for neuron1 in NN.layers[i+1].neurons:
                sigma1 += neuron1.delta * neuron1.weights[j+1]
            neuron.delta = neuron.output * (1 - neuron.output) * sigma1
    learning_rate = 0.3
    alpha = 0.9
    for i,neuron in enumerate(NN.layers[-1].neurons):
        # bias weight update
        diff = learning_rate * neuron.delta + alpha  * neuron.weights_diff[0]
        #print " this is :",alpha * (n - 1) * neuron.weights_diff[0]
        neuron.weights[0] += diff
        neuron.weights_diff[0] = diff
        #print NN.layers[-1].inputs,"here"
        for j in range(1, (len(neuron.weights))):
            diff = learning_rate * neuron.delta  * NN.layers[-1].inputs[j - 1] + alpha  * neuron.weights_diff[j]
            neuron.weights[j] += diff
            neuron.weights_diff[j] = diff

    #hidden layers
    for i in range((len(NN.layers) - 2), -1, -1):
        inputs = NN.layers[i].inputs
        for j, neuron in enumerate(NN.layers[i].neurons):
            diff = learning_rate * neuron.delta + alpha *  neuron.weights_diff[0]
            neuron.weights[0] += diff
            neuron.weights_diff[0] = diff
            for k in range(1, (len(neuron.weights))):
                #print " k is :",k,"and length is ",len(neuron.weights)
                diff = learning_rate * neuron.delta * NN.layers[i].inputs[k - 1] + alpha  * neuron.weights_diff[k]
                neuron.weights[k] += diff
                neuron.weights_diff[k] = diff
                # print i,' - Hiddden layer deltas :',NN.layers[i].deltas



def main():
    #---------------------------------
    input_cases = []
    df = pd.read_csv(argv[1], engine='python')
    attributes =  df.columns.values
    #print attributes
    output_attributes = []
    input_attributes = []
    for a in attributes:
        if('Output' in a):
            output_attributes += [a]
        else:
            input_attributes += [a]
    #print input_attributes
    #print output_attributes
    percent = float(argv[2]) * 0.01
    data_train = df.sample( frac = percent)
    data_test = df.loc[~df.index.isin(data_train.index)]

    outputs_train = data_train[output_attributes]
    inputs_train = data_train[input_attributes]

    outputs_test = data_test[output_attributes]
    inputs_test = data_test[input_attributes]


    input_train_list = inputs_train.values.tolist()
    output_train_list = outputs_train.values.tolist()

    input_test_list = inputs_test.values.tolist()
    output_test_list = outputs_test.values.tolist()
    #----------------------------------
    no_hidden_layers = int(argv[4])
    no_neurons_list = []
    for i in range(no_hidden_layers):
        no_neurons_list += [int(argv[i + 5])]
    #-------------------------------------------

    NN = NeuralNetwork(no_inputs = len(input_train_list[0]), no_outputs= len(output_train_list[0]), no_hidden_layers = no_hidden_layers,no_neurons_list = no_neurons_list,input_data = input_train_list[0])
    #print "-------------------------------------------------------"
    factor = 0.2
    j = 1
    Total_Error = 0.0
    Iter = 500
    n = 0
    c = 0
    while(j <= Iter):

        j = j  + 1
        Total_Error = 0.0
        for i in range(len(input_train_list)):
            c = c+ 1
            #print "iteration is :",c
            sum = 0.0
            n = n+ 1
            forward_feed(NN,input_train_list[i])
            #print_weights(NN)
            #print "Actual : ",output_train_list[i]
            for k in range(len(output_train_list[i])):
                sum = sum + factor * ((output_train_list[i][k] - NN.layers[-1].output[k])**2)
            sum = sum/(len(output_train_list[i]))
            Total_Error += sum
            backward_propagation(NN, output_train_list[i],n)
        Error = Total_Error/float((len(input_train_list) ))
        if (Error <= float(argv[3]) ):
            break
    print_weights(NN)
    print ("Total Training Error observed is:",Total_Error/(len(input_train_list)))
    Error_Test  =  0.0
    for i in range(len(input_test_list)):
        forward_feed(NN, input_test_list[i])
        for k in range(len(output_test_list[i])):
            sum = sum + factor * ((output_test_list[i][k] - NN.layers[-1].output[k])**2)
        sum = sum/(len(output_test_list[i] ) )
        Total_Error += sum
        Error_Test = Total_Error/(len(input_test_list) )
    print ("Total Testing Error observed is :", Error_Test)
if __name__ == "__main__":
    main()