from matrix import matrix
import math
import random

def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def dsigmoid(y):
    return y * (1 - y)

class Neurol_Network():
    def __init__(self,input_nodes,hidden_nodes,output_nodes):
        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes

        self.weights_ih = matrix(self.hidden_nodes,self.input_nodes)
        self.weights_ho = matrix(self.output_nodes,self.hidden_nodes)

        self.bias_h = matrix(self.hidden_nodes,1)
        self.bias_o = matrix(self.output_nodes,1)

        self.learing_rate = 0.15

    def feedfoward(self,input_arr):

        # Generating the hidden output
        input_num = matrix.fromArray(input_arr)
        hidden = matrix.multiply_static(self.weights_ih,input_num)
        
        #print (self.bias_h.data)
        hidden.add(self.bias_h)

        # activation function
        hidden.map(sigmoid)

        # Generating the output
        output = matrix.multiply_static(self.weights_ho,hidden)
        output.add(self.bias_o)
        output.map(sigmoid)
        output = output.toArray()
        # sending back
        return output

    def train(self,inputs,targets):
        # Generating the hidden output
        input_matrix = matrix.fromArray(inputs)
        hidden = matrix.multiply_static(self.weights_ih,input_matrix)
        hidden.add(self.bias_h)

        # activation function
        hidden.map(sigmoid)

        # Generating the output
        outputs = matrix.multiply_static(self.weights_ho,hidden)

        outputs.add(self.bias_o)
        outputs.map(sigmoid)

        targets = matrix.fromArray(targets)
        # Calculate the output layer error
        output_error = matrix.subtract_static(targets,outputs)

        # Calculate gradient
        gradient = matrix.map_static(outputs,dsigmoid)
        gradient.multyply_matrix(output_error)
        gradient.multyply_scalar(self.learing_rate)

        # Calculate deltas
        hidden_T = matrix.transpose_static(hidden)
        weight_ho_deltas = matrix.multiply_static(gradient,hidden_T)

        # adjust the weights by deltas
        self.weights_ho.add(weight_ho_deltas)
        # adjust the bias by deltas(gradient)
        self.bias_o.add(gradient)

        # Calculate the hidden layer error
        who_t = matrix.transpose_static(self.weights_ho)
        hidden_error = matrix.multiply_static(who_t,output_error)

        # Calculate hidden gradient
        hidden_gradient = matrix.map_static(hidden,dsigmoid)
        hidden_gradient.multyply_matrix(hidden_error)
        hidden_gradient.multyply_scalar(self.learing_rate)

        # Calculate input --> hidden deltas
        inputs_T = matrix.transpose_static(input_matrix)
        weight_ih_deltas = matrix.multiply_static(hidden_gradient,inputs_T)

        # adjust the weights by deltas
        self.weights_ih.add(weight_ih_deltas)
        # adjust the bias by deltas(gradient)
        self.bias_h.add(hidden_gradient)


    # Adding for neural evolution
    def copy(self):
        def Copy(val):
            return val

        m = Neurol_Network(self.input_nodes,self.hidden_nodes,self.output_nodes)

        m.weights_ih = matrix.map_static(self.weights_ih,Copy)
        m.weights_ho = matrix.map_static(self.weights_ho,Copy)
        m.bias_h = matrix.map_static(self.bias_h,Copy)
        m.bias_o = matrix.map_static(self.bias_o,Copy)
        m.learing_rate = self.learing_rate
        return m

    def mutate(self,rate):
        def Mutate(val):
            if random.uniform(0,1) < rate:
                return random.uniform(-1,1)

            else:
                return val
        self.weights_ih.map(Mutate)
        self.weights_ho.map(Mutate)
        self.bias_h.map(Mutate)
        self.bias_o.map(Mutate)
