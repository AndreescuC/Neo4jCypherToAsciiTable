class Graph:
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_node_by_name(self, name):
        return [n for n in self.nodes if n.name == name][0]

    def get_edges_for(self, n1, n2):
        return [
            e for e in self.edges
            if (e.from_node == n1.name and e.to_node == n2.name) or
               (e.to_node == n1.name and e.from_node == n2.name)
        ]

    def get_related_nodes_for(self, node):
        nodes = []
        for e in self.edges:
            if e.to_node == node.name:
                nodes.append(e.from_node)
            if e.from_node == node.name:
                nodes.append(e.to_node)

        return nodes

    def get_labeled_related_nodes_for(self, node, labels):
        return [n for n in self.get_related_nodes_for(node) if len(set(self.get_node_by_name(n).labels) & set(labels)) > 0]

    def __str__(self):
        return f"Graph with {len(self.nodes)} nodes and {len(self.edges)} edges:\n" \
               f"N: {self.nodes.__str__()}\n" \
               f"E: {self.edges.__str__()}\n"

    def __repr__(self):
        return self.__str__()


class Node:
    def __init__(self, name, labels, properties):
        self.name = name
        self.labels = labels
        self.properties = properties

    def add_label(self, label):
        self.labels.append(label)

    def add_property(self, key, value):
        self.properties[key] = value

    def has_label(self, label):
        return label in self.labels

    def __str__(self):
        return f"<{self.name}|{self.labels}|{self.properties}>"

    def __repr__(self):
        return self.__str__()


class Edge:
    def __init__(self, name, from_node, to_node, identifier=None):
        self.name = name
        self.from_node = from_node
        self.to_node = to_node
        self.identifier = identifier

    def __str__(self):
        return f"[{self.from_node}-{self.name}->{self.to_node}]"

    def __repr__(self):
        return self.__str__()
