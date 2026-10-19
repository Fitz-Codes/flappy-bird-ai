import math

class Node:
    def __init__(self, idNumber):
        self.id = idNumber
        self.layer = 0
        self.inputValue = 0
        self.outputValue = 0
        self.connections = []

    def activate(self):
        def sigmoid(x):
            return 1/(1+math.exp(-x))

        if self.layer == 1:
            self.outputValue = sigmoid(self.inputValue)

        for i in range(0, len(self.connections)):
            self.connections[i].toNode.inputValue += self.connections[i].weight * self.outputValue
            