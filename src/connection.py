import random

class Connection:
    def __init__(self, fromNode, toNode, weight):
        self.fromNode = fromNode
        self.toNode = toNode
        self.weight = weight

    def mutate_weight(self):
        if random.uniform(0, 1) < .1:
            self.weight = random.uniform(-1, 1)
        else:
            self.weight += random.gauss(0, 1)/10
            if self.weight > 1:
                self.weight = 1
            if self.weight < -1:
                self.weight = -1

    def clone(self, fromNode, toNode):
        clone = Connection(fromNode, toNode, self.weight)
        return clone