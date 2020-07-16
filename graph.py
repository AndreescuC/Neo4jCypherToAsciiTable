class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_edges_for(self, n1, n2):
        return [
            e for e in self.edges
            if (e.from_node == n1 and e.to_node == n2) or (e.to_node == n1 and e.from_node == n2)
        ]


class Node:
    def __init__(self):
        self.labels = []
        self.edges = []
        self.properties = {}

    def add_label(self, label):
        self.labels.append(label)

    def add_property(self, key, value):
        self.properties[key] = value

    def has_label(self, label):
        return label in self.labels


class Edge:
    def __init__(self, name, from_node, to_node):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
