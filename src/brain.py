import connection
import node
import pickle
import random


class Brain:

    def __init__(self, inputs, clone=False):
        self.connections = []
        self.nodes = []
        self.inputs = inputs
        self.net = []
        self.layers = 3  # Layer 0: Input/Bias, Layer 1: Hidden, Layer 2: Output

        if not clone:
            # 1. Create input nodes (Layer 0)
            for i in range(0, self.inputs):
                n = node.Node(i)
                n.layer = 0
                self.nodes.append(n)

            # 2. Create single bias node (Layer 0)
            bias_node = node.Node(self.inputs)
            bias_node.layer = 0
            self.nodes.append(bias_node)

            # 3. Create hidden node (Layer 1)
            hidden_node = node.Node(self.inputs + 1)
            hidden_node.layer = 1
            self.nodes.append(hidden_node)

            # 4. Create output node (Layer 2)
            output_node = node.Node(self.inputs + 2)
            output_node.layer = 2
            self.nodes.append(output_node)

            # 5. Connect Input + Bias nodes to Hidden Node
            for i in range(0, self.inputs + 1):
                self.connections.append(
                    connection.Connection(
                        self.nodes[i], hidden_node, random.uniform(-1, 1)
                    )
                )

            # 6. Connect Hidden Node to Output Node
            self.connections.append(
                connection.Connection(
                    hidden_node, output_node, random.uniform(-1, 1)
                )
            )

            # Build the ordered network array
            self.generate_net()

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
        # Set input node values
        for i in range(0, self.inputs):
            self.nodes[i].outputValue = vision[i]

        # Set bias node output (located at index equal to self.inputs)
        self.nodes[self.inputs].outputValue = 1.0

        # Activate all nodes in topological layer order
        for i in range(0, len(self.net)):
            self.net[i].activate()

        # Get output from the output node (the last node in self.nodes)
        outputValue = self.nodes[-1].outputValue

        # Reset accumulated inputs for next frame
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
        clone.generate_net()
        return clone

    def getNode(self, id):
        for n in self.nodes:
            if n.id == id:
                return n
        return None

    def mutate(self):
        if random.uniform(0, 1) < 0.9:
            for i in range(0, len(self.connections)):
                self.connections[i].mutate_weight()

    def save(self, filename="best_brain.pkl"):
        """Saves the current Brain instance to a binary file."""
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename="best_brain.pkl"):
        """Loads and returns a Brain instance from a binary file."""
        with open(filename, "rb") as f:
            return pickle.load(f)