import connection
import node
import random


class Brain:

    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 2

        if not clone:
            # Create input nodes
            for i in range(0, self.inputs):
                self.nodes.append(node.Node(i))
                self.nodes[i].layer = 0
            # Create bias nodeS
            self.nodes.append(node.Node(3))
            self.nodes[3].layer = 1
            self.nodes.append(node.Node(4))
            self.nodes[4].layer = 1
            # Create output node
            self.nodes.append(node.Node(5))
            self.nodes[5].layer = 1

            # Create connection between nodes
            for i in range(0, 4):
                self.connections.append(
                    connection.Connection(
                        self.nodes[i], self.nodes[4], random.uniform(-1, 1)
                    )
                )

    def connect_nodes(self):
        for i in range(0, len(self.nodes)):
            self.nodes[i].connections = []

        for i in range(0, len(self.connections)):
            self.connections[i].fromNode.connections.append(self.connections[i])

    def generate_net(self):
        self.connect_nodes()
        self.net = []
        for i in range(0, self.layers):
            for j in range(0, len(self.nodes)):
                if self.nodes[j].layer == i:
                    self.net.append(self.nodes[j])

    def feed_forward(self, vision):
        for i in range(0, self.inputs):
            self.nodes[i].outputValue = vision[i]

        self.nodes[3].outputValue = 1

        for i in range(0, len(self.net)):
            self.net[i].activate()

        outputValue = self.nodes[4].outputValue

        for i in range(0, len(self.nodes)):
            self.nodes[i].inputValue = 0

        return outputValue

    def clone(self):
        clone = Brain(self.inputs, True)

        for n in self.nodes:
            clone.nodes.append(n.clone())

        for c in self.connections:
            clone.connections.append(
                c.clone(
                    clone.getNode(c.fromNode.id), clone.getNode(c.toNode.id)
                )
            )

        clone.layers = self.layers
        clone.connect_nodes()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n

    def mutate(self):
        if random.uniform(0, 1) < 0.9:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()